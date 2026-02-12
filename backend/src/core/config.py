import os
from typing import Optional


class Config:
    """
    Configuration class to manage application settings
    """
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")
    
    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Better Auth settings
    BETTER_AUTH_SECRET: Optional[str] = os.getenv("BETTER_AUTH_SECRET")
    
    # Application settings
    APP_NAME: str = "Todo AI Chatbot"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS settings
    ALLOWED_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",  # Default Next.js port
        "http://localhost:3001",  # Alternative Next.js port
        "https://yourdomain.com",  # Production domain
    ]
    
    # Performance settings
    RESPONSE_TIME_THRESHOLD: float = 3.0  # Maximum response time in seconds
    MAX_CONCURRENT_REQUESTS: int = 100


# Create a global config instance
config = Config()