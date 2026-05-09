"""
Strategy Validator - Simplified 5-Point Strategy
=================================================
Beginner-friendly momentum strategy
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
from settings import *


class StrategyValidator:
    """Simplified 5-point momentum strategy"""

    def validate(self, symbol, candles_df, hist_df):
        """
        Validate stock against 5-point strategy

        Returns: dict with signal info or None
        """
        if candles_df is None or len(candles_df) < 10:
            return None

        if hist_df is None or len(hist_df) < 5:
            return None

        result = {
            'symbol': symbol,
            'is_valid': False,
            'signal_type': None,
            'strength': 0,
            'conditions_met': []
        }

        # Check each condition
        checks = [
            self._check_volume(candles_df, hist_df),
            self._check_gap(candles_df, hist_df),
            self._check_pattern(candles_df),
            self._check_momentum(candles_df),
            self._check_vwap(candles_df)
        ]

        # Count passed checks
        passed = sum(1 for check in checks if check[0])
        total = len(checks)

        # Determine signal type from pattern check
        signal_type = checks[2][1]  # Pattern check returns signal type

        if signal_type and passed >= 4:  # Need 4 out of 5 conditions
            result['is_valid'] = True
            result['signal_type'] = signal_type
            result['strength'] = int((passed / total) * 10)
            result['conditions_met'] = [name for passed, name, _ in checks if passed]

        return result if result['is_valid'] else None

    def _check_volume(self, candles_df, hist_df):
        """Check if volume is above average"""
        try:
            current_volume = candles_df['volume'].sum()
            avg_volume = hist_df['volume'].mean()

            if current_volume > avg_volume * MIN_VOLUME_RATIO:
                return (True, "Volume", "Above average")
            return (False, "Volume", "Below average")

        except:
            return (False, "Volume", "Error")

    def _check_gap(self, candles_df, hist_df):
        """Check gap is not too large"""
        try:
            prev_close = hist_df['close'].iloc[-1]
            today_open = candles_df['open'].iloc[0]

            gap_pct = abs((today_open - prev_close) / prev_close * 100)

            if gap_pct < MAX_GAP_PERCENT:
                return (True, "Gap", f"{gap_pct:.2f}%")
            return (False, "Gap", f"Too large: {gap_pct:.2f}%")

        except:
            return (False, "Gap", "Error")

    def _check_pattern(self, candles_df):
        """Check 3-candle reversal pattern"""
        try:
            if len(candles_df) < 3:
                return (False, "Pattern", "Not enough candles", None)

            # Get first 3 candles
            first_3 = candles_df.head(3)

            # Check colors
            colors = ['green' if row['close'] > row['open'] else 'red'
                     for _, row in first_3.iterrows()]

            # Bullish: Red → Green → Green
            if colors == ['red', 'green', 'green']:
                return (True, "Pattern", "Bullish reversal", "BULLISH")

            # Bearish: Green → Red → Red
            elif colors == ['green', 'red', 'red']:
                return (True, "Pattern", "Bearish reversal", "BEARISH")

            return (False, "Pattern", "No pattern", None)

        except:
            return (False, "Pattern", "Error", None)

    def _check_momentum(self, candles_df):
        """Check momentum continuation"""
        try:
            if len(candles_df) < 8:
                return (False, "Momentum", "Not enough candles")

            # Check candles 4-8
            momentum_candles = candles_df.iloc[3:8]

            # Count directional candles
            bullish_count = sum(1 for _, row in momentum_candles.iterrows()
                              if row['close'] > row['open'])
            bearish_count = len(momentum_candles) - bullish_count

            if bullish_count >= MIN_MOMENTUM_CANDLES:
                return (True, "Momentum", f"Bullish: {bullish_count}/5")
            elif bearish_count >= MIN_MOMENTUM_CANDLES:
                return (True, "Momentum", f"Bearish: {bearish_count}/5")

            return (False, "Momentum", "Weak")

        except:
            return (False, "Momentum", "Error")

    def _check_vwap(self, candles_df):
        """Check VWAP confirmation"""
        try:
            # Check last 5 candles respect VWAP
            last_5 = candles_df.tail(5)

            bullish_vwap = sum(1 for _, row in last_5.iterrows()
                              if row['close'] > row['vwap'])
            bearish_vwap = sum(1 for _, row in last_5.iterrows()
                              if row['close'] < row['vwap'])

            if bullish_vwap >= 4:
                return (True, "VWAP", "Above VWAP")
            elif bearish_vwap >= 4:
                return (True, "VWAP", "Below VWAP")

            return (False, "VWAP", "Mixed")

        except:
            return (False, "VWAP", "Error")


if __name__ == "__main__":
    print("Strategy Validator - Simplified 5-Point")
    print("Conditions:")
    print("1. Volume > Average")
    print("2. Gap < 0.5%")
    print("3. 3-Candle Pattern")
    print("4. Momentum (3/5 candles)")
    print("5. VWAP Confirmation")
