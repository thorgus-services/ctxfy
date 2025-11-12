"""Unit tests for MCP models following TDD principles."""

from datetime import datetime

import pytest

from src.core.models.mcp_models import HealthStatus, PromptRequest, PromptResponse
from src.core.use_cases.mcp_use_cases import (
    calculate_health_status,
    create_prompt_response,
    process_prompt_request,
)


class TestPromptRequestModel:
    """Test immutable value objects."""

    def test_prompt_request_creation(self):
        """Test creating a valid PromptRequest."""
        request = PromptRequest(
            name="test_prompt",
            parameters={"param1": "value1"}
        )

        assert request.name == "test_prompt"
        assert request.parameters == {"param1": "value1"}
        assert isinstance(request.prompt_id, str)
        assert len(request.prompt_id) > 0

    def test_prompt_request_validation(self):
        """Test validation in PromptRequest."""
        with pytest.raises(ValueError):
            PromptRequest(name="", parameters={})

        with pytest.raises(ValueError):
            PromptRequest(name="test", parameters="invalid")


class TestPromptResponseModel:
    """Test PromptResponse immutable value object."""

    def test_prompt_response_creation(self):
        """Test creating a valid PromptResponse."""
        response = PromptResponse(
            request_id="test-id",
            result="test content",
            latency_ms=100.0,
            llm_model="default"
        )

        assert response.request_id == "test-id"
        assert response.result == "test content"
        assert response.latency_ms == 100.0
        assert response.llm_model == "default"

    def test_prompt_response_validation(self):
        """Test validation in PromptResponse."""
        with pytest.raises(ValueError):
            PromptResponse(
                request_id="",
                result="test",
                latency_ms=100.0,
                llm_model="default"
            )

        with pytest.raises(ValueError):
            PromptResponse(
                request_id="test-id",
                result=123,  # Should be string
                latency_ms=100.0,
                llm_model="default"
            )

        with pytest.raises(ValueError):
            PromptResponse(
                request_id="test-id",
                result="test",
                latency_ms=-10.0,  # Should be non-negative
                llm_model="default"
            )


class TestHealthStatusModel:
    """Test HealthStatus immutable value object."""

    def test_health_status_creation(self):
        """Test creating a valid HealthStatus."""
        status = HealthStatus(status="healthy")

        assert status.status == "healthy"
        assert isinstance(status.timestamp, datetime)
        assert status.uptime_seconds == 0.0
        assert status.version == "1.0.0"

    def test_health_status_validation(self):
        """Test validation in HealthStatus."""
        with pytest.raises(ValueError):
            HealthStatus(status="invalid")

        with pytest.raises(ValueError):
            HealthStatus(status="healthy", uptime_seconds=-10.0)


class TestCoreUseCases:
    """Test pure functions in core use cases."""

    def test_process_prompt_request(self):
        """Test processing a prompt request."""
        start_time = datetime.now()
        request = process_prompt_request(
            name="test-prompt",
            parameters={"param": "value"},
            start_time=start_time,
            llm_model="default"
        )

        assert request.name == "test-prompt"
        assert request.parameters == {"param": "value"}
        assert isinstance(request.prompt_id, str)

    def test_create_prompt_response(self):
        """Test creating a prompt response with calculated latency."""
        start_time = datetime.now()
        # Simulate some time passing
        import time
        time.sleep(0.001)  # 1ms delay

        response = create_prompt_response(
            request_id="test-id",
            result="test response",
            start_time=start_time,
            llm_model="default"
        )

        assert response.request_id == "test-id"
        assert response.result == "test response"
        assert response.llm_model == "default"
        assert response.latency_ms > 0  # Should be greater than 0 due to delay

    def test_calculate_health_status(self):
        """Test calculating health status."""
        start_time = datetime.now()
        status = calculate_health_status(start_time)

        assert status.status == "healthy"  # Default status
        assert isinstance(status.timestamp, datetime)
        assert status.uptime_seconds >= 0
        assert status.version == "1.0.0"