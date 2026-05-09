"""
Configuration - Basic Scanner
==============================
Simple settings for beginners
"""

from datetime import time

# ==================== DATA SOURCE ====================
DATA_SOURCE = "yahoo"  # Yahoo Finance (FREE)

# ==================== MARKET TIMINGS ====================
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)
SCAN_START = time(9, 20)
SCAN_END = time(15, 0)

# ==================== STRATEGY SETTINGS ====================
# Simplified 5-point strategy for beginners
MIN_VOLUME_RATIO = 1.2          # 20% above average
MAX_GAP_PERCENT = 0.5            # Max 0.5% gap
MIN_MOMENTUM_CANDLES = 3         # 3 out of 5 candles
MAX_PULLBACK_CANDLES = 1         # Max 1 pullback
VWAP_STRICT = True               # Must respect VWAP

# ==================== SCANNING ====================
SCAN_INTERVAL_SECONDS = 120      # Scan every 2 minutes (slower for beginners)
CANDLE_INTERVAL = '5m'           # 5-minute candles

# ==================== SIGNALS ====================
MIN_SIGNAL_STRENGTH = 6          # Lower threshold (more signals for learning)
MAX_SIGNALS_DISPLAY = 10         # Show top 10 signals

# ==================== RISK MANAGEMENT ====================
RISK_REWARD_RATIO = 2.0          # 1:2 R:R
SL_METHOD = 'vwap'               # Stop-loss based on VWAP

# ==================== ALERTS ====================
ENABLE_CONSOLE_ALERTS = True
ENABLE_SOUND_ALERTS = True
ENABLE_TELEGRAM = False          # Disabled by default

# ==================== OUTPUT ====================
SAVE_SIGNALS = True
SIGNALS_DIR = 'output'
LOG_DIR = 'logs'

# ==================== STOCKS ====================
STOCKS_FILE = 'config/stocks.txt'

# Backup stock list (Top 25 liquid F&O stocks)
STOCKS_BACKUP = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
    'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
    'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'HCLTECH',
    'SUNPHARMA', 'BAJFINANCE', 'WIPRO', 'ULTRACEMCO', 'TITAN',
    'NESTLEIND', 'TATAMOTORS', 'ONGC', 'NTPC', 'POWERGRID'
]

# ==================== HELPER FUNCTIONS ====================

def is_market_open():
    from datetime import datetime
    now = datetime.now().time()
    return MARKET_OPEN <= now <= MARKET_CLOSE

def is_scanning_time():
    from datetime import datetime
    now = datetime.now().time()
    return SCAN_START <= now <= SCAN_END

import os
def create_directories():
    os.makedirs(SIGNALS_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

# Create directories on import
create_directories()

print("✅ Configuration loaded - Basic Scanner")
print(f"📊 Data Source: Yahoo Finance (FREE)")
print(f"📈 Scanning: {len(STOCKS_BACKUP)} stocks")
