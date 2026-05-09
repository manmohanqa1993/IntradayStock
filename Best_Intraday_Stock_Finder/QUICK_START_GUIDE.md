# 🚀 Quick Start Guide - Best Intraday Stock Finder

## 🆓 NEW: HYBRID NSE + Yahoo Finance (BEST FREE!)

**No broker API needed!** The scanner now works with **HYBRID NSE+Yahoo (FREE)**

- ✅ No API keys required
- ✅ No broker account needed
- ✅ Works immediately
- ✅ NSE Official daily data (most accurate)
- ✅ Yahoo Finance 5-min candles
- ⚠️ 15-20 minute data delay (good for learning/paper trading)

**Want real-time?** See Step 2 for broker setup (optional)

---

## ⏱️ 2-Minute Setup (FREE Version)

### Step 1: Install Python Packages (1 minute)

```bash
cd Best_Intraday_Stock_Finder
pip install -r requirements.txt
```

**Install only for your broker:**

```bash
# For Zerodha
pip install kiteconnect

# For Angel One
pip install smartapi-python

# For Upstox
pip install upstox-python-sdk

# For Fyers
pip install fyers-apiv3
```

---

### Step 2: Run Scanner (1 minute) - Already Configured!

**No configuration needed!** Scanner is pre-set to use FREE Hybrid NSE+Yahoo.

```bash
python Best_Intraday_Stock_Finder.py
```

**That's it!** 🎉 No API keys, no broker setup needed!

---

## ⚡ (OPTIONAL) Upgrade to Real-Time Data

**Only if you want 0-second delay for live trading:**

### Configure Broker API:

Open `config.py` and change:

```python
# Line 17: Switch from FREE to your broker
BROKER = "zerodha"  # Or "angel", "upstox", "fyers"

# Then add API credentials below
ZERODHA_CONFIG = {
    'api_key': 'your_api_key',
    'api_secret': 'your_secret'
}
```

**For learning/paper trading?** Stick with FREE version!

---

## 📊 What Happens Next?

1. Scanner connects to your broker
2. Starts scanning at 9:20 AM (after first candle)
3. Scans every 60 seconds
4. Shows signals in real-time:

```
📈 BULLISH SIGNALS (2)
═══════════════════════════

1. RELIANCE - Strength: 9/10
   ─────────────────────────
   💰 Entry: ₹1450
   🛑 SL: ₹1440
   🎯 Target: ₹1470
   📊 R:R = 1:2
```

---

## 🔔 Optional: Enable Telegram Alerts

### 1. Create Telegram Bot

1. Open Telegram, search [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow instructions
4. Copy your **Bot Token**

### 2. Get Your Chat ID

1. Search [@userinfobot](https://t.me/userinfobot)
2. Start conversation
3. Copy your **Chat ID**

### 3. Update Config

In `config.py`:

```python
# Line 121
ENABLE_TELEGRAM = True

# Line 122
TELEGRAM_BOT_TOKEN = 'paste_your_bot_token'

# Line 123
TELEGRAM_CHAT_ID = 'paste_your_chat_id'
```

### 4. Test

```bash
python alert_system.py
```

Should see: "✅ Telegram connection successful!"

---

## ⚙️ Customize Settings (Optional)

### Change Scan Frequency

```python
# config.py, Line 65
SCAN_INTERVAL_SECONDS = 60  # Change to 30 for faster scans
```

### Change Signal Sensitivity

```python
# config.py, Line 75
MIN_SIGNAL_STRENGTH = 7  # Lower to 5 for more signals
```

### Change Stop-Loss Method

```python
# config.py, Line 133
SL_METHOD = 'vwap'  # Options: 'vwap', 'atr', 'percentage'
```

---

## 🎯 Daily Trading Workflow

### Morning (9:00 AM)

```bash
# Start scanner at 9:00 AM
python Best_Intraday_Stock_Finder.py
```

Scanner will:
- Wait until 9:15 AM (market open)
- Start scanning at 9:20 AM (after first candle)

### During Market Hours

- Monitor alerts (Console/Telegram/Sound)
- Review signals and enter trades
- Use provided Entry/SL/Target levels

### End of Day

- Check `signals_output/` folder for saved signals
- Review performance
- Check logs for any errors

---

## 📝 Quick Reference

### File Purposes

| File | What It Does |
|------|-------------|
| `config.py` | **Edit this** - All settings |
| `Best_Intraday_Stock_Finder.py` | **Run this** - Main program |
| `fno_stocks_list.txt` | List of stocks to scan (editable) |
| `signals_output/` | Generated signals saved here |
| `logs/` | Error logs and debug info |

### Important Config Settings

| Setting | Location | Purpose |
|---------|----------|---------|
| `BROKER` | Line 12 | Which broker to use |
| API credentials | Lines 15-36 | Broker login |
| `SCAN_INTERVAL_SECONDS` | Line 65 | How often to scan |
| `MIN_SIGNAL_STRENGTH` | Line 75 | Signal quality filter |
| `ENABLE_TELEGRAM` | Line 121 | Turn on Telegram alerts |

---

## 🆘 Common Issues

### ❌ "Failed to connect to broker"

**Fix**: Check API credentials in `config.py`

### ❌ "ModuleNotFoundError: No module named 'kiteconnect'"

**Fix**: 
```bash
pip install kiteconnect
```

### ❌ "Market is currently closed"

**Normal**: Scanner works 9:15 AM - 3:30 PM IST only

You can test anytime by typing `y` when prompted.

### ⚠️ "No signals found"

**Normal**: Not every scan finds signals. Market may be:
- Choppy (no clear trends)
- Outside our strategy conditions
- Low volatility day

Try again in next scan.

---

## 💡 Pro Tips

### 1. Start Small
- Test with paper trading first
- Use small position sizes initially
- Get comfortable with signals

### 2. Follow the Rules
- **Always use stop-loss**
- Don't trade ALL signals
- Pick highest strength signals (9-10)

### 3. Optimize Scanning
- Edit `fno_stocks_list.txt` to scan only stocks you trade
- Fewer stocks = faster scans

### 4. Monitor Performance
- Check `signals_output/` daily
- Track which signals worked
- Adjust settings based on results

---

## 📞 Need Help?

1. **Check README.md** - Detailed documentation
2. **Check logs/** - See what went wrong
3. **Review config.py** - Verify all settings

---

## ✅ Pre-Flight Checklist

Before running:

- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Broker selected in config.py
- [ ] API credentials added in config.py
- [ ] (Optional) Telegram configured
- [ ] Market hours (9:15 AM - 3:30 PM IST)

---

## 🎉 Ready to Trade!

You're all set! Run the scanner and start finding high-probability intraday setups.

**Remember**:
- This is a tool, not a guarantee
- Always use stop-losses
- Risk management is key
- Trade responsibly

**Good luck! 📈**
