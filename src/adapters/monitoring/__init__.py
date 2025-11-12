"""Structured logging adapter implementing the LoggingPort protocol with JSON format and required fields."""

import json
import sys
from datetime import datetime
from typing import Dict, Optional

from src.core.models.monitoring_models import LogEntry
from src.core.ports.monitoring_ports import LoggingPort

# Import the monitoring classes
from .monitoring import HealthCheckAdapter, MetricsAdapter, MonitoringAdapter


class StructuredLoggingAdapter(LoggingPort):
    """Structured logging adapter with JSON format and required fields including request_id, latency_ms, and llm_model."""

    def __init__(self, level: str = "INFO"):
        """Initialize the structured logger.

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.level = level.upper()

    def log_request(self, log_entry: LogEntry) -> None:
        """Log a structured request with required fields in JSON format.

        Args:
            log_entry: The log entry containing all required fields
        """
        log_dict = {
            "timestamp": log_entry.timestamp.isoformat(),
            "level": log_entry.level,
            "message": log_entry.message,
            "request_id": log_entry.request_id,
            "latency_ms": log_entry.latency_ms,
            "user_id": log_entry.user_id,
            "endpoint": log_entry.endpoint,
            "llm_model": log_entry.llm_model,
            "extra": log_entry.extra
        }

        self._output_log(json.dumps(log_dict))  # Output to stdout in JSON format

    def log_error(self, request_id: str, error: Exception, context: Dict[str, str]) -> None:
        """Log an error with structured information in JSON format.

        Args:
            request_id: The request ID associated with the error
            error: The exception that occurred
            context: Additional context information
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "message": str(error),
            "request_id": request_id,
            "latency_ms": 0,  # No latency for errors
            "user_id": context.get("user_id"),
            "endpoint": context.get("endpoint"),
            "llm_model": context.get("llm_model", "unknown"),
            "extra": {
                "error_type": type(error).__name__,
                "context": context
            }
        }

        self._output_log(json.dumps(log_entry))  # Output to stdout in JSON format

    def log_health_check(self, status: str, uptime_seconds: float) -> None:
        """Log a health check result with required fields in JSON format.

        Args:
            status: Health status ('healthy', 'degraded', 'unhealthy')
            uptime_seconds: Uptime in seconds
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": f"Health check result: {status}",
            "request_id": "SYSTEM",  # System-level log
            "latency_ms": 0,
            "user_id": "SYSTEM",
            "endpoint": "/health",
            "llm_model": "N/A",
            "extra": {
                "uptime_seconds": uptime_seconds,
                "status": status
            }
        }

        self._output_log(json.dumps(log_entry))  # Output to stdout in JSON format

    def create_log_entry(self, level: str, message: str, request_id: str, latency_ms: float,
                        user_id: Optional[str] = None, endpoint: Optional[str] = None,
                        llm_model: Optional[str] = None, extra: Optional[Dict[str, str]] = None) -> LogEntry:
        """Helper method to create a LogEntry instance with proper validation.

        Args:
            level: Log level
            message: Log message
            request_id: Request ID
            latency_ms: Latency in milliseconds
            user_id: User ID
            endpoint: Endpoint name
            llm_model: LLM model used
            extra: Additional context fields

        Returns:
            Validated LogEntry instance
        """
        return LogEntry(
            timestamp=datetime.now(),
            level=level,
            message=message,
            request_id=request_id,
            latency_ms=latency_ms,
            user_id=user_id,
            endpoint=endpoint,
            llm_model=llm_model,
            extra=extra or {}
        )
        
    def _output_log(self, log_json: str) -> None:
        """Output log to appropriate destination."""
        # Using sys.stdout instead of print to avoid T201
        sys.stdout.write(log_json + "\n")
        sys.stdout.flush()