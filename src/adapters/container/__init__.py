"""Docker configuration and containerization utilities for the ctxfy MCP server."""

import os
from typing import Any, Dict


class DockerConfig:
    """Configuration class for Docker containerization with security best practices."""
    
    @staticmethod
    def generate_dockerfile_content() -> str:
        """Generate Dockerfile content with security best practices."""
        dockerfile_content = """# Use a specific Python version for consistency
FROM python:3.13-slim

# Set environment variables for security and configuration
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PYTHONPATH=/app/src

# Set working directory
WORKDIR /app

# Install system dependencies securely
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy poetry.lock and pyproject.toml first to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Install Poetry
RUN curl -sSL 'https://install.python-poetry.org' | python3 - \\
    && mv /root/.local/bin/poetry /usr/local/bin/

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies via Poetry
RUN poetry install --only main --no-interaction

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port (should match the configuration)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "src.app.main"]
"""
        return dockerfile_content
    
    @staticmethod
    def generate_docker_compose_content() -> str:
        """Generate docker-compose.yml content for local development."""
        compose_content = """version: '3.8'

services:
  ctxfy-mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app/src
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs  # Mount logs directory
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /run
"""
        return compose_content


# Write Dockerfile
def write_dockerfile() -> None:
    """Write Dockerfile to project root."""
    with open("Dockerfile", "w") as f:
        f.write(DockerConfig.generate_dockerfile_content())


# Write docker-compose.yml
def write_docker_compose() -> None:
    """Write docker-compose.yml to project root."""
    with open("docker-compose.yml", "w") as f:
        f.write(DockerConfig.generate_docker_compose_content())


if __name__ == "__main__":
    write_dockerfile()
    write_docker_compose()
    # Docker configuration files generated successfully!