# 📈 AI Stock Predictor & Analyst

An AI-powered system that predicts stock prices using Machine Learning and generates human-readable explanations using a Large Language Model.

This project combines **financial data analysis**, **time-series prediction**, and **Generative AI** to create an automated **AI financial analyst**.

---

# 🚀 Features

### 📊 Stock Price Prediction
- Uses historical stock market data
- Implements a **sliding window time-series prediction**
- Predicts **future stock price movements**

### 📉 Trend Detection
Based on predicted price change, the system classifies the trend into:

- 📈 Upward
- 📉 Downward
- ➡️ Stable

### 🧠 AI Explanation
The prediction results are passed to an LLM which generates a **natural language explanation** of the stock behavior.

Example output:
# 📈 AI Stock Predictor & Analyst

An AI-powered system that predicts stock prices using Machine Learning and generates human-readable explanations using a Large Language Model.

This project combines **financial data analysis**, **time-series prediction**, and **Generative AI** to create an automated **AI financial analyst**.

---

# 🚀 Features

### 📊 Stock Price Prediction
- Uses historical stock market data
- Implements a **sliding window time-series prediction**
- Predicts **future stock price movements**

### 📉 Trend Detection
Based on predicted price change, the system classifies the trend into:

- 📈 Upward
- 📉 Downward
- ➡️ Stable

### 🧠 AI Explanation
The prediction results are passed to an LLM which generates a **natural language explanation** of the stock behavior.

Example output:

---

# 🏗 System Architecture


Stock Market Data (Yahoo Finance)
│
▼
Data Preprocessing
│
▼
Machine Learning Model
(Sliding Window Prediction)
│
▼
Trend Detection
(Up / Down / Stable)
│
▼
LLM Explanation Engine
(Groq API)
│
▼
Final AI Analysis Output

---

# 🧠 AI Model

The explanation engine uses a Large Language Model.

**Model:** `llama-3.3-70b-versatile`  
**Provider:** Groq

This model was selected because it provides:

- Strong reasoning capability
- Fast inference
- High-quality natural language explanations
- Good performance for analytical tasks

The model analyzes:
- Current stock price
- Predicted price
- Percentage change
- Market trend

and generates a human-readable explanation.

---

# 📊 Data Source

Stock data is fetched from **Yahoo Finance** using the `yfinance` library.

Data features include:

- Open
- High
- Low
- Close
- Volume

Example companies used in this project:

---

# 🧠 AI Model

The explanation engine uses a Large Language Model.

**Model:** `llama-3.3-70b-versatile`  
**Provider:** Groq

This model was selected because it provides:

- Strong reasoning capability
- Fast inference
- High-quality natural language explanations
- Good performance for analytical tasks

The model analyzes:
- Current stock price
- Predicted price
- Percentage change
- Market trend

and generates a human-readable explanation.

---

# 📊 Data Source

Stock data is fetched from **Yahoo Finance** using the `yfinance` library.

Data features include:

- Open
- High
- Low
- Close
- Volume

Example companies used in this project:

---

# 🧠 AI Model

The explanation engine uses a Large Language Model.

**Model:** `llama-3.3-70b-versatile`  
**Provider:** Groq

This model was selected because it provides:

- Strong reasoning capability
- Fast inference
- High-quality natural language explanations
- Good performance for analytical tasks

The model analyzes:
- Current stock price
- Predicted price
- Percentage change
- Market trend

and generates a human-readable explanation.

---

# 📊 Data Source

Stock data is fetched from **Yahoo Finance** using the `yfinance` library.

Data features include:

- Open
- High
- Low
- Close
- Volume

Example companies used in this project:

---

# 🧠 AI Model

The explanation engine uses a Large Language Model.

**Model:** `llama-3.3-70b-versatile`  
**Provider:** Groq

This model was selected because it provides:

- Strong reasoning capability
- Fast inference
- High-quality natural language explanations
- Good performance for analytical tasks

The model analyzes:
- Current stock price
- Predicted price
- Percentage change
- Market trend

and generates a human-readable explanation.

---

# 📊 Data Source

Stock data is fetched from **Yahoo Finance** using the `yfinance` library.

Data features include:

- Open
- High
- Low
- Close
- Volume

Example companies used in this project:
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

---

# ⚙️ Machine Learning Approach

The model uses a **sliding window time-series technique**.

Example:
Day1 Day2 Day3 Day4 Day5 → Predict Day6


Training sample example:
[2140, 2139, 2138, 2136, 2137] → 2133


This approach helps the model learn **short-term market patterns**.

---

# 📉 Trend Classification

Trend is determined using percentage change between predicted and current price.


change % = (predicted_price - current_price) / current_price * 100


Trend thresholds:


+1% → Upward 📈
< -1% → Downward 📉
Else → Stable ➡️


These thresholds help reduce **normal market noise**.

---

# 🛠 Tech Stack

### Programming Language
- Python

### Libraries
- NumPy
- Pandas
- Scikit-learn
- yfinance

### AI / LLM
- Groq API
- llama-3.3-70b-versatile

---

# 📦 Installation

Clone the repository:


git clone https://github.com/yourusername/ai-stock-analyst.git


Navigate to the project directory:


cd ai-stock-analyst


Install dependencies:


pip install -r requirements.txt


---

# 🔑 API Setup

Create a `.env` file in the root directory and add your Groq API key:


GROQ_API_KEY=your_api_key_here


---

# ▶️ Running the Project

Run the main script:


python main.py


Example output:


Stock: ICICI Bank
Current Price: 2137
Predicted Price: 2133
Trend: Stable

AI Analysis:
The predicted price shows minimal deviation from the current market
price, suggesting balanced market sentiment with no strong upward
or downward momentum in the short term.


---

# 🔮 Future Improvements

Possible enhancements:

- LSTM or Transformer-based prediction models
- Technical indicators (RSI, MACD, Moving Averages)
- Real-time dashboard using Streamlit
- Portfolio-level analysis
- AI trading signals

---

