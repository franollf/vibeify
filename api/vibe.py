from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from models import Vibe  # Make sure this matches your table

router = APIRouter(prefix="/vibe", tags=["Vibe"])

class VibeInput(BaseModel):
    user_id: int
    mood: str
    energy_level: float
    activity: str

@router.post("/")
def log_vibe(vibe: VibeInput, db: Session = Depends(get_db)):
    new_vibe = Vibe(
        user_id=vibe.user_id,
        mood=vibe.mood,
        energy_level=vibe.energy_level,
        activity=vibe.activity,
        timestamp=datetime.utcnow()
    )
    db.add(new_vibe)
    db.commit()
    db.refresh(new_vibe)
    
    return {
        "message": "Vibe logged!",
        "vibe": {
            "id": new_vibe.id,
            "user_id": new_vibe.user_id,
            "mood": new_vibe.mood,
            "energy_level": new_vibe.energy_level,
            "activity": new_vibe.activity,
            "timestamp": new_vibe.timestamp
        }
    }
        