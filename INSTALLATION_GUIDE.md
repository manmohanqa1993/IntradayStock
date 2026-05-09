# 🔧 Installation Guide - Complete Setup

## ✅ Quick Check: Do You Have Python?

Open Command Prompt and type:
```bash
python --version
```

**Should show**: Python 3.8 or higher (e.g., Python 3.11.5)

**If not installed**:
1. Download from: https://www.python.org/downloads/
2. During installation: ✅ Check "Add Python to PATH"
3. Restart computer after installation

---

## 📦 Required Packages Installation

### Method 1: One-Click Install (Easiest) ⭐

**Double-click**: `install_requirements.bat`

This will install everything automatically!

### Method 2: Manual Install

Open Command Prompt in the stock folder and run:

```bash
pip install -r requirements.txt
```

### Method 3: Individual Install

If above doesn't work, install one by one:

```bash
pip install yfinance
pip install pandas
pip install numpy
pip install requests
pip install beautifulsoup4
```

**For Upstox Scanner** (optional, only if using Upstox):
```bash
pip install upstox-client
```

---

## ✅ Verify Installation

Run this command to check:
```bash
python -c "import yfinance, pandas, numpy; print('✅ All packages installed!')"
```

**Should show**: ✅ All packages installed!

---

## 🎯 What Each Package Does:

| Package | Purpose | Required For |
|---------|---------|--------------|
| **yfinance** | Yahoo Finance data | All scanners, backtesting |
| **pandas** | Data analysis | All scanners, backtesting |
| **numpy** | Numerical calculations | All scanners, backtesting |
| **requests** | HTTP requests | NSE direct scanner |
| **beautifulsoup4** | Web scraping | NSE direct scanner |
| **upstox-client** | Upstox API | Upstox scanner only |

---

## 🚀 Quick Start After Installation

### 1. Test Installation:
```bash
python test_all_apis.py
```

This will check if everything works!

### 2. Run Your First Scan:
```bash
python intraday_scanner_pro.py
```

Or double-click: `run_pro_scanner.bat`

---

## ⚠️ Common Installation Issues

### Issue 1: "pip is not recognized"

**Solution**: Python not added to PATH

**Fix**:
1. Reinstall Python
2. ✅ Check "Add Python to PATH" during installation
3. OR manually add to PATH:
   - Search "Environment Variables" in Windows
   - Edit PATH
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311`
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts`

### Issue 2: "Access Denied" or "Permission Error"

**Solution**: Run as Administrator

**Fix**:
1. Right-click Command Prompt
2. Select "Run as Administrator"
3. Run installation commands

### Issue 3: "ModuleNotFoundError: No module named 'yfinance'"

**Solution**: Package not installed

**Fix**:
```bash
pip install yfinance
```

### Issue 4: Multiple Python Versions

**Solution**: Use specific Python version

**Fix**:
```bash
python3 -m pip install -r requirements.txt
# OR
py -3 -m pip install -r requirements.txt
```

### Issue 5: Corporate Firewall/Proxy

**Solution**: Install with proxy settings

**Fix**:
```bash
pip install --proxy=http://your-proxy:port yfinance
# OR download packages manually from PyPI
```

---

## 🔍 Detailed Installation Steps

### For Windows:

**Step 1: Open Command Prompt**
1. Press `Win + R`
2. Type: `cmd`
3. Press Enter

**Step 2: Navigate to Stock Folder**
```bash
cd C:\Users\Manmohan.Pradhan\Desktop\stock
```

**Step 3: Install Packages**
```bash
pip install -r requirements.txt
```

**Step 4: Wait**
- Will download and install packages
- Takes 2-5 minutes depending on internet speed

**Step 5: Verify**
```bash
python test_all_apis.py
```

---

## 📋 Installation Checklist

Before running scanners, ensure:

- [ ] Python 3.8+ installed
- [ ] Python added to PATH
- [ ] pip working (`pip --version`)
- [ ] yfinance installed
- [ ] pandas installed
- [ ] numpy installed
- [ ] requests installed (for NSE direct)
- [ ] Can run: `python --version`
- [ ] Can run: `pip --version`
- [ ] Test script passes: `python test_all_apis.py`

---

## 🎯 After Installation

### Test Each Scanner:

**1. Professional Scanner:**
```bash
python intraday_scanner_pro.py
```
Should scan stocks and show results (takes 5-8 min)

**2. Basic Scanner:**
```bash
python intraday_scanner.py
```

**3. Backtest:**
```bash
python backtest_scanner.py
```
Should test strategy on historical data (takes 10-15 min)

---

## 💡 Pro Tips

### Keep Packages Updated:
```bash
pip install --upgrade yfinance pandas numpy
```

### Check Installed Versions:
```bash
pip list
```

### Uninstall if Needed:
```bash
pip uninstall yfinance
pip uninstall pandas
```

### Create Virtual Environment (Advanced):
```bash
# Create virtual environment
python -m venv stock_env

# Activate it
stock_env\Scripts\activate

# Install packages
pip install -r requirements.txt

# Deactivate when done
deactivate
```

---

## 🆘 Still Having Issues?

### Option 1: Use Google Colab (No Installation Needed!)
1. Upload: `NSE_Intraday_Scanner_Colab.ipynb`
2. Go to: https://colab.research.google.com/
3. Upload notebook
4. Click "Runtime" → "Run all"
5. Everything runs in cloud!

### Option 2: Fresh Python Installation
1. Uninstall current Python completely
2. Download latest from https://www.python.org/
3. Install with "Add to PATH" ✅ checked
4. Restart computer
5. Install packages again

### Option 3: Use Anaconda
1. Download: https://www.anaconda.com/download
2. Install Anaconda
3. Open Anaconda Prompt
4. Run: `conda install -c conda-forge yfinance pandas numpy`

---

## 📊 Expected Installation Time

| Step | Time |
|------|------|
| Python installation | 5-10 min |
| Package download | 2-5 min |
| Package installation | 1-3 min |
| Verification | 1 min |
| **Total** | **~10-20 min** |

---

## ✅ Final Verification

Run this complete test:

```bash
python -c "
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime

print('✅ All packages imported successfully!')
print(f'yfinance version: {yf.__version__}')
print(f'pandas version: {pd.__version__}')
print(f'numpy version: {np.__version__}')
print('🎉 Ready to scan!')
"
```

**Should show**:
```
✅ All packages imported successfully!
yfinance version: 0.2.xx
pandas version: 2.x.x
numpy version: 1.xx.x
🎉 Ready to scan!
```

---

## 🎯 You're Ready!

Once all packages are installed:

1. ✅ Run: `python intraday_scanner_pro.py`
2. ✅ See scanning in action
3. ✅ Get 3-5 trading setups
4. ✅ Start backtesting with: `python backtest_advanced.py`

---

## 📞 Quick Reference

**Install everything:**
```bash
pip install -r requirements.txt
```

**Verify installation:**
```bash
python test_all_apis.py
```

**Run scanner:**
```bash
python intraday_scanner_pro.py
```

**Run backtest:**
```bash
python backtest_advanced.py
```

---

**Installation done? Let's scan!** 🚀📈
