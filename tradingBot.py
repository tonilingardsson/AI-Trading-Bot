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
        def initialize(self, symbol: str= "SPY", cash_at_risk: float= 0.5):
            self.symbol = symbol
            self.sleeptime = "24H"
            # This is goint to capture what our last trade was
            self.last_trade = None
            # Make cash_at_risk available as an attribute
            self.cash_at_risk = cash_at_risk
            print(f"Stratety initialized for the symbol: {self.symbol}")
            # Trading position management
        def position_sizing(self):
                # DINAMICALLY Get the current cash available for trading
            cash = self.get_cash()
            # Get the last price for the symbol
            last_price = self.get_last_price(self.symbol)
            # Calculate the position size (or quantity) based on the cash at risk
            position_size = round((cash * self.cash_at_risk) / last_price,0)
            print(f"Avaliable cash: ${cash:.2f}")
            print(f"Last price for {self.symbol}: ${last_price:.2f}")
            return cash, last_price, position_size

        def on_trading_iteration(self):
                cash, last_price, position_size = self.position_sizing()

                if cash > last_price:
                    # Check if we have an open position
                    if self.last_trade is None :
                        order = self.create_order(
                            self.symbol,
                            position_size,
                            "buy",
                            # Type: market, limit, buy_stop, sell_stop, limit_if_touched, etc
                            type="bracket",
                            # Set a strategy for the order, selling when the price goes up 20%
                            take_profit_price= last_price * 1.2,
                            # Set a strategy for the order, selling when the price goes down 5%
                            stop_loss_price=last_price * 0.95,
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
    strategy = MLTrader(name="mlstrategy", broker=broker, parameters={"symbol": "SPY", "cash_at_risk": 0.5})
    # If you want a more risky bot, raise the cash_at_risk to 0.75, or to 1; if want a more conservative bot, lower it to 0.25 or 0.1
    strategy.backtest(
        YahooDataBacktesting,
        start_date,
        end_date,
        parameters={"symbol": "SPY"}
    )