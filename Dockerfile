# Use a specific Python version for consistency
FROM python:3.13-slim

# Set environment variables for security and configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Set working directory
WORKDIR /app

# Install system dependencies securely
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy poetry.lock and pyproject.toml first to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Install Poetry
RUN curl -sSL 'https://install.python-poetry.org' | python3 - \
    && mv /root/.local/bin/poetry /usr/local/bin/

# Configure Poetry
RUN poetry config virtualenvs.create false

# Copy application code before installing dependencies to handle the project installation properly
COPY . .

# Install dependencies via Poetry (this will install both external dependencies and the project itself)
RUN poetry install --only main --no-interaction

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port (should match the configuration)
EXPOSE 8000

# Health check - verify the port is open using netcat (MCP servers don't expose standard HTTP endpoints)
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD nc -z localhost 8000 || exit 1

# Run the application
CMD ["python", "-m", "src.app.main"]