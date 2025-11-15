"""LLM sampling adapter."""
import asyncio
from typing import Any, Dict, List, Optional

from src.core.ports.llm_ports import LLMPort


class LLMSampler(LLMPort):
    """Adapter for LLM sampling operations."""

    def __init__(self, ctx: Any = None, config: Optional[Dict[str, Any]] = None):
        self.ctx = ctx
        self.config = config or {}

    async def sample(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Sample from an LLM with the given prompt."""
        # In a real implementation, this would call an actual LLM
        # For now, just return a mock response
        return {
            "response": f"Mock response to: {prompt}",
            "model": "mock-llm",
            "tokens_used": 0,
            "success": True
        }

    async def batch_sample(self, prompts: List[str], params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Sample from an LLM with multiple prompts."""
        return [await self.sample(prompt, params) for prompt in prompts]

    # Additional methods required by tests
    async def sample_prompt(self, prompt: str, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 1000, timeout: Optional[float] = None) -> str:
        """Sample from an LLM with more parameters."""
        if self.ctx is None:
            raise RuntimeError("LLM sampling requires MCP context")

        try:
            # Use the ctx to make the actual call
            # If ctx has a sample method that takes the prompt and other parameters
            if hasattr(self.ctx, 'sample'):
                # Call the sample method with keyword arguments as expected by tests
                result = await self.ctx.sample(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # If the result is a string, return it directly
                if isinstance(result, str):
                    return result
                # If it's a dict with a response field, get the response
                elif isinstance(result, dict) and 'response' in result:
                    return result['response']
                else:
                    # Fallback to returning the result as-is
                    return str(result) if result is not None else "No response"
            else:
                # Mock implementation for test purposes
                return f"Response to: {prompt}"
        except asyncio.TimeoutError:
            raise RuntimeError("LLM sampling timed out") from None
        except Exception as e:
            raise RuntimeError(f"LLM sampling failed: {str(e)}") from e