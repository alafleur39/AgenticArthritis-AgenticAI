from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./agentarthritis.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email Service
    sendgrid_api_key: Optional[str] = None
    from_email: str = "noreply@agentarthritis.com"
    
    # OpenAI API
    openai_api_key: Optional[str] = None
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:12000"]
    
    class Config:
        env_file = ".env"


settings = Settings()