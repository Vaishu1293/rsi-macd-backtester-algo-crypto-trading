import backtrader as bt
import csv

class RSIMACDStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)
        self.macd = bt.indicators.MACD(self.data.close)
        self.macd_line = self.macd.macd
        self.macd_signal = self.macd.signal
        self.macd_hist = self.macd.macd - self.macd.signal
        self.order = None
        self.trade_log = []
        print("🔧 Indicators initialized.")

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} - {txt}")

    def notify_trade(self, trade):
        if trade.isclosed:
            try:
                entry_price_estimate = trade.price - (trade.pnl if trade.pnl else 0)
                entry_date = bt.num2date(trade.dtopen).date()
                exit_date = bt.num2date(trade.dtclose).date()
                pnl = round(trade.pnl, 2)
                size = trade.size
                duration = (exit_date - entry_date).days

                self.trade_log.append({
                    'entry_date': entry_date,
                    'exit_date': exit_date,
                    'entry_price': round(entry_price_estimate, 2),
                    'exit_price': round(trade.price, 2),
                    'duration_days': duration,
                    'pnl': pnl,
                    'size': size
                })

                self.log(f"📒 Trade closed | Entry: ~{entry_price_estimate:.2f} → Exit: {trade.price:.2f} | PnL: {pnl:.2f}")
            except Exception as e:
                self.log(f"⚠️ Error in notify_trade: {e}")


    def next(self):
        self.log(
            f"Close={self.data.close[0]:.2f}, "
            f"RSI={self.rsi[0]:.2f}, "
            f"MACD={self.macd_line[0]:.2f}, "
            f"Signal={self.macd_signal[0]:.2f}, "
            f"Hist={self.macd_hist[0]:.2f}"
        )

        # Very basic buy/sell logic for testing:
        if not self.position:
            if self.rsi[0] < 50 and self.macd_hist[0] > -0.5:
                self.order = self.buy(size=1)
                self.log("📈 BUY triggered")
        else:
            if self.rsi[0] > 49 and self.macd_hist[0] < -0.5:
                self.order = self.sell(size=1)
                self.log("📉 SELL triggered")
