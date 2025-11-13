"""Immutable value objects for error handling following our core architecture principles."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ApplicationError:
    """Immutable value object for application errors following our core architecture principles."""
    error_code: str
    message: str
    details: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.error_code or not isinstance(self.error_code, str):
            raise ValueError("Error code must be a valid string")
        if not self.message or not isinstance(self.message, str):
            raise ValueError("Message must be a valid string")
        if self.details is not None and not isinstance(self.details, str):
            raise ValueError("Details must be a string if provided")
        if self.request_id is not None and not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a string if provided")


@dataclass(frozen=True)
class ErrorDetails:
    """Immutable value object for detailed error information following our core architecture principles."""
    field_name: Optional[str] = None
    error_type: Optional[str] = None
    description: str = ""
    code: str = ""

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if self.field_name is not None and not isinstance(self.field_name, str):
            raise ValueError("Field name must be a string if provided")
        if self.error_type is not None and not isinstance(self.error_type, str):
            raise ValueError("Error type must be a string if provided")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.code, str):
            raise ValueError("Code must be a string")


@dataclass(frozen=True)
class ErrorResponse:
    """Immutable value object for structured error responses following our core architecture principles."""
    error: ApplicationError
    details: tuple[ErrorDetails, ...] = field(default_factory=tuple)
    status_code: int = 400

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not isinstance(self.error, ApplicationError):
            raise ValueError("Error must be an ApplicationError instance")
        if not isinstance(self.details, tuple):
            raise ValueError("Details must be a tuple")
        if not isinstance(self.status_code, int) or self.status_code < 100 or self.status_code > 599:
            raise ValueError("Status code must be a valid HTTP status code")
        # Validate each detail in the tuple
        for detail in self.details:
            if not isinstance(detail, ErrorDetails):
                raise ValueError("details must contain only ErrorDetails instances")


class ErrorCodes:
    """Error codes for the application."""
    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_TEMPLATE = "INVALID_TEMPLATE"
    INVALID_REQUEST = "INVALID_REQUEST"
    INJECTION_ATTEMPT = "INJECTION_ATTEMPT"
    
    # Processing errors
    PROCESSING_ERROR = "PROCESSING_ERROR"
    LLM_SAMPLING_ERROR = "LLM_SAMPLING_ERROR"
    TEMPLATE_RENDERING_ERROR = "TEMPLATE_RENDERING_ERROR"
    
    # General errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"