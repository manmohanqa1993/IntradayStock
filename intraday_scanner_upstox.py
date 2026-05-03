"""
NSE Intraday Stock Scanner - UPSTOX REAL-TIME VERSION (FREE)
Uses Upstox API for live tick-by-tick data
FREE for Upstox account holders!
"""

import upstox_client
from upstox_client.rest import ApiException
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIGURATION ====================
# Get these from https://developer.upstox.com/
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
ACCESS_TOKEN = "your_access_token_here"  # Generated after login
REDIRECT_URI = "http://127.0.0.1:5000"

# Import complete F&O stock list
try:
    from nse_fno_stocks import NSE_FNO_SYMBOLS
    NSE_STOCKS = NSE_FNO_SYMBOLS
except ImportError:
    # Fallback to basic list if import fails
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
api_instance = None
instrument_map = {}

# ==================== INITIALIZATION ====================

def initialize_upstox():
    """Initialize Upstox client"""
    global api_instance

    configuration = upstox_client.Configuration()
    configuration.access_token = ACCESS_TOKEN

    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

    print("✅ Upstox API initialized (FREE!)")
    return api_instance

def get_instrument_key(symbol):
    """Convert symbol to Upstox instrument key format"""
    # Upstox format: NSE_EQ|INE002A01018 or NSE_EQ|{SYMBOL}
    return f"NSE_EQ|{symbol}"

# ==================== TECHNICAL INDICATORS ====================

def calculate_vwap(df):
    """Calculate VWAP"""
    df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
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

def get_historical_data(symbol, from_date, to_date):
    """Fetch historical intraday data from Upstox"""
    try:
        instrument_key = get_instrument_key(symbol)

        # Create historical API instance
        configuration = upstox_client.Configuration()
        configuration.access_token = ACCESS_TOKEN
        history_api = upstox_client.HistoryApi(upstox_client.ApiClient(configuration))

        # Fetch data (5-minute interval)
        api_response = history_api.get_historical_candle_data1(
            instrument_key=instrument_key,
            interval="5minute",
            to_date=to_date.strftime("%Y-%m-%d"),
            from_date=from_date.strftime("%Y-%m-%d")
        )

        if not api_response.data or not api_response.data.candles:
            return None

        # Convert to DataFrame
        candles = api_response.data.candles
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'oi'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df = df.sort_index()

        return df

    except ApiException as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return None

def get_live_quote(symbol):
    """Get real-time quote from Upstox"""
    try:
        instrument_key = get_instrument_key(symbol)

        # Fetch live quote
        api_response = api_instance.get_full_market_quote(instrument_key)

        if not api_response.data:
            return None

        # Extract quote data
        quote_data = api_response.data[instrument_key]

        return {
            'ltp': quote_data.last_price,
            'open': quote_data.ohlc.open,
            'high': quote_data.ohlc.high,
            'low': quote_data.ohlc.low,
            'close': quote_data.ohlc.close,
            'prev_close': quote_data.ohlc.close,  # Previous close
            'volume': quote_data.volume,
            'bid': quote_data.depth.buy[0].price if quote_data.depth and quote_data.depth.buy else 0,
            'ask': quote_data.depth.sell[0].price if quote_data.depth and quote_data.depth.sell else 0,
            'avg_price': quote_data.average_price if hasattr(quote_data, 'average_price') else quote_data.last_price
        }

    except ApiException as e:
        print(f"Error fetching quote for {symbol}: {e}")
        return None

# ==================== ANALYSIS ====================

def analyze_stock_realtime(symbol):
    """Analyze a single stock with real-time Upstox data"""

    # Get historical data (last 5 days)
    to_date = datetime.now()
    from_date = to_date - timedelta(days=5)

    df = get_historical_data(symbol, from_date, to_date)

    if df is None or len(df) < 50:
        return None

    # Get live quote
    quote = get_live_quote(symbol)
    if not quote:
        return None

    # Current metrics
    current_price = quote['ltp']
    current_volume = quote['volume']
    prev_close = quote['prev_close']

    # Calculate indicators
    df = calculate_vwap(df)
    df['ema_20'] = calculate_ema(df['close'], 20)
    df['ema_50'] = calculate_ema(df['close'], 50)
    df['rsi'] = calculate_rsi(df['close'])
    df['macd'], df['macd_signal'] = calculate_macd(df['close'])
    df['atr'] = calculate_atr(df)

    # Latest values
    latest = df.iloc[-1]
    vwap = latest['vwap']
    ema_20 = latest['ema_20']
    ema_50 = latest['ema_50']
    rsi = latest['rsi']
    macd = latest['macd']
    macd_signal = latest['macd_signal']
    atr = latest['atr']

    # Calculate metrics
    pct_change = ((current_price - prev_close) / prev_close) * 100
    gap = abs(pct_change)

    # Average volume
    avg_volume = df['volume'].mean()
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0

    # Opening Range
    or_high = df['high'].head(3).max()
    or_low = df['low'].head(3).min()

    # Previous day high/low
    prev_day_high = quote['high']
    prev_day_low = quote['low']

    # ATR percentage
    atr_pct = (atr / current_price) * 100 if current_price > 0 else 0

    # VWAP position
    vwap_position = "Above" if current_price > vwap else "Below"
    vwap_distance = abs(current_price - vwap) / vwap * 100

    # Determine direction and criteria
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
        'Bid': round(quote['bid'], 2),
        'Ask': round(quote['ask'], 2),
        'LTP': round(current_price, 2)
    }

# ==================== SCANNER ====================

def scan_market_realtime():
    """Scan market with real-time Upstox data"""
    print("\n" + "="*100)
    print(f"🟢 LIVE NSE SCANNER - UPSTOX API (FREE) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    print("⚡ Using REAL-TIME data with ZERO delay (Upstox API)")
    print(f"Universe: {len(NSE_STOCKS)} stocks\n")

    opportunities = []
    processed = 0

    for symbol in NSE_STOCKS:
        processed += 1
        print(f"Scanning: {symbol} ({processed}/{len(NSE_STOCKS)})", end='\r')

        result = analyze_stock_realtime(symbol)
        if result:
            opportunities.append(result)

        # Rate limiting - Upstox allows 10 requests/sec
        time.sleep(0.15)

    print("\n")

    if not opportunities:
        print("⚠️  No stocks meeting criteria found.")
        print("Try scanning at different times or adjust criteria.\n")
        return

    # Separate bullish and bearish opportunities
    bullish_opps = [opp for opp in opportunities if opp['Direction'] == 'BULLISH']
    bearish_opps = [opp for opp in opportunities if opp['Direction'] == 'BEARISH']

    # Sort by score
    bullish_opps.sort(key=lambda x: x['Score'], reverse=True)
    bearish_opps.sort(key=lambda x: x['Score'], reverse=True)

    # Limit to top 10 each
    bullish_opps = bullish_opps[:10]
    bearish_opps = bearish_opps[:10]

    print(f"✅ Found {len(bullish_opps)} Bullish + {len(bearish_opps)} Bearish Opportunities\n")

    # ==================== BULLISH SECTION ====================
    if bullish_opps:
        print("="*100)
        print(f"🟢 BULLISH OPPORTUNITIES ({len(bullish_opps)} stocks) - LIVE DATA")
        print("="*100)

        for i, opp in enumerate(bullish_opps, 1):
            print(f"\n{i}. {opp['Symbol']} - 🚀 {opp['Direction']} (REAL-TIME)")
            print(f"   LTP: ₹{opp['LTP']} | Bid: ₹{opp['Bid']} | Ask: ₹{opp['Ask']}")
            print(f"   Change: {opp['Change%']:+.2f}% | Volume: {opp['Volume_Ratio']:.2f}x avg")
            print(f"   VWAP: ₹{opp['VWAP']} ({opp['VWAP_Position']}) | RSI: {opp['RSI']} | ATR: {opp['ATR%']:.2f}%")
            print(f"   Setup: {opp['Setup']}")
            print(f"   Quality Score: {opp['Score']}/8 ⭐")
            print(f"   EMA20: ₹{opp['EMA20']} | EMA50: ₹{opp['EMA50']}")

        print("\n" + "="*100)
    else:
        print("\n🟢 No bullish opportunities found at this time.\n")

    print("\n")

    # ==================== BEARISH SECTION ====================
    if bearish_opps:
        print("="*100)
        print(f"🔴 BEARISH OPPORTUNITIES ({len(bearish_opps)} stocks) - LIVE DATA")
        print("="*100)

        for i, opp in enumerate(bearish_opps, 1):
            print(f"\n{i}. {opp['Symbol']} - 📉 {opp['Direction']} (REAL-TIME)")
            print(f"   LTP: ₹{opp['LTP']} | Bid: ₹{opp['Bid']} | Ask: ₹{opp['Ask']}")
            print(f"   Change: {opp['Change%']:+.2f}% | Volume: {opp['Volume_Ratio']:.2f}x avg")
            print(f"   VWAP: ₹{opp['VWAP']} ({opp['VWAP_Position']}) | RSI: {opp['RSI']} | ATR: {opp['ATR%']:.2f}%")
            print(f"   Setup: {opp['Setup']}")
            print(f"   Quality Score: {opp['Score']}/8 ⭐")
            print(f"   EMA20: ₹{opp['EMA20']} | EMA50: ₹{opp['EMA50']}")

        print("\n" + "="*100)
    else:
        print("\n🔴 No bearish opportunities found at this time.\n")

    print("\n💡 Real-time Upstox data - Perfect for intraday trading!")
    print("💰 FREE for Upstox account holders")
    print("⚠️  Always use stop-loss. This is not financial advice.\n")

    # Save results
    df_results = pd.DataFrame(opportunities)
    filename = f"upstox_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_results.to_csv(filename, index=False)
    print(f"📊 Results saved to: {filename}\n")

# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n🚀 Initializing Upstox Real-Time Scanner (FREE!)...")
    print("="*100)

    # Initialize Upstox
    try:
        initialize_upstox()
        # Run scan
        scan_market_realtime()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure to:")
        print("1. Install upstox_client: pip install upstox-client")
        print("2. Generate access token (see upstox_login.py)")
        print("3. Update API credentials in this file\n")
