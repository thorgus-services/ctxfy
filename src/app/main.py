"""Main application entry point with dependency injection for the ctxfy MCP Server."""

import asyncio
from typing import TYPE_CHECKING, Optional

import structlog
from fastmcp import FastMCP

from src.app.dependencies import AppDependencies
from src.app.handlers.auth_handlers import register_auth_handlers
from src.app.handlers.documentation_handlers import register_documentation_handlers
from src.app.handlers.monitoring_handlers import register_monitoring_handlers
from src.config import settings

if TYPE_CHECKING:
    pass


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


class MCPServerApp:
    """Main MCP server application class with dependency injection following hexagonal architecture."""

    def __init__(self, dependencies: Optional[AppDependencies] = None) -> None:
        self.dependencies = dependencies or AppDependencies()
        self.mcp = FastMCP()
        self.mcp._handlers = {}  # type: ignore[attr-defined]

        if not hasattr(self.mcp, 'start'):
            async def default_start(host: str = "127.0.0.1", port: int = 8000) -> None:
                pass
            self.mcp.start = default_start  # type: ignore
        self._setup_server()

    def _setup_server(self) -> None:
        """Set up the FastMCP server with all required functionality by registering handlers."""

        auth_handlers = register_auth_handlers(
            self.mcp,
            self.dependencies.auth_adapter,
            self.dependencies.logging_adapter,
            self.dependencies
        )
        self.mcp._handlers.update(auth_handlers)  # type: ignore[attr-defined]


        monitoring_handlers = register_monitoring_handlers(
            self.mcp,
            self.dependencies.monitoring_adapter,
            self.dependencies.logging_adapter,
            self.dependencies.monitoring_adapter,
            self.dependencies
        )
        self.mcp._handlers.update(monitoring_handlers)  # type: ignore[attr-defined]

        self.dependencies.openapi_generator.update_mcp_server(self.mcp)
        self.dependencies.mcp_tools_docs_generator.set_mcp_server(self.mcp)

        doc_handlers = register_documentation_handlers(
            self.mcp,
            self.dependencies
        )
        self.mcp._handlers.update(doc_handlers)  # type: ignore[attr-defined]

    async def start_server(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Start the MCP server (for direct execution, not ASGI deployment)."""
        log_entry = self.dependencies.logging_adapter.create_log_entry(
            level="INFO",
            message="MCP Server starting (direct execution mode)",
            request_id="SERVER_START",
            latency_ms=0,
            endpoint="server",
            llm_model="N/A",
            extra={"host": host, "port": str(port)}
        )
        self.dependencies.logging_adapter.log_request(log_entry)

        await self.mcp.run_http_async(host=host, port=port, transport='http',
                                      uvicorn_config={'ws': None})

    def serve_with_uvicorn(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Serve the application using uvicorn (ASGI server)."""
        import uvicorn

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

        uvicorn.run(
            "src.app.main:create_app",
            host=host,
            port=port,
            factory=True,
            reload=False,
            log_level="info"
        )

    def get_app(self) -> FastMCP:
        """Get the FastMCP app instance."""
        return self.mcp


def create_app() -> FastMCP:
    """ASGI application factory that creates and returns the FastMCP ASGI app."""
    app = MCPServerApp()
    return app.get_app()


async def main() -> None:
    """Main entry point for the application."""
    app = MCPServerApp()

    host = settings.server_host
    port = settings.server_port

    await app.start_server(host=host, port=port)


if __name__ == "__main__":
    asyncio.run(main())