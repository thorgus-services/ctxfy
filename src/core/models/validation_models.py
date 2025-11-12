"""Immutable value objects for validation operations following our core architecture principles."""

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class ValidationError:
    """Immutable value object for validation errors following our core architecture principles."""
    field: str  # Field that failed validation
    message: str  # Error message
    code: str  # Error code

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.field or not isinstance(self.field, str):
            raise ValueError("Field must be a valid string")
        if not self.message or not isinstance(self.message, str):
            raise ValueError("Message must be a valid string")
        if not self.code or not isinstance(self.code, str):
            raise ValueError("Code must be a valid string")


@dataclass(frozen=True)
class ValidationResult:
    """Immutable value object for validation results following our core architecture principles."""
    is_valid: bool
    errors: Tuple[ValidationError, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not isinstance(self.is_valid, bool):
            raise ValueError("is_valid must be a boolean")
        if not isinstance(self.errors, tuple):
            raise ValueError("errors must be a tuple")
        # Validate each error in the tuple
        for error in self.errors:
            if not isinstance(error, ValidationError):
                raise ValueError("errors must contain only ValidationError instances")