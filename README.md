# 📈 StockSense AI
**Stock Market Analyzer using LSTM + Groq LLaMA 3.3 + Streamlit**

![Language](https://img.shields.io/badge/Language-Python-blue?style=flat-square) ![ML](https://img.shields.io/badge/Model-LSTM-green?style=flat-square) ![LLM](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3-orange?style=flat-square) ![UI](https://img.shields.io/badge/UI-Streamlit-red?style=flat-square)

---

## 1. Project Overview

StockSense AI is a real-time stock market analyzer for **NSE Indian stocks** built using Python. It fetches live market data, computes technical indicators, trains an LSTM model to predict the next day's price, and uses **Groq LLaMA 3.3** to explain everything in plain English — even for someone with zero finance knowledge.

> No paid APIs. No subscriptions. Just a free Groq key and you're good to go.

---

## 2. Features

| Feature | What it Does |
|---|---|
| **Live Data** | Fetches real-time OHLCV data from Yahoo Finance via `yfinance` |
| **Technical Indicators** | RSI, MACD, Bollinger Bands, EMA(20), ATR — all computed automatically |
| **LSTM Prediction** | Trains a 2-layer LSTM model and predicts next day's closing price |
| **AI Explanation** | Groq LLaMA 3.3 explains the prediction in simple language |
| **Interactive Charts** | Candlestick, price forecast, volume, ATR — all with dark terminal UI |
| **Your API Key** | You paste your own Groq key in the sidebar — nothing is hardcoded |

---

## 3. Project Structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI — all charts, layout, sidebar, metric cards |
| `predictor.py` | All ML logic — data fetching, indicators, LSTM, LLM call |
| `requirements.txt` | All dependencies for deployment |

---

## 4. Supported Stocks

| Symbol | Company |
|---|---|
| `RELIANCE.NS` | Reliance Industries |
| `TCS.NS` | Tata Consultancy Services |
| `INFY.NS` | Infosys |
| `HDFCBANK.NS` | HDFC Bank |
| `ICICIBANK.NS` | ICICI Bank |
| `ITC.NS` | ITC Limited |
| `LT.NS` | Larsen & Toubro |
| `BHARTIARTL.NS` | Bharti Airtel |
| `SBIN.NS` | State Bank of India |

---

## 5. Technical Indicators Used

| Indicator | What it Tells Us |
|---|---|
| **RSI (14)** | Momentum — above 70 = overbought, below 30 = oversold |
| **MACD** | Trend direction — positive = bullish, negative = bearish |
| **Bollinger Bands (20)** | Volatility range — price bounces between upper and lower bands |
| **EMA (20)** | Smoothed trend baseline — 20-day exponential moving average |
| **ATR (14)** | Average True Range — measures how much the price moves daily |

---

## 6. LSTM Model Architecture

```
Input → LSTM(64, return_sequences=True) → Dropout(0.2)
      → LSTM(64) → Dropout(0.2) → Dense(1) → Predicted Price
```

- **Lookback window:** 10 days
- **Epochs:** 100 (with early stopping)
- **Batch size:** 15
- **Optimizer:** Adam
- **Loss:** MSE
- **Normalization:** MinMaxScaler — scaled to 0–1 before training, denormalized after prediction

---

## 7. How to Run Locally

**Requirements**
- Python 3.9+
- Free Groq API key from [console.groq.com](https://console.groq.com)

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Run**
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser, paste your Groq key in the sidebar, select a stock and hit **Execute Analysis**.

---

## 8. Deploy on Streamlit Cloud (Free)

1. Push all 3 files to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub and select the repo
4. Set `app.py` as the entry point
5. Done — live public URL in minutes

---

## 9. Run on Google Colab

```python
!pip install streamlit pyngrok

from pyngrok import ngrok
!streamlit run app.py &
url = ngrok.connect(8501)
print(url)
```

Opens a public URL — no local machine needed.

---

## 10. Sample Output

```
=== StockSense AI ===
FETCH  | Received 124 rows · 2024-10-01 → 2025-04-01
CALC   | RSI · MACD · BB · EMA · ATR ready
LSTM   | Training complete · Prediction → ₹1423.50
LLM    | AI explanation generated successfully
DONE   | Dashboard rendered ↓

--- Results ---
Symbol:         ICICIBANK.NS
Current Price:  ₹1401.20
Predicted:      ₹1423.50
Change:         +1.59%
Trend:          Upward 📈
RSI:            58.3  → NEUTRAL
MACD:           4.21  → BULLISH
```

---

## 11. Summary

- ✅ Fetches real-time NSE stock data via yFinance
- ✅ Computes 5 technical indicators automatically
- ✅ Trains LSTM from scratch on live price history
- ✅ Predicts next day closing price
- ✅ Groq LLaMA 3.3 explains results in plain English
- ✅ Bloomberg-style dark terminal UI built with Streamlit
- ✅ User provides their own Groq key — nothing hardcoded
- ✅ Free to deploy on Streamlit Cloud

---

*StockSense AI — Not financial advice · Educational use only*
