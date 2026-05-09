1# 🚀 Kite (Zerodha) Scanner Setup Guide

## What is Kite Connect?

**Kite Connect** is Zerodha's official API that provides:
- ✅ **Real-time tick data** (zero delay)
- ✅ **Live market quotes** with bid/ask prices
- ✅ **Historical data** for backtesting
- ✅ **Order placement** capability (optional)
- ✅ **FREE for Zerodha customers!**

---

## ⚠️ Prerequisites

1. **Active Zerodha Trading Account** (Demat + Trading)
2. **Python 3.8+** installed
3. **Internet connection**
4. **Zerodha Developer Account** (free to create)

---

## 📋 Setup Steps

### Step 1: Create Kite Connect App (5 minutes)

1. **Go to**: https://developers.kite.trade/
2. **Login** with your Zerodha credentials
3. Click **"Create new app"**
4. Fill in details:
   - **App name**: "Intraday Scanner" (or any name)
   - **Redirect URL**: `http://127.0.0.1` (important!)
   - **Description**: "Personal stock scanner"
   - **Type**: Select "Connect"
5. Click **"Create"**

6. **You'll get**:
   ```
   API Key: xxxxxxxxxxxxxxxx
   API Secret: yyyyyyyyyyyyyyyy
   ```
   **Copy these!** You'll need them.

---

### Step 2: Install Required Package (1 minute)

```bash
pip install kiteconnect
```

Or add to your `requirements.txt`:
```
kiteconnect
```

---

### Step 3: Generate Access Token (3 minutes)

**Access tokens expire daily at 6:00 AM**, so you need to generate a fresh one each day.

#### Method A: Using the Login Script (Recommended)

1. **Open**: `kite_login.py`
2. **Update your credentials**:
   ```python
   API_KEY = "your_api_key_here"        # From Step 1
   API_SECRET = "your_api_secret_here"  # From Step 1
   ```

3. **Run the script**:
   ```bash
   python kite_login.py
   ```

4. **Follow the prompts**:
   - Opens a login URL in browser
   - Login with Zerodha credentials
   - Copy the `request_token` from redirected URL
   - Paste it back in the terminal

5. **You'll get**:
   ```
   ACCESS_TOKEN = "zzzzzzzzzzzzzzzz"
   ```

6. **Copy this token** to `intraday_scanner_kite.py`:
   ```python
   API_KEY = "xxxxxxxxxxxxxxxx"
   API_SECRET = "yyyyyyyyyyyyyyyy"
   ACCESS_TOKEN = "zzzzzzzzzzzzzzzz"
   ```

---

### Step 4: Run the Scanner (2 minutes)

**Method A: Batch File (Easy)**
```bash
Double-click: run_kite_scanner.bat
```

**Method B: Command Line**
```bash
python intraday_scanner_kite.py
```

---

## 📊 How It Works

### Data Flow:
```
Zerodha Kite API
    ↓
Live Tick Data (Zero Delay)
    ↓
Professional Filters Applied
    ↓
3-5 Premium Trading Setups
    ↓
CSV Saved: kite_scanner_output/YYYY-MM-DD/scan_HHMM.csv
```

### Filters Applied:
1. ✅ Price >₹100
2. ✅ Movement: 1.5% to 2% (no excessive gaps)
3. ✅ Volume: 2× average, >500K shares
4. ✅ VWAP alignment
5. ✅ EMA trend (20>50 bullish, 20<50 bearish)
6. ✅ RSI ranges (50-70 buy, 30-50 sell)
7. ✅ Breakout/breakdown confirmation
8. ✅ ATR >1% OR range >1.5%
9. ✅ Entry/Stop/Target with 1:2 R:R

---

## 🔄 Daily Workflow

### Morning Routine (Before Market Opens):

**1. Generate Fresh Token** (6:00 AM - 9:00 AM)
```bash
python kite_login.py
```
This gives you a fresh access token valid until next day.

**2. Update Token** in `intraday_scanner_kite.py`
```python
ACCESS_TOKEN = "new_token_here"
```

**3. Run Scanner** (During market hours)
```bash
python intraday_scanner_kite.py
```
Or double-click: `run_kite_scanner.bat`

---

## 🆚 Comparison: Kite vs Yahoo Finance

| Feature | Kite (Zerodha) | Yahoo Finance |
|---------|----------------|---------------|
| **Data Delay** | ⚡ Zero delay | 🕐 15 minutes |
| **Bid/Ask Prices** | ✅ Yes | ❌ No |
| **Cost** | 💰 Free (Zerodha customers) | 💰 Free (everyone) |
| **Setup** | 🔧 Moderate (API setup needed) | 🔧 Easy (no setup) |
| **Token Validity** | 🔄 Daily renewal | ♾️ No expiry |
| **Data Quality** | ⭐⭐⭐⭐⭐ Exchange data | ⭐⭐⭐⭐ Delayed data |
| **Best For** | Active day trading | Swing trading |

---

## 📁 Output Files

Scanner saves results in organized folders:

```
kite_scanner_output/
├── 2026-05-04/
│   ├── scan_0945.csv    ← First scan
│   ├── scan_1030.csv    ← Second scan
│   └── scan_1400.csv    ← Third scan
└── 2026-05-05/
    └── scan_0945.csv
```

---

## ⚠️ Common Issues

### Issue 1: "TokenException: Invalid access token"

**Cause**: Access token expired (they expire daily at 6:00 AM)

**Fix**: 
```bash
python kite_login.py
```
Generate a fresh token and update `intraday_scanner_kite.py`

---

### Issue 2: "NetworkException: Connection timeout"

**Cause**: Internet connection or Zerodha server issue

**Fix**:
- Check internet connection
- Try again in 2-3 minutes
- Check Zerodha server status: https://status.kite.trade/

---

### Issue 3: "InputException: Incorrect API credentials"

**Cause**: Wrong API_KEY or API_SECRET

**Fix**:
- Verify credentials at https://developers.kite.trade/
- Make sure you copied them correctly
- No extra spaces or quotes

---

### Issue 4: "Request token expired"

**Cause**: Request token valid for only 2-3 minutes

**Fix**:
- Re-run `kite_login.py`
- Complete the login process quickly
- Paste request_token within 2 minutes

---

## 🔐 Security Best Practices

1. **Never share** your API_KEY, API_SECRET, or ACCESS_TOKEN
2. **Don't commit** credentials to GitHub/version control
3. **Regenerate** API credentials if accidentally exposed
4. **Use** only for personal trading, not for distribution
5. **Store** credentials in a secure location

---

## 💡 Pro Tips

### Tip 1: Automate Daily Token Generation

Create a scheduled task to run `kite_login.py` automatically at 8:00 AM daily.

### Tip 2: Multiple Scans Throughout Day

Run scanner at:
- **9:45 AM** - Opening range setups
- **10:30 AM** - Trend confirmation
- **2:00 PM** - Afternoon momentum

### Tip 3: Combine with Live Monitor

Modify `live_monitor.py` to use Kite instead of Yahoo Finance for continuous real-time scanning.

### Tip 4: Order Placement (Advanced)

Kite API can also place orders directly. Add this feature for one-click trading (use with caution!).

---

## 📚 Additional Resources

- **Kite Connect Docs**: https://kite.trade/docs/connect/v3/
- **API Forum**: https://forum.kite.trade/
- **Python Library**: https://github.com/zerodhatech/pykiteconnect
- **Rate Limits**: 3 requests/second per API key

---

## 🎯 Quick Command Reference

```bash
# Install package
pip install kiteconnect

# Generate access token (daily)
python kite_login.py

# Run scanner
python intraday_scanner_kite.py
# OR
Double-click: run_kite_scanner.bat

# Check installed version
pip show kiteconnect
```

---

## ✅ Setup Checklist

Before running the scanner, ensure:

- [ ] Zerodha trading account is active
- [ ] Created Kite Connect app at developers.kite.trade
- [ ] Copied API_KEY and API_SECRET
- [ ] Installed kiteconnect package (`pip install kiteconnect`)
- [ ] Generated fresh ACCESS_TOKEN (runs daily)
- [ ] Updated credentials in `intraday_scanner_kite.py`
- [ ] Tested connection with `kite_login.py`
- [ ] Ready to scan during market hours (9:15 AM - 3:30 PM)

---

## 🚀 Ready to Trade!

Once setup is complete:

1. **Generate token** each morning: `python kite_login.py`
2. **Run scanner** at key times: `run_kite_scanner.bat`
3. **Get 3-5 premium setups** with entry/stop/target
4. **Trade with confidence** using real-time data!

---

**Need Help?**
- Kite Support: https://support.zerodha.com/
- Developer Forum: https://forum.kite.trade/

**Happy Trading!** 📈💰
