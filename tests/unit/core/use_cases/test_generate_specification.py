from datetime import datetime, timezone

import pytest

from src.core.models.specification_workflow import BusinessRequirements
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase


def test_generate_specification_with_valid_requirements():
    use_case = GenerateSpecificationUseCase()
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = use_case.execute(BusinessRequirements("User precisa de dashboard para métricas"), created_at)

    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert result.content.startswith('{')
    assert "dashboard" in result.content.lower()
    assert created_at in result.content


def test_generate_specification_with_empty_requirements():
    use_case = GenerateSpecificationUseCase()
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    with pytest.raises(ValueError):
        use_case.execute(BusinessRequirements(""), created_at)


def test_generate_specification_with_api_requirements():
    """Test specification generation with API requirements"""
    use_case = GenerateSpecificationUseCase()
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = use_case.execute(BusinessRequirements("Sistema precisa de API REST para gerenciar usuários"), created_at)

    assert "api" in result.content.lower()
    assert "REST API" in result.content
    assert "usuários" in result.content or "users" in result.content
    assert created_at in result.content


def test_generate_specification_filename_generation():
    """Test generation of meaningful filename"""
    use_case = GenerateSpecificationUseCase()
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = use_case.execute(BusinessRequirements("Sistema de relatórios financeiros"), created_at)

    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert "relatórios" in result.filename or "financeiros" in result.filename


def test_generate_specification_acceptance_criteria():
    """Test generation of acceptance criteria based on requirements"""
    use_case = GenerateSpecificationUseCase()
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = use_case.execute(BusinessRequirements("Sistema de métricas em tempo real"), created_at)

    assert "métricas" in result.content.lower()
    assert "real" in result.content.lower()
    assert "Dashboard exibe métricas em tempo real" in result.content
    assert created_at in result.content


def test_generate_specification_with_empty_timestamp():
    """Test generation with empty timestamp"""
    use_case = GenerateSpecificationUseCase()

    result = use_case.execute(BusinessRequirements("Simple requirements"), "")

    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.content.startswith('{')
    assert '"created_at": ""' in result.content