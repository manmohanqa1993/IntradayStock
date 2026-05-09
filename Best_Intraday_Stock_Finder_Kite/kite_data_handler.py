"""
Kite Data Handler - Zerodha Kite Connect Integration
=====================================================
Real-time data from Zerodha Kite API
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import time

try:
    from kiteconnect import KiteConnect
    KITE_AVAILABLE = True
except ImportError:
    KITE_AVAILABLE = False
    print("⚠️ kiteconnect not installed. Run: pip install kiteconnect")

from config import *

logger = logging.getLogger(__name__)


# ==================== KITE ADAPTER ====================

class KiteDataHandler:
    """Zerodha Kite Connect API Handler"""

    def __init__(self, config):
        self.config = config
        self.name = "Zerodha Kite Connect"
        self.kite = None
        self.is_connected = False
        self.instrument_tokens = {}  # Cache for instrument tokens
        self.cache = {}
        self.cache_timestamps = {}

    def connect(self):
        """Connect to Kite API"""
        if not KITE_AVAILABLE:
            logger.error("❌ KiteConnect library not installed")
            print("❌ KiteConnect library not installed")
            print("Install it: pip install kiteconnect")
            return False

        try:
            api_key = self.config['api_key']
            api_secret = self.config['api_secret']
            access_token = self.config.get('access_token', '')

            if not api_key or api_key == 'your_kite_api_key_here':
                logger.error("❌ Kite API key not configured in config.py")
                print("❌ Kite API key not configured in config.py")
                print("\n📝 How to fix:")
                print("1. Open config.py")
                print("2. Set KITE_CONFIG['api_key'] = 'your_actual_key'")
                print("3. Set KITE_CONFIG['api_secret'] = 'your_actual_secret'")
                return False

            self.kite = KiteConnect(api_key=api_key)

            # If access token exists, use it
            if access_token:
                self.kite.set_access_token(access_token)

                # Verify token is valid
                try:
                    profile = self.kite.profile()
                    self.is_connected = True
                    logger.info(f"✅ Connected to {self.name}")
                    print(f"✅ Connected to {self.name}")
                    print(f"👤 User: {profile.get('user_name', 'N/A')}")
                    print(f"📧 Email: {profile.get('email', 'N/A')}")

                    # Load instrument tokens
                    self._load_instruments()

                    return True

                except Exception as e:
                    logger.warning(f"Access token invalid or expired: {str(e)}")
                    print(f"⚠️ Access token invalid or expired")
                    access_token = ''  # Will trigger manual login

            # Manual login required
            if not access_token:
                print("\n🔐 KITE LOGIN REQUIRED")
                print("=" * 50)
                print("\n📝 Steps to login:")
                print("1. Open this URL in browser:")

                login_url = self.kite.login_url()
                print(f"\n{login_url}\n")

                print("2. Login with your Zerodha credentials")
                print("3. After login, you'll be redirected to a URL like:")
                print("   http://127.0.0.1/?request_token=XXXXXX&action=login")
                print("\n4. Copy the 'request_token' from URL and paste below:")

                request_token = input("\n🔑 Enter request_token: ").strip()

                if not request_token:
                    logger.error("No request token provided")
                    print("❌ No request token provided")
                    return False

                # Generate access token
                data = self.kite.generate_session(request_token, api_secret=api_secret)
                access_token = data['access_token']

                self.kite.set_access_token(access_token)

                # Save to config for future use
                print(f"\n✅ Login successful!")
                print(f"\n💾 IMPORTANT: Save this access token to config.py:")
                print(f"   KITE_CONFIG['access_token'] = '{access_token}'")
                print(f"\n⚠️ Token expires at end of day - you'll need to re-login tomorrow")

                # Update config
                self.config['access_token'] = access_token

                # Verify connection
                profile = self.kite.profile()
                self.is_connected = True

                logger.info(f"✅ Connected to {self.name}")
                print(f"\n👤 Logged in as: {profile.get('user_name', 'N/A')}")

                # Load instrument tokens
                self._load_instruments()

                return True

        except Exception as e:
            logger.error(f"❌ Error connecting to Kite: {str(e)}")
            print(f"❌ Error connecting to Kite: {str(e)}")
            return False

    def _load_instruments(self):
        """Load instrument tokens for faster lookup"""
        try:
            print("📥 Loading instrument list from Kite...")
            instruments = self.kite.instruments("NSE")

            # Create symbol -> token mapping
            for inst in instruments:
                if inst['segment'] == 'NSE':
                    symbol = inst['tradingsymbol']
                    self.instrument_tokens[symbol] = inst['instrument_token']

            logger.info(f"Loaded {len(self.instrument_tokens)} NSE instruments")
            print(f"✅ Loaded {len(self.instrument_tokens)} NSE instruments")

        except Exception as e:
            logger.warning(f"Could not load instruments: {str(e)}")
            print(f"⚠️ Could not load instruments: {str(e)}")

    def get_instrument_token(self, symbol):
        """Get instrument token for symbol"""
        if symbol in self.instrument_tokens:
            return self.instrument_tokens[symbol]

        # Try to fetch if not cached
        try:
            instruments = self.kite.instruments("NSE")
            for inst in instruments:
                if inst['tradingsymbol'] == symbol and inst['segment'] == 'NSE':
                    token = inst['instrument_token']
                    self.instrument_tokens[symbol] = token
                    return token
        except Exception as e:
            logger.error(f"Could not find token for {symbol}: {str(e)}")

        return None

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
        cache_key = f"intraday_{symbol}_{interval}"

        # Check cache
        if ENABLE_CACHE and cache_key in self.cache:
            timestamp = self.cache_timestamps[cache_key]
            if (datetime.now() - timestamp).seconds < CACHE_DURATION_SECONDS:
                return self.cache[cache_key]

        try:
            token = self.get_instrument_token(symbol)
            if not token:
                logger.warning(f"No instrument token found for {symbol}")
                return None

            from_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            to_date = datetime.now()

            data = self.kite.historical_data(
                instrument_token=token,
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )

            if not data:
                logger.debug(f"No intraday data for {symbol}")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(data)
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'])

            # Add VWAP
            df['vwap'] = self._calculate_vwap(df)

            # Cache it
            if ENABLE_CACHE:
                self.cache[cache_key] = df
                self.cache_timestamps[cache_key] = datetime.now()

            return df

        except Exception as e:
            logger.error(f"Error getting intraday data for {symbol}: {str(e)}")
            return None

    def get_historical_data(self, symbol, days=15):
        """Get last N days daily data"""
        cache_key = f"hist_{symbol}_{days}"

        # Check cache
        if ENABLE_CACHE and cache_key in self.cache:
            timestamp = self.cache_timestamps[cache_key]
            if (datetime.now() - timestamp).seconds < CACHE_DURATION_SECONDS:
                return self.cache[cache_key]

        try:
            token = self.get_instrument_token(symbol)
            if not token:
                return None

            to_date = datetime.now()
            from_date = to_date - timedelta(days=days+10)  # Extra buffer for weekends

            data = self.kite.historical_data(
                instrument_token=token,
                from_date=from_date,
                to_date=to_date,
                interval='day'
            )

            if not data:
                return None

            df = pd.DataFrame(data)
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date'] = pd.to_datetime(df['date'])

            # Cache it
            if ENABLE_CACHE:
                self.cache[cache_key] = df.tail(days)
                self.cache_timestamps[cache_key] = datetime.now()

            return df.tail(days)

        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {str(e)}")
            return None

    def get_stock_info(self, symbol):
        """Get stock metadata"""
        try:
            quote = self.kite.quote(f"NSE:{symbol}")
            data = quote[f"NSE:{symbol}"]

            # Get historical data for averages
            hist = self.get_historical_data(symbol, days=30)

            if hist is not None and not hist.empty:
                avg_volume = hist['volume'].mean()
                current_price = data['last_price']
                avg_turnover = avg_volume * current_price
            else:
                avg_volume = data.get('volume', 0)
                current_price = data['last_price']
                avg_turnover = avg_volume * current_price

            return {
                'symbol': symbol,
                'price': current_price,
                'avg_volume': avg_volume,
                'avg_turnover': avg_turnover,
                'oi': data.get('oi', 0),
                'ohlc': data.get('ohlc', {})
            }

        except Exception as e:
            logger.error(f"Error getting stock info for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'price': 0,
                'avg_volume': 0,
                'avg_turnover': 0,
                'oi': 0
            }

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
    # Test Kite connection
    print("Kite Data Handler Test")
    print("=" * 50)

    config = get_kite_config()
    handler = KiteDataHandler(config)

    if handler.connect():
        print("\n✅ Connection successful!")

        # Test data fetch
        print("\nTesting data fetch for RELIANCE...")
        candles = handler.get_intraday_data('RELIANCE')

        if candles is not None:
            print(f"✅ Fetched {len(candles)} candles")
            print(f"Latest close: ₹{candles['close'].iloc[-1]:.2f}")
        else:
            print("❌ Could not fetch data")
    else:
        print("\n❌ Connection failed")
