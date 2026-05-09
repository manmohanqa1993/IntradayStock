# 📊 Intraday Scanner Suite - Complete Guide

## 🎯 4 Scanners to Choose From

Located in: `C:\Users\Manmohan.Pradhan\Desktop\stock\`

---

## 📂 Available Scanners

### 1. **Intraday_Scanner** (Basic - Beginner)
```
📁 Intraday_Scanner/
   Data: Yahoo Finance (FREE)
   Strategy: 5-Point (Simplified)
   Stocks: Top 25 liquid F&O
   Delay: 15-20 minutes
   Setup: 2 minutes
   Cost: ₹0
```

### 2. **Intraday_Scanner_Pro** (Professional)
```
📁 Intraday_Scanner_Pro/
   Data: Hybrid NSE + Yahoo (FREE)
   Strategy: 8-Point (Professional)
   Stocks: 125+ F&O stocks
   Delay: 15-20 minutes
   Setup: 5 minutes
   Cost: ₹0
```

### 3. **Intraday_Scanner_Realtime** (Multi-Broker)
```
📁 Intraday_Scanner_Realtime/
   Data: Multi-broker (FREE/Zerodha/Angel/Upstox/Fyers)
   Strategy: 8-Point
   Stocks: 125+ F&O stocks
   Delay: 0 sec (real-time) or 15-20 min (FREE)
   Setup: 15 minutes (with broker)
   Cost: ₹0 (FREE) or ₹2K/month (broker)
```

### 4. **Intraday_Scanner_Kite** (Zerodha Only)
```
📁 Intraday_Scanner_Kite/
   Data: Zerodha Kite Connect API
   Strategy: 8-Point
   Stocks: 125+ F&O stocks
   Delay: 0 seconds (real-time)
   Setup: 15 minutes
   Cost: ₹2,000/month
```

---

## 🎯 Quick Decision Matrix

### Choose **Intraday_Scanner** (Basic) if:
- ✅ Complete beginner
- ✅ Learning trading basics
- ✅ Want simplest setup
- ✅ Top 25 stocks enough
- ✅ Don't need complexity

### Choose **Intraday_Scanner_Pro** if:
- ✅ Understand basics
- ✅ Want professional 8-point strategy
- ✅ Need all 125+ F&O stocks
- ✅ Want best FREE data (NSE official)
- ✅ Serious about learning
- ✅ Paper trading

### Choose **Intraday_Scanner_Realtime** if:
- ✅ Want flexibility
- ✅ May use different brokers
- ✅ Can start FREE, upgrade later
- ✅ Want multi-broker support
- ✅ Experimenting with brokers

### Choose **Intraday_Scanner_Kite** if:
- ✅ Trading with real money
- ✅ Have Zerodha account
- ✅ Need real-time data (0 sec delay)
- ✅ Want exact prices
- ✅ Budget allows ₹2K/month
- ✅ Serious trader

---

## 📊 Feature Comparison

| Feature | Basic | Pro | Realtime | Kite |
|---------|-------|-----|----------|------|
| **Data Source** | Yahoo | NSE+Yahoo | Multi | Kite |
| **Strategy** | 5-Point | 8-Point | 8-Point | 8-Point |
| **Stocks** | 25 | 125+ | 125+ | 125+ |
| **Delay** | 15-20min | 15-20min | 0s/15min | 0s |
| **Cost** | ₹0 | ₹0 | ₹0-2K | ₹2K |
| **Setup** | Easy | Easy | Moderate | Moderate |
| **Best For** | Learning | Advanced learning | Flexibility | Live trading |

---

## 📁 Clean Folder Structure (All Scanners)

```
Scanner_Name/
├── src/                    # Source code
│   ├── scanner.py          # Main scanner logic
│   ├── data_handler.py     # Data fetching
│   ├── strategy.py         # Strategy validation
│   └── alerts.py           # Alert system
├── config/                 # Configuration
│   ├── settings.py         # All settings
│   └── stocks.txt          # Stock list
├── docs/                   # Documentation
│   └── README.md           # Scanner-specific guide
├── logs/                   # Log files (auto-created)
├── output/                 # Signal outputs (auto-created)
├── run.bat                 # ▶️ RUN THIS to start
├── setup.bat               # 📦 Setup/install
├── login.bat               # 🔐 (Kite only - daily login)
├── requirements.txt        # Python dependencies
└── run.py                  # Main entry point
```

---

## 🚀 Getting Started

### For Any Scanner:

```bash
# 1. Navigate to scanner folder
cd Scanner_Name

# 2. Install requirements
setup.bat

# 3. (Optional) Configure
# Edit config/settings.py if needed

# 4. Run
run.bat
```

### Scanner-Specific Steps:

**Basic / Pro:**
- No configuration needed
- Just install and run

**Realtime:**
- Edit `config/settings.py`
- Choose broker: "free", "zerodha", "angel", etc.
- Add API credentials if using broker

**Kite:**
- Get API key from https://developers.kite.trade/
- Edit `config/settings.py` - add credentials
- Run `login.bat` daily
- Then `run.bat`

---

## 💡 Recommended Path

### Week 1-2: Start with Basic
```
Folder: Intraday_Scanner/
Goal: Learn the basics
- Simple 5-point strategy
- Top 25 stocks
- Get comfortable with alerts
```

### Week 3-4: Upgrade to Pro
```
Folder: Intraday_Scanner_Pro/
Goal: Master advanced strategy
- 8-point professional strategy
- All 125+ F&O stocks
- NSE official data
- Paper trade seriously
```

### Week 5-8: Test Realtime (FREE mode)
```
Folder: Intraday_Scanner_Realtime/
BROKER = "free"
Goal: Prepare for real trading
- Same data as Pro
- Get used to Realtime interface
- Track performance seriously
```

### Week 9+: Go Live with Kite
```
Folder: Intraday_Scanner_Kite/
OR: Intraday_Scanner_Realtime/ (BROKER = "zerodha")
Goal: Live trading
- Real-time data
- Exact prices
- Start with small positions
```

---

## 📖 Documentation

Each scanner has its own README:
- `Intraday_Scanner/docs/README.md`
- `Intraday_Scanner_Pro/docs/README.md`
- `Intraday_Scanner_Realtime/docs/README.md`
- `Intraday_Scanner_Kite/docs/README.md`

---

## 🔄 Can You Use Multiple?

**YES!** All scanners are independent:

### Scenario 1: Learning + Live
- **Morning**: Run Pro (FREE) to find candidates
- **Trading**: Run Kite for live real-time trades

### Scenario 2: Comparison
- Run Basic to learn
- Run Pro to master
- Compare signal quality

### Scenario 3: Backup
- Primary: Kite (real-time)
- Backup: Pro (if Kite API down)

---

## ⚙️ Customization

All scanners share similar `config/settings.py`:

```python
# Scan frequency
SCAN_INTERVAL_SECONDS = 60  # seconds

# Signal quality
MIN_SIGNAL_STRENGTH = 7  # 0-10 scale

# Risk management
RISK_REWARD_RATIO = 2.0  # 1:2 R:R
SL_METHOD = 'vwap'  # 'vwap', 'atr', 'percentage'

# Alerts
ENABLE_CONSOLE_ALERTS = True
ENABLE_SOUND_ALERTS = True
ENABLE_TELEGRAM = False  # Set True + add credentials
```

---

## 💰 Cost Summary

| Scanner | Monthly Cost | Annual Cost |
|---------|--------------|-------------|
| Basic | ₹0 | ₹0 |
| Pro | ₹0 | ₹0 |
| Realtime (FREE) | ₹0 | ₹0 |
| Realtime (Zerodha) | ₹2,000 | ₹24,000 |
| Kite | ₹2,000 | ₹24,000 |

**ROI Calculation (Kite/Realtime):**
- Just 2 good trades/month covers ₹2K cost
- If profitable, easily pays for itself!

---

## 📞 Support

### Each Scanner:
- Logs: `logs/` folder
- Signals: `output/` folder
- Config: `config/settings.py`
- Stocks: `config/stocks.txt`

### General Issues:
1. Check scanner's `docs/README.md`
2. Check `logs/scanner.log` for errors
3. Verify Python installed: `python --version`
4. Reinstall: `setup.bat`

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| **Install** | `setup.bat` |
| **Run** | `run.bat` |
| **Login (Kite)** | `login.bat` |
| **View Logs** | Open `logs/scanner.log` |
| **View Signals** | Open `output/` folder |
| **Edit Settings** | Edit `config/settings.py` |
| **Change Stocks** | Edit `config/stocks.txt` |

---

## 🎯 Final Recommendation

```
┌─────────────────────────────────────────┐
│  NEW TO TRADING?                        │
│  → Start: Intraday_Scanner (Basic)      │
│  → Then: Intraday_Scanner_Pro           │
│                                         │
│  LEARNING SERIOUSLY?                    │
│  → Use: Intraday_Scanner_Pro            │
│                                         │
│  READY TO TRADE?                        │
│  → Use: Intraday_Scanner_Kite           │
│  → Or: Intraday_Scanner_Realtime        │
│                                         │
│  WANT FLEXIBILITY?                      │
│  → Use: Intraday_Scanner_Realtime       │
└─────────────────────────────────────────┘
```

---

## 🎉 You're Ready!

**All 4 scanners are installed and ready to use!**

Pick one, navigate to its folder, and run:
```bash
run.bat
```

**Happy Trading! 📈**

*Trade responsibly. Use stop-losses. Start small. Build gradually.*
