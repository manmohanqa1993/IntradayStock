"""
Kite Connect Login Helper
Generates access token for Kite API
Run this ONCE to get your access token
"""

from kiteconnect import KiteConnect
import logging

# Your API credentials from https://developers.kite.trade/
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"

# Initialize logger
logging.basicConfig(level=logging.DEBUG)

# Initialize Kite Connect
kite = KiteConnect(api_key=API_KEY)

# Step 1: Get login URL
print("\n" + "="*80)
print("KITE CONNECT LOGIN - STEP-BY-STEP GUIDE")
print("="*80 + "\n")

login_url = kite.login_url()
print("Step 1: Open this URL in your browser:")
print(f"\n{login_url}\n")

print("Step 2: Login with your Zerodha credentials")
print("Step 3: After login, you'll be redirected to a URL like:")
print("        http://127.0.0.1/?request_token=XXXXXX&action=login&status=success")
print("\nStep 4: Copy the 'request_token' from the URL")

# Get request token from user
request_token = input("\nPaste your request_token here: ").strip()

try:
    # Step 2: Generate access token
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]

    print("\n" + "="*80)
    print("✅ SUCCESS! Your access token has been generated:")
    print("="*80)
    print(f"\nACCESS_TOKEN = \"{access_token}\"")
    print("\n" + "="*80)

    # Save to file
    with open("kite_credentials.txt", "w") as f:
        f.write(f"API_KEY = \"{API_KEY}\"\n")
        f.write(f"API_SECRET = \"{API_SECRET}\"\n")
        f.write(f"ACCESS_TOKEN = \"{access_token}\"\n")

    print("\n✅ Credentials saved to: kite_credentials.txt")
    print("\nNow update these values in 'intraday_scanner_kite.py':")
    print(f"   API_KEY = \"{API_KEY}\"")
    print(f"   API_SECRET = \"{API_SECRET}\"")
    print(f"   ACCESS_TOKEN = \"{access_token}\"")

    print("\n⚠️  IMPORTANT:")
    print("   - Access token expires daily at 6:00 AM")
    print("   - Re-run this script each day to get a fresh token")
    print("   - Keep your credentials secure and never share them")
    print("\n" + "="*80 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure API_KEY and API_SECRET are correct")
    print("2. Check if request_token is valid (it expires in 2-3 minutes)")
    print("3. Ensure you have an active Zerodha trading account")
    print("4. Visit https://developers.kite.trade/ for API setup\n")
