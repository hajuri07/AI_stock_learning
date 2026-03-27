from google.colab import userdata
userdata.get('GROQ_API_KEY')

# Commented out IPython magic to ensure Python compatibility.
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
# %pip install Groq
from groq import Groq

companies = [
"RELIANCE.NS",
"TCS.NS",
"INFY.NS",
"HDFCBANK.NS",
"ICICIBANK.NS",

"ITC.NS",
"LT.NS",
"BHARTIARTL.NS",
"SBIN.NS"
]

def fetch_data():

    all_data = []

    for symbol in companies:

        stock = yf.Ticker(symbol)

        hist = stock.history(period="6mo")

        hist["Symbol"] = symbol

        hist=hist[["Open","High","Low","Close","Volume","Symbol"]]

        all_data.append(hist)

    data = pd.concat([df for df in all_data if not df.empty])

    return data

data = fetch_data()

def predict(symbol,data):

  stock_data=data[data["Symbol"]==symbol]
  prices=stock_data["Close"].values.reshape(-1,1)
  x,y_price=[],[]

  for i in range(5,len(prices)):
    x.append(prices[i-5:i,0])
    y_price.append(prices[i,0])

  x = np.array(x)
  y_price = np.array(y_price)


  model=LinearRegression()
  model.fit(x,y_price)
  last_5 = prices[-5:].reshape(1, -1)
  predicted_price = model.predict(last_5)[0]
  current_price = prices[-1,0]

        # determine trend
  change_pct = ((predicted_price - current_price) / current_price) * 100

  if change_pct > 0.3:
    trend = "Upward 📈"
  elif change_pct < -0.3:
            trend = "Downward 📉"
  else:
    trend = "Stable ➡️"
  explanation = get_llm_explanation(
          symbol=symbol,
          current_price=round(float(current_price), 2),
          predicted_price=round(float(predicted_price), 2),
          change_pct=round(float(change_pct), 2),
          trend=trend
)
  return {
              "symbol": symbol, # Added symbol to the returned dictionary
              "current_price": round(float(current_price), 2),
              "predicted_price": round(float(predicted_price), 2),
              "change_percent": round(float(change_pct), 2),
              "trend": trend,
              "AI_explanation": explanation

          }

client = Groq(api_key="")

def get_llm_explanation(symbol,current_price,predicted_price,change_pct,trend):
  prompt=f"""
    You are a friendly financial advisor explaining stocks to a beginner student.

    Company: {symbol}
    Current Price: ₹{current_price}
    Predicted Price Tomorrow: ₹{predicted_price}
    Expected Change: {change_pct}%
    Trend: {trend}
    Imagine You are genius about finance and you have to
    Explain this in 3-4 simple sentences that a student with in a way that a student/person with
    zero finance knowledge can understand.
    Be friendly, simple, and encouraging.
    be very confident and intelligent
    and also tell why you are saying that there is somechange and all

    Don't use complex financial jargon.
    """
  response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]

    )
  return response.choices[0].message.content

df = fetch_data()
result = predict("ICICIBANK.NS", df)

print(f"Symbol: {result['symbol']}")
print(f"Current Price: ₹{result['current_price']}")
print(f"Predicted Price: ₹{result['predicted_price']}")
print(f"Change: {result['change_percent']}% ")
print(f"Trend: {result['trend']}")
print(f"\nAI Explanation:")
print(result['AI_explanation'])
