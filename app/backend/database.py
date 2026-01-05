import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# Get DB URL from environment.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback just so local tests don't crash immediately, 
    # but K8s MUST provide the real URL.
    DATABASE_URL = "sqlite:///./test.db" 

# Create the engine (connection to Postgres)
# echo=True prints SQL queries to logs (good for debugging)
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get a DB session in endpoints
def get_session():
    with Session(engine) as session:
        yield session
