import asyncio
import time
from typing import Any


class LLMSampler:
    """Provides ctx.sample() interface wrapper with error handling and performance monitoring"""
    
    def __init__(self, ctx: Any = None) -> None:
        self.ctx = ctx
    
    async def sample_prompt(
        self, 
        prompt: str, 
        model: str = "gpt-4o", 
        temperature: float = 0.7, 
        max_tokens: int = 1000,
        timeout: float = 30.0
    ) -> Any:
        """Sample LLM with the given prompt and parameters"""
        if self.ctx is None:
            raise RuntimeError("LLM sampling requires MCP context (ctx)")
        
        start_time = time.time()
        
        try:
            # Directly call the ctx.sample() method with provided parameters
            result = await self.ctx.sample(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return result
            
        except asyncio.TimeoutError as e:
            execution_time = (time.time() - start_time) * 1000
            raise Exception(f"LLM sampling timed out after {timeout}s (executed for {execution_time:.2f}ms)") from e
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise Exception(f"LLM sampling failed: {str(e)} (executed for {execution_time:.2f}ms)") from e
    

    
