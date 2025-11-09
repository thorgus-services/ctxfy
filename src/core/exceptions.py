"""Domain-specific exceptions for context stack generation."""

from typing import Optional


class ContextGenerationError(Exception):
    """Base exception for context generation errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class InvalidFeatureDescriptionError(ContextGenerationError):
    """Raised when a feature description is invalid."""
    
    def __init__(self, message: str = "Invalid feature description provided"):
        super().__init__(message, "INVALID_FEATURE_DESC")


class ContextStackGenerationFailedError(ContextGenerationError):
    """Raised when context stack generation fails."""
    
    def __init__(self, message: str = "Context stack generation failed"):
        super().__init__(message, "STACK_GENERATION_FAILED")


class ValidationError(ContextGenerationError):
    """Raised when validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        error_msg = f"Validation error: {message}"
        if field:
            error_msg += f" (field: {field})"
        super().__init__(error_msg, "VALIDATION_ERROR")


class UnsupportedTechnologyError(ContextGenerationError):
    """Raised when an unsupported technology is specified."""
    
    def __init__(self, technology: str):
        self.technology = technology
        super().__init__(
            f"Unsupported technology: {technology}", 
            "UNSUPPORTED_TECH"
        )