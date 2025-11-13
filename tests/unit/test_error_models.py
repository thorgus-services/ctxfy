from datetime import datetime

import pytest

from src.core.models.error_models import (
    ApplicationError,
    ErrorCodes,
    ErrorDetails,
    ErrorResponse,
)


def test_application_error_with_valid_data_creates_instance():
    """Test that ApplicationError can be created with valid data"""
    error = ApplicationError(
        error_code="TEST_ERROR",
        message="Test error message"
    )
    assert error.error_code == "TEST_ERROR"
    assert error.message == "Test error message"
    assert isinstance(error.timestamp, datetime)


def test_application_error_with_invalid_error_code_raises_error():
    """Test that ApplicationError with invalid error code raises error"""
    with pytest.raises(ValueError):
        ApplicationError(
            error_code="",  # Invalid - empty
            message="Test error message"
        )


def test_application_error_with_invalid_message_raises_error():
    """Test that ApplicationError with invalid message raises error"""
    with pytest.raises(ValueError):
        ApplicationError(
            error_code="TEST_ERROR",
            message=""  # Invalid - empty
        )


def test_error_details_with_valid_data_creates_instance():
    """Test that ErrorDetails can be created with valid data"""
    error_detail = ErrorDetails(
        field_name="test_field",
        error_type="validation_error",
        description="Test description",
        code="ERR001"
    )
    assert error_detail.field_name == "test_field"
    assert error_detail.error_type == "validation_error"
    assert error_detail.description == "Test description"
    assert error_detail.code == "ERR001"


def test_error_details_with_invalid_field_name():
    """Test that ErrorDetails with invalid field name handles correctly"""
    # Field name can be None, so let's test with a non-string value
    with pytest.raises(ValueError):
        ErrorDetails(
            field_name=123  # Invalid - not string or None
        )


def test_error_response_with_valid_data_creates_instance():
    """Test that ErrorResponse can be created with valid data"""
    app_error = ApplicationError(
        error_code=ErrorCodes.VALIDATION_ERROR,
        message="Validation failed"
    )
    details = (
        ErrorDetails(
            field_name="test_field",
            error_type="validation_error",
            description="Field failed validation",
            code="ERR001"
        ),
    )
    response = ErrorResponse(
        error=app_error,
        details=details,
        status_code=400
    )
    assert isinstance(response.error, ApplicationError)
    assert len(response.details) == 1
    assert response.status_code == 400


def test_error_response_with_invalid_error_raises_error():
    """Test that ErrorResponse with invalid error raises error"""
    with pytest.raises(ValueError):
        ErrorResponse(
            error="invalid_error_type",  # Should be ApplicationError instance
            details=(),
            status_code=400
        )


def test_error_response_with_invalid_status_code_raises_error():
    """Test that ErrorResponse with invalid status code raises error"""
    app_error = ApplicationError(
        error_code=ErrorCodes.VALIDATION_ERROR,
        message="Validation failed"
    )
    with pytest.raises(ValueError):
        ErrorResponse(
            error=app_error,
            details=(),
            status_code=99  # Invalid - not a valid HTTP status code
        )


def test_error_codes_constants():
    """Test that ErrorCodes constants are defined properly"""
    assert ErrorCodes.VALIDATION_ERROR == "VALIDATION_ERROR"
    assert ErrorCodes.INVALID_TEMPLATE == "INVALID_TEMPLATE"
    assert ErrorCodes.INVALID_REQUEST == "INVALID_REQUEST"
    assert ErrorCodes.PROCESSING_ERROR == "PROCESSING_ERROR"
    assert ErrorCodes.INTERNAL_ERROR == "INTERNAL_ERROR"