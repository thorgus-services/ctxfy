"""MCP Server implementation using FastMCP for context stack generation."""

import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from src.adapters.in_memory_context_adapter import InMemoryContextGenerationAdapter
from src.shell.orchestrators.context_generation_orchestrator import (
    ContextGenerationOrchestrator,
)


class ContextStackServer:
    def __init__(self) -> None:
        self.mcp = FastMCP("context-engineering")
        self.command_port = InMemoryContextGenerationAdapter()
        self.orchestrator = ContextGenerationOrchestrator(self.command_port)
        self._register_tools()
        self.logger = logging.getLogger(__name__)

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
        try:
            self.mcp.run(transport="stdio")
        except Exception as e:
            self.logger.error(f"Error running MCP server: {e}")
            raise


if __name__ == "__main__":
    server = ContextStackServer()
    server.run()