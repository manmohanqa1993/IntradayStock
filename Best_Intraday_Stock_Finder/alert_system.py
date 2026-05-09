"""
Alert System - Multi-channel Notifications
==========================================
Sends alerts via Console, Sound, and Telegram
"""

import logging
from datetime import datetime
import requests

from config import *

logger = logging.getLogger(__name__)


class AlertSystem:
    """
    Multi-channel alert system for trading signals
    """

    def __init__(self):
        self.telegram_enabled = ENABLE_TELEGRAM and TELEGRAM_BOT_TOKEN != 'your_telegram_bot_token'
        self.sound_enabled = ENABLE_SOUND_ALERTS
        self.console_enabled = ENABLE_CONSOLE_ALERTS

        if self.telegram_enabled:
            logger.info("✅ Telegram alerts enabled")
        if self.sound_enabled:
            logger.info("✅ Sound alerts enabled")
        if self.console_enabled:
            logger.info("✅ Console alerts enabled")

    def send_alert(self, signal):
        """
        Send alert for new signal

        Args:
            signal: Signal dict with all details
        """
        try:
            # Console alert
            if self.console_enabled:
                self._console_alert(signal)

            # Sound alert
            if self.sound_enabled:
                self._sound_alert(signal)

            # Telegram alert
            if self.telegram_enabled:
                self._telegram_alert(signal)

        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")

    def _console_alert(self, signal):
        """Print alert to console"""
        symbol = signal['symbol']
        signal_type = signal['signal']
        strength = signal['signal_strength']
        entry = signal.get('entry_price', 'N/A')
        sl = signal.get('stop_loss', 'N/A')
        target = signal.get('target_price', 'N/A')

        alert_msg = f"\n🔔 ALERT: {symbol} - {signal_type} SIGNAL (Strength: {strength}/10)"
        alert_msg += f"\n   Entry: ₹{entry} | SL: ₹{sl} | Target: ₹{target}"

        print(alert_msg)

    def _sound_alert(self, signal):
        """Play sound alert"""
        try:
            # For Windows
            try:
                import winsound
                # Different beeps for bullish vs bearish
                if signal['signal'] == 'BULLISH':
                    # Higher pitch for bullish
                    winsound.Beep(1500, 400)
                else:
                    # Lower pitch for bearish
                    winsound.Beep(800, 400)

            except ImportError:
                # For Linux/Mac - use alternative
                import os
                os.system('play -nq -t alsa synth 0.5 sine 1000')

        except Exception as e:
            logger.debug(f"Sound alert not available: {str(e)}")

    def _telegram_alert(self, signal):
        """Send Telegram message"""
        try:
            # Format message
            message = self._format_telegram_message(signal)

            # Send via Telegram Bot API
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }

            response = requests.post(url, data=payload, timeout=10)

            if response.status_code == 200:
                logger.debug(f"Telegram alert sent for {signal['symbol']}")
            else:
                logger.warning(f"Telegram alert failed: {response.status_code}")

        except Exception as e:
            logger.error(f"Error sending Telegram alert: {str(e)}")

    def _format_telegram_message(self, signal):
        """Format signal as Telegram message"""
        symbol = signal['symbol']
        signal_type = signal['signal']
        strength = signal['signal_strength']

        # Emoji based on signal type
        emoji = "📈" if signal_type == "BULLISH" else "📉"

        # Build message
        msg = f"{emoji} <b>{signal_type} SIGNAL</b>\n\n"
        msg += f"📊 <b>Symbol:</b> {symbol}\n"
        msg += f"⭐ <b>Strength:</b> {strength}/10\n\n"

        msg += f"💰 <b>Trade Setup:</b>\n"
        msg += f"  • Entry: ₹{signal.get('entry_price', 'N/A')}\n"
        msg += f"  • Stop Loss: ₹{signal.get('stop_loss', 'N/A')}\n"
        msg += f"  • Target: ₹{signal.get('target_price', 'N/A')}\n"
        msg += f"  • R:R Ratio: 1:{signal.get('risk_reward_ratio', 'N/A')}\n\n"

        msg += f"📊 <b>Signal Details:</b>\n"

        # Volume
        vol_ratio = signal['checks']['volume'].get('volume_ratio', 'N/A')
        msg += f"  • Volume: {vol_ratio}x average\n"

        # Gap
        gap = signal['checks']['gap'].get('gap_percent', 'N/A')
        msg += f"  • Gap: {gap}%\n"

        # Pattern
        pattern = signal['checks']['pattern'].get('pattern', 'N/A')
        msg += f"  • Pattern: {pattern}\n"

        # VWAP
        vwap_respect = signal['checks']['vwap'].get('vwap_respect_count', 'N/A')
        vwap_total = signal['checks']['vwap'].get('total_candles', 'N/A')
        msg += f"  • VWAP Respect: {vwap_respect}/{vwap_total} candles\n"

        msg += f"\n⏰ <b>Time:</b> {signal['timestamp'].strftime('%H:%M:%S')}\n"

        msg += f"\n⚠️ <i>Trade at your own risk</i>"

        return msg


# ==================== STANDALONE TELEGRAM TEST ====================

def test_telegram_connection():
    """Test Telegram bot connection"""
    print("\n" + "="*60)
    print("Testing Telegram Connection")
    print("="*60 + "\n")

    if TELEGRAM_BOT_TOKEN == 'your_telegram_bot_token':
        print("❌ Telegram bot token not configured")
        print("Please update TELEGRAM_BOT_TOKEN in config.py\n")
        return False

    if TELEGRAM_CHAT_ID == 'your_telegram_chat_id':
        print("❌ Telegram chat ID not configured")
        print("Please update TELEGRAM_CHAT_ID in config.py\n")
        return False

    try:
        # Send test message
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        test_message = "🧪 Test message from Best Intraday Stock Finder\n\nIf you see this, Telegram alerts are working! ✅"

        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': test_message
        }

        response = requests.post(url, data=payload, timeout=10)

        if response.status_code == 200:
            print("✅ Telegram connection successful!")
            print(f"Test message sent to chat ID: {TELEGRAM_CHAT_ID}\n")
            return True
        else:
            print(f"❌ Telegram connection failed: HTTP {response.status_code}")
            print(f"Response: {response.text}\n")
            return False

    except Exception as e:
        print(f"❌ Error testing Telegram: {str(e)}\n")
        return False


if __name__ == "__main__":
    # Test alerts
    print("Alert System Module Loaded")

    # Test Telegram if enabled
    if ENABLE_TELEGRAM:
        test_telegram_connection()

    # Test sound alert
    if ENABLE_SOUND_ALERTS:
        print("Testing sound alert...")
        alert_sys = AlertSystem()
        try:
            alert_sys._sound_alert({'signal': 'BULLISH'})
            print("✅ Sound alert test complete\n")
        except Exception as e:
            print(f"⚠️  Sound alert not available: {str(e)}\n")
