import backtrader as bt
from strategies.rsi_macd_strategy import RSIMACDStrategy
import yfinance as yf
import pandas as pd
import os

# ----------------------------
# Step 1: Download historical data
# ----------------------------
symbol = "BTC-USD"
os.makedirs("data", exist_ok=True)
csv_path = f"data/{symbol.replace('-', '_')}_daily.csv"

if not os.path.exists(csv_path):
    print("📥 Downloading historical data...")
    df = yf.download(symbol, start="2020-01-01", end="2024-12-31", interval="1d")
    df.to_csv(csv_path, index=True)  # Ensure index is saved
else:
    print("📂 Loading existing data from CSV...")
    df = pd.read_csv(csv_path)

# ----------------------------
# Step 2: Normalize Date column and index
# ----------------------------
# If 'Date' is missing, it might be stored as 'Unnamed: 0'
if "Date" not in df.columns:
    if "Unnamed: 0" in df.columns:
        df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    else:
        raise ValueError("❌ No 'Date' or 'Unnamed: 0' column found in CSV.")

# Ensure 'Date' column is datetime
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df.set_index("Date", inplace=True)

# Drop any rows with missing price values (optional but safe)
df.dropna(subset=["Open", "High", "Low", "Close", "Volume"], inplace=True)

# ----------------------------
# Step 3: Show data sample
# ----------------------------
print("📊 Data Sample:")
print(df.head())

# ----------------------------
# Step 4: Define Strategy
# ----------------------------
class TestStrategy(bt.Strategy):
    def __init__(self):
        print("🔍 Strategy initialized")

    def next(self):
        print(f"🕒 Date: {self.datas[0].datetime.date(0)}, Close: {self.datas[0].close[0]}")

# ----------------------------
# Step 5: Initialize Backtrader engine
# ----------------------------
cerebro = bt.Cerebro()
cerebro.broker.set_cash(100000)  # Starting balance

# ----------------------------
# Step 6: Convert Pandas DataFrame to Backtrader data feed
# ----------------------------
data_feed = bt.feeds.PandasData(dataname=df)

# ----------------------------
# Step 7: Add data + strategy
# ----------------------------
cerebro.adddata(data_feed)
# cerebro.addstrategy(TestStrategy)
# Replace TestStrategy with RSIMACDStrategy
cerebro.addstrategy(RSIMACDStrategy)

# ----------------------------
# Step 8: Run backtest
# ----------------------------
print("🚀 Running Backtest...")
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.run()

# ----------------------------
# Step 9: Plot results
# ----------------------------
cerebro.plot()

strat = results[0] # Get the strategy instance
# Extract analyzer reports
sharpe = strat.analyzers.sharpe.get_analysis()
trades = strat.analyzers.trades.get_analysis()
drawdown = strat.analyzers.drawdown.get_analysis()

print("\n📊 PERFORMANCE SUMMARY:")
# Sharpe Ratio
sharpe_ratio = sharpe.get('sharperatio', None)

if sharpe_ratio is not None:
    print(f"✅ Sharpe Ratio: {sharpe_ratio:.2f}")
else:
    print("⚠️ Sharpe Ratio: Not available (maybe no trades or flat returns)")
# Trade Stats
total_trades = trades.total.total if trades.total.total else 0
won_trades = trades.won.total if trades.won.total else 0
lost_trades = trades.lost.total if trades.lost.total else 0
if total_trades > 0:
    win_rate = (won_trades / total_trades) * 100
    print(f"✅ Win Rate: {won_trades}/{total_trades} ({win_rate:.2f}%)")
else:
    print("⚠️ Win Rate: No trades made")
# Max Drawdown

max_dd = drawdown.max.drawdown
print(f"📉 Max Drawdown: {max_dd:.2f}%")
# Portfolio Value
final_value = cerebro.broker.getvalue()
print(f"💰 Final Portfolio Value: ${final_value:.2f}")

# Print full analyzer outputs
print("Full Sharpe:", sharpe)
print("Full Trades:", trades)
print("Full Drawdown:", drawdown)
