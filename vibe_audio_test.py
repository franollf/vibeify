# song_features_test.py
import requests
import urllib.parse
import random
import json
import psycopg2

# ======================
# CONFIGURATION
# ======================
ACCESS_TOKEN = "BQC_VOhLN4sXf4WR61sCcY2GFOUG4BhSqc0THs7VbEkZILKkubgy6rRgVDFBG570sEQEpMswoZPfCkkPusdZMjVwwXJUrjPc0dHkwV8f0z9QacYXtc9kzbM4p3xZKZAJNHIZbCu3kYpEspdoRSIZzBa44GHY9E5EIxUic0DUBpWFuh5nDlBCPOgiI2MuZvTMQqc1BxmjjpG_8BFQVKhygME5eeWMEOncqNRwmGRhQI1wCGGoNQ8qhUvE0JTZ3OJOWwN9O4sKdZY82bAqbZN4_J2GgE9m"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

DB_CONFIG = {
    "dbname": "vibewave",
    "user": "franollf",
    "password": "",  # add if needed
    "host": "localhost",
    "port": 5432
}

# ======================
# DATABASE FUNCTIONS
# ======================
def save_playlist_to_db(user_id, playlist_name, playlist_id):
    """Save created playlist info to PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Create table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id SERIAL PRIMARY KEY,
                user_id TEXT,
                playlist_name TEXT,
                playlist_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert playlist record
        cur.execute("""
            INSERT INTO playlists (user_id, playlist_name, playlist_id)
            VALUES (%s, %s, %s)
        """, (user_id, playlist_name, playlist_id))

        conn.commit()
        cur.close()
        conn.close()
        print(f"💾 Playlist '{playlist_name}' saved to database!")
    except Exception as e:
        print("⚠️ Database error:", e)

# ======================
# SPOTIFY HELPERS
# ======================
def get_user_id():
    r = requests.get("https://api.spotify.com/v1/me", headers=HEADERS)
    if r.status_code == 200:
        return r.json()["id"]
    print("⚠️ Could not get user ID:", r.text)
    return None

def search_artists_by_keyword(keyword, limit=5):
    q = urllib.parse.quote(keyword)
    url = f"https://api.spotify.com/v1/search?q={q}&type=artist&limit={limit}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("artists", {}).get("items", [])
    print("⚠️ Artist search failed:", r.text)
    return []

def get_top_tracks_for_artist(artist_id, market="US"):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market={market}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("tracks", [])
    return []

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
    concept = input("Enter a mood/concept (e.g., 'relaxing', 'study'): ").strip().lower()
    user_id = get_user_id()
    if not user_id:
        return

    artists = search_artists_by_keyword(concept, limit=10)
    if not artists:
        print("😔 No artists found for that concept.")
        return

    all_tracks = []
    for artist in artists:
        tracks = get_top_tracks_for_artist(artist["id"])
        tracks = [t for t in tracks if concept.lower() not in t["name"].lower()]
        all_tracks.extend(tracks)

    if not all_tracks:
        print(f"😔 No tracks found that exclude '{concept}'.")
        return

    random.shuffle(all_tracks)
    track_uris = [t["uri"] for t in all_tracks[:20]]

    playlist_name = input("Name your playlist: ").strip()
    playlist_id = create_playlist(user_id, playlist_name)
    if not playlist_id:
        return

    add_tracks_to_playlist(playlist_id, track_uris)

    # Save playlist info to DB
    save_playlist_to_db(user_id, playlist_name, playlist_id)

    print(f"🎶 Playlist '{playlist_name}' created with {len(track_uris)} tracks!")

if __name__ == "__main__":
    main()
