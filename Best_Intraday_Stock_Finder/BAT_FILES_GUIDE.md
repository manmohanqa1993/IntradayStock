# 🖱️ Batch Files Guide - Easy Windows Setup

## 📁 All Batch Files Created

I've created **8 batch files** for easy point-and-click operation:

---

## 1️⃣ **Quick_Setup.bat** ⭐ START HERE!

**Purpose**: Complete automated setup wizard

**What it does**:
- ✅ Checks if Python is installed
- ✅ Installs all required packages
- ✅ Opens config.py for you to add credentials
- ✅ Guides you through Telegram setup
- ✅ Shows next steps

**Usage**:
```
Double-click → Quick_Setup.bat
```

**First time?** → Use this file!

---

## 2️⃣ **Install_Requirements.bat**

**Purpose**: Install Python packages only

**What it does**:
- Installs all packages from requirements.txt
- Shows installation progress
- Reports success/failure

**Usage**:
```
Double-click → Install_Requirements.bat
```

**When to use**: 
- After downloading the project
- After updating requirements.txt

---

## 3️⃣ **Run_Scanner.bat** 🚀 MAIN FILE

**Purpose**: Start the stock screener

**What it does**:
- Checks Python installation
- Runs Best_Intraday_Stock_Finder.py
- Shows all signals in console
- Runs until you press Ctrl+C

**Usage**:
```
Double-click → Run_Scanner.bat
```

**Use this**: Every trading day to start scanning!

**Tip**: Create desktop shortcut for quick access

---

## 4️⃣ **Test_Telegram.bat**

**Purpose**: Test Telegram alert connection

**What it does**:
- Tests if Telegram bot is configured correctly
- Sends test message to your Telegram
- Shows success/error messages

**Usage**:
```
Double-click → Test_Telegram.bat
```

**When to use**:
- After configuring Telegram in config.py
- To verify alerts are working

---

## 5️⃣ **Test_Free_API.bat**

**Purpose**: Test FREE Yahoo Finance connection

**What it does**:
- Tests if yfinance is installed
- Fetches RELIANCE data from Yahoo
- Shows current price and candle count
- Verifies API is working

**Usage**:
```
Double-click → Test_Free_API.bat
```

**When to use**:
- First time setup (if using FREE Yahoo only)
- To verify Yahoo Finance is accessible

---

## 6️⃣ **Test_Hybrid_API.bat** ⭐ NEW!

**Purpose**: Test HYBRID NSE + Yahoo connection

**What it does**:
- ✅ Tests NSE Official data connection
- ✅ Tests Yahoo Finance 5-min candles
- ✅ Shows data from both sources
- ✅ Verifies hybrid mode is working

**Usage**:
```
Double-click → Test_Hybrid_API.bat
```

**When to use**:
- **RECOMMENDED:** Use this if running FREE hybrid mode
- Verifies both NSE and Yahoo are working
- Tests the best free setup

---

## 7️⃣ **View_Signals.bat**

**Purpose**: Open signals output folder

**What it does**:
- Opens `signals_output/` folder in Explorer
- Shows all generated CSV and JSON files
- Organized by date

**Usage**:
```
Double-click → View_Signals.bat
```

**When to use**:
- After running scanner
- To review past signals
- To analyze performance

---

## 8️⃣ **View_Logs.bat**

**Purpose**: View error logs and debug info

**What it does**:
- Opens `logs/screener.log` in Notepad
- Shows all scanner activity
- Helps debug issues

**Usage**:
```
Double-click → View_Logs.bat
```

**When to use**:
- If scanner crashes
- If signals aren't showing
- To debug broker connection issues

---

## 🎯 Quick Start - Which File to Use?

### First Time Setup (Day 1):

**FREE Version (No broker API):**
1. **Quick_Setup.bat** ← Start here
2. **Test_Hybrid_API.bat** ← Verify NSE+Yahoo connection
3. **Run_Scanner.bat** ← Start scanning!

**Broker API Version:**
1. **Quick_Setup.bat** ← Start here
2. Add broker credentials in config.py
3. **Test_Telegram.bat** (optional)
4. **Run_Scanner.bat** ← Start scanning!

### Daily Usage (Day 2+):

1. **Run_Scanner.bat** ← Start of day
2. Let it run during market hours
3. **View_Signals.bat** ← End of day

### Troubleshooting:

1. Scanner not working? → **View_Logs.bat**
2. Telegram not alerting? → **Test_Telegram.bat**
3. Need to reinstall? → **Install_Requirements.bat**

---

## 📝 File Locations

All batch files are in:
```
Best_Intraday_Stock_Finder/
├── Quick_Setup.bat          ⭐ Setup wizard
├── Install_Requirements.bat  📦 Install packages
├── Run_Scanner.bat          🚀 Start scanner (MAIN)
├── Test_Telegram.bat        💬 Test alerts
├── Test_Free_API.bat        🆓 Test Yahoo Finance
├── Test_Hybrid_API.bat      ⭐ Test NSE+Yahoo (NEW!)
├── View_Signals.bat         📊 See signals
└── View_Logs.bat            📄 Check logs
```

---

## 💡 Pro Tips

### Create Desktop Shortcuts:

**For daily use, create shortcut**:
1. Right-click `Run_Scanner.bat`
2. Send to → Desktop (create shortcut)
3. Rename to "Stock Scanner"
4. Double-click daily to scan!

### Run Multiple Scanners:

You can run multiple instances with different settings:
1. Copy the entire folder
2. Rename to "Scanner_Zerodha", "Scanner_Angel", etc.
3. Configure each with different broker
4. Run all simultaneously!

### Auto-Start on Windows Login:

1. Press Win+R
2. Type: `shell:startup`
3. Create shortcut to `Run_Scanner.bat` here
4. Scanner will start automatically when you login!

---

## ⚠️ Common Issues

### "Python is not recognized"

**Solution**: 
1. Install Python from https://www.python.org/
2. **CHECK** "Add Python to PATH" during installation
3. Restart computer
4. Run `Quick_Setup.bat` again

### "Access Denied" or "Permission Error"

**Solution**:
1. Right-click the .bat file
2. Select "Run as Administrator"

### "Module not found"

**Solution**:
1. Run `Install_Requirements.bat`
2. If still fails, manually install:
   ```
   pip install pandas numpy requests kiteconnect
   ```

### Batch file opens and closes immediately

**Solution**:
- This is normal if there's an error
- Open Command Prompt manually
- Navigate to folder: `cd C:\Users\...\Best_Intraday_Stock_Finder`
- Run manually: `python Best_Intraday_Stock_Finder.py`
- You'll see the actual error

---

## 🔧 Customizing Batch Files

All .bat files are editable:
1. Right-click → Edit
2. Modify as needed
3. Save

**Example - Change Python command**:
```batch
REM Change this:
python Best_Intraday_Stock_Finder.py

REM To this (if using python3):
python3 Best_Intraday_Stock_Finder.py
```

---

## ✅ Verification

After running `Quick_Setup.bat`, verify:

- [ ] Python installed (shows version)
- [ ] Packages installed (no errors)
- [ ] config.py has your broker credentials
- [ ] (Optional) Telegram configured
- [ ] Can run `Run_Scanner.bat` without errors

---

## 📞 Quick Reference

| Want to... | Use this file... |
|-----------|-----------------|
| Setup everything first time | Quick_Setup.bat |
| Start scanning | Run_Scanner.bat |
| Install/update packages | Install_Requirements.bat |
| Test Telegram | Test_Telegram.bat |
| See generated signals | View_Signals.bat |
| Debug issues | View_Logs.bat |

---

## 🎉 Ready to Use!

Just double-click the files - no command line needed!

**Recommended workflow**:
1. **Morning**: Double-click `Run_Scanner.bat`
2. **Let it run** during market hours
3. **Evening**: Check `View_Signals.bat` for results

**That's it!** 📈

---

## 🆘 Still Need Help?

1. Check `View_Logs.bat` for errors
2. Review README.md for detailed docs
3. Verify config.py has correct credentials

**Happy Trading!** 🚀
