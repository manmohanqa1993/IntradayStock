# 🎯 Best Intraday Stock Finder

**Production-ready F&O momentum continuation screener for Indian stock market**

## 📋 Features

✅ **FREE Data Sources** - Hybrid NSE Official + Yahoo Finance (NO API KEYS!)  
✅ **Real-time F&O Stock Scanning** - Scans all NSE F&O stocks  
✅ **8-Point Strategy Validation** - Comprehensive momentum continuation strategy  
✅ **Multi-Broker Support** - FREE (Hybrid/Yahoo/NSE) + Zerodha/Angel/Upstox/Fyers  
✅ **Automated Signal Generation** - Entry/Stop-Loss/Target levels  
✅ **Multi-Channel Alerts** - Console, Sound, Telegram  
✅ **Modular Architecture** - Clean, maintainable code  
✅ **Risk Management** - Auto SL/Target calculation with R:R ratio  
✅ **Market Trend Filter** - Optional Nifty/BankNifty alignment  
✅ **Backtesting Ready** - Test strategies on historical data  
✅ **Performance Optimized** - Multi-threaded scanning  

---

## 🚀 Quick Start

### Option 1: FREE Version (Recommended for Beginners)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run scanner (Already configured for FREE!)
python Best_Intraday_Stock_Finder.py

# That's it! No configuration needed!
```

**Uses:** Hybrid NSE Official + Yahoo Finance - NO API keys required!

### Option 2: Broker API (For Real-time Trading)

Edit `config.py`:

```python
# Select your broker
BROKER = "zerodha"  # or "angel", "upstox", "fyers"

# Add API credentials
ZERODHA_CONFIG = {
    'api_key': 'your_api_key_here',
    'api_secret': 'your_api_secret_here',
    'access_token': ''  # Generated after login
}
```

Then run:

```bash
python Best_Intraday_Stock_Finder.py
```

---

## 📊 Strategy Overview

### Core Conditions

The screener implements a professional momentum continuation strategy with 8 validation points:

#### 1️⃣ **Relative Volume Filter**
- Current day volume > 15-day average volume
- Ensures active trading and institutional participation

#### 2️⃣ **Gap Filter**
- Gap < 0.5% from previous day close
- Avoids stocks with large gap-up/gap-down openings

#### 3️⃣ **First Candle Move Filter**
- First 5-min candle move < 2%
- Avoids excessive opening volatility

#### 4️⃣ **Three-Candle Reversal Pattern**
- **BULLISH**: Red → Green → Green
- **BEARISH**: Green → Red → Red
- High-priority confirmation signal

#### 5️⃣ **Momentum Continuation**
- Majority of next 4-5 candles in trend direction
- Maintains higher highs/lows (bullish) or lower highs/lows (bearish)

#### 6️⃣ **Pullback Validation**
- Maximum 1 opposite-color pullback candle allowed
- Pullback volume must be lower than previous candle

#### 7️⃣ **VWAP Confirmation**
- **Bullish**: Candles close above VWAP
- **Bearish**: Candles close below VWAP
- Acts as trend confirmation

#### 8️⃣ **Liquidity Filter**
- Minimum avg daily volume: 500,000 shares
- Minimum avg daily turnover: ₹1 crore
- Price range: ₹50 - ₹50,000

---

## 📁 Project Structure

```
Best_Intraday_Stock_Finder/
│
├── config.py                    # All configuration parameters
├── Best_Intraday_Stock_Finder.py  # Main screener application
├── strategy_validator.py        # Strategy logic & validation
├── data_handler.py              # Broker integration layer
├── alert_system.py              # Alert notifications
├── fno_stocks_list.txt          # F&O stocks list
├── requirements.txt             # Python dependencies
│
├── logs/                        # Log files
├── signals_output/              # Generated signals
└── data/                        # Cached data
```

---

## ⚙️ Configuration

All settings are in `config.py`:

### Strategy Parameters

```python
# Volume filter
VOLUME_LOOKBACK_DAYS = 15
MIN_VOLUME_RATIO = 1.0

# Gap filter
MAX_GAP_PERCENT = 0.5

# First candle filter
MAX_FIRST_CANDLE_MOVE = 2.0

# Momentum
MOMENTUM_OBSERVATION_CANDLES = 5
MIN_MOMENTUM_CANDLES = 3

# Pullback
MAX_PULLBACK_CANDLES = 1

# VWAP
VWAP_STRICT_MODE = True
```

### Scanning Settings

```python
# Market hours
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)

# Scanning window
SCAN_START_TIME = time(9, 20)
SCAN_END_TIME = time(15, 0)

# Scan interval
SCAN_INTERVAL_SECONDS = 60  # Every 60 seconds

# Signal strength threshold
MIN_SIGNAL_STRENGTH = 7  # Out of 10
```

### Risk Management

```python
# Auto SL/Target calculation
AUTO_CALCULATE_SL_TARGET = True

# Risk-reward ratio
RISK_REWARD_RATIO = 2.0  # 1:2

# Stop-loss method
SL_METHOD = 'vwap'  # Options: 'vwap', 'atr', 'percentage'
```

---

## 🔔 Alert Setup

### Telegram Alerts

1. Create a Telegram bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
3. Update `config.py`:

```python
ENABLE_TELEGRAM = True
TELEGRAM_BOT_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'
```

4. Test connection:

```bash
python alert_system.py
```

---

## 📈 Output Format

For each detected signal:

```
📈 BULLISH SIGNALS (3)
=====================================

1. RELIANCE - Strength: 9/10
   ─────────────────────────────────
   💰 Entry: ₹1450 | SL: ₹1440 | Target: ₹1470
   📊 Risk: ₹10 | Reward: ₹20 | R:R = 1:2
   📈 Volume Ratio: 2.5x | Gap: 0.2%
   🎯 VWAP: ₹1445 | Pattern: red-green-green
   ⏰ Time: 10:35:00
```

### Signal Strength (0-10 scale)

- **9-10**: Excellent - All conditions perfectly met
- **7-8**: Very Good - Strong setup
- **5-6**: Good - Acceptable setup
- **<5**: Filtered out (not displayed)

---

## 🔧 Broker Setup

### Zerodha Kite

1. Create app at https://developers.kite.trade/
2. Get API Key and Secret
3. Generate access token using `kite_login.py`

### Angel One

1. Generate API key from Angel One app
2. Use client ID and password
3. Enable TOTP if required

### Upstox

1. Create app at https://api.upstox.com/
2. Get API credentials
3. Generate access token

### Fyers

1. Create app at https://api-dashboard.fyers.in/
2. Get App ID and Secret
3. Generate access token

---

## ⚡ Performance Optimization

### Multi-threading

```python
USE_MULTITHREADING = True
MAX_WORKERS = 5  # Parallel scans
```

### Caching

```python
ENABLE_CACHE = True
CACHE_DURATION_SECONDS = 300  # 5 minutes
```

### Selective Scanning

Edit `fno_stocks_list.txt` to include only stocks you want to scan.

---

## 📊 Example Workflow

### Morning Setup (9:00 AM)

1. Start scanner at 9:15 AM when market opens
2. Scanner begins at 9:20 AM (after first candle)
3. Scans every 60 seconds

### During Market Hours

4. Receives real-time signals with alerts
5. Reviews entry/SL/target levels
6. Executes trades via broker platform

### End of Day

7. Reviews signal history
8. Analyzes performance
9. Adjusts parameters if needed

---

## 🛡️ Risk Disclaimer

⚠️ **IMPORTANT**:

- This tool provides signals, NOT trading advice
- Past performance does not guarantee future results
- Always use stop-losses
- Risk only capital you can afford to lose
- Consult a financial advisor before trading
- The creators are not responsible for any trading losses

**Trade at your own risk!**

---

## 🐛 Troubleshooting

### "Failed to connect to broker"

- Check API credentials in `config.py`
- Ensure access token is valid
- Verify broker API is active

### "No signals found"

- Market may be choppy (normal)
- Try lowering `MIN_SIGNAL_STRENGTH`
- Check if enough stocks meet liquidity filter

### "Module not found"

```bash
pip install -r requirements.txt
```

### "Market is closed"

- Scanner only works during market hours (9:15 AM - 3:30 PM IST)
- Use `Continue anyway? (y/n)` for testing

---

## 📞 Support

For issues, suggestions, or contributions:

1. Check documentation
2. Review config.py settings
3. Check logs/ folder for detailed errors

---

## 📜 License

This project is provided as-is for educational and personal use.

---

## 🙏 Acknowledgments

Built with:
- Python 3.8+
- pandas, numpy
- Broker APIs (Kite, Angel, Upstox, Fyers)

---

**Happy Trading! 📈**

*Remember: The best trade is the one you don't take when conditions aren't perfect.*
