from fastmcp import FastMCP

from src.core.use_cases.generate_specification import GenerateSpecificationUseCase
from src.shell.adapters.tools.specification_generation_tool import (
    SpecificationGenerationTool,
)
from src.shell.registry.dynamic_prompt_registry import dynamic_prompt_registry
from src.shell.registry.tool_registry import tool_registry


class MCPOrchestrator:
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self._initialize_components()

    def _initialize_components(self) -> None:
        self._setup_tools()
        self._setup_prompts()

    def _setup_tools(self) -> None:
        use_case = GenerateSpecificationUseCase()
        tool = SpecificationGenerationTool(use_case=use_case)
        tool_registry.register_tool("generate_specification", tool)
        tool_registry.register_all_to_mcp(self.mcp)

    def _setup_prompts(self) -> None:
        dynamic_prompt_registry.load_and_register_all_prompts(self.mcp)
