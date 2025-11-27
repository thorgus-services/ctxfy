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
)


def test_format_specification_content_with_timestamp():
    """Test formatting specification content with provided timestamp"""
    requirements = "Build a user dashboard"
    save_directory = "ctxfy/specifications/"
    created_at = "2023-01-01T00:00:00Z"
    
    result = _format_specification_content(requirements, save_directory, created_at)
    
    assert "user dashboard" in result
    assert "2023-01-01T00:00:00Z" in result
    assert save_directory in result
    assert result.startswith('{')
    assert '"created_at": "2023-01-01T00:00:00Z"' in result


def test_format_specification_content_with_empty_timestamp():
    """Test formatting specification content with empty timestamp"""
    requirements = "Build a user dashboard"
    
    result = _format_specification_content(requirements, "ctxfy/specifications/", "")
    
    assert "user dashboard" in result
    assert '"created_at": ""' in result


def test_validate_business_requirements_with_valid_input():
    """Test validation of valid business requirements"""
    valid_requirements = "Create a dashboard for user metrics"
    
    result = _validate_business_requirements(valid_requirements)
    
    assert result is True


def test_validate_business_requirements_with_empty_input():
    """Test validation of empty business requirements"""
    empty_requirements = ""
    
    result = _validate_business_requirements(empty_requirements)
    
    assert result is False


def test_validate_business_requirements_with_whitespace_only():
    """Test validation of whitespace-only business requirements"""
    whitespace_requirements = "   \n\t  "
    
    result = _validate_business_requirements(whitespace_requirements)
    
    assert result is False


def test_clean_business_requirements_removes_special_chars():
    """Test cleaning business requirements removes special characters"""
    # Note: The function preserves some special characters: ., :; - and ()
    dirty_requirements = "Build a dashboard!@#$%^&*() for users"

    result = _clean_business_requirements(dirty_requirements)

    # Only parentheses are preserved, other special chars are removed
    expected = "Build a dashboard() for users"
    assert result == expected


def test_clean_business_requirements_preserves_valid_chars():
    """Test cleaning business requirements preserves valid characters"""
    requirements_with_valid_chars = "Build a dashboard, for users: requirements; (metrics)"
    
    result = _clean_business_requirements(requirements_with_valid_chars)
    
    assert result == requirements_with_valid_chars


def test_extract_important_words_from_short_text():
    """Test extracting important words from short text"""
    text = "user dashboard metrics"
    
    result = _extract_important_words(text, max_words=3, min_length=3)
    
    assert "user" in result
    assert "dashboard" in result
    assert len(result) <= 3


def test_extract_important_words_from_long_text():
    """Test extracting important words from long text"""
    text = "create a comprehensive user dashboard with metrics reporting and analytics capabilities"
    
    result = _extract_important_words(text, max_words=4, min_length=4)
    
    assert len(result) <= 4
    assert all(len(word) >= 4 for word in result)


def test_generate_specification_id_from_content():
    """Test generating specification ID from content"""
    content = "user dashboard requirements"
    
    result = _generate_specification_id(content)
    
    assert isinstance(result, str)
    assert len(result) == 8  # First 8 chars of SHA256 hash


def test_generate_specification_filename_from_content():
    """Test generating specification filename from content"""
    content = "User dashboard for metrics"
    
    result = _generate_specification_filename(content)
    
    assert result.startswith("spec_")
    assert result.endswith(".json")
    assert "dashboard" in result or "user" in result


def test_generate_specification_filename_with_no_meaningful_words():
    """Test generating specification filename when no meaningful words found"""
    content = "a an the of"
    
    result = _generate_specification_filename(content)
    
    assert result.startswith("spec_")
    assert result.endswith(".json")


def test_extract_components_from_requirements_with_dashboard():
    """Test extracting components when requirements contain 'dashboard'"""
    requirements = "Create a dashboard for metrics"
    
    result = _extract_components_from_requirements(requirements, "ctxfy/specifications/")
    
    assert "ctxfy/specifications/" in result
    assert "frontend/dashboard" in result
    assert "backend/metrics-service" in result


def test_extract_components_from_requirements_with_api():
    """Test extracting components when requirements contain 'api'"""
    requirements = "Need an API for user management"
    
    result = _extract_components_from_requirements(requirements, "ctxfy/specifications/")
    
    assert "ctxfy/specifications/" in result
    assert "api/gateway" in result


def test_generate_description_from_short_requirements():
    """Test generating description from short requirements"""
    requirements = "Build a user dashboard for metrics"
    
    result = _generate_description(requirements)
    
    assert result == "Build a user dashboard for metrics"


def test_generate_description_from_long_requirements():
    """Test generating description from long requirements (truncated)"""
    requirements = "Build a comprehensive user dashboard for monitoring all system metrics including CPU, memory, disk usage, network traffic, and application performance in real-time with alerting capabilities and historical reporting"
    
    result = _generate_description(requirements)
    
    assert result.endswith("...")
    assert len(result.split()) <= 16  # 15 + "..."


def test_generate_acceptance_criteria_basic():
    """Test generating basic acceptance criteria"""
    requirements = "General requirements"
    
    result = _generate_acceptance_criteria(requirements)
    
    assert "Especificação gerada no formato JSON válido" in result
    assert "Arquivo salvo no diretório ctxfy/specifications/" in result
    assert "Conteúdo acessível para geração de código automatizada" in result


def test_generate_acceptance_criteria_with_metrics():
    """Test generating acceptance criteria specific to metrics requirements"""
    requirements = "System with metrics reporting dashboard"

    result = _generate_acceptance_criteria(requirements)

    assert "Dashboard exibe métricas em tempo real" in result


def test_format_specification_content_with_special_characters():
    """Test formatting specification content with special characters that need escaping"""
    requirements = 'Build an API with "quotes" and {braces}'
    save_directory = "ctxfy/specifications/"
    created_at = "2023-01-01T00:00:00Z"

    result = _format_specification_content(requirements, save_directory, created_at)

    # Ensure JSON is properly formatted even with special characters
    assert result.startswith('{')
    assert '"business_requirements": "Build an API with \\"quotes\\" and {braces}"' in result
    assert created_at in result