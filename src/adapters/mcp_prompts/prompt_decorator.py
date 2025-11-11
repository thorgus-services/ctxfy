import functools
from typing import Any, Callable

from fastmcp import Server


class MCPPromptAdapter:
    """Implements @mcp.prompt decorator following FastMCP specifications"""
    
    def __init__(self, server: Server):
        self.server = server
        
    def prompt(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator for registering server-side prompt templates with FastMCP"""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            # Register the prompt with FastMCP
            @self.server.prompt(name)
            async def wrapper(ctx: Any, **kwargs: Any) -> Any:
                """Wrapper that handles the MCP prompt execution"""
                try:
                    # Execute the request using core use case
                    # This is a simplified implementation - in practice, this would coordinate
                    # with the various adapters to perform the complete operation
                    # result = execute_prompt_request(request)
                    
                    # The actual execution would involve:
                    # 1. Template retrieval from registry
                    # 2. Variable validation
                    # 3. Template substitution
                    # 4. LLM sampling via ctx.sample()
                    
                    # For now, just call the original function to simulate the behavior
                    return await func(ctx, **kwargs)
                    
                except Exception as e:
                    # Handle errors appropriately
                    raise e
            
            # Preserve original function metadata
            functools.update_wrapper(wrapper, func)
            return wrapper
        
        return decorator


# Global instance to be used by the application
def create_prompt_decorator(server: Server) -> Callable[[str], Callable[[Callable[..., Any]], Callable[..., Any]]]:
    """Factory function to create the prompt decorator with the server instance"""
    adapter = MCPPromptAdapter(server)
    return adapter.prompt