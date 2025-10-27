from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Vibe(Base):
    __tablename__ = "vibes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood = Column(String)
    energy_level = Column(Float)
    activity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Song(Base):
    __tablename__ = "songs"

    id = Column(String, primary_key=True)  # Spotify track ID
    name = Column(String)
    artist = Column(String)
    danceability = Column(Float)
    energy = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)