"""
BEST INTRADAY STOCK FINDER
==========================
Production-ready F&O momentum continuation screener for Indian stock market

Features:
- Real-time F&O stock scanning
- 8-point strategy validation
- Multi-broker support
- Signal generation with entry/SL/target
- Alerts (Telegram, Sound, Console)
- Backtesting capability

Author: Custom Built
Date: May 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json

# Import custom modules
from config import *
from strategy_validator import MomentumStrategyValidator, calculate_vwap, calculate_atr
from data_handler import DataHandler, load_fno_stocks
from alert_system import AlertSystem

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(os.path.join('logs', LOG_FILE)),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ==================== MAIN SCREENER CLASS ====================

class IntradayStockFinder:
    """
    Main screener class - orchestrates scanning and signal generation
    """

    def __init__(self):
        """Initialize screener"""
        self.name = "Best Intraday Stock Finder"
        self.version = "1.0"

        logger.info("="*80)
        logger.info(f"{self.name} v{self.version}")
        logger.info("="*80)

        # Initialize components
        self.data_handler = DataHandler()
        self.validator = MomentumStrategyValidator()
        self.alert_system = AlertSystem()

        # Load F&O stocks
        self.fno_stocks = load_fno_stocks()
        logger.info(f"Loaded {len(self.fno_stocks)} F&O stocks")

        # Signal storage
        self.active_signals = []
        self.signal_history = []

        # Running state
        self.is_running = False
        self.scan_count = 0

    def start(self):
        """Start the screener"""
        logger.info("Starting screener...")

        # Connect to broker
        if not self.data_handler.connect():
            logger.error("Failed to connect to broker. Please check credentials.")
            return False

        logger.info(f"✅ Connected to {self.data_handler.broker.name}")

        # Check market hours
        if not is_market_open():
            logger.warning("Market is currently closed")
            if input("Continue anyway? (y/n): ").lower() != 'y':
                return False

        self.is_running = True

        # Start scanning loop
        self._run_scanning_loop()

        return True

    def stop(self):
        """Stop the screener"""
        logger.info("Stopping screener...")
        self.is_running = False

    def _run_scanning_loop(self):
        """Main scanning loop"""
        logger.info("="*80)
        logger.info("🚀 SCANNING STARTED")
        logger.info("="*80)

        try:
            while self.is_running:
                # Check if it's scanning time
                if not is_scanning_time():
                    if is_market_open():
                        logger.info("Outside scanning window, waiting...")
                        time.sleep(60)
                        continue
                    else:
                        logger.info("Market closed. Stopping scanner.")
                        break

                # Run scan
                self._run_scan()

                # Clear old signals
                self._cleanup_old_signals()

                # Save signals
                if SAVE_SIGNALS_TO_FILE:
                    self._save_signals()

                # Wait before next scan
                logger.info(f"Next scan in {SCAN_INTERVAL_SECONDS} seconds...")
                time.sleep(SCAN_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            logger.info("Scan interrupted by user")
        except Exception as e:
            logger.error(f"Error in scanning loop: {str(e)}")
        finally:
            self.stop()

    def _run_scan(self):
        """Execute one complete scan cycle"""
        self.scan_count += 1
        scan_start = datetime.now()

        logger.info("="*80)
        logger.info(f"SCAN #{self.scan_count} - {scan_start.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*80)

        # Scan stocks in parallel
        signals = []

        if USE_MULTITHREADING:
            signals = self._scan_parallel()
        else:
            signals = self._scan_sequential()

        # Filter by minimum signal strength
        quality_signals = [s for s in signals if s.get('signal_strength', 0) >= MIN_SIGNAL_STRENGTH]

        # Sort by signal strength
        quality_signals.sort(key=lambda x: x['signal_strength'], reverse=True)

        # Limit displayed signals
        display_signals = quality_signals[:MAX_SIGNALS_DISPLAY]

        # Update active signals
        self.active_signals = display_signals

        # Add to history
        self.signal_history.extend(display_signals)

        # Display results
        self._display_signals(display_signals)

        # Send alerts
        for signal in display_signals:
            self.alert_system.send_alert(signal)

        # Scan summary
        scan_duration = (datetime.now() - scan_start).seconds
        logger.info("="*80)
        logger.info(f"Scan #{self.scan_count} completed in {scan_duration}s")
        logger.info(f"Signals found: {len(signals)} total, {len(quality_signals)} quality, {len(display_signals)} displayed")
        logger.info("="*80)

    def _scan_parallel(self):
        """Scan stocks in parallel using ThreadPoolExecutor"""
        signals = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all scan tasks
            future_to_symbol = {
                executor.submit(self._scan_single_stock, symbol): symbol
                for symbol in self.fno_stocks
            }

            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    result = future.result()
                    if result and result.get('passed'):
                        signals.append(result)
                except Exception as e:
                    logger.error(f"Error scanning {symbol}: {str(e)}")

        return signals

    def _scan_sequential(self):
        """Scan stocks sequentially"""
        signals = []

        for i, symbol in enumerate(self.fno_stocks, 1):
            logger.info(f"Scanning {symbol} ({i}/{len(self.fno_stocks)})...")

            try:
                result = self._scan_single_stock(symbol)
                if result and result.get('passed'):
                    signals.append(result)
            except Exception as e:
                logger.error(f"Error scanning {symbol}: {str(e)}")

        return signals

    def _scan_single_stock(self, symbol):
        """
        Scan a single stock

        Returns:
            dict: Validation result with signal details
        """
        try:
            # Fetch data
            intraday_candles = self.data_handler.get_intraday_candles(symbol)
            historical_data = self.data_handler.get_historical_data(symbol, VOLUME_LOOKBACK_DAYS)
            stock_info = self.data_handler.get_stock_info(symbol)

            if intraday_candles is None or historical_data is None or stock_info is None:
                return None

            # Validate stock
            result = self.validator.validate_stock(
                symbol=symbol,
                candles_df=intraday_candles,
                historical_data=historical_data,
                stock_info=stock_info
            )

            if result.get('passed'):
                # Calculate entry/SL/target
                result = self._calculate_trade_levels(result, intraday_candles)

            return result

        except Exception as e:
            logger.error(f"Error in _scan_single_stock for {symbol}: {str(e)}")
            return None

    def _calculate_trade_levels(self, signal, candles_df):
        """
        Calculate entry, stop-loss, and target prices

        Args:
            signal: Signal dict from validator
            candles_df: Candle data

        Returns:
            Updated signal with trade levels
        """
        try:
            symbol = signal['symbol']
            signal_type = signal['signal']
            current_price = candles_df.iloc[-1]['close']
            vwap = candles_df.iloc[-1]['vwap']

            # Entry
            signal['entry_price'] = round(current_price, 2)

            # Stop Loss calculation
            if SL_METHOD == 'vwap':
                if signal_type == 'BULLISH':
                    sl = vwap
                else:
                    sl = vwap

            elif SL_METHOD == 'previous_candle_low':
                if signal_type == 'BULLISH':
                    sl = candles_df.iloc[-2]['low']
                else:
                    sl = candles_df.iloc[-2]['high']

            elif SL_METHOD == 'atr':
                atr = calculate_atr(candles_df)
                if signal_type == 'BULLISH':
                    sl = current_price - (atr * SL_ATR_MULTIPLIER)
                else:
                    sl = current_price + (atr * SL_ATR_MULTIPLIER)

            else:  # percentage
                if signal_type == 'BULLISH':
                    sl = current_price * (1 - SL_PERCENTAGE/100)
                else:
                    sl = current_price * (1 + SL_PERCENTAGE/100)

            signal['stop_loss'] = round(sl, 2)

            # Calculate risk
            risk = abs(current_price - sl)
            signal['risk'] = round(risk, 2)

            # Calculate target (based on risk-reward ratio)
            reward = risk * RISK_REWARD_RATIO

            if signal_type == 'BULLISH':
                target = current_price + reward
            else:
                target = current_price - reward

            signal['target_price'] = round(target, 2)
            signal['reward'] = round(reward, 2)
            signal['risk_reward_ratio'] = RISK_REWARD_RATIO

            # Calculate position size (simple)
            risk_percent = (risk / current_price) * 100
            signal['risk_percent'] = round(risk_percent, 2)

            return signal

        except Exception as e:
            logger.error(f"Error calculating trade levels: {str(e)}")
            return signal

    def _display_signals(self, signals):
        """Display signals in console"""
        if not signals:
            logger.info("\n⚠️  No signals found in this scan\n")
            return

        # Separate bullish and bearish
        bullish = [s for s in signals if s['signal'] == 'BULLISH']
        bearish = [s for s in signals if s['signal'] == 'BEARISH']

        # Display bullish
        if bullish:
            print("\n" + "="*100)
            print(f"📈 BULLISH SIGNALS ({len(bullish)})")
            print("="*100)

            for i, signal in enumerate(bullish, 1):
                self._print_signal(i, signal)

        # Display bearish
        if bearish:
            print("\n" + "="*100)
            print(f"📉 BEARISH SIGNALS ({len(bearish)})")
            print("="*100)

            for i, signal in enumerate(bearish, 1):
                self._print_signal(i, signal)

        print("\n" + "="*100 + "\n")

    def _print_signal(self, rank, signal):
        """Print single signal"""
        print(f"\n{rank}. {signal['symbol']} - Strength: {signal['signal_strength']}/10")
        print(f"   {'─'*95}")
        print(f"   💰 Entry: ₹{signal['entry_price']} | SL: ₹{signal['stop_loss']} | Target: ₹{signal['target_price']}")
        print(f"   📊 Risk: ₹{signal['risk']} | Reward: ₹{signal['reward']} | R:R = 1:{signal['risk_reward_ratio']}")
        print(f"   📈 Volume Ratio: {signal['checks']['volume']['volume_ratio']}x | Gap: {signal['checks']['gap']['gap_percent']:.2f}%")
        print(f"   🎯 VWAP: ₹{signal['checks']['vwap'].get('vwap', 'N/A')} | Pattern: {signal['checks']['pattern']['pattern']}")
        print(f"   ⏰ Time: {signal['timestamp'].strftime('%H:%M:%S')}")

    def _cleanup_old_signals(self):
        """Remove expired signals"""
        cutoff_time = datetime.now() - timedelta(minutes=SIGNAL_EXPIRY_MINUTES)

        self.active_signals = [
            s for s in self.active_signals
            if s['timestamp'] > cutoff_time
        ]

    def _save_signals(self):
        """Save signals to file"""
        try:
            if not self.active_signals:
                return

            date_str = datetime.now().strftime('%Y-%m-%d')

            # Save as CSV
            if SAVE_AS_CSV:
                csv_file = os.path.join(SIGNALS_OUTPUT_DIR, CSV_FILENAME_FORMAT.format(date=date_str))
                df = pd.DataFrame(self.active_signals)
                df.to_csv(csv_file, index=False)
                logger.debug(f"Signals saved to {csv_file}")

            # Save as JSON
            if SAVE_AS_JSON:
                json_file = os.path.join(SIGNALS_OUTPUT_DIR, JSON_FILENAME_FORMAT.format(date=date_str))
                with open(json_file, 'w') as f:
                    json.dump(self.active_signals, f, indent=2, default=str)
                logger.debug(f"Signals saved to {json_file}")

        except Exception as e:
            logger.error(f"Error saving signals: {str(e)}")

    def get_active_signals(self):
        """Get currently active signals"""
        return self.active_signals

    def get_signal_summary(self):
        """Get summary statistics"""
        total_signals = len(self.signal_history)
        bullish_count = len([s for s in self.signal_history if s['signal'] == 'BULLISH'])
        bearish_count = len([s for s in self.signal_history if s['signal'] == 'BEARISH'])

        avg_strength = np.mean([s['signal_strength'] for s in self.signal_history]) if self.signal_history else 0

        return {
            'total_signals': total_signals,
            'bullish_signals': bullish_count,
            'bearish_signals': bearish_count,
            'avg_signal_strength': round(avg_strength, 2),
            'scan_count': self.scan_count
        }


# ==================== ALERT SYSTEM (PLACEHOLDER) ====================
# Will be implemented in separate file

class AlertSystem:
    """Simple alert system"""

    def __init__(self):
        pass

    def send_alert(self, signal):
        """Send alert for new signal"""
        if ENABLE_CONSOLE_ALERTS:
            print(f"\n🔔 NEW SIGNAL: {signal['symbol']} - {signal['signal']} (Strength: {signal['signal_strength']}/10)")

        if ENABLE_SOUND_ALERTS:
            self._play_sound()

        if ENABLE_TELEGRAM:
            self._send_telegram(signal)

    def _play_sound(self):
        """Play alert sound"""
        try:
            # Simple beep for Windows
            import winsound
            winsound.Beep(1000, 500)
        except:
            pass

    def _send_telegram(self, signal):
        """Send Telegram alert"""
        # Implement Telegram bot integration
        pass


# ==================== MAIN EXECUTION ====================

def main():
    """Main entry point"""
    print("\n" + "="*100)
    print("🎯 BEST INTRADAY STOCK FINDER - F&O Momentum Continuation Scanner")
    print("="*100)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Broker: {BROKER.upper()}")
    print(f"🕒 Market Hours: {MARKET_OPEN} - {MARKET_CLOSE}")
    print(f"🔍 Scan Window: {SCAN_START_TIME} - {SCAN_END_TIME}")
    print(f"⏱️  Scan Interval: {SCAN_INTERVAL_SECONDS} seconds")
    print(f"🎯 Min Signal Strength: {MIN_SIGNAL_STRENGTH}/10")
    print("="*100 + "\n")

    # Create screener instance
    screener = IntradayStockFinder()

    # Start scanning
    try:
        screener.start()
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
    finally:
        # Show summary
        summary = screener.get_signal_summary()
        print("\n" + "="*100)
        print("📊 SESSION SUMMARY")
        print("="*100)
        print(f"Total Scans: {summary['scan_count']}")
        print(f"Total Signals: {summary['total_signals']}")
        print(f"  • Bullish: {summary['bullish_signals']}")
        print(f"  • Bearish: {summary['bearish_signals']}")
        print(f"Avg Signal Strength: {summary['avg_signal_strength']}/10")
        print("="*100 + "\n")

        print("✅ Screener stopped successfully\n")


if __name__ == "__main__":
    main()
