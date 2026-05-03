# Real-Time Data Setup Guide

## 📊 Overview

Upgrade your scanner from 15-minute delayed data to **ZERO-DELAY real-time tick data** for scalping and precise entries.

---

## 🎯 Provider Comparison

| Provider | Cost | Data Quality | Best For |
|----------|------|--------------|----------|
| **Zerodha Kite** | ₹2,000/month | Excellent | Active traders, most reliable |
| **Upstox** | Free for clients | Good | Budget option |
| **Fyers** | ₹2,000/month | Excellent | Advanced features |

---

## 🚀 Option 1: Zerodha Kite Connect (Recommended)

### Prerequisites
1. **Zerodha Trading Account** (open at https://zerodha.com)
2. **Kite Connect Subscription**: ₹2,000/month
   - Subscribe at: https://kite.trade/

### Setup Steps

#### Step 1: Create Kite Connect App

1. Go to https://developers.kite.trade/
2. Login with your Zerodha credentials
3. Create a new app:
   - **App name**: My Intraday Scanner
   - **Redirect URL**: http://127.0.0.1:5000 (or any URL)
   - **Description**: Intraday stock scanner
4. Note down:
   - **API Key**
   - **API Secret**

#### Step 2: Install Python Library

```bash
pip install kiteconnect
```

#### Step 3: Generate Access Token

Create a file `kite_login.py`:

```python
from kiteconnect import KiteConnect

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

kite = KiteConnect(api_key=API_KEY)

# Generate login URL
print("Login URL:")
print(kite.login_url())

# After login, you'll get redirected to a URL with request_token
# Example: http://127.0.0.1:5000/?request_token=XXXXXX&action=login&status=success
# Copy the request_token from URL

request_token = input("Enter request_token from URL: ")

# Generate access token
data = kite.generate_session(request_token, api_secret=API_SECRET)
print("\nYour ACCESS TOKEN:")
print(data["access_token"])

# Save this token - it's valid for the entire day
```

Run it:
```bash
python kite_login.py
```

#### Step 4: Configure Scanner

Edit `intraday_scanner_realtime.py` and update:

```python
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
ACCESS_TOKEN = "your_access_token_here"  # Generated from step 3
```

#### Step 5: Run Scanner

```bash
python intraday_scanner_realtime.py
```

---

## 🔄 Option 2: Upstox API (Free for Clients)

### Prerequisites
- Upstox trading account
- API access (free for Upstox clients)

### Setup Steps

1. **Get API Credentials**:
   - Go to https://api.upstox.com/
   - Create app, get API key & secret

2. **Install Library**:
```bash
pip install upstox-python-sdk
```

3. **Create Upstox Version**:
   - Similar to Kite version
   - Replace `kiteconnect` with `upstox_client`
   - Adjust API calls

**Note**: Upstox has slightly different API structure. Let me know if you need the full implementation.

---

## 🌐 Option 3: Free Alternative - NSE India Official (Limited)

For basic real-time quotes (not for heavy scanning):

```python
import requests

def get_nse_quote(symbol):
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()
```

**Limitations**:
- Rate limited (max 10-20 requests/min)
- No historical data
- Requires cookie management
- Not suitable for scanning 70+ stocks

---

## ⚡ Benefits of Real-Time Data

### What Changes:

| Feature | Yahoo Finance (Free) | Real-Time API |
|---------|---------------------|---------------|
| **Delay** | ~15 minutes | 0 seconds |
| **Update Frequency** | Every 5 min candle | Tick-by-tick |
| **Bid/Ask Spread** | ❌ Not available | ✅ Live depth |
| **Order Book** | ❌ No | ✅ Full depth |
| **Scalping** | ❌ Not suitable | ✅ Perfect |
| **Swing Intraday** | ✅ Works | ✅ Better |
| **Cost** | Free | ₹2,000/month |

### Trading Strategies Unlocked:

1. **Scalping** (1-5 min trades)
   - Catch exact breakouts
   - Exit at precise levels
   - Tick-level stop-loss

2. **Opening Range Breakouts**
   - Real-time 9:15-9:30 data
   - Instant breakout alerts

3. **VWAP Trades**
   - Minute-by-minute VWAP calculation
   - Precise entries near VWAP

4. **Momentum Trades**
   - Catch sudden volume spikes
   - Real-time RSI/MACD signals

---

## 🔧 Code Differences

### Yahoo Finance (Current):
```python
# 15-minute delayed
import yfinance as yf
data = yf.download('RELIANCE.NS', interval='5m')
```

### Kite Connect (Real-Time):
```python
# Live tick data
from kiteconnect import KiteConnect
kite = KiteConnect(api_key=API_KEY)
quote = kite.quote("NSE:RELIANCE")  # Instant!
```

---

## 📊 Which One Should You Choose?

### Choose **Zerodha Kite** if:
- You're a serious trader
- You need most reliable data
- You can afford ₹2,000/month
- You want best documentation

### Choose **Upstox** if:
- You already have account with them
- You want free API access
- You're okay with occasional glitches

### Stick with **Yahoo Finance** if:
- You're learning/paper trading
- You trade swing positions (hold >30 min)
- You don't need exact entry/exit
- Budget is a concern

---

## ⚠️ Important Notes

### Access Token Validity
- Kite access tokens expire **daily**
- Must regenerate each day
- Can automate with selenium (advanced)

### Rate Limits
- Kite: 3 requests/second
- Upstox: 10 requests/second
- Plan your scan frequency accordingly

### Costs
- Kite/Fyers: ₹2,000/month (₹24,000/year)
- Data costs are **separate** from brokerage
- Tax deductible as business expense

### Backup Plan
- Keep Yahoo Finance version as backup
- APIs can have downtime
- Always have fallback

---

## 🎯 Recommendation

**Start with Yahoo Finance version** to:
1. Learn the strategy
2. Backtest your approach
3. Paper trade first

**Upgrade to Kite Connect when**:
1. You're profitable with delayed data
2. You need scalping precision
3. 15-min delay is limiting your performance

---

## 🆘 Troubleshooting

### "Token expired" error
```bash
# Re-run kite_login.py to get new token
python kite_login.py
```

### "Insufficient funds" or trading errors
```bash
# This scanner is READ-ONLY
# It doesn't place trades
# Check if you have data subscription active
```

### Data fetch errors
```bash
# Check if market is open
# Verify API credentials
# Check internet connection
# Confirm subscription is active
```

---

## 📞 Support

- **Kite Connect**: https://kite.trade/forum/
- **Upstox**: support@upstox.com

---

**Ready to go live? Start with Option 1 (Zerodha Kite) for best results!** 🚀
