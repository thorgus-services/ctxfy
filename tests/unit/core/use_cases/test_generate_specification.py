import pytest

from src.core.models.specification_workflow import BusinessRequirements
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase


def test_generate_specification_with_valid_requirements():
    use_case = GenerateSpecificationUseCase()
    result = use_case.execute(BusinessRequirements("User precisa de dashboard para métricas"))

    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert result.content.startswith('{')
    assert "dashboard" in result.content.lower()


def test_generate_specification_with_empty_requirements():
    use_case = GenerateSpecificationUseCase()
    with pytest.raises(ValueError):
        use_case.execute(BusinessRequirements(""))


def test_generate_specification_with_api_requirements():
    """Test specification generation with API requirements"""
    use_case = GenerateSpecificationUseCase()
    result = use_case.execute(BusinessRequirements("Sistema precisa de API REST para gerenciar usuários"))

    assert "api" in result.content.lower()
    assert "REST API" in result.content
    assert "usuários" in result.content or "users" in result.content


def test_generate_specification_filename_generation():
    """Test generation of meaningful filename"""
    use_case = GenerateSpecificationUseCase()
    result = use_case.execute(BusinessRequirements("Sistema de relatórios financeiros"))

    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert "relatórios" in result.filename or "financeiros" in result.filename


def test_generate_specification_acceptance_criteria():
    """Test generation of acceptance criteria based on requirements"""
    use_case = GenerateSpecificationUseCase()
    result = use_case.execute(BusinessRequirements("Sistema de métricas em tempo real"))

    assert "métricas" in result.content.lower()
    assert "real" in result.content.lower()
    assert "Dashboard exibe métricas em tempo real" in result.content