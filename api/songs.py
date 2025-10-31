from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Song
from spotify_client import get_audio_features, get_access_token
from pydantic import BaseModel

class TrackInput(BaseModel):
    track_id: str

router = APIRouter(prefix="/songs", tags=["Songs"])

@router.post("/load")
def load_song(track: TrackInput, db: Session = Depends(get_db)):
    track_id = track.track_id  # extract track_id from the body

    # Check if song is already in DB
    existing_song = db.query(Song).filter(Song.track_id == track_id).first()
    if existing_song:
        return {"message": "Song already exists", "song": existing_song}

    # Get Spotify data
    try:
        features = get_audio_features(track_id)
        track_info = get_track_info(track_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Save to database
    new_song = Song(
        track_id=track_id,
        name=track_info["name"],
        artist=", ".join([artist["name"] for artist in track_info["artists"]]),
        danceability=features["danceability"],
        energy=features["energy"],
        valence=features["valence"],
        tempo=features["tempo"]
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    return {"message": "Song saved!", "song": new_song}
