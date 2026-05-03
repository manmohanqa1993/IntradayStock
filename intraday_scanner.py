"""
NSE Intraday Stock Scanner
Identifies high-probability intraday trading opportunities based on technical criteria
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import complete F&O stock list
try:
    from nse_fno_stocks import NSE_FNO_STOCKS
except ImportError:
    # Fallback to basic list if import fails
    NSE_FNO_STOCKS = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
        'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS',
        'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'HCLTECH.NS',
        'SUNPHARMA.NS', 'BAJFINANCE.NS', 'WIPRO.NS', 'ULTRACEMCO.NS', 'TITAN.NS',
        'NESTLEIND.NS', 'TATAMOTORS.NS', 'ONGC.NS', 'NTPC.NS', 'POWERGRID.NS',
        'M&M.NS', 'TECHM.NS', 'BAJAJFINSV.NS', 'ADANIPORTS.NS', 'TATASTEEL.NS',
        'COALINDIA.NS', 'HINDALCO.NS', 'INDUSINDBK.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
        'CIPLA.NS', 'GRASIM.NS', 'JSWSTEEL.NS', 'HEROMOTOCO.NS', 'EICHERMOT.NS',
        'BRITANNIA.NS', 'BPCL.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'APOLLOHOSP.NS',
        'ADANIENT.NS', 'BAJAJ-AUTO.NS', 'PIDILITIND.NS', 'SIEMENS.NS', 'DLF.NS',
        'VEDL.NS', 'GODREJCP.NS', 'HAVELLS.NS', 'BANDHANBNK.NS', 'ICICIGI.NS',
        'SBILIFE.NS', 'HDFCLIFE.NS', 'DABUR.NS', 'MARICO.NS', 'AMBUJACEM.NS',
        'ACC.NS', 'BIOCON.NS', 'BERGEPAINT.NS', 'GAIL.NS', 'INDIGO.NS',
        'BANKBARODA.NS', 'PNB.NS', 'CANBK.NS', 'FEDERALBNK.NS', 'IDEA.NS',
        'SAIL.NS', 'NMDC.NS', 'BEL.NS', 'BHEL.NS', 'PFC.NS'
    ]

def calculate_vwap(df):
    """Calculate VWAP"""
    df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
    return df

def calculate_ema(df, period):
    """Calculate EMA"""
    return df['Close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(df, period=14):
    """Calculate RSI"""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(df):
    """Calculate MACD"""
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_atr(df, period=14):
    """Calculate ATR"""
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(period).mean()
    return atr

def get_stock_data(symbol, period='5d', interval='5m'):
    """Fetch stock data from yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)

        if df.empty or len(df) < 50:
            return None

        # Get previous day's close
        daily_data = ticker.history(period='10d', interval='1d')
        if len(daily_data) >= 2:
            prev_close = daily_data['Close'].iloc[-2]
        else:
            prev_close = df['Close'].iloc[0]

        return df, prev_close, ticker.info
    except Exception as e:
        return None

def analyze_stock(symbol):
    """Analyze a single stock against all criteria"""

    data = get_stock_data(symbol)
    if data is None:
        return None

    df, prev_close, info = data

    # Current metrics
    current_price = df['Close'].iloc[-1]
    current_volume = df['Volume'].sum()

    # Calculate indicators
    df = calculate_vwap(df)
    df['EMA_20'] = calculate_ema(df, 20)
    df['EMA_50'] = calculate_ema(df, 50)
    df['RSI'] = calculate_rsi(df)
    df['MACD'], df['MACD_Signal'] = calculate_macd(df)
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

    # Previous candles
    prev_candle = df.iloc[-2]

    # Calculate metrics
    pct_change = ((current_price - prev_close) / prev_close) * 100
    gap = abs(pct_change)

    # Average volume (last 20 days worth of 5-min candles)
    avg_volume = df['Volume'].tail(100).mean() * 78  # Approximate daily volume
    volume_ratio = (current_volume / avg_volume) if avg_volume > 0 else 0

    # Opening Range (first 3 candles = 15 min)
    or_high = df['High'].head(3).max()
    or_low = df['Low'].head(3).min()

    # Previous day high/low estimate
    prev_day_high = df['High'].tail(78).max()
    prev_day_low = df['Low'].tail(78).min()

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

    if current_price > or_high or current_price > prev_day_high:
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

    if current_price < or_low or current_price < prev_day_low:
        bearish_criteria += 1
        setup.append("Breakdown")

    if volume_ratio > 1.5:
        bearish_criteria += 1
        setup.append("Volume Surge")

    if atr_pct > 1:
        bearish_criteria += 1

    # Determine direction based on stronger criteria
    if bullish_criteria >= 5:
        direction = "BULLISH"
        score = bullish_criteria
    elif bearish_criteria >= 5:
        direction = "BEARISH"
        score = bearish_criteria
    else:
        return None  # Not enough criteria met

    # Filter low quality setups
    if volume_ratio < 1.5:
        return None

    if avg_volume < 1000000:
        return None

    # Get sector info
    sector = info.get('sector', 'Unknown')

    return {
        'Symbol': symbol.replace('.NS', ''),
        'Direction': direction,
        'Price': round(current_price, 2),
        'Change%': round(pct_change, 2),
        'Volume_Ratio': round(volume_ratio, 2),
        'VWAP_Position': vwap_position,
        'VWAP': round(vwap, 2),
        'Setup': ' | '.join(setup[:3]),  # Top 3 setups
        'RSI': round(rsi, 1),
        'Sector': sector,
        'Score': score,
        'EMA20': round(ema_20, 2),
        'EMA50': round(ema_50, 2),
        'ATR%': round(atr_pct, 2)
    }

def scan_market():
    """Scan entire market for opportunities"""
    print("\n" + "="*100)
    print(f"NSE INTRADAY SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    print("Scanning NSE F&O stocks for high-probability intraday setups...")
    print(f"Universe: {len(NSE_FNO_STOCKS)} stocks\n")

    opportunities = []
    processed = 0

    for symbol in NSE_FNO_STOCKS:
        processed += 1
        print(f"Scanning: {symbol} ({processed}/{len(NSE_FNO_STOCKS)})", end='\r')

        result = analyze_stock(symbol)
        if result:
            opportunities.append(result)

    print("\n")

    if not opportunities:
        print("⚠️  No stocks meeting the criteria found at this time.")
        print("Market may be consolidating or criteria too strict.\n")
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
        print(f"🟢 BULLISH OPPORTUNITIES ({len(bullish_opps)} stocks)")
        print("="*100)

        for i, opp in enumerate(bullish_opps, 1):
            print(f"\n{i}. {opp['Symbol']} - 🚀 {opp['Direction']}")
            print(f"   Price: ₹{opp['Price']} | Change: {opp['Change%']:+.2f}% | Volume: {opp['Volume_Ratio']:.2f}x avg")
            print(f"   VWAP: ₹{opp['VWAP']} ({opp['VWAP_Position']}) | RSI: {opp['RSI']} | ATR: {opp['ATR%']:.2f}%")
            print(f"   Setup: {opp['Setup']}")
            print(f"   Sector: {opp['Sector']} | Quality Score: {opp['Score']}/8")
            print(f"   EMA20: ₹{opp['EMA20']} | EMA50: ₹{opp['EMA50']}")

        print("\n" + "="*100)
    else:
        print("\n🟢 No bullish opportunities found at this time.\n")

    print("\n")

    # ==================== BEARISH SECTION ====================
    if bearish_opps:
        print("="*100)
        print(f"🔴 BEARISH OPPORTUNITIES ({len(bearish_opps)} stocks)")
        print("="*100)

        for i, opp in enumerate(bearish_opps, 1):
            print(f"\n{i}. {opp['Symbol']} - 📉 {opp['Direction']}")
            print(f"   Price: ₹{opp['Price']} | Change: {opp['Change%']:+.2f}% | Volume: {opp['Volume_Ratio']:.2f}x avg")
            print(f"   VWAP: ₹{opp['VWAP']} ({opp['VWAP_Position']}) | RSI: {opp['RSI']} | ATR: {opp['ATR%']:.2f}%")
            print(f"   Setup: {opp['Setup']}")
            print(f"   Sector: {opp['Sector']} | Quality Score: {opp['Score']}/8")
            print(f"   EMA20: ₹{opp['EMA20']} | EMA50: ₹{opp['EMA50']}")

        print("\n" + "="*100)
    else:
        print("\n🔴 No bearish opportunities found at this time.\n")

    print("\n💡 Focus on top 5 setups with Score ≥ 6 for best probability")
    print("⚠️  Always use stop-loss and position sizing. This is not financial advice.\n")

    # Save to CSV
    df_results = pd.DataFrame(opportunities)
    filename = f"intraday_scan_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df_results.to_csv(filename, index=False)
    print(f"📊 Results saved to: {filename}\n")

if __name__ == "__main__":
    scan_market()
