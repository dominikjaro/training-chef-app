import os
# The google.generativeai package is deprecated and will be removed in a future version.
# Please migrate to the google.genai package.
# For now, we will ignore the warning.
import google.generativeai as genai
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")
genai.configure(api_key=api_key)

# Instantiate a FastMCP server
server = FastMCP(
    name="Training Chef Agent"
)

@server.tool()
def ask_chef(question: str, current_weight: float, ftp: int, body_type: str) -> str:
    """
    Provides expert cycling chef advice based on user's metrics and question.

    :param question: The user's question for the chef.
    :param current_weight: The user's current weight in kg.
    :param ftp: The user's Functional Threshold Power.
    :param body_type: The user's body type (e.g., ectomorph, mesomorph, endomorph).
    :return: Actionable advice from the cycling chef.
    """
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = (
        f"You are an expert cycling chef. The user is a {body_type} weighing {current_weight}kg "
        f"with an FTP of {ftp}. They ask: '{question}'. Give brief, actionable advice."
    )
    
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    server.run()
