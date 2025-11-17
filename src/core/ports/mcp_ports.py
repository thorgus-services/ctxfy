"""Core protocols for MCP server functionality following our architectural patterns.

Primary ports (driving) are named with *CommandPort/*QueryPort convention.
Secondary ports (driven) are named with *GatewayPort/*RepositoryPort/*PublisherPort convention.
"""

from typing import Protocol


class MCPLoggingPort(Protocol):
    """Secondary port for MCP-specific logging operations - driven port following naming convention."""

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