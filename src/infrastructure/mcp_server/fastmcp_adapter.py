"""FastMCP integration adapter implementing MCP server functionality.

This adapter implements the MCPHealthQueryPort protocol to integrate 
with health checking functionality. The actual server is handled in main.py
since FastMCP is designed as a framework rather than an injectable component.
"""

from datetime import datetime
from typing import Optional

from src.core.models.mcp_models import HealthStatus
from src.core.ports.mcp_ports import (
    MCPHealthQueryPort,
)
from src.core.use_cases.mcp_use_cases import calculate_health_status


class FastMCPServerAdapter(MCPHealthQueryPort):
    """Adapter that implements MCP health check functionality."""
    
    def __init__(self, start_time: Optional[datetime] = None):
        """Initialize the FastMCP server adapter.
        
        Args:
            start_time: When the server started (for health checks)
        """
        self.start_time = start_time or datetime.now()
    
    async def get_health_status(self) -> HealthStatus:
        """Get the current health status of the MCP server."""
        return calculate_health_status(self.start_time)