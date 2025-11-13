import pytest

from src.core.models.validation_models import ValidationError, ValidationResult


def test_validation_error_with_valid_data_creates_instance():
    """Test that ValidationError can be created with valid data"""
    error = ValidationError(
        field="test_field",
        message="Test error message",
        code="TEST_ERROR"
    )
    assert error.field == "test_field"
    assert error.message == "Test error message"
    assert error.code == "TEST_ERROR"
    assert error.details is None


def test_validation_error_with_details_creates_instance():
    """Test that ValidationError can be created with details"""
    error = ValidationError(
        field="test_field",
        message="Test error message",
        code="TEST_ERROR",
        details="Additional error details"
    )
    assert error.field == "test_field"
    assert error.message == "Test error message"
    assert error.code == "TEST_ERROR"
    assert error.details == "Additional error details"


def test_validation_error_with_invalid_field_raises_error():
    """Test that ValidationError with invalid field raises error"""
    with pytest.raises(ValueError):
        ValidationError(
            field="",  # Invalid - empty
            message="Test error message",
            code="TEST_ERROR"
        )


def test_validation_error_with_invalid_message_raises_error():
    """Test that ValidationError with invalid message raises error"""
    with pytest.raises(ValueError):
        ValidationError(
            field="test_field",
            message="",  # Invalid - empty
            code="TEST_ERROR"
        )


def test_validation_error_with_invalid_code_raises_error():
    """Test that ValidationError with invalid code raises error"""
    with pytest.raises(ValueError):
        ValidationError(
            field="test_field",
            message="Test error message",
            code=""  # Invalid - empty
        )


def test_validation_error_with_invalid_details_raises_error():
    """Test that ValidationError with invalid details raises error"""
    with pytest.raises(ValueError):
        ValidationError(
            field="test_field",
            message="Test error message",
            code="TEST_ERROR",
            details=123  # Invalid - should be string or None
        )


def test_validation_result_with_valid_data_creates_instance():
    """Test that ValidationResult can be created with valid data"""
    error = ValidationError(
        field="test_field",
        message="Test error message",
        code="TEST_ERROR"
    )
    result = ValidationResult(
        is_valid=False,
        errors=(error,),
        details="Validation process details"
    )
    assert result.is_valid is False
    assert len(result.errors) == 1
    assert result.details == "Validation process details"


def test_validation_result_defaults():
    """Test that ValidationResult has proper defaults"""
    result = ValidationResult(is_valid=True)
    assert result.is_valid is True
    assert result.errors == ()
    assert result.details is None


def test_validation_result_with_invalid_is_valid_raises_error():
    """Test that ValidationResult with invalid is_valid raises error"""
    with pytest.raises(ValueError):
        ValidationResult(
            is_valid="not_a_boolean",  # Should be boolean
            errors=()
        )


def test_validation_result_with_invalid_errors_raises_error():
    """Test that ValidationResult with invalid errors raises error"""
    with pytest.raises(ValueError):
        ValidationResult(
            is_valid=True,
            errors="not_a_tuple"  # Should be tuple
        )


def test_validation_result_with_invalid_error_type_raises_error():
    """Test that ValidationResult with invalid error type raises error"""
    with pytest.raises(ValueError):
        ValidationResult(
            is_valid=False,
            errors=(  # Tuple containing invalid type
                "not_a_validation_error",
            )
        )


def test_validation_result_with_invalid_details_type_raises_error():
    """Test that ValidationResult with invalid details type raises error"""
    error = ValidationError(
        field="test_field",
        message="Test error message", 
        code="TEST_ERROR"
    )
    with pytest.raises(ValueError):
        ValidationResult(
            is_valid=False,
            errors=(error,),
            details=123  # Should be string or None
        )