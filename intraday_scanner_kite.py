"""
NSE Intraday Stock Scanner - KITE (ZERODHA) REAL-TIME VERSION
Uses Kite Connect API for live tick-by-tick data
Requires Zerodha trading account
"""

from kiteconnect import KiteConnect
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIGURATION ====================
# Get these from https://developers.kite.trade/
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
ACCESS_TOKEN = "your_access_token_here"  # Generated after login

# Import complete F&O stock list
try:
    from nse_fno_stocks import NSE_FNO_SYMBOLS
    NSE_STOCKS = NSE_FNO_SYMBOLS
except ImportError:
    NSE_STOCKS = [
        'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
        'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
        'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'HCLTECH',
        'SUNPHARMA', 'BAJFINANCE', 'WIPRO', 'ULTRACEMCO', 'TITAN'
    ]

# Global variables
kite = None
instrument_tokens = {}

# ==================== INITIALIZATION ====================

def initialize_kite():
    """Initialize Kite Connect client"""
    global kite

    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(ACCESS_TOKEN)

    print("✅ Kite Connect API initialized (Zerodha)")
    return kite

def get_instrument_token(symbol):
    """Get instrument token for a symbol"""
    global instrument_tokens

    # Cache instrument tokens
    if not instrument_tokens:
        instruments = kite.instruments("NSE")
        for inst in instruments:
            instrument_tokens[inst['tradingsymbol']] = inst['instrument_token']

    return instrument_tokens.get(symbol)

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
    """Fetch historical intraday data from Kite"""
    try:
        instrument_token = get_instrument_token(symbol)

        if not instrument_token:
            return None

        # Fetch 5-minute candles
        data = kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval="5minute"
        )

        if not data:
            return None

        # Convert to DataFrame
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df = df.sort_index()

        return df

    except Exception as e:
        # print(f"Error fetching historical data for {symbol}: {e}")
        return None

def get_live_quote(symbol):
    """Get real-time quote from Kite"""
    try:
        instrument_token = get_instrument_token(symbol)

        if not instrument_token:
            return None

        # Fetch live quote
        quote = kite.quote([f"NSE:{symbol}"])[f"NSE:{symbol}"]

        return {
            'ltp': quote['last_price'],
            'open': quote['ohlc']['open'],
            'high': quote['ohlc']['high'],
            'low': quote['ohlc']['low'],
            'close': quote['ohlc']['close'],
            'prev_close': quote['ohlc']['close'],
            'volume': quote['volume'],
            'bid': quote['depth']['buy'][0]['price'] if quote['depth']['buy'] else 0,
            'ask': quote['depth']['sell'][0]['price'] if quote['depth']['sell'] else 0,
            'avg_price': quote['average_price']
        }

    except Exception as e:
        # print(f"Error fetching quote for {symbol}: {e}")
        return None

# ==================== ANALYSIS ====================

def analyze_stock_kite(symbol):
    """Analyze a single stock with real-time Kite data"""

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

    # Price filter: Must be >₹100
    if current_price < 100:
        return None

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

    # FILTER: Remove stocks with >2% gap (too much gap up/down)
    if abs(pct_change) > 2.0:
        return None

    # FILTER: Momentum - Must be moving ±1.5%
    if abs(pct_change) < 1.5:
        return None

    # Average volume
    avg_volume = df['volume'].mean()
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0

    # FILTER: Volume must be 2x average
    if volume_ratio < 2.0:
        return None

    # FILTER: Average volume > 500,000 shares
    if avg_volume < 500000:
        return None

    # Opening Range
    or_high = df['high'].head(3).max()
    or_low = df['low'].head(3).min()

    # Day high/low
    day_high = quote['high']
    day_low = quote['low']

    # ATR percentage
    atr_pct = (atr / current_price) * 100 if current_price > 0 else 0

    # Intraday range
    intraday_range_pct = ((day_high - day_low) / current_price) * 100

    # FILTER: Volatility - ATR > 1% OR range > 1.5%
    if atr_pct < 1 and intraday_range_pct < 1.5:
        return None

    # VWAP position
    vwap_position = "Above" if current_price > vwap else "Below"

    # Determine direction and criteria
    direction = None
    setup = []
    score = 0
    reasons = []

    # ==================== BULLISH CHECKS ====================
    if pct_change > 1.5:
        bullish_score = 0
        bullish_reasons = []

        # VWAP (MUST)
        if current_price > vwap:
            bullish_score += 2
            bullish_reasons.append("✅ Price above VWAP")
        else:
            return None

        # EMA Trend (MUST)
        if ema_20 > ema_50:
            bullish_score += 2
            bullish_reasons.append("✅ 20 EMA > 50 EMA")
        else:
            return None

        # RSI (MUST be 50-70)
        if 50 <= rsi <= 70:
            bullish_score += 2
            bullish_reasons.append(f"✅ RSI: {rsi:.1f}")
        else:
            return None

        # MACD
        if macd > macd_signal:
            bullish_score += 1
            bullish_reasons.append("✅ MACD Bullish")

        # Breakout (at least one required)
        breakout = False
        if current_price > or_high:
            bullish_score += 1
            bullish_reasons.append("✅ OR Breakout")
            breakout = True
        if current_price >= day_high * 0.995:
            bullish_score += 1
            bullish_reasons.append("✅ At Day High")
            breakout = True

        if not breakout:
            return None

        # Near day high
        if current_price >= day_high * 0.98:
            bullish_score += 1
            bullish_reasons.append("✅ Near Day High")

        # Minimum score
        if bullish_score >= 8:
            direction = "BUY"
            reasons = bullish_reasons
            score = bullish_score

    # ==================== BEARISH CHECKS ====================
    elif pct_change < -1.5:
        bearish_score = 0
        bearish_reasons = []

        # VWAP (MUST)
        if current_price < vwap:
            bearish_score += 2
            bearish_reasons.append("✅ Price below VWAP")
        else:
            return None

        # EMA Trend (MUST)
        if ema_20 < ema_50:
            bearish_score += 2
            bearish_reasons.append("✅ 20 EMA < 50 EMA")
        else:
            return None

        # RSI (MUST be 30-50)
        if 30 <= rsi <= 50:
            bearish_score += 2
            bearish_reasons.append(f"✅ RSI: {rsi:.1f}")
        else:
            return None

        # MACD
        if macd < macd_signal:
            bearish_score += 1
            bearish_reasons.append("✅ MACD Bearish")

        # Breakdown (at least one required)
        breakdown = False
        if current_price < or_low:
            bearish_score += 1
            bearish_reasons.append("✅ OR Breakdown")
            breakdown = True
        if current_price <= day_low * 1.005:
            bearish_score += 1
            bearish_reasons.append("✅ At Day Low")
            breakdown = True

        if not breakdown:
            return None

        # Near day low
        if current_price <= day_low * 1.02:
            bearish_score += 1
            bearish_reasons.append("✅ Near Day Low")

        # Minimum score
        if bearish_score >= 8:
            direction = "SELL"
            reasons = bearish_reasons
            score = bearish_score

    if direction is None:
        return None

    # Calculate trade levels
    if direction == "BUY":
        entry = round(current_price, 2)
        stop_loss = round(min(day_low, current_price - (1.5 * atr)), 2)
        risk = entry - stop_loss
        target = round(entry + (2 * risk), 2)
    else:
        entry = round(current_price, 2)
        stop_loss = round(max(day_high, current_price + (1.5 * atr)), 2)
        risk = stop_loss - entry
        target = round(entry - (2 * risk), 2)

    rr_ratio = round(abs(target - entry) / abs(risk), 2) if risk > 0 else 0

    return {
        'Symbol': symbol,
        'Action': direction,
        'Entry': entry,
        'StopLoss': stop_loss,
        'Target': target,
        'Risk': round(abs(risk), 2),
        'Reward': round(abs(target - entry), 2),
        'RR_Ratio': rr_ratio,
        'Price': round(current_price, 2),
        'Change%': round(pct_change, 2),
        'Volume_Ratio': round(volume_ratio, 2),
        'VWAP_Position': vwap_position,
        'VWAP': round(vwap, 2),
        'RSI': round(rsi, 1),
        'Score': score,
        'EMA20': round(ema_20, 2),
        'EMA50': round(ema_50, 2),
        'ATR%': round(atr_pct, 2),
        'Bid': round(quote['bid'], 2),
        'Ask': round(quote['ask'], 2),
        'LTP': round(current_price, 2),
        'Reasons': reasons
    }

# ==================== SCANNER ====================

def scan_market_kite():
    """Scan market with real-time Kite data"""
    print("\n" + "="*120)
    print(f"🟢 LIVE NSE SCANNER - KITE/ZERODHA API - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*120 + "\n")
    print("⚡ Using REAL-TIME Zerodha data with ZERO delay")
    print(f"Universe: {len(NSE_STOCKS)} F&O stocks\n")

    opportunities = []
    processed = 0

    for symbol in NSE_STOCKS:
        processed += 1
        print(f"Scanning: {symbol} ({processed}/{len(NSE_STOCKS)})", end='\r')

        result = analyze_stock_kite(symbol)
        if result:
            opportunities.append(result)

        # Rate limiting
        time.sleep(0.1)

    print("\n")

    if not opportunities:
        print("⚠️  No high-quality setups found meeting ALL criteria.")
        print("Market conditions may not be favorable for trading right now.\n")
        return

    # Separate by action
    buy_setups = [opp for opp in opportunities if opp['Action'] == 'BUY']
    sell_setups = [opp for opp in opportunities if opp['Action'] == 'SELL']

    # Sort by score
    buy_setups.sort(key=lambda x: x['Score'], reverse=True)
    sell_setups.sort(key=lambda x: x['Score'], reverse=True)

    # Limit to top 3-5 total
    buy_setups = buy_setups[:3]
    sell_setups = sell_setups[:3]
    total_setups = buy_setups + sell_setups
    total_setups.sort(key=lambda x: x['Score'], reverse=True)
    total_setups = total_setups[:5]

    # Re-separate for display
    final_buy = [s for s in total_setups if s['Action'] == 'BUY']
    final_sell = [s for s in total_setups if s['Action'] == 'SELL']

    print(f"✅ Found {len(total_setups)} PREMIUM High-Probability Setups\n")

    # ==================== BUY SETUPS ====================
    if final_buy:
        print("="*120)
        print(f"🟢 BUY OPPORTUNITIES ({len(final_buy)} setups) - KITE LIVE DATA")
        print("="*120)

        for i, trade in enumerate(final_buy, 1):
            print(f"\n{i}. 🎯 {trade['Symbol']} - BUY SETUP (REAL-TIME)")
            print(f"   {'─'*115}")
            print(f"   📈 ENTRY:     ₹{trade['Entry']} | LTP: ₹{trade['LTP']} | Bid: ₹{trade['Bid']} | Ask: ₹{trade['Ask']}")
            print(f"   🛑 STOP LOSS: ₹{trade['StopLoss']} (Risk: ₹{trade['Risk']})")
            print(f"   🎯 TARGET:    ₹{trade['Target']} (Reward: ₹{trade['Reward']})")
            print(f"   💰 RISK-REWARD RATIO: 1:{trade['RR_Ratio']}")
            print(f"   {'─'*115}")
            print(f"   📊 Change: {trade['Change%']:+.2f}% | Vol: {trade['Volume_Ratio']:.1f}x | VWAP: ₹{trade['VWAP']}")
            print(f"   📉 RSI: {trade['RSI']} | ATR: {trade['ATR%']:.2f}% | EMA20: ₹{trade['EMA20']} | EMA50: ₹{trade['EMA50']}")
            print(f"   ⭐ Quality Score: {trade['Score']}/12")
            print(f"\n   ✅ REASONS FOR TRADE:")
            for reason in trade['Reasons']:
                print(f"      {reason}")

        print("\n" + "="*120)

    if final_buy and final_sell:
        print("\n")

    # ==================== SELL SETUPS ====================
    if final_sell:
        print("="*120)
        print(f"🔴 SELL OPPORTUNITIES ({len(final_sell)} setups) - KITE LIVE DATA")
        print("="*120)

        for i, trade in enumerate(final_sell, 1):
            print(f"\n{i}. 🎯 {trade['Symbol']} - SELL SETUP (REAL-TIME)")
            print(f"   {'─'*115}")
            print(f"   📉 ENTRY:     ₹{trade['Entry']} | LTP: ₹{trade['LTP']} | Bid: ₹{trade['Bid']} | Ask: ₹{trade['Ask']}")
            print(f"   🛑 STOP LOSS: ₹{trade['StopLoss']} (Risk: ₹{trade['Risk']})")
            print(f"   🎯 TARGET:    ₹{trade['Target']} (Reward: ₹{trade['Reward']})")
            print(f"   💰 RISK-REWARD RATIO: 1:{trade['RR_Ratio']}")
            print(f"   {'─'*115}")
            print(f"   📊 Change: {trade['Change%']:+.2f}% | Vol: {trade['Volume_Ratio']:.1f}x | VWAP: ₹{trade['VWAP']}")
            print(f"   📈 RSI: {trade['RSI']} | ATR: {trade['ATR%']:.2f}% | EMA20: ₹{trade['EMA20']} | EMA50: ₹{trade['EMA50']}")
            print(f"   ⭐ Quality Score: {trade['Score']}/12")
            print(f"\n   ✅ REASONS FOR TRADE:")
            for reason in trade['Reasons']:
                print(f"      {reason}")

        print("\n" + "="*120)

    print("\n")
    print("="*120)
    print("⚠️  PROFESSIONAL TRADING RULES")
    print("="*120)
    print("1. ALWAYS use the stop loss mentioned - No exceptions!")
    print("2. Risk only 1-2% of capital per trade")
    print("3. Wait for entry price or better - Don't chase")
    print("4. Book partial profits at 1:1 and move SL to entry")
    print("5. Exit if setup invalidates")
    print("6. This is NOT financial advice - Trade at your own risk")
    print("="*120 + "\n")

    # Save results in organized folder structure
    if total_setups:
        df_results = pd.DataFrame(total_setups)
        # Flatten reasons list to string
        df_results['Reasons'] = df_results['Reasons'].apply(lambda x: ' | '.join(x))

        # Create date-based folder structure
        date_folder = datetime.now().strftime('%Y-%m-%d')
        output_path = os.path.join('kite_scanner_output', date_folder)
        os.makedirs(output_path, exist_ok=True)

        # Save with time in filename
        filename = f"scan_{datetime.now().strftime('%H%M%S')}.csv"
        filepath = os.path.join(output_path, filename)
        df_results.to_csv(filepath, index=False)
        print(f"📊 Results saved to: {filepath}\n")

# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n🚀 Initializing Kite/Zerodha Real-Time Scanner...")
    print("="*120)

    # Initialize Kite
    try:
        initialize_kite()
        # Run scan
        scan_market_kite()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure to:")
        print("1. Install kiteconnect: pip install kiteconnect")
        print("2. Generate access token (see kite_login.py)")
        print("3. Update API credentials in this file")
        print("4. Have an active Zerodha trading account\n")
