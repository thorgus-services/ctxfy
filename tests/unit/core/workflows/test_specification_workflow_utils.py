
import json

from src.core.models.specification_result import SpecificationResult
from src.core.models.specification_workflow import BusinessRequirements
from src.core.workflows.specification_workflow import (
    _clean_business_requirements,
    _extract_components_from_requirements,
    _extract_important_words,
    _format_specification_content,
    _generate_acceptance_criteria,
    _generate_description,
    _generate_specification_filename,
    _generate_specification_id,
    _validate_business_requirements,
    execute_specification_generation,
)


def test_validate_business_requirements_with_valid_input():
    """Test _validate_business_requirements with valid business requirements"""
    requirements = BusinessRequirements("Valid business requirements")
    assert _validate_business_requirements(requirements) is True


def test_validate_business_requirements_with_empty_input():
    """Test _validate_business_requirements with empty requirements"""
    requirements = BusinessRequirements("")
    assert _validate_business_requirements(requirements) is False


def test_validate_business_requirements_with_whitespace_only():
    """Test _validate_business_requirements with whitespace-only requirements"""
    requirements = BusinessRequirements("   ")
    assert _validate_business_requirements(requirements) is False


def test_validate_business_requirements_with_none_like_input():
    """Test _validate_business_requirements with None-like string input"""
    requirements = BusinessRequirements("None")
    assert _validate_business_requirements(requirements) is True


def test_clean_business_requirements_with_normal_input():
    """Test _clean_business_requirements with normal business requirements"""
    requirements = BusinessRequirements("User needs dashboard for metrics")
    cleaned = _clean_business_requirements(requirements)
    assert cleaned == "User needs dashboard for metrics"


def test_clean_business_requirements_with_special_characters():
    """Test _clean_business_requirements with special characters that should be removed"""
    requirements = BusinessRequirements("User needs dashboard for metrics!@#$%")
    cleaned = _clean_business_requirements(requirements)
    assert cleaned == "User needs dashboard for metrics"


def test_clean_business_requirements_with_punctuation():
    """Test _clean_business_requirements preserves allowed punctuation"""
    requirements = BusinessRequirements("User needs dashboard: real-time metrics; monitoring (alerts)")
    cleaned = _clean_business_requirements(requirements)
    assert cleaned == "User needs dashboard: real-time metrics; monitoring (alerts)"


def test_clean_business_requirements_with_empty_input():
    """Test _clean_business_requirements with empty input"""
    requirements = BusinessRequirements("")
    cleaned = _clean_business_requirements(requirements)
    assert cleaned == ""


def test_extract_important_words_with_multiple_words():
    """Test _extract_important_words extracts important words correctly"""
    text = "dashboard for metrics and analytics"
    result = _extract_important_words(text, max_words=3, min_length=4)
    assert result == ["dashboard", "metrics", "analytics"]


def test_extract_important_words_with_few_words():
    """Test _extract_important_words when there are fewer words than max"""
    text = "user interface"
    result = _extract_important_words(text, max_words=5, min_length=3)
    assert result == ["user", "interface"]


def test_extract_important_words_with_short_words_filtered():
    """Test _extract_important_words filters out short words"""
    text = "a user needs an interface for the dashboard"
    result = _extract_important_words(text, max_words=5, min_length=4)
    assert "a" not in result
    assert "an" not in result
    assert "the" not in result
    # "user" has 4 chars, so it should be included since min_length=4 means >= 4
    assert "user" in result
    assert "needs" in result
    assert "interface" in result
    assert "dashboard" in result


def test_extract_important_words_with_empty_input():
    """Test _extract_important_words with empty input"""
    text = ""
    result = _extract_important_words(text, max_words=3, min_length=4)
    assert result == ["spec"]


def test_generate_specification_id_with_same_content():
    """Test _generate_specification_id generates consistent IDs for same content"""
    content = "User needs dashboard for metrics"
    id1 = _generate_specification_id(content)
    id2 = _generate_specification_id(content)
    assert id1 == id2


def test_generate_specification_id_with_different_content():
    """Test _generate_specification_id generates different IDs for different content"""
    content1 = "User needs dashboard for metrics"
    content2 = "System needs API for authentication"
    id1 = _generate_specification_id(content1)
    id2 = _generate_specification_id(content2)
    assert id1 != id2


def test_generate_specification_id_output_format():
    """Test _generate_specification_id output format"""
    content = "User needs dashboard for metrics"
    spec_id = _generate_specification_id(content)
    assert len(spec_id) == 8
    int(spec_id, 16)


def test_generate_specification_filename_with_meaningful_words():
    """Test _generate_specification_filename generates filename with meaningful words"""
    content = "dashboard for metrics and analytics"
    filename = _generate_specification_filename(content)
    assert filename.startswith("spec_")
    assert filename.endswith(".json")
    assert "dashboard" in filename or "metrics" in filename or "analytics" in filename


def test_generate_specification_filename_with_short_content():
    """Test _generate_specification_filename with short content"""
    content = "API"
    filename = _generate_specification_filename(content)
    assert filename.startswith("spec_")
    assert filename.endswith(".json")


def test_generate_specification_filename_with_empty_content():
    """Test _generate_specification_filename with empty content"""
    content = ""
    filename = _generate_specification_filename(content)
    assert filename.startswith("spec_")
    assert filename.endswith(".json")


def test_generate_specification_filename_truncation():
    """Test _generate_specification_filename truncates long filenames"""
    content = "very_long_word_for_testing_filename_truncation_purposes"
    filename = _generate_specification_filename(content)
    assert len(filename) <= 30
    assert filename.startswith("spec_")
    assert filename.endswith(".json")


def test_extract_components_from_requirements_with_dashboard():
    """Test _extract_components_from_requirements detects dashboard requirements"""
    requirements = "User needs dashboard for metrics"
    components = _extract_components_from_requirements(requirements)
    assert "frontend/dashboard" in components
    assert "backend/metrics-service" in components


def test_extract_components_from_requirements_with_api():
    """Test _extract_components_from_requirements detects API requirements"""
    requirements = "System needs API for user management"
    components = _extract_components_from_requirements(requirements)
    assert "api/gateway" in components


def test_extract_components_from_requirements_with_interface():
    """Test _extract_components_from_requirements detects interface requirements"""
    requirements = "System needs user interface for data visualization"
    components = _extract_components_from_requirements(requirements)
    assert "api/gateway" in components


def test_extract_components_from_requirements_default():
    """Test _extract_components_from_requirements includes default save directory"""
    requirements = "Random requirement"
    components = _extract_components_from_requirements(requirements)
    assert "ctxfy/specifications/" in components


def test_extract_components_from_requirements_with_custom_directory():
    """Test _extract_components_from_requirements with custom save directory"""
    requirements = "User needs dashboard for metrics"
    components = _extract_components_from_requirements(requirements, "custom/path/")
    assert "custom/path/" in components
    assert "frontend/dashboard" in components
    assert "backend/metrics-service" in components


def test_generate_description_with_short_text():
    """Test _generate_description generates description for short text"""
    requirements = "User needs dashboard"
    description = _generate_description(requirements)
    assert description == "User needs dashboard"


def test_generate_description_with_long_text():
    """Test _generate_description truncates long text"""
    requirements = "User needs dashboard for metrics and analytics and reporting and visualization and monitoring and alerting and more functionality"
    description = _generate_description(requirements)
    assert len(description.split()) <= 16
    if len(requirements.split()) > 15:
        assert "..." in description
    else:
        long_requirements = " ".join([f"word{i}" for i in range(20)])
        long_description = _generate_description(long_requirements)
        assert "..." in long_description


def test_generate_acceptance_criteria_default_criteria():
    """Test _generate_acceptance_criteria includes default criteria"""
    requirements = "Random requirement"
    criteria = _generate_acceptance_criteria(requirements)
    assert "Especificação gerada no formato JSON válido" in criteria
    assert "Arquivo salvo no diretório ctxfy/specifications/" in criteria
    assert "Conteúdo acessível para geração de código automatizada" in criteria


def test_generate_acceptance_criteria_metrics_criteria():
    """Test _generate_acceptance_criteria includes metrics-specific criteria"""
    requirements = "System with metrics and real-time monitoring"
    criteria = _generate_acceptance_criteria(requirements)
    assert "Dashboard exibe métricas em tempo real" in criteria


def test_generate_acceptance_criteria_no_metrics_criteria():
    """Test _generate_acceptance_criteria does not include metrics criteria when not relevant"""
    requirements = "System for file storage"
    criteria = _generate_acceptance_criteria(requirements)
    assert "Dashboard exibe métricas em tempo real" not in criteria


def test_format_specification_content_basic_structure():
    """Test _format_specification_content creates proper JSON structure"""
    requirements = "User needs dashboard for metrics"
    content = _format_specification_content(requirements)

    data = json.loads(content)

    assert "title" in data
    assert "description" in data
    assert "business_requirements" in data
    assert "architecture" in data
    assert "components" in data
    assert "interfaces" in data
    assert "security" in data
    assert "acceptance_criteria" in data
    assert "created_at" in data

    assert data["business_requirements"] == requirements


def test_format_specification_content_with_custom_directory():
    """Test _format_specification_content includes custom directory in components"""
    requirements = "User needs dashboard for metrics"
    content = _format_specification_content(requirements, "custom/path/")

    data = json.loads(content)

    assert "custom/path/" in str(data["components"])


def test_format_specification_content_with_dashboard_requirements():
    """Test _format_specification_content detects dashboard in requirements"""
    requirements = "User needs dashboard for metrics"
    content = _format_specification_content(requirements)

    data = json.loads(content)

    components_str = str(data["components"])
    assert "dashboard" in components_str


def test_execute_specification_generation_basic():
    """Test execute_specification_generation function creates proper SpecificationResult"""

    requirements = BusinessRequirements("User needs dashboard for metrics")
    result = execute_specification_generation(requirements)

    assert isinstance(result, SpecificationResult)
    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert result.content.startswith("{")
    assert "dashboard" in result.content.lower()


def test_execute_specification_generation_with_custom_directory():
    """Test execute_specification_generation function with custom save directory"""

    requirements = BusinessRequirements("User needs API for authentication")
    result = execute_specification_generation(requirements, "custom/path/")

    assert isinstance(result, SpecificationResult)
    assert "custom/path/" in result.content
    assert "api" in result.content.lower()