from typing import Any, Optional

from fastmcp import Context

from src.core.ports.generic_prompt_ports import GenericPromptCommandPort

from .yaml_prompt_loader import YAMLPromptLoader


class GenericYAMLPrompt(GenericPromptCommandPort):
    """
    Base class for prompts that use YAML configuration.
    Provides flexible parameter mapping using **kwargs.
    """

    def __init__(self, prompt_name: str, prompts_directory: Optional[str] = None):
        self.prompt_name = prompt_name
        self.yaml_loader = YAMLPromptLoader(prompts_directory)

    async def generate(self, ctx: Context, **kwargs: Any) -> str:
        """
        Generate a prompt using flexible parameters.

        Args:
            ctx: FastMCP context
            **kwargs: Parameters to format the prompt template

        Returns:
            Formatted prompt string
        """
        # Format and return the prompt using provided kwargs
        formatted_prompt = self.yaml_loader.format_prompt(self.prompt_name, **kwargs)

        if formatted_prompt is None:
            raise ValueError(f"Prompt '{self.prompt_name}' not found or could not be loaded")

        return formatted_prompt