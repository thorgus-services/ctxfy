
from src.adapters.validation import SchemaValidationAdapter


def test_schema_validation_adapter_validate_prompt_request_with_valid_data():
    """Test SchemaValidationAdapter with valid prompt request data"""
    valid_data = {
        "name": "test_prompt",
        "parameters": {"param1": "value1"},
        "request_id": "req-123"
    }
    
    result = SchemaValidationAdapter.validate_prompt_request(valid_data)
    assert result.is_valid is True
    assert result.errors == ()


def test_schema_validation_adapter_validate_prompt_request_with_invalid_name():
    """Test SchemaValidationAdapter with invalid name"""
    invalid_data = {
        "name": "",  # Invalid - empty
        "parameters": {"param1": "value1"},
        "request_id": "req-123"
    }
    
    result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert any(error.field == "name" for error in result.errors)


def test_schema_validation_adapter_validate_prompt_request_with_invalid_parameters():
    """Test SchemaValidationAdapter with invalid parameters"""
    invalid_data = {
        "name": "test_prompt",
        "parameters": "not_a_dict",  # Invalid - should be dict
        "request_id": "req-123"
    }
    
    result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert any(error.field == "parameters" for error in result.errors)


def test_schema_validation_adapter_validate_prompt_request_with_invalid_request_id():
    """Test SchemaValidationAdapter with invalid request_id"""
    invalid_data = {
        "name": "test_prompt",
        "parameters": {"param1": "value1"},
        "request_id": ""  # Invalid - empty
    }
    
    result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert any(error.field == "request_id" for error in result.errors)


def test_schema_validation_adapter_validate_prompt_request_missing_required_fields():
    """Test SchemaValidationAdapter with missing required fields"""
    custom_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "parameters": {"type": "object"},
            "request_id": {"type": "string", "minLength": 1},
            "user_id": {"type": "string", "minLength": 1}
        },
        "required": ["name", "parameters", "request_id", "user_id"]  # user_id is required
    }
    
    invalid_data = {
        "name": "test_prompt",
        "parameters": {"param1": "value1"},
        "request_id": "req-123"
        # Missing user_id
    }
    
    result = SchemaValidationAdapter.validate_prompt_request(invalid_data, custom_schema)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert any("user_id" in error.field for error in result.errors)


def test_schema_validation_adapter_validate_prompt_request_with_custom_schema():
    """Test SchemaValidationAdapter with custom schema (validates basic structure, not type constraints)"""
    custom_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "parameters": {"type": "object"},
            "request_id": {"type": "string", "minLength": 1},
            "age": {"type": "integer"}
        },
        "required": ["name", "parameters", "request_id"]
    }
    
    data_with_extra_field = {
        "name": "test_prompt",
        "parameters": {"param1": "value1"},
        "request_id": "req-123",
        "age": "not_an_integer"  # This won't be validated by the basic validation
    }
    
    # Basic validation passes because age isn't in required fields
    result = SchemaValidationAdapter.validate_prompt_request(data_with_extra_field, custom_schema)
    assert result.is_valid is True


def test_schema_validation_adapter_validate_prompt_request_with_exception():
    """Test SchemaValidationAdapter when exception occurs during validation"""
    # Provide data that will cause an exception during validation
    result = SchemaValidationAdapter.validate_prompt_request(None)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert result.errors[0].code == "validation_exception"


def test_schema_validation_adapter_create_pydantic_model_from_schema():
    """Test creating Pydantic model from schema"""
    schema = {
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name"]
    }
    
    model_class = SchemaValidationAdapter.create_pydantic_model_from_schema(schema, "TestModel")
    assert model_class.__name__ == "TestModel"
    
    # Test creating an instance
    instance = model_class(name="Alice", age=30)
    assert instance.name == "Alice"
    assert instance.age == 30


def test_schema_validation_adapter_create_pydantic_model_without_properties():
    """Test creating Pydantic model without properties"""
    schema = {
        "type": "object",
        "additionalProperties": True
    }  # No properties defined
    
    model_class = SchemaValidationAdapter.create_pydantic_model_from_schema(schema, "EmptyModel")
    assert model_class.__name__ == "EmptyModel"
    
    # Test creating an instance
    instance = model_class()
    assert instance is not None


def test_schema_validation_adapter_create_structured_error_response():
    """Test creating structured error response"""
    from src.core.models.error_models import ErrorCodes
    
    error_response = SchemaValidationAdapter.create_structured_error_response(
        error_code=ErrorCodes.VALIDATION_ERROR,
        message="Test validation error",
        details="Additional details",
        request_id="req-123",
        status_code=422
    )
    
    assert error_response.error.error_code == ErrorCodes.VALIDATION_ERROR
    assert "Test validation error" in error_response.error.message
    assert error_response.error.details == "Additional details"
    assert error_response.error.request_id == "req-123"
    assert error_response.status_code == 422
    assert len(error_response.details) > 0


def test_schema_validation_adapter_create_structured_error_response_defaults():
    """Test creating structured error response with default values"""
    error_response = SchemaValidationAdapter.create_structured_error_response(
        error_code="TEST_ERROR",
        message="Test error"  # Using only required params
    )
    
    assert error_response.error.error_code == "TEST_ERROR"
    assert error_response.error.message == "Test error"
    assert error_response.error.details is None
    assert error_response.error.request_id is None
    assert error_response.status_code == 400  # Default status code