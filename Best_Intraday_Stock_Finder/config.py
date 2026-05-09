"""
Configuration File for Best Intraday Stock Finder
================================================
All strategy parameters and broker settings in one place
"""

import os
from datetime import time

# ==================== DATA SOURCE CONFIGURATION ====================

# Select your data source
# Options:
#   "free" or "hybrid" - HYBRID NSE+Yahoo (BEST FREE - NO API KEYS!)
#                        Uses NSE for official daily data + Yahoo for 5-min candles
#   "nse"              - NSE only (daily data only, no 5-min candles)
#   "yahoo"            - Yahoo Finance only
#   "zerodha", "angel", "upstox", "fyers" - Broker APIs (requires API keys)

BROKER = "free"  # FREE Hybrid NSE+Yahoo - Best of both worlds!

# FREE API Configuration (Hybrid NSE + Yahoo)
FREE_CONFIG = {
    # No configuration needed - completely free!
    'note': 'Hybrid uses NSE (official daily data) + Yahoo Finance (5-min candles)',
    'nse_for_daily': True,  # Use NSE for historical daily data
    'yahoo_for_intraday': True  # Use Yahoo for 5-min candles
}

# Broker API Credentials (Optional - only if using paid brokers)
ZERODHA_CONFIG = {
    'api_key': 'your_kite_api_key',
    'api_secret': 'your_kite_api_secret',
    'access_token': ''  # Generated after login
}

ANGEL_CONFIG = {
    'api_key': 'your_angel_api_key',
    'client_id': 'your_client_id',
    'password': 'your_password',
    'totp_secret': ''
}

UPSTOX_CONFIG = {
    'api_key': 'your_upstox_api_key',
    'api_secret': 'your_upstox_secret',
    'redirect_uri': 'http://127.0.0.1:5000'
}

FYERS_CONFIG = {
    'app_id': 'your_fyers_app_id',
    'secret_id': 'your_fyers_secret',
    'redirect_uri': 'http://127.0.0.1:5000'
}

# ==================== MARKET SETTINGS ====================

# Market hours (IST)
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)

# Scanning window (when to start looking for signals)
SCAN_START_TIME = time(9, 20)  # After first candle completes
SCAN_END_TIME = time(15, 0)    # Stop scanning before close

# Candle timeframe
CANDLE_INTERVAL = '5min'  # 5-minute candles
CANDLE_INTERVAL_SECONDS = 300

# ==================== STRATEGY PARAMETERS ====================

# 1. RELATIVE VOLUME FILTER
VOLUME_LOOKBACK_DAYS = 15  # Compare with 15-day average
MIN_VOLUME_RATIO = 1.0     # Current volume must be > average (1.0 = 100%)

# 2. LIQUIDITY FILTER
MIN_AVG_DAILY_VOLUME = 500000      # Minimum 5 lakh shares/day
MIN_AVG_DAILY_TURNOVER = 10000000  # Minimum 1 crore daily turnover
MIN_PRICE = 50                      # Avoid penny stocks
MAX_PRICE = 50000                   # Avoid ultra high-price stocks

# 3. GAP FILTER
MAX_GAP_PERCENT = 0.5  # Maximum 0.5% gap allowed

# 4. FIRST CANDLE MOVE FILTER
MAX_FIRST_CANDLE_MOVE = 2.0  # Maximum 2% first candle move

# 5. THREE-CANDLE REVERSAL
CANDLE_PATTERN_WINDOW = 3  # First 3 candles for pattern

# 6. MOMENTUM CONTINUATION
MOMENTUM_OBSERVATION_CANDLES = 5  # Observe next 4-5 candles
MIN_MOMENTUM_CANDLES = 3          # At least 3 out of 5 should be in direction

# 7. PULLBACK VALIDATION
MAX_PULLBACK_CANDLES = 1  # Only 1 pullback candle allowed

# 8. VWAP CONFIRMATION
VWAP_STRICT_MODE = True  # All candles must respect VWAP (True/False)

# ==================== SCANNING SETTINGS ====================

# Scan interval (how often to check for signals)
SCAN_INTERVAL_SECONDS = 60  # Scan every 60 seconds

# Number of stocks to scan in parallel
MAX_CONCURRENT_SCANS = 10

# Cache settings
ENABLE_CACHE = True
CACHE_DURATION_SECONDS = 300  # 5 minutes

# ==================== SIGNAL SETTINGS ====================

# Minimum signal strength (0-10 scale)
MIN_SIGNAL_STRENGTH = 7

# Signal expiry (how long signal remains valid)
SIGNAL_EXPIRY_MINUTES = 15

# Maximum signals to show
MAX_SIGNALS_DISPLAY = 20

# ==================== ALERT SETTINGS ====================

# Telegram alerts
ENABLE_TELEGRAM = False
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
TELEGRAM_CHAT_ID = 'your_telegram_chat_id'

# Sound alerts
ENABLE_SOUND_ALERTS = True
ALERT_SOUND_FILE = 'alert.wav'  # Place in same directory

# Console alerts
ENABLE_CONSOLE_ALERTS = True

# ==================== RISK MANAGEMENT ====================

# Auto stop-loss and target calculation
AUTO_CALCULATE_SL_TARGET = True

# Risk-reward ratio
RISK_REWARD_RATIO = 2.0  # 1:2 risk-reward

# Stop-loss based on
SL_METHOD = 'vwap'  # Options: 'vwap', 'previous_candle_low', 'atr', 'percentage'
SL_PERCENTAGE = 1.0  # If SL_METHOD = 'percentage'
SL_ATR_MULTIPLIER = 1.5  # If SL_METHOD = 'atr'

# ==================== F&O STOCK LIST ====================

# Will be loaded from NSE F&O list
# Keep this updated with current F&O stocks
FNO_STOCKS_FILE = 'fno_stocks_list.txt'

# Or use this hardcoded list (backup)
FNO_STOCKS_BACKUP = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
    'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
    'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'HCLTECH',
    'SUNPHARMA', 'BAJFINANCE', 'WIPRO', 'ULTRACEMCO', 'TITAN',
    'NESTLEIND', 'TATAMOTORS', 'ONGC', 'NTPC', 'POWERGRID',
    'M&M', 'TECHM', 'BAJAJFINSV', 'ADANIPORTS', 'TATASTEEL',
    'COALINDIA', 'HINDALCO', 'INDUSINDBK', 'DIVISLAB', 'DRREDDY',
    'CIPLA', 'GRASIM', 'JSWSTEEL', 'HEROMOTOCO', 'EICHERMOT',
    'BRITANNIA', 'BPCL', 'SHREECEM', 'TATACONSUM', 'APOLLOHOSP',
    'ADANIENT', 'BAJAJ-AUTO', 'HDFCLIFE', 'SBILIFE', 'BANKBARODA'
]

# ==================== BACKTESTING SETTINGS ====================

BACKTEST_START_DATE = '2024-01-01'
BACKTEST_END_DATE = '2024-12-31'
BACKTEST_INITIAL_CAPITAL = 100000
BACKTEST_POSITION_SIZE_PERCENT = 10  # 10% of capital per trade

# ==================== LOGGING SETTINGS ====================

LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'screener.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Log rotation
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# ==================== OUTPUT SETTINGS ====================

# Save signals to file
SAVE_SIGNALS_TO_FILE = True
SIGNALS_OUTPUT_DIR = 'signals_output'

# CSV format
SAVE_AS_CSV = True
CSV_FILENAME_FORMAT = 'signals_{date}.csv'

# JSON format
SAVE_AS_JSON = True
JSON_FILENAME_FORMAT = 'signals_{date}.json'

# ==================== PERFORMANCE SETTINGS ====================

# Multi-threading
USE_MULTITHREADING = True
MAX_WORKERS = 5

# Memory optimization
CLEAR_OLD_DATA_AFTER_MINUTES = 30

# ==================== NIFTY/BANKNIFTY TREND CONFIRMATION ====================

# Use market trend as filter
USE_MARKET_TREND_FILTER = True

# Market indices to track
TRACK_NIFTY = True
TRACK_BANKNIFTY = True

# Trend determination
MARKET_TREND_EMA_FAST = 9
MARKET_TREND_EMA_SLOW = 21

# Only take trades aligned with market
ONLY_TRADE_WITH_MARKET_TREND = False  # Set True for conservative approach

# ==================== ADVANCED FILTERS ====================

# Additional quality filters
FILTER_BY_SECTOR_ROTATION = False  # Only scan hot sectors
MIN_RSI = 40  # Avoid oversold
MAX_RSI = 80  # Avoid overbought

# Volatility filter
USE_ATR_FILTER = True
MIN_ATR_PERCENT = 0.5  # Minimum volatility
MAX_ATR_PERCENT = 5.0  # Maximum volatility

# ==================== UI SETTINGS ====================

# Dashboard
ENABLE_DASHBOARD = False  # Set True if you want web dashboard
DASHBOARD_PORT = 8050
DASHBOARD_HOST = '127.0.0.1'

# Refresh rate
DASHBOARD_REFRESH_SECONDS = 5

# ==================== HELPER FUNCTIONS ====================

def get_broker_config():
    """Get active data source configuration"""
    broker_configs = {
        'free': FREE_CONFIG,
        'yahoo': FREE_CONFIG,
        'yfinance': FREE_CONFIG,
        'zerodha': ZERODHA_CONFIG,
        'angel': ANGEL_CONFIG,
        'upstox': UPSTOX_CONFIG,
        'fyers': FYERS_CONFIG
    }
    return broker_configs.get(BROKER.lower(), FREE_CONFIG)

def is_market_open():
    """Check if market is currently open"""
    from datetime import datetime
    now = datetime.now().time()
    return MARKET_OPEN <= now <= MARKET_CLOSE

def is_scanning_time():
    """Check if it's time to scan for signals"""
    from datetime import datetime
    now = datetime.now().time()
    return SCAN_START_TIME <= now <= SCAN_END_TIME

def create_output_directories():
    """Create necessary output directories"""
    os.makedirs(SIGNALS_OUTPUT_DIR, exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)

# ==================== VALIDATION ====================

def validate_config():
    """Validate configuration parameters"""
    errors = []

    if MAX_GAP_PERCENT < 0:
        errors.append("MAX_GAP_PERCENT must be positive")

    if MAX_FIRST_CANDLE_MOVE < 0:
        errors.append("MAX_FIRST_CANDLE_MOVE must be positive")

    if MIN_VOLUME_RATIO < 0:
        errors.append("MIN_VOLUME_RATIO must be positive")

    if RISK_REWARD_RATIO < 1:
        errors.append("RISK_REWARD_RATIO should be at least 1")

    if MAX_PULLBACK_CANDLES < 0:
        errors.append("MAX_PULLBACK_CANDLES must be non-negative")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

    return True

# Run validation on import
validate_config()

# Create directories on import
create_output_directories()

print("✅ Configuration loaded successfully")
print(f"📊 Data Source: {BROKER.upper()}")
if BROKER.lower() in ['free', 'hybrid']:
    print("🆓 Using HYBRID NSE+Yahoo (BEST FREE!) - No setup required!")
    print("   📍 NSE Official: Daily data + Live quotes")
    print("   📊 Yahoo Finance: 5-minute candles")
elif BROKER.lower() in ['yahoo', 'yfinance']:
    print("🆓 Using FREE Yahoo Finance API - No setup required!")
elif BROKER.lower() == 'nse':
    print("🆓 Using NSE Official Data - No setup required!")
print(f"🕒 Scan window: {SCAN_START_TIME} to {SCAN_END_TIME}")
print(f"📈 Candle interval: {CANDLE_INTERVAL}")
print(f"🎯 Min signal strength: {MIN_SIGNAL_STRENGTH}/10")
