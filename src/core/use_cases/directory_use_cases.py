import os
import re

from src.core.models.directory_models import (
    DirectoryConfig,
    DirectoryOperation,
    ValidationResult,
)
from src.core.models.filesystem_models import DirectoryTraversalCheck


def validate_directory_config(config: DirectoryConfig) -> ValidationResult:
    """Pure function to validate directory configuration"""
    errors = []

    if not config.base_path.strip():
        errors.append("Base path cannot be empty")

    if not config.subdirectories:
        errors.append("Must specify at least one subdirectory")

    if not config.readme_content.strip():
        errors.append("README content should not be empty")

    # Validate subdirectory names for security
    invalid_chars = ["../", "..\\", "<", ">", "|", "*", "?"]
    for subdir in config.subdirectories:
        for char in invalid_chars:
            if char in subdir:
                errors.append(f"Invalid character '{char}' in subdirectory name: {subdir}")

    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )


def generate_default_readme(config: DirectoryConfig) -> str:
    """Pure function to generate default README content"""
    timestamp = str(config.__class__.__name__)
    return f"""# ctxfy/ Directory
This directory and its subdirectories are managed by the ctxfy MCP server.

## Structure
- `{config.base_path}/` - Root directory managed by server
- `{"/".join([config.base_path] + list(config.subdirectories[:1]))}/` - Specifications directory

## Responsibilities
- **Server**: Creates and manages this directory structure
- **Client**: Provides the filesystem context where these directories will be created
- **User**: May store files in these directories but should be aware that server operations may modify them

## Security Notice
This directory is created and managed by the ctxfy MCP server. All file operations in this directory are handled through the Model Context Protocol (MCP) to maintain security boundaries between server and client.

Directory created on: {timestamp}
"""


def build_directory_operation(path: str, operation_type: str) -> DirectoryOperation:
    """Pure function for creating directory operations"""
    return DirectoryOperation(
        operation_type=operation_type,
        target_path=path
    )


def validate_path_security(path: str) -> ValidationResult:
    """Pure function for path security validation"""
    errors = []

    # Check for directory traversal attempts
    if "../" in path or "..\\" in path:
        errors.append("Directory traversal detected in path")

    # Additional security checks can be added here

    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )


def check_directory_traversal(path: str) -> DirectoryTraversalCheck:
    """Pure function to check for directory traversal attempts"""
    violations = []
    
    # Check for directory traversal patterns
    traversal_patterns = [
        r'\.\./',  # Unix-style parent directory
        r'\.\.\\', # Windows-style parent directory
        r'\.\.\\\\', # Multiple backslashes
        r'\.\./+', # Multiple forward slashes
    ]
    
    for pattern in traversal_patterns:
        if re.search(pattern, path):
            violations.append(f"Directory traversal pattern detected: {pattern}")
    
    # Check if the normalized path goes outside of expected boundaries
    normalized = os.path.normpath(path)
    parts = normalized.split(os.sep)
    if '..' in parts or parts[0] == '..':
        violations.append("Normalized path contains parent directory references")
    
    is_safe = len(violations) == 0
    
    return DirectoryTraversalCheck(
        is_safe=is_safe,
        safe_path=normalized if is_safe else path,
        original_path=path,
        violations=tuple(violations)
    )