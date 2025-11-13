"""Schema validation adapter implementing validation using Pydantic and JSON Schema."""

from typing import Any, Dict, Optional, Type, Union

from pydantic import BaseModel, ValidationError, create_model

from src.core.models.error_models import (
    ApplicationError,
    ErrorCodes,
    ErrorDetails,
    ErrorResponse,
)
from src.core.models.validation_models import ValidationError as CoreValidationError
from src.core.models.validation_models import ValidationResult
from src.core.ports.validation_ports import ValidationPort


class SchemaValidationAdapter:
    """Schema validation adapter implementing validation for prompt requests using Pydantic."""

    @staticmethod
    def validate_prompt_request(data: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate a prompt request against a schema.

        Args:
            data: The prompt request data to validate
            schema: The schema to validate against (optional)

        Returns:
            ValidationResult with validation result and any errors
        """
        if schema is None:
            # Use a basic schema if none is provided
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "parameters": {"type": "object"},
                    "request_id": {"type": "string", "minLength": 1}
                },
                "required": ["name", "parameters"]
            }

        try:
            # Basic validation checks
            errors = []

            # Check required fields based on schema
            if "required" in schema:
                for required_field in schema["required"]:
                    if required_field not in data:
                        errors.append(
                            CoreValidationError(
                                field=required_field,
                                message=f"Field '{required_field}' is required",
                                code="missing_required_field"
                            )
                        )

            # Check types and constraints for known fields
            if "name" in data:
                if not isinstance(data["name"], str) or len(data["name"]) == 0:
                    errors.append(
                        CoreValidationError(
                            field="name",
                            message="Field 'name' must be a non-empty string",
                            code="invalid_type"
                        )
                    )

            if "parameters" in data:
                if not isinstance(data["parameters"], dict):
                    errors.append(
                        CoreValidationError(
                            field="parameters",
                            message="Field 'parameters' must be an object",
                            code="invalid_type"
                        )
                    )

            if "request_id" in data:
                if not isinstance(data["request_id"], str) or len(data["request_id"]) == 0:
                    errors.append(
                        CoreValidationError(
                            field="request_id",
                            message="Field 'request_id' must be a non-empty string",
                            code="invalid_type"
                        )
                    )

            # Additional parameter-specific validation based on schema properties
            if "properties" in schema and "parameters" in data:
                for param_name, param_schema in schema["properties"].items():
                    if param_name in data.get("parameters", {}):
                        param_value = data["parameters"][param_name]

                        # Check type
                        if "type" in param_schema:
                            expected_type = param_schema["type"]
                            if expected_type == "string" and not isinstance(param_value, str):
                                errors.append(
                                    CoreValidationError(
                                        field=f"parameters.{param_name}",
                                        message=f"Parameter '{param_name}' must be a string",
                                        code="invalid_type"
                                    )
                                )
                            elif expected_type == "number" and not isinstance(param_value, (int, float)):
                                errors.append(
                                    CoreValidationError(
                                        field=f"parameters.{param_name}",
                                        message=f"Parameter '{param_name}' must be a number",
                                        code="invalid_type"
                                    )
                                )
                            elif expected_type == "integer" and not isinstance(param_value, int):
                                errors.append(
                                    CoreValidationError(
                                        field=f"parameters.{param_name}",
                                        message=f"Parameter '{param_name}' must be an integer",
                                        code="invalid_type"
                                    )
                                )
                            elif expected_type == "boolean" and not isinstance(param_value, bool):
                                errors.append(
                                    CoreValidationError(
                                        field=f"parameters.{param_name}",
                                        message=f"Parameter '{param_name}' must be a boolean",
                                        code="invalid_type"
                                    )
                                )
                            elif expected_type == "object" and not isinstance(param_value, dict):
                                errors.append(
                                    CoreValidationError(
                                        field=f"parameters.{param_name}",
                                        message=f"Parameter '{param_name}' must be an object",
                                        code="invalid_type"
                                    )
                                )
                            elif expected_type == "array" and not isinstance(param_value, list):
                                errors.append(
                                    CoreValidationError(
                                        field=f"parameters.{param_name}",
                                        message=f"Parameter '{param_name}' must be an array",
                                        code="invalid_type"
                                    )
                                )

            # Return validation result
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=tuple(errors)
            )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=(
                    CoreValidationError(
                        field="unknown",
                        message=f"Validation error: {str(e)}",
                        code="validation_exception"
                    ),
                )
            )

    @staticmethod
    def create_pydantic_model_from_schema(schema: Dict[str, Any], model_name: str = "DynamicModel") -> Type[BaseModel]:
        """Create a Pydantic model from a JSON schema.

        Args:
            schema: The JSON schema to create a model from
            model_name: Name for the created model

        Returns:
            Pydantic model class
        """
        if "properties" not in schema:
            # Create a basic model with no fields if no properties are defined
            return create_model(model_name)

        # Build field definitions as tuples of (type, default_value)
        field_definitions: Dict[str, Any] = {}

        for field_name, field_schema in schema["properties"].items():
            field_type: Any = Any

            # Map JSON schema types to Python types
            json_type = field_schema.get("type")
            if json_type == "string":
                field_type = str
            elif json_type == "integer":
                field_type = int
            elif json_type == "number":
                field_type = Union[int, float]
            elif json_type == "boolean":
                field_type = bool
            elif json_type == "array":
                field_type = list
            elif json_type == "object":
                field_type = dict

            # Default all fields to None to make them optional
            default_value = ... if field_name in schema.get("required", []) else None
            field_definitions[field_name] = (field_type, default_value)

        # Create the Pydantic model with field definitions
        return create_model(model_name, **field_definitions)

    @staticmethod
    def validate_data_with_pydantic(data: Any, model: Type[BaseModel]) -> ValidationResult:
        """Validate data using a Pydantic model.

        Args:
            data: The data to validate
            model: The Pydantic model to validate against

        Returns:
            ValidationResult with validation result and any errors
        """
        try:
            # Type check if data is a dictionary
            if not isinstance(data, dict):
                return ValidationResult(
                    is_valid=False,
                    errors=(
                        CoreValidationError(
                            field="data",
                            message=f"Expected dictionary but got {type(data).__name__}",
                            code="invalid_type"
                        ),
                    )
                )
            
            # Attempt to create model instance which will trigger validation
            model(**data)

            # If successful, return valid result
            return ValidationResult(
                is_valid=True,
                errors=()
            )
        except ValidationError as e:
            # Convert Pydantic validation errors to our validation format
            errors = []
            for pydantic_error in e.errors():
                field = ".".join([str(loc) for loc in pydantic_error['loc']])
                errors.append(
                    CoreValidationError(
                        field=field,
                        message=pydantic_error['msg'],
                        code=pydantic_error['type']
                    )
                )

            return ValidationResult(
                is_valid=False,
                errors=tuple(errors)
            )
        except Exception as e:
            # Handle any other exceptions that might occur during validation
            return ValidationResult(
                is_valid=False,
                errors=(
                    CoreValidationError(
                        field="data",
                        message=f"Validation error: {str(e)}",
                        code="validation_exception"
                    ),
                )
            )

    @staticmethod
    def create_structured_error_response(error_code: str, message: str, details: Optional[str] = None, request_id: Optional[str] = None, status_code: int = 400) -> ErrorResponse:
        """Create a structured error response following our error handling principles."""
        error = ApplicationError(
            error_code=error_code,
            message=message,
            details=details,
            request_id=request_id
        )
        
        error_details = (ErrorDetails(description=message, code=error_code),) if message else ()
        
        return ErrorResponse(
            error=error,
            details=error_details,
            status_code=status_code
        )