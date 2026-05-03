# NSE Intraday Stock Scanner

Professional-grade intraday trading scanner for NSE stocks with strict technical criteria.

## Features

✅ **Free & Open Source** - Uses Yahoo Finance (no API keys needed)  
✅ **Live Market Data** - 5-minute candle data during market hours  
✅ **70+ F&O Stocks** - Focuses on highly liquid stocks  
✅ **10+ Technical Filters** - VWAP, EMA, RSI, MACD, Volume, Gap, Breakout  
✅ **Quality Score** - Ranks stocks by criteria confluence  
✅ **Live Monitoring** - Continuous scanning during market hours  
✅ **CSV Export** - Save results for further analysis  

---

## Installation

### Step 1: Install Python
Make sure you have Python 3.8+ installed.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Option 1: Single Scan (Recommended for beginners)

Run once to get current opportunities:

```bash
python intraday_scanner.py
```

**Output:**
- Lists 5-10 high-quality stocks meeting most criteria
- Shows direction (Bullish/Bearish), price, volume, VWAP, RSI, setup
- Saves results to CSV file with timestamp

**Best Time to Run:**
- 9:30 AM - After market opens (catch gap & opening range breakouts)
- 11:00 AM - Mid-morning momentum
- 1:00 PM - Post-lunch session
- 2:30 PM - Final hour opportunities

---

### Option 2: Live Monitoring (Advanced)

Automatically scans every 15 minutes during market hours:

```bash
python live_monitor.py
```

**Features:**
- Runs continuously during NSE hours (9:15 AM - 3:30 PM)
- Scans every 15 minutes
- Auto-pauses when market is closed
- Press `Ctrl+C` to stop

---

## How It Works

### Data Source
- **Yahoo Finance (yfinance)** - Free, reliable, 5-minute candle data
- **Near real-time** - 15-min delay (acceptable for intraday scanning)
- **No API limits** - Unlike paid services

### Technical Criteria Applied

| Criteria | Threshold |
|----------|-----------|
| Volume | > 1.5x average |
| Gap | ≥ 1.5% from previous close |
| VWAP | Price must hold above/below VWAP |
| EMA Trend | 20 EMA > 50 EMA (bullish) or vice versa |
| RSI | 55-75 (bullish), 25-45 (bearish) |
| MACD | Fresh crossover |
| ATR | > 1% of price (volatility expansion) |
| Breakout | Above previous day high or OR high |

**Minimum Score:** 5/8 criteria must be met

---

## Output Explanation

```
1. RELIANCE - BULLISH
   Price: ₹2,456.75 | Change: +2.34% | Volume: 2.1x avg
   VWAP: ₹2,445.20 (Above) | RSI: 68.5 | ATR: 1.8%
   Setup: Gap Up | Above VWAP | Breakout
   Sector: Energy | Quality Score: 7/8
   EMA20: ₹2,440.30 | EMA50: ₹2,410.50
```

**Key Fields:**
- **Direction**: Trade direction (Bullish = Buy, Bearish = Sell)
- **Change%**: Gap from previous close
- **Volume Ratio**: Current volume vs 20-day average
- **VWAP Position**: Critical - price should hold its side
- **RSI**: Momentum strength (not overbought/oversold)
- **Setup**: Key reasons for selection
- **Quality Score**: Higher = more criteria met (≥6 is excellent)

---

## Trading Guidelines

### ⚠️ Risk Management (CRITICAL)

1. **Stop Loss**: Always use 1-2% below entry (bullish) or above (bearish)
2. **Position Size**: Never risk more than 1-2% of capital per trade
3. **Target**: 1:2 or 1:3 risk-reward ratio
4. **Time Limit**: Exit all positions by 3:15 PM (avoid closing volatility)

### 🎯 Best Practices

1. **Focus on Score ≥ 6** - These have highest probability
2. **Confirm VWAP hold** - Most critical filter
3. **Check Nifty trend** - Trade with the market, not against it
4. **Avoid first 15 mins** - Let opening range form
5. **Use limit orders** - Avoid slippage in fast-moving stocks

### 🚫 Avoid

- Stocks with major news/events (earnings, court rulings)
- Stocks constantly crossing VWAP (choppy)
- Low volume stocks (even if they appear in results)
- Trading without stop-loss

---

## Limitations

### Data Delay
- Yahoo Finance has ~15 min delay on free tier
- Good enough for swing/positional intraday (not scalping)
- For tick-by-tick data, use paid APIs (Zerodha Kite, Upstox)

### Coverage
- Currently scans 70 F&O stocks (most liquid)
- Can add more stocks by editing `NSE_FNO_STOCKS` list in `intraday_scanner.py`

### Accuracy
- Technical indicators are probabilistic, not guaranteed
- Always backtest and paper trade first
- No system is 100% accurate

---

## Customization

### Add More Stocks
Edit `intraday_scanner.py` and add symbols to `NSE_FNO_STOCKS` list:

```python
NSE_FNO_STOCKS = [
    'RELIANCE.NS',
    'TCS.NS',
    'YOURSTOCK.NS',  # Add your stock here
]
```

### Change Scan Interval
Edit `live_monitor.py`:

```python
live_monitor(interval_minutes=10)  # Scan every 10 minutes instead of 15
```

### Adjust Criteria
Edit `analyze_stock()` function in `intraday_scanner.py` to change thresholds.

---

## Troubleshooting

### "No module named 'yfinance'"
```bash
pip install yfinance pandas numpy
```

### "No stocks meeting criteria found"
- Market may be range-bound (no strong trends)
- Try scanning at different times (9:30 AM, 11 AM, 1 PM)
- Criteria might be too strict - check if any stocks had Score 4+

### Data fetch errors
- Check internet connection
- Yahoo Finance may be temporarily down
- Some stocks may have delisted/changed symbols

---

## Disclaimer

**⚠️ THIS IS NOT FINANCIAL ADVICE**

This tool is for educational and informational purposes only. Trading involves substantial risk of loss. Past performance does not guarantee future results. Always:

- Do your own research
- Use proper risk management
- Paper trade before going live
- Consult a financial advisor

The developers are not responsible for any trading losses.

---

## Support

For issues, questions, or suggestions, create an issue or modify the code as needed.

**Happy Trading! 📈**
