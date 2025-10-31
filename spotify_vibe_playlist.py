# vibe_finder_test.py
import requests
import json
import urllib.parse

# ======================
# CONFIGURATION
# ======================
# ⚠️ Paste your short-lived access token here (from your auth script)
ACCESS_TOKEN = "BQArgz42io1vwEzvX6LG6Cct0VlKGXiT1xygZIElJhOGRiWKyJn-pSIScjaW-_T-bQfDjyI5qCdCZlcd-ovp53AinFlhU9i9MrFqQhghByZ9nKy7T8-atn2_ceYXAXfwH8xn-fsyN47n-UU6yy7F_f8z-ErXkEO_7PFs_CM0Oj_4IouEhVBSTZ6n4uuZhBs6qc6sDjtQwB6YQnbVKFbCKNCHlTToZX5rhNyc7P8d9MFNJFoFUAQxX-MAuPEzgFIYQfD57NGg08xnVuSGwYkuuY46nTF6"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

# Map vibes to artist genres
VIBE_GENRES = {
    "Soft": ["acoustic", "folk", "lofi", "ambient", "piano", "chill"],
    "Chill": ["chill", "ambient", "lofi", "downtempo", "soft", "acoustic"],
    "Hype": ["hip hop", "rap", "trap", "edm", "pop", "dance"]
}

# ======================
# SPOTIFY HELPERS
# ======================
def get_user_id():
    r = requests.get("https://api.spotify.com/v1/me", headers=HEADERS)
    if r.status_code == 200:
        return r.json()["id"]
    print("⚠️ Could not get user ID:", r.text)
    return None

def search_tracks(keyword, limit=50):
    tracks = []
    url = f"https://api.spotify.com/v1/search?q={urllib.parse.quote(keyword)}&type=track&limit={limit}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        items = r.json().get("tracks", {}).get("items", [])
        tracks.extend(items)
    else:
        print("⚠️ Search failed:", r.text)
    return tracks

def get_artist_genres(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("genres", [])
    return []

def filter_tracks_by_genres(tracks, vibe_name):
    """Filter tracks by artist genres for the selected vibe"""
    if not vibe_name or vibe_name not in VIBE_GENRES:
        return tracks  # No vibe filtering

    vibe_keywords = VIBE_GENRES[vibe_name]
    filtered_tracks = []

    for t in tracks:
        artist = t["artists"][0]
        artist_genres = get_artist_genres(artist["id"])
        if any(v.lower() in g.lower() for g in vibe_keywords for g in artist_genres):
            filtered_tracks.append(t)

    return filtered_tracks

def create_playlist(user_id, name):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    data = {"name": name, "description": "Auto-generated playlist", "public": False}
    r = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if r.status_code == 201:
        return r.json()["id"]
    print("⚠️ Failed to create playlist:", r.text)
    return None

def add_tracks_to_playlist(playlist_id, uris):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    data = {"uris": uris}
    r = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if r.status_code in [200, 201]:
        print(f"✅ Added {len(uris)} tracks to playlist!")
    else:
        print("⚠️ Failed to add tracks:", r.text)

# ======================
# MAIN
# ======================
def main():
    keyword = input("Enter a search keyword (e.g., 'cleaning', 'relaxing'): ").strip()
    vibe_choice = input("Optional vibe (Soft, Chill, Hype): ").strip()

    user_id = get_user_id()
    if not user_id:
        return

    print(f"🎧 Searching for tracks with keyword '{keyword}'...")
    tracks = search_tracks(keyword)
    if not tracks:
        print("😔 No tracks found for that keyword.")
        return

    # Filter tracks by artist genres based on vibe
    tracks = filter_tracks_by_genres(tracks, vibe_choice)
    if not tracks:
        print(f"😔 No tracks matched your vibe '{vibe_choice}'.")
        return

    vibe_tracks = [f"{t['name']} - {t['artists'][0]['name']}" for t in tracks]
    vibe_uris = [t["uri"] for t in tracks]

    playlist_name = input("Name Your Playlist: ").strip()
    playlist_id = create_playlist(user_id, playlist_name)
    if not playlist_id:
        return

    add_tracks_to_playlist(playlist_id, vibe_uris)
    print(f"🎶 Playlist '{playlist_name}' created with {len(vibe_tracks)} tracks!")

if __name__ == "__main__":
    main()
