from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

APCA_API_KEY = os.getenv("API_KEY")
APCA_API_SECRET = os.getenv("API_SECRET")
APCA_API_BASE_URL = os.getenv("API_BASE_URL")

ALPACA_CREDENTIALS = {
    "API_KEY": APCA_API_KEY,
    "API_SECRET": APCA_API_SECRET,
    "API_URL": APCA_API_BASE_URL,
    "PAPER": True,
}

# Create a new class
class MLTrader(Strategy):
        def initialize(self, symbol: str= "SPY"):
            self.symbol = symbol
            self.sleeptime = "24H"
            # This is goint to capture what our last trade was
            self.last_trade = None
            print(f"Stratety initialized for the symbol: {self.symbol}")
            # Trading position management
        def position_sizing(self):
                # DINAMICALLY Get the current cash available for trading
            cash = self.get_cash()
            last_price = self.get_last_price(self.symbol)
            print(f"Avaliable cash: ${cash:.2f}")
            print(f"Last price for {self.symbol}: ${last_price:.2f}")
            return cash, last_price

        def on_trading_iteration(self):
                if self.last_trade is None :
                    order = self.create_order(
                        self.symbol,
                        10,
                        "buy",
                        # Type: market, limit, buy_stop, sell_stop, limit_if_touched, etc
                        type="market",
                    )
                    # Let's pass the order to the broker
                    self.submit_order(order)
                    self.last_trade = "buy"
                    print(f"Placed buy order for {self.symbol}: 10 shares")

if __name__ == "__main__":
    # Set the start and end dates for backtesting
    # You can change these dates to your desired backtesting period
    # For example, to backtest from December 15, 2023 to December 31, 2023
    # You can also use datetime.now() to get the current date and time
    start_date = datetime(2023, 12, 15)
    end_date = datetime(2023, 12, 31)
    broker = Alpaca(ALPACA_CREDENTIALS)
    strategy = MLTrader(name="mlstrategy", broker=broker, parameters={"symbol": "SPY"})
    strategy.backtest(
        YahooDataBacktesting,
        start_date,
        end_date,
        parameters={"symbol": "SPY"}
    )