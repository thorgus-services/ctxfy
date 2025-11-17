"""Authentication handlers for the ctxfy MCP Server."""

from typing import TYPE_CHECKING, Annotated, Any, Dict, Optional

from fastmcp import FastMCP
from pydantic import Field

from src.core.models.error_models import ApplicationError, ErrorCodes
from src.core.ports.auth_ports import AuthCommandPort
from src.core.ports.monitoring_ports import LoggingPort
from src.shell.orchestrators.auth_orchestrator import AuthOrchestrator

if TYPE_CHECKING:
    pass


def register_auth_handlers(
    mcp: FastMCP,
    auth_command_port: AuthCommandPort,
    logging_adapter: LoggingPort,
    dependencies: Any
) -> Dict[str, Any]:
    """Register authentication-related handlers with the FastMCP server."""
    handlers = {}

    auth_orchestrator = AuthOrchestrator(auth_command_port, logging_adapter)

    async def create_api_key(
        ctx: Any,
        user_id: Annotated[str, Field(
            description="Unique identifier for the user requesting the API key"
        )],
        scope: Annotated[str, Field(
            description="Access scope for the API key",
            default="read"
        )] = "read",
        ttl_hours: Annotated[Optional[int], Field(
            description="Time-to-live in hours for the API key",
            default=None
        )] = None
    ) -> Dict[str, Any]:
        """Create a new API key for authentication."""
        request_id = f"req-{id(ctx)}" if ctx else f"api-key-{user_id}"

        try:
            result = await auth_orchestrator.create_api_key(user_id, scope, ttl_hours)
            return result
        except Exception as e:
            logging_adapter.log_error(
                request_id=request_id,
                error=e,
                context={
                    "endpoint": "create-api-key",
                    "user_id": user_id
                }
            )

            error = ApplicationError(
                error_code=ErrorCodes.INTERNAL_ERROR,
                message=str(e),
                details=str(type(e).__name__),
                request_id=request_id
            )

            return {
                "success": False,
                "error": {
                    "message": error.message,
                    "error_code": error.error_code.value if hasattr(error.error_code, 'value') else str(error.error_code),
                    "request_id": error.request_id,
                    "details": []
                }
            }

    handlers['create-api-key'] = {'fn': create_api_key}

    mcp.tool(
        name="create-api-key",
        description="Create a new API key for authentication.",
        tags={"auth", "security"},
        annotations={
            "title": "Create API Key",
            "readOnlyHint": False,
            "destructiveHint": False
        }
    )(create_api_key)

    return handlers