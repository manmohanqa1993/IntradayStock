"""
Strategy Validator - Core Trading Logic
========================================
Implements all strategy conditions for momentum continuation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Import config
from config import *

logger = logging.getLogger(__name__)


class MomentumStrategyValidator:
    """
    Validates stocks against momentum continuation strategy conditions
    """

    def __init__(self):
        self.name = "Momentum Continuation Strategy"
        logger.info(f"Initialized {self.name}")

    # ==================== 1. RELATIVE VOLUME FILTER ====================

    def check_relative_volume(self, current_volume, historical_data):
        """
        Check if current day volume > 15-day average volume

        Args:
            current_volume: Today's total volume so far
            historical_data: DataFrame with last 15 days data

        Returns:
            (bool, float, dict): (passed, volume_ratio, details)
        """
        try:
            if historical_data is None or len(historical_data) < VOLUME_LOOKBACK_DAYS:
                return False, 0, {'error': 'Insufficient historical data'}

            # Calculate 15-day average volume
            avg_volume = historical_data['volume'].tail(VOLUME_LOOKBACK_DAYS).mean()

            if avg_volume == 0:
                return False, 0, {'error': 'Zero average volume'}

            # Calculate ratio
            volume_ratio = current_volume / avg_volume

            passed = volume_ratio > MIN_VOLUME_RATIO

            details = {
                'current_volume': current_volume,
                'avg_15day_volume': avg_volume,
                'volume_ratio': round(volume_ratio, 2),
                'threshold': MIN_VOLUME_RATIO,
                'passed': passed
            }

            logger.debug(f"Volume check: ratio={volume_ratio:.2f}, passed={passed}")

            return passed, volume_ratio, details

        except Exception as e:
            logger.error(f"Error in relative volume check: {str(e)}")
            return False, 0, {'error': str(e)}

    # ==================== 2. GAP FILTER ====================

    def check_gap(self, prev_day_close, today_open):
        """
        Check if gap is less than 0.5%

        Args:
            prev_day_close: Previous day's last candle close
            today_open: Today's first candle open

        Returns:
            (bool, float, dict): (passed, gap_percent, details)
        """
        try:
            gap_percent = abs((today_open - prev_day_close) / prev_day_close) * 100

            passed = gap_percent < MAX_GAP_PERCENT

            gap_direction = "Gap Up" if today_open > prev_day_close else "Gap Down"

            details = {
                'prev_close': prev_day_close,
                'today_open': today_open,
                'gap_percent': round(gap_percent, 3),
                'gap_direction': gap_direction,
                'threshold': MAX_GAP_PERCENT,
                'passed': passed
            }

            logger.debug(f"Gap check: {gap_percent:.3f}%, {gap_direction}, passed={passed}")

            return passed, gap_percent, details

        except Exception as e:
            logger.error(f"Error in gap check: {str(e)}")
            return False, 0, {'error': str(e)}

    # ==================== 3. FIRST CANDLE MOVE FILTER ====================

    def check_first_candle_move(self, first_candle):
        """
        Check if first 5-min candle move is less than 2%

        Args:
            first_candle: dict/Series with open, high, low, close

        Returns:
            (bool, float, dict): (passed, move_percent, details)
        """
        try:
            open_price = first_candle['open']
            close_price = first_candle['close']

            move_percent = abs((close_price - open_price) / open_price) * 100

            passed = move_percent < MAX_FIRST_CANDLE_MOVE

            candle_type = "Green" if close_price > open_price else "Red"

            details = {
                'open': open_price,
                'close': close_price,
                'move_percent': round(move_percent, 3),
                'candle_type': candle_type,
                'threshold': MAX_FIRST_CANDLE_MOVE,
                'passed': passed
            }

            logger.debug(f"First candle: {move_percent:.3f}%, {candle_type}, passed={passed}")

            return passed, move_percent, details

        except Exception as e:
            logger.error(f"Error in first candle check: {str(e)}")
            return False, 0, {'error': str(e)}

    # ==================== 4. THREE-CANDLE REVERSAL PATTERN ====================

    def check_three_candle_pattern(self, candles_df):
        """
        Check for 3-candle reversal pattern

        BULLISH: Red -> Green -> Green
        BEARISH: Green -> Red -> Red

        Args:
            candles_df: DataFrame with first 3 candles (open, close columns)

        Returns:
            (str, dict): ('BULLISH'/'BEARISH'/None, details)
        """
        try:
            if len(candles_df) < 3:
                return None, {'error': 'Need 3 candles'}

            # Get first 3 candles
            c1 = candles_df.iloc[0]
            c2 = candles_df.iloc[1]
            c3 = candles_df.iloc[2]

            # Determine candle colors
            c1_type = 'green' if c1['close'] > c1['open'] else 'red'
            c2_type = 'green' if c2['close'] > c2['open'] else 'red'
            c3_type = 'green' if c3['close'] > c3['open'] else 'red'

            pattern = f"{c1_type}-{c2_type}-{c3_type}"

            signal = None

            # BULLISH pattern: red-green-green
            if c1_type == 'red' and c2_type == 'green' and c3_type == 'green':
                signal = 'BULLISH'

            # BEARISH pattern: green-red-red
            elif c1_type == 'green' and c2_type == 'red' and c3_type == 'red':
                signal = 'BEARISH'

            details = {
                'candle_1': c1_type,
                'candle_2': c2_type,
                'candle_3': c3_type,
                'pattern': pattern,
                'signal': signal,
                'passed': signal is not None
            }

            logger.debug(f"3-candle pattern: {pattern}, signal={signal}")

            return signal, details

        except Exception as e:
            logger.error(f"Error in 3-candle pattern check: {str(e)}")
            return None, {'error': str(e)}

    # ==================== 5. MOMENTUM CONTINUATION ====================

    def check_momentum_continuation(self, candles_df, signal_type):
        """
        Check if momentum continues after initial 3-candle setup

        Observe next 4-5 candles (total 7-8 candles from start)

        Args:
            candles_df: DataFrame with all candles after pattern
            signal_type: 'BULLISH' or 'BEARISH'

        Returns:
            (bool, dict): (passed, details)
        """
        try:
            if len(candles_df) < (3 + MOMENTUM_OBSERVATION_CANDLES):
                return False, {'error': 'Not enough candles for momentum check'}

            # Get candles after the initial 3-candle pattern
            momentum_candles = candles_df.iloc[3:3+MOMENTUM_OBSERVATION_CANDLES]

            green_count = 0
            red_count = 0

            for idx, candle in momentum_candles.iterrows():
                if candle['close'] > candle['open']:
                    green_count += 1
                else:
                    red_count += 1

            if signal_type == 'BULLISH':
                # Majority should be green
                passed = green_count >= MIN_MOMENTUM_CANDLES
                dominant_color = 'green'
                dominant_count = green_count

            else:  # BEARISH
                # Majority should be red
                passed = red_count >= MIN_MOMENTUM_CANDLES
                dominant_color = 'red'
                dominant_count = red_count

            details = {
                'total_candles': len(momentum_candles),
                'green_candles': green_count,
                'red_candles': red_count,
                'required_minimum': MIN_MOMENTUM_CANDLES,
                'dominant_color': dominant_color,
                'dominant_count': dominant_count,
                'passed': passed
            }

            logger.debug(f"Momentum continuation: {dominant_color}={dominant_count}/{len(momentum_candles)}, passed={passed}")

            return passed, details

        except Exception as e:
            logger.error(f"Error in momentum continuation check: {str(e)}")
            return False, {'error': str(e)}

    # ==================== 6. PULLBACK VALIDATION ====================

    def check_pullback_validity(self, candles_df, signal_type):
        """
        Check if pullbacks are valid (max 1 pullback with lower volume)

        Args:
            candles_df: DataFrame with candles after pattern (3 onwards)
            signal_type: 'BULLISH' or 'BEARISH'

        Returns:
            (bool, dict): (passed, details)
        """
        try:
            if len(candles_df) < 4:
                return True, {'message': 'Too early for pullback check'}

            # Get candles after initial 3-candle pattern
            check_candles = candles_df.iloc[3:]

            pullback_count = 0
            pullback_details = []

            for i in range(len(check_candles)):
                candle = check_candles.iloc[i]

                is_green = candle['close'] > candle['open']
                is_red = candle['close'] < candle['open']

                # Identify pullback
                is_pullback = False

                if signal_type == 'BULLISH' and is_red:
                    is_pullback = True
                elif signal_type == 'BEARISH' and is_green:
                    is_pullback = True

                if is_pullback:
                    pullback_count += 1

                    # Check volume condition (pullback volume < previous candle volume)
                    if i > 0:
                        prev_candle = check_candles.iloc[i-1]
                        volume_valid = candle['volume'] < prev_candle['volume']
                    else:
                        volume_valid = True  # First candle, no previous to compare

                    pullback_details.append({
                        'candle_index': i + 3,  # Actual index in full series
                        'volume': candle['volume'],
                        'prev_volume': prev_candle['volume'] if i > 0 else None,
                        'volume_valid': volume_valid
                    })

            # Check if pullbacks are within limit
            pullback_count_valid = pullback_count <= MAX_PULLBACK_CANDLES

            # Check if all pullbacks have valid volume
            all_pullbacks_volume_valid = all([pb['volume_valid'] for pb in pullback_details])

            passed = pullback_count_valid and (len(pullback_details) == 0 or all_pullbacks_volume_valid)

            details = {
                'pullback_count': pullback_count,
                'max_allowed': MAX_PULLBACK_CANDLES,
                'pullback_count_valid': pullback_count_valid,
                'pullback_details': pullback_details,
                'all_volumes_valid': all_pullbacks_volume_valid,
                'passed': passed
            }

            logger.debug(f"Pullback validation: count={pullback_count}, volumes_valid={all_pullbacks_volume_valid}, passed={passed}")

            return passed, details

        except Exception as e:
            logger.error(f"Error in pullback validation: {str(e)}")
            return False, {'error': str(e)}

    # ==================== 7. VWAP CONFIRMATION ====================

    def check_vwap_confirmation(self, candles_df, signal_type):
        """
        Check if candles respect VWAP

        BULLISH: Close above VWAP
        BEARISH: Close below VWAP

        Args:
            candles_df: DataFrame with candles and VWAP column
            signal_type: 'BULLISH' or 'BEARISH'

        Returns:
            (bool, dict): (passed, details)
        """
        try:
            if 'vwap' not in candles_df.columns:
                return False, {'error': 'VWAP not calculated'}

            # Check candles after initial pattern (from candle 3 onwards)
            check_candles = candles_df.iloc[3:]

            vwap_respect_count = 0
            vwap_violation_count = 0

            for idx, candle in check_candles.iterrows():
                if signal_type == 'BULLISH':
                    # Should close above VWAP
                    if candle['close'] > candle['vwap']:
                        vwap_respect_count += 1
                    else:
                        vwap_violation_count += 1

                else:  # BEARISH
                    # Should close below VWAP
                    if candle['close'] < candle['vwap']:
                        vwap_respect_count += 1
                    else:
                        vwap_violation_count += 1

            total_candles = len(check_candles)

            if VWAP_STRICT_MODE:
                # All candles must respect VWAP
                passed = vwap_violation_count == 0
            else:
                # Majority must respect VWAP (>70%)
                passed = (vwap_respect_count / total_candles) > 0.7 if total_candles > 0 else False

            details = {
                'total_candles': total_candles,
                'vwap_respect_count': vwap_respect_count,
                'vwap_violation_count': vwap_violation_count,
                'strict_mode': VWAP_STRICT_MODE,
                'passed': passed
            }

            logger.debug(f"VWAP confirmation: respect={vwap_respect_count}/{total_candles}, passed={passed}")

            return passed, details

        except Exception as e:
            logger.error(f"Error in VWAP confirmation: {str(e)}")
            return False, {'error': str(e)}

    # ==================== 8. LIQUIDITY FILTER ====================

    def check_liquidity(self, stock_info):
        """
        Check if stock meets minimum liquidity requirements

        Args:
            stock_info: dict with avg_volume, avg_turnover, price

        Returns:
            (bool, dict): (passed, details)
        """
        try:
            avg_volume = stock_info.get('avg_volume', 0)
            avg_turnover = stock_info.get('avg_turnover', 0)
            price = stock_info.get('price', 0)

            volume_ok = avg_volume >= MIN_AVG_DAILY_VOLUME
            turnover_ok = avg_turnover >= MIN_AVG_DAILY_TURNOVER
            price_ok = MIN_PRICE <= price <= MAX_PRICE

            passed = volume_ok and turnover_ok and price_ok

            details = {
                'avg_volume': avg_volume,
                'min_volume': MIN_AVG_DAILY_VOLUME,
                'volume_ok': volume_ok,
                'avg_turnover': avg_turnover,
                'min_turnover': MIN_AVG_DAILY_TURNOVER,
                'turnover_ok': turnover_ok,
                'price': price,
                'price_range': f"{MIN_PRICE}-{MAX_PRICE}",
                'price_ok': price_ok,
                'passed': passed
            }

            logger.debug(f"Liquidity check: vol={volume_ok}, turnover={turnover_ok}, price={price_ok}, passed={passed}")

            return passed, details

        except Exception as e:
            logger.error(f"Error in liquidity check: {str(e)}")
            return False, {'error': str(e)}

    # ==================== FULL STRATEGY VALIDATION ====================

    def validate_stock(self, symbol, candles_df, historical_data, stock_info):
        """
        Run complete strategy validation on a stock

        Args:
            symbol: Stock symbol
            candles_df: Today's 5-min candle data
            historical_data: Last 15 days daily data
            stock_info: Stock metadata (avg_volume, turnover, price, etc.)

        Returns:
            dict: Validation results with signal, strength, and all checks
        """
        try:
            logger.info(f"Validating {symbol}...")

            result = {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'signal': None,
                'signal_strength': 0,
                'checks': {},
                'passed': False
            }

            # Minimum candles needed
            if len(candles_df) < 8:
                result['error'] = 'Not enough candles yet (need at least 8)'
                return result

            # ==== CHECK 1: Liquidity ====
            liquidity_passed, liquidity_details = self.check_liquidity(stock_info)
            result['checks']['liquidity'] = liquidity_details
            if not liquidity_passed:
                logger.debug(f"{symbol}: Failed liquidity filter")
                return result

            # ==== CHECK 2: Gap ====
            prev_day_close = historical_data.iloc[-1]['close']
            today_open = candles_df.iloc[0]['open']
            gap_passed, gap_percent, gap_details = self.check_gap(prev_day_close, today_open)
            result['checks']['gap'] = gap_details
            if not gap_passed:
                logger.debug(f"{symbol}: Failed gap filter ({gap_percent:.2f}%)")
                return result

            # ==== CHECK 3: First Candle Move ====
            first_candle_passed, first_move, first_details = self.check_first_candle_move(candles_df.iloc[0])
            result['checks']['first_candle'] = first_details
            if not first_candle_passed:
                logger.debug(f"{symbol}: Failed first candle filter ({first_move:.2f}%)")
                return result

            # ==== CHECK 4: 3-Candle Pattern ====
            signal_type, pattern_details = self.check_three_candle_pattern(candles_df)
            result['checks']['pattern'] = pattern_details
            if signal_type is None:
                logger.debug(f"{symbol}: No valid 3-candle pattern")
                return result

            result['signal'] = signal_type

            # ==== CHECK 5: Relative Volume ====
            current_volume = candles_df['volume'].sum()
            volume_passed, volume_ratio, volume_details = self.check_relative_volume(current_volume, historical_data)
            result['checks']['volume'] = volume_details
            if not volume_passed:
                logger.debug(f"{symbol}: Failed volume filter (ratio={volume_ratio:.2f})")
                return result

            # ==== CHECK 6: Momentum Continuation ====
            momentum_passed, momentum_details = self.check_momentum_continuation(candles_df, signal_type)
            result['checks']['momentum'] = momentum_details
            if not momentum_passed:
                logger.debug(f"{symbol}: Failed momentum continuation")
                return result

            # ==== CHECK 7: Pullback Validation ====
            pullback_passed, pullback_details = self.check_pullback_validity(candles_df, signal_type)
            result['checks']['pullback'] = pullback_details
            if not pullback_passed:
                logger.debug(f"{symbol}: Failed pullback validation")
                return result

            # ==== CHECK 8: VWAP Confirmation ====
            vwap_passed, vwap_details = self.check_vwap_confirmation(candles_df, signal_type)
            result['checks']['vwap'] = vwap_details
            if not vwap_passed:
                logger.debug(f"{symbol}: Failed VWAP confirmation")
                return result

            # ==== ALL CHECKS PASSED! ====
            result['passed'] = True

            # Calculate signal strength (0-10)
            strength = 0
            strength += 2 if volume_ratio > 1.5 else 1  # Volume strength
            strength += 2 if gap_percent < 0.2 else 1   # Gap quality
            strength += 2 if vwap_details['vwap_violation_count'] == 0 else 1  # VWAP respect
            strength += 2 if pullback_details['pullback_count'] == 0 else 1  # Clean move
            strength += 2 if momentum_details['dominant_count'] >= 4 else 1  # Momentum strength

            result['signal_strength'] = min(strength, 10)

            logger.info(f"✅ {symbol}: {signal_type} signal with strength {result['signal_strength']}/10")

            return result

        except Exception as e:
            logger.error(f"Error validating {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'error': str(e),
                'passed': False
            }


# ==================== HELPER FUNCTIONS ====================

def calculate_vwap(candles_df):
    """Calculate VWAP for candles"""
    try:
        typical_price = (candles_df['high'] + candles_df['low'] + candles_df['close']) / 3
        vwap = (typical_price * candles_df['volume']).cumsum() / candles_df['volume'].cumsum()
        return vwap
    except Exception as e:
        logger.error(f"Error calculating VWAP: {str(e)}")
        return pd.Series([0] * len(candles_df))


def calculate_atr(candles_df, period=14):
    """Calculate ATR for stop-loss calculation"""
    try:
        high_low = candles_df['high'] - candles_df['low']
        high_close = abs(candles_df['high'] - candles_df['close'].shift())
        low_close = abs(candles_df['low'] - candles_df['close'].shift())

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(period).mean()

        return atr.iloc[-1] if len(atr) > 0 else 0
    except Exception as e:
        logger.error(f"Error calculating ATR: {str(e)}")
        return 0


if __name__ == "__main__":
    # Test validator
    print("Strategy Validator Module Loaded")
    validator = MomentumStrategyValidator()
    print(f"✅ {validator.name} initialized")
