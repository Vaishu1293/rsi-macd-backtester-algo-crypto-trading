import os
from dotenv import load_dotenv
from alpaca.data.historical import CryptoHistoricalDataClient
from core.alpaca_client import place_market_order, get_position
from alpaca.data.live import CryptoDataStream
import asyncio

load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

# Create streaming client
stream = CryptoDataStream(API_KEY, API_SECRET)

# Callback handler for incoming bars (1-minute candles)
async def handle_bar(data):
    print(f"🕒 {data.timestamp} | ⏫ Open: {data.open} | ⏬ Close: {data.close} | 🔄 Volume: {data.volume}")

# Start WebSocket listener
async def start_ws(symbol="BTC/USD"):
    print(f"🛰 Starting Alpaca WebSocket for {symbol} [1m]...")
    stream.subscribe_bars(handle_bar, symbol)
    await stream.run()

def check_signal(df):
    latest = df.iloc[-1]
    symbol = "BTC/USD"
    qty = 0.01  # or a realistic lot size

    current_pos = get_position(symbol)
    in_position = current_pos is not None

    # --- BUY Signal Logic ---
    if (
        latest["rsi"] < 30 and
        latest["macd"] > latest["macd_signal"]
    ):
        if not in_position:
            print(f"✅ BUY Signal @ {latest['close']}")
            place_market_order(symbol, "buy", qty)
        else:
            print("🔒 Already in position – skipping BUY")

    # --- SELL Signal Logic ---
    elif (
        latest["rsi"] > 70 and
        latest["macd"] < latest["macd_signal"]
    ):
        if in_position:
            print(f"🔻 SELL Signal @ {latest['close']}")
            place_market_order(symbol, "sell", qty)
        else:
            print("🚫 No position – skipping SELL")

