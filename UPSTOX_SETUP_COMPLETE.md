# 🟢 Complete Upstox Real-Time Setup Guide (FREE!)

## ✅ What You Need

### 1. **Upstox Trading Account** (FREE)
- If you don't have one: https://upstox.com/open-account/
- Account opening is free
- No minimum balance required for API access

### 2. **API Access** (FREE for Upstox clients)
- Cost: **₹0/month** (FREE!)
- Available to all Upstox account holders
- No monthly subscription needed

### 3. **Python** (Already have)
- Python 3.8+ (you already have this)

---

## 📋 Complete Setup Checklist

### ☐ Step 1: Open Upstox Account (if not done)
- Visit: https://upstox.com
- Complete KYC process
- Wait for approval (1-2 days)

### ☐ Step 2: Create API App

1. **Login to Developer Console**:
   - Go to: https://account.upstox.com/developer/apps
   - Login with your Upstox credentials

2. **Create New App**:
   - Click "Create App"
   - Fill details:
     ```
     App Name: My Intraday Scanner
     Redirect URL: http://127.0.0.1:5000
     Description: Stock scanner for intraday trading
     ```

3. **Save Credentials**:
   - Copy **API Key** (looks like: abc123xyz456)
   - Copy **API Secret** (looks like: def789ghi012)
   - Keep these secure!

### ☐ Step 3: Install Python Libraries

Open Command Prompt in your `stock` folder and run:

```bash
pip install -r requirements_upstox.txt
```

Or install individually:
```bash
pip install upstox-client pandas numpy
```

### ☐ Step 4: Configure Login Script

1. Open `upstox_login.py`
2. Update these lines (around line 8-10):
   ```python
   API_KEY = "your_api_key_from_step_2"
   API_SECRET = "your_api_secret_from_step_2"
   REDIRECT_URI = "http://127.0.0.1:5000"
   ```

### ☐ Step 5: Generate Access Token

Run the login script:
```bash
python upstox_login.py
```

**What will happen:**
1. Browser opens with Upstox login
2. You login and authorize
3. URL changes to: `http://127.0.0.1:5000/?code=XXXXXX`
4. Copy the code after `?code=`
5. Paste in terminal
6. Access token is generated!

**Example:**
```
Redirected URL: http://127.0.0.1:5000/?code=abc123
Enter code: abc123  ← Type this
```

### ☐ Step 6: Configure Scanner

1. Open `intraday_scanner_upstox.py`
2. Update credentials (line 15-17):
   ```python
   API_KEY = "your_api_key"
   API_SECRET = "your_api_secret"
   ACCESS_TOKEN = "token_from_step_5"  # Paste token here
   ```

Alternatively, copy from `upstox_token.txt` (auto-generated).

### ☐ Step 7: Run Scanner!

```bash
python intraday_scanner_upstox.py
```

**Expected Output:**
```
🟢 LIVE NSE SCANNER - UPSTOX API (FREE)
⚡ Using REAL-TIME data with ZERO delay
Universe: 50 stocks

✅ Found 8 High-Quality Opportunities:

1. RELIANCE - BULLISH 🟢 LIVE (FREE API)
   LTP: ₹2,456.75 | Bid: ₹2,456.50 | Ask: ₹2,457.00
   Change: +2.34% | Volume: 2.1x avg
   ...
```

---

## 🎯 Summary: What You Need

| Item | Where to Get | Cost | Status |
|------|-------------|------|--------|
| **Upstox Account** | https://upstox.com | Free | ☐ |
| **API Key** | https://account.upstox.com/developer/apps | Free | ☐ |
| **API Secret** | Same as above | Free | ☐ |
| **Access Token** | Run `upstox_login.py` | Free | ☐ |
| **Python Libraries** | `pip install upstox-client` | Free | ☐ |

**Total Cost: ₹0 (COMPLETELY FREE!)**

---

## 🔄 Daily Workflow

### Every Morning (Takes 2 minutes):

1. **Generate fresh token** (expires daily):
   ```bash
   python upstox_login.py
   ```

2. **Update scanner** with new token:
   - Copy token from `upstox_token.txt`
   - Paste in `intraday_scanner_upstox.py`

3. **Run scanner**:
   ```bash
   python intraday_scanner_upstox.py
   ```

### Optional: Automate Token Generation

You can save credentials in environment variables:
```bash
# Windows (Command Prompt)
set UPSTOX_API_KEY=your_key
set UPSTOX_API_SECRET=your_secret

# Or add to script permanently
```

---

## ⚠️ Important Notes

### Token Validity
- **Expires**: End of trading day (3:30 PM)
- **Re-generate**: Every morning before market
- **Quick process**: Takes 30 seconds

### Rate Limits
- **10 requests/second** (very generous)
- **Scanner respects limits** (0.15s delay between stocks)
- No daily request limit

### Market Hours
- **Works only during**: 9:15 AM - 3:30 PM IST
- Outside hours: Historical data still available

### Data Quality
- **Delay**: 0 seconds (live!)
- **Update frequency**: Tick-by-tick
- **Depth**: 5 levels bid/ask
- **Quality**: Same as paid Kite Connect

---

## 🆘 Troubleshooting

### "Module not found: upstox_client"
```bash
pip install upstox-client
```

### "Invalid API credentials"
- Check if API_KEY and API_SECRET are correct
- Verify you copied them completely (no spaces)
- Go to Upstox developer console and regenerate if needed

### "Token expired"
- Access tokens expire daily
- Re-run `upstox_login.py` every morning
- Can't avoid this (security feature)

### "Authorization code invalid"
- Code expires in 5 minutes
- Don't refresh browser after authorization
- Copy code immediately after redirect

### "Instrument not found"
- Some stocks may have different symbols
- Check Upstox instrument master:
  https://assets.upstox.com/market-quote/instruments/exchange/NSE.csv

### "Rate limit exceeded"
- Scanner has 0.15s delay (within limits)
- If scanning more stocks, increase delay:
  ```python
  time.sleep(0.2)  # Line 331 in upstox scanner
  ```

---

## 🎁 Benefits vs Yahoo Finance

| Feature | Yahoo (Free) | Upstox (FREE!) |
|---------|-------------|----------------|
| **Data Delay** | 15 minutes | 0 seconds ⚡ |
| **Cost** | Free | Free 💰 |
| **Bid/Ask** | ❌ | ✅ |
| **Order Depth** | ❌ | ✅ 5 levels |
| **Update Speed** | 5 min candles | Tick-by-tick |
| **Scalping** | ❌ | ✅ |
| **API Limits** | Unlimited | 10 req/sec |
| **Account Required** | No | Yes (free) |

---

## 📞 Support

### Upstox Support
- **Developer Docs**: https://upstox.com/developer/api-documentation/
- **Forum**: https://forum.upstox.com/
- **Email**: api@upstox.com
- **Phone**: 080-47181888

### Common Links
- **Developer Console**: https://account.upstox.com/developer/apps
- **Instrument List**: https://assets.upstox.com/market-quote/instruments/
- **API Limits**: https://upstox.com/developer/api-documentation/rate-limiting

---

## 🚀 Next Steps After Setup

1. **Paper Trade First**:
   - Watch signals for 1-2 weeks
   - Don't trade real money yet
   - Validate strategy

2. **Customize Scanner**:
   - Add/remove stocks in `NSE_STOCKS` list
   - Adjust criteria thresholds
   - Add more indicators

3. **Set Up Live Monitor**:
   - Create auto-refreshing version
   - Add alerts for new signals
   - Build notification system

4. **Upgrade Strategy**:
   - Backtest with historical data
   - Add machine learning
   - Build automated trading (be careful!)

---

## ✅ Quick Start Summary

**For someone who has Upstox account:**

1. Get API credentials (5 min): https://account.upstox.com/developer/apps
2. Install library: `pip install upstox-client`
3. Update `upstox_login.py` with credentials
4. Run `python upstox_login.py` → Get token
5. Update `intraday_scanner_upstox.py` with token
6. Run `python intraday_scanner_upstox.py`
7. Start scanning! 🎉

**Total time: 10-15 minutes**
**Total cost: ₹0**

---

**You now have FREE real-time NSE data! Happy trading! 📈**
