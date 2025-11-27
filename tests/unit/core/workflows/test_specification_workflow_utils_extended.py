
from src.core.models.specification_workflow import BusinessRequirements
from src.core.workflows.specification_workflow import (
    _clean_business_requirements,
    _extract_components_from_requirements,
    _extract_important_words,
    _generate_acceptance_criteria,
    _generate_description,
    _generate_specification_filename,
    _generate_specification_id,
)


def test_clean_business_requirements_various_scenarios():
    result = _clean_business_requirements(BusinessRequirements("User needs dashboard!@#$%^&*()"))
    assert result == "User needs dashboard()"

    result = _clean_business_requirements(BusinessRequirements("User: needs? dashboard! for; metrics."))
    assert result == "User: needs dashboard for; metrics."

    result = _clean_business_requirements(BusinessRequirements("User needs dashboard© for metrics™"))
    assert "©" not in result and "™" not in result


def test_extract_important_words_various_scenarios():
    """Test _extract_important_words with various scenarios"""
    result = _extract_important_words("word test case", max_words=5, min_length=4)
    assert result == ["word", "test", "case"]

    result = _extract_important_words("a word testing case example", max_words=3, min_length=4)
    assert "a" not in result
    assert "word" in result
    assert "testing" in result
    assert "case" in result
    assert len(result) == 3

    result = _extract_important_words("a an the of", max_words=5, min_length=4)
    assert result == []


def test_generate_specification_id_consistency():
    """Test _generate_specification_id consistency across multiple calls"""
    content = "User needs dashboard for metrics"

    ids = [_generate_specification_id(content) for _ in range(5)]

    assert all(id == ids[0] for id in ids)

    content2 = "System needs API for authentication"
    id2 = _generate_specification_id(content2)
    assert id2 != ids[0]


def test_generate_specification_filename_edge_cases():
    """Test _generate_specification_filename with edge cases"""
    long_content = "very_long_word_for_testing_filename_truncation_purposes_exceeding_limit"
    result = _generate_specification_filename(long_content)
    assert result.startswith("spec_")
    assert result.endswith(".json")

    short_content = "a b c"
    result = _generate_specification_filename(short_content)
    assert result.startswith("spec_")
    assert result.endswith(".json")

    special_content = "user-dashboard for_metrics&analytics"
    result = _generate_specification_filename(special_content)


def test_extract_components_from_requirements_edge_cases():
    """Test _extract_components_from_requirements with edge cases"""
    content = "User needs dashboard and API for metrics"
    result = _extract_components_from_requirements(content)
    assert "frontend/dashboard" in result
    assert "backend/metrics-service" in result
    assert "api/gateway" in result
    assert "ctxfy/specifications/" in result

    content = "User interface for analytics API"
    result = _extract_components_from_requirements(content)
    assert "api/gateway" in result

    content = "System needs monitoring dashboard"
    custom_dir = "custom/monitoring/path/"
    result = _extract_components_from_requirements(content, custom_dir)
    assert custom_dir in result
    assert "frontend/dashboard" in result
    assert "backend/metrics-service" in result


def test_generate_description_edge_cases():
    """Test _generate_description with edge cases"""
    fifteen_words = " ".join(["word"] * 15)
    result = _generate_description(fifteen_words)
    assert result == fifteen_words

    sixteen_words = " ".join(["word"] * 16)
    result = _generate_description(sixteen_words)
    assert result.endswith("...")

    result = _generate_description("")
    assert result == ""

    result = _generate_description("single")
    assert result == "single"


def test_generate_acceptance_criteria_variations():
    """Test _generate_acceptance_criteria with different variations"""
    content = "Sistema de métricas em tempo real"
    result = _generate_acceptance_criteria(content)
    assert "Dashboard exibe métricas em tempo real" in result

    content = "System with real-time metrics"
    result = _generate_acceptance_criteria(content)
    assert "Dashboard exibe métricas em tempo real" in result

    content = "System for file storage and backup"
    result = _generate_acceptance_criteria(content)
    assert "Dashboard exibe métricas em tempo real" not in result

    content = "Any requirement"
    result = _generate_acceptance_criteria(content)
    assert "Especificação gerada no formato JSON válido" in result
    assert "Arquivo salvo no diretório ctxfy/specifications/" in result
    assert "Conteúdo acessível para geração de código automatizada" in result