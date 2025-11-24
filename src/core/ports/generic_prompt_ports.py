from typing import Any, Protocol

from fastmcp import Context


class GenericPromptCommandPort(Protocol):
    """
    Generic protocol for prompt commands that can accept flexible parameters.
    This allows different prompts to be called with different parameter sets
    without needing specific protocol definitions for each prompt type.
    """
    
    async def generate(self, ctx: Context, **kwargs: Any) -> str:
        """
        Generate a prompt using flexible parameters.
        
        Args:
            ctx: FastMCP context
            **kwargs: Flexible parameters that will be used to format the prompt template
            
        Returns:
            Formatted prompt string
        """
        ...