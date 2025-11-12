"""FastMCP authentication middleware for API key validation."""

from typing import Any, Awaitable, Callable

from fastmcp.server import Context

from src.adapters.auth import ApiKeyAuthAdapter
from src.core.models.auth_models import AuthResult


class AuthMiddleware:
    """API key authentication middleware for FastMCP server."""

    def __init__(self, auth_adapter: ApiKeyAuthAdapter):
        self.auth_adapter = auth_adapter

    async def authenticate_request(self, ctx: Context, next_handler: Callable[..., Awaitable[Any]]) -> Any:
        """Authenticate the request using API key from headers."""
        # Extract API key from headers
        api_key: str | None = None
        if hasattr(ctx, 'headers'):
            # Try common header names for API keys
            for header_name in ['authorization', 'x-api-key', 'api-key']:
                if header_name in ctx.headers:
                    header_value = ctx.headers[header_name]
                    # Handle Bearer token format
                    if header_value.lower().startswith('bearer '):
                        api_key = header_value[7:].strip()
                    else:
                        api_key = header_value
                    break

        # Validate the API key - pass empty string if none found to avoid type error
        auth_result: AuthResult = await self.auth_adapter.validate_api_key(api_key or "")

        if not auth_result.is_authenticated:
            # Return error response
            return {
                "error": "Authentication failed",
                "message": auth_result.error_message or "Invalid or missing API key"
            }

        # Add user info to context for the next handler
        # Note: We can't directly set attributes on Context, so we'll need to handle this differently
        # For now, return error if trying to set custom attributes on FastMCP Context
        # In a real implementation, you'd likely store this in a request-scoped storage mechanism

        # Call the next handler
        return await next_handler(ctx)

    def create_auth_decorator(self, required_scope: str = "read") -> Callable[..., Any]:
        """Create an authentication decorator for specific routes."""
        async def auth_wrapper(handler_func: Callable[..., Any]) -> Callable[..., Any]:
            async def authenticated_handler(ctx: Context, *args: Any, **kwargs: Any) -> Any:
                # Extract API key from headers
                api_key: str | None = None
                if hasattr(ctx, 'headers'):
                    for header_name in ['authorization', 'x-api-key', 'api-key']:
                        if header_name in ctx.headers:
                            header_value = ctx.headers[header_name]
                            if header_value.lower().startswith('bearer '):
                                api_key = header_value[7:].strip()
                            else:
                                api_key = header_value
                            break

                # Validate the API key
                auth_result: AuthResult = await self.auth_adapter.validate_api_key(api_key or "")

                if not auth_result.is_authenticated:
                    return {
                        "error": "Authentication failed",
                        "message": auth_result.error_message or "Invalid or missing API key"
                    }

                # Check scope if required
                if required_scope and auth_result.scope != "admin" and auth_result.scope != required_scope:
                    return {
                        "error": "Insufficient permissions",
                        "message": f"Required scope: {required_scope}, your scope: {auth_result.scope}"
                    }

                # In a real implementation, you'd store auth info in request-scoped storage
                # rather than trying to add attributes to the FastMCP Context object

                # Call the original handler
                return await handler_func(ctx, *args, **kwargs)

            return authenticated_handler

        return auth_wrapper