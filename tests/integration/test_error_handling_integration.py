
from src.adapters.validation import SchemaValidationAdapter
from src.core.models.error_models import (
    ApplicationError,
    ErrorCodes,
    ErrorDetails,
    ErrorResponse,
)
from src.core.models.validation_models import ValidationError


def test_complete_validation_error_flow():
    """Test complete validation with error handling and structured responses."""
    # Create some test data with validation errors
    invalid_data = {
        "name": "",  # Empty name should fail validation
        "parameters": "not_a_dict",  # Should be dict
        "request_id": "valid_id"
    }
    
    # Validate the data
    result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
    
    # Check that validation failed
    assert result.is_valid is False
    assert len(result.errors) > 0
    
    # Check that errors are properly structured
    for error in result.errors:
        assert isinstance(error, ValidationError)
        assert error.field in ["name", "parameters"]
        assert isinstance(error.message, str)
        assert isinstance(error.code, str)


def test_structured_error_response_creation():
    """Test creating structured error responses."""
    error_response = SchemaValidationAdapter.create_structured_error_response(
        error_code=ErrorCodes.VALIDATION_ERROR,
        message="Validation failed for field 'name'",
        details="Name field cannot be empty",
        request_id="req-123",
        status_code=400
    )
    
    # Check that the error response is properly structured
    assert isinstance(error_response, ErrorResponse)
    assert isinstance(error_response.error, ApplicationError)
    assert error_response.error.error_code == ErrorCodes.VALIDATION_ERROR
    assert "Validation failed" in error_response.error.message
    assert error_response.error.request_id == "req-123"
    assert error_response.status_code == 400
    assert len(error_response.details) > 0
    assert isinstance(error_response.details[0], ErrorDetails)


def test_error_response_with_multiple_details():
    """Test error response with multiple error details."""
    # Create an error
    error = ApplicationError(
        error_code=ErrorCodes.PROCESSING_ERROR,
        message="Multiple validation issues occurred",
        details="Several fields failed validation"
    )
    
    # Create error details
    details = (
        ErrorDetails(field_name="name", error_type="invalid_type", description="Name must be non-empty", code="VAL_001"),
        ErrorDetails(field_name="age", error_type="invalid_range", description="Age must be positive", code="VAL_002")
    )
    
    # Create error response
    error_response = ErrorResponse(
        error=error,
        details=details,
        status_code=422
    )
    
    # Validate structure
    assert error_response.error.error_code == ErrorCodes.PROCESSING_ERROR
    assert len(error_response.details) == 2
    assert error_response.status_code == 422
    assert error_response.details[0].field_name == "name"
    assert error_response.details[1].field_name == "age"


def test_error_codes_constants():
    """Test that all expected error codes are defined."""
    assert hasattr(ErrorCodes, 'VALIDATION_ERROR')
    assert hasattr(ErrorCodes, 'INVALID_TEMPLATE')
    assert hasattr(ErrorCodes, 'INVALID_REQUEST')
    assert hasattr(ErrorCodes, 'INJECTION_ATTEMPT')
    assert hasattr(ErrorCodes, 'PROCESSING_ERROR')
    assert hasattr(ErrorCodes, 'LLM_SAMPLING_ERROR')
    assert hasattr(ErrorCodes, 'TEMPLATE_RENDERING_ERROR')
    assert hasattr(ErrorCodes, 'INTERNAL_ERROR')
    assert hasattr(ErrorCodes, 'TIMEOUT_ERROR')
    assert hasattr(ErrorCodes, 'AUTHENTICATION_ERROR')
    assert hasattr(ErrorCodes, 'AUTHORIZATION_ERROR')