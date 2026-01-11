from typing import Dict, Union

from fastmcp import FastMCP

from src.core.ports.specification_ports import SpecificationGenerationCommandPort
from src.core.ports.task_ports import ProcessTaskCommandPort

# Union type for all supported tool types
ToolType = Union[SpecificationGenerationCommandPort, ProcessTaskCommandPort]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolType] = {}

    def register_tool(self, name: str, tool: ToolType) -> None:
        self._tools[name] = tool

    def register_all_to_mcp(self, mcp: FastMCP) -> None:
        for name, tool in self._tools.items():
            # Get the description from the tool's docstring or use a generic one
            description = getattr(tool, '__doc__', f"Tool for {name}")
            if not description or description == object.__doc__:
                # Provide default descriptions based on tool name
                if name == "generate_specification":
                    description = "Generates technical specifications from business requirements"
                elif name == "process_task":
                    description = "Processes markdown files containing user stories or tasks"
                else:
                    description = f"Tool for {name}"

            mcp.tool(
                name=name,
                description=description
            )(tool.execute)

tool_registry = ToolRegistry()