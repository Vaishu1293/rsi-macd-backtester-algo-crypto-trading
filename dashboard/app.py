import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

# === Streamlit Page Config ===
st.set_page_config(page_title="AlgoBot Live Dashboard", layout="wide")
st.title("🚀 Live Algo Trading Dashboard")

# === File Paths ===
TRADE_LOG_PATH = "results/trade_log.csv"
EQUITY_PATH = "results/equity_curve.csv"

# === Load Trade Log ===
if os.path.exists(TRADE_LOG_PATH):
    trades_df = pd.read_csv(TRADE_LOG_PATH)
else:
    trades_df = pd.DataFrame(columns=[
        "entry_date", "exit_date", "entry_price",
        "exit_price", "duration_days", "pnl", "size"
    ])

# === Load Equity Curve ===
if os.path.exists(EQUITY_PATH):
    equity_df = pd.read_csv(EQUITY_PATH, index_col=0, parse_dates=True)
else:
    equity_df = pd.DataFrame(columns=["cumulative"])

# === Sidebar Settings ===
st.sidebar.title("📊 Strategy Settings")
st.sidebar.markdown("**Model:** RSI + MACD + 5 Indicators")
st.sidebar.markdown("**Asset:** BTC/USDT")
st.sidebar.markdown("**Interval:** 1-minute")
st.sidebar.markdown("**Capital:** 100,000 USDT")

# === Main Content Layout ===
col1, col2 = st.columns([2, 1])

# === Equity Curve Chart ===
with col1:
    st.subheader("📈 Equity Curve")
    if not equity_df.empty:
        st.line_chart(equity_df)
    else:
        st.info("No equity data yet.")

# === Recent Trade Signals Table ===
with col2:
    st.subheader("🧠 Recent Trade Signals")
    if not trades_df.empty:
        recent = trades_df.tail(5).sort_values(by="exit_date", ascending=False)
        st.table(recent[["entry_date", "exit_date", "pnl"]])
    else:
        st.info("No trades yet.")

# === Full Trade Log ===
st.subheader("📒 Full Trade Log")
if not trades_df.empty:
    st.dataframe(trades_df[::-1])  # Show latest trades at the top
else:
    st.warning("Trade log is currently empty.")

# === Auto Refresh ===
st.markdown("⏱️ Auto-refresh in 15 seconds...")
time.sleep(15)
st.experimental_rerun()
