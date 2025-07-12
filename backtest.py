import backtrader as bt
import csv
from strategies.rsi_macd_strategy import RSIMACDStrategy
import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt


symbol = "BTC-USD"
os.makedirs("data", exist_ok=True)
csv_path = f"data/{symbol.replace('-', '_')}_daily.csv"

if not os.path.exists(csv_path):
    print("📥 Downloading historical data...")
    df = yf.download(symbol, start="2020-01-01", end="2024-12-31", interval="1d")
    df.to_csv(csv_path, index=True)
else:
    print("📂 Loading existing data from CSV...")
    df = pd.read_csv(csv_path)

if "Date" not in df.columns:
    if "Unnamed: 0" in df.columns:
        df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    else:
        raise ValueError("❌ No 'Date' or 'Unnamed: 0' column found in CSV.")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df.set_index("Date", inplace=True)
df.dropna(subset=["Open", "High", "Low", "Close", "Volume"], inplace=True)

print("📊 Data Sample:")
print(df.head())

cerebro = bt.Cerebro()
cerebro.broker.set_cash(100000)
data_feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data_feed)
cerebro.addstrategy(RSIMACDStrategy)

cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='returns')

print("🚀 Running Backtest...")
results = cerebro.run()
cerebro.plot()
print("results: ", results)
strat = results[0]
sharpe = strat.analyzers.sharpe.get_analysis()
trades = strat.analyzers.trades.get_analysis()
drawdown = strat.analyzers.drawdown.get_analysis()

returns = strat.analyzers.returns.get_analysis()


print("\n📊 PERFORMANCE SUMMARY:")
sharpe_ratio = sharpe.get('sharperatio', None)
if sharpe_ratio is not None:
    print(f"✅ Sharpe Ratio: {sharpe_ratio:.2f}")
else:
    print("⚠️ Sharpe Ratio: Not available")

total_trades = trades.total.total if trades.total.total else 0
won_trades = trades.won.total if trades.won.total else 0
lost_trades = trades.lost.total if trades.lost.total else 0
if total_trades > 0:
    win_rate = (won_trades / total_trades) * 100
    print(f"✅ Win Rate: {won_trades}/{total_trades} ({win_rate:.2f}%)")
else:
    print("⚠️ Win Rate: No trades made")

max_dd = drawdown.max.drawdown
print(f"📉 Max Drawdown: {max_dd:.2f}%")
final_value = cerebro.broker.getvalue()
print(f"💰 Final Portfolio Value: ${final_value:.2f}")

# ✅ Step 2.5.B – Export Full Trade Log to CSV
if hasattr(strat, 'trade_log'):
    os.makedirs("results", exist_ok=True)
    csv_file = "results/trade_log.csv"
    with open(csv_file, mode="w", newline="") as f:
        fieldnames = ['entry_date', 'exit_date', 'entry_price', 'exit_price', 'duration_days', 'pnl', 'size']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in strat.trade_log:
            writer.writerow(row)
    print(f"📂 Trade log saved to {csv_file}")

    df_log = pd.read_csv(csv_file)
    print("\n📊 Trade Summary Stats:")
    print(df_log.describe())
else:
    print("⚠️ No trade log found in strategy.")


returns_series = pd.Series(returns)
cumulative = (1 + returns_series).cumprod()
# Plot Equity Curve
plt.figure(figsize=(12, 6))
plt.plot(cumulative, label="Equity Curve")
plt.title("📈 Portfolio Equity Curve")
plt.xlabel("Date")
plt.ylabel("Cumulative Returns")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("results/equity_curve.png")
plt.show()

cumulative.to_csv("results/equity_curve.csv")



