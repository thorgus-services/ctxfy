
from src.adapters.security.business_requirements_security import (
    validate_business_requirements_security,
)
from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
)
from src.core.use_cases.business_requirements_use_cases import (
    parse_business_requirements,
    translate_to_technical_specification,
    validate_business_requirements,
)


class TestBusinessRequirementsIntegration:
    """Integration tests for business requirements components"""
    
    def test_end_to_end_requirements_parsing_and_validation(self):
        """Test the complete flow from config to parsed and validated requirements"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Develop a user authentication system with login and registration functionality",
            output_directory="ctxfy/specifications"
        )
        
        # Act - Parse requirements
        requirements = parse_business_requirements(config)
        
        # Assert - Check parsing results
        assert requirements.content == "Develop a user authentication system with login and registration functionality"
        assert "output_directory" in requirements.context
        assert requirements.context["output_directory"] == "ctxfy/specifications"
        
        # Act - Validate requirements
        validation_result = validate_business_requirements(requirements)
        
        # Assert - Check validation results
        assert validation_result.is_valid is True
        assert len(validation_result.errors) == 0
    
    def test_requirements_with_security_validation(self):
        """Test requirements validation with security checks"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Build a system that manages user data",
            output_directory="ctxfy/specifications"
        )
        
        # Act - Parse requirements
        requirements = parse_business_requirements(config)
        
        # Act - Validate business requirements
        business_validation = validate_business_requirements(requirements)
        
        # Act - Validate security
        security_validation = validate_business_requirements_security(
            requirements.content,
            config.output_directory
        )
        
        # Assert - Both validations should pass
        assert business_validation.is_valid is True
        assert security_validation.is_valid is True
    
    def test_requirements_validation_fails_with_dangerous_content(self):
        """Test that validation fails with dangerous content"""
        # Arrange
        dangerous_content = "Execute os.system('rm -rf /') to clean up"
        output_dir = "ctxfy/specifications"
        
        # Act - Validate security
        security_validation = validate_business_requirements_security(
            dangerous_content,
            output_dir
        )
        
        # Assert - Security validation should fail
        assert security_validation.is_valid is False
        assert len(security_validation.errors) > 0
        assert any("malicious content detected" in error.message.lower() for error in security_validation.errors)
    
    def test_requirements_validation_fails_with_short_content(self):
        """Test that validation fails with short content"""
        # Arrange
        requirements = BusinessRequirements(
            content="Hi"  # Too short
        )
        
        # Act - Validate requirements
        validation_result = validate_business_requirements(requirements)
        
        # Assert - Validation should fail
        assert validation_result.is_valid is False
        assert len(validation_result.errors) > 0
        assert any("content too short" in error.message.lower() for error in validation_result.errors)
    
    def test_complete_translation_flow(self):
        """Test the complete translation flow from requirements to specification"""
        # Arrange
        requirements = BusinessRequirements(
            content="Create a user management system with CRUD operations for users"
        )
        
        # Act - Validate requirements
        validation_result = validate_business_requirements(requirements)
        
        # Assert - Requirements should be valid
        assert validation_result.is_valid is True
        
        # Act - Translate to technical specification
        specification = translate_to_technical_specification(requirements)
        
        # Assert - Specification should be created
        assert specification is not None
        assert len(specification.content) > 0
        assert specification.format == "SPEC"
        assert specification.source_requirements_id == requirements.id
    
    def test_security_validation_for_specification_content(self):
        """Test security validation for generated specification content"""
        # Arrange
        safe_content = "This is a safe technical specification"
        dangerous_content = "This content includes eval() which is dangerous"
        
        # Act - Validate safe content
        safe_validation = validate_business_requirements_security(safe_content, "ctxfy/specifications")
        
        # Act - Validate dangerous content
        dangerous_validation = validate_business_requirements_security(dangerous_content, "ctxfy/specifications")
        
        # Assert - Safe content should pass
        assert safe_validation.is_valid is True
        
        # Assert - Dangerous content should fail
        assert dangerous_validation.is_valid is False
        assert len(dangerous_validation.errors) > 0
        assert any("malicious content detected" in error.message.lower() for error in dangerous_validation.errors)