from typing import Any, Callable, cast

from fastmcp import FastMCP as Server


def _preserve_function_metadata(target_func: Any, source_func: Callable[..., Any]) -> None:
    """
    Preserves function metadata (name and doc) from source function to target function.

    Args:
        target_func: The function/object to copy metadata to
        source_func: The function to copy metadata from
    """
    # Try to preserve the function name
    if hasattr(target_func, '__name__'):
        try:
            target_func.__name__ = source_func.__name__
        except AttributeError:
            # Some objects may have read-only __name__, so ignore if we can't set it
            pass

    # Try to preserve the function docstring
    if hasattr(target_func, '__doc__'):
        try:
            target_func.__doc__ = source_func.__doc__
        except AttributeError:
            # Some objects may have read-only __doc__, so ignore if we can't set it
            pass


class MCPPromptAdapter:
    """Implements @mcp.prompt decorator following FastMCP specifications"""

    def __init__(self, server: Server):
        self.server = server

    def prompt(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator for registering server-side prompt templates with FastMCP"""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            # Create wrapper function first
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

            # Register the wrapper with FastMCP to get the registered function
            registered_func = self.server.prompt(name)(wrapper)

            # Preserve original function metadata (name and doc) on the registered function
            _preserve_function_metadata(registered_func, func)

            # Return with proper type cast to satisfy mypy
            return cast(Callable[..., Any], registered_func)

        return decorator


# Global instance to be used by the application
def create_prompt_decorator(server: Server) -> Callable[[str], Callable[[Callable[..., Any]], Callable[..., Any]]]:
    """Factory function to create the prompt decorator with the server instance"""
    adapter = MCPPromptAdapter(server)
    return adapter.prompt