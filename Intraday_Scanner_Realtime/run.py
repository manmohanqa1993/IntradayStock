"""
Intraday Scanner Realtime - Multi-Broker Version
================================================
Real-time data from multiple brokers
Supports: Zerodha, Angel One, Upstox, Fyers, FREE (Hybrid)
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from scanner import IntradayScanner

def main():
    """Main entry point"""
    print("="*60)
    print(" INTRADAY SCANNER REALTIME")
    print(" Multi-Broker Support")
    print("="*60)
    print()

    scanner = IntradayScanner()
    scanner.start()

if __name__ == "__main__":
    main()
