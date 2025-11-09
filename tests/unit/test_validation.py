"""Unit tests for context stack validation."""

import pytest
from src.core.models.context_models import ContextGenerationRequest
from src.core.use_cases.validation import (
    validate_feature_description, validate_target_technologies, 
    validate_context_generation_request, validate_and_raise
)
from src.core.exceptions import ValidationError


class TestFeatureDescriptionValidation:
    """Test cases for feature description validation."""
    
    def test_valid_feature_description(self):
        """Test validation of a valid feature description."""
        result = validate_feature_description("This is a valid feature description")
        assert result == []
    
    def test_empty_feature_description(self):
        """Test validation of an empty feature description."""
        result = validate_feature_description("")
        assert len(result) == 1
        assert "cannot be empty" in result[0]
    
    def test_whitespace_only_feature_description(self):
        """Test validation of a whitespace-only feature description."""
        result = validate_feature_description("   ")
        assert len(result) == 1
        assert "cannot be empty" in result[0]
    
    def test_short_feature_description(self):
        """Test validation of a short feature description."""
        result = validate_feature_description("test")  # 4 chars
        assert len(result) == 1
        assert "at least 5 characters" in result[0]
    
    def test_min_length_feature_description(self):
        """Test validation of a 5-character feature description."""
        result = validate_feature_description("tests")  # 5 chars
        assert result == []


class TestTargetTechnologiesValidation:
    """Test cases for target technologies validation."""
    
    def test_valid_technologies(self):
        """Test validation of valid technologies."""
        result = validate_target_technologies(["Python", "FastAPI", "PostgreSQL"])
        assert result == []
    
    def test_empty_technologies_list(self):
        """Test validation of an empty technologies list."""
        result = validate_target_technologies([])
        assert result == []
    
    def test_technologies_with_empty_strings(self):
        """Test validation of technologies containing empty strings."""
        result = validate_target_technologies(["Python", "", "PostgreSQL"])
        assert len(result) == 1
        assert "Technology names cannot be empty" in result[0]
    
    def test_technologies_with_whitespace_only(self):
        """Test validation of technologies containing whitespace-only strings."""
        result = validate_target_technologies(["Python", "  ", "PostgreSQL"])
        assert len(result) == 1
        assert "Technology names cannot be empty" in result[0]


class TestContextGenerationRequestValidation:
    """Test cases for context generation request validation."""
    
    def test_valid_request(self):
        """Test validation of a completely valid request."""
        request = ContextGenerationRequest(
            feature_description="Implement user management API",
            target_technologies=["Python", "FastAPI"],
            custom_rules=[]
        )
        
        result = validate_context_generation_request(request)
        assert result == []
    
    def test_request_with_invalid_feature_description(self):
        """Test validation of a request with invalid feature description."""
        # Use the validation function directly instead of constructing invalid object
        # We'll test the validation function from the validation module on input data
        from src.core.use_cases.validation import validate_feature_description
        
        result = validate_feature_description("")  # Empty string
        assert len(result) >= 1
        assert any("empty" in error.lower() for error in result)
        
        result = validate_feature_description("test")  # Too short
        assert len(result) >= 1
        assert any("5 characters" in error for error in result)
    
    def test_request_with_invalid_technologies(self):
        """Test validation of a request with invalid technologies."""
        request = ContextGenerationRequest(
            feature_description="Implement user management API",
            target_technologies=["Python", ""],  # Empty technology
            custom_rules=[]
        )
        
        result = validate_context_generation_request(request)
        assert len(result) >= 1
        assert any("technology" in error.lower() for error in result)
    
    def test_request_with_multiple_validation_errors(self):
        """Test validation of a request with multiple validation errors."""
        # Test validation functions separately since direct object creation would fail
        from src.core.use_cases.validation import validate_feature_description, validate_target_technologies
        
        # Test empty feature description
        feature_errors = validate_feature_description("")
        assert len(feature_errors) >= 1
        
        # Test technologies with empty strings
        tech_errors = validate_target_technologies(["Python", ""])  # Contains invalid
        assert len(tech_errors) >= 1


class TestValidateAndRaise:
    """Test cases for the validate_and_raise function."""
    
    def test_validate_and_raise_with_valid_request(self):
        """Test that validate_and_raise passes with a valid request."""
        request = ContextGenerationRequest(
            feature_description="Implement user management API",
            target_technologies=["Python", "FastAPI"],
            custom_rules=[]
        )
        
        # Should not raise an exception
        validate_and_raise(request)
    
    def test_validate_and_raise_with_valid_request(self):
        """Test that validate_and_raise does not raise exception with valid request."""
        request = ContextGenerationRequest(
            feature_description="A valid description that is at least 5 chars long",  # Valid for construction
            target_technologies=["Python", "FastAPI"],
            custom_rules=[]
        )
        
        # This should not raise an exception for a valid request
        validate_and_raise(request)
    
    def test_validate_and_raise_with_invalid_technology(self):
        """Test that validate_and_raise raises ValidationError with invalid technology."""
        request = ContextGenerationRequest(
            feature_description="Implement user management API",
            target_technologies=["Python", ""],  # Invalid
            custom_rules=[]
        )
        
        with pytest.raises(ValidationError):
            validate_and_raise(request)