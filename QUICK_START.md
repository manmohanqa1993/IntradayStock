# ⚡ Quick Start Guide - Get Running in 10 Minutes

## 🎯 Step-by-Step Setup

### Step 1: Check Python (1 minute)

Open Command Prompt:
```bash
python --version
```

✅ **If shows "Python 3.x.x"** → Go to Step 2  
❌ **If error** → Install Python from https://www.python.org/ (check "Add to PATH")

---

### Step 2: Install Packages (3-5 minutes)

**Method A: One-Click (Easiest)**
1. Double-click: **`install_requirements.bat`**
2. Wait for completion
3. Should show: "✅ All packages installed!"

**Method B: Command Line**
```bash
cd C:\Users\Manmohan.Pradhan\Desktop\stock
pip install -r requirements.txt
```

---

### Step 3: Verify Installation (30 seconds)

```bash
python test_all_apis.py
```

Should test all APIs and show results.

---

### Step 4: Run Your First Scan! (5-8 minutes)

**Double-click**: **`run_pro_scanner.bat`**

OR run:
```bash
python intraday_scanner_pro.py
```

**Output**: 3-5 premium trading setups with entry/stop/target!

---

## 📦 What Gets Installed:

| Package | Size | Purpose |
|---------|------|---------|
| yfinance | ~10 MB | Stock data from Yahoo Finance |
| pandas | ~40 MB | Data analysis |
| numpy | ~20 MB | Calculations |
| requests | ~1 MB | Web requests |
| beautifulsoup4 | ~2 MB | Web scraping |

**Total**: ~75 MB download

---

## ✅ Installation Checklist:

- [ ] Python installed (3.8+)
- [ ] Ran: `install_requirements.bat`
- [ ] Shows: "✅ All packages installed!"
- [ ] Tested: `python test_all_apis.py`
- [ ] Ready to scan!

---

## 🚀 What to Run:

### For Live Trading Signals:
```bash
# Professional scanner (BEST)
python intraday_scanner_pro.py

# Basic scanner (more results)
python intraday_scanner.py
```

### For Strategy Testing:
```bash
# Quick backtest
python backtest_scanner.py

# Full analytics
python backtest_advanced.py
```

---

## ⚠️ Common Issues:

### "Python not found"
**Fix**: Install Python and add to PATH

### "pip not recognized"  
**Fix**: Reinstall Python with "Add to PATH" checked

### "Permission denied"
**Fix**: Run Command Prompt as Administrator

### "Package install failed"
**Fix**: Try one by one:
```bash
pip install yfinance
pip install pandas
pip install numpy
```

---

## 💡 Next Steps:

1. ✅ **Install packages** (Step 2 above)
2. ✅ **Run scanner** during market hours (9:15 AM - 3:30 PM)
3. ✅ **Get 3-5 setups** with entry/stop/target
4. ✅ **Backtest** to see historical performance
5. ✅ **Paper trade** for practice
6. ✅ **Go live** when confident

---

## 📞 Quick Commands:

```bash
# Install everything
pip install -r requirements.txt

# Test installation
python test_all_apis.py

# Run scanner
python intraday_scanner_pro.py

# Run backtest
python backtest_advanced.py

# Check Python version
python --version

# Check installed packages
pip list
```

---

## 🎯 Timeline:

| Task | Time |
|------|------|
| Check Python | 1 min |
| Install packages | 3-5 min |
| Verify installation | 1 min |
| First scan | 5-8 min |
| **Total** | **~10-15 min** |

---

## 📚 Full Guides:

- **Installation details**: `INSTALLATION_GUIDE.md`
- **Scanner features**: `PRO_SCANNER_GUIDE.md`
- **Backtesting**: `BACKTESTING_GUIDE.md`
- **Complete system**: `README_COMPLETE.md`

---

**Ready? Double-click `install_requirements.bat` now!** 🚀
