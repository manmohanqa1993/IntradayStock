"""
Professional NSE Intraday Scanner with Quality Rating System
Identifies TOP 3 Bullish + TOP 3 Bearish high-probability opportunities
Features: Entry/Stop/Target levels, Quality Rating (1-12 scale), Nifty Trend Analysis
Based on professional trader criteria
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
    NSE_LIQUID_STOCKS = NSE_FNO_STOCKS
except ImportError:
    # Fallback to basic list if import fails
    NSE_LIQUID_STOCKS = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
        'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS',
        'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'HCLTECH.NS',
        'SUNPHARMA.NS', 'BAJFINANCE.NS', 'WIPRO.NS', 'ULTRACEMCO.NS', 'TITAN.NS',
        'NESTLEIND.NS', 'TATAMOTORS.NS', 'ONGC.NS', 'NTPC.NS', 'POWERGRID.NS',
        'M&M.NS', 'TECHM.NS', 'BAJAJFINSV.NS', 'ADANIPORTS.NS', 'TATASTEEL.NS',
        'COALINDIA.NS', 'HINDALCO.NS', 'INDUSINDBK.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
        'CIPLA.NS', 'GRASIM.NS', 'JSWSTEEL.NS', 'HEROMOTOCO.NS', 'EICHERMOT.NS',
        'BRITANNIA.NS', 'BPCL.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'APOLLOHOSP.NS',
        'ADANIENT.NS', 'BAJAJ-AUTO.NS', 'HDFCLIFE.NS', 'SBILIFE.NS', 'BANKBARODA.NS'
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

def get_rating_label(score):
    """Convert score to rating label (Score out of 12)"""
    if score >= 10:
        return "⭐⭐⭐ EXCELLENT"
    elif score >= 8.5:
        return "⭐⭐ VERY GOOD"
    elif score >= 7.5:
        return "⭐ GOOD"
    else:
        return "FAIR"

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

def calculate_support_resistance(df):
    """Calculate key support and resistance levels"""
    # Recent swing highs and lows
    recent_high = df['High'].tail(20).max()
    recent_low = df['Low'].tail(20).min()

    # Previous day levels
    prev_day_high = df['High'].tail(78).max()
    prev_day_low = df['Low'].tail(78).min()

    return {
        'recent_high': recent_high,
        'recent_low': recent_low,
        'prev_day_high': prev_day_high,
        'prev_day_low': prev_day_low
    }

def calculate_trade_levels(direction, current_price, atr, support_resistance):
    """Calculate entry, stop loss, and target prices"""

    if direction == "BUY":
        # Entry at current price or slight pullback
        entry = round(current_price, 2)

        # Stop loss: Below recent low or 1.5x ATR
        stop_loss = round(min(support_resistance['recent_low'], current_price - (1.5 * atr)), 2)

        # Target: 1:2 risk-reward ratio
        risk = entry - stop_loss
        target = round(entry + (2 * risk), 2)

    else:  # SELL
        # Entry at current price
        entry = round(current_price, 2)

        # Stop loss: Above recent high or 1.5x ATR
        stop_loss = round(max(support_resistance['recent_high'], current_price + (1.5 * atr)), 2)

        # Target: 1:2 risk-reward ratio
        risk = stop_loss - entry
        target = round(entry - (2 * risk), 2)

    # Calculate risk-reward
    risk_amount = abs(entry - stop_loss)
    reward_amount = abs(target - entry)
    rr_ratio = round(reward_amount / risk_amount, 2) if risk_amount > 0 else 0

    return {
        'entry': entry,
        'stop_loss': stop_loss,
        'target': target,
        'risk': round(risk_amount, 2),
        'reward': round(reward_amount, 2),
        'rr_ratio': rr_ratio
    }

def analyze_stock_professional(symbol, nifty_trend):
    """Professional analysis with all criteria"""

    data = get_stock_data(symbol)
    if data is None:
        return None

    df, prev_close, info = data

    # Current metrics
    current_price = df['Close'].iloc[-1]
    current_volume = df['Volume'].sum()

    # FILTER 1: Price must be > ₹100
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

    # FILTER 2A: Remove stocks with >2% gap (too much gap up/down)
    if abs(pct_change) > 2.0:
        return None

    # FILTER 2B: Momentum - Must be moving ±1.5%
    if abs(pct_change) < 1.5:
        return None

    # Average volume
    avg_volume = df['Volume'].tail(100).mean() * 78
    volume_ratio = (current_volume / avg_volume) if avg_volume > 0 else 0

    # FILTER 3: Volume must be 2x average (changed from 1.5x)
    if volume_ratio < 2.0:
        return None

    # FILTER 4: Average volume > 500,000 shares per day
    if avg_volume < 500000:
        return None

    # Opening Range (first 3 candles = 15 min)
    or_high = df['High'].head(3).max()
    or_low = df['Low'].head(3).min()

    # Previous day high/low
    prev_day_high = df['High'].tail(78).max()
    prev_day_low = df['Low'].tail(78).min()

    # ATR percentage
    atr_pct = (atr / current_price) * 100 if current_price > 0 else 0

    # Intraday range
    intraday_range_pct = ((day_high - day_low) / current_price) * 100

    # FILTER 5: Volatility - ATR > 1% OR intraday range > 1.5%
    if atr_pct < 1 and intraday_range_pct < 1.5:
        return None

    # Near day high/low check
    near_day_high = (current_price >= day_high * 0.98)  # Within 2% of day high
    near_day_low = (current_price <= day_low * 1.02)    # Within 2% of day low

    # Support/Resistance levels
    sr_levels = calculate_support_resistance(df)

    # Determine direction and check ALL criteria
    direction = None
    reasons = []
    score = 0

    # ==================== BULLISH ANALYSIS ====================
    if pct_change > 1.5:  # Moving up
        bullish_score = 0
        bullish_reasons = []

        # Criterion 1: VWAP (MUST)
        if current_price > vwap:
            bullish_score += 2
            bullish_reasons.append("✅ Price above VWAP")
        else:
            return None  # VWAP is mandatory

        # Criterion 2: Moving Average Trend (MUST)
        if ema_20 > ema_50:
            bullish_score += 2
            bullish_reasons.append("✅ 20 EMA > 50 EMA (Bullish trend)")
        else:
            return None  # EMA trend is mandatory

        # Criterion 3: RSI (MUST be 50-70)
        if 50 <= rsi <= 70:
            bullish_score += 2
            bullish_reasons.append(f"✅ RSI: {rsi:.1f} (Strong momentum)")
        else:
            return None  # RSI range is mandatory

        # Criterion 4: MACD Confirmation
        if macd > macd_signal:
            bullish_score += 1
            bullish_reasons.append("✅ MACD Bullish crossover")

        # Criterion 5: Breakout (at least one required)
        breakout = False
        if current_price > or_high:
            bullish_score += 1
            bullish_reasons.append("✅ Opening Range Breakout")
            breakout = True
        if current_price > prev_day_high:
            bullish_score += 1
            bullish_reasons.append("✅ Previous Day High Breakout")
            breakout = True
        if current_price >= day_high * 0.995:
            bullish_score += 1
            bullish_reasons.append("✅ At Day High")
            breakout = True

        if not breakout:
            return None  # At least one breakout is mandatory

        # Criterion 6: Near day high preference
        if near_day_high:
            bullish_score += 1
            bullish_reasons.append("✅ Near Day High (Strong momentum)")

        # Criterion 7: Market alignment
        if nifty_trend == "BULLISH":
            bullish_score += 1
            bullish_reasons.append("✅ Nifty is Bullish")
        elif nifty_trend == "BEARISH":
            bullish_score -= 1
            bullish_reasons.append("⚠️ Nifty is Bearish (against trade)")

        # Must have minimum score
        if bullish_score >= 8:
            direction = "BUY"
            reasons = bullish_reasons
            score = bullish_score

    # ==================== BEARISH ANALYSIS ====================
    elif pct_change < -1.5:  # Moving down
        bearish_score = 0
        bearish_reasons = []

        # Criterion 1: VWAP (MUST)
        if current_price < vwap:
            bearish_score += 2
            bearish_reasons.append("✅ Price below VWAP")
        else:
            return None  # VWAP is mandatory

        # Criterion 2: Moving Average Trend (MUST)
        if ema_20 < ema_50:
            bearish_score += 2
            bearish_reasons.append("✅ 20 EMA < 50 EMA (Bearish trend)")
        else:
            return None  # EMA trend is mandatory

        # Criterion 3: RSI (MUST be 30-50)
        if 30 <= rsi <= 50:
            bearish_score += 2
            bearish_reasons.append(f"✅ RSI: {rsi:.1f} (Strong selling)")
        else:
            return None  # RSI range is mandatory

        # Criterion 4: MACD Confirmation
        if macd < macd_signal:
            bearish_score += 1
            bearish_reasons.append("✅ MACD Bearish crossover")

        # Criterion 5: Breakdown (at least one required)
        breakdown = False
        if current_price < or_low:
            bearish_score += 1
            bearish_reasons.append("✅ Opening Range Breakdown")
            breakdown = True
        if current_price < prev_day_low:
            bearish_score += 1
            bearish_reasons.append("✅ Previous Day Low Breakdown")
            breakdown = True
        if current_price <= day_low * 1.005:
            bearish_score += 1
            bearish_reasons.append("✅ At Day Low")
            breakdown = True

        if not breakdown:
            return None  # At least one breakdown is mandatory

        # Criterion 6: Near day low preference
        if near_day_low:
            bearish_score += 1
            bearish_reasons.append("✅ Near Day Low (Strong momentum)")

        # Criterion 7: Market alignment
        if nifty_trend == "BEARISH":
            bearish_score += 1
            bearish_reasons.append("✅ Nifty is Bearish")
        elif nifty_trend == "BULLISH":
            bearish_score -= 1
            bearish_reasons.append("⚠️ Nifty is Bullish (against trade)")

        # Must have minimum score
        if bearish_score >= 8:
            direction = "SELL"
            reasons = bearish_reasons
            score = bearish_score

    # If no direction determined, not qualified
    if direction is None:
        return None

    # Calculate trade levels
    trade_levels = calculate_trade_levels(direction, current_price, atr, sr_levels)

    # Get sector
    sector = info.get('sector', 'Unknown')

    return {
        'Symbol': symbol.replace('.NS', ''),
        'Action': direction,
        'Entry': trade_levels['entry'],
        'StopLoss': trade_levels['stop_loss'],
        'Target': trade_levels['target'],
        'Risk': trade_levels['risk'],
        'Reward': trade_levels['reward'],
        'RR_Ratio': trade_levels['rr_ratio'],
        'Current_Price': round(current_price, 2),
        'Change%': round(pct_change, 2),
        'Volume_Ratio': round(volume_ratio, 2),
        'VWAP': round(vwap, 2),
        'RSI': round(rsi, 1),
        'Score': score,
        'Rating': get_rating_label(score),
        'Sector': sector,
        'Reasons': reasons,
        'Day_High': round(day_high, 2),
        'Day_Low': round(day_low, 2)
    }

def scan_market_professional():
    """Professional intraday scanner with strict criteria"""
    print("\n" + "="*120)
    print(f"🎯 PROFESSIONAL NSE INTRADAY SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*120 + "\n")

    # First, check Nifty trend
    print("📊 Analyzing Nifty 50 trend...")
    nifty_trend = get_nifty_trend()

    if nifty_trend == "BULLISH":
        print(f"✅ Nifty Trend: 🟢 BULLISH (Prefer LONG trades)")
        print(f"💡 Recommendation: Focus on BULLISH setups for better probability\n")
    elif nifty_trend == "BEARISH":
        print(f"✅ Nifty Trend: 🔴 BEARISH (Prefer SHORT trades)")
        print(f"💡 Recommendation: Focus on BEARISH setups for better probability\n")
    else:
        print(f"⚠️  Nifty Trend: ⚪ NEUTRAL (Trade with caution)")
        print(f"💡 Recommendation: Trade both sides carefully, no clear market bias\n")

    print(f"Scanning {len(NSE_LIQUID_STOCKS)} F&O stocks...")
    print("Applying professional trader criteria...")
    print("Target: TOP 3 Bullish + TOP 3 Bearish high-quality setups\n")

    opportunities = []
    processed = 0

    for symbol in NSE_LIQUID_STOCKS:
        processed += 1
        print(f"Scanning: {symbol} ({processed}/{len(NSE_LIQUID_STOCKS)})", end='\r')

        result = analyze_stock_professional(symbol, nifty_trend)
        if result:
            opportunities.append(result)

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

    # Limit to TOP 3 each direction
    final_buy = buy_setups[:3]
    final_sell = sell_setups[:3]
    total_setups = final_buy + final_sell

    print(f"✅ Found TOP {len(final_buy)} Bullish + TOP {len(final_sell)} Bearish High-Quality Setups\n")

    # ==================== BUY SETUPS ====================
    if final_buy:
        print("="*120)
        print(f"🟢 TOP 3 BULLISH OPPORTUNITIES")
        print("="*120)

        for i, trade in enumerate(final_buy, 1):
            print(f"\n{i}. 🎯 {trade['Symbol']} - {trade['Rating']}")
            print(f"   {'─'*115}")
            print(f"   📈 ENTRY:     ₹{trade['Entry']}")
            print(f"   🛑 STOP LOSS: ₹{trade['StopLoss']} (Risk: ₹{trade['Risk']})")
            print(f"   🎯 TARGET:    ₹{trade['Target']} (Reward: ₹{trade['Reward']})")
            print(f"   💰 RISK-REWARD RATIO: 1:{trade['RR_Ratio']}")
            print(f"   {'─'*115}")
            print(f"   📊 Current: ₹{trade['Current_Price']} | Change: {trade['Change%']:+.2f}% | Vol: {trade['Volume_Ratio']:.1f}x")
            print(f"   📉 VWAP: ₹{trade['VWAP']} | RSI: {trade['RSI']} | Day Range: ₹{trade['Day_Low']}-₹{trade['Day_High']}")
            print(f"   🏆 Quality Score: {trade['Score']}/12 | 🏢 Sector: {trade['Sector']}")
            print(f"\n   ✅ REASONS FOR TRADE:")
            for reason in trade['Reasons']:
                print(f"      {reason}")

        print("\n" + "="*120)
    else:
        print("\n🟢 No high-quality bullish setups found at this time.\n")

    if final_buy and final_sell:
        print("\n")

    # ==================== SELL SETUPS ====================
    if final_sell:
        print("="*120)
        print(f"🔴 TOP 3 BEARISH OPPORTUNITIES")
        print("="*120)

        for i, trade in enumerate(final_sell, 1):
            print(f"\n{i}. 🎯 {trade['Symbol']} - {trade['Rating']}")
            print(f"   {'─'*115}")
            print(f"   📉 ENTRY:     ₹{trade['Entry']}")
            print(f"   🛑 STOP LOSS: ₹{trade['StopLoss']} (Risk: ₹{trade['Risk']})")
            print(f"   🎯 TARGET:    ₹{trade['Target']} (Reward: ₹{trade['Reward']})")
            print(f"   💰 RISK-REWARD RATIO: 1:{trade['RR_Ratio']}")
            print(f"   {'─'*115}")
            print(f"   📊 Current: ₹{trade['Current_Price']} | Change: {trade['Change%']:+.2f}% | Vol: {trade['Volume_Ratio']:.1f}x")
            print(f"   📈 VWAP: ₹{trade['VWAP']} | RSI: {trade['RSI']} | Day Range: ₹{trade['Day_Low']}-₹{trade['Day_High']}")
            print(f"   🏆 Quality Score: {trade['Score']}/12 | 🏢 Sector: {trade['Sector']}")
            print(f"\n   ✅ REASONS FOR TRADE:")
            for reason in trade['Reasons']:
                print(f"      {reason}")

        print("\n" + "="*120)
    else:
        print("\n🔴 No high-quality bearish setups found at this time.\n")

    print("\n")
    print("="*120)
    print("📊 QUALITY RATING SYSTEM")
    print("="*120)
    print("⭐⭐⭐ EXCELLENT  (10-12 points) - Highest probability setups, all criteria met")
    print("⭐⭐ VERY GOOD    (8.5-9.9 points) - Strong setups, most criteria met")
    print("⭐ GOOD          (7.5-8.4 points) - Good setups, minimum criteria met")
    print("="*120)
    print()
    print("="*120)
    print("⚠️  PROFESSIONAL TRADING RULES")
    print("="*120)
    print("1. ALWAYS use the stop loss mentioned - No exceptions!")
    print("2. Risk only 1-2% of capital per trade")
    print("3. Prioritize EXCELLENT and VERY GOOD rated stocks")
    print("4. Focus on setups aligned with Nifty trend (marked with ✅)")
    print("5. Wait for entry price or better - Don't chase")
    print("6. Book partial profits at 1:1 and move SL to entry")
    print("7. Exit if setup invalidates (breaks SL or key levels)")
    print("8. These are high-probability setups, NOT guaranteed profits")
    print("9. This is NOT financial advice - Trade at your own risk")
    print("="*120 + "\n")

    # Save to CSV in organized folder structure
    if total_setups:
        df_results = pd.DataFrame(total_setups)
        # Flatten reasons list to string
        df_results['Reasons'] = df_results['Reasons'].apply(lambda x: ' | '.join(x))

        # Create date-based folder structure
        date_folder = datetime.now().strftime('%Y-%m-%d')
        output_path = os.path.join('pro_scanner_output', date_folder)
        os.makedirs(output_path, exist_ok=True)

        # Save with time in filename
        filename = f"scan_{datetime.now().strftime('%H%M')}.csv"
        filepath = os.path.join(output_path, filename)
        df_results.to_csv(filepath, index=False)
        print(f"📊 Results saved to: {filepath}\n")

if __name__ == "__main__":
    scan_market_professional()
