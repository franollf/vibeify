# spotify_auth.py
import os
import requests
import urllib.parse
import base64
import webbrowser
from dotenv import load_dotenv

# ======================
# Load environment variables
# ======================
load_dotenv()  # Make sure your .env file is in the same directory

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# ======================
# Safety check
# ======================
if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
    print("❌ Missing environment variables. Check your .env file!")
    print("CLIENT_ID:", CLIENT_ID)
    print("CLIENT_SECRET:", "Loaded" if CLIENT_SECRET else None)
    print("REDIRECT_URI:", REDIRECT_URI)
    exit(1)

# ======================
# Step 1: Direct user to Spotify authorization URL
# ======================
SCOPE = "playlist-modify-private user-read-private"

auth_url = (
    "https://accounts.spotify.com/authorize?"
    f"client_id={CLIENT_ID}"
    f"&response_type=code"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&scope={urllib.parse.quote(SCOPE)}"
)

print("Go to this URL to authorize the app:")
print(auth_url)
webbrowser.open(auth_url)

# ======================
# Step 2: User enters the authorization code
# ======================
auth_code = input("\nEnter the authorization code from the URL after approval: ").strip()

# ======================
# Step 3: Exchange authorization code for access & refresh tokens
# ======================
token_url = "https://accounts.spotify.com/api/token"
data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI
}

# Spotify requires Base64 encoded client_id:client_secret in Authorization header
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
headers = {"Authorization": f"Basic {auth_header}"}

response = requests.post(token_url, data=data, headers=headers)

if response.status_code == 200:
    tokens = response.json()
    print("\n✅ Access Token:", tokens["access_token"])
    print("🔄 Refresh Token:", tokens["refresh_token"])
    print("ℹ️ Use these tokens in your scripts to authenticate Spotify API calls.")
else:
    print("\n❌ Failed to get tokens.")
    print("Status code:", response.status_code)
    print("Response:", response.text)
