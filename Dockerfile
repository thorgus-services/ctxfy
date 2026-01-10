# Multi-stage build: builder stage for dependencies
FROM python:3.13-slim AS builder

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.3

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Copy source code
COPY src ./src

# Configure Poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only=main --no-interaction

# Runtime stage: minimal image for execution
FROM python:3.13-slim

# Install minimal system dependencies needed at runtime
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src ./src
COPY resources ./resources
COPY example.env ./.env
COPY pyproject.toml ./

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Create workspace directory with appropriate permissions
RUN mkdir -p /workspace && chown -R appuser:appuser /workspace

# Switch to non-root user
USER appuser

# Health check using file-based status indicator
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD test -f /tmp/ctxfy_health_status.json && cat /tmp/ctxfy_health_status.json | jq -e '.status == "healthy"' > /dev/null || exit 1

# Set entrypoint to run the MCP server with health monitoring
ENTRYPOINT ["python", "-m", "src.app"]
CMD ["run_health_monitor"]