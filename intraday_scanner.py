"""
NSE Intraday Stock Scanner - Enhanced Quality Rating System
Identifies TOP 5 high-quality bullish and TOP 5 bearish opportunities
Quality rating: 1-10 scale based on weighted criteria
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
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

def get_nifty_trend():
    """Analyze Nifty 50 trend to determine market direction"""
    try:
        nifty = yf.Ticker("^NSEI")
        df = nifty.history(period='5d', interval='5m')

        if df.empty or len(df) < 50:
            return "NEUTRAL"

        # Calculate EMAs
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()

        latest = df.iloc[-1]
        current_price = latest['Close']
        ema_20 = latest['EMA_20']
        ema_50 = latest['EMA_50']

        # Get previous day close
        daily_data = nifty.history(period='10d', interval='1d')
        if len(daily_data) >= 2:
            prev_close = daily_data['Close'].iloc[-2]
            pct_change = ((current_price - prev_close) / prev_close) * 100
        else:
            pct_change = 0

        # Determine trend
        if current_price > ema_20 and ema_20 > ema_50 and pct_change > 0:
            return "BULLISH"
        elif current_price < ema_20 and ema_20 < ema_50 and pct_change < 0:
            return "BEARISH"
        else:
            return "NEUTRAL"
    except:
        return "NEUTRAL"

def get_rating_label(score):
    """Convert score to rating label"""
    if score >= 8.5:
        return "⭐⭐⭐ EXCELLENT"
    elif score >= 7.0:
        return "⭐⭐ VERY GOOD"
    elif score >= 6.0:
        return "⭐ GOOD"
    else:
        return "FAIR"

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

def analyze_stock(symbol, nifty_trend):
    """Analyze a single stock with enhanced quality rating (1-10 scale)"""

    data = get_stock_data(symbol)
    if data is None:
        return None

    df, prev_close, info = data

    # Current metrics
    current_price = df['Close'].iloc[-1]
    current_volume = df['Volume'].sum()

    # QUALITY FILTER 1: Price must be > ₹100
    if current_price < 100:
        return None

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

    # Day high/low
    day_high = df['High'].max()
    day_low = df['Low'].min()

    # Calculate metrics
    pct_change = ((current_price - prev_close) / prev_close) * 100

    # QUALITY FILTER 2: Remove stocks with >2% gap (too risky)
    if abs(pct_change) > 2.0:
        return None

    # QUALITY FILTER 3: Must have minimum movement (1.5%)
    if abs(pct_change) < 1.5:
        return None

    # Average volume
    avg_volume = df['Volume'].tail(100).mean() * 78
    volume_ratio = (current_volume / avg_volume) if avg_volume > 0 else 0

    # QUALITY FILTER 4: Volume must be 1.5x average
    if volume_ratio < 1.5:
        return None

    # QUALITY FILTER 5: Minimum liquidity (1M shares daily)
    if avg_volume < 1000000:
        return None

    # Opening Range
    or_high = df['High'].head(3).max()
    or_low = df['Low'].head(3).min()

    # Previous day high/low
    prev_day_high = df['High'].tail(78).max()
    prev_day_low = df['Low'].tail(78).min()

    # ATR percentage
    atr_pct = (atr / current_price) * 100 if current_price > 0 else 0

    # Intraday range
    intraday_range_pct = ((day_high - day_low) / current_price) * 100

    # QUALITY FILTER 6: Volatility check
    if atr_pct < 0.5 and intraday_range_pct < 1.0:
        return None

    # VWAP position
    vwap_position = "Above" if current_price > vwap else "Below"
    vwap_distance = abs(current_price - vwap) / vwap * 100

    # Determine direction and calculate QUALITY SCORE (1-10 scale)
    direction = None
    setup = []
    quality_score = 0.0
    reasons = []

    # ==================== BULLISH QUALITY SCORING ====================
    if pct_change > 1.5:
        score = 0.0
        bullish_reasons = []

        # Criterion 1: VWAP Position (Max 2.0 points)
        if current_price > vwap:
            if vwap_distance < 1:
                score += 2.0
                bullish_reasons.append("Strong VWAP Support")
            else:
                score += 1.5
                bullish_reasons.append("Above VWAP")
            setup.append("Above VWAP")
        else:
            return None  # Must be above VWAP for bullish

        # Criterion 2: EMA Alignment (Max 2.0 points)
        if current_price > ema_20 and ema_20 > ema_50:
            ema_distance = ((ema_20 - ema_50) / ema_50) * 100
            if ema_distance > 1:
                score += 2.0
                bullish_reasons.append("Strong EMA Trend")
            else:
                score += 1.5
                bullish_reasons.append("EMA Aligned")
            setup.append("EMA Bullish")

        # Criterion 3: RSI Momentum (Max 2.0 points)
        if 55 <= rsi <= 75:
            if 60 <= rsi <= 70:
                score += 2.0
                bullish_reasons.append(f"Optimal RSI ({rsi:.1f})")
            else:
                score += 1.5
                bullish_reasons.append(f"RSI {rsi:.1f}")
            setup.append("RSI Momentum")

        # Criterion 4: MACD Confirmation (Max 1.0 point)
        if macd > macd_signal:
            macd_diff = abs(macd - macd_signal)
            if macd_diff > 0.5:
                score += 1.0
                bullish_reasons.append("Strong MACD")
            else:
                score += 0.5
                bullish_reasons.append("MACD+")

        # Criterion 5: Breakout Confirmation (Max 1.5 points)
        if current_price > or_high:
            score += 1.0
            bullish_reasons.append("OR Breakout")
            setup.append("Breakout")
        if current_price > prev_day_high:
            score += 0.5
            bullish_reasons.append("Prev Day High Break")

        # Criterion 6: Volume Strength (Max 1.0 point)
        if volume_ratio > 2.5:
            score += 1.0
            bullish_reasons.append("Huge Volume")
            setup.append("Volume Surge")
        elif volume_ratio > 2.0:
            score += 0.75
            bullish_reasons.append("Strong Volume")
        elif volume_ratio > 1.5:
            score += 0.5
            bullish_reasons.append("Good Volume")

        # Criterion 7: Price Momentum (Max 0.5 points)
        if current_price >= day_high * 0.98:
            score += 0.5
            bullish_reasons.append("Near Day High")

        # Criterion 8: Market Alignment Bonus (Max 0.5 points)
        if nifty_trend == "BULLISH":
            score += 0.5
            bullish_reasons.append("Nifty Bullish ✅")
        elif nifty_trend == "BEARISH":
            bullish_reasons.append("⚠️ Nifty Bearish")

        # QUALITY FILTER: Minimum score 6.0 for bullish
        if score >= 6.0:
            direction = "BULLISH"
            quality_score = score
            reasons = bullish_reasons

    # ==================== BEARISH QUALITY SCORING ====================
    elif pct_change < -1.5:
        score = 0.0
        bearish_reasons = []

        # Criterion 1: VWAP Position (Max 2.0 points)
        if current_price < vwap:
            if vwap_distance < 1:
                score += 2.0
                bearish_reasons.append("Strong VWAP Resistance")
            else:
                score += 1.5
                bearish_reasons.append("Below VWAP")
            setup.append("Below VWAP")
        else:
            return None  # Must be below VWAP for bearish

        # Criterion 2: EMA Alignment (Max 2.0 points)
        if current_price < ema_20 and ema_20 < ema_50:
            ema_distance = ((ema_50 - ema_20) / ema_50) * 100
            if ema_distance > 1:
                score += 2.0
                bearish_reasons.append("Strong EMA Downtrend")
            else:
                score += 1.5
                bearish_reasons.append("EMA Aligned")
            setup.append("EMA Bearish")

        # Criterion 3: RSI Weakness (Max 2.0 points)
        if 25 <= rsi <= 45:
            if 30 <= rsi <= 40:
                score += 2.0
                bearish_reasons.append(f"Optimal RSI ({rsi:.1f})")
            else:
                score += 1.5
                bearish_reasons.append(f"RSI {rsi:.1f}")
            setup.append("RSI Weakness")

        # Criterion 4: MACD Confirmation (Max 1.0 point)
        if macd < macd_signal:
            macd_diff = abs(macd - macd_signal)
            if macd_diff > 0.5:
                score += 1.0
                bearish_reasons.append("Strong MACD-")
            else:
                score += 0.5
                bearish_reasons.append("MACD-")

        # Criterion 5: Breakdown Confirmation (Max 1.5 points)
        if current_price < or_low:
            score += 1.0
            bearish_reasons.append("OR Breakdown")
            setup.append("Breakdown")
        if current_price < prev_day_low:
            score += 0.5
            bearish_reasons.append("Prev Day Low Break")

        # Criterion 6: Volume Strength (Max 1.0 point)
        if volume_ratio > 2.5:
            score += 1.0
            bearish_reasons.append("Huge Volume")
            setup.append("Volume Surge")
        elif volume_ratio > 2.0:
            score += 0.75
            bearish_reasons.append("Strong Volume")
        elif volume_ratio > 1.5:
            score += 0.5
            bearish_reasons.append("Good Volume")

        # Criterion 7: Price Momentum (Max 0.5 points)
        if current_price <= day_low * 1.02:
            score += 0.5
            bearish_reasons.append("Near Day Low")

        # Criterion 8: Market Alignment Bonus (Max 0.5 points)
        if nifty_trend == "BEARISH":
            score += 0.5
            bearish_reasons.append("Nifty Bearish ✅")
        elif nifty_trend == "BULLISH":
            bearish_reasons.append("⚠️ Nifty Bullish")

        # QUALITY FILTER: Minimum score 6.0 for bearish
        if score >= 6.0:
            direction = "BEARISH"
            quality_score = score
            reasons = bearish_reasons

    # If no direction determined or score too low, reject
    if direction is None or quality_score < 6.0:
        return None

    # Calculate trade levels (Entry/Stop/Target)
    if direction == "BULLISH":
        entry = round(current_price, 2)
        stop_loss = round(min(day_low, current_price - (1.5 * atr)), 2)
        risk = entry - stop_loss
        target = round(entry + (2 * risk), 2)
    else:  # BEARISH
        entry = round(current_price, 2)
        stop_loss = round(max(day_high, current_price + (1.5 * atr)), 2)
        risk = stop_loss - entry
        target = round(entry - (2 * risk), 2)

    rr_ratio = round(abs(target - entry) / abs(risk), 2) if abs(risk) > 0 else 0

    # Get sector info
    sector = info.get('sector', 'Unknown')

    return {
        'Symbol': symbol.replace('.NS', ''),
        'Direction': direction,
        'Entry': entry,
        'StopLoss': stop_loss,
        'Target': target,
        'Risk': round(abs(risk), 2),
        'RR_Ratio': rr_ratio,
        'Price': round(current_price, 2),
        'Change%': round(pct_change, 2),
        'Volume_Ratio': round(volume_ratio, 2),
        'VWAP_Position': vwap_position,
        'VWAP': round(vwap, 2),
        'Setup': ' | '.join(setup[:3]),
        'RSI': round(rsi, 1),
        'Sector': sector,
        'Quality_Score': round(quality_score, 1),
        'Rating': get_rating_label(quality_score),
        'Reasons': ' | '.join(reasons[:5]),
        'EMA20': round(ema_20, 2),
        'EMA50': round(ema_50, 2),
        'ATR%': round(atr_pct, 2)
    }

def scan_market():
    """Scan market for TOP 5 high-quality opportunities in each direction"""
    print("\n" + "="*120)
    print(f"🎯 NSE HIGH-QUALITY SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*120 + "\n")

    # First, check Nifty 50 trend
    print("📊 Analyzing Nifty 50 market trend...")
    nifty_trend = get_nifty_trend()

    if nifty_trend == "BULLISH":
        print(f"✅ Nifty 50 Trend: 🟢 BULLISH")
        print(f"💡 Recommendation: Focus on BULLISH setups for better probability\n")
    elif nifty_trend == "BEARISH":
        print(f"✅ Nifty 50 Trend: 🔴 BEARISH")
        print(f"💡 Recommendation: Focus on BEARISH setups for better probability\n")
    else:
        print(f"⚠️  Nifty 50 Trend: ⚪ NEUTRAL")
        print(f"💡 Recommendation: Trade both sides with caution, no clear market bias\n")

    print("Scanning for TOP 5 BULLISH + TOP 5 BEARISH high-quality setups...")
    print(f"Universe: {len(NSE_FNO_STOCKS)} F&O stocks")
    print("Quality Rating: 1-10 scale (Minimum: 6.0)\n")

    opportunities = []
    processed = 0

    for symbol in NSE_FNO_STOCKS:
        processed += 1
        print(f"Scanning: {symbol} ({processed}/{len(NSE_FNO_STOCKS)})", end='\r')

        result = analyze_stock(symbol, nifty_trend)
        if result:
            opportunities.append(result)

    print("\n")

    if not opportunities:
        print("⚠️  No high-quality stocks found meeting strict criteria (Score ≥ 6.0)")
        print("Market may be consolidating. Try again later.\n")
        return

    # Separate bullish and bearish opportunities
    bullish_opps = [opp for opp in opportunities if opp['Direction'] == 'BULLISH']
    bearish_opps = [opp for opp in opportunities if opp['Direction'] == 'BEARISH']

    # Sort by Quality Score (highest first)
    bullish_opps.sort(key=lambda x: x['Quality_Score'], reverse=True)
    bearish_opps.sort(key=lambda x: x['Quality_Score'], reverse=True)

    # ⭐ LIMIT TO TOP 5 EACH ⭐
    bullish_opps = bullish_opps[:5]
    bearish_opps = bearish_opps[:5]

    print(f"✅ Found TOP {len(bullish_opps)} Bullish + TOP {len(bearish_opps)} Bearish High-Quality Stocks\n")

    # ==================== TOP 5 BULLISH SECTION ====================
    if bullish_opps:
        print("="*120)
        print(f"🟢 TOP 5 HIGH-QUALITY BULLISH STOCKS (GAINERS)")
        print("="*120)

        for i, opp in enumerate(bullish_opps, 1):
            print(f"\n{i}. 🎯 {opp['Symbol']} - {opp['Rating']}")
            print(f"   ───────────────────────────────────────────────────────────")
            print(f"   📈 ENTRY: ₹{opp['Entry']} | STOP: ₹{opp['StopLoss']} | TARGET: ₹{opp['Target']}")
            print(f"   💰 Risk: ₹{opp['Risk']} | Risk-Reward: 1:{opp['RR_Ratio']}")
            print(f"   ───────────────────────────────────────────────────────────")
            print(f"   📊 Price: ₹{opp['Price']} | Change: {opp['Change%']:+.2f}% | Volume: {opp['Volume_Ratio']:.1f}x")
            print(f"   📉 VWAP: ₹{opp['VWAP']} ({opp['VWAP_Position']}) | RSI: {opp['RSI']} | ATR: {opp['ATR%']:.2f}%")
            print(f"   🏆 Quality Score: {opp['Quality_Score']}/10.0")
            print(f"   🎯 Setup: {opp['Setup']}")
            print(f"   🏢 Sector: {opp['Sector']}")
            print(f"   ✅ Strengths: {opp['Reasons']}")

        print("\n" + "="*120)
    else:
        print("\n🟢 No high-quality bullish opportunities found at this time.\n")

    print("\n")

    # ==================== TOP 5 BEARISH SECTION ====================
    if bearish_opps:
        print("="*120)
        print(f"🔴 TOP 5 HIGH-QUALITY BEARISH STOCKS (SHORTING CANDIDATES)")
        print("="*120)

        for i, opp in enumerate(bearish_opps, 1):
            print(f"\n{i}. 🎯 {opp['Symbol']} - {opp['Rating']}")
            print(f"   ───────────────────────────────────────────────────────────")
            print(f"   📉 ENTRY: ₹{opp['Entry']} | STOP: ₹{opp['StopLoss']} | TARGET: ₹{opp['Target']}")
            print(f"   💰 Risk: ₹{opp['Risk']} | Risk-Reward: 1:{opp['RR_Ratio']}")
            print(f"   ───────────────────────────────────────────────────────────")
            print(f"   📊 Price: ₹{opp['Price']} | Change: {opp['Change%']:+.2f}% | Volume: {opp['Volume_Ratio']:.1f}x")
            print(f"   📈 VWAP: ₹{opp['VWAP']} ({opp['VWAP_Position']}) | RSI: {opp['RSI']} | ATR: {opp['ATR%']:.2f}%")
            print(f"   🏆 Quality Score: {opp['Quality_Score']}/10.0")
            print(f"   🎯 Setup: {opp['Setup']}")
            print(f"   🏢 Sector: {opp['Sector']}")
            print(f"   ✅ Strengths: {opp['Reasons']}")

        print("\n" + "="*120)
    else:
        print("\n🔴 No high-quality bearish opportunities found at this time.\n")

    print("\n")
    print("="*120)
    print("📊 MARKET TREND ANALYSIS")
    print("="*120)
    if nifty_trend == "BULLISH":
        print("🟢 Nifty 50: BULLISH - Market favors LONG trades (Higher success probability)")
        print("   → Stocks aligned with Nifty get +0.5 bonus points in quality score")
    elif nifty_trend == "BEARISH":
        print("🔴 Nifty 50: BEARISH - Market favors SHORT trades (Higher success probability)")
        print("   → Stocks aligned with Nifty get +0.5 bonus points in quality score")
    else:
        print("⚪ Nifty 50: NEUTRAL - No clear market bias, trade with extra caution")
        print("   → Consider waiting for clearer market direction")
    print("="*120)
    print()
    print("="*120)
    print("📋 QUALITY RATING SYSTEM")
    print("="*120)
    print("⭐⭐⭐ EXCELLENT  (8.5-10.5) - Highest probability setups")
    print("⭐⭐ VERY GOOD    (7.0-8.4)  - Strong setups")
    print("⭐ GOOD          (6.0-6.9)  - Good setups")
    print("="*120)
    print("\n⚠️  TRADING RULES:")
    print("1. ALWAYS use stop loss mentioned")
    print("2. Risk only 1-2% of capital per trade")
    print("3. Focus on EXCELLENT and VERY GOOD rated stocks")
    print("4. Prioritize setups aligned with Nifty trend (marked with ✅)")
    print("5. Wait for entry price - Don't chase")
    print("6. This is NOT financial advice - Trade at your own risk\n")

    # Save to CSV in organized folder structure
    all_results = bullish_opps + bearish_opps
    if all_results:
        df_results = pd.DataFrame(all_results)

        # Create date-based folder structure
        date_folder = datetime.now().strftime('%Y-%m-%d')
        output_path = os.path.join('basic_scanner_output', date_folder)
        os.makedirs(output_path, exist_ok=True)

        # Save with time in filename
        filename = f"scan_{datetime.now().strftime('%H%M')}.csv"
        filepath = os.path.join(output_path, filename)
        df_results.to_csv(filepath, index=False)
        print(f"📊 Results saved to: {filepath}\n")

if __name__ == "__main__":
    scan_market()
