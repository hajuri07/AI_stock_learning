📈 AI Stock Predictor & Analyst

An intelligent AI-powered stock prediction and analysis system that forecasts stock prices using Machine Learning and provides natural language explanations using a Large Language Model (LLM).

This project combines financial data analysis, machine learning, and generative AI to create an automated AI financial analyst that predicts stock trends and explains market behavior.

🚀 Features
📊 Stock Price Prediction
Uses historical stock market data
Implements a sliding window time-series prediction approach
Predicts future stock price movement
📉 Trend Classification

Based on predicted price change, the system classifies the market trend as:

📈 Upward
📉 Downward
➡️ Stable
🧠 AI Explanation Engine

The predicted results are passed to a Large Language Model which generates a human-like explanation of the stock trend.

Example output:

Stock: ICICI Bank
Current Price: ₹2137
Predicted Price: ₹2133
Trend: Stable

Explanation:
The predicted price shows only a minor change from the current price,
indicating a relatively stable market condition. This suggests that
recent trading activity does not show strong bullish or bearish momentum.
🏗️ System Architecture
        +---------------------+
        |  Stock Market Data  |
        |    (Yahoo Finance)  |
        +----------+----------+
                   |
                   v
        +---------------------+
        | Data Preprocessing  |
        |  Feature Selection  |
        +----------+----------+
                   |
                   v
        +---------------------+
        |  ML Prediction      |
        | Sliding Window      |
        | Time Series Model   |
        +----------+----------+
                   |
                   v
        +---------------------+
        | Trend Detection     |
        | Up / Down / Stable  |
        +----------+----------+
                   |
                   v
        +---------------------+
        | LLM Explanation     |
        | (Groq API)          |
        | llama-3.3-70b       |
        +----------+----------+
                   |
                   v
        +---------------------+
        | Final AI Analysis   |
        +---------------------+
🧠 AI Model Used
Large Language Model

The explanation engine uses:

Model: llama-3.3-70b-versatile
Provider: Groq

Why this model?

High-quality reasoning
Fast inference using Groq
Excellent natural language explanations
Ideal for analytical tasks like financial interpretation

The model analyzes:

Current stock price
Predicted stock price
Percentage change
Market trend

And produces a human-readable explanation.

📊 Data Source

Stock data is fetched using:

Yahoo Finance API

Library used:

yfinance

Data includes:

Open price
High price
Low price
Close price
Volume

Example companies used:

RELIANCE
TCS
INFY
HDFCBANK
ICICIBANK
TATAMOTORS
ITC
LT
BHARTIARTL
SBIN
⚙️ Machine Learning Approach
Sliding Window Time Series Prediction

The model uses a 5-day sliding window to predict the next price.

Example:

Day1 Day2 Day3 Day4 Day5 → Predict Day6

Training samples look like:

[2140, 2139, 2138, 2136, 2137] → 2133

This allows the model to learn short-term price patterns.

📉 Trend Classification Logic

The predicted trend is calculated using percentage change:

change % = (predicted_price - current_price) / current_price * 100

Trend thresholds:

> +1%  → Upward 📈
< -1%  → Downward 📉
Else   → Stable ➡️

This helps filter normal market noise.

🛠️ Tech Stack
Programming Language
Python
Libraries
NumPy
Pandas
yfinance
Scikit-learn
AI / LLM
Groq API
llama-3.3-70b-versatile
Data Handling
Pandas DataFrames
Time-series preprocessing
📦 Installation

Clone the repository:

git clone https://github.com/yourusername/ai-stock-analyst.git

Move into project directory:

cd ai-stock-analyst

Install dependencies:

pip install -r requirements.txt
🔑 Setup API Key

Create a .env file:

GROQ_API_KEY=your_api_key_here
▶️ Run The Project
python main.py

Example output:

Stock: ICICI Bank
Current Price: 2137
Predicted Price: 2133
Trend: Stable

AI Analysis:
The predicted price shows minimal deviation from the current market price,
indicating relatively balanced market sentiment. This suggests neither
strong buying nor selling pressure in the short term.
📌 Future Improvements

Possible upgrades for this project:

LSTM deep learning models
Technical indicators (RSI, MACD, Moving Averages)
Real-time dashboard
Streamlit web interface
Multi-stock portfolio analysis
AI trading signals
