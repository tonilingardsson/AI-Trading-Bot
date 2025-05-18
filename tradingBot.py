from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDENTIALS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True,
}