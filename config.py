import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application Settings with Logfire Configuration"""
    
    # API Keys
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    logfire_token: str = Field(default="", env="LOGFIRE_TOKEN")
    logfire_project_name: str = Field(default="agent-project", env="LOGFIRE_PROJECT")
    
    # Model Configuration
    model_name: str = Field(default="gpt-4", env="MODEL_NAME")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    max_tokens: int = Field(default=2000, env="MAX_TOKENS")
    
    # Agent Configuration
    enable_logging: bool = Field(default=True, env="ENABLE_LOGGING")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Performance Settings
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    timeout_seconds: int = Field(default=30, env="TIMEOUT_SECONDS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
