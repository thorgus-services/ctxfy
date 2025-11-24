from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.models.specification_result import (
    SpecificationContent,
    SpecificationFilename,
    SpecificationId,
    SpecificationResult,
)
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase
from src.shell.adapters.tools.specification_generation_tool import (
    SpecificationGenerationTool,
)


@pytest.mark.asyncio
async def test_execute_with_valid_requirements():
    """Test execution of tool with valid requirements"""
    mock_use_case = MagicMock(spec=GenerateSpecificationUseCase)
    mock_result = SpecificationResult(
        id=SpecificationId("test-id-123"),
        content=SpecificationContent('{"test": "content"}'),
        filename=SpecificationFilename("test_spec.json")
    )
    mock_use_case.execute.return_value = mock_result

    ctx_mock = AsyncMock()
    tool = SpecificationGenerationTool(use_case=mock_use_case)

    result = await tool.execute(ctx_mock, "Requisitos de negócio válidos")

    assert result["specification_id"] == "test-id-123"
    assert result["content"] == '{"test": "content"}'
    assert result["suggested_filename"] == "test_spec.json"
    ctx_mock.info.assert_called()


@pytest.mark.asyncio
async def test_execute_with_invalid_requirements():
    """Test execution of tool with invalid requirements"""
    mock_use_case = MagicMock(spec=GenerateSpecificationUseCase)
    mock_use_case.execute.side_effect = ValueError("Requisitos inválidos")

    ctx_mock = AsyncMock()
    tool = SpecificationGenerationTool(use_case=mock_use_case)

    with pytest.raises(ValueError):
        await tool.execute(ctx_mock, "")

    ctx_mock.error.assert_called()


@pytest.mark.asyncio
async def test_execute_logs_properly():
    """Test that execution performs proper logging"""
    mock_use_case = MagicMock(spec=GenerateSpecificationUseCase)
    mock_result = SpecificationResult(
        id=SpecificationId("test-id-123"),
        content=SpecificationContent('{"test": "content"}'),
        filename=SpecificationFilename("test_spec.json")
    )
    mock_use_case.execute.return_value = mock_result

    ctx_mock = AsyncMock()
    tool = SpecificationGenerationTool(use_case=mock_use_case)

    await tool.execute(ctx_mock, "Test requirements for logging")

    ctx_mock.info.assert_called()
    assert ctx_mock.info.call_count >= 2