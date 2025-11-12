"""Main application entry point with dependency injection for the ctxfy MCP Server."""

import asyncio
import os
from datetime import datetime
from typing import Any, Dict, Optional

import structlog
from fastmcp.server import FastMCP

from src.adapters.api_docs import OpenAPIDocGenerator
from src.adapters.auth import ApiKeyAuthAdapter, InMemoryApiKeyRepository
from src.adapters.auth.middleware import AuthMiddleware
from src.adapters.monitoring import StructuredLoggingAdapter
from src.adapters.monitoring.monitoring import MonitoringAdapter
from src.adapters.validation import SchemaValidationAdapter
from src.core.models.auth_models import ApiKeyRequest

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


class AppDependencies:
    """Container for application dependencies with dependency injection."""

    def __init__(self) -> None:

        # Initialize the in-memory API key repository
        self.api_key_repo = InMemoryApiKeyRepository()

        # Initialize authentication adapter
        self.auth_adapter = ApiKeyAuthAdapter(self.api_key_repo)

        # Initialize monitoring and logging
        self.start_time = datetime.now()
        self.monitoring_adapter = MonitoringAdapter(self.start_time)
        self.logging_adapter = StructuredLoggingAdapter()

        # Initialize validation adapter
        self.validation_adapter = SchemaValidationAdapter()

        # Initialize auth middleware
        self.auth_middleware = AuthMiddleware(self.auth_adapter)

        # Initialize OpenAPI documentation
        self.openapi_generator = OpenAPIDocGenerator(
            mcp_server=None,  # Will be set after FastMCP initialization
            title="ctxfy MCP Server API",
            description="Production-ready ctxfy MCP Server with authentication, monitoring, and documentation",
            version="1.0.0"
        )


class MCPServerApp:
    """Main MCP server application class with dependency injection."""

    def __init__(self, dependencies: Optional[AppDependencies] = None) -> None:
        self.dependencies = dependencies or AppDependencies()
        self.mcp = FastMCP()
        # Ensure start method exists for test mocking purposes
        if not hasattr(self.mcp, 'start'):
            # Add a default start method that can be mocked
            async def default_start(host: str = "127.0.0.1", port: int = 8000) -> None:
                pass
            self.mcp.start = default_start  # type: ignore
        self._setup_server()

    def _setup_server(self) -> None:
        """Set up the FastMCP server with all required functionality."""
        # Register built-in prompts
        self._register_builtin_prompts()

        # Set up health check endpoint
        self._setup_health_check()

        # Set up metrics endpoint
        self._setup_metrics()

        # Set up API key management
        self._setup_api_key_management()

        # Set up documentation endpoints
        self._setup_documentation()

        # Update the OpenAPI generator with the actual MCP server instance
        self.dependencies.openapi_generator.mcp_server = self.mcp

    def _register_builtin_prompts(self) -> None:
        """Register built-in prompts with the FastMCP server."""
        # Example prompt - in a real application, you'd have more substantial prompts
        @self.mcp.prompt("sample-prompt")
        async def sample_prompt(ctx: Any, param1: str = "default") -> str:
            """A sample prompt for testing and demonstration."""
            # Log the request
            from datetime import datetime
            start_time = datetime.now()

            try:
                # Execute the prompt logic
                result = f"Processed: {param1}"

                # Calculate latency
                latency_ms = (datetime.now() - start_time).total_seconds() * 1000

                # Log the successful execution
                log_entry = self.dependencies.logging_adapter.create_log_entry(
                    level="INFO",
                    message="Sample prompt executed successfully",
                    request_id="N/A",  # Would get from context in real implementation
                    latency_ms=latency_ms,
                    endpoint="sample-prompt",
                    llm_model="default"
                )
                self.dependencies.logging_adapter.log_request(log_entry)

                # Record metrics
                self.dependencies.monitoring_adapter.record_prompt_execution(
                    template_id="sample-prompt",
                    latency_ms=latency_ms,
                    success=True
                )

                return result
            except Exception as e:
                # Log the error
                self.dependencies.logging_adapter.log_error(
                    request_id="N/A",
                    error=e,
                    context={
                        "endpoint": "sample-prompt",
                        "param1": param1
                    }
                )

                # Record metrics for failure
                self.dependencies.monitoring_adapter.record_prompt_execution(
                    template_id="sample-prompt",
                    latency_ms=0,
                    success=False
                )

                raise e

    def _setup_health_check(self) -> None:
        """Set up the health check endpoint."""
        @self.mcp.prompt("health")
        async def health_check(ctx: Any) -> Dict[str, Any]:
            """Health check endpoint returning system status."""
            health_status = await self.dependencies.monitoring_adapter.get_health_status()
            return {
                "status": health_status.status,
                "timestamp": health_status.timestamp.isoformat(),
                "uptime_seconds": health_status.uptime_seconds,
                "version": health_status.version,
                "checks": health_status.checks
            }

    def _setup_metrics(self) -> None:
        """Set up the metrics endpoint."""
        @self.mcp.prompt("metrics")
        async def metrics_endpoint(ctx: Any) -> str:
            """Metrics endpoint returning Prometheus-formatted metrics."""
            metrics_data = self.dependencies.monitoring_adapter.get_prometheus_metrics()
            return metrics_data.decode('utf-8')  # Return as string

    def _setup_api_key_management(self) -> None:
        """Set up API key management endpoints."""
        @self.mcp.prompt("create-api-key")
        async def create_api_key(ctx: Any, user_id: str, scope: str = "read", ttl_hours: Optional[int] = None) -> Dict[str, Any]:
            """Create a new API key."""
            try:
                # Create an ApiKeyRequest instance
                api_key_request = ApiKeyRequest(
                    user_id=user_id,
                    scope=scope,
                    ttl_hours=ttl_hours
                )

                # Generate and store the API key
                new_key = await self.dependencies.auth_adapter.create_api_key(api_key_request)

                # Log the successful creation
                log_entry = self.dependencies.logging_adapter.create_log_entry(
                    level="INFO",
                    message="API key created successfully",
                    request_id=api_key_request.request_id,
                    latency_ms=0,  # Latency not applicable for this sync operation
                    user_id=user_id,
                    endpoint="create-api-key"
                )
                self.dependencies.logging_adapter.log_request(log_entry)

                return {"api_key": new_key, "key_id": api_key_request.request_id}
            except Exception as e:
                # Log the error
                self.dependencies.logging_adapter.log_error(
                    request_id="N/A",
                    error=e,
                    context={
                        "endpoint": "create-api-key",
                        "user_id": user_id
                    }
                )
                raise e

    def _setup_documentation(self) -> None:
        """Set up documentation endpoints."""
        # The OpenAPI documentation is generated automatically
        # but we can register additional endpoints for docs if needed
        pass

    async def start_server(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Start the MCP server."""
        # Log server startup
        log_entry = self.dependencies.logging_adapter.create_log_entry(
            level="INFO",
            message="MCP Server starting",
            request_id="SERVER_START",
            latency_ms=0,
            endpoint="server",
            llm_model="N/A",
            extra={"host": host, "port": str(port)}
        )
        self.dependencies.logging_adapter.log_request(log_entry)

        # Run the FastMCP HTTP server with proper parameters
        # Specify HTTP transport and avoid websockets configuration issues
        await self.mcp.run_http_async(host=host, port=port, transport='http', 
                                      uvicorn_config={'ws': None})  # Disable WebSocket to avoid 'websockets-sansio' issues

    def get_app(self) -> FastMCP:
        """Get the FastMCP app instance."""
        return self.mcp


# Main entry point
async def main() -> None:
    """Main entry point for the application."""
    app = MCPServerApp()
    
    # Get host and port from environment variables with defaults
    host = os.getenv("SERVER_HOST", "0.0.0.0")  # nosec B104 - Allow binding to all interfaces for Docker; override with env var for production
    port = int(os.getenv("SERVER_PORT", "8000"))
    
    await app.start_server(host=host, port=port)


if __name__ == "__main__":
    asyncio.run(main())