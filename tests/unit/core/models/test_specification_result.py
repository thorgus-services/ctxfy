from dataclasses import FrozenInstanceError

import pytest

from src.core.models.specification_result import (
    SpecificationContent,
    SpecificationFilename,
    SpecificationId,
    SpecificationResult,
)


def test_specification_result_immutability():
    """Test that the value object is immutable"""
    result = SpecificationResult(
        id=SpecificationId("test-123"),
        content=SpecificationContent("conteúdo original"),
        filename=SpecificationFilename("test.json")
    )
    with pytest.raises(FrozenInstanceError):
        result.content = "novo conteúdo"
