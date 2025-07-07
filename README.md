
# 🤖 QuantEdge AI – Real-Time Algorithmic Trading Platform

An enterprise-grade, modular **AI-powered trading bot system** built for:

- 💹 Live Binance trading (testnet)
- 📊 Backtesting with indicators and metrics
- 📬 Real-time Telegram alerts
- 🌐 Streamlit web dashboard
- 🔒 Risk-managed, pluggable strategies

---

## 🧠 Powered By

- **Python** · **Backtrader** · **pandas-ta**
- **Binance API (Testnet)** · **Telegram Bot API**
- **Streamlit** · **Matplotlib** · **WebSockets**

---

## ✅ Core Features

### 🔁 Real-Time Trading Bot
- Connects to Binance Futures Testnet via WebSocket
- Streams live OHLCV candles (1m)
- Computes 7+ indicators (RSI, MACD, EMA, SMA, ATR, Bollinger Bands, Stochastic)
- Executes **market BUY/SELL orders** based on signal logic
- Sends real-time alerts via Telegram

### 📈 Backtesting Engine
- Built on **Backtrader**
- Supports:
  - Daily OHLCV from Yahoo via `yfinance`
  - RSI + MACD + SMA/EMA + ATR-based strategies
  - Signal logging
  - Trade export to `CSV`
- Metrics: Sharpe Ratio, Win Rate, Max Drawdown

### 📊 Streamlit Dashboard
- Real-time **equity curve** plot
- View **latest trades + full trade log**
- Tabbed display of **backtest charts + strategy code**

### 🔒 Risk Management
- Position sizing based on `MAX_RISK_PERCENT`
- Dynamic quantity using **ATR x STOP_LOSS_BUFFER**
- Prevents overtrading or double entries

### 📬 Telegram Bot
- Sends alerts for each BUY/SELL action
- Supports status commands via message (optional)

---

## 📂 Project Structure

```

algo-trading-bot/
├── core/
│   ├── binance\_client.py      # Binance API & auth
│   ├── ws\_listener.py         # WebSocket stream + signal engine
│   └── telegram\_alerts.py     # Telegram notifications
├── strategies/
│   └── rsi\_macd\_strategy.py   # Backtrader strategy logic
├── dashboard/
│   └── app.py                 # Streamlit dashboard
├── results/                   # trade\_log.csv, equity\_curve.csv, PNGs
├── backtest.py                # Full backtesting script
├── test\_ws.py                 # Live Binance bot runner
├── test\_connection.py         # API test for Binance
├── requirements.txt
├── .env.example
└── README.md

````

---

## ⚙️ Setup Instructions

### 1. 🔧 Install Requirements

```bash
pip install -r requirements.txt
````

### 2. 📁 Configure `.env`

Create your `.env` using the example below:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret
BINANCE_URL=https://testnet.binancefuture.com
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=@your_telegram_id
STARTING_BALANCE=100000
MAX_RISK_PERCENT=1
STOP_LOSS_BUFFER=1.5
```

---

## 🚀 Run the System

### ▶️ Backtest Strategy

```bash
python backtest.py
```

* Outputs: equity curve, trade log, Sharpe/WinRate, PNG chart

### 🔁 Start Live Bot (WebSocket + Signal Engine + Orders)

```bash
python test_ws.py
```

* Will auto-trade on testnet if signal matches logic.

### 🌐 Launch Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Visit [http://localhost:8501](http://localhost:8501)

---

## 📬 Telegram Setup (Optional)

1. Search for **BotFather** on Telegram
2. Create bot → Get token → Add to `.env`
3. Get your **chat ID** from `@userinfobot` or use `@yourusername`

---

## 📊 Performance Metrics

* ✅ Sharpe Ratio (risk-adjusted return)
* ✅ Win Rate (signal effectiveness)
* ✅ Max Drawdown (capital risk)
* ✅ Equity curve PNG + CSV logs

---

## 📦 Deploy-Ready for GitHub or Cloud

* Includes `.env.example`, `requirements.txt`, and folder scaffolding
* Suitable for:

  * ✅ GitHub push
  * ✅ Cloud deployment (Render, GCP, AWS)
  * ✅ Hackathons & demo use

---

## 🔜 Coming Next

* [ ] GARCH-based volatility model (Module 7)
* [ ] K-Means stock clustering strategy (Module 8)
* [ ] AI Agent DAO integration (Stage 5)
* [ ] Web3 Wallet-based strategy runner

---

## 👤 Client: QuantEdge AI

This system was developed as part of a modular AI trading stack for **QuantEdge AI**, a FinTech company serving:

* Crypto hedge funds
* Retail algo traders
* Telegram bot signal resellers
* Institutional DeFi analytics

---

## 💡 License

MIT License · Use at your own risk on real markets.

---
