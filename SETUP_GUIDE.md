# Quick Setup Guide

## Step 1: Install Python

You need Python 3.8 or higher. Choose one option:

### Option A: Official Python (Recommended)
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Restart your terminal/command prompt

### Option B: Microsoft Store
1. Open Microsoft Store
2. Search "Python 3.12"
3. Click Install

## Step 2: Verify Installation

Open a NEW command prompt or terminal and run:
```bash
python --version
```

You should see something like: `Python 3.12.x`

## Step 3: Install Dependencies

In the `stock` folder, run:
```bash
python -m pip install -r requirements.txt
```

Or install manually:
```bash
python -m pip install yfinance pandas numpy
```

## Step 4: Run the Scanner

### Single Scan
```bash
python intraday_scanner.py
```

### Live Monitor (Continuous)
```bash
python live_monitor.py
```

---

## Quick Test

After installing dependencies, run:
```bash
python -c "import yfinance; print('✓ Setup successful!')"
```

If you see "✓ Setup successful!" - you're ready to scan!

---

## Troubleshooting

### "python is not recognized"
- Python is not installed or not in PATH
- Reinstall Python and check "Add to PATH"
- Restart terminal

### "'pip' is not recognized"
- Use `python -m pip` instead of just `pip`

### Permission errors during install
```bash
python -m pip install --user yfinance pandas numpy
```

---

## Next Steps

Once setup is complete:
1. Read `README.md` for full usage guide
2. Run your first scan during market hours (9:15 AM - 3:30 PM)
3. Review the results and understand the criteria
4. Paper trade before going live!
