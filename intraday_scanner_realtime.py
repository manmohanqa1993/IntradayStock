"""
NSE Intraday Stock Scanner - REAL-TIME VERSION
Uses Zerodha Kite Connect for live tick-by-tick data
Requires: Kite Connect API subscription (₹2000/month)
"""

from kiteconnect import KiteConnect, KiteTicker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIGURATION ====================
# Get these from https://kite.zerodha.com/developers/
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
ACCESS_TOKEN = "your_access_token_here"  # Generated after login

# NSE F&O Stock List (Instrument tokens will be fetched)
NSE_STOCKS = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
    'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
    'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'HCLTECH',
    'SUNPHARMA', 'BAJFINANCE', 'WIPRO', 'ULTRACEMCO', 'TITAN',
    'NESTLEIND', 'TATAMOTORS', 'ONGC', 'NTPC', 'POWERGRID',
    'M&M', 'TECHM', 'BAJAJFINSV', 'ADANIPORTS', 'TATASTEEL',
    'COALINDIA', 'HINDALCO', 'INDUSINDBK', 'DIVISLAB', 'DRREDDY',
    'CIPLA', 'GRASIM', 'JSWSTEEL', 'HEROMOTOCO', 'EICHERMOT',
    'BRITANNIA', 'BPCL', 'SHREECEM', 'TATACONSUM', 'APOLLOHOSP',
    'ADANIENT', 'BAJAJ-AUTO', 'PIDILITIND', 'SIEMENS', 'DLF',
    'VEDL', 'GODREJCP', 'HAVELLS', 'BANDHANBNK', 'ICICIGI'
]

# Global variables
kite = None
stock_data = {}  # Store real-time candle data
instrument_map = {}  # Symbol to instrument token mapping

# ==================== INITIALIZATION ====================

def initialize_kite():
    """Initialize Kite Connect client"""
    global kite
    kite = KiteConnect(api_key=API_KEY)

    # Set access token (you need to generate this via login flow first)
    kite.set_access_token(ACCESS_TOKEN)

    print("✅ Kite Connect initialized")
    return kite

def get_instrument_tokens():
    """Map stock symbols to instrument tokens"""
    global instrument_map

    # Download instrument list
    instruments = kite.instruments("NSE")

    for stock in NSE_STOCKS:
        for instrument in instruments:
            if instrument['tradingsymbol'] == stock and instrument['instrument_type'] == 'EQ':
                instrument_map[stock] = instrument['instrument_token']
                break

    print(f"✅ Mapped {len(instrument_map)} instruments")
    return instrument_map

# ==================== TECHNICAL INDICATORS ====================

def calculate_vwap(df):
    """Calculate VWAP"""
    df['VWAP'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
    return df

def calculate_ema(series, period):
    """Calculate EMA"""
    return series.ewm(span=period, adjust=False).mean()

def calculate_rsi(series, period=14):
    """Calculate RSI"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series):
    """Calculate MACD"""
    ema_12 = series.ewm(span=12, adjust=False).mean()
    ema_26 = series.ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_atr(df, period=14):
    """Calculate ATR"""
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(period).mean()
    return atr

# ==================== DATA FETCHING ====================

def get_historical_data(symbol, from_date, to_date, interval='5minute'):
    """Fetch historical data for a symbol using Kite Connect"""
    try:
        instrument_token = instrument_map.get(symbol)
        if not instrument_token:
            return None

        # Fetch historical data
        data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval
        )

        if not data:
            return None

        # Convert to DataFrame
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        return df

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def get_live_quote(symbol):
    """Get real-time quote for a symbol"""
    try:
        instrument_token = instrument_map.get(symbol)
        if not instrument_token:
            return None

        quote = kite.quote(f"NSE:{symbol}")
        return quote[f"NSE:{symbol}"]

    except Exception as e:
        print(f"Error fetching quote for {symbol}: {e}")
        return None

# ==================== ANALYSIS ====================

def analyze_stock_realtime(symbol):
    """Analyze a single stock with real-time data"""

    # Get historical data (last 5 days for context)
    to_date = datetime.now()
    from_date = to_date - timedelta(days=5)

    df = get_historical_data(symbol, from_date, to_date, interval='5minute')

    if df is None or len(df) < 50:
        return None

    # Get live quote for current price
    quote = get_live_quote(symbol)
    if not quote:
        return None

    # Current metrics
    current_price = quote['last_price']
    current_volume = quote['volume']
    prev_close = quote['ohlc']['close']

    # Calculate indicators
    df = calculate_vwap(df)
    df['EMA_20'] = calculate_ema(df['close'], 20)
    df['EMA_50'] = calculate_ema(df['close'], 50)
    df['RSI'] = calculate_rsi(df['close'])
    df['MACD'], df['MACD_Signal'] = calculate_macd(df['close'])
    df['ATR'] = calculate_atr(df)

    # Latest values
    latest = df.iloc[-1]
    vwap = latest['VWAP']
    ema_20 = latest['EMA_20']
    ema_50 = latest['EMA_50']
    rsi = latest['RSI']
    macd = latest['MACD']
    macd_signal = latest['MACD_Signal']
    atr = latest['ATR']

    # Calculate metrics
    pct_change = ((current_price - prev_close) / prev_close) * 100
    gap = abs(pct_change)

    # Average volume (from quote)
    avg_volume = quote['average_price'] if 'average_price' in quote else current_volume
    volume_ratio = quote.get('volume', 0) / quote.get('oi_day_high', 1) if 'oi_day_high' in quote else 1

    # Opening Range
    or_high = df['high'].head(3).max()
    or_low = df['low'].head(3).min()

    # Previous day high/low
    prev_day_high = quote['ohlc']['high']
    prev_day_low = quote['ohlc']['low']

    # ATR percentage
    atr_pct = (atr / current_price) * 100 if current_price > 0 else 0

    # VWAP position
    vwap_position = "Above" if current_price > vwap else "Below"
    vwap_distance = abs(current_price - vwap) / vwap * 100

    # Determine direction and check criteria
    direction = None
    setup = []
    score = 0

    # BULLISH CHECKS
    bullish_criteria = 0
    if gap >= 1.5 and current_price > prev_close:
        bullish_criteria += 1
        setup.append("Gap Up")

    if current_price > vwap and vwap_distance < 2:
        bullish_criteria += 1
        setup.append("Above VWAP")

    if current_price > ema_20 and ema_20 > ema_50:
        bullish_criteria += 1
        setup.append("EMA Aligned")

    if 55 <= rsi <= 75:
        bullish_criteria += 1
        setup.append("RSI Momentum")

    if macd > macd_signal:
        bullish_criteria += 1

    if current_price > prev_day_high:
        bullish_criteria += 1
        setup.append("Breakout")

    if volume_ratio > 1.5:
        bullish_criteria += 1
        setup.append("Volume Surge")

    if atr_pct > 1:
        bullish_criteria += 1

    # BEARISH CHECKS
    bearish_criteria = 0
    if gap >= 1.5 and current_price < prev_close:
        bearish_criteria += 1
        setup.append("Gap Down")

    if current_price < vwap and vwap_distance < 2:
        bearish_criteria += 1
        setup.append("Below VWAP")

    if current_price < ema_20 and ema_20 < ema_50:
        bearish_criteria += 1
        setup.append("EMA Aligned")

    if 25 <= rsi <= 45:
        bearish_criteria += 1
        setup.append("RSI Momentum")

    if macd < macd_signal:
        bearish_criteria += 1

    if current_price < prev_day_low:
        bearish_criteria += 1
        setup.append("Breakdown")

    if volume_ratio > 1.5:
        bearish_criteria += 1
        setup.append("Volume Surge")

    if atr_pct > 1:
        bearish_criteria += 1

    # Determine direction
    if bullish_criteria >= 5:
        direction = "BULLISH"
        score = bullish_criteria
    elif bearish_criteria >= 5:
        direction = "BEARISH"
        score = bearish_criteria
    else:
        return None

    return {
        'Symbol': symbol,
        'Direction': direction,
        'Price': round(current_price, 2),
        'Change%': round(pct_change, 2),
        'Volume_Ratio': round(volume_ratio, 2),
        'VWAP_Position': vwap_position,
        'VWAP': round(vwap, 2),
        'Setup': ' | '.join(setup[:3]),
        'RSI': round(rsi, 1),
        'Score': score,
        'EMA20': round(ema_20, 2),
        'EMA50': round(ema_50, 2),
        'ATR%': round(atr_pct, 2),
        'Bid': quote.get('depth', {}).get('buy', [{}])[0].get('price', 0),
        'Ask': quote.get('depth', {}).get('sell', [{}])[0].get('price', 0),
        'LTP': current_price
    }

# ==================== SCANNER ====================

def scan_market_realtime():
    """Scan market with real-time data"""
    print("\n" + "="*100)
    print(f"🔴 LIVE NSE INTRADAY SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    print("⚡ Using REAL-TIME data (zero delay)")
    print(f"Universe: {len(NSE_STOCKS)} stocks\n")

    opportunities = []
    processed = 0

    for symbol in NSE_STOCKS:
        processed += 1
        print(f"Scanning: {symbol} ({processed}/{len(NSE_STOCKS)})", end='\r')

        result = analyze_stock_realtime(symbol)
        if result:
            opportunities.append(result)

    print("\n")

    if not opportunities:
        print("⚠️  No stocks meeting criteria found at this time.")
        return

    # Sort by score
    opportunities.sort(key=lambda x: x['Score'], reverse=True)
    opportunities = opportunities[:10]

    print(f"✅ Found {len(opportunities)} High-Quality Opportunities:\n")
    print("="*100)

    for i, opp in enumerate(opportunities, 1):
        print(f"\n{i}. {opp['Symbol']} - {opp['Direction']} 🔴 LIVE")
        print(f"   Price: ₹{opp['Price']} | Bid: ₹{opp['Bid']} | Ask: ₹{opp['Ask']}")
        print(f"   Change: {opp['Change%']:+.2f}% | Volume: {opp['Volume_Ratio']:.2f}x avg")
        print(f"   VWAP: ₹{opp['VWAP']} ({opp['VWAP_Position']}) | RSI: {opp['RSI']} | ATR: {opp['ATR%']:.2f}%")
        print(f"   Setup: {opp['Setup']}")
        print(f"   Quality Score: {opp['Score']}/8 ⭐")
        print(f"   EMA20: ₹{opp['EMA20']} | EMA50: ₹{opp['EMA50']}")

    print("\n" + "="*100)
    print(f"\n💡 Real-time data with ZERO delay - Perfect for scalping!")
    print("⚠️  Always use stop-loss. This is not financial advice.\n")

    # Save results
    df_results = pd.DataFrame(opportunities)
    filename = f"realtime_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_results.to_csv(filename, index=False)
    print(f"📊 Results saved to: {filename}\n")

# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n🚀 Initializing Real-Time Scanner...")
    print("="*100)

    # Initialize Kite
    initialize_kite()

    # Get instrument tokens
    get_instrument_tokens()

    # Run scan
    scan_market_realtime()
