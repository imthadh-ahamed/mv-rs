from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    DATABASE_NAME: str = Field("movie_recommendation_db", env="DATABASE_NAME")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        ["http://localhost:3000", "http://localhost:3001"], 
        env="ALLOWED_ORIGINS"
    )
    
    # Environment
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    DEBUG: bool = Field(True, env="DEBUG")
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    # ML Models
    MODELS_PATH: str = Field("ml_models", env="MODELS_PATH")
    
    # Server
    PORT: int = Field(8000, env="PORT")
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
