from fastapi import FastAPI
from api import auth, vibe, recommendations
from database import SessionLocal

app = FastAPI(title="VibeWave API")

app.include_router(auth.router)
app.include_router(vibe.router)
app.include_router(recommendations.router)

@app.get("/")
def home():
    return {"message": "Welcome to VibeWave!"}

##uvicorn main:app --reload
