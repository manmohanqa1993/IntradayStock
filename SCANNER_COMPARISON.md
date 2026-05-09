# 📊 Scanner Comparison Guide - Which One Should You Use?

## 🎯 Quick Recommendation

| Your Situation | Best Scanner | File to Run |
|----------------|--------------|-------------|
| **Have Zerodha account** | 🥇 Kite Scanner | `run_kite_scanner.bat` |
| **No broker account yet** | 🥈 Yahoo Finance Pro | `run_pro_scanner.bat` |
| **Just starting out** | 🥈 Yahoo Finance Basic | `run_scanner.bat` |

---

## 📋 Complete Comparison

### 1. 🟢 Kite Scanner (Zerodha) - **BEST FOR ACTIVE TRADERS**

**File**: `intraday_scanner_kite.py`  
**Run**: `run_kite_scanner.bat`

| Feature | Details |
|---------|---------|
| **Data Source** | Zerodha Kite Connect API |
| **Data Delay** | ⚡ **ZERO delay** (real-time) |
| **Bid/Ask Prices** | ✅ Yes (Live) |
| **Cost** | 💰 **FREE** (for Zerodha customers) |
| **Setup Difficulty** | 🔧 Moderate (API setup, daily token) |
| **Accuracy** | ⭐⭐⭐⭐⭐ Exchange-grade data |
| **Best For** | **Day trading, scalping, quick entries** |

**Pros:**
- ✅ Real-time tick-by-tick data
- ✅ Live bid/ask spreads
- ✅ Zero delay
- ✅ Can place orders directly (optional)
- ✅ Most accurate for intraday

**Cons:**
- ❌ Requires Zerodha trading account
- ❌ Access token expires daily (must regenerate)
- ❌ Setup takes 10-15 minutes initially
- ❌ Need to run login script daily

**When to Use:**
- You have an active Zerodha account
- Need real-time data for quick decisions
- Trading actively during market hours
- Want to place orders via API

---

### 2. 🟠 Professional Scanner (Yahoo Finance) - **NO SETUP REQUIRED**

**File**: `intraday_scanner_pro.py`  
**Run**: `run_pro_scanner.bat`

| Feature | Details |
|---------|---------|
| **Data Source** | Yahoo Finance |
| **Data Delay** | 🕐 **15 minutes** |
| **Bid/Ask Prices** | ❌ No |
| **Cost** | 💰 **FREE** (for everyone) |
| **Setup Difficulty** | ✅ **ZERO** (just run!) |
| **Accuracy** | ⭐⭐⭐⭐ Good for swing/positional |
| **Best For** | **Swing trading, learning, no account needed** |

**Pros:**
- ✅ No broker account needed
- ✅ Zero setup - works instantly
- ✅ Free for everyone
- ✅ No daily token generation
- ✅ Reliable and stable

**Cons:**
- ❌ 15-minute data delay
- ❌ No bid/ask prices
- ❌ Not ideal for scalping

**When to Use:**
- Just starting out (no broker account yet)
- Swing trading (delay doesn't matter)
- Learning the strategy
- Want zero-hassle setup

---

### 3. 🟦 Basic Scanner (Yahoo Finance) - **SIMPLE VERSION**

**File**: `intraday_scanner.py`  
**Run**: `run_scanner.bat`

| Feature | Details |
|---------|---------|
| **Data Source** | Yahoo Finance |
| **Data Delay** | 🕐 **15 minutes** |
| **Results** | Shows top 10 stocks (vs 3-5 in Pro) |
| **Filters** | Fewer filters, easier criteria |
| **Setup Difficulty** | ✅ **ZERO** |
| **Best For** | **Beginners, more opportunities** |

**Pros:**
- ✅ Easy to understand
- ✅ More stocks shown (10 vs 5)
- ✅ Less strict filters
- ✅ Good for learning

**Cons:**
- ❌ 15-minute delay
- ❌ Less selective than Pro
- ❌ May show lower quality setups

**When to Use:**
- First time using scanners
- Want to see more opportunities
- Learning technical analysis

---

## 🔄 Live Monitor

**File**: `live_monitor.py`  
**Run**: `run_live_monitor.bat`

**What it does**: Runs the basic scanner **continuously every 15 minutes** during market hours.

**Use case**: Set it and forget it - automatically scans all day.

---

## 📊 Feature Comparison Table

| Feature | Kite | Pro (Yahoo) | Basic (Yahoo) |
|---------|------|-------------|---------------|
| **Real-time Data** | ✅ | ❌ (15 min) | ❌ (15 min) |
| **Bid/Ask** | ✅ | ❌ | ❌ |
| **Setup Required** | Yes | No | No |
| **Broker Account** | Zerodha | None | None |
| **Results Count** | 3-5 | 3-5 | 10 |
| **Filter Strictness** | Highest | Highest | Moderate |
| **Best For** | Day trading | Swing trading | Learning |
| **Cost** | Free* | Free | Free |

*Free for account holders

---

## 🎯 Decision Tree

```
Do you have a broker account?
├─ Yes → Which broker?
│  └─ Zerodha → Use Kite Scanner 🥇
│
└─ No → What's your goal?
   ├─ Day trading → Get Zerodha account → Use Kite 🥇
   ├─ Swing trading → Use Pro Scanner (Yahoo) 🥈
   └─ Just learning → Use Basic Scanner 🟦
```

---

## 💡 Recommendations by Trading Style

### Scalping (1-5 minute holds)
**MUST USE**: Kite (real-time data essential)

### Day Trading (5-60 minute holds)
**Recommended**: Kite  
**Alternative**: Pro Scanner (with price verification)

### Swing Trading (1-5 day holds)
**Perfect**: Pro Scanner (15-min delay doesn't matter)

### Positional Trading (weeks/months)
**Perfect**: Pro Scanner or Basic Scanner

---

## 🚀 Getting Started

### If you have Zerodha:
1. Read: `KITE_SETUP_GUIDE.md`
2. Install: `pip install kiteconnect`
3. Setup: Run `python kite_login.py` (once)
4. Run: Double-click `run_kite_scanner.bat`

### If you don't have any account:
1. Install: `pip install -r requirements.txt`
2. Run: Double-click `run_pro_scanner.bat`
3. Start learning and testing!

---

## 📁 Output Files Location

All scanners save to organized folders:

```
stock/
├── kite_scanner_output/
│   └── 2026-05-04/
│       └── scan_0945.csv
│
├── pro_scanner_output/
│   └── 2026-05-04/
│       └── scan_0945.csv
│
└── basic_scanner_output/
    └── 2026-05-04/
        └── scan_0945.csv
```

---

## ⚡ Quick Commands

```bash
# Install packages
pip install -r requirements.txt

# For Kite only
pip install kiteconnect

# Run scanners
python intraday_scanner_kite.py     # Kite (real-time)
python intraday_scanner_pro.py      # Pro (delayed)
python intraday_scanner.py          # Basic (delayed)
```

---

## 🎓 My Recommendation

**For Serious Traders:**
Get a Zerodha account → Use Kite Scanner → Real-time advantage

**For Beginners:**
Start with Pro Scanner → Learn the strategy → Open broker account later

**For Swing Traders:**
Use Pro Scanner → 15-min delay doesn't affect swing trades

---

**Happy Trading!** 📈💰

Choose the scanner that fits your needs and trading style!
