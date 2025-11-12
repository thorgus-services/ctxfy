"""Integration tests for server components following TDD principles.

Tests the core functionality with real/fake adapters, no mocks of core logic, following our testing strategy:
- Unit tests for business logic (pure functions only)
- Integration tests for complete flows (real/fake adapters, no mocks of core logic)
"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.infrastructure.llm.llm_adapter import LLMAdapter
from src.infrastructure.logging.structured_logger import StructuredLogger
from src.shell.orchestrators.orchestrator import MCPOrchestrator


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