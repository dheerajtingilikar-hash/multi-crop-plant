import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# API key for Plant.id
PLANT_ID_API_KEY = os.getenv("PLANT_ID_API_KEY")

# Database URL (defaults to SQLite if not provided)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./plants.db")
