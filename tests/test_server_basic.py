"""Basic tests for server functionality following TDD principles.

Tests the core functionality without mocking core logic, following our testing strategy:
- Unit tests for business logic (pure functions only)
- Integration tests for complete flows (real/fake adapters, no mocks of core logic)
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from src.core.models.mcp_models import HealthStatus, PromptRequest, PromptResponse
from src.core.use_cases.mcp_use_cases import (
    calculate_health_status,
    create_prompt_response,
    process_prompt_request,
)
from src.infrastructure.llm.llm_adapter import LLMAdapter
from src.infrastructure.logging.structured_logger import StructuredLogger
from src.shell.orchestrators.orchestrator import MCPOrchestrator


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
            prompt_id="test-id",
            content="test content",
            latency_ms=100.0,
            llm_model="default"
        )
        
        assert response.prompt_id == "test-id"
        assert response.content == "test content"
        assert response.latency_ms == 100.0
        assert response.llm_model == "default"
    
    def test_prompt_response_validation(self):
        """Test validation in PromptResponse."""
        with pytest.raises(ValueError):
            PromptResponse(
                prompt_id="",
                content="test",
                latency_ms=100.0,
                llm_model="default"
            )
        
        with pytest.raises(ValueError):
            PromptResponse(
                prompt_id="test-id",
                content=123,  # Should be string
                latency_ms=100.0,
                llm_model="default"
            )
        
        with pytest.raises(ValueError):
            PromptResponse(
                prompt_id="test-id",
                content="test",
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
            prompt_id="test-id",
            content="test response",
            start_time=start_time,
            llm_model="default"
        )
        
        assert response.prompt_id == "test-id"
        assert response.content == "test response"
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


class TestStructuredLogger:
    """Test structured logging functionality."""
    
    def test_logging_initialization(self):
        """Test logger initialization."""
        logger = StructuredLogger(level="INFO")
        assert logger.level == "INFO"
    
    def test_log_prompt_request(self, capsys):
        """Test logging a prompt request."""
        logger = StructuredLogger(level="INFO")
        
        # Log a prompt request
        logger.log_prompt_request(
            prompt_id="test-id",
            name="test-prompt",
            latency_ms=100.0,
            llm_model="default"
        )
        
        # Capture output and verify it's JSON
        captured = capsys.readouterr()
        output = captured.out
        assert "prompt_id" in output
        assert "test-id" in output
        assert "latency_ms" in output
        assert "100.0" in output


class TestLLMAdapter:
    """Test LLM adapter functionality."""
    
    @pytest.mark.asyncio
    async def test_sample_text(self):
        """Test basic text sampling."""
        adapter = LLMAdapter(default_model="test-model")
        result = await adapter.sample_text("test prompt", "test-model")
        
        assert isinstance(result, str)
        assert "test prompt" in result
    
    @pytest.mark.asyncio
    async def test_sample_text_with_context(self):
        """Test sampling with mocked context."""
        # Create a mock context that has a sample method
        mock_ctx = AsyncMock()
        mock_ctx.sample.return_value = "mocked response"
        
        adapter = LLMAdapter(default_model="test-model")
        result = await adapter.sample_text_with_context(mock_ctx, "test prompt", "test-model")
        
        # Verify that ctx.sample was called with correct parameters
        mock_ctx.sample.assert_called_once_with(messages="test prompt", model_preferences="test-model")
        assert result == "mocked response"


class TestOrchestrator:
    """Test orchestrator functionality."""
    
    @pytest.mark.asyncio
    async def test_handle_sample_prompt(self):
        """Test handling a sample prompt."""
        # Create mocks
        mock_ctx = AsyncMock()
        mock_ctx.sample.return_value = "test response"
        
        mock_logging_adapter = Mock()
        mock_logging_adapter.log_prompt_request = Mock()
        mock_logging_adapter.log_error = Mock()
        
        # Create orchestrator with mocked dependencies
        orchestrator = MCPOrchestrator(
            llm_adapter=LLMAdapter(), 
            logging_adapter=mock_logging_adapter
        )
        
        # Call the method
        result = await orchestrator.handle_sample_prompt(mock_ctx, "test", "topic")
        
        # Verify the result
        assert result == "test response"
        # Verify ctx.sample was called
        mock_ctx.sample.assert_called_once()
        # Verify logging was called
        mock_logging_adapter.log_prompt_request.assert_called_once()


# Integration test for the complete flow
@pytest.mark.asyncio
async def test_complete_prompt_flow():
    """Integration test for the complete prompt handling flow."""
    # Create real adapters (not mocks)
    logger = StructuredLogger(level="INFO")
    llm_adapter = LLMAdapter(default_model="default")
    
    # Create orchestrator with real adapters
    orchestrator = MCPOrchestrator(
        llm_adapter=llm_adapter,
        logging_adapter=logger
    )
    
    # Create a mock context to simulate FastMCP context
    mock_ctx = AsyncMock()
    mock_ctx.sample.return_value = "integration test response"
    
    # Execute the flow
    result = await orchestrator.handle_sample_prompt(mock_ctx, "integration", "test")
    
    # Verify the result
    assert result == "integration test response"
    # Verify ctx.sample was called
    mock_ctx.sample.assert_called_once()