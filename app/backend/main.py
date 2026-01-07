import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from typing import Optional

# --- NEW SECURITY IMPORTS ---
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Imports from our separate files
from database import engine, get_session
from models import SQLModel, Profile, User

# ---------------------------------------------------------
# CONFIGURATION & SETUP
# ---------------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
ALLOWED_USERS_ENV = os.getenv("ALLOWED_USERS", "")

# Process whitelist into a Python set for fast lookups
# Cleans up spaces and converts to lowercase
WHITELISTED_EMAILS = set(email.strip().lower() for email in ALLOWED_USERS_ENV.split(",") if email.strip())

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not set. AI features will fail.")

if not GOOGLE_CLIENT_ID:
    print("CRITICAL WARNING: GOOGLE_CLIENT_ID not set. Authentication will fail.")

print(f"Whitelist loaded with {len(WHITELISTED_EMAILS)} allowed users.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    print("Database tables checked/created.")
    yield

app = FastAPI(lifespan=lifespan)

# ---------------------------------------------------------
# THE BOUNCER (Security Dependency)
# ---------------------------------------------------------
# This tells FastAPI to look for a "Bearer" token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """
    Validates Google token, checks whitelist, and retrieves/creates DB User.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    whitelist_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not on the allow list for this application.",
    )

    try:
        # 1. Verify the token with Google's servers
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        
        # Get email and Google's unique user ID (sub)
        email = idinfo.get('email').lower()
        google_sub = idinfo.get('sub')
        name = idinfo.get('name')

        if not email or not google_sub:
            raise credentials_exception
            
        # 2. CHECK THE WHITELIST
        if email not in WHITELISTED_EMAILS:
            print(f"Blocked login attempt from non-whitelisted email: {email}")
            raise whitelist_exception

    except ValueError as e:
        print(f"Token verification failed: {e}")
        raise credentials_exception

    # 3. Find the user in our DB, or create them if new
    user = session.exec(select(User).where(User.google_sub == google_sub)).first()
    
    if not user:
        print(f"First time login for allowed user: {email}. Creating record.")
        user = User(email=email, google_sub=google_sub, full_name=name)
        session.add(user)
        session.commit()
        session.refresh(user)
        
    # Return the full User database object
    return user

# ---------------------------------------------------------
# SECURE API ENDPOINTS (Multi-User!)
# ---------------------------------------------------------

@app.get("/")
def read_root():
    # This endpoint remains public for health checks
    return {"message": "Training Chef API is running (Secure Mode)"}

@app.get("/api/profile")
# NOTE THE CHANGE: We now depend on 'current_user', not just 'session'
def get_profile(current_user: User = Depends(get_current_user)):
    # SQLModel automatically loads the related profile thanks to the relationship defined in models.py
    if current_user.profile:
        return current_user.profile
    return {}

@app.post("/api/profile")
def create_or_update_profile(
    profile_data: Profile, 
    # We need both the user AND the session here to save data
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Check if THIS specific user already has a profile
    if current_user.profile:
        # Update existing
        current_user.profile.currentWeight = profile_data.currentWeight
        current_user.profile.height = profile_data.height
        current_user.profile.ftp = profile_data.ftp
        current_user.profile.bodyType = profile_data.bodyType
        session.add(current_user.profile)
        action = "updated"
    else:
        # Create new and LINK IT to the user
        new_profile = Profile(
            **profile_data.model_dump(), # Copy data from input
            user_id=current_user.id      # Link to the logged-in user
        )
        session.add(new_profile)
        action = "created"
        
    session.commit()
    # Re-fetch user to get updated profile relationship
    session.refresh(current_user) 
    return {"message": f"Profile {action}", "data": current_user.profile}


@app.post("/api/chat")
async def chat_with_ai(
    message: str, 
    # Secure the chat too!
    current_user: User = Depends(get_current_user)
): 
    if not API_KEY:
        return {"response": "Error: Server is missing GEMINI_API_KEY."}

    # Use the profile of the LOGGED IN user
    profile = current_user.profile
    
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