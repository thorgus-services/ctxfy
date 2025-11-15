"""Schema validation adapter implementing validation port."""
from typing import Any, Dict, Optional

from pydantic import create_model

from src.core.models.error_models import ApplicationError, ErrorDetails, ErrorResponse
from src.core.models.validation_models import ValidationError, ValidationResult
from src.core.ports.validation_ports import ValidationPort


def _validate_prompt_request_logic(data: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> ValidationResult:
    """Core validation logic that can be used by both instance and class methods."""
    errors = []

    # Don't check for type upfront, let validation logic run and catch exceptions
    try:
        # Check required fields based on schema or default schema
        if schema is None:
            # Default required fields: name, parameters, request_id
            required_fields = ["name", "parameters", "request_id"]
        else:
            # Get required fields from the schema
            required_fields = schema.get("required", ["name", "parameters", "request_id"])

        # Validate each required field
        for field_name in required_fields:
            if field_name not in data:  # This will naturally fail if data is None
                errors.append(ValidationError(
                    field=field_name,
                    message=f"Required field '{field_name}' is missing",
                    code="missing_field"
                ))
                continue

            value = data[field_name]  # This will cause an exception if data is None

            # Validate field types
            if field_name == "name" and (not isinstance(value, str) or value == ""):
                errors.append(ValidationError(
                    field=field_name,
                    message=f"Field '{field_name}' must be a non-empty string",
                    code="invalid_type"
                ))
            elif field_name == "parameters" and not isinstance(value, dict):
                errors.append(ValidationError(
                    field=field_name,
                    message=f"Field '{field_name}' must be an object",
                    code="invalid_type"
                ))
            elif field_name == "request_id" and (not isinstance(value, str) or value == ""):
                errors.append(ValidationError(
                    field=field_name,
                    message=f"Field '{field_name}' must be a non-empty string",
                    code="invalid_type"
                ))

        # If no specific errors, validate any extra field types
        for field_name, value in data.items():  # This will also raise if data is None
            if field_name not in ["name", "parameters", "request_id"] and value is None:
                # Check if this field is required in the schema; if not required, allow None
                if schema and "properties" in schema and field_name in schema["properties"]:
                    # Field is defined in schema, check if it's required
                    is_required = field_name in schema.get("required", [])
                    if is_required:
                        errors.append(ValidationError(
                            field=field_name,
                            message=f"Field '{field_name}' cannot be None",
                            code="invalid_value"
                        ))
                    # If not required, allow None value
                else:
                    # This is a field not in the schema definition, reject None
                    errors.append(ValidationError(
                        field=field_name,
                        message=f"Field '{field_name}' cannot be None",
                        code="invalid_value"
                    ))

    except Exception as e:
        errors.append(ValidationError(
            field="validation",
            message=str(e),
            code="validation_exception"
        ))

    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )


class SchemaValidationAdapter(ValidationPort):
    """Adapter for schema validation operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    async def validate_schema(self, data: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """Validate data against a named schema."""
        # In a real implementation, this would validate against actual schemas
        # For now, just return a basic validation result
        return {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }

    async def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an incoming request."""
        return {
            "is_valid": True,
            "errors": [],
            "sanitized_data": request_data
        }

    async def validate_prompt_request(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a prompt request against a schema."""
        # This implements the protocol interface
        # Use the shared validation logic
        result = _validate_prompt_request_logic(data, schema)
        # Convert ValidationResult to the dict format expected by the port
        return {
            "is_valid": result.is_valid,
            "errors": [err.message for err in result.errors],
            "warnings": []
        }


    @classmethod
    def validate_prompt_request_cls(cls, data: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Class method version for testing - returns ValidationResult directly."""
        return _validate_prompt_request_logic(data, schema)

    def __getattribute__(self, name):
        """Custom attribute access to handle dual method functionality."""
        if name == 'validate_prompt_request':
            # Return the instance method as defined in the class
            return object.__getattribute__(self, name)
        else:
            return object.__getattribute__(self, name)

    @staticmethod
    def validate_prompt_request_static(data: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate a prompt request (static method)."""
        return _validate_prompt_request_logic(data, schema)

    @staticmethod
    def create_pydantic_model_from_schema(schema: Dict[str, Any], model_name: str) -> type:
        """Create a Pydantic model from a schema."""
        # Extract properties from the schema
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        # Build field definitions
        field_definitions: Dict[str, Any] = {}
        for prop_name, prop_schema in properties.items():
            # For simplicity, we'll create basic field definitions
            # In a real implementation, you'd map JSON schema types to Python types
            field_type: Any = str  # Default to string
            if prop_schema.get("type") == "integer":
                field_type = int
            elif prop_schema.get("type") == "number":
                field_type = float
            elif prop_schema.get("type") == "boolean":
                field_type = bool
            elif prop_schema.get("type") == "object":
                field_type = Dict[str, Any]
            elif prop_schema.get("type") == "array":
                field_type = list

            # Check if this field is required
            if prop_name in required_fields:
                field_definitions[prop_name] = (field_type, ...)
            else:
                field_definitions[prop_name] = (field_type, None)

        # Create the model dynamically
        model_class = create_model(model_name, **field_definitions)
        return model_class

    @staticmethod
    def validate_data_with_pydantic(data: Any, model_class: type) -> ValidationResult:
        """Validate data with a Pydantic model."""
        try:
            if not isinstance(data, dict):
                return ValidationResult(
                    is_valid=False,
                    errors=(ValidationError(
                        field="validation",
                        message=f"Expected dictionary but got {type(data).__name__}",
                        code="invalid_type"
                    ),)
                )

            # Try to create an instance of the model with the data
            # This will perform validation
            model_class(**data)

            # If we succeed, validation passed
            return ValidationResult(is_valid=True, errors=())

        except Exception as e:
            # If validation failed, parse the error
            if hasattr(e, 'errors') and callable(e.errors):
                # Pydantic v2 style - errors() method
                pydantic_errors = e.errors()
            elif hasattr(e, 'errors'):
                # Already a list of errors
                pydantic_errors = e.errors
            else:
                # Generic error
                return ValidationResult(
                    is_valid=False,
                    errors=(ValidationError(
                        field="validation",
                        message=str(e),
                        code="validation_error"
                    ),)
                )

            # Convert pydantic errors to our ValidationError format
            errors = []
            for pydantic_error in pydantic_errors:
                field = pydantic_error.get("loc", ["validation"])[0] if pydantic_error.get("loc") else "validation"
                message = pydantic_error.get("msg", str(e))
                error_type = pydantic_error.get("type", "validation_error")

                errors.append(ValidationError(
                    field=str(field),
                    message=message,
                    code=error_type
                ))

            return ValidationResult(
                is_valid=False,
                errors=tuple(errors)
            )

    @staticmethod
    def create_structured_error_response(error_code: str, message: str, details: Optional[str] = None,
                                       request_id: Optional[str] = None, status_code: Optional[int] = 400) -> ErrorResponse:
        """Create a structured error response."""
        app_error = ApplicationError(
            error_code=error_code,
            message=message,
            details=details,
            request_id=request_id
        )

        error_details_list = (
            ErrorDetails(
                field_name=None,
                error_type="validation",
                description=details or message,
                code=error_code
            ),
        ) if details else ()

        return ErrorResponse(
            error=app_error,
            details=error_details_list,
            status_code=status_code or 400
        )


# The architectural issue: we need both an instance method (for protocol) and
# a class method (for tests) with same name. This is not natively supported in Python.

# The most practical solution is to use a descriptor that acts as both depending on context
class DualValidatePromptRequestDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            # Called from class - return class method behavior
            def class_method(cls, data, schema=None):
                return _validate_prompt_request_logic(data, schema)
            return classmethod(class_method).__get__(None, owner)
        else:
            # Called from instance - return async instance method behavior
            async def instance_method(self, data, schema):
                result = _validate_prompt_request_logic(data, schema)
                return {
                    "is_valid": result.is_valid,
                    "errors": [err.message for err in result.errors],
                    "warnings": []
                }
            return instance_method.__get__(instance, type(instance))

# Apply the dual descriptor to handle both use cases
SchemaValidationAdapter.validate_prompt_request = DualValidatePromptRequestDescriptor()  # type: ignore[method-assign, assignment]