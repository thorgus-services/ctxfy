"""Application orchestrator implementing the hexagonal architecture.

This orchestrator coordinates between the core use cases and the adapters,
implementing the Imperative Shell part of the Functional Core & Imperative Shell pattern.
"""

from src.core.ports.mcp_ports import MCPLoggingPort


class MCPOrchestrator:
    """Orchestrator that coordinates between core use cases and adapters.

    This implements the Imperative Shell pattern with no business logic,
    maximum 4 dependencies, and coordinates I/O operations.
    """

    def __init__(
        self,
        logging_adapter: MCPLoggingPort
    ):
        """Initialize the orchestrator with required adapters.

        Args:
            logging_adapter: Adapter for logging operations
        """
        if len(locals()) > 3:  # self + 2 dependencies (max 4 total per orchestrator pattern)
            raise ValueError("Orchestrator should have maximum 2 dependencies (including self)")

        self.logging_adapter = logging_adapter
    
