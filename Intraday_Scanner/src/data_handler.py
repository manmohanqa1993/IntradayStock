"""
Data Handler - Yahoo Finance
=============================
Simple data fetching for beginners
"""

import pandas as pd
import logging

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance not installed. Run: pip install yfinance")

logger = logging.getLogger(__name__)


class DataHandler:
    """Simple Yahoo Finance data handler"""

    def __init__(self):
        self.name = "Yahoo Finance (FREE)"
        self.suffix = ".NS"  # NSE India

    def get_intraday_candles(self, symbol):
        """Get today's 5-minute candles"""
        try:
            if not YFINANCE_AVAILABLE:
                return None

            ticker = yf.Ticker(f"{symbol}{self.suffix}")
            df = ticker.history(period='1d', interval='5m')

            if df.empty:
                return None

            # Standardize columns
            df = df.reset_index()
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'])

            # Calculate VWAP
            typical_price = (df['high'] + df['low'] + df['close']) / 3
            df['vwap'] = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()

            return df

        except Exception as e:
            logger.debug(f"Error fetching {symbol}: {e}")
            return None

    def get_historical_data(self, symbol, days=15):
        """Get last N days of daily data"""
        try:
            if not YFINANCE_AVAILABLE:
                return None

            ticker = yf.Ticker(f"{symbol}{self.suffix}")
            df = ticker.history(period=f"{days+5}d")

            if df.empty:
                return None

            df = df.reset_index()
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'])

            return df.tail(days)

        except Exception as e:
            logger.debug(f"Error fetching historical {symbol}: {e}")
            return None


if __name__ == "__main__":
    # Test
    handler = DataHandler()
    print(f"Data Handler: {handler.name}")

    candles = handler.get_intraday_candles('RELIANCE')
    if candles is not None:
        print(f"✅ Fetched {len(candles)} candles for RELIANCE")
    else:
        print("❌ Could not fetch data")
