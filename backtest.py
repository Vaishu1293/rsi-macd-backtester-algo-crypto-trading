import yfinance as yf
import pandas as pd
import os
# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")
# Choose asset and timeframe
symbol = "BTC-USD"
start_date = "2020-01-01"
end_date = "2024-12-31"
# Fetch data
df = yf.download(symbol, start=start_date, end=end_date, interval="1d")
# Save to CSV
csv_path = f"data/{symbol.replace('-', '_')}_daily.csv"
df.to_csv(csv_path)
print(f"✅ Data saved to {csv_path}")
print(df.head())