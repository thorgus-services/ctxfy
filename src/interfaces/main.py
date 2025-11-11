"""Main application entry point for the ctxfy MCP Server.

This module composes all the adapters and starts the MCP server
following the hexagonal architecture pattern.
"""

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING

from fastmcp.server import FastMCP

if TYPE_CHECKING:
    from fastmcp.server import Context

from src.infrastructure.llm.llm_adapter import LLMAdapter
from src.infrastructure.logging.structured_logger import StructuredLogger
from src.shell.orchestrators.orchestrator import MCPOrchestrator


async def main() -> None:
    """Main entry point for the ctxfy MCP Server."""
    # Initialize the structured logger
    logger = StructuredLogger(level="INFO")
    
    # Initialize the LLM adapter
    llm_adapter = LLMAdapter(default_model="default")
    
    # Initialize the orchestrator with adapters
    orchestrator = MCPOrchestrator(
        llm_adapter=llm_adapter,
        logging_adapter=logger
    )
    
    # Create the FastMCP server - this is our primary interface to MCP
    server = FastMCP(
        name="ctxfy-mcp-server",
        version="1.0.0"
    )
    
    # Register the health check endpoint
    @server.get("/health")  # type: ignore[attr-defined, misc]
    async def health_check() -> dict[str, str | float | int]:
        # Log the health check
        logger.log_health_check("healthy", 0)  # In a real implementation, track actual uptime
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": 0,  # In a real implementation, track actual uptime
            "version": "1.0.0"
        }
    
    # Register the example prompt that uses ctx.sample functionality
    @server.prompt("ctx.sample.example")
    async def sample_prompt(ctx: "Context", name: str = "world", topic: str = "general") -> str:
        """Example prompt that demonstrates ctx.sample functionality."""
        # Delegate to the orchestrator
        return await orchestrator.handle_sample_prompt(ctx, name, topic)
    
    # Start the server
    logger.log_health_check("starting", 0)
    server.run()


if __name__ == "__main__":
    asyncio.run(main())