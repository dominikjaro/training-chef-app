from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class ProfileModel(BaseModel):
    weight: float
    height: float
    ftp: int
    body_type: str

# In-memory storage for profile data
profile_data: Optional[ProfileModel] = None

@app.post("/api/profile")
def create_profile(profile: ProfileModel):
    global profile_data
    profile_data = profile
    return {"message": "Profile created successfully", "data": profile_data}

@app.get("/api/profile")
def get_profile():
    if profile_data:
        return profile_data
    return {"message": "No profile data found. Please create a profile first."}

@app.post("/api/chat")
def chat_with_ai(message: str):
    return {"response": f"This is a fake AI response to your message: '{message}'"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Training Chef API"}