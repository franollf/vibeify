from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Song
from spotify_client import get_audio_features

router = APIRouter(prefix="/songs", tags=["Songs"])

@router.post("/load")
def load_songs(track_ids: list[str], db: Session = Depends(get_db)):
    features = get_audio_features(track_ids)
    for f in features:
        song = Song(
            id=f["id"],
            name=f.get("name", ""),
            artist=f.get("artists", [{}])[0].get("name", ""),
            danceability=f["danceability"],
            energy=f["energy"],
            valence=f["valence"],
            tempo=f["tempo"]
        )
        db.merge(song)  # insert or update
    db.commit()
    return {"message": f"{len(features)} songs loaded."}
