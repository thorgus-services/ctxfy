import asyncio
from unittest.mock import AsyncMock

import pytest

from src.adapters.llm_sampling.llm_sampler import LLMSampler


class TestLLMSampler:
    """Tests for LLMSampler class."""

    def test_init_without_ctx(self):
        """Test initializing LLMSampler without ctx."""
        sampler = LLMSampler()
        assert sampler.ctx is None

    def test_init_with_ctx(self):
        """Test initializing LLMSampler with ctx."""
        mock_ctx = AsyncMock()
        sampler = LLMSampler(ctx=mock_ctx)
        assert sampler.ctx is mock_ctx

    @pytest.mark.asyncio
    async def test_sample_prompt_success(self):
        """Test sample_prompt with successful response."""
        mock_ctx = AsyncMock()
        mock_ctx.sample.return_value = "Generated test response"
        
        sampler = LLMSampler(ctx=mock_ctx)
        result = await sampler.sample_prompt(
            prompt="Test prompt",
            model="gpt-4o",
            temperature=0.7,
            max_tokens=100
        )
        
        assert result == "Generated test response"
        mock_ctx.sample.assert_called_once_with(
            prompt="Test prompt",
            model="gpt-4o",
            temperature=0.7,
            max_tokens=100
        )

    @pytest.mark.asyncio
    async def test_sample_prompt_with_default_parameters(self):
        """Test sample_prompt with default parameters."""
        mock_ctx = AsyncMock()
        mock_ctx.sample.return_value = "Default response"
        
        sampler = LLMSampler(ctx=mock_ctx)
        result = await sampler.sample_prompt(prompt="Test prompt")
        
        assert result == "Default response"
        mock_ctx.sample.assert_called_once_with(
            prompt="Test prompt",
            model="gpt-4o",
            temperature=0.7,
            max_tokens=1000  # default max_tokens
        )

    @pytest.mark.asyncio
    async def test_sample_prompt_without_ctx_raises_error(self):
        """Test sample_prompt without ctx raises RuntimeError."""
        sampler = LLMSampler(ctx=None)
        
        with pytest.raises(RuntimeError, match="LLM sampling requires MCP context"):
            await sampler.sample_prompt(prompt="Test prompt")

    @pytest.mark.asyncio
    async def test_sample_prompt_timeout_error(self):
        """Test sample_prompt with timeout."""
        mock_ctx = AsyncMock()
        mock_ctx.sample.side_effect = asyncio.TimeoutError()
        
        sampler = LLMSampler(ctx=mock_ctx)
        
        with pytest.raises(Exception, match="LLM sampling timed out"):
            await sampler.sample_prompt(
                prompt="Test prompt",
                timeout=0.1  # Very short timeout
            )

    @pytest.mark.asyncio
    async def test_sample_prompt_general_error(self):
        """Test sample_prompt with general error."""
        mock_ctx = AsyncMock()
        mock_ctx.sample.side_effect = Exception("API error")
        
        sampler = LLMSampler(ctx=mock_ctx)
        
        with pytest.raises(Exception, match="LLM sampling failed: API error"):
            await sampler.sample_prompt(prompt="Test prompt")