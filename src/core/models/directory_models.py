from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class DirectoryConfig:
    """Configuration for directory creation operations"""
    base_path: str
    subdirectories: Tuple[str, ...] = field(default_factory=lambda: ("specifications",))
    readme_content: str = ""
    validation_rules: Tuple[str, ...] = field(default_factory=lambda: ("no_traversal", "valid_chars"))

    def __post_init__(self) -> None:
        if not self.base_path.strip():
            raise ValueError("Base path cannot be empty")
        if not self.subdirectories:
            raise ValueError("Must specify at least one subdirectory")
        if not isinstance(self.subdirectories, tuple):
            # Ensure tuple type for immutability
            object.__setattr__(self, 'subdirectories', tuple(self.subdirectories))


@dataclass(frozen=True)
class SecurePath:
    """Secure path representation with validation"""
    raw_path: str
    sanitized_path: str
    is_safe: bool
    validation_errors: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.raw_path:
            raise ValueError("Raw path cannot be empty")
        if self.is_safe and not self.sanitized_path:
            raise ValueError("Sanitized path required when path is safe")


@dataclass(frozen=True)
class DirectoryOperation:
    """Representation of a directory operation"""
    operation_type: str  # "create", "validate", "check", "readme"
    target_path: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        valid_types = ("create", "validate", "check", "readme")
        if self.operation_type not in valid_types:
            raise ValueError(f"Operation type must be one of {valid_types}")


@dataclass(frozen=True)
class DirectoryStatus:
    """Status of a directory"""
    path: str
    exists: bool
    permissions: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.path:
            raise ValueError("Path cannot be empty")


@dataclass(frozen=True)
class ValidationResult:
    """Result of a validation operation"""
    is_valid: bool
    errors: Tuple[str, ...] = field(default_factory=tuple)
    warnings: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.is_valid and self.errors:
            raise ValueError("Valid result cannot have errors")