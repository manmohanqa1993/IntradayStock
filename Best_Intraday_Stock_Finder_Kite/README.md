# 📊 Best Intraday Stock Finder - KITE EDITION

**Real-time F&O momentum continuation screener using Zerodha Kite Connect API**

---

## ⚡ Key Features

- 🔴 **Real-time data** from Zerodha Kite (0 seconds delay)
- 📊 **8-point strategy validation** for high-quality signals
- 🎯 **Auto Entry/SL/Target** calculation
- 📈 **F&O stocks only** (NSE 125+ stocks)
- 🔔 **Multi-channel alerts** (Console, Sound, Telegram)
- 💾 **Auto-save signals** to CSV/JSON
- 🧵 **Multi-threaded scanning** for speed
- ⚙️ **Fully customizable** strategy parameters

---

## 🚀 Quick Start

### 1. Install

```bash
Double-click → Install_Requirements.bat
```

### 2. Configure

Open `config.py` and add your Kite API credentials:

```python
KITE_CONFIG = {
    'api_key': 'your_kite_api_key',
    'api_secret': 'your_kite_secret',
    'access_token': ''
}
```

### 3. Login

```bash
Double-click → Kite_Login.bat
```

Follow the login process and save your access token.

### 4. Run

```bash
Double-click → Run_Scanner.bat
```

---

## 📋 Files Overview

| File | Purpose |
|------|---------|
| **Run_Scanner.bat** | 🚀 Start the scanner (MAIN) |
| **Kite_Login.bat** | 🔐 Login and get access token |
| **Test_Kite_Connection.bat** | 🧪 Test API connection |
| **Install_Requirements.bat** | 📦 Install packages |
| **View_Signals.bat** | 📊 See generated signals |
| **View_Logs.bat** | 📄 Check error logs |
| **config.py** | ⚙️ All settings (EDIT THIS) |
| **KITE_SETUP_GUIDE.md** | 📖 Complete setup guide |

---

## 📖 Documentation

**Read the complete guide:**
- [KITE_SETUP_GUIDE.md](KITE_SETUP_GUIDE.md) - Full setup instructions

**Key topics:**
- Getting Kite API credentials
- First-time login process
- Daily token refresh
- Strategy customization
- Telegram alerts setup
- Troubleshooting

---

## 💰 Cost

- **Kite API**: ₹2,000/month (Zerodha charges)
- **Scanner**: FREE (this software)

**Total**: ₹2,000/month for real-time data

---

## 🎯 Strategy Overview

### 8 Mandatory Conditions:

1. ✅ **Relative Volume** > 15-day average
2. ✅ **Gap** < 0.5% from previous close
3. ✅ **First Candle** move < 2%
4. ✅ **3-Candle Pattern** (Red→Green→Green or Green→Red→Red)
5. ✅ **Momentum** (3 out of 5 candles in direction)
6. ✅ **Pullback** (max 1 opposite candle)
7. ✅ **VWAP** confirmation (price above/below VWAP)
8. ✅ **Liquidity** (min 5L volume, ₹1Cr turnover)

**All 8 must pass for signal to appear!**

---

## 📊 Sample Output

```
🔍 SCAN #1 - 09:25:30 AM
═══════════════════════════════════════════════

📈 BULLISH SIGNALS (2)
═══════════════════════════════════════════════

1. RELIANCE - Strength: 9/10
   ─────────────────────────
   💰 Entry: ₹1453
   🛑 SL: ₹1447
   🎯 Target: ₹1465
   📊 R:R = 1:2

2. TCS - Strength: 8/10
   ─────────────────────────
   💰 Entry: ₹3825
   🛑 SL: ₹3815
   🎯 Target: ₹3845
   📊 R:R = 1:2
```

---

## ⚙️ Customization

### Change Scan Frequency

**config.py (Line 98):**
```python
SCAN_INTERVAL_SECONDS = 60  # Scan every 60 seconds
```

### Adjust Signal Quality

**config.py (Line 110):**
```python
MIN_SIGNAL_STRENGTH = 7  # Show only 7+ strength signals
```

### Change Risk-Reward

**config.py (Line 139):**
```python
RISK_REWARD_RATIO = 2.0  # 1:2 risk-reward
```

### Modify Stop-Loss Method

**config.py (Line 142):**
```python
SL_METHOD = 'vwap'  # Options: 'vwap', 'atr', 'percentage'
```

---

## 🔔 Telegram Alerts

**Enable in config.py:**

```python
ENABLE_TELEGRAM = True
TELEGRAM_BOT_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'
```

**Setup:**
1. Search @BotFather on Telegram
2. Create new bot
3. Copy bot token
4. Search @userinfobot for chat ID
5. Update config.py

---

## ❓ Troubleshooting

### ❌ "kiteconnect not installed"

```bash
pip install kiteconnect
```

### ❌ "Access token expired"

```bash
Double-click → Kite_Login.bat
```

Save the new token to config.py

### ❌ "No signals found"

**Normal behavior** - not every scan finds signals.

Market may be:
- Choppy (no clear trends)
- Low volatility
- No stocks meeting all 8 conditions

---

## 🆚 Kite vs FREE Version

| Feature | Kite | FREE |
|---------|------|------|
| Data Delay | 0 sec | 15-20 min |
| Cost | ₹2K/month | ₹0 |
| Best For | Live trading | Learning |
| Accuracy | Perfect | Good |

**Choose:**
- **Kite** if trading with real money
- **FREE** if learning/paper trading

---

## 📞 Support

1. Check `KITE_SETUP_GUIDE.md` for detailed help
2. Run `View_Logs.bat` to see error messages
3. Run `Test_Kite_Connection.bat` to verify API

---

## ⚠️ Important Notes

- **Daily re-login required** (access token expires)
- **This is a scanner, not auto-trader** (you place trades manually)
- **Use stop-losses** on all trades
- **Risk management is critical**
- **Trade only 9-10/10 strength signals**

---

## ✅ Pre-Flight Checklist

Before running:

- [ ] Kite API key obtained
- [ ] config.py updated with credentials
- [ ] Requirements installed
- [ ] First login completed
- [ ] Access token saved
- [ ] Connection tested
- [ ] Market hours (9:15 AM - 3:30 PM)

---

## 🎉 Ready to Scan!

```bash
Double-click → Run_Scanner.bat
```

**Happy Trading! 📈**

*Trade responsibly. This is a tool, not financial advice.*
