from fastmcp import FastMCP

from src.core.use_cases.generate_specification import GenerateSpecificationUseCase
from src.core.use_cases.process_task_use_case import ProcessTaskUseCase
from src.shell.adapters.tools.process_task_tool import ProcessTaskTool
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
        # Register specification generation tool
        spec_use_case = GenerateSpecificationUseCase()
        spec_tool = SpecificationGenerationTool(use_case=spec_use_case)
        tool_registry.register_tool("generate_specification", spec_tool)

        # Register process task tool
        task_use_case = ProcessTaskUseCase()
        task_tool = ProcessTaskTool(use_case=task_use_case)
        tool_registry.register_tool("process_task", task_tool)

        tool_registry.register_all_to_mcp(self.mcp)

    def _setup_prompts(self) -> None:
        dynamic_prompt_registry.load_and_register_all_prompts(self.mcp)
