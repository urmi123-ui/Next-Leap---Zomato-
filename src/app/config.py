import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_provider: str = "groq"
    llm_api_key: str = ""
    llm_model: str = "llama-3.1-8b-instant"
    
    data_path: str = "data/processed/restaurants.parquet"
    max_candidates: int = 30

    # Pydantic Settings Config to load from .env file
    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
