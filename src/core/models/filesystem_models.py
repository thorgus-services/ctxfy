from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class FilesystemOperation:
    """Immutable value object for filesystem operations"""
    operation_type: str  # "create_dir", "create_file", "check_exists", "delete"
    path: str
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        valid_types = ("create_dir", "create_file", "check_exists", "delete")
        if self.operation_type not in valid_types:
            raise ValueError(f"Operation type must be one of {valid_types}")
        if not self.path:
            raise ValueError("Path cannot be empty")


@dataclass(frozen=True)
class FileOperationResult:
    """Result of a filesystem operation"""
    success: bool
    path: str
    message: str = ""
    operation_details: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.path:
            raise ValueError("Path cannot be empty")
        if not isinstance(self.success, bool):
            raise ValueError("Success must be a boolean")


@dataclass(frozen=True)
class DirectoryTraversalCheck:
    """Result of a directory traversal security check"""
    is_safe: bool
    safe_path: str
    original_path: str
    violations: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.is_safe, bool):
            raise ValueError("Is_safe must be a boolean")
        if not self.original_path:
            raise ValueError("Original path cannot be empty")