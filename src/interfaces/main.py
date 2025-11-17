"""Main application entry point with dependency injection for the ctxfy MCP Server."""

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Any, Dict, Optional

import structlog
from fastmcp import FastMCP
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.adapters.api_docs import MCPToolsDocsGenerator, OpenAPIDocGenerator
from src.adapters.auth import ApiKeyAuthAdapter, InMemoryApiKeyRepository
from src.adapters.auth.middleware import AuthMiddleware
from src.adapters.monitoring import StructuredLoggingAdapter
from src.adapters.monitoring.monitoring import MonitoringAdapter
from src.adapters.validation import SchemaValidationAdapter
from src.config import settings
from src.core.models.auth_models import ApiKeyRequest
from src.core.models.error_models import (
    ApplicationError,
    ErrorCodes,
)

# For type checking compatibility
if TYPE_CHECKING:
    
    class FastMCPWithHandlers(FastMCP):
        _handlers: Dict[str, Any]

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

        # Initialize MCP tools documentation generator
        self.mcp_tools_docs_generator = MCPToolsDocsGenerator()


class MCPServerApp:
    """Main MCP server application class with dependency injection."""

    def __init__(self, dependencies: Optional[AppDependencies] = None) -> None:
        self.dependencies = dependencies or AppDependencies()
        self.mcp = FastMCP()
        # Initialize handlers dictionary for testing purposes to access registered functions
        self.mcp._handlers = {}  # type: ignore[attr-defined]
        
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

        # Update the OpenAPI generator with the actual MCP server instance
        self.dependencies.openapi_generator.update_mcp_server(self.mcp)

        # Update the MCP tools documentation generator with the actual MCP server instance
        self.dependencies.mcp_tools_docs_generator.set_mcp_server(self.mcp)

        # Set up documentation endpoints after updating the generator
        self._setup_documentation()

    def _register_builtin_prompts(self) -> None:
        """Register built-in prompts with the FastMCP server."""
        # Currently no built-in prompts implemented
        pass

    def _setup_health_check(self) -> None:
        """Set up the health check endpoint using custom route as required by GoFastMCP."""
        @self.mcp.custom_route("/health", methods=["GET"])
        async def health_check(request: Request) -> JSONResponse:
            """
            Health check endpoint returning system status.

            Returns:
                JSONResponse: Health status information including status, timestamp,
                             uptime, version, and service checks

            Example Response:
                {
                    "status": "healthy",
                    "timestamp": "2023-10-10T12:00:00Z",
                    "uptime_seconds": 3600,
                    "version": "1.0.0",
                    "checks": {},
                    "service": "ctxfy-mcp-server"
                }
            """
            try:
                health_status = await self.dependencies.monitoring_adapter.get_health_status()
                return JSONResponse({
                    "status": health_status.status,
                    "timestamp": health_status.timestamp.isoformat(),
                    "uptime_seconds": health_status.uptime_seconds,
                    "version": health_status.version,
                    "checks": health_status.checks,
                    "service": "ctxfy-mcp-server"
                })
            except Exception as e:
                # Log the error
                request_id = "health-check"
                self.dependencies.logging_adapter.log_error(
                    request_id=request_id,
                    error=e,
                    context={
                        "endpoint": "health",
                    }
                )

                # Create structured error response
                error = ApplicationError(
                    error_code=ErrorCodes.INTERNAL_ERROR,
                    message="Health check failed",
                    details=str(e),
                    request_id=request_id
                )

                # Return error representation
                return JSONResponse({
                    "status": "unhealthy",
                    "timestamp": datetime.now().isoformat(),
                    "error": error.message,
                    "error_code": error.error_code.value if hasattr(error.error_code, 'value') else str(error.error_code),
                    "service": "ctxfy-mcp-server"
                }, status_code=500)


    def _setup_metrics(self) -> None:
        """Set up the metrics endpoint."""
        @self.mcp.custom_route("/metrics", methods=["GET"])
        async def metrics_endpoint(request: Request) -> Response:
            """
            Metrics endpoint returning Prometheus-formatted metrics.

            Returns:
                Response: Plain text response with Prometheus-formatted metrics
            """
            try:
                metrics_data = self.dependencies.monitoring_adapter.get_prometheus_metrics()
                # Return as plain text response (standard for Prometheus)
                return Response(
                    content=metrics_data.decode('utf-8'),
                    media_type="text/plain; version=0.0.4; charset=utf-8"
                )
            except Exception as e:
                # Log the error
                request_id = "metrics-check"
                self.dependencies.logging_adapter.log_error(
                    request_id=request_id,
                    error=e,
                    context={
                        "endpoint": "metrics",
                    }
                )

                # Create structured error response
                error = ApplicationError(
                    error_code=ErrorCodes.INTERNAL_ERROR,
                    message="Metrics collection failed",
                    details=str(e),
                    request_id=request_id
                )

                error_code_value = error.error_code.value if hasattr(error.error_code, 'value') else str(error.error_code)
                return Response(
                    content=f"# Error collecting metrics: {error.message} (code: {error_code_value})",
                    status_code=500,
                    media_type="text/plain; charset=utf-8"
                )

    def _setup_api_key_management(self) -> None:
        """Set up API key management endpoints."""
        @self.mcp.tool(
            name="create-api-key",
            description="Create a new API key for authentication.",
            tags={"auth", "security"},
            annotations={
                "title": "Create API Key",
                "readOnlyHint": False,
                "destructiveHint": False
            }
        )
        async def create_api_key(
            ctx: Any,
            user_id: Annotated[str, Field(
                description="Unique identifier for the user requesting the API key"
            )],
            scope: Annotated[str, Field(
                description="Access scope for the API key",
                default="read"
            )] = "read",
            ttl_hours: Annotated[Optional[int], Field(
                description="Time-to-live in hours for the API key",
                default=None
            )] = None
        ) -> Dict[str, Any]:
            """Create a new API key for authentication.

            This tool generates a new API key that can be used for authenticating
            requests to the MCP server. The API key can have different scopes and
            time-to-live settings.

            Args:
                ctx: FastMCP context object
                user_id: Unique identifier for the user requesting the API key
                scope: Access scope for the API key (defaults to "read")
                ttl_hours: Time-to-live in hours for the API key (optional)

            Returns:
                Dict[str, str]: A dictionary containing the generated API key and its ID

            Example:
                Input: {"user_id": "user-123", "scope": "read", "ttl_hours": 24}
                Output: {"api_key": "generated_key_value", "key_id": "request_id"}
            """
            request_id = f"req-{id(ctx)}" if ctx else f"api-key-{user_id}"

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
                    request_id=request_id,
                    error=e,
                    context={
                        "endpoint": "create-api-key",
                        "user_id": user_id
                    }
                )

                # Log error details
                log_entry = self.dependencies.logging_adapter.create_log_entry(
                    level="ERROR",
                    message=f"API key creation failed: {str(e)}",
                    request_id=request_id,
                    latency_ms=0,
                    endpoint="create-api-key",
                    llm_model="N/A",
                    extra={"user_id": user_id, "scope": scope}
                )
                self.dependencies.logging_adapter.log_request(log_entry)

                # Create and return structured error response
                error = ApplicationError(
                    error_code=ErrorCodes.INTERNAL_ERROR,
                    message=str(e),
                    details=str(type(e).__name__),
                    request_id=request_id
                )

                # Log error details
                log_entry = self.dependencies.logging_adapter.create_log_entry(
                    level="ERROR",
                    message=f"API key creation failed: {str(e)}",
                    request_id=request_id,
                    latency_ms=0,
                    endpoint="create-api-key",
                    llm_model="N/A",
                    extra={"user_id": user_id, "scope": scope}
                )
                self.dependencies.logging_adapter.log_request(log_entry)

                # For MCP, return error details in a structured way
                return {
                    "success": False,
                    "error": {
                        "message": error.message,
                        "error_code": error.error_code.value if hasattr(error.error_code, 'value') else str(error.error_code),
                        "request_id": error.request_id,
                        "details": []
                    }
                }

        # Add to handlers for testability
        self.mcp._handlers['create-api-key'] = {'fn': create_api_key}  # type: ignore[attr-defined]

    def _setup_documentation(self) -> None:
        """Set up documentation endpoints."""
        # Register endpoint to serve OpenAPI specification
        @self.mcp.custom_route("/openapi.json", methods=["GET"])
        async def openapi_spec(request: Request) -> JSONResponse:
            """Endpoint to serve the OpenAPI specification."""
            spec = await self.dependencies.openapi_generator.get_openapi_spec()
            return JSONResponse(spec)

        # Register endpoint for interactive API documentation (Swagger UI equivalent)
        @self.mcp.custom_route("/docs", methods=["GET"])
        async def api_docs(request: Request) -> Response:
            """Endpoint to serve interactive API documentation."""
            swagger_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ctxfy MCP Server API Documentation</title>
                <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.11.0/swagger-ui.css">
            </head>
            <body>
                <div id="swagger-ui"></div>
                <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.11.0/swagger-ui-bundle.js"></script>
                <script>
                const ui = SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.presets.standalone
                    ]
                });
                </script>
            </body>
            </html>
            """
            return Response(content=swagger_html, media_type="text/html")

        # Register endpoint to serve MCP tools specification
        @self.mcp.custom_route("/mcp-tools", methods=["GET"])
        async def mcp_tools_spec(request: Request) -> JSONResponse:
            """Endpoint to serve MCP tools specification."""
            tools_spec = await self.dependencies.mcp_tools_docs_generator.get_mcp_tools_docs()
            return JSONResponse(tools_spec)



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

    def serve_with_uvicorn(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Serve the application using uvicorn (ASGI server).

        This method allows the application to be deployed using standard ASGI servers.
        """
        import uvicorn

        # Log server startup
        log_entry = self.dependencies.logging_adapter.create_log_entry(
            level="INFO",
            message="MCP Server starting (ASGI mode with uvicorn)",
            request_id="SERVER_START",
            latency_ms=0,
            endpoint="server",
            llm_model="N/A",
            extra={"host": host, "port": str(port), "server_type": "uvicorn"}
        )
        self.dependencies.logging_adapter.log_request(log_entry)

        # Run with uvicorn using the ASGI app
        uvicorn.run(
            "src.interfaces.main:create_app",
            host=host,
            port=port,
            factory=True,  # Tells uvicorn to call create_app() to get the app
            reload=False,  # Disable reload in production
            log_level="info"
        )

    def get_app(self) -> FastMCP:
        """Get the FastMCP app instance."""
        return self.mcp


def create_app() -> FastMCP:
    """ASGI application factory that creates and returns the FastMCP ASGI app.

    This allows the application to be served with standard ASGI servers like uvicorn.
    """
    app = MCPServerApp()
    return app.get_app()


# Main entry point
async def main() -> None:
    """Main entry point for the application."""
    app = MCPServerApp()

    # Get host and port from settings (with environment variable overrides)
    host = settings.server_host
    port = settings.server_port

    await app.start_server(host=host, port=port)


if __name__ == "__main__":
    asyncio.run(main())