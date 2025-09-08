"""
Configuration management for FastAPI backend
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Modular FastAPI Backend"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    DATABASE_ECHO: bool = False
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Browser Automation
    BROWSER_HEADLESS: bool = True
    BROWSER_TIMEOUT: int = 30000
    
    # Docker
    DOCKER_NETWORK: str = "kogic-network"
    CONTAINER_NAME: str = "fastapi-backend"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
