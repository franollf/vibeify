from fastapi import FastAPI
from api import auth, vibe, recommendations
from database import SessionLocal
from api import vibe, songs

app = FastAPI(title="VibeWave API")

app.include_router(auth.router)
app.include_router(vibe.router)
app.include_router(recommendations.router)
app.include_router(songs.router)

@app.get("/")
def home():
    return {"message": "Welcome to VibeWave!"}

from fastapi import FastAPI
from spotify_client import get_access_token

app = FastAPI()

@app.get("/spotify-test")
def spotify_test():
    token = get_access_token()
    return {"token": token[:20] + "..."}  # first 20 chars only

##uvicorn main:app --reload
