"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Configuration and Environment Settings
"""
import os
from pydantic import BaseModel

class Settings(BaseModel):
    """Global configuration settings for NERA backend service"""
    PROJECT_NAME: str = "NERA - AI Logistics & Disaster Resilience Engine"
    VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")

# Instantiate singleton settings object for application-wide access
settings = Settings()
