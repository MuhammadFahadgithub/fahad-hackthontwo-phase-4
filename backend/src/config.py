"""
Configuration module for the Todo Chatbot application
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://todouser:todopass@localhost:5432/tododb")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Application settings
APP_NAME = "Todo Chatbot"
API_V1_STR = "/api/v1"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# AI Model settings (for chat processing)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")