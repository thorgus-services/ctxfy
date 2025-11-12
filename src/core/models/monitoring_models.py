"""Immutable value objects for monitoring and logging operations following our core architecture principles."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class LogEntry:
    """Immutable value object for structured logging following our core architecture principles."""
    timestamp: datetime
    level: str  # INFO, ERROR, DEBUG, WARNING
    message: str
    request_id: str
    latency_ms: float
    user_id: Optional[str] = None
    endpoint: Optional[str] = None
    llm_model: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if self.level not in ['INFO', 'ERROR', 'DEBUG', 'WARNING', 'CRITICAL']:
            raise ValueError("Log level must be INFO, ERROR, DEBUG, WARNING, or CRITICAL")
        if not self.message or not isinstance(self.message, str):
            raise ValueError("Message must be a valid string")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")
        if not isinstance(self.latency_ms, (int, float)) or self.latency_ms < 0:
            raise ValueError("Latency must be a non-negative number")
        if self.extra is None:
            raise ValueError("Extra fields must be a dictionary")


@dataclass(frozen=True)
class Metric:
    """Immutable value object for metrics collection following our core architecture principles."""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Metric name must be a valid string")
        if not isinstance(self.value, (int, float)):
            raise ValueError("Metric value must be a number")
        if not isinstance(self.labels, dict):
            raise ValueError("Labels must be a dictionary")


@dataclass(frozen=True)
class HealthStatus:
    """Immutable value object for health status following our core architecture principles."""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    timestamp: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0
    version: str = "1.0.0"
    checks: Dict[str, Any] = field(default_factory=dict)  # Detailed health checks

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if self.status not in ['healthy', 'degraded', 'unhealthy']:
            raise ValueError("Status must be 'healthy', 'degraded', or 'unhealthy'")
        if self.uptime_seconds < 0:
            raise ValueError("Uptime must be non-negative")
        if not self.version or not isinstance(self.version, str):
            raise ValueError("Version must be a valid string")


@dataclass(frozen=True)
class RequestMetrics:
    """Immutable value object for request-specific metrics following our core architecture principles."""
    request_id: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: float
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")
        if not self.endpoint or not isinstance(self.endpoint, str):
            raise ValueError("Endpoint must be a valid string")
        if not self.method or not isinstance(self.method, str):
            raise ValueError("Method must be a valid string")
        if not isinstance(self.status_code, int) or self.status_code < 100 or self.status_code > 599:
            raise ValueError("Status code must be a valid HTTP status code")
        if not isinstance(self.latency_ms, (int, float)) or self.latency_ms < 0:
            raise ValueError("Latency must be a non-negative number")