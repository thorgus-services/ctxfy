"""Metrics collection and health monitoring adapter implementing the MetricsPort and HealthQueryPort protocols."""

from datetime import datetime
from typing import Dict, Optional

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

from src.core.models.monitoring_models import HealthStatus, Metric, RequestMetrics
from src.core.ports.monitoring_ports import HealthQueryPort, MetricsPort


class MetricsAdapter(MetricsPort):
    """Metrics collection adapter implementing the MetricsPort protocol with Prometheus integration."""

    def __init__(self) -> None:
        # Create a new registry for this instance to avoid duplicate metrics
        self.registry = CollectorRegistry()

        # Initialize Prometheus metrics
        self.prompt_execution_counter = Counter(
            'prompt_executions_total',
            'Total number of prompt executions',
            labelnames=['template_id', 'success'],
            registry=self.registry
        )

        self.prompt_execution_histogram = Histogram(
            'prompt_execution_duration_seconds',
            'Prompt execution time in seconds',
            labelnames=['template_id'],
            registry=self.registry
        )

        self.api_key_usage_counter = Counter(
            'api_key_usage_total',
            'Total API key usage',
            labelnames=['api_key', 'endpoint'],
            registry=self.registry
        )

        self.request_counter = Counter(
            'requests_total',
            'Total requests processed',
            labelnames=['endpoint', 'method', 'status_code'],
            registry=self.registry
        )

        self.request_duration_histogram = Histogram(
            'request_duration_seconds',
            'Request duration in seconds',
            labelnames=['endpoint', 'method'],
            registry=self.registry
        )

        self.active_requests_gauge = Gauge(
            'active_requests',
            'Number of active requests',
            registry=self.registry
        )

    def record_prompt_execution(self, template_id: str, latency_ms: float, success: bool) -> None:
        """Record metrics for a prompt execution."""
        # Increment execution counter
        self.prompt_execution_counter.labels(
            template_id=template_id,
            success=str(success).lower()
        ).inc()

        # Record execution time (convert ms to seconds for Prometheus)
        self.prompt_execution_histogram.labels(
            template_id=template_id
        ).observe(latency_ms / 1000.0)

    def record_api_key_usage(self, api_key: str, endpoint: str) -> None:
        """Record usage metrics for an API key."""
        # Increment API key usage counter
        self.api_key_usage_counter.labels(
            api_key=api_key[:8] + '...' if len(api_key) > 8 else api_key,  # Obfuscate key
            endpoint=endpoint
        ).inc()

    def collect_metrics(self) -> Dict[str, Metric]:
        """Collect all available metrics."""
        # This method returns metrics in our internal format
        # For Prometheus integration, use generate_latest() to get the raw metrics
        return {}

    def record_request(self, request_metrics: RequestMetrics) -> None:
        """Record metrics for a specific request."""
        # Increment request counter
        self.request_counter.labels(
            endpoint=request_metrics.endpoint,
            method=request_metrics.method,
            status_code=str(request_metrics.status_code)
        ).inc()

        # Record request duration (convert ms to seconds for Prometheus)
        self.request_duration_histogram.labels(
            endpoint=request_metrics.endpoint,
            method=request_metrics.method
        ).observe(request_metrics.latency_ms / 1000.0)

    def get_prometheus_metrics(self) -> bytes:
        """Get metrics in Prometheus format."""
        return generate_latest(self.registry)

    def get_prometheus_content_type(self) -> str:
        """Get the content type for Prometheus metrics."""
        return CONTENT_TYPE_LATEST


class HealthCheckAdapter(HealthQueryPort):
    """Health check adapter implementing the HealthQueryPort protocol."""

    def __init__(self, start_time: Optional[datetime] = None) -> None:
        self.start_time = start_time or datetime.now()

    async def get_health_status(self) -> HealthStatus:
        """Get the current health status of the system."""
        # Calculate uptime
        uptime = datetime.now() - self.start_time
        uptime_seconds = uptime.total_seconds()

        # Perform basic checks (in a real implementation, you'd check dependencies)
        checks = {
            "uptime": {
                "status": "ok",
                "uptime_seconds": uptime_seconds
            },
            "dependencies": {
                "status": "ok",  # In a real implementation, check actual dependencies
                "timestamp": datetime.now().isoformat()
            }
        }

        # Determine overall status (in a real implementation, check if any critical checks failed)
        overall_status = "healthy"  # Assume healthy if all checks pass

        return HealthStatus(
            status=overall_status,
            timestamp=datetime.now(),
            uptime_seconds=uptime_seconds,
            version="1.0.0",
            checks=checks
        )

    def get_uptime_seconds(self) -> float:
        """Get the current uptime in seconds."""
        uptime = datetime.now() - self.start_time
        return uptime.total_seconds()


class MonitoringAdapter(MetricsAdapter, HealthCheckAdapter):
    """Combined monitoring adapter implementing both metrics and health check functionality."""

    def __init__(self, start_time: Optional[datetime] = None) -> None:
        MetricsAdapter.__init__(self)
        HealthCheckAdapter.__init__(self, start_time)