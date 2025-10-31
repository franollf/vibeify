import requests
import json

# ======================
# CONFIGURATION
# ======================
ACCESS_TOKEN = "BQAWwmp9bJhQpeDujn1cBWRtLcax4CaotWJsc37mCQwjia1TNAZPfdAFS7Ve5_45Os8nEJexrFHx-UBXclgzvWOYwOF4PVdPTpAm9hUtXOFpAfSgPqeeGdh8fXFcG1FM5YGnQEoNELE"  # Replace with your access token
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

VIBE_GENRES = {
    "Indie Rock": ["indie", "alternative", "garage", "punk"],
    "Hype": ["hip hop", "rap", "trap", "drill", "edm", "dubstep"],
    "Chill": ["lofi", "acoustic", "chill", "ambient", "folk"],
    "Pop / Dance": ["pop", "dance", "house", "disco", "electronic"],
    "Smooth": ["soul", "r&b", "funk", "motown", "jazz"]
}

# ======================
# SPOTIFY SEARCH + GENRE FILTER
# ======================
def get_artist_genres(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("genres", [])
    return []

def search_tracks(keyword, limit=200):
    tracks = []
    for offset in range(0, limit, 50):
        url = f"https://api.spotify.com/v1/search?q={keyword}&type=track&limit=50&offset={offset}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        items = r.json().get("tracks", {}).get("items", [])
        tracks.extend(items)
    return tracks

def match_vibe(genres, vibe_list):
    for g in genres:
        for v in vibe_list:
            if v in g.lower():  # partial match instead of exact match
                return True
    return False

# ======================
# MAIN
# ======================
def main():
    keyword = input("Enter a search keyword (e.g., 'chill', 'party', 'indie'): ").strip()
    vibe_choice = input("Optional: Enter a target vibe (Indie Rock, Hype, Chill, Pop / Dance, Smooth): ").strip()
    
    vibe_genres = VIBE_GENRES.get(vibe_choice, [])
    
    print(f"\n🎧 Searching for tracks with keyword: '{keyword}' ...")
    tracks = search_tracks(keyword)
    
    vibe_tracks = []
    for t in tracks:
        artist = t["artists"][0]
        artist_genres = get_artist_genres(artist["id"])
        if match_vibe(artist_genres, vibe_genres):
            vibe_tracks.append(f"{t['name']} - {artist['name']}")
            print(f"→ {t['name']} - {artist['name']} ({artist_genres})")
        if len(vibe_tracks) >= 15:
            break
    
    if vibe_tracks:
        filename = f"playlist_{vibe_choice.replace(' ', '_')}.txt"
        with open(filename, "w") as f:
            f.write("\n".join(vibe_tracks))
        print(f"\n🎶 Found {len(vibe_tracks)} tracks matching your vibe '{vibe_choice}'")
        print(f"✅ Playlist saved to {filename}")
    else:
        print(f"\n😔 No tracks matched your vibe '{vibe_choice}'")

if __name__ == "__main__":
    main()
