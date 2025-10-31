import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_access_token():
    """Get Spotify API token via Client Credentials flow."""
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()  # will raise if auth fails
    return response.json()["access_token"]

def get_audio_features(track_id: str):
    """Fetch Spotify audio features for a track."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # will raise if token invalid
    return response.json()

def get_track_info(track_id: str):
    """Fetch Spotify track information."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # will raise if token invalid
    return response.json()


print(get_access_token())


### BQCWZRCA5AuiarRR7A4RPV6Bm_CFS1opBuoHXnJVi_Vvoxi62OfJq2RMn8Xd4GszofwgR2_tA2s3y3OgRs5LvMcDKa3QnA6pVaPJ30P6hqJVN8PRsCCJFh_uVOBlHubOn-ZWI8itSMQ
