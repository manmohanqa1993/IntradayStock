"""
Intraday Scanner - Main Scanner
================================
Simple scanner for beginners
"""

import pandas as pd
import time
import os
import sys
from datetime import datetime
import logging

# Add config to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
from settings import *

from data_handler import DataHandler
from strategy import StrategyValidator
from alerts import AlertSystem

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'scanner.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class IntradayScanner:
    """Main scanner class"""

    def __init__(self):
        self.data_handler = DataHandler()
        self.validator = StrategyValidator()
        self.alerts = AlertSystem()
        self.stocks = self._load_stocks()
        self.signals_found = []

    def _load_stocks(self):
        """Load stock list"""
        try:
            if os.path.exists(STOCKS_FILE):
                with open(STOCKS_FILE, 'r') as f:
                    stocks = [line.strip() for line in f if line.strip()]
                print(f"✅ Loaded {len(stocks)} stocks from file")
                return stocks
            else:
                print(f"⚠️ Using default stock list ({len(STOCKS_BACKUP)} stocks)")
                return STOCKS_BACKUP
        except:
            return STOCKS_BACKUP

    def start(self):
        """Start scanning"""
        print("🚀 Scanner Started")
        print("="*60)
        print()

        # Check market status
        if not is_market_open():
            print("⚠️ Market is closed (9:15 AM - 3:30 PM IST)")
            response = input("Run in TEST mode? (y/n): ").strip().lower()
            if response != 'y':
                print("Stopped. Come back during market hours!")
                return

        scan_count = 0

        try:
            while True:
                scan_count += 1
                print(f"\n{'='*60}")
                print(f"🔍 SCAN #{scan_count} - {datetime.now().strftime('%I:%M:%S %p')}")
                print(f"{'='*60}\n")

                signals = self._scan_all_stocks()

                if signals:
                    self._display_signals(signals)
                    self._save_signals(signals)
                else:
                    print(f"📊 No signals found")
                    print(f"   Scanned: {len(self.stocks)} stocks")

                print(f"\n💤 Waiting {SCAN_INTERVAL_SECONDS}s...")
                print("   Press Ctrl+C to stop")
                time.sleep(SCAN_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n\n⏹️ Scanner stopped")
            print(f"   Total scans: {scan_count}")
            print(f"   Signals found: {len(self.signals_found)}")

    def _scan_all_stocks(self):
        """Scan all stocks"""
        signals = []

        for symbol in self.stocks:
            signal = self._scan_stock(symbol)
            if signal:
                signals.append(signal)

        return signals

    def _scan_stock(self, symbol):
        """Scan single stock"""
        try:
            # Get data
            candles = self.data_handler.get_intraday_candles(symbol)
            hist = self.data_handler.get_historical_data(symbol)

            if candles is None or hist is None:
                return None

            # Validate strategy
            result = self.validator.validate(symbol, candles, hist)

            if result:
                # Calculate trade levels
                result = self._calculate_levels(result, candles)
                return result

            return None

        except Exception as e:
            logger.debug(f"Error scanning {symbol}: {e}")
            return None

    def _calculate_levels(self, signal, candles):
        """Calculate entry/SL/target"""
        try:
            latest = candles.iloc[-1]
            entry = latest['close']
            vwap = latest['vwap']

            # Simple SL based on VWAP
            if signal['signal_type'] == 'BULLISH':
                sl = vwap * 0.998  # 0.2% below VWAP
            else:
                sl = vwap * 1.002  # 0.2% above VWAP

            # Target based on R:R
            risk = abs(entry - sl)
            reward = risk * RISK_REWARD_RATIO

            if signal['signal_type'] == 'BULLISH':
                target = entry + reward
            else:
                target = entry - reward

            signal['entry'] = round(entry, 2)
            signal['sl'] = round(sl, 2)
            signal['target'] = round(target, 2)
            signal['rr'] = f"1:{RISK_REWARD_RATIO}"

            return signal

        except:
            return signal

    def _display_signals(self, signals):
        """Display signals"""
        bullish = [s for s in signals if s['signal_type'] == 'BULLISH']
        bearish = [s for s in signals if s['signal_type'] == 'BEARISH']

        if bullish:
            print(f"\n📈 BULLISH SIGNALS ({len(bullish)})")
            print("="*60)
            for i, sig in enumerate(bullish[:MAX_SIGNALS_DISPLAY], 1):
                self._print_signal(i, sig)

        if bearish:
            print(f"\n📉 BEARISH SIGNALS ({len(bearish)})")
            print("="*60)
            for i, sig in enumerate(bearish[:MAX_SIGNALS_DISPLAY], 1):
                self._print_signal(i, sig)

        # Send alerts
        for sig in signals:
            self.alerts.send_signal_alert(sig)

    def _print_signal(self, index, signal):
        """Print single signal"""
        print(f"\n{index}. {signal['symbol']} - Strength: {signal['strength']}/10")
        print("─" * 40)
        print(f"   💰 Entry: ₹{signal['entry']}")
        print(f"   🛑 SL: ₹{signal['sl']}")
        print(f"   🎯 Target: ₹{signal['target']}")
        print(f"   📊 R:R = {signal['rr']}")

    def _save_signals(self, signals):
        """Save signals to CSV"""
        try:
            if not SAVE_SIGNALS or not signals:
                return

            df = pd.DataFrame(signals)
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = os.path.join(SIGNALS_DIR, f'signals_{date_str}.csv')

            df.to_csv(filename, mode='a',
                     header=not os.path.exists(filename),
                     index=False)

            self.signals_found.extend(signals)

        except Exception as e:
            logger.error(f"Error saving signals: {e}")


if __name__ == "__main__":
    scanner = IntradayScanner()
    scanner.start()
