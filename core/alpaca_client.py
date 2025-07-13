import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL")

# Connect to Alpaca
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL)

# 🔄 Check current position
def get_position(symbol="BTC/USD"):
    try:
        position = api.get_position(symbol.replace("/", ""))
        return position
    except tradeapi.rest.APIError:
        return None  # No open position

# 🟢 Place a market order
def place_market_order(symbol, side, quantity):
    try:
        order = api.submit_order(
            symbol=symbol.replace("/", ""),
            qty=quantity,
            side=side.lower(),  # 'buy' or 'sell'
            type='market',
            time_in_force='gtc'
        )
        print(f"🟢 {side.upper()} Order Executed: ID {order.id}")
        return order
    except Exception as e:
        print(f"❌ Order Error: {e}")
        return None
