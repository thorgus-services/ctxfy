
from src.adapters.validation import SchemaValidationAdapter


class TestSchemaValidationAdapter:
    """Tests for SchemaValidationAdapter class."""

    def test_validate_prompt_request_with_valid_data_and_none_schema(self):
        """Test validate_prompt_request with valid data using default schema."""
        valid_data = {
            "name": "test_prompt",
            "parameters": {"param1": "value1"},
            "request_id": "req-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(valid_data, None)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_prompt_request_with_invalid_name_type(self):
        """Test validate_prompt_request with invalid name type."""
        invalid_data = {
            "name": 123,  # Should be string
            "parameters": {"param1": "value1"},
            "request_id": "req-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
        assert result.is_valid is False
        assert any("name" in error.field and "string" in error.message for error in result.errors)

    def test_validate_prompt_request_with_invalid_parameters_type(self):
        """Test validate_prompt_request with invalid parameters type."""
        invalid_data = {
            "name": "test_prompt",
            "parameters": "not_a_dict",  # Should be dict
            "request_id": "req-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
        assert result.is_valid is False
        assert any("parameters" in error.field and "object" in error.message for error in result.errors)

    def test_validate_prompt_request_with_invalid_request_id_type(self):
        """Test validate_prompt_request with invalid request_id type."""
        invalid_data = {
            "name": "test_prompt",
            "parameters": {"param1": "value1"},
            "request_id": 456  # Should be string
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
        assert result.is_valid is False
        assert any("request_id" in error.field and "string" in error.message for error in result.errors)

    def test_validate_prompt_request_with_custom_schema_success(self):
        """Test validate_prompt_request with custom schema that passes validation."""
        custom_schema = {
            "required": ["name", "parameters", "request_id", "user_id"],
            "properties": {
                "name": {"type": "string"},
                "parameters": {"type": "object"},
                "request_id": {"type": "string"},
                "user_id": {"type": "string"}
            }
        }
        
        valid_data = {
            "name": "test_prompt",
            "parameters": {"param1": "value1"},
            "request_id": "req-123",
            "user_id": "user-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(valid_data, custom_schema)
        assert result.is_valid is True

    def test_validate_prompt_request_with_custom_schema_missing_field(self):
        """Test validate_prompt_request with custom schema missing required field."""
        custom_schema = {
            "required": ["name", "parameters", "request_id", "user_id"],
            "properties": {
                "name": {"type": "string"},
                "parameters": {"type": "object"},
                "request_id": {"type": "string"},
                "user_id": {"type": "string"}
            }
        }
        
        invalid_data = {
            "name": "test_prompt",
            "parameters": {"param1": "value1"},
            "request_id": "req-123"
            # Missing user_id
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(invalid_data, custom_schema)
        assert result.is_valid is False
        assert any("user_id" in error.field for error in result.errors)

    def test_validate_prompt_request_exception_handling(self):
        """Test validate_prompt_request with exception during validation."""
        # Pass None which should cause an exception during the processing
        result = SchemaValidationAdapter.validate_prompt_request(None)
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert result.errors[0].code == "validation_exception"

    def test_validate_prompt_request_empty_string_values(self):
        """Test validate_prompt_request with empty string values."""
        invalid_data = {
            "name": "",  # Empty string
            "parameters": {"param1": "value1"},
            "request_id": "req-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
        assert result.is_valid is False
        assert any("name" in error.field and "non-empty" in error.message for error in result.errors)

    def test_validate_prompt_request_missing_required_fields_with_default_schema(self):
        """Test validate_prompt_request missing required fields with default schema."""
        invalid_data = {
            # Missing required 'name' field
            "parameters": {"param1": "value1"},
            "request_id": "req-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
        assert result.is_valid is False
        assert any("name" in error.field for error in result.errors)

    def test_create_pydantic_model_from_schema_with_all_types(self):
        """Test create_pydantic_model_from_schema with different data types."""
        schema = {
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "score": {"type": "number"},
                "is_active": {"type": "boolean"},
                "items": {"type": "array"},
                "metadata": {"type": "object"}
            },
            "required": ["name"]
        }
        
        model_class = SchemaValidationAdapter.create_pydantic_model_from_schema(schema, "TestModel")
        assert model_class.__name__ == "TestModel"
        
        # Test creating an instance with some data
        instance = model_class(name="Alice", age=30, score=95.5, is_active=True)
        assert instance.name == "Alice"
        assert instance.age == 30
        assert instance.score == 95.5
        assert instance.is_active is True

    def test_create_pydantic_model_from_schema_without_properties(self):
        """Test create_pydantic_model_from_schema with schema that has no properties."""
        schema = {
            "type": "object"
            # No properties defined
        }
        
        model_class = SchemaValidationAdapter.create_pydantic_model_from_schema(schema, "EmptyModel")
        assert model_class.__name__ == "EmptyModel"
        
        # Should be able to create an instance
        instance = model_class()
        assert instance is not None

    def test_create_pydantic_model_from_schema_with_nested_properties(self):
        """Test create_pydantic_model_from_schema with complex schema."""
        schema = {
            "properties": {
                "user": {"type": "object"},
                "count": {"type": "integer"}
            },
            "required": ["user"]
        }
        
        model_class = SchemaValidationAdapter.create_pydantic_model_from_schema(schema, "ComplexModel")
        instance = model_class(user={"name": "Alice"}, count=5)
        assert instance.user == {"name": "Alice"}
        assert instance.count == 5

    def test_create_pydantic_model_from_schema_with_no_schema(self):
        """Test create_pydantic_model_from_schema when schema has no properties."""
        schema = {}  # No properties key
        
        model_class = SchemaValidationAdapter.create_pydantic_model_from_schema(schema, "NoPropsModel")
        instance = model_class()
        assert instance is not None

    def test_validate_data_with_pydantic_valid_data(self):
        """Test validate_data_with_pydantic with valid data."""
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            name: str
            age: int
        
        valid_data = {
            "name": "Alice",
            "age": 30
        }
        
        result = SchemaValidationAdapter.validate_data_with_pydantic(valid_data, TestModel)
        assert result.is_valid is True
        assert result.errors == ()

    def test_validate_data_with_pydantic_invalid_data(self):
        """Test validate_data_with_pydantic with invalid data."""
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            name: str
            age: int
        
        invalid_data = {
            "name": "Alice",
            "age": "not_a_number"  # Should be int
        }
        
        result = SchemaValidationAdapter.validate_data_with_pydantic(invalid_data, TestModel)
        assert result.is_valid is False
        assert len(result.errors) > 0
        # Check that errors contain pydantic validation info
        assert any("age" in error.field for error in result.errors)

    def test_validate_data_with_pydantic_with_exception(self):
        """Test validate_data_with_pydantic error handling."""
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            name: str
        
        # Test with non-dict input - should return invalid result, not raise exception
        result = SchemaValidationAdapter.validate_data_with_pydantic("not_a_dict", TestModel)
        # Should return invalid result rather than raising an exception
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert result.errors[0].message == "Expected dictionary but got str"

    def test_create_structured_error_response_basic(self):
        """Test creating a basic structured error response."""
        from src.core.models.error_models import ErrorCodes
        
        error_response = SchemaValidationAdapter.create_structured_error_response(
            error_code=ErrorCodes.VALIDATION_ERROR,
            message="Test validation error"
        )
        
        assert error_response.error.error_code == ErrorCodes.VALIDATION_ERROR
        assert "Test validation error" in error_response.error.message
        assert error_response.status_code == 400  # Default status code

    def test_create_structured_error_response_with_all_params(self):
        """Test creating a structured error response with all parameters."""
        from src.core.models.error_models import ErrorCodes
        
        error_response = SchemaValidationAdapter.create_structured_error_response(
            error_code=ErrorCodes.INTERNAL_ERROR,
            message="Internal server error",
            details="Additional error details",
            request_id="req-123",
            status_code=500
        )
        
        assert error_response.error.error_code == ErrorCodes.INTERNAL_ERROR
        assert error_response.error.message == "Internal server error"
        assert error_response.error.details == "Additional error details"
        assert error_response.error.request_id == "req-123"
        assert error_response.status_code == 500
        assert len(error_response.details) > 0