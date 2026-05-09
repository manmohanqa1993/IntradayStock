# 📊 Intraday Scanner Kite - Zerodha Real-time

**Professional scanner with Zerodha Kite Connect API (Real-time data)**

---

## ⚡ Features

- 🔴 **Zerodha Kite API** (0-second delay)
- 📊 **8-Point Strategy**
- 📈 **125+ F&O stocks**
- 🎯 **Exact entry/exit prices**
- 💰 **Real-time order book**

---

## 💰 Cost

- Kite API: ₹2,000/month (Zerodha)
- Scanner: FREE (this software)

---

## 🚀 Quick Start

```bash
cd Intraday_Scanner_Kite

# 1. Setup
batch\setup.bat

# 2. Get API credentials
# Visit: https://developers.kite.trade/
# Get: API Key + API Secret

# 3. Configure
# Edit: config/settings.py
# Add your API key and secret

# 4. Login (DAILY)
batch\login.bat

# 5. Run
batch\run.bat
```

---

## 📁 Structure

```
Intraday_Scanner_Kite/
├── src/               # Code
│   ├── scanner.py     # Main scanner
│   ├── data_handler.py # Kite API
│   ├── strategy.py    # 8-point strategy
│   └── alerts.py      # Alerts
├── config/            # Configuration
│   ├── settings.py    # Kite settings
│   └── stocks.txt     # F&O stocks
├── batch/             # Batch files
│   ├── run.bat        # RUN THIS
│   ├── setup.bat      # Setup
│   └── login.bat      # Daily login
├── docs/              # Documentation
└── run.py             # Entry point
```

---

## ⚙️ Configuration

Edit `config/settings.py`:

```python
KITE_CONFIG = {
    'api_key': 'your_kite_api_key',
    'api_secret': 'your_kite_secret',
    'access_token': ''  # Generated daily
}
```

---

## 🔐 Daily Login

**Access token expires daily at 3:30 PM**

Each trading day:
```bash
batch\login.bat
```

Follow prompts, save token to config/settings.py

---

## 💡 Who Should Use This?

**Use Scanner Kite if:**
- ✅ Trading with real money
- ✅ Need 0-second delay
- ✅ Want exact prices
- ✅ Have Zerodha account
- ✅ Budget allows ₹2K/month

**Use FREE scanner if:**
- 📚 Still learning
- 📝 Paper trading
- 💰 Budget tight

---

## 📞 Support

- Config: `config/settings.py`
- Logs: `logs/kite_scanner.log`
- Signals: `output/` folder

---

**Real-time Zerodha data! ⚡**
