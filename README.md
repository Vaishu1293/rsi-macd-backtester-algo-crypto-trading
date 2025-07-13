# QuantEdge AI – Real-Time Algorithmic Trading Platform (Alpaca Edition)

An enterprise-grade, modular AI-powered trading bot system built for:

💹 Live **Alpaca** trading (paper trading or live)  
📊 Backtesting with indicators and metrics  
📬 Real-time Telegram alerts  
🌐 Streamlit web dashboard  
🔒 Risk-managed, pluggable strategies

---

## 🧠 Powered By
**Python** · **Backtrader** · **pandas-ta**  
**Alpaca API** · **Telegram Bot API**  
**Streamlit** · **Matplotlib** · **WebSockets**

---

## ✅ Core Features

### 🔁 Real-Time Trading Bot
- Connects to **Alpaca WebSocket API**
- Streams live OHLCV candles (1m)
- Computes 7+ indicators (RSI, MACD, EMA, SMA, ATR, Bollinger Bands, Stochastic)
- Executes market **BUY/SELL** orders based on signal logic
- Sends real-time alerts via **Telegram**

### 📈 Backtesting Engine
- Built on **Backtrader**
- Supports:
  - Daily OHLCV from **Yahoo Finance** via `yfinance`
  - RSI + MACD + EMA/SMA + ATR-based strategies
  - Signal logging and result export
  - Metrics: **Sharpe Ratio**, **Win Rate**, **Max Drawdown**

### 📊 Streamlit Dashboard
- Real-time equity curve plot
- View latest trades + full trade log
- **Tabbed view**: Live trades, backtest charts, and strategy logic

### 🔒 Risk Management
- Position sizing via `MAX_RISK_PERCENT`
- Dynamic quantity using `ATR × STOP_LOSS_BUFFER`
- Prevents overtrading and overlapping entries

### 📬 Telegram Bot
- Sends alerts for each BUY/SELL action
- Supports status and control commands (optional)

---

## 📂 Project Structure

```

algo-trading-bot/
├── core/
│   ├── alpaca\_client.py        # Alpaca API client and trading logic
│   ├── ws\_listener.py          # WebSocket stream + signal engine
│   └── telegram\_alerts.py      # Telegram notifications
├── strategies/
│   └── rsi\_macd\_strategy.py    # Backtrader strategy logic
├── dashboard/
│   └── app.py                  # Streamlit dashboard UI
├── results/                    # trade\_log.csv, equity\_curve.csv, PNGs
├── backtest.py                 # Full backtesting script
├── test\_ws.py                  # Real-time live bot runner (Alpaca)
├── test\_connection.py          # API test for Alpaca
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

### 2. 📁 Configure .env

Create your `.env` using the template below:

```
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=@your_telegram_id

STARTING_BALANCE=100000
MAX_RISK_PERCENT=1
STOP_LOSS_BUFFER=1.5
```

> 🔒 Never commit `.env` to GitHub. Add it to `.gitignore`.

---

## 🚀 Run the System

### ▶️ Backtest Strategy

```bash
python backtest.py
```

Outputs: equity curve, trade log, Sharpe/WinRate, PNG chart

### 🔁 Start Live Bot (WebSocket + Signal Engine + Orders)

```bash
python test_ws.py
```

Will auto-trade on Alpaca (paper account) if signals match logic.

### 🌐 Launch Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Visit `http://localhost:8501` in your browser

---

## 📬 Telegram Setup (Optional)

1. Search **BotFather** on Telegram and create a new bot.
2. Copy the bot token and add to `.env`.
3. Get your chat ID from [@userinfobot](https://t.me/userinfobot) or use your `@username`.

---

## 📊 Performance Metrics

* ✅ Sharpe Ratio (risk-adjusted return)
* ✅ Win Rate (signal effectiveness)
* ✅ Max Drawdown (capital risk)
* ✅ Equity curve PNG + CSV logs

---

## 📦 Deploy-Ready for GitHub or Cloud

Includes:

* `.env.example`
* `requirements.txt`
* Organized modular structure

Ready for:

* ✅ GitHub push
* ✅ Deployment to Render, GCP, or AWS
* ✅ Hackathons & demo use

---

## 🔜 Coming Next

* GARCH-based volatility model (Module 7)
* K-Means stock clustering strategy (Module 8)
* AI Agent DAO integration (Stage 5)
* Web3 Wallet-based strategy runner

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
