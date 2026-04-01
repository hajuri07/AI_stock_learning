

import numpy as np
import pandas as pd
import yfinance as yf
import ta
import json
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from groq import Groq

# ── Constants ──────────────────────────────────────────────
LSTM_LOOKBACK = 10
LSTM_EPOCHS   = 100

# Dict format so app.py can show clean names in dropdown
COMPANIES = {
    "RELIANCE  ·  Reliance Industries":   "RELIANCE.NS",
    "TCS       ·  Tata Consultancy Svcs": "TCS.NS",
    "INFY      ·  Infosys":               "INFY.NS",
    "HDFCBANK  ·  HDFC Bank":             "HDFCBANK.NS",
    "ICICIBANK ·  ICICI Bank":            "ICICIBANK.NS",
    "ITC       ·  ITC Limited":           "ITC.NS",
    "LT        ·  Larsen & Toubro":       "LT.NS",
    "AIRTEL    ·  Bharti Airtel":         "BHARTIARTL.NS",
    "SBIN      ·  State Bank of India":   "SBIN.NS",
}


# ── Step 1: Fetch Data ──────────────────────────────────────
def fetch_data(symbol: str, period: str = "6mo") -> pd.DataFrame:
    stock = yf.Ticker(symbol)
    hist  = stock.history(period=period)
    if hist.empty:
        raise ValueError(f"No data returned for symbol: {symbol}")
    hist["Symbol"] = symbol
    hist = hist[["Open", "High", "Low", "Close", "Volume", "Symbol"]]
    return hist


# ── Step 2: Add Technical Indicators ───────────────────────
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['RSI']         = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    macd              = ta.trend.MACD(df['Close'])
    df['MACD']        = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    df['MACD_hist']   = macd.macd_diff()
    bb                = ta.volatility.BollingerBands(df['Close'], window=20)
    df['BB_high']     = bb.bollinger_hband()
    df['BB_low']      = bb.bollinger_lband()
    df['BB_mid']      = bb.bollinger_mavg()
    df['EMA_20']      = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    df['ATR']         = ta.volatility.AverageTrueRange(
                            df['High'], df['Low'], df['Close']
                        ).average_true_range()
    df.dropna(inplace=True)
    return df


# ── Step 3: Train LSTM ──────────────────────────────────────
def trainLSTM(prices, lookback=LSTM_LOOKBACK, epochs=LSTM_EPOCHS):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices.reshape(-1, 1))
    x, y   = [], []
    for i in range(lookback, len(scaled)):
        x.append(scaled[i - lookback:i, 0])
        y.append(scaled[i, 0])
    x = np.array(x).reshape(-1, lookback, 1)
    y = np.array(y)

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(lookback, 1)),
        Dropout(0.2),
        LSTM(64),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(x, y, epochs=epochs, batch_size=15, verbose=0)

    last_seq    = scaled[-lookback:].reshape(1, lookback, 1)
    pred_scaled = model.predict(last_seq, verbose=0)[0][0]
    return float(scaler.inverse_transform([[pred_scaled]])[0][0])


# ── Step 4: LLM Explanation ────────────────────────────────
def get_llm_explanation(groq_api_key, symbol, current_price,
                         lstm_price, change_pct, trend, rsi, macd):
    if not groq_api_key or groq_api_key.strip() == "":
        return "⚠️ No Groq API key provided. Enter your key in the sidebar to enable AI explanations."
    try:
        client = Groq(api_key=groq_api_key.strip())
        prompt = f"""
You are a friendly and genius financial advisor explaining stocks to a beginner student.
Tell him like you are the only person in the world who can explain this easily and
take him from beginner to advanced level.

Company: {symbol}
Current Price: ₹{current_price}
LSTM Predicted Price: ₹{lstm_price}
Expected Change: {change_pct}%
Trend: {trend}
RSI (momentum): {rsi:.1f} — above 70 means overbought, below 30 means oversold
MACD: {macd:.2f} — positive means bullish momentum

Explain this in 4-5 simple sentences a student with zero finance knowledge can understand.
Mention what RSI and MACD are telling us in simple words.
Be friendly, confident, and encouraging. No complex jargon.
"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ LLM call failed: {str(e)}"


# ── Step 5: Predict ─────────────────────────────────────────
def predict(symbol, data, groq_api_key=""):
    stock_data = data[data["Symbol"] == symbol].copy()
    stock_data = add_indicators(stock_data)

    prices        = stock_data["Close"].values
    current_price = prices[-1]

    lstm_price = trainLSTM(prices, lookback=LSTM_LOOKBACK, epochs=LSTM_EPOCHS)
    if lstm_price is None:
        lstm_price = current_price

    predicted_price = lstm_price
    change_pct      = ((predicted_price - current_price) / current_price) * 100

    if change_pct > 0.3:
        trend = "Upward 📈"
    elif change_pct < -0.3:
        trend = "Downward 📉"
    else:
        trend = "Stable ➡️"

    rsi  = stock_data["RSI"].iloc[-1]
    macd = stock_data["MACD"].iloc[-1]

    explanation = get_llm_explanation(
        groq_api_key=groq_api_key,
        symbol=symbol,
        current_price=round(float(current_price), 2),
        lstm_price=round(float(lstm_price), 2),
        change_pct=round(float(change_pct), 2),
        trend=trend,
        rsi=rsi,
        macd=macd
    )

    return {
        "symbol":          symbol,
        "current_price":   round(float(current_price), 2),
        "predicted_price": round(float(predicted_price), 2),
        "change_percent":  round(float(change_pct), 2),
        "trend":           trend,
        "rsi":             round(float(rsi), 2),
        "macd":            round(float(macd), 2),
        "atr":             round(float(stock_data["ATR"].iloc[-1]), 2),
        "volume":          float(stock_data["Volume"].iloc[-1]),
        "rsi_status":      "OVERBOUGHT" if rsi > 70 else "OVERSOLD" if rsi < 30 else "NEUTRAL",
        "macd_status":     "BULLISH" if macd > 0 else "BEARISH",
        "AI_explanation":  explanation,
        "df":              stock_data,   # full df for charts in app.py
    }


# ── Step 6: Full pipeline (called by app.py) ────────────────
def run_prediction(symbol: str, period: str, groq_api_key: str, log_callback=None):
    """
    This is what app.py calls.
    Matches the import: from predictor import COMPANIES, run_prediction
    """
    import time

    def log(tag, cls, msg):
        if log_callback:
            log_callback(tag, cls, msg)

    log("INIT",  "tag-run", f"Session started · target={symbol} · window={period}")
    time.sleep(0.15)

    log("FETCH", "tag-run", f"Connecting to Yahoo Finance · {symbol}")
    data = fetch_data(symbol, period)
    log("FETCH", "tag-ok",  f"Received {len(data)} rows · {data.index[0].date()} → {data.index[-1].date()}")

    log("CALC",  "tag-run", "Computing RSI · MACD · BB · EMA · ATR")

    log("LSTM",  "tag-run", f"Training · 2×LSTM(64) + Dropout + Dense · epochs={LSTM_EPOCHS}")
    result = predict(symbol, data, groq_api_key)
    log("LSTM",  "tag-ok",  f"Prediction → ₹{result['predicted_price']}")

    log("LLM",   "tag-ai",  "Sending context to Groq · LLaMA-3.3-70B")
    if "⚠️" in result["AI_explanation"]:
        log("LLM", "tag-warn", result["AI_explanation"][:80])
    else:
        log("LLM", "tag-ok", "AI explanation generated successfully")

    log("DONE",  "tag-ok",  "All steps complete · rendering dashboard ↓")

    # rename key so app.py can access it as result["explanation"]
    result["explanation"] = result.pop("AI_explanation")
    return result
