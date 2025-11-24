from unittest.mock import AsyncMock

import pytest

from src.core.models.specification_result import SaveDirectoryPath
from src.core.models.specification_workflow import BusinessRequirements
from src.shell.adapters.prompt_loaders.generic_yaml_prompt import GenericYAMLPrompt


@pytest.mark.asyncio
async def test_generate_returns_proper_instructions():
    """Test that the prompt generates appropriate save instructions"""
    prompt = GenericYAMLPrompt("specification_save_instruction")
    ctx_mock = AsyncMock()

    result = await prompt.generate(
        ctx_mock,
        save_directory=str(SaveDirectoryPath("ctxfy/specifications/")),
        business_requirements=str(BusinessRequirements("Requisitos de negócio para teste"))
    )

    assert "ctxfy/specifications/" in result
    assert "SAVE INSTRUCTIONS" in result
    assert "Create the" in result
    assert "Save the complete specification file" in result
    assert "Requisitos de negócio para teste" in result


@pytest.mark.asyncio
async def test_generate_with_custom_directory():
    """Test that the prompt accepts custom directory"""
    prompt = GenericYAMLPrompt("specification_save_instruction")
    ctx_mock = AsyncMock()

    result = await prompt.generate(
        ctx_mock,
        save_directory=str(SaveDirectoryPath("custom/path/to/specs")),
        business_requirements=str(BusinessRequirements("Requisitos de negócio"))
    )

    assert "custom/path/to/specs" in result
    assert "custom/path/to/specs" in result
    assert "SAVE INSTRUCTIONS" in result
    assert "Requisitos de negócio" in result


@pytest.mark.asyncio
async def test_generate_uses_default_directory():
    """Test that the prompt uses default directory when not specified"""
    prompt = GenericYAMLPrompt("specification_save_instruction")
    ctx_mock = AsyncMock()

    result = await prompt.generate(
        ctx_mock,
        save_directory="ctxfy/specifications/",
        business_requirements="Requisitos de negócio"
    )

    assert "ctxfy/specifications/" in result
    assert "SAVE INSTRUCTIONS" in result
    assert "Requisitos de negócio" in result