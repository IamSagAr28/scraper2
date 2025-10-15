from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Court Cause List API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for fetching court cause lists in real-time"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
    # Scraping Configuration
    SCRAPING_TIMEOUT: int = 30  # seconds
    CHROME_HEADLESS: bool = True
    MAX_RETRY_ATTEMPTS: int = 3
    
    # PDF Configuration
    OUTPUT_DIR: str = "output"
    PDF_CLEANUP_DELAY: int = 300  # seconds (5 minutes)
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()
