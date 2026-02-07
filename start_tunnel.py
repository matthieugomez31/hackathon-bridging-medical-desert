import sys
import time
from pyngrok import ngrok, conf

# ==========================================
# 🔑 CONFIGURATION
# ==========================================
# Paste your token inside the quotes (starts with "2...")
NGROK_AUTH_TOKEN = "39MU9pzbHVguROroIp8U9sXml1m_2MdzwJAQNCNFN9sy6yDU1"
PORT = 8000
# ==========================================

def start_tunnel():
    """
    Automatically installs and launches a secure tunnel to your local API.
    """
    print("🚀 Initializing Tunnel Sequence...")

    # 1. Check Token
    if "COLLE_TON_TOKEN" in NGROK_AUTH_TOKEN:
        print("\n❌ ERROR: You must paste your Ngrok Token in start_tunnel.py (Line 9)")
        print("👉 Get it here: https://dashboard.ngrok.com/get-started/your-authtoken")
        sys.exit(1)

    # 2. Authenticate
    # Pyngrok manages the binary installation automatically
    try:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    except Exception as e:
        print(f"⚠️ Auth Warning: {e}")

    # 3. Open Tunnel
    print(f"🔌 Connecting to port {PORT}...")
    try:
        # Force HTTP protocol to avoid browser warning complications if possible
        public_url = ngrok.connect(PORT, "http").public_url
        
        print("\n" + "="*60)
        print(f"✅ TUNNEL IS ONLINE! (Managed by Python)")
        print(f"🔗 SEND THIS URL TO FRANÇOIS:")
        print(f"   {public_url}/analyze")
        print("="*60 + "\n")
        print("⛔ DO NOT CLOSE THIS WINDOW. Press CTRL+C to stop.")

        # Keep the script running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down tunnel...")
        ngrok.kill()
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("💡 Tip: Make sure your API server is running in another terminal!")

if __name__ == "__main__":
    start_tunnel()