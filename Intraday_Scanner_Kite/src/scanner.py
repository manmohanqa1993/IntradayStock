"""
Best Intraday Stock Finder - KITE VERSION
=========================================
Real-time F&O momentum continuation screener using Zerodha Kite Connect API

Author: AI-Powered Trading System
Version: 1.0 - Kite Edition
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import *
from kite_data_handler import KiteDataHandler, load_fno_stocks
from strategy_validator import MomentumStrategyValidator
from alert_system import AlertSystem

# Setup logging
os.makedirs('logs', exist_ok=True)

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=LOG_MAX_BYTES,
    backupCount=LOG_BACKUP_COUNT
)
handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    handlers=[handler]
)

logger = logging.getLogger(__name__)


class IntradayStockFinder:
    """Main scanner class for finding intraday momentum setups"""

    def __init__(self):
        self.data_handler = None
        self.validator = MomentumStrategyValidator()
        self.alert_system = AlertSystem()
        self.fno_stocks = []
        self.found_signals = []
        self.last_scan_time = None

    def initialize(self):
        """Initialize all components"""
        print("\n" + "="*60)
        print(" BEST INTRADAY STOCK FINDER - KITE EDITION")
        print("="*60)
        print()

        # Load F&O stocks
        print("📋 Loading F&O stock list...")
        self.fno_stocks = load_fno_stocks()
        print(f"✅ Loaded {len(self.fno_stocks)} F&O stocks")
        print()

        # Initialize Kite connection
        print("🔌 Connecting to Zerodha Kite...")
        kite_config = get_kite_config()
        self.data_handler = KiteDataHandler(kite_config)

        if not self.data_handler.connect():
            print("\n❌ Failed to connect to Kite API")
            print("\n📝 Please check:")
            print("1. Your API key and secret are correct in config.py")
            print("2. You have completed the login process")
            print("3. Your access token is valid (regenerate if expired)")
            return False

        print()

        # Test alert system
        if ENABLE_TELEGRAM:
            print("📱 Testing Telegram connection...")
            if self.alert_system.test_connection():
                print("✅ Telegram alerts enabled")
            else:
                print("⚠️ Telegram alerts disabled (check config.py)")
        print()

        logger.info("Scanner initialized successfully")
        return True

    def start(self):
        """Start the scanning loop"""
        if not self.initialize():
            return

        print("🚀 SCANNER STARTED")
        print("="*60)
        print()

        # Check market status
        if not is_market_open():
            print("⚠️ Market is currently closed (9:15 AM - 3:30 PM IST)")
            print()
            response = input("Do you want to run in TEST MODE? (y/n): ").strip().lower()

            if response != 'y':
                print("Scanner stopped. Come back during market hours!")
                return

            print("\n🧪 Running in TEST MODE - scanning with available data")
            print()

        self._run_scanning_loop()

    def _run_scanning_loop(self):
        """Main scanning loop"""
        scan_count = 0

        try:
            while True:
                scan_count += 1
                current_time = datetime.now()

                print(f"\n{'='*60}")
                print(f"🔍 SCAN #{scan_count} - {current_time.strftime('%I:%M:%S %p')}")
                print(f"{'='*60}\n")

                # Run scan
                signals = self._run_scan()

                # Display results
                if signals:
                    self._display_signals(signals)
                    self._save_signals(signals)
                    self._send_alerts(signals)
                else:
                    print("📊 No signals found in this scan")
                    print(f"   Scanned {len(self.fno_stocks)} stocks")
                    print(f"   No setups meeting all 8 conditions")

                # Check if still scanning time
                if is_market_open() and not is_scanning_time():
                    print("\n⏰ Scanning window ended (3:00 PM)")
                    print("Market closes at 3:30 PM")

                    response = input("\nContinue scanning? (y/n): ").strip().lower()
                    if response != 'y':
                        break

                # Wait for next scan
                print(f"\n💤 Waiting {SCAN_INTERVAL_SECONDS} seconds until next scan...")
                print(f"   Press Ctrl+C to stop")

                time.sleep(SCAN_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n\n⏹️  Scanner stopped by user")
            logger.info("Scanner stopped by user")

        except Exception as e:
            print(f"\n❌ Error in scanning loop: {str(e)}")
            logger.error(f"Error in scanning loop: {str(e)}", exc_info=True)

        finally:
            print("\n👋 Scanner shutdown complete")
            print(f"   Total scans performed: {scan_count}")
            print(f"   Total signals found: {len(self.found_signals)}")

    def _run_scan(self):
        """Run a single scan across all stocks"""
        signals = []

        if USE_MULTITHREADING:
            signals = self._scan_parallel()
        else:
            for symbol in self.fno_stocks:
                signal = self._scan_single_stock(symbol)
                if signal:
                    signals.append(signal)

        self.last_scan_time = datetime.now()
        return signals

    def _scan_parallel(self):
        """Scan stocks in parallel using threading"""
        signals = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_stock = {
                executor.submit(self._scan_single_stock, symbol): symbol
                for symbol in self.fno_stocks
            }

            for future in as_completed(future_to_stock):
                symbol = future_to_stock[future]
                try:
                    signal = future.result()
                    if signal:
                        signals.append(signal)
                except Exception as e:
                    logger.error(f"Error scanning {symbol}: {str(e)}")

        return signals

    def _scan_single_stock(self, symbol):
        """Scan a single stock for signals"""
        try:
            # Get intraday candles
            candles_df = self.data_handler.get_intraday_data(symbol, CANDLE_INTERVAL)

            if candles_df is None or len(candles_df) < 10:
                return None

            # Get historical data for volume comparison
            hist_data = self.data_handler.get_historical_data(symbol, VOLUME_LOOKBACK_DAYS)

            if hist_data is None:
                return None

            # Get stock info for liquidity filter
            stock_info = self.data_handler.get_stock_info(symbol)

            # Validate stock against strategy
            result = self.validator.validate_stock(symbol, candles_df, hist_data, stock_info)

            if result and result['is_valid']:
                # Calculate trade levels
                signal = self._calculate_trade_levels(result, candles_df)
                return signal

            return None

        except Exception as e:
            logger.debug(f"Error scanning {symbol}: {str(e)}")
            return None

    def _calculate_trade_levels(self, signal, candles_df):
        """Calculate entry, stop-loss, and target levels"""
        try:
            signal_type = signal['signal_type']
            latest_candle = candles_df.iloc[-1]
            latest_vwap = latest_candle['vwap']

            # Entry price (current price)
            entry_price = latest_candle['close']

            # Stop-loss calculation
            if SL_METHOD == 'vwap':
                if signal_type == 'BULLISH':
                    stop_loss = latest_vwap - (latest_vwap * 0.002)  # 0.2% below VWAP
                else:
                    stop_loss = latest_vwap + (latest_vwap * 0.002)  # 0.2% above VWAP

            elif SL_METHOD == 'previous_candle_low':
                if signal_type == 'BULLISH':
                    stop_loss = candles_df['low'].iloc[-2]
                else:
                    stop_loss = candles_df['high'].iloc[-2]

            elif SL_METHOD == 'percentage':
                if signal_type == 'BULLISH':
                    stop_loss = entry_price * (1 - SL_PERCENTAGE/100)
                else:
                    stop_loss = entry_price * (1 + SL_PERCENTAGE/100)

            elif SL_METHOD == 'atr':
                # Calculate ATR
                high_low = candles_df['high'] - candles_df['low']
                atr = high_low.rolling(window=14).mean().iloc[-1]

                if signal_type == 'BULLISH':
                    stop_loss = entry_price - (atr * SL_ATR_MULTIPLIER)
                else:
                    stop_loss = entry_price + (atr * SL_ATR_MULTIPLIER)

            else:
                stop_loss = latest_vwap

            # Target calculation (based on R:R ratio)
            risk = abs(entry_price - stop_loss)
            reward = risk * RISK_REWARD_RATIO

            if signal_type == 'BULLISH':
                target_price = entry_price + reward
            else:
                target_price = entry_price - reward

            # Add to signal
            signal['entry_price'] = round(entry_price, 2)
            signal['stop_loss'] = round(stop_loss, 2)
            signal['target_price'] = round(target_price, 2)
            signal['risk_reward_ratio'] = f"1:{RISK_REWARD_RATIO}"
            signal['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            return signal

        except Exception as e:
            logger.error(f"Error calculating trade levels: {str(e)}")
            return signal

    def _display_signals(self, signals):
        """Display signals in console"""
        bullish = [s for s in signals if s['signal_type'] == 'BULLISH']
        bearish = [s for s in signals if s['signal_type'] == 'BEARISH']

        if bullish:
            print(f"\n📈 BULLISH SIGNALS ({len(bullish)})")
            print("="*60)
            for i, signal in enumerate(bullish[:MAX_SIGNALS_DISPLAY], 1):
                self._print_signal(i, signal)

        if bearish:
            print(f"\n📉 BEARISH SIGNALS ({len(bearish)})")
            print("="*60)
            for i, signal in enumerate(bearish[:MAX_SIGNALS_DISPLAY], 1):
                self._print_signal(i, signal)

    def _print_signal(self, index, signal):
        """Print a single signal"""
        print(f"\n{index}. {signal['symbol']} - Strength: {signal['strength']}/10")
        print("─" * 40)
        print(f"   💰 Entry: ₹{signal['entry_price']}")
        print(f"   🛑 SL: ₹{signal['stop_loss']}")
        print(f"   🎯 Target: ₹{signal['target_price']}")
        print(f"   📊 R:R = {signal['risk_reward_ratio']}")

        if 'conditions_met' in signal:
            print(f"   ✅ Conditions: {'/'.join(signal['conditions_met'])}")

    def _save_signals(self, signals):
        """Save signals to CSV and JSON files"""
        if not SAVE_SIGNALS_TO_FILE or not signals:
            return

        try:
            os.makedirs(SIGNALS_OUTPUT_DIR, exist_ok=True)
            date_str = datetime.now().strftime('%Y-%m-%d')

            # Convert to DataFrame
            df = pd.DataFrame(signals)

            # Save as CSV
            if SAVE_AS_CSV:
                csv_file = os.path.join(
                    SIGNALS_OUTPUT_DIR,
                    CSV_FILENAME_FORMAT.format(date=date_str)
                )
                df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
                logger.info(f"Saved signals to {csv_file}")

            # Save as JSON
            if SAVE_AS_JSON:
                json_file = os.path.join(
                    SIGNALS_OUTPUT_DIR,
                    JSON_FILENAME_FORMAT.format(date=date_str)
                )
                df.to_json(json_file, orient='records', indent=2)
                logger.info(f"Saved signals to {json_file}")

            # Add to found signals
            self.found_signals.extend(signals)

        except Exception as e:
            logger.error(f"Error saving signals: {str(e)}")

    def _send_alerts(self, signals):
        """Send alerts for new signals"""
        for signal in signals:
            self.alert_system.send_signal_alert(signal)


def main():
    """Main entry point"""
    scanner = IntradayStockFinder()
    scanner.start()


if __name__ == "__main__":
    main()
