"""
Data Handler - FREE API Integration Layer
=========================================
Fetches data using FREE APIs (Yahoo Finance)
NO BROKER API KEYS NEEDED!
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import time
from abc import ABC, abstractmethod

# Try to import free APIs
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance not installed. Run: pip install yfinance")

try:
    from nsepy import get_history
    from nsepy.live import get_quote
    NSEPY_AVAILABLE = True
except ImportError:
    NSEPY_AVAILABLE = False
    print("⚠️ nsepy not installed. Run: pip install nsepy")

from config import *

logger = logging.getLogger(__name__)


# ==================== BASE BROKER CLASS ====================

class BrokerAdapter(ABC):
    """Abstract base class for broker adapters"""

    def __init__(self, config):
        self.config = config
        self.name = "BaseBroker"
        self.is_connected = False

    @abstractmethod
    def connect(self):
        """Establish connection to broker API"""
        pass

    @abstractmethod
    def get_live_price(self, symbol):
        """Get current live price"""
        pass

    @abstractmethod
    def get_intraday_data(self, symbol, interval='5min'):
        """Get today's intraday candle data"""
        pass

    @abstractmethod
    def get_historical_data(self, symbol, days=15):
        """Get historical daily data"""
        pass

    @abstractmethod
    def get_stock_info(self, symbol):
        """Get stock metadata (avg volume, turnover, etc.)"""
        pass


# ==================== FREE YAHOO FINANCE ADAPTER ====================

class YahooFinanceAdapter(BrokerAdapter):
    """Yahoo Finance - FREE API (No credentials needed!)"""

    def __init__(self, config):
        super().__init__(config)
        self.name = "Yahoo Finance (FREE)"
        self.suffix = ".NS"  # NSE India suffix

    def connect(self):
        """No connection needed - it's free!"""
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance not installed. Run: pip install yfinance")
            return False

        self.is_connected = True
        logger.info(f"✅ Connected to {self.name} - NO API KEY NEEDED!")
        return True

    def get_live_price(self, symbol):
        """Get current price from Yahoo Finance"""
        try:
            ticker = yf.Ticker(f"{symbol}{self.suffix}")
            data = ticker.history(period='1d', interval='1m')

            if not data.empty:
                return data['Close'].iloc[-1]
            return None

        except Exception as e:
            logger.error(f"Error getting live price for {symbol}: {str(e)}")
            return None

    def get_intraday_data(self, symbol, interval='5m'):
        """Get today's 5-min candle data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(f"{symbol}{self.suffix}")

            # Get today's data with 5-minute interval
            df = ticker.history(period='1d', interval='5m')

            if df.empty:
                logger.debug(f"No intraday data for {symbol}")
                return None

            # Rename columns to match our format
            df = df.reset_index()
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

            # Filter only today's data
            today = datetime.now().date()
            df['date'] = pd.to_datetime(df['date'])
            df = df[df['date'].dt.date == today]

            if len(df) < 3:
                logger.debug(f"Not enough candles for {symbol} ({len(df)} candles)")
                return None

            return df

        except Exception as e:
            logger.error(f"Error getting intraday data for {symbol}: {str(e)}")
            return None

    def get_historical_data(self, symbol, days=15):
        """Get last N days daily data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(f"{symbol}{self.suffix}")

            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+10)  # Extra buffer

            df = ticker.history(start=start_date, end=end_date, interval='1d')

            if df.empty:
                return None

            # Rename columns
            df = df.reset_index()
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'])

            return df.tail(days)

        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {str(e)}")
            return None

    def get_stock_info(self, symbol):
        """Get stock metadata from Yahoo Finance"""
        try:
            ticker = yf.Ticker(f"{symbol}{self.suffix}")
            info = ticker.info

            # Get recent data for volume calculation
            hist = ticker.history(period='30d')

            avg_volume = hist['Volume'].mean() if not hist.empty else 0
            current_price = hist['Close'].iloc[-1] if not hist.empty else 0
            avg_turnover = avg_volume * current_price

            return {
                'symbol': symbol,
                'price': current_price,
                'avg_volume': avg_volume,
                'avg_turnover': avg_turnover,
                'market_cap': info.get('marketCap', 0)
            }

        except Exception as e:
            logger.error(f"Error getting stock info for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'price': 0,
                'avg_volume': 0,
                'avg_turnover': 0,
                'market_cap': 0
            }


# ==================== NSE ADAPTER (FREE OFFICIAL DATA) ====================

class NSEAdapter(BrokerAdapter):
    """NSE India - Official FREE Data Source"""

    def __init__(self, config):
        super().__init__(config)
        self.name = "NSE India (FREE)"

    def connect(self):
        """No connection needed - it's free!"""
        if not NSEPY_AVAILABLE:
            logger.error("nsepy not installed. Run: pip install nsepy")
            return False

        self.is_connected = True
        logger.info(f"✅ Connected to {self.name} - Official NSE Data!")
        return True

    def get_live_price(self, symbol):
        """Get current live price from NSE"""
        try:
            quote = get_quote(symbol)
            if quote and 'lastPrice' in quote:
                return quote['lastPrice']
            return None
        except Exception as e:
            logger.debug(f"Error getting NSE live price for {symbol}: {str(e)}")
            return None

    def get_intraday_data(self, symbol, interval='5m'):
        """
        NSE doesn't provide intraday candles via nsepy
        Returns None - use Yahoo Finance for 5-min candles
        """
        logger.debug("NSE doesn't provide 5-min candles. Use Yahoo Finance.")
        return None

    def get_historical_data(self, symbol, days=15):
        """Get last N days daily data from NSE"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days+10)  # Extra buffer

            df = get_history(
                symbol=symbol,
                start=start_date,
                end=end_date
            )

            if df.empty:
                return None

            # Rename columns to match our format
            df = df.reset_index()
            df.columns = [col.lower() for col in df.columns]

            # Ensure we have required columns
            if 'date' not in df.columns:
                df.rename(columns={'index': 'date'}, inplace=True)

            df['date'] = pd.to_datetime(df['date'])

            # Select only needed columns
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]

            return df.tail(days)

        except Exception as e:
            logger.error(f"Error getting NSE historical data for {symbol}: {str(e)}")
            return None

    def get_stock_info(self, symbol):
        """Get stock metadata from NSE"""
        try:
            # Get recent historical data to calculate averages
            hist = self.get_historical_data(symbol, days=30)

            if hist is None or hist.empty:
                return {
                    'symbol': symbol,
                    'price': 0,
                    'avg_volume': 0,
                    'avg_turnover': 0
                }

            avg_volume = hist['volume'].mean()
            current_price = hist['close'].iloc[-1]
            avg_turnover = avg_volume * current_price

            return {
                'symbol': symbol,
                'price': current_price,
                'avg_volume': avg_volume,
                'avg_turnover': avg_turnover
            }

        except Exception as e:
            logger.error(f"Error getting NSE stock info for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'price': 0,
                'avg_volume': 0,
                'avg_turnover': 0
            }


# ==================== HYBRID NSE + YAHOO ADAPTER (BEST OF BOTH) ====================

class HybridNSEYahooAdapter(BrokerAdapter):
    """
    HYBRID: Combines NSE (official) + Yahoo Finance (5-min candles)

    Strategy:
    - Uses Yahoo Finance for 5-minute intraday candles (only source available)
    - Uses NSE for daily data verification (more accurate)
    - Uses NSE for live quotes when available
    - Falls back gracefully if either source fails
    """

    def __init__(self, config):
        super().__init__(config)
        self.name = "Hybrid NSE+Yahoo (BEST FREE)"
        self.nse = NSEAdapter(config)
        self.yahoo = YahooFinanceAdapter(config)
        self.use_nse_for_daily = True  # Prefer NSE for daily data

    def connect(self):
        """Connect to both sources"""
        yahoo_ok = self.yahoo.connect()
        nse_ok = self.nse.connect()

        if yahoo_ok or nse_ok:
            self.is_connected = True
            logger.info(f"✅ Connected to {self.name}")
            logger.info(f"   Yahoo Finance: {'✅' if yahoo_ok else '❌'}")
            logger.info(f"   NSE Official: {'✅' if nse_ok else '❌'}")
            return True
        else:
            logger.error("❌ Failed to connect to both Yahoo and NSE")
            return False

    def get_live_price(self, symbol):
        """Get live price - prefer NSE, fallback to Yahoo"""
        # Try NSE first (more accurate, official)
        if self.nse.is_connected:
            price = self.nse.get_live_price(symbol)
            if price:
                return price

        # Fallback to Yahoo Finance
        if self.yahoo.is_connected:
            return self.yahoo.get_live_price(symbol)

        return None

    def get_intraday_data(self, symbol, interval='5m'):
        """
        Get 5-min candles - ONLY Yahoo provides this
        NSE doesn't have intraday candle API
        """
        if self.yahoo.is_connected:
            return self.yahoo.get_intraday_data(symbol, interval)

        logger.error("Yahoo Finance not available - cannot fetch 5-min candles")
        return None

    def get_historical_data(self, symbol, days=15):
        """Get daily historical data - prefer NSE, fallback to Yahoo"""
        # Try NSE first (official, more accurate)
        if self.nse.is_connected and self.use_nse_for_daily:
            data = self.nse.get_historical_data(symbol, days)
            if data is not None and not data.empty:
                logger.debug(f"Using NSE data for {symbol}")
                return data

        # Fallback to Yahoo Finance
        if self.yahoo.is_connected:
            logger.debug(f"Using Yahoo data for {symbol}")
            return self.yahoo.get_historical_data(symbol, days)

        return None

    def get_stock_info(self, symbol):
        """Get stock info - prefer NSE, fallback to Yahoo"""
        # Try NSE first
        if self.nse.is_connected:
            info = self.nse.get_stock_info(symbol)
            if info and info['price'] > 0:
                return info

        # Fallback to Yahoo
        if self.yahoo.is_connected:
            return self.yahoo.get_stock_info(symbol)

        return {
            'symbol': symbol,
            'price': 0,
            'avg_volume': 0,
            'avg_turnover': 0
        }


# ==================== ZERODHA KITE ADAPTER (OPTIONAL) ====================

class ZerodhaAdapter(BrokerAdapter):
    """Zerodha Kite Connect API adapter"""

    def __init__(self, config):
        super().__init__(config)
        self.name = "Zerodha Kite"
        self.kite = None

    def connect(self):
        """Connect to Kite API"""
        try:
            from kiteconnect import KiteConnect

            api_key = self.config['api_key']
            access_token = self.config.get('access_token', '')

            self.kite = KiteConnect(api_key=api_key)

            if access_token:
                self.kite.set_access_token(access_token)
                self.is_connected = True
                logger.info(f"✅ Connected to {self.name}")
                return True
            else:
                logger.warning("Access token not found. Please login first.")
                return False

        except ImportError:
            logger.error("KiteConnect library not installed. Run: pip install kiteconnect")
            return False
        except Exception as e:
            logger.error(f"Error connecting to Kite: {str(e)}")
            return False

    def get_live_price(self, symbol):
        """Get current LTP"""
        try:
            quote = self.kite.quote(f"NSE:{symbol}")
            return quote[f"NSE:{symbol}"]["last_price"]
        except Exception as e:
            logger.error(f"Error getting live price for {symbol}: {str(e)}")
            return None

    def get_intraday_data(self, symbol, interval='5minute'):
        """Get today's 5-min candle data"""
        try:
            from_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            to_date = datetime.now()

            data = self.kite.historical_data(
                instrument_token=self.get_instrument_token(symbol),
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )

            df = pd.DataFrame(data)
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'])

            return df

        except Exception as e:
            logger.error(f"Error getting intraday data for {symbol}: {str(e)}")
            return None

    def get_historical_data(self, symbol, days=15):
        """Get last N days daily data"""
        try:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days+10)  # Extra buffer

            data = self.kite.historical_data(
                instrument_token=self.get_instrument_token(symbol),
                from_date=from_date,
                to_date=to_date,
                interval='day'
            )

            df = pd.DataFrame(data)
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'])

            return df.tail(days)

        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {str(e)}")
            return None

    def get_stock_info(self, symbol):
        """Get stock metadata"""
        try:
            quote = self.kite.quote(f"NSE:{symbol}")
            data = quote[f"NSE:{symbol}"]

            # Calculate average volume (approximate from available data)
            avg_volume = data.get('average_price', 0) * data.get('volume', 0)

            return {
                'symbol': symbol,
                'price': data['last_price'],
                'avg_volume': data.get('volume', 0),  # Today's volume as proxy
                'avg_turnover': avg_volume,
                'oi': data.get('oi', 0)
            }

        except Exception as e:
            logger.error(f"Error getting stock info for {symbol}: {str(e)}")
            return None

    def get_instrument_token(self, symbol):
        """Get instrument token for symbol"""
        # This should be cached from instruments dump
        # For now, return symbol (implement proper token mapping)
        return symbol


# ==================== ANGEL ONE ADAPTER ====================

class AngelOneAdapter(BrokerAdapter):
    """Angel One SmartAPI adapter"""

    def __init__(self, config):
        super().__init__(config)
        self.name = "Angel One"
        self.smart_api = None

    def connect(self):
        """Connect to Angel One SmartAPI"""
        try:
            from SmartApi import SmartConnect

            api_key = self.config['api_key']
            self.smart_api = SmartConnect(api_key=api_key)

            # Login
            data = self.smart_api.generateSession(
                self.config['client_id'],
                self.config['password']
            )

            if data['status']:
                self.is_connected = True
                logger.info(f"✅ Connected to {self.name}")
                return True
            else:
                logger.error(f"Failed to connect to {self.name}")
                return False

        except ImportError:
            logger.error("SmartApi library not installed. Run: pip install smartapi-python")
            return False
        except Exception as e:
            logger.error(f"Error connecting to Angel One: {str(e)}")
            return False

    def get_live_price(self, symbol):
        """Get LTP from Angel One"""
        try:
            token = self.get_token(symbol)
            data = self.smart_api.ltpData("NSE", symbol, token)
            return data['data']['ltp']
        except Exception as e:
            logger.error(f"Error getting live price: {str(e)}")
            return None

    def get_intraday_data(self, symbol, interval='FIVE_MINUTE'):
        """Get intraday candles"""
        try:
            token = self.get_token(symbol)
            from_date = datetime.now().replace(hour=9, minute=0)
            to_date = datetime.now()

            params = {
                "exchange": "NSE",
                "symboltoken": token,
                "interval": interval,
                "fromdate": from_date.strftime('%Y-%m-%d %H:%M'),
                "todate": to_date.strftime('%Y-%m-%d %H:%M')
            }

            data = self.smart_api.getCandleData(params)

            if data['status']:
                df = pd.DataFrame(data['data'])
                df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
                df['date'] = pd.to_datetime(df['date'])
                return df
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting intraday data: {str(e)}")
            return None

    def get_historical_data(self, symbol, days=15):
        """Get historical data"""
        # Implementation similar to intraday with daily interval
        pass

    def get_stock_info(self, symbol):
        """Get stock info"""
        # Implementation using quote API
        pass

    def get_token(self, symbol):
        """Get token for symbol"""
        # Implement token mapping
        return symbol


# ==================== UPSTOX ADAPTER ====================

class UpstoxAdapter(BrokerAdapter):
    """Upstox API adapter"""

    def __init__(self, config):
        super().__init__(config)
        self.name = "Upstox"

    def connect(self):
        """Connect to Upstox"""
        try:
            from upstox_client import Configuration, ApiClient

            configuration = Configuration()
            configuration.access_token = self.config.get('access_token', '')

            self.api_client = ApiClient(configuration)
            self.is_connected = True
            logger.info(f"✅ Connected to {self.name}")
            return True

        except ImportError:
            logger.error("upstox_client not installed. Run: pip install upstox-python-sdk")
            return False
        except Exception as e:
            logger.error(f"Error connecting to Upstox: {str(e)}")
            return False

    def get_live_price(self, symbol):
        # Implement using Upstox quote API
        pass

    def get_intraday_data(self, symbol, interval='5m'):
        # Implement using Upstox historical API
        pass

    def get_historical_data(self, symbol, days=15):
        # Implement
        pass

    def get_stock_info(self, symbol):
        # Implement
        pass


# ==================== FYERS ADAPTER ====================

class FyersAdapter(BrokerAdapter):
    """Fyers API adapter"""

    def __init__(self, config):
        super().__init__(config)
        self.name = "Fyers"

    def connect(self):
        """Connect to Fyers"""
        try:
            from fyers_api import fyersModel

            self.fyers = fyersModel.FyersModel(
                client_id=self.config['app_id'],
                token=self.config.get('access_token', ''),
                is_async=False
            )

            self.is_connected = True
            logger.info(f"✅ Connected to {self.name}")
            return True

        except ImportError:
            logger.error("fyers-api not installed. Run: pip install fyers-api")
            return False
        except Exception as e:
            logger.error(f"Error connecting to Fyers: {str(e)}")
            return False

    def get_live_price(self, symbol):
        # Implement
        pass

    def get_intraday_data(self, symbol, interval='5'):
        # Implement
        pass

    def get_historical_data(self, symbol, days=15):
        # Implement
        pass

    def get_stock_info(self, symbol):
        # Implement
        pass


# ==================== DATA HANDLER (MAIN CLASS) ====================

class DataHandler:
    """
    Main data handler - manages broker connection and data fetching
    """

    def __init__(self, broker_name=None):
        """
        Initialize data handler

        Args:
            broker_name: Name of broker to use (default from config)
        """
        self.broker_name = broker_name or BROKER
        self.broker = None
        self.cache = {}
        self.cache_timestamps = {}

        self._init_broker()

    def _init_broker(self):
        """Initialize data source adapter"""
        broker_config = get_broker_config()

        adapters = {
            'free': HybridNSEYahooAdapter,  # Default: Best of both worlds!
            'hybrid': HybridNSEYahooAdapter,
            'nse': NSEAdapter,
            'yahoo': YahooFinanceAdapter,
            'yfinance': YahooFinanceAdapter,
            'zerodha': ZerodhaAdapter,
            'angel': AngelOneAdapter,
            'upstox': UpstoxAdapter,
            'fyers': FyersAdapter
        }

        adapter_class = adapters.get(self.broker_name.lower())

        if adapter_class:
            self.broker = adapter_class(broker_config)
            logger.info(f"Initialized {self.broker.name} adapter")
        else:
            # Default to Yahoo Finance if broker not recognized
            logger.warning(f"Unknown broker '{self.broker_name}', using Yahoo Finance (FREE)")
            self.broker = YahooFinanceAdapter(broker_config)

    def connect(self):
        """Connect to broker"""
        return self.broker.connect()

    def get_live_price(self, symbol):
        """Get current price with caching"""
        cache_key = f"price_{symbol}"

        if ENABLE_CACHE and cache_key in self.cache:
            timestamp = self.cache_timestamps[cache_key]
            if (datetime.now() - timestamp).seconds < 5:  # 5 second cache
                return self.cache[cache_key]

        price = self.broker.get_live_price(symbol)

        if ENABLE_CACHE and price:
            self.cache[cache_key] = price
            self.cache_timestamps[cache_key] = datetime.now()

        return price

    def get_intraday_candles(self, symbol):
        """Get today's 5-min candles"""
        cache_key = f"intraday_{symbol}"

        if ENABLE_CACHE and cache_key in self.cache:
            timestamp = self.cache_timestamps[cache_key]
            if (datetime.now() - timestamp).seconds < 60:  # 1 minute cache
                return self.cache[cache_key]

        candles = self.broker.get_intraday_data(symbol, CANDLE_INTERVAL)

        if candles is not None and not candles.empty:
            # Add VWAP
            candles['vwap'] = self._calculate_vwap(candles)

            if ENABLE_CACHE:
                self.cache[cache_key] = candles
                self.cache_timestamps[cache_key] = datetime.now()

        return candles

    def get_historical_data(self, symbol, days=15):
        """Get historical daily data"""
        cache_key = f"hist_{symbol}_{days}"

        if ENABLE_CACHE and cache_key in self.cache:
            timestamp = self.cache_timestamps[cache_key]
            if (datetime.now() - timestamp).seconds < CACHE_DURATION_SECONDS:
                return self.cache[cache_key]

        hist_data = self.broker.get_historical_data(symbol, days)

        if ENABLE_CACHE and hist_data is not None:
            self.cache[cache_key] = hist_data
            self.cache_timestamps[cache_key] = datetime.now()

        return hist_data

    def get_stock_info(self, symbol):
        """Get stock metadata"""
        return self.broker.get_stock_info(symbol)

    def _calculate_vwap(self, candles_df):
        """Calculate VWAP"""
        try:
            typical_price = (candles_df['high'] + candles_df['low'] + candles_df['close']) / 3
            vwap = (typical_price * candles_df['volume']).cumsum() / candles_df['volume'].cumsum()
            return vwap
        except Exception as e:
            logger.error(f"Error calculating VWAP: {str(e)}")
            return pd.Series([0] * len(candles_df))

    def clear_cache(self):
        """Clear all cached data"""
        self.cache = {}
        self.cache_timestamps = {}
        logger.info("Cache cleared")


# ==================== F&O STOCK LIST MANAGER ====================

def load_fno_stocks():
    """Load F&O stock list"""
    try:
        if os.path.exists(FNO_STOCKS_FILE):
            with open(FNO_STOCKS_FILE, 'r') as f:
                stocks = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(stocks)} F&O stocks from file")
            return stocks
        else:
            logger.warning(f"F&O stocks file not found, using backup list")
            return FNO_STOCKS_BACKUP

    except Exception as e:
        logger.error(f"Error loading F&O stocks: {str(e)}")
        return FNO_STOCKS_BACKUP


if __name__ == "__main__":
    # Test data handler
    print("Data Handler Module Loaded")
    handler = DataHandler()
    print(f"✅ Broker: {handler.broker.name}")

    # Load F&O stocks
    stocks = load_fno_stocks()
    print(f"✅ Loaded {len(stocks)} F&O stocks")
