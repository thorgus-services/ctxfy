"""Core protocols for monitoring operations following our architectural patterns.

Primary ports (driving) are named with *CommandPort/*QueryPort convention.
Secondary ports (driven) are named with *GatewayPort/*RepositoryPort/*PublisherPort convention.
"""

from abc import abstractmethod
from typing import Dict, Optional

from src.core.models.monitoring_models import (
    HealthStatus,
    LogEntry,
    Metric,
    RequestMetrics,
)


class LoggingPort:
    """Primary port for logging operations - driving port following naming convention."""

    @abstractmethod
    def log_request(self, log_entry: LogEntry) -> None:
        """Log a structured request with required fields."""
        pass

    @abstractmethod
    def log_error(self, request_id: str, error: Exception, context: Dict[str, str]) -> None:
        """Log an error with structured information."""
        pass

    @abstractmethod
    def log_health_check(self, status: str, uptime_seconds: float) -> None:
        """Log a health check result."""
        pass

    @abstractmethod
    def create_log_entry(self, level: str, message: str, request_id: str, latency_ms: float,
                        user_id: Optional[str] = None, endpoint: Optional[str] = None,
                        llm_model: Optional[str] = None, extra: Optional[Dict[str, str]] = None) -> LogEntry:
        """Helper method to create a LogEntry instance with proper validation."""
        pass


class MetricsPort:
    """Primary port for metrics collection operations - driving port following naming convention."""

    @abstractmethod
    def record_prompt_execution(self, template_id: str, latency_ms: float, success: bool) -> None:
        """Record metrics for a prompt execution."""
        pass

    @abstractmethod
    def record_api_key_usage(self, api_key: str, endpoint: str) -> None:
        """Record usage metrics for an API key."""
        pass

    @abstractmethod
    def collect_metrics(self) -> Dict[str, Metric]:
        """Collect all available metrics."""
        pass

    @abstractmethod
    def record_request(self, request_metrics: RequestMetrics) -> None:
        """Record metrics for a specific request."""
        pass


class HealthQueryPort:
    """Primary port for health check operations - driving port following naming convention."""

    @abstractmethod
    async def get_health_status(self) -> HealthStatus:
        """Get the current health status of the system."""
        pass