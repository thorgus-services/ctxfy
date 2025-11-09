"""Settings for the MCP context stack generator."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings for the context stack generator."""
    
    app_name: str = "MCP Context Stack Generator"
    version: str = "1.0.0"
    debug: bool = False
    
    # MCP Configuration
    mcp_server_host: str = "127.0.0.1"
    mcp_server_port: int = 8000
    
    # Performance
    generation_timeout: int = 15  # seconds
    
    class Config:
        env_file = ".env"


settings = Settings()