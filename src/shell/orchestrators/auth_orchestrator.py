"""Auth orchestrator implementing Imperative Shell pattern for authentication operations."""

from typing import Any, Dict, Optional

from src.core.models.auth_models import ApiKeyRequest
from src.core.ports.auth_ports import AuthCommandPort
from src.core.ports.monitoring_ports import LoggingPort


class AuthOrchestrator:
    """Orchestrator for authentication operations using the Imperative Shell pattern."""

    def __init__(
        self,
        auth_command_port: AuthCommandPort,
        logging_adapter: LoggingPort
    ) -> None:
        if len(locals()) > 4:  # self + 2 dependencies
            raise ValueError("Orchestrator should have maximum 3 dependencies (4 including self)")

        self.auth_command_port = auth_command_port
        self.logging_adapter = logging_adapter

    async def create_api_key(
        self,
        user_id: str,
        scope: str = "read",
        ttl_hours: Optional[int] = None
    ) -> Dict[str, Any]:
        """Orchestrate the creation of an API key."""
        request_id = f"api-key-{user_id}"

        try:
            api_key_request = ApiKeyRequest(
                user_id=user_id,
                scope=scope,
                ttl_hours=ttl_hours
            )

            new_key = await self.auth_command_port.create_api_key(api_key_request)

            log_entry = self.logging_adapter.create_log_entry(
                level="INFO",
                message="API key created successfully",
                request_id=api_key_request.request_id,
                latency_ms=0,
                user_id=user_id,
                endpoint="create-api-key"
            )
            self.logging_adapter.log_request(log_entry)

            return {"api_key": new_key, "key_id": api_key_request.request_id}
        except Exception as e:
            self.logging_adapter.log_error(
                request_id=request_id,
                error=e,
                context={
                    "endpoint": "create-api-key",
                    "user_id": user_id
                }
            )

            return {
                "success": False,
                "error": {
                    "message": str(e),
                    "request_id": request_id,
                    "details": []
                }
            }