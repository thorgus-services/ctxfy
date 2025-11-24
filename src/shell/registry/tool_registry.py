from typing import Dict

from fastmcp import FastMCP

from src.core.ports.specification_ports import SpecificationGenerationCommandPort


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, SpecificationGenerationCommandPort] = {}

    def register_tool(self, name: str, tool: SpecificationGenerationCommandPort) -> None:
        self._tools[name] = tool

    def register_all_to_mcp(self, mcp: FastMCP) -> None:
        for name, tool in self._tools.items():
            mcp.tool(
                name=name,
                description="Generates technical specifications from business requirements"
            )(tool.execute)

tool_registry = ToolRegistry()