"""Health and monitoring handlers for the ctxfy MCP Server."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.core.models.error_models import ApplicationError, ErrorCodes
from src.core.ports.monitoring_ports import LoggingPort

if TYPE_CHECKING:
    pass


def register_monitoring_handlers(
    mcp: FastMCP,
    monitoring_adapter: Any,
    logging_adapter: LoggingPort,
    monitoring_port: Any,
    dependencies: Any
) -> Dict[str, Any]:
    """Register health and monitoring handlers with the FastMCP server."""
    handlers: Dict[str, Any] = {}

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        """Health check endpoint returning system status."""
        try:
            health_status = await monitoring_adapter.get_health_status()
            return JSONResponse({
                "status": health_status.status,
                "timestamp": health_status.timestamp.isoformat(),
                "uptime_seconds": health_status.uptime_seconds,
                "version": health_status.version,
                "checks": health_status.checks,
                "service": "ctxfy-mcp-server"
            })
        except Exception as e:
            request_id = "health-check"
            logging_adapter.log_error(
                request_id=request_id,
                error=e,
                context={
                    "endpoint": "health",
                }
            )

            error = ApplicationError(
                error_code=ErrorCodes.INTERNAL_ERROR,
                message="Health check failed",
                details=str(e),
                request_id=request_id
            )

            return JSONResponse({
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": error.message,
                "error_code": error.error_code.value if hasattr(error.error_code, 'value') else str(error.error_code),
                "service": "ctxfy-mcp-server"
            }, status_code=500)

    @mcp.custom_route("/metrics", methods=["GET"])
    async def metrics_endpoint(request: Request) -> Response:
        """Metrics endpoint returning Prometheus-formatted metrics."""
        try:
            metrics_data = dependencies.monitoring_adapter.get_prometheus_metrics()
            return Response(
                content=metrics_data.decode('utf-8'),
                media_type="text/plain; version=0.0.4; charset=utf-8"
            )
        except Exception as e:
            request_id = "metrics-check"
            logging_adapter.log_error(
                request_id=request_id,
                error=e,
                context={
                    "endpoint": "metrics",
                }
            )

            error = ApplicationError(
                error_code=ErrorCodes.INTERNAL_ERROR,
                message="Metrics collection failed",
                details=str(e),
                request_id=request_id
            )

            error_code_value = error.error_code.value if hasattr(error.error_code, 'value') else str(error.error_code)
            return Response(
                content=f"# Error collecting metrics: {error.message} (code: {error_code_value})",
                status_code=500,
                media_type="text/plain; charset=utf-8"
            )

    return handlers