import os
import httpx
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from contextlib import asynccontextmanager

# Database Imports
from sqlmodel import Field, Session, SQLModel, create_engine, select

# MCP Imports
from mcp import ClientSession
from mcp.client.sse import sse_client

# ---------------------------------------------------------
# 1. DATABASE CONFIGURATION
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine (connection to Postgres)
# echo=True prints SQL queries to logs (good for debugging)
engine = create_engine(DATABASE_URL, echo=True)

# ---------------------------------------------------------
# 2. DATA MODELS (Tables)
# ---------------------------------------------------------
# This class defines BOTH the API validation AND the Database Table
class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    currentWeight: float
    height: float
    ftp: int
    bodyType: str

# Function to create tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Function to get a DB session (Dependency Injection)
def get_session():
    with Session(engine) as session:
        yield session

# ---------------------------------------------------------
# 3. APP SETUP
# ---------------------------------------------------------
# Lifespan handles startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() # Create tables if they don't exist
    yield

app = FastAPI(lifespan=lifespan)

# AI Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# ---------------------------------------------------------
# 4. API ENDPOINTS
# ---------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Training Chef API"}

@app.post("/api/profile")
def create_profile(profile: Profile, session: Session = Depends(get_session)):
    # Check if profile exists (Single User Mode for now)
    existing_profile = session.exec(select(Profile)).first()
    
    if existing_profile:
        # Update existing
        existing_profile.currentWeight = profile.currentWeight
        existing_profile.height = profile.height
        existing_profile.ftp = profile.ftp
        existing_profile.bodyType = profile.bodyType
        session.add(existing_profile)
        session.commit()
        session.refresh(existing_profile)
        return {"message": "Profile updated", "data": existing_profile}
    else:
        # Create new
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return {"message": "Profile created", "data": profile}

@app.get("/api/profile")
def get_profile(session: Session = Depends(get_session)):
    # Get the first profile found
    profile = session.exec(select(Profile)).first()
    if profile:
        return profile
    return {"message": "No profile data found."}

@app.post("/api/chat")
async def chat_with_ai(message: str, session: Session = Depends(get_session)): 
    if not API_KEY:
        return {"response": "Error: Server is missing GEMINI_API_KEY."}

    # Fetch Profile from DB for Context
    profile = session.exec(select(Profile)).first()
    
    if profile:
        persona = (
            f"You are an expert Cycling Chef. "
            f"The user is a {profile.bodyType} weighing {profile.currentWeight}kg "
            f"with an FTP of {profile.ftp} watts."
        )
    else:
        persona = "You are an expert Cycling Chef. Ask the user to set up their profile first."

    # Chat Logic (Simplified for brevity - add MCP back if needed)
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(f"{persona}\nUser Question: {message}")
        return {"response": response.text}

    except Exception as e:
        print(f"Error: {e}")
        return {"response": "I'm having trouble thinking right now."}