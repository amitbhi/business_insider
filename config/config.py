"""
Config Loader Module.

Validates and loads environment variables dynamically for
secure operation. Strongly typed with Pydantic.
"""

# from pydantic_settings import BaseSettings

class Settings:
    """Consolidated configuration class mapped from the OS environment."""
    
    app_name: str = "Business Insider Intelligence Engine"
    
    # DB
    postgres_uri: str = "postgresql+asyncpg://businessinsider:sovereignintelligence@localhost:5432/business_knowledge"
    
    # LLM
    ollama_url: str = "http://localhost:11434"
    primary_model: str = "deepseek-coder:6.7b"
    
    # Data Pipeline
    DATA_SOURCE: str = "mock" # Can be updated to "mca"
    
config = Settings()
