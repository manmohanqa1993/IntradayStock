"""
NSE Intraday Scanner - Direct NSE Website Scraping
NO API NEEDED - Works when all APIs fail!
Scrapes data directly from NSE India website
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

# NSE F&O Stock List (without .NS suffix)
NSE_STOCKS = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
    'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'KOTAKBANK',
    'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'HCLTECH',
    'SUNPHARMA', 'BAJFINANCE', 'WIPRO', 'ULTRACEMCO', 'TITAN',
    'NESTLEIND', 'TATAMOTORS', 'ONGC', 'NTPC', 'POWERGRID',
    'M&M', 'TECHM', 'BAJAJFINSV', 'ADANIPORTS', 'TATASTEEL',
    'COALINDIA', 'HINDALCO', 'INDUSINDBK', 'DIVISLAB', 'DRREDDY',
    'CIPLA', 'GRASIM', 'JSWSTEEL', 'HEROMOTOCO', 'EICHERMOT',
    'BRITANNIA', 'BPCL', 'SHREECEM', 'TATACONSUM', 'APOLLOHOSP'
]

# Create session with proper headers
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nseindia.com/',
    'Origin': 'https://www.nseindia.com',
}

def initialize_session():
    """Initialize session by getting cookies from NSE"""
    try:
        response = session.get(
            'https://www.nseindia.com',
            headers=headers,
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error initializing session: {e}")
        return False

def get_stock_quote(symbol):
    """Get real-time quote from NSE India website"""
    try:
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"

        response = session.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            if 'priceInfo' in data and 'metadata' in data:
                price_info = data['priceInfo']
                metadata = data['metadata']

                return {
                    'symbol': symbol,
                    'ltp': float(price_info.get('lastPrice', 0)),
                    'open': float(price_info.get('open', 0)),
                    'high': float(price_info.get('intraDayHighLow', {}).get('max', 0)),
                    'low': float(price_info.get('intraDayHighLow', {}).get('min', 0)),
                    'close': float(price_info.get('close', 0)),
                    'prev_close': float(price_info.get('previousClose', 0)),
                    'change': float(price_info.get('change', 0)),
                    'pct_change': float(price_info.get('pChange', 0)),
                    'volume': int(data.get('preOpenMarket', {}).get('totalTradedVolume', 0)),
                    'avg_price': float(price_info.get('vwap', 0)),
                    'sector': metadata.get('industry', 'Unknown')
                }

        return None

    except Exception as e:
        # Silently fail to avoid spam
        return None

def calculate_simple_rsi(prices, period=14):
    """Calculate simple RSI"""
    if len(prices) < period:
        return 50  # Neutral

    deltas = np.diff(prices)
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]

    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def analyze_stock_simple(symbol):
    """Analyze stock with simple criteria (no historical data)"""

    quote = get_stock_quote(symbol)
    if not quote:
        return None

    ltp = quote['ltp']
    prev_close = quote['prev_close']
    pct_change = quote['pct_change']
    vwap = quote['avg_price']
    high = quote['high']
    low = quote['low']

    if ltp == 0 or prev_close == 0:
        return None

    # Simple analysis based on current data only
    gap = abs(pct_change)

    # Determine direction
    direction = None
    setup = []
    score = 0

    # BULLISH criteria
    if pct_change > 1.5:  # Gap up
        score += 1
        setup.append("Gap Up")

    if ltp > vwap:  # Above VWAP
        score += 1
        setup.append("Above VWAP")

    if ltp >= high * 0.99:  # Near day high
        score += 1
        setup.append("Near High")

    if pct_change > 0:  # Positive momentum
        score += 1

    # BEARISH criteria
    bearish_score = 0
    if pct_change < -1.5:  # Gap down
        bearish_score += 1
        setup.append("Gap Down")

    if ltp < vwap:  # Below VWAP
        bearish_score += 1
        setup.append("Below VWAP")

    if ltp <= low * 1.01:  # Near day low
        bearish_score += 1
        setup.append("Near Low")

    if pct_change < 0:  # Negative momentum
        bearish_score += 1

    # Determine final direction
    if score >= 3:
        direction = "BULLISH"
    elif bearish_score >= 3:
        direction = "BEARISH"
        score = bearish_score
    else:
        return None  # Not strong enough

    return {
        'Symbol': symbol,
        'Direction': direction,
        'LTP': round(ltp, 2),
        'Change%': round(pct_change, 2),
        'VWAP': round(vwap, 2),
        'High': round(high, 2),
        'Low': round(low, 2),
        'Setup': ' | '.join(setup[:3]),
        'Score': score,
        'Sector': quote['sector']
    }

def scan_market_nse():
    """Scan market using NSE website directly"""
    print("\n" + "="*100)
    print(f"🌐 NSE DIRECT SCANNER (NO API NEEDED) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    print("🔧 Scraping data directly from NSE India website...")
    print("⚠️  This is slower due to rate limiting (1 request/2 seconds)")
    print(f"🎯 Scanning {len(NSE_STOCKS)} stocks (will take ~3-4 minutes)...\n")

    # Initialize session
    if not initialize_session():
        print("❌ Failed to initialize NSE session")
        print("Possible reasons:")
        print("1. NSE website is down")
        print("2. Internet connection issues")
        print("3. Firewall blocking access")
        print("\nTry using Google Colab instead!")
        return

    print("✅ NSE session initialized\n")

    opportunities = []
    processed = 0

    for symbol in NSE_STOCKS:
        processed += 1
        print(f"Scanning: {symbol} ({processed}/{len(NSE_STOCKS)})", end='\r')

        result = analyze_stock_simple(symbol)
        if result:
            opportunities.append(result)

        # IMPORTANT: Respect NSE rate limits (1 request per 2 seconds)
        time.sleep(2)

    print("\n")

    if not opportunities:
        print("⚠️  No stocks meeting criteria found.")
        print("Note: This simple scanner has limited filters without historical data.\n")
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
        print(f"🟢 BULLISH OPPORTUNITIES ({len(bullish_opps)} stocks) - NSE DIRECT")
        print("="*100)

        for i, opp in enumerate(bullish_opps, 1):
            print(f"\n{i}. {opp['Symbol']} - 🚀 {opp['Direction']}")
            print(f"   LTP: ₹{opp['LTP']} | Change: {opp['Change%']:+.2f}%")
            print(f"   VWAP: ₹{opp['VWAP']} | High: ₹{opp['High']} | Low: ₹{opp['Low']}")
            print(f"   Setup: {opp['Setup']}")
            print(f"   Sector: {opp['Sector']} | Score: {opp['Score']}/4")

        print("\n" + "="*100)
    else:
        print("\n🟢 No bullish opportunities found at this time.\n")

    print("\n")

    # ==================== BEARISH SECTION ====================
    if bearish_opps:
        print("="*100)
        print(f"🔴 BEARISH OPPORTUNITIES ({len(bearish_opps)} stocks) - NSE DIRECT")
        print("="*100)

        for i, opp in enumerate(bearish_opps, 1):
            print(f"\n{i}. {opp['Symbol']} - 📉 {opp['Direction']}")
            print(f"   LTP: ₹{opp['LTP']} | Change: {opp['Change%']:+.2f}%")
            print(f"   VWAP: ₹{opp['VWAP']} | High: ₹{opp['High']} | Low: ₹{opp['Low']}")
            print(f"   Setup: {opp['Setup']}")
            print(f"   Sector: {opp['Sector']} | Score: {opp['Score']}/4")

        print("\n" + "="*100)
    else:
        print("\n🔴 No bearish opportunities found at this time.\n")

    print("\n" + "="*100)
    print("\n💡 This is a simplified scanner (no historical data)")
    print("⏱️  Slower due to NSE rate limits (2 sec per stock)")
    print("⚠️  For better results, use Google Colab with Yahoo Finance")
    print("\n🔗 Google Colab: https://colab.research.google.com/")
    print("📁 Upload: NSE_Intraday_Scanner_Colab.ipynb\n")

    # Save results
    df_results = pd.DataFrame(opportunities)
    filename = f"nse_direct_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_results.to_csv(filename, index=False)
    print(f"📊 Results saved to: {filename}\n")

if __name__ == "__main__":
    print("\n🌐 NSE DIRECT SCRAPER - When All APIs Fail!")
    print("="*100)
    print("\nThis scanner:")
    print("✅ Works WITHOUT any API")
    print("✅ Scrapes NSE India website directly")
    print("✅ Real-time data (but slower)")
    print("⚠️  Takes 3-4 minutes (rate limited to 1 request/2 sec)")
    print("⚠️  Simplified analysis (no historical data)")
    print("\n" + "="*100 + "\n")

    scan_market_nse()
