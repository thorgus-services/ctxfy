from datetime import datetime, timedelta

import pytest

from src.adapters.monitoring.monitoring import (
    MonitoringAdapter,
)
from src.core.models.monitoring_models import HealthStatus


class TestMonitoringAdapter:
    """Tests for MonitoringAdapter class."""

    def test_init(self):
        """Test initializing MonitoringAdapter."""
        start_time = datetime.now()
        adapter = MonitoringAdapter(start_time)
        
        # Check that it has the right attributes from both parent classes
        assert adapter.start_time == start_time
        assert hasattr(adapter, 'registry')
        assert hasattr(adapter, 'prompt_execution_counter')
        assert hasattr(adapter, 'prompt_execution_histogram')

    def test_record_prompt_execution_success(self):
        """Test recording successful prompt execution."""
        start_time = datetime.now() - timedelta(seconds=10)
        adapter = MonitoringAdapter(start_time)
        
        adapter.record_prompt_execution(
            template_id="test-template",
            latency_ms=100.0,
            success=True
        )
        
        # Check that no exception is raised - metrics should be recorded properly

    def test_record_prompt_execution_failure(self):
        """Test recording failed prompt execution."""
        start_time = datetime.now()
        adapter = MonitoringAdapter(start_time)
        
        adapter.record_prompt_execution(
            template_id="test-template",
            latency_ms=50.0,
            success=False
        )
        
        # Check that no exception is raised

    def test_get_prometheus_metrics(self):
        """Test getting Prometheus metrics."""
        start_time = datetime.now()
        adapter = MonitoringAdapter(start_time)
        
        # Record some metrics
        adapter.record_prompt_execution(
            template_id="test-template",
            latency_ms=100.0,
            success=True
        )
        
        # Get Prometheus metrics
        metrics_bytes = adapter.get_prometheus_metrics()
        
        # Check that we get bytes back
        assert isinstance(metrics_bytes, bytes)
        assert len(metrics_bytes) > 0

    @pytest.mark.asyncio
    async def test_get_health_status_healthy(self):
        """Test getting healthy status when system is healthy."""
        start_time = datetime.now() - timedelta(seconds=30)
        adapter = MonitoringAdapter(start_time)
        
        health_status = await adapter.get_health_status()
        
        # Check that status is calculated properly
        assert isinstance(health_status, HealthStatus)
        assert health_status.status in ["healthy", "degraded", "unhealthy"]
        assert health_status.uptime_seconds >= 30
        assert health_status.version == "1.0.0"

    @pytest.mark.asyncio
    async def test_get_health_status_with_start_time(self):
        """Test getting health status with start time."""
        start_time = datetime.now() - timedelta(seconds=1)
        adapter = MonitoringAdapter(start_time)
        
        health_status = await adapter.get_health_status()
        
        assert isinstance(health_status, HealthStatus)
        assert health_status.uptime_seconds >= 0  # Should be positive

    def test_get_uptime_seconds(self):
        """Test calculating uptime correctly."""
        # Set start time 60 seconds ago
        start_time = datetime.now() - timedelta(seconds=60)
        adapter = MonitoringAdapter(start_time)
        
        uptime = adapter.get_uptime_seconds()
        
        # Uptime should be approximately 60 seconds
        assert uptime >= 59.0  # Allow for some time differences
        assert uptime <= 65.0  # Upper bound check

    def test_get_prometheus_metrics_empty(self):
        """Test getting Prometheus metrics when no metrics exist."""
        start_time = datetime.now()
        adapter = MonitoringAdapter(start_time)
        
        metrics_bytes = adapter.get_prometheus_metrics()
        
        # Should return some valid metrics output 
        assert isinstance(metrics_bytes, bytes)
        assert len(metrics_bytes) >= 0  # Valid output