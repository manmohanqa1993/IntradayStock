"""
API Diagnostic Tool - Test all data sources
This will tell you exactly what's working and what's not
"""

import sys
print("Python version:", sys.version)
print("\n" + "="*70)
print("TESTING ALL DATA SOURCES - DIAGNOSTIC TOOL")
print("="*70 + "\n")

# Test 1: Yahoo Finance
print("1️⃣ Testing Yahoo Finance...")
print("-" * 70)
try:
    import yfinance as yf
    print("✅ yfinance library installed")

    # Try to fetch data
    ticker = yf.Ticker("RELIANCE.NS")
    data = ticker.history(period="1d", interval="5m")

    if not data.empty:
        print(f"✅ Yahoo Finance WORKING!")
        print(f"   Last price: ₹{data['Close'].iloc[-1]:.2f}")
        print(f"   Data points: {len(data)}")
    else:
        print("❌ Yahoo Finance returned empty data")

except ImportError:
    print("❌ yfinance not installed")
    print("   Fix: pip install yfinance")
except Exception as e:
    print(f"❌ Yahoo Finance ERROR: {e}")

print()

# Test 2: Direct NSE Website
print("2️⃣ Testing NSE India Website...")
print("-" * 70)
try:
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # Test NSE website connectivity
    url = "https://www.nseindia.com/api/quote-equity?symbol=RELIANCE"
    session = requests.Session()

    # First request to get cookies
    session.get("https://www.nseindia.com", headers=headers, timeout=10)

    # Second request for data
    response = session.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        if 'priceInfo' in data:
            price = data['priceInfo']['lastPrice']
            print(f"✅ NSE India Website WORKING!")
            print(f"   RELIANCE price: ₹{price}")
        else:
            print("⚠️ NSE response format changed")
    else:
        print(f"❌ NSE Website returned status: {response.status_code}")

except ImportError:
    print("❌ requests library not installed")
    print("   Fix: pip install requests")
except Exception as e:
    print(f"❌ NSE Website ERROR: {e}")

print()

# Test 3: Upstox
print("3️⃣ Testing Upstox API...")
print("-" * 70)
try:
    import upstox_client
    print("✅ upstox_client library installed")
    print("⚠️  Need credentials to test connection")
    print("   Run: python upstox_login.py")
except ImportError:
    print("❌ upstox-client not installed")
    print("   Fix: pip install upstox-client")
except Exception as e:
    print(f"❌ Upstox ERROR: {e}")

print()

# Test 4: Internet Connectivity
print("4️⃣ Testing Internet Connectivity...")
print("-" * 70)
try:
    import requests

    # Test Google
    response = requests.get("https://www.google.com", timeout=5)
    if response.status_code == 200:
        print("✅ Google.com reachable")

    # Test NSE
    response = requests.get("https://www.nseindia.com", timeout=5)
    if response.status_code == 200:
        print("✅ NSEIndia.com reachable")

    # Test Yahoo Finance
    response = requests.get("https://finance.yahoo.com", timeout=5)
    if response.status_code == 200:
        print("✅ Yahoo Finance reachable")

except Exception as e:
    print(f"❌ Internet connectivity issue: {e}")

print()

# Test 5: Proxy/Firewall Detection
print("5️⃣ Checking for Proxy/Firewall...")
print("-" * 70)
try:
    import os

    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')

    if http_proxy or https_proxy:
        print(f"⚠️  Proxy detected!")
        if http_proxy:
            print(f"   HTTP_PROXY: {http_proxy}")
        if https_proxy:
            print(f"   HTTPS_PROXY: {https_proxy}")
        print("   This might block API access")
    else:
        print("✅ No proxy detected")

except Exception as e:
    print(f"❌ Error checking proxy: {e}")

print()

# Summary and Recommendations
print("="*70)
print("SUMMARY & RECOMMENDATIONS")
print("="*70 + "\n")

print("Based on the tests above:\n")
print("✅ = Working - You can use this")
print("⚠️  = Needs setup - Follow instructions")
print("❌ = Not working - See fix suggestions\n")

print("RECOMMENDED SOLUTIONS:")
print("-" * 70)
print("\n1. IF YAHOO FINANCE IS WORKING (✅):")
print("   → Use: python intraday_scanner.py")
print("   → Or use Google Colab with Yahoo version")
print("   → 15-min delay but RELIABLE\n")

print("2. IF NSE WEBSITE IS WORKING (✅):")
print("   → Use the NSE scraper (I'll create it for you)")
print("   → Real-time data, no API needed")
print("   → Rate limited but FREE\n")

print("3. IF NOTHING WORKS LOCALLY (❌):")
print("   → Use Google Colab (recommended!)")
print("   → Upload: NSE_Intraday_Scanner_Colab.ipynb")
print("   → Bypasses all local restrictions")
print("   → Link: https://colab.research.google.com/\n")

print("4. IF YOU HAVE NETWORK RESTRICTIONS:")
print("   → Company firewall blocking APIs")
print("   → Use Google Colab from personal laptop/home")
print("   → Or use mobile hotspot\n")

print("="*70)
print("\nNEXT STEP: Tell me which tests passed (✅) and I'll create")
print("          the best solution for YOUR specific situation!")
print("="*70)
