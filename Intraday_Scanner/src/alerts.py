"""
Alert System - Simple Alerts
=============================
Console and sound alerts for beginners
"""

import sys


class AlertSystem:
    """Simple alert system"""

    def __init__(self):
        self.alert_count = 0

    def send_signal_alert(self, signal):
        """Send alert for new signal"""
        try:
            self.alert_count += 1

            # Sound alert (simple beep)
            try:
                import winsound
                winsound.Beep(1000, 200)  # 1000 Hz for 200ms
            except:
                print('\a')  # Terminal beep

            return True

        except Exception as e:
            print(f"Alert error: {e}")
            return False


if __name__ == "__main__":
    alert = AlertSystem()
    signal = {'symbol': 'TEST', 'signal_type': 'BULLISH'}
    alert.send_signal_alert(signal)
    print("✅ Alert test complete")
