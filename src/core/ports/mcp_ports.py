"""Core protocols for MCP server functionality following our architectural patterns.

Primary ports (driving) are named with *CommandPort/*QueryPort convention.
Secondary ports (driven) are named with *GatewayPort/*RepositoryPort/*PublisherPort convention.
"""

from typing import TYPE_CHECKING, Awaitable, Callable, Protocol

from src.core.models.mcp_models import HealthStatus

if TYPE_CHECKING:
    from fastmcp.server import Context


class MCPServerCommandPort(Protocol):
    """Primary port for MCP server operations - driving port following naming convention."""
    
    async def register_prompt_handler(self, name: str, handler: Callable[..., Awaitable[None]]) -> None:
        """Register a prompt handler with the MCP server."""
        ...
    
    async def start_server(self) -> None:
        """Start the MCP server."""
        ...


class MCPHealthQueryPort(Protocol):
    """Primary port for health check operations - driving port following naming convention."""
    
    async def get_health_status(self) -> HealthStatus:
        """Get the current health status of the MCP server."""
        ...


class LLMAdapterPort(Protocol):
    """Secondary port for LLM operations - driven port following naming convention."""
    
    async def sample_text(self, prompt: str, model: str = "default") -> str:
        """Sample text from an LLM with the provided prompt."""
        ...

    async def sample_text_with_context(self, ctx: "Context", prompt: str, model: str = "default") -> str:
        """Sample text from an LLM using the FastMCP context."""
        ...


class LoggingPort(Protocol):
    """Secondary port for logging operations - driven port following naming convention."""
    
    def log_prompt_request(
        self, 
        prompt_id: str, 
        name: str, 
        latency_ms: float, 
        llm_model: str
    ) -> None:
        """Log a prompt request with required fields."""
        ...

    def log_error(
        self,
        prompt_id: str,
        name: str,
        error: Exception,
        llm_model: str
    ) -> None:
        """Log an error with required fields."""
        ...