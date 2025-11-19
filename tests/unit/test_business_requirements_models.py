from datetime import datetime

import pytest

from src.adapters.security.business_requirements_security import (
    build_secure_output_path,
    sanitize_requirements_text,
    validate_business_requirements_security,
    validate_specification_content,
)
from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
    TechnicalSpecification,
    TranslationResult,
    TranslationStatus,
)
from src.core.use_cases.business_requirements_use_cases import (
    parse_business_requirements,
    translate_to_technical_specification,
    validate_business_requirements,
    validate_translation_config,
)


class TestBusinessRequirementConfig:
    """Test cases for BusinessRequirementConfig value object"""
    
    def test_valid_config_creation(self):
        """Test creating a valid BusinessRequirementConfig"""
        config = BusinessRequirementConfig(
            requirements_text="Test business requirements",
            output_directory="ctxfy/specifications"
        )
        assert config.requirements_text == "Test business requirements"
        assert config.output_directory == "ctxfy/specifications"
        assert isinstance(config.security_context, dict)
        assert isinstance(config.validation_rules, tuple)
    
    def test_config_creation_with_defaults(self):
        """Test creating a config with default values"""
        config = BusinessRequirementConfig(requirements_text="Test requirements")
        assert config.output_directory == "ctxfy/specifications"
        assert config.requirements_text == "Test requirements"
    
    def test_config_validation_fails_empty_requirements(self):
        """Test that config validation fails with empty requirements text"""
        with pytest.raises(ValueError, match="Requirements text must be a valid string"):
            BusinessRequirementConfig(requirements_text="")
    
    def test_config_validation_fails_empty_output_directory(self):
        """Test that config validation fails with empty output directory"""
        with pytest.raises(ValueError, match="Output directory must be a valid string"):
            BusinessRequirementConfig(requirements_text="Test", output_directory="")


class TestBusinessRequirements:
    """Test cases for BusinessRequirements value object"""
    
    def test_valid_business_requirements_creation(self):
        """Test creating valid BusinessRequirements"""
        requirements = BusinessRequirements(
            id="test-id",
            content="Test business requirements content",
            context={"key": "value"},
            metadata={"source": "test"}
        )
        assert requirements.id == "test-id"
        assert requirements.content == "Test business requirements content"
        assert requirements.context == {"key": "value"}
        assert requirements.metadata == {"source": "test"}
    
    def test_business_requirements_creation_with_defaults(self):
        """Test creating BusinessRequirements with default values"""
        requirements = BusinessRequirements(content="Test content")
        assert requirements.id is not None
        assert requirements.content == "Test content"
        assert isinstance(requirements.context, dict)
        assert isinstance(requirements.metadata, dict)
    
    def test_business_requirements_validation_fails_empty_content(self):
        """Test that creation fails with empty content"""
        with pytest.raises(ValueError, match="Content must be a valid string"):
            BusinessRequirements(content="")


class TestTechnicalSpecification:
    """Test cases for TechnicalSpecification value object"""
    
    def test_valid_technical_specification_creation(self):
        """Test creating valid TechnicalSpecification"""
        spec = TechnicalSpecification(
            content="Technical specification content",
            format="SPEC",
            source_requirements_id="req-123"
        )
        assert spec.content == "Technical specification content"
        assert spec.format == "SPEC"
        assert spec.source_requirements_id == "req-123"
        assert isinstance(spec.generated_at, datetime)
    
    def test_technical_specification_creation_with_defaults(self):
        """Test creating TechnicalSpecification with default values"""
        spec = TechnicalSpecification(content="Content", format="SPEC")
        assert spec.content == "Content"
        assert spec.format == "SPEC"
        assert spec.spec_id is not None


class TestTranslationResult:
    """Test cases for TranslationResult value object"""
    
    def test_valid_translation_result_creation(self):
        """Test creating valid TranslationResult"""
        spec = TechnicalSpecification(content="Content", format="SPEC")
        result = TranslationResult(
            success=True,
            specification=spec,
            errors=(),
            warnings=("Warning1",)
        )
        assert result.success is True
        assert result.specification == spec
        assert result.errors == ()
        assert result.warnings == ("Warning1",)
    
    def test_translation_result_creation_with_failure(self):
        """Test creating TranslationResult for failure case"""
        result = TranslationResult(
            success=False,
            errors=("Error1", "Error2"),
            warnings=()
        )
        assert result.success is False
        assert result.specification is None
        assert result.errors == ("Error1", "Error2")


class TestTranslationStatus:
    """Test cases for TranslationStatus value object"""
    
    def test_valid_translation_status_creation(self):
        """Test creating valid TranslationStatus"""
        status = TranslationStatus(
            translation_id="trans-123",
            status="completed",
            progress=1.0
        )
        assert status.translation_id == "trans-123"
        assert status.status == "completed"
        assert status.progress == 1.0
    
    def test_translation_status_validation_fails_invalid_status(self):
        """Test that creation fails with invalid status"""
        with pytest.raises(ValueError, match="Status must be one of"):
            TranslationStatus(translation_id="trans-123", status="invalid")
    
    def test_translation_status_validation_fails_invalid_progress(self):
        """Test that creation fails with invalid progress value"""
        with pytest.raises(ValueError, match="Progress must be between 0.0 and 1.0"):
            TranslationStatus(translation_id="trans-123", status="pending", progress=2.0)


class TestBusinessRequirementsUseCases:
    """Test cases for business requirements use cases"""
    
    def test_parse_business_requirements(self):
        """Test parsing business requirements from config"""
        config = BusinessRequirementConfig(
            requirements_text="Implement user authentication system",
            output_directory="ctxfy/specifications"
        )
        requirements = parse_business_requirements(config)
        
        assert requirements.content == "Implement user authentication system"
        assert "output_directory" in requirements.context
        assert "parsed_at" in requirements.context
        assert requirements.metadata["character_count"] == len("Implement user authentication system")
    
    def test_validate_business_requirements_valid(self):
        """Test validating valid business requirements"""
        requirements = BusinessRequirements(
            content="This is a valid business requirement with sufficient content to pass validation"
        )
        result = validate_business_requirements(requirements)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_validate_business_requirements_invalid_short_content(self):
        """Test validating business requirements with short content"""
        requirements = BusinessRequirements(content="Hi")
        result = validate_business_requirements(requirements)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("content too short" in error.message.lower() for error in result.errors)

    def test_validate_business_requirements_sensitive_content(self):
        """Test validating business requirements with sensitive content"""
        requirements = BusinessRequirements(content="Need to store password in database")
        result = validate_business_requirements(requirements)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("sensitive information detected" in error.message.lower() for error in result.errors)
    
    def test_validate_translation_config_valid(self):
        """Test validating valid translation configuration"""
        config = BusinessRequirementConfig(
            requirements_text="Valid business requirements",
            output_directory="ctxfy/specifications"
        )
        result = validate_translation_config(config)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_translate_to_technical_specification(self):
        """Test translating business requirements to technical specification"""
        requirements = BusinessRequirements(content="Create a login system")
        spec = translate_to_technical_specification(requirements)
        
        assert spec.content is not None
        assert len(spec.content) > 0
        assert spec.format == "SPEC"
        assert spec.source_requirements_id == requirements.id


class TestSecurityValidation:
    """Test cases for security validation functions"""
    
    def test_validate_business_requirements_security_safe_content(self):
        """Test validating safe business requirements"""
        result = validate_business_requirements_security(
            "Implement user registration system",
            "ctxfy/specifications"
        )
        assert result.is_valid is True
    
    def test_validate_business_requirements_security_dangerous_path(self):
        """Test validating requirements with dangerous path"""
        result = validate_business_requirements_security(
            "Implement user registration",
            "../../../etc"
        )
        assert result.is_valid is False
        assert len(result.errors) > 0
        # Check for any error containing path traversal related terms
        assert any("traversal" in error.message.lower() or "path" in error.message.lower() for error in result.errors)
    
    def test_validate_business_requirements_security_dangerous_content(self):
        """Test validating requirements with dangerous content"""
        result = validate_business_requirements_security(
            "Execute os.system command",
            "ctxfy/specifications"
        )
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("malicious content detected" in error.message.lower() for error in result.errors)
    
    def test_validate_specification_content_safe(self):
        """Test validating safe specification content"""
        result = validate_specification_content("This is a safe specification")
        assert result.is_valid is True
    
    def test_validate_specification_content_dangerous(self):
        """Test validating specification content with dangerous patterns"""
        result = validate_specification_content("This content contains eval() function")
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("dangerous pattern detected" in error.message.lower() for error in result.errors)
    
    def test_sanitize_requirements_text(self):
        """Test sanitizing requirements text"""
        text_with_traversal = "Requirements with ../ traversal attempt"
        sanitized = sanitize_requirements_text(text_with_traversal)
        assert "../" not in sanitized
        assert "Requirements with  traversal attempt" == sanitized
    
    def test_build_secure_output_path_valid(self):
        """Test building secure output path with valid inputs"""
        path = build_secure_output_path("ctxfy/specifications", "test_spec.md")
        assert path == "ctxfy/specifications/test_spec.md"
    
    def test_build_secure_output_path_invalid_traversal(self):
        """Test building secure output path with traversal attempt"""
        with pytest.raises(ValueError, match="Directory traversal detected"):
            build_secure_output_path("ctxfy/specifications", "../../../test_spec.md")