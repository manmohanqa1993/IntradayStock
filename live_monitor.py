"""
Live Market Monitor - Runs continuously during market hours
Scans every 15 minutes and alerts on new opportunities
"""

import time
from datetime import datetime, time as dt_time
from intraday_scanner import scan_market

def is_market_hours():
    """Check if current time is during NSE market hours (9:15 AM - 3:30 PM IST)"""
    now = datetime.now()
    current_time = now.time()

    # NSE market hours
    market_open = dt_time(9, 15)
    market_close = dt_time(15, 30)

    # Check if weekday (Monday=0, Sunday=6)
    is_weekday = now.weekday() < 5

    return is_weekday and market_open <= current_time <= market_close

def live_monitor(interval_minutes=15):
    """
    Monitor market continuously during trading hours

    Args:
        interval_minutes: How often to scan (default: 15 minutes)
    """
    print("\n" + "="*100)
    print("🔴 LIVE MARKET MONITOR - STARTED")
    print("="*100)
    print(f"Scan Interval: Every {interval_minutes} minutes")
    print(f"Market Hours: 9:15 AM - 3:30 PM IST (Mon-Fri)")
    print("="*100 + "\n")

    scan_count = 0

    while True:
        if is_market_hours():
            scan_count += 1
            print(f"\n🔄 Scan #{scan_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            try:
                scan_market()
            except Exception as e:
                print(f"❌ Error during scan: {e}")

            print(f"\n⏳ Next scan in {interval_minutes} minutes...")
            print("-" * 100)

            time.sleep(interval_minutes * 60)
        else:
            now = datetime.now()
            print(f"\n⏸️  Market closed. Current time: {now.strftime('%H:%M:%S')}")

            if now.weekday() >= 5:
                print("   It's weekend. Market opens Monday 9:15 AM.")
            else:
                print("   Market hours: 9:15 AM - 3:30 PM IST")

            print("   Checking again in 5 minutes...")
            time.sleep(300)  # Check every 5 minutes when market is closed

if __name__ == "__main__":
    try:
        live_monitor(interval_minutes=15)
    except KeyboardInterrupt:
        print("\n\n⏹️  Live monitor stopped by user.")
        print("="*100 + "\n")
