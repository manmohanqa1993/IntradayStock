"""
Upstox Login Script - Generate Access Token
Run this ONCE to get your access token for the day
"""

import upstox_client
import webbrowser

# ==================== YOUR CREDENTIALS ====================
# Get these from https://account.upstox.com/developer/apps

API_KEY = "your_api_key_here"          # Your API Key from Upstox Developer Console
API_SECRET = "your_api_secret_here"    # Your API Secret
REDIRECT_URI = "http://127.0.0.1:5000" # Must match what you set in Upstox app

# ==================== LOGIN FLOW ====================

def generate_access_token():
    """Generate Upstox access token"""

    print("\n" + "="*70)
    print("UPSTOX API LOGIN - ACCESS TOKEN GENERATOR")
    print("="*70 + "\n")

    # Step 1: Generate login URL
    session = upstox_client.SessionApi()

    login_url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"

    print("Step 1: Opening Upstox login page in browser...")
    print(f"\nLogin URL: {login_url}\n")

    # Open browser
    webbrowser.open(login_url)

    print("="*70)
    print("INSTRUCTIONS:")
    print("="*70)
    print("1. Browser will open with Upstox login page")
    print("2. Login with your Upstox credentials")
    print("3. Click 'Authorize' to grant access")
    print("4. You'll be redirected to a URL like:")
    print("   http://127.0.0.1:5000/?code=XXXXXX")
    print("5. Copy the 'code' parameter from that URL")
    print("="*70 + "\n")

    # Step 2: Get authorization code
    auth_code = input("Enter the 'code' from redirected URL: ").strip()

    # Step 3: Generate access token
    print("\nGenerating access token...")

    try:
        configuration = upstox_client.Configuration()
        api_instance = upstox_client.LoginApi(upstox_client.ApiClient(configuration))

        api_response = api_instance.token(
            grant_type='authorization_code',
            code=auth_code,
            client_id=API_KEY,
            client_secret=API_SECRET,
            redirect_uri=REDIRECT_URI
        )

        access_token = api_response.access_token

        print("\n" + "="*70)
        print("✅ SUCCESS! Your Access Token:")
        print("="*70)
        print(f"\n{access_token}\n")
        print("="*70)

        print("\n📋 NEXT STEPS:")
        print("="*70)
        print("1. Copy the access token above")
        print("2. Open 'intraday_scanner_upstox.py'")
        print("3. Update this line:")
        print(f"   ACCESS_TOKEN = '{access_token}'")
        print("4. Run: python intraday_scanner_upstox.py")
        print("="*70)

        print("\n⏰ IMPORTANT:")
        print("- This token expires at end of day")
        print("- Re-run this script tomorrow for new token")
        print("- Keep token secure (don't share)\n")

        # Save to file for convenience
        with open('upstox_token.txt', 'w') as f:
            f.write(f"# Upstox Access Token - Generated: {__import__('datetime').datetime.now()}\n")
            f.write(f"# Valid until: End of trading day\n\n")
            f.write(f"ACCESS_TOKEN = '{access_token}'\n")

        print("✅ Token saved to 'upstox_token.txt'\n")

        return access_token

    except upstox_client.ApiException as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("- Check if API_KEY and API_SECRET are correct")
        print("- Verify REDIRECT_URI matches Upstox app settings")
        print("- Make sure authorization code is fresh (expires in 5 min)")
        return None

# ==================== MAIN ====================

if __name__ == "__main__":
    if API_KEY == "your_api_key_here" or API_SECRET == "your_api_secret_here":
        print("\n❌ ERROR: Please update API_KEY and API_SECRET first!\n")
        print("Get them from: https://account.upstox.com/developer/apps\n")
        exit(1)

    generate_access_token()
