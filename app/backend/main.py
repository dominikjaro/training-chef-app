import os
import httpx
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# MCP Imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

app = FastAPI()

# ---------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found. AI features will not work.")

# ---------------------------------------------------------
# 2. DATA MODELS
# ---------------------------------------------------------
class ProfileModel(BaseModel):
    weight: float = Field(alias="currentWeight")
    height: float
    ftp: int
    body_type: str = Field(alias="bodyType")
    
    class Config:
        populate_by_name = True

# In-memory storage for profile data
profile_data: Optional[ProfileModel] = None

# ---------------------------------------------------------
# 3. API ENDPOINTS
# ---------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Training Chef API"}

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
async def chat_with_ai(message: str): # Receives ?message=... from frontend
    if not API_KEY:
        return {"response": "Error: Server is missing GEMINI_API_KEY."}

    # The internal DNS address of your MCP Service in Kubernetes
    mcp_url = "http://mcp-server.mcp-server.svc.cluster.local:8080/sse"
    
    # Define the System Persona
    if profile_data:
        persona = (
            f"You are an expert Cycling Chef and a nutritionist. "
            f"The user is a {profile_data.body_type} weighing {profile_data.weight}kg "
            f"with an FTP of {profile_data.ftp} watts."
        )
    else:
        persona = "You are an expert Cycling Chef and a nutritionist. Ask the user to set up their profile first."

    try:
        # --- CONNECT TO MCP SERVER ---
        # We use a context manager to open/close the connection safely
        async with sse_client(mcp_url) as (read, write):
            async with ClientSession(read, write) as session:
                
                # A. Discover Tools
                await session.initialize()
                tools_list = await session.list_tools()
                
                # B. Inform Gemini about the tools
                available_tools_desc = ", ".join([t.name for t in tools_list.tools])
                
                system_instruction = (
                    f"{persona}\n"
                    f"You have access to these external tools: [{available_tools_desc}]. "
                    f"If you need to use a tool, output exactly: USE_TOOL: <tool_name>"
                )
                
                # C. Generate Initial Thought
                system_instruction = (
                    f"{persona}\n"
                    f"You have access to these external tools: [{available_tools_desc}]. "
                    f"Only use a tool if the user explicitly asks for 'Strava stats'. "
                    f"Otherwise, just answer their question helpfully."
                )
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"{system_instruction}\nUser Question: {message}")
                ai_text = response.text

                # D. Tool Execution Logic (Simplified)
                # If Gemini says "USE_TOOL: get_strava_stats", we execute it.
                if "USE_TOOL: get_strava_stats" in ai_text:
                    pass
                    
                return {"response": ai_text}

    except Exception as e:
        # --- FALLBACK (If MCP is down) ---
        print(f"MCP Connection Error: {e}")
        # We still want the chat to work, even if tools are broken
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{persona}\nUser: {message}")
        return {"response": response.text}