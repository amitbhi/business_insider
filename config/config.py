from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    """Consolidated configuration class mapped from the OS environment."""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")
    
    app_name: str = "Business Insider Intelligence Engine"
    
    # DB
    postgres_uri: str = "postgresql+asyncpg://businessinsider:sovereignintelligence@localhost:5432/business_knowledge"
    
    # LLM
    ollama_url: str = "http://localhost:11434"
    primary_model: str = "deepseek-coder:6.7b"
    
    # Data Pipeline
    DATA_SOURCE: str = "mock" # Can be updated to "mca"
    
    # SEC EDGAR
    SEC_USER_AGENT: str = "BusinessInsider/1.0 (amitvishnu@gmail.com)"
    USE_LIVE_SEC: bool = False

config = Settings()
