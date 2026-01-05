import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session, select

# --- IMPORTS FROM OUR NEW SEPARATE FILES ---
from database import engine, get_session
from models import SQLModel, Profile, User # Import the new models

# ---------------------------------------------------------
# APP SETUP & DATABASE MIGRATION
# ---------------------------------------------------------
# Lifespan handles startup events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This uses the imported 'engine' and the imported 'SQLModel' metadata
    # from models.py to create the new 'user' and 'profile' tables.
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully.")
    yield

app = FastAPI(lifespan=lifespan)

# AI Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not set. AI features will fail.")

# ---------------------------------------------------------
# API ENDPOINTS (TEMPORARILY SINGLE-PLAYER)
# ---------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Training Chef API (Multi-User Ready)"}

@app.post("/api/profile")
# Note: We use Depends(get_session) imported from database.py
def create_profile(profile_data: Profile, session: Session = Depends(get_session)):
    # WARNING: This is still "single player". It grabs the first one it finds.
    # We will fix this in the next step when we add Auth.
    existing_profile = session.exec(select(Profile)).first()
    
    if existing_profile:
        existing_profile.currentWeight = profile_data.currentWeight
        existing_profile.height = profile_data.height
        existing_profile.ftp = profile_data.ftp
        existing_profile.bodyType = profile_data.bodyType
        session.add(existing_profile)
        session.commit()
        session.refresh(existing_profile)
        return {"message": "Profile updated", "data": existing_profile}
    else:
        # NOTE: This will currently create a profile with user_id=None.
        # This is okay for testing this exact step, but will change soon.
        session.add(profile_data)
        session.commit()
        session.refresh(profile_data)
        return {"message": "Profile created", "data": profile_data}

@app.get("/api/profile")
def get_profile(session: Session = Depends(get_session)):
    # Still single player mode for now
    profile = session.exec(select(Profile)).first()
    if profile:
        return profile
    # Return empty JSON instead of a message string so the frontend form doesn't break
    return {} 

@app.post("/api/chat")
async def chat_with_ai(message: str, session: Session = Depends(get_session)): 
    if not API_KEY:
        return {"response": "Error: Server is missing GEMINI_API_KEY."}

    # Still single player mode for now
    profile = session.exec(select(Profile)).first()
    
    if profile:
        persona = (
            f"You are an expert Cycling Chef. "
            f"The user is a {profile.bodyType} weighing {profile.currentWeight}kg "
            f"with an FTP of {profile.ftp} watts."
        )
    else:
        persona = "You are an expert Cycling Chef. The user has not set up their profile yet, so give general advice."

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(f"{persona}\nUser Question: {message}")
        return {"response": response.text}

    except Exception as e:
        print(f"AI Error: {e}")
        return {"response": "I'm having trouble contacting my brain right now."}