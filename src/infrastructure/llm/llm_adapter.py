"""LLM adapter implementing the LLMAdapterPort protocol.

This adapter provides ctx.sample() functionality for LLM text generation
while maintaining proper logging and architecture boundaries.
"""

import asyncio

from fastmcp import Context

from src.core.ports.mcp_ports import LLMAdapterPort


class LLMAdapter(LLMAdapterPort):
    """Adapter for LLM sampling operations using the ctx.sample pattern."""
    
    def __init__(self, default_model: str = "default"):
        """Initialize the LLM adapter.
        
        Args:
            default_model: Default model to use if none specified
        """
        self.default_model = default_model
    
    async def sample_text(self, prompt: str, model: str = "default") -> str:
        """Sample text from an LLM with the provided prompt.
        
        Args:
            prompt: Input prompt for text generation
            model: LLM model to use (defaults to default_model)
            
        Returns:
            str: Generated text from the LLM
        """
        # In the actual FastMCP implementation, this would use the ctx.sample functionality
        # For now, we'll simulate the sampling with a simple echo
        # The actual implementation would happen in the orchestrator where ctx is available
        # since ctx is provided by the FastMCP framework during prompt execution
        
        # Simulate some processing time
        await asyncio.sleep(0.01)  # 10ms simulation delay
        
        # Return a simulated response
        # This is where actual LLM integration would happen
        # The actual implementation would use FastMCP's ctx.sample() function
        return f"Simulated response for prompt: {prompt[:50]}..."
    
    async def sample_text_with_context(self, ctx: Context, prompt: str, model: str = "default") -> str:
        """Sample text from an LLM using the FastMCP context.
        
        Args:
            ctx: FastMCP context object that provides the sample method
            prompt: Input prompt for text generation
            model: LLM model to use (defaults to default_model)
            
        Returns:
            str: Generated text from the LLM
        """
        # Use the actual FastMCP ctx.sample method
        # Note: The actual parameters would be different in real implementation
        result = await ctx.sample(messages=prompt, model_preferences=model)
        
        # Extract text content from the result appropriately
        # In a real implementation, we'd properly handle the content types
        if hasattr(result, 'text'):
            return result.text
        else:
            return str(result)