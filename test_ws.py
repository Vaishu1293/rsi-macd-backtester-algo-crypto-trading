import nest_asyncio
import asyncio
from core.ws_listener import start_ws

# Patch the running event loop (for Anaconda/Jupyter/Windows terminals)
nest_asyncio.apply()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_ws("BTC/USD"))
