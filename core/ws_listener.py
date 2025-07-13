import os
import asyncio
from dotenv import load_dotenv
from alpaca.data.live import CryptoDataStream
from core.telegram_alerts import send_message
from alpaca.data.historical import CryptoHistoricalDataClient
from core.alpaca_client import place_market_order, get_position

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
        capital = float(os.getenv("STARTING_BALANCE"))
        risk_pct = float(os.getenv("MAX_RISK_PERCENT"))
        atr = latest["atr"]
        if atr and atr > 0:
            risk_amount = capital * (risk_pct / 100)
            stop_distance = atr * float(os.getenv("STOP_LOSS_BUFFER"))
            qty = round(risk_amount / stop_distance, 3)

        if not in_position:
            print(f"✅ BUY Signal @ {latest['close']}")
            send_message(f"✅ BUY Signal @ {latest['close']:.2f}")
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
            send_message(f"🔻 SELL Signal @ {latest['close']:.2f}")
            place_market_order(symbol, "sell", qty)
        else:
            print("🚫 No position – skipping SELL")

