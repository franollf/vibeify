# spotify.py
import requests
import os

SPOTIFY_CLIENT_ID = os.getenv("f0d66f5bf6c344e1b2e395c924d15a4a")
SPOTIFY_CLIENT_SECRET = os.getenv("42f9c3a0a72f4cff998f658d31c19009")

def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
    response.raise_for_status()
    return response.json()["access_token"]

def get_audio_features(track_ids):
    token = get_spotify_token()
    url = "https://api.spotify.com/v1/audio-features"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"ids": ",".join(track_ids)}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["audio_features"]
