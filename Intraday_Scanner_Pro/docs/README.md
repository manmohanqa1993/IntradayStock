# 📊 Intraday Scanner Pro - Professional Version

**Advanced F&O scanner with Hybrid NSE + Yahoo Finance (BEST FREE setup!)**

---

## ⚡ Features

- 🆓 **Hybrid NSE + Yahoo** (NSE official data + Yahoo 5-min candles)
- 📊 **8-Point Strategy** (professional validation)
- 📈 **125+ F&O stocks** (all NSE F&O)
- 🔔 **Multi-channel alerts** (Console, Sound, Telegram)
- 💾 **CSV/JSON export**
- 🧵 **Multi-threaded** scanning
- 🎯 **Advanced risk management**

---

## 🚀 Quick Start

```bash
cd Intraday_Scanner_Pro
batch\setup.bat
batch\run.bat
```

---

## 📁 Clean Folder Structure

```
Intraday_Scanner_Pro/
├── src/                    # Source code
│   ├── scanner.py          # Main scanner
│   ├── data_handler.py     # Hybrid NSE+Yahoo
│   ├── strategy.py         # 8-point strategy
│   └── alerts.py           # Multi-channel alerts
├── config/                 # Configuration
│   ├── settings.py         # All settings
│   └── stocks.txt          # 125+ F&O stocks
├── batch/                  # Batch files
│   ├── run.bat             # RUN THIS
│   └── setup.bat           # Setup
├── docs/                   # Documentation
├── logs/                   # Logs (auto-created)
├── output/                 # Signals (auto-created)
├── requirements.txt        # Dependencies
└── run.py                  # Entry point
```

---

## 🎯 8-Point Strategy

1. ✅ **Relative Volume** > 15-day average
2. ✅ **Gap** < 0.5%
3. ✅ **First Candle** move < 2%
4. ✅ **3-Candle Reversal** pattern
5. ✅ **Momentum** continuation (3/5 candles)
6. ✅ **Pullback** validation (max 1)
7. ✅ **VWAP** confirmation
8. ✅ **Liquidity** filter

**ALL 8 must pass for signal!**

---

## 📊 Data Sources

| Data Type | Primary | Fallback |
|-----------|---------|----------|
| 5-min candles | Yahoo Finance | - |
| Daily OHLC | NSE Official | Yahoo |
| Live quotes | NSE Official | Yahoo |
| Volume | NSE Official | Yahoo |

**Best of both worlds - Official NSE + Yahoo intraday!**

---

## ⚙️ Customization

Edit `config/settings.py`:

```python
BROKER = "free"  # Hybrid NSE+Yahoo
SCAN_INTERVAL_SECONDS = 60
MIN_SIGNAL_STRENGTH = 7
ENABLE_TELEGRAM = False  # Set True + add credentials
```

---

## 💡 Who Should Use This?

**Use Scanner Pro if:**
- ✅ Want best FREE data (NSE official)
- ✅ Ready for advanced 8-point strategy
- ✅ Scanning all 125+ F&O stocks
- ✅ Serious about learning pro trading
- ✅ Want Telegram alerts
- ✅ Need CSV/JSON export

**Use Basic Scanner if:**
- 📚 Complete beginner
- 📝 Want simpler 5-point strategy
- 🎯 Top 25 stocks enough

**Upgrade to Realtime/Kite if:**
- 💰 Trading with real money
- ⚡ Need 0-second delay
- 🎯 Want exact entry prices

---

## 📞 Support

- Logs: `logs/scanner.log`
- Signals: `output/` folder
- Config: `config/settings.py`

---

**Best FREE scanner setup! 🚀**
