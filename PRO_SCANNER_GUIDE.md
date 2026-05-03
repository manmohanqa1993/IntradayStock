# 🎯 Professional Intraday Scanner - Complete Guide

## ✅ All Requirements Implemented

Based on your professional trader requirements, this scanner now includes **EVERYTHING**:

### ✅ Filters Implemented:

1. **Liquidity Filter**
   - ✅ Price > ₹100
   - ✅ Average volume > 500,000 shares
   - ✅ Current volume must be 2× the average (changed from 1.5×)

2. **Momentum Filter**
   - ✅ Stock moving ±1.5% intraday
   - ✅ Prefer stocks near day high (for BUY) or day low (for SELL)

3. **VWAP Trend Confirmation**
   - ✅ BUY only if price above VWAP
   - ✅ SELL only if price below VWAP

4. **Moving Average Trend**
   - ✅ Bullish: 20 EMA > 50 EMA
   - ✅ Bearish: 20 EMA < 50 EMA

5. **Volatility Filter**
   - ✅ ATR > 1% OR intraday range > 1.5%

6. **Breakout Conditions** (at least one required)
   - ✅ Break of day high/low
   - ✅ Break of 15-min opening range
   - ✅ Break of previous day high/low

7. **Preferred Stocks**
   - ✅ Focus only on Nifty 50 and Bank Nifty (50 most liquid stocks)

8. **Indicator Confirmation**
   - ✅ RSI 50-70 for bullish
   - ✅ RSI 30-50 for bearish
   - ✅ MACD crossover confirmation

9. **Market Direction Filter** ⭐ NEW!
   - ✅ Analyzes Nifty 50 trend
   - ✅ Prefers long when Nifty bullish
   - ✅ Prefers short when Nifty bearish

---

## 🎯 Output Features (All Implemented):

### For Each Stock:
- ✅ Stock name
- ✅ Trade direction (BUY/SELL) - Clear action labels
- ✅ Entry price
- ✅ Stop loss (calculated using ATR)
- ✅ Target price (1:2 risk-reward ratio)
- ✅ Risk amount in ₹
- ✅ Reward amount in ₹
- ✅ Risk-Reward ratio
- ✅ Detailed reasons (which conditions satisfied)
- ✅ Quality score out of 12
- ✅ Current price, volume, RSI, VWAP
- ✅ Day high/low range
- ✅ Sector information

### Limits:
- ✅ Shows only 3-5 highest quality setups
- ✅ Separate sections for BUY and SELL
- ✅ Avoids low-volume, sideways stocks
- ✅ Clean, professional output format

---

## 🚀 How to Use

### Method 1: Double-click (Easiest)
```
Double-click: run_pro_scanner.bat
```

### Method 2: Command Line
```bash
python intraday_scanner_pro.py
```

---

## 📊 Sample Output

```
================================================================================
🎯 PROFESSIONAL NSE INTRADAY SCANNER - 2026-05-03 10:30:00
================================================================================

📊 Analyzing Nifty 50 trend...
✅ Nifty Trend: 🟢 BULLISH (Prefer LONG trades)

Scanning 50 highly liquid stocks...
Applying professional trader criteria...

✅ Found 3 PREMIUM High-Probability Setups

================================================================================
🟢 BUY OPPORTUNITIES (2 setups)
================================================================================

1. 🎯 RELIANCE - BUY SETUP
   ───────────────────────────────────────────────────────────────────────
   📈 ENTRY:     ₹2,450.00
   🛑 STOP LOSS: ₹2,430.00 (Risk: ₹20.00)
   🎯 TARGET:    ₹2,490.00 (Reward: ₹40.00)
   💰 RISK-REWARD RATIO: 1:2.0
   ───────────────────────────────────────────────────────────────────────
   📊 Current: ₹2,450.00 | Change: +2.1% | Vol: 2.3x
   📉 VWAP: ₹2,435.00 | RSI: 65.3 | Day Range: ₹2,400-₹2,452
   🏢 Sector: Energy | Quality Score: 10/12 ⭐

   ✅ REASONS FOR TRADE:
      ✅ Price above VWAP
      ✅ 20 EMA > 50 EMA (Bullish trend)
      ✅ RSI: 65.3 (Strong momentum)
      ✅ MACD Bullish crossover
      ✅ At Day High
      ✅ Opening Range Breakout
      ✅ Near Day High (Strong momentum)
      ✅ Nifty is Bullish

================================================================================

⚠️  PROFESSIONAL TRADING RULES
================================================================================
1. ALWAYS use the stop loss mentioned - No exceptions!
2. Risk only 1-2% of capital per trade
3. Wait for entry price or better - Don't chase
4. Book partial profits at 1:1 and move SL to entry
5. Exit if setup invalidates (breaks SL or key levels)
6. These are high-probability setups, NOT guaranteed profits
7. This is NOT financial advice - Trade at your own risk
================================================================================
```

---

## 🔍 What Makes This Scanner "Professional"?

### 1. **Strict Quality Filters**
- Only 3-5 best setups (vs 10+ in basic scanners)
- Minimum quality score of 8/12 required
- All mandatory criteria must be met (no compromises)

### 2. **Real Trade Levels**
- Calculated entry, stop loss, and target
- 1:2 minimum risk-reward ratio
- ATR-based stop loss (adapts to volatility)

### 3. **Market Context**
- Analyzes Nifty trend first
- Prefers trades aligned with market
- Warns when trading against market

### 4. **Professional Criteria**
- Price > ₹100 (ensures liquidity)
- Volume > 500K shares daily
- 2× volume surge required
- Near high/low for momentum confirmation

### 5. **Complete Reasoning**
- Shows exactly why each trade qualifies
- Transparent scoring system
- Easy to verify setup validity

---

## 📋 Comparison: Basic vs Professional Scanner

| Feature | Basic Scanner | Pro Scanner |
|---------|--------------|-------------|
| **Stocks Shown** | Top 10 | Top 3-5 only |
| **Entry/SL/Target** | ❌ No | ✅ Yes |
| **Volume Filter** | 1.5× | 2× (stricter) |
| **Price Filter** | None | > ₹100 |
| **Nifty Trend** | ❌ No | ✅ Yes |
| **Day High/Low** | ❌ No | ✅ Yes |
| **Trade Reasons** | Basic | Detailed |
| **Risk-Reward** | ❌ No | ✅ 1:2 minimum |
| **Quality Score** | 8 points | 12 points |
| **Output** | Mixed | Separate BUY/SELL |

---

## 🎓 Understanding the Output

### Quality Score (Out of 12):
- **10-12 points**: Excellent setup, high confidence
- **8-9 points**: Good setup, tradeable
- **< 8 points**: Rejected (not shown)

### Risk-Reward Ratio:
- **1:2** = For every ₹1 risk, ₹2 potential reward
- **1:3** = Even better (shown when available)
- Never shows trades with < 1:2 RR

### Reasons Checklist:
Each trade shows which criteria it satisfies:
- ✅ = Criteria met
- ⚠️ = Warning (e.g., against market trend)

---

## ⚠️ Important Notes

### 1. When to Use This Scanner:
- ✅ Market hours (9:15 AM - 3:30 PM)
- ✅ When Nifty is trending (not sideways)
- ✅ On volatile days (high ATR)

### 2. When NOT to Use:
- ❌ Pre-market or after hours
- ❌ During lunch time (12:30-1:30 PM) - low volume
- ❌ On flat/consolidation days

### 3. Trade Management:
- Enter at given entry price (or better)
- Use EXACT stop loss mentioned
- Book 50% at 1:1, move SL to entry
- Book remaining at target or trail SL

### 4. Position Sizing:
```
Risk per trade = 1% of capital
Position size = (1% of capital) / (Entry - Stop Loss)

Example:
Capital = ₹1,00,000
Risk = ₹1,000 (1%)
Entry = ₹2,450
Stop = ₹2,430
Risk per share = ₹20

Position size = ₹1,000 / ₹20 = 50 shares
```

---

## 🔧 Files Included

| File | Purpose |
|------|---------|
| `intraday_scanner_pro.py` | Professional scanner (ALL features) |
| `intraday_scanner.py` | Basic scanner (simpler, more results) |
| `intraday_scanner_upstox.py` | Real-time with Upstox API |
| `scanner_nse_direct.py` | No API needed (slow) |
| `run_pro_scanner.bat` | Quick launcher for Pro scanner |

---

## 💡 Tips for Best Results

### 1. **Scan Multiple Times**
- Scan at 9:30 AM (opening range setup)
- Scan at 10:00 AM (trend confirmation)
- Scan at 2:00 PM (afternoon momentum)

### 2. **Combine with Chart**
- Always verify on chart before entering
- Check for clean breakout/breakdown
- Confirm volume at entry

### 3. **Trade Management**
- Never skip stop loss
- Don't chase if entry missed
- Be patient for setup

### 4. **Track Performance**
- Save scanner output (auto-saved to CSV)
- Maintain trade journal
- Review winning setups

---

## 🆚 Which Scanner Should I Use?

### Use **Pro Scanner** if:
- ✅ You want only the BEST setups
- ✅ You follow strict risk management
- ✅ You prefer quality over quantity
- ✅ You want entry/stop/target levels
- ✅ You trade seriously with real money

### Use **Basic Scanner** if:
- You want more options to choose from
- You're learning/practicing
- You want simpler output
- You scan for general ideas

---

## 📞 Quick Start Checklist

- [ ] Market is open (9:15 AM - 3:30 PM)
- [ ] Run: `python intraday_scanner_pro.py`
- [ ] Check Nifty trend (shown at top)
- [ ] Review 3-5 setups shown
- [ ] Verify on chart
- [ ] Enter at entry price with stop loss
- [ ] Manage trade as per rules

---

## ⚡ Summary of Changes

### What Was Added (Based on Your Requirements):

1. ✅ **Nifty trend analysis** - Market direction filter
2. ✅ **Entry/Stop/Target prices** - Complete trade plan
3. ✅ **Volume changed to 2×** - Stricter filter
4. ✅ **Price > ₹100 filter** - Liquidity requirement
5. ✅ **Near day high/low check** - Momentum confirmation
6. ✅ **Limited to 3-5 setups** - Quality over quantity
7. ✅ **BUY/SELL labels** - Clear action words
8. ✅ **Detailed reasons** - Transparent criteria
9. ✅ **Risk-Reward ratio** - Professional risk management
10. ✅ **Separate BUY/SELL sections** - Better organization

---

**You now have a COMPLETE professional-grade intraday scanner! 🎉**

Run it and see the difference in quality! 📈
