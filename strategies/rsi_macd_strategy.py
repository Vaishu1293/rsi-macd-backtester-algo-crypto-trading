import backtrader as bt

class RSIMACDStrategy(bt.Strategy):
    def __init__(self):
        # Initialize indicators
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)
        self.macd = bt.indicators.MACD(self.data.close)  # default fast=12, slow=26, signal=9
        self.macd_line = self.macd.macd
        self.macd_signal = self.macd.signal
        self.macd_hist = self.macd_line - self.macd_signal  # MACD histogram

        self.order = None
        print("🔧 Indicators initialized.")

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} - {txt}")

    def next(self):
        # Log current prices and indicator values
        self.log(
            f"Close={self.data.close[0]:.2f}, "
            f"RSI={self.rsi[0]:.2f}, "
            f"MACD={self.macd_line[0]:.2f}, "
            f"Signal={self.macd_signal[0]:.2f}, "
            f"Hist={self.macd_hist[0]:.2f}"
        )
