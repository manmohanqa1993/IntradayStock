# 📊 Intraday Scanner - Basic Version

**Simple, beginner-friendly F&O scanner using Yahoo Finance (FREE)**

---

## ✅ Features

- 🆓 **FREE** Yahoo Finance data
- 📊 **5-Point Strategy** (simplified for beginners)
- 📈 **Top 25 liquid F&O stocks**
- 🔔 **Sound alerts**
- 💾 **Auto-save signals** to CSV
- 🎯 **Entry/SL/Target** levels

---

## 🚀 Quick Start

### 1. Install

```bash
cd Intraday_Scanner
setup.bat
```

### 2. Run

```bash
run.bat
```

That's it!

---

## 📁 Folder Structure

```
Intraday_Scanner/
├── src/               # Source code
│   ├── scanner.py     # Main scanner
│   ├── data_handler.py # Yahoo Finance
│   ├── strategy.py    # 5-point strategy
│   └── alerts.py      # Alerts
├── config/            # Configuration
│   ├── settings.py    # Settings
│   └── stocks.txt     # Stock list
├── docs/              # Documentation
├── logs/              # Logs (auto-created)
├── output/            # Signals (auto-created)
├── run.bat            # ▶️ RUN THIS
├── setup.bat          # 📦 Setup
├── requirements.txt   # Dependencies
└── run.py             # Entry point
```

---

## ⚙️ Strategy (5 Points)

1. ✅ **Volume** > 20% above average
2. ✅ **Gap** < 0.5%
3. ✅ **3-Candle Pattern** (reversal)
4. ✅ **Momentum** (3/5 candles in direction)
5. ✅ **VWAP** confirmation

**Need 4/5 to generate signal**

---

## 📊 Sample Output

```
📈 BULLISH SIGNALS (2)

1. RELIANCE - Strength: 8/10
   💰 Entry: ₹1450
   🛑 SL: ₹1444
   🎯 Target: ₹1462
   📊 R:R = 1:2
```

---

## ⚙️ Customization

Edit `config/settings.py`:

```python
MIN_VOLUME_RATIO = 1.2        # Volume threshold
MAX_GAP_PERCENT = 0.5          # Max gap
SCAN_INTERVAL_SECONDS = 120    # Scan frequency
MIN_SIGNAL_STRENGTH = 6        # Signal quality
```

---

## 💡 For Beginners

**This is the BASIC version**:
- ✅ Easiest to understand
- ✅ Simplified 5-point strategy
- ✅ Top 25 liquid stocks only
- ✅ FREE data (15-20 min delay)

**When ready for more:**
- Upgrade to **Intraday_Scanner_Pro** (8-point strategy, 125+ stocks)
- Upgrade to **Intraday_Scanner_Realtime** (Multi-broker, real-time)
- Upgrade to **Intraday_Scanner_Kite** (Zerodha real-time)

---

## 📞 Support

- Check `logs/scanner.log` for errors
- Signals saved in `output/` folder
- Edit `config/stocks.txt` to change stock list

---

**Perfect for learning! 📚**
