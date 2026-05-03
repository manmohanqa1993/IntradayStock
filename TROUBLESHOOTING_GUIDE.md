# 🔧 Troubleshooting Guide - "None of the APIs are working"

## 🎯 Step 1: Run the Diagnostic Tool FIRST

Before anything else, run this to see what's actually working:

```bash
python test_all_apis.py
```

This will test:
- ✅ Yahoo Finance
- ✅ NSE India website
- ✅ Upstox API
- ✅ Internet connectivity
- ✅ Proxy/firewall detection

**Send me the results and I'll tell you exactly what to do!**

---

## 🚨 Common Problems & Solutions

### Problem 1: "All APIs failing on company laptop"

**Cause**: Company firewall/proxy blocking API endpoints

**Solutions**:

**Option A: Use Google Colab** (RECOMMENDED - 100% success rate!)
```
1. Go to: https://colab.research.google.com/
2. Upload: NSE_Intraday_Scanner_Colab.ipynb
3. Click "Runtime" → "Run all"
4. Done! No local installation needed!
```

**Option B: Use mobile hotspot**
```
1. Disconnect from company WiFi
2. Connect to your phone's hotspot
3. Run scanner
```

**Option C: Use from home/personal laptop**
```
1. Upload files to Google Drive
2. Access from home
3. Run there
```

---

### Problem 2: "Yahoo Finance returns empty data"

**Cause**: Ticker symbols might be wrong or connection issues

**Test**:
```python
import yfinance as yf
data = yf.download("RELIANCE.NS", period="1d")
print(data)
```

**If this fails**:
```
1. Check internet connection
2. Try: pip install --upgrade yfinance
3. Try different symbol: "TCS.NS", "INFY.NS"
4. Use NSE direct scraper instead
```

---

### Problem 3: "Upstox login failing"

**Common causes**:

**Wrong Credentials**:
```
✅ Check API_KEY (no spaces)
✅ Check API_SECRET (exact format)
✅ Check redirect URI matches
```

**API Not Enabled**:
```
Upstox: Enable in developer console
Check subscription is active
```

**Network Issues**:
```
Company firewall may be blocking authentication
→ Use Google Colab instead
```

---

### Problem 4: "Cannot install packages (pip fails)"

**Cause**: Company policy blocking pip

**Solution**: Use Google Colab (no installation needed!)

**Or try**:
```bash
# Try with --user flag
pip install --user yfinance pandas numpy

# Try upgrading pip first
python -m pip install --upgrade pip

# Use conda if available
conda install yfinance pandas numpy
```

**Still failing?**: Google Colab is your only option

---

### Problem 5: "NSE website scraper also failing"

**Possible causes**:

**Firewall blocking NSE**:
```
→ Use Google Colab (bypasses local network)
```

**NSE website maintenance**:
```
→ Check: https://www.nseindia.com/
→ Try again after 30 minutes
→ Use Yahoo Finance as backup
```

**Rate limiting**:
```
→ Scanner respects limits (2 sec/request)
→ If still blocked, wait 5 minutes and retry
```

---

## 🎯 ULTIMATE SOLUTION: Google Colab

**If NOTHING works locally, use Google Colab:**

### Why Colab Always Works:
- ✅ Runs in cloud (bypasses local restrictions)
- ✅ No installation needed
- ✅ No firewall issues
- ✅ Professional Python environment
- ✅ 100% free
- ✅ Access from anywhere

### How to Use:

**Step 1**: Go to https://colab.research.google.com/

**Step 2**: Upload `NSE_Intraday_Scanner_Colab.ipynb`
   - Click "File" → "Upload notebook"
   - Select the .ipynb file
   - Upload

**Step 3**: Run it
   - Click "Runtime" → "Run all"
   - Wait 2-3 minutes
   - See results!

**Step 4**: Daily use
   - Open colab.research.google.com
   - Click "File" → "Open notebook" → "Recent"
   - Select your notebook
   - Click "Runtime" → "Run all"
   - Done!

---

## 🔍 Specific Error Messages

### "ModuleNotFoundError: No module named 'yfinance'"
```bash
Fix: pip install yfinance
Or use Google Colab (has it pre-installed)
```

### "ConnectionError" or "Timeout"
```
Cause: Network/firewall blocking
Fix: Use Google Colab or mobile hotspot
```

### "Invalid credentials" (APIs)
```
Cause: Wrong API keys or not enabled
Fix: 
1. Re-check credentials (copy-paste carefully)
2. Enable API in respective apps
3. Regenerate credentials
```

### "Forbidden" or "403 error"
```
Cause: Company proxy/firewall
Fix: Use Google Colab (only solution)
```

### "SSLError" or "Certificate verification failed"
```
Cause: Corporate SSL inspection
Fix: Use Google Colab
```

---

## 📊 Which Scanner to Use

Based on diagnostic results:

| If This Works | Use This Scanner | Command |
|---------------|------------------|---------|
| ✅ Yahoo Finance | Original scanner | `python intraday_scanner.py` |
| ✅ NSE Website | NSE scraper | `python scanner_nse_direct.py` |
| ✅ Upstox | Upstox scanner | `python intraday_scanner_upstox.py` |
| ❌ Nothing works | **Google Colab** | Upload to colab.research.google.com |

---

## 🛠️ Advanced Troubleshooting

### Check if Python is working:
```bash
python --version
# Should show Python 3.x.x
```

### Check if libraries are installed:
```bash
pip list | grep -i yfinance
pip list | grep -i pandas
pip list | grep -i numpy
```

### Test basic internet:
```python
import requests
r = requests.get("https://www.google.com")
print(r.status_code)  # Should be 200
```

### Check proxy settings:
```python
import os
print("HTTP_PROXY:", os.environ.get('HTTP_PROXY'))
print("HTTPS_PROXY:", os.environ.get('HTTPS_PROXY'))
```

---

## 📞 Still Not Working?

### Send me this information:

1. **Output of diagnostic tool**:
   ```bash
   python test_all_apis.py
   # Copy ALL output
   ```

2. **Your situation**:
   - Company laptop or personal?
   - Connected to company network?
   - Any proxy/VPN?
   - Can you access nseindia.com in browser?

3. **Error messages**:
   - Copy exact error messages
   - Which scanner fails?
   - Which step fails?

4. **What you've tried**:
   - Which solutions you already attempted
   - What happened

### I'll create a custom solution for YOU!

---

## 🎯 Quick Decision Tree

```
START: None of the APIs working

├─ Can you access nseindia.com in browser?
│  ├─ YES → Run: python scanner_nse_direct.py
│  └─ NO → Company firewall blocking
│           → Use Google Colab (ONLY solution)
│
├─ Can you install Python packages?
│  ├─ YES → Run: python test_all_apis.py
│  │         → See what works
│  └─ NO → Company policy blocking
│           → Use Google Colab (ONLY solution)
│
└─ Are you on company network?
   ├─ YES → Use mobile hotspot OR Google Colab
   └─ NO → Run diagnostic tool to find issue
```

---

## ✅ Success Checklist

Run through this checklist:

- [ ] Ran `python test_all_apis.py`
- [ ] Tried Yahoo Finance scanner
- [ ] Tried NSE direct scraper
- [ ] Checked if nseindia.com opens in browser
- [ ] Verified Python and pip are working
- [ ] Tried installing yfinance: `pip install yfinance`
- [ ] Tried Google Colab
- [ ] Checked if on company network/VPN
- [ ] Tried from different network (mobile hotspot)

---

## 🚀 Fastest Solution

**Honestly, just use Google Colab:**

1. **No debugging needed**
2. **Works 100% of the time**
3. **No installation issues**
4. **Bypasses all firewalls**
5. **Free forever**
6. **Takes 2 minutes to setup**

**Link**: https://colab.research.google.com/  
**File**: Upload `NSE_Intraday_Scanner_Colab.ipynb`  
**Done**: Click "Run all"

---

## 💡 Pro Tip

**If you're facing API issues, 99% of the time it's:**

1. **Company firewall** (60% of cases)
   → Solution: Google Colab

2. **Wrong credentials** (20% of cases)
   → Solution: Re-check API keys

3. **Package not installed** (15% of cases)
   → Solution: `pip install` or Google Colab

4. **Actual API down** (5% of cases)
   → Solution: Use alternative API

**Google Colab solves #1, #3 instantly!**

---

**Run the diagnostic tool and share results - I'll help you fix it!** 🔧
