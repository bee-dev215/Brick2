"""Application configuration settings."""

from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Ad Orchestrator"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-here"
    
    # Database - BRICK 1 Integration
    DATABASE_URL: str = "postgresql+asyncpg://user:password@64.227.99.111:5432/brick_orchestration"
    DATABASE_URL_SYNC: str = "postgresql://user:password@64.227.99.111:5432/brick_orchestration"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External Services
    AD_SERVICE_URL: str = "https://api.ad-service.com"
    ANALYTICS_SERVICE_URL: str = "https://api.analytics.com"
    
    class Config:
        """Pydantic config."""
        
        env_file = ".env"
        case_sensitive = True


settings = Settings()
