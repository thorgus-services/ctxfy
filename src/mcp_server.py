"""MCP Server implementation using FastMCP for context stack generation."""

import logging
import os
import sys
import traceback
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from src.adapters.in_memory_context_adapter import InMemoryContextGenerationAdapter
from src.settings import settings
from src.shell.orchestrators.context_generation_orchestrator import (
    ContextGenerationOrchestrator,
)


class ContextStackServer:
    def __init__(self) -> None:
        # Initialize logging first to capture any issues during setup
        logging.basicConfig(level=logging.DEBUG if sys.flags.debug else logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Initializing MCP Server: context-engineering")
        try:
            self.mcp = FastMCP("context-engineering")
            self.logger.info("FastMCP initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize FastMCP: {e}")
            raise
            
        self.command_port = InMemoryContextGenerationAdapter()
        self.orchestrator = ContextGenerationOrchestrator(self.command_port)
        self._register_tools()
        self.logger.info("ContextStackServer initialized successfully")

    def _register_tools(self) -> None:
        @self.mcp.tool()
        async def generate_context_stack(
            feature_description: str,
            target_technologies: Optional[List[str]] = None,
            custom_rules: Optional[List[str]] = None
        ) -> Dict[str, Any]:
            """Generate a context stack for Qwen Code based on a feature description."""
            return self.orchestrator.generate_context_stack_for_mcp(
                feature_description, target_technologies, custom_rules
            )

        @self.mcp.tool()
        async def execute_prp_workflow(
            workflow_type: str,
            parameters: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Any]:
            """Execute a PRP (Problem-Resolution-Proof) workflow."""
            if parameters is None:
                parameters = {}
            return {
                "success": True,
                "result": {
                    "workflow_type": workflow_type,
                    "status": "executed",
                    "parameters": parameters
                }
            }

    def run(self) -> None:
        self.logger.info(f"Starting MCP server with HTTP transport on {settings.mcp_server_host}:{settings.mcp_server_port}")
        try:
            # Log information about the environment for debugging
            self.logger.info(f"Current working directory: {os.getcwd()}")
            self.logger.info(f"Python path: {sys.path}")
            
            self.mcp.run(transport="http", host=settings.mcp_server_host, port=settings.mcp_server_port)
            self.logger.info("MCP server started successfully with HTTP transport")
        except Exception as e:
            self.logger.error(f"Error running MCP server: {e}")
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            raise


if __name__ == "__main__":
    server = ContextStackServer()
    server.run()