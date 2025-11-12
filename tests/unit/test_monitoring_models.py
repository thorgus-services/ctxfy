"""Unit tests for monitoring models following TDD principles."""

from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from src.core.models.monitoring_models import (
    HealthStatus,
    LogEntry,
    Metric,
    RequestMetrics,
)


class TestLogEntry:
    """Test log entry value object."""

    def test_log_entry_creation(self):
        """Test creating a valid LogEntry."""
        now = datetime.now()
        log_entry = LogEntry(
            timestamp=now,
            level="INFO",
            message="Test message",
            request_id="test-request-id",
            latency_ms=100.0,
            user_id="test-user",
            endpoint="/test",
            llm_model="gpt-4"
        )

        assert log_entry.timestamp == now
        assert log_entry.level == "INFO"
        assert log_entry.message == "Test message"
        assert log_entry.request_id == "test-request-id"
        assert log_entry.latency_ms == 100.0
        assert log_entry.user_id == "test-user"
        assert log_entry.endpoint == "/test"
        assert log_entry.llm_model == "gpt-4"
        assert log_entry.extra == {}

    def test_log_entry_with_extra_fields(self):
        """Test creating a LogEntry with extra fields."""
        log_entry = LogEntry(
            timestamp=datetime.now(),
            level="ERROR",
            message="Error occurred",
            request_id="test-request-id",
            latency_ms=50.0,
            extra={"error_code": "E001", "component": "api"}
        )

        assert log_entry.extra == {"error_code": "E001", "component": "api"}

    def test_log_entry_immutable(self):
        """Test that LogEntry is immutable."""
        log_entry = LogEntry(
            timestamp=datetime.now(),
            level="INFO",
            message="Test message",
            request_id="test-request-id",
            latency_ms=100.0
        )

        with pytest.raises(FrozenInstanceError):
            log_entry.message = "New message"

    def test_log_entry_validation_level(self):
        """Test validation of log level."""
        valid_levels = ["INFO", "ERROR", "DEBUG", "WARNING", "CRITICAL"]
        for level in valid_levels:
            log_entry = LogEntry(
                timestamp=datetime.now(),
                level=level,
                message="Test message",
                request_id="test-request-id",
                latency_ms=100.0
            )
            assert log_entry.level == level

        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                level="INVALID",  # Invalid level should fail
                message="Test message",
                request_id="test-request-id",
                latency_ms=100.0
            )

    def test_log_entry_validation_message(self):
        """Test validation of message."""
        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="",  # Empty message should fail
                request_id="test-request-id",
                latency_ms=100.0
            )

        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message=123,  # Non-string message should fail
                request_id="test-request-id",
                latency_ms=100.0
            )

    def test_log_entry_validation_request_id(self):
        """Test validation of request_id."""
        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="Test message",
                request_id="",  # Empty request_id should fail
                latency_ms=100.0
            )

        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="Test message",
                request_id=123,  # Non-string request_id should fail
                latency_ms=100.0
            )

    def test_log_entry_validation_latency_ms(self):
        """Test validation of latency_ms."""
        # Valid non-negative latency
        log_entry = LogEntry(
            timestamp=datetime.now(),
            level="INFO",
            message="Test message",
            request_id="test-request-id",
            latency_ms=100.0  # Valid positive number
        )
        assert log_entry.latency_ms == 100.0

        # Valid zero latency
        log_entry_zero = LogEntry(
            timestamp=datetime.now(),
            level="INFO",
            message="Test message",
            request_id="test-request-id",
            latency_ms=0  # Valid zero
        )
        assert log_entry_zero.latency_ms == 0

        # Invalid negative latency
        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="Test message",
                request_id="test-request-id",
                latency_ms=-10.0  # Negative should fail
            )

    def test_log_entry_validation_extra(self):
        """Test validation of extra field."""
        with pytest.raises(ValueError):
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="Test message",
                request_id="test-request-id",
                latency_ms=100.0,
                extra=None  # None should fail
            )


class TestMetric:
    """Test metric value object."""

    def test_metric_creation(self):
        """Test creating a valid Metric."""
        now = datetime.now()
        metric = Metric(
            name="test.metric",
            value=42.5,
            labels={"env": "test", "service": "api"},
            timestamp=now
        )

        assert metric.name == "test.metric"
        assert metric.value == 42.5
        assert metric.labels == {"env": "test", "service": "api"}
        assert metric.timestamp == now

    def test_metric_default_timestamp(self):
        """Test Metric with default timestamp."""
        metric = Metric(
            name="test.metric",
            value=42.5
        )

        assert metric.name == "test.metric"
        assert metric.value == 42.5
        assert isinstance(metric.timestamp, datetime)

    def test_metric_immutable(self):
        """Test that Metric is immutable."""
        metric = Metric(
            name="test.metric",
            value=42.5
        )

        with pytest.raises(FrozenInstanceError):
            metric.value = 100.0

    def test_metric_validation_name(self):
        """Test validation of metric name."""
        with pytest.raises(ValueError):
            Metric(
                name="",  # Empty name should fail
                value=42.5
            )

        with pytest.raises(ValueError):
            Metric(
                name=123,  # Non-string name should fail
                value=42.5
            )

    def test_metric_validation_value(self):
        """Test validation of metric value."""
        # Valid int value
        metric_int = Metric(
            name="test.metric",
            value=42  # Integer should be valid
        )
        assert metric_int.value == 42

        # Valid float value
        metric_float = Metric(
            name="test.metric",
            value=42.5  # Float should be valid
        )
        assert metric_float.value == 42.5

        # Invalid string value
        with pytest.raises(ValueError):
            Metric(
                name="test.metric",
                value="42.5"  # String should fail
            )

    def test_metric_validation_labels(self):
        """Test validation of metric labels."""
        with pytest.raises(ValueError):
            Metric(
                name="test.metric",
                value=42.5,
                labels="invalid"  # String instead of dict should fail
            )


class TestHealthStatus:
    """Test health status value object."""

    def test_health_status_creation(self):
        """Test creating a valid HealthStatus."""
        now = datetime.now()
        health = HealthStatus(
            status="healthy",
            timestamp=now,
            uptime_seconds=3600.0,
            version="1.0.0",
            checks={"db": {"status": "ok"}, "cache": {"status": "ok"}}
        )

        assert health.status == "healthy"
        assert health.timestamp == now
        assert health.uptime_seconds == 3600.0
        assert health.version == "1.0.0"
        assert health.checks == {"db": {"status": "ok"}, "cache": {"status": "ok"}}

    def test_health_status_defaults(self):
        """Test HealthStatus with default values."""
        health = HealthStatus(status="healthy")

        assert health.status == "healthy"
        assert isinstance(health.timestamp, datetime)
        assert health.uptime_seconds == 0.0
        assert health.version == "1.0.0"
        assert health.checks == {}

    def test_health_status_immutable(self):
        """Test that HealthStatus is immutable."""
        health = HealthStatus(status="healthy")

        with pytest.raises(FrozenInstanceError):
            health.status = "unhealthy"

    def test_health_status_validation_status(self):
        """Test validation of health status."""
        valid_statuses = ["healthy", "degraded", "unhealthy"]
        for status in valid_statuses:
            health = HealthStatus(status=status)
            assert health.status == status

        with pytest.raises(ValueError):
            HealthStatus(status="invalid")  # Invalid status should fail

    def test_health_status_validation_uptime_seconds(self):
        """Test validation of uptime_seconds."""
        # Valid non-negative uptime
        health = HealthStatus(
            status="healthy",
            uptime_seconds=3600.0  # Valid positive number
        )
        assert health.uptime_seconds == 3600.0

        # Valid zero uptime
        health_zero = HealthStatus(
            status="healthy",
            uptime_seconds=0.0  # Valid zero
        )
        assert health_zero.uptime_seconds == 0.0

        # Invalid negative uptime
        with pytest.raises(ValueError):
            HealthStatus(
                status="healthy",
                uptime_seconds=-1.0  # Negative should fail
            )

    def test_health_status_validation_version(self):
        """Test validation of version."""
        with pytest.raises(ValueError):
            HealthStatus(
                status="healthy",
                version=""  # Empty version should fail
            )

        with pytest.raises(ValueError):
            HealthStatus(
                status="healthy",
                version=123  # Non-string version should fail
            )


class TestRequestMetrics:
    """Test request metrics value object."""

    def test_request_metrics_creation(self):
        """Test creating a valid RequestMetrics."""
        now = datetime.now()
        metrics = RequestMetrics(
            request_id="test-request-id",
            endpoint="/api/test",
            method="GET",
            status_code=200,
            latency_ms=150.5,
            user_id="test-user",
            timestamp=now
        )

        assert metrics.request_id == "test-request-id"
        assert metrics.endpoint == "/api/test"
        assert metrics.method == "GET"
        assert metrics.status_code == 200
        assert metrics.latency_ms == 150.5
        assert metrics.user_id == "test-user"
        assert metrics.timestamp == now

    def test_request_metrics_defaults(self):
        """Test RequestMetrics with default values."""
        metrics = RequestMetrics(
            request_id="test-request-id",
            endpoint="/api/test",
            method="POST",
            status_code=201,
            latency_ms=200.0
        )

        assert metrics.request_id == "test-request-id"
        assert metrics.endpoint == "/api/test"
        assert metrics.method == "POST"
        assert metrics.status_code == 201
        assert metrics.latency_ms == 200.0
        assert metrics.user_id is None  # Should default to None
        assert isinstance(metrics.timestamp, datetime)  # Should have default timestamp

    def test_request_metrics_immutable(self):
        """Test that RequestMetrics is immutable."""
        metrics = RequestMetrics(
            request_id="test-request-id",
            endpoint="/api/test",
            method="GET",
            status_code=200,
            latency_ms=150.5
        )

        with pytest.raises(FrozenInstanceError):
            metrics.status_code = 500

    def test_request_metrics_validation_request_id(self):
        """Test validation of request_id."""
        with pytest.raises(ValueError):
            RequestMetrics(
                request_id="",  # Empty request_id should fail
                endpoint="/api/test",
                method="GET",
                status_code=200,
                latency_ms=150.5
            )

    def test_request_metrics_validation_endpoint(self):
        """Test validation of endpoint."""
        with pytest.raises(ValueError):
            RequestMetrics(
                request_id="test-request-id",
                endpoint="",  # Empty endpoint should fail
                method="GET",
                status_code=200,
                latency_ms=150.5
            )

        with pytest.raises(ValueError):
            RequestMetrics(
                request_id="test-request-id",
                endpoint=123,  # Non-string endpoint should fail
                method="GET",
                status_code=200,
                latency_ms=150.5
            )

    def test_request_metrics_validation_method(self):
        """Test validation of method."""
        with pytest.raises(ValueError):
            RequestMetrics(
                request_id="test-request-id",
                endpoint="/api/test",
                method="",  # Empty method should fail
                status_code=200,
                latency_ms=150.5
            )

    def test_request_metrics_validation_status_code(self):
        """Test validation of status_code."""
        valid_codes = [200, 201, 404, 500]  # Some valid HTTP codes
        for code in valid_codes:
            metrics = RequestMetrics(
                request_id="test-request-id",
                endpoint="/api/test",
                method="GET",
                status_code=code,
                latency_ms=150.5
            )
            assert metrics.status_code == code

        invalid_codes = [99, 600, 1000]  # Invalid HTTP codes
        for code in invalid_codes:
            with pytest.raises(ValueError):
                RequestMetrics(
                    request_id="test-request-id",
                    endpoint="/api/test",
                    method="GET",
                    status_code=code,
                    latency_ms=150.5
                )

    def test_request_metrics_validation_latency_ms(self):
        """Test validation of latency_ms."""
        # Valid non-negative latency
        metrics = RequestMetrics(
            request_id="test-request-id",
            endpoint="/api/test",
            method="GET",
            status_code=200,
            latency_ms=150.5  # Valid positive number
        )
        assert metrics.latency_ms == 150.5

        # Valid zero latency
        metrics_zero = RequestMetrics(
            request_id="test-request-id",
            endpoint="/api/test",
            method="GET",
            status_code=200,
            latency_ms=0.0  # Valid zero
        )
        assert metrics_zero.latency_ms == 0.0

        # Invalid negative latency
        with pytest.raises(ValueError):
            RequestMetrics(
                request_id="test-request-id",
                endpoint="/api/test",
                method="GET",
                status_code=200,
                latency_ms=-10.0  # Negative should fail
            )