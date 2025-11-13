"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings with validation and environment variable overrides."""
    
    server_host: str = "127.0.0.1"
    server_port: int = 8000

    model_config = {'env_prefix': 'CTXFY_'}  # Use CTXFY_ as prefix for environment variables


# Create a global settings instance
settings = AppSettings()