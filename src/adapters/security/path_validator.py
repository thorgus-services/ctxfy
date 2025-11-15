import os
import re

from src.core.models.directory_models import SecurePath, ValidationResult
from src.core.models.filesystem_models import DirectoryTraversalCheck
from src.core.ports.filesystem_ports import ClientFilesystemPort


class PathValidator:
    """Security adapter for path validation and security checks"""
    
    def __init__(self) -> None:
        # Define patterns that are considered unsafe
        self.unsafe_patterns = [
            r'\.\./',      # Unix-style parent directory
            r'\.\.\\',     # Windows-style parent directory
            r'\.\.\\\\',   # Multiple backslashes
            r'\.\./+',     # Multiple forward slashes
            r'<.*>',       # HTML tags
            r'[|><*?"]',   # File system unsafe characters
        ]

    def validate_path(self, path: str) -> ValidationResult:
        """Validate if a path is safe to use in filesystem operations"""
        errors = []

        # Check for directory traversal patterns directly in the original path
        traversal_patterns = [r'\.\./', r'\.\.\\', r'\.\.\\\\', r'\.\./+']
        for pattern in traversal_patterns:
            if re.search(pattern, path):
                errors.append(f"Directory traversal pattern detected in path: {path}")
                break

        # Check for absolute paths that might be outside safe boundaries
        if os.path.isabs(path):
            errors.append("Absolute paths are not allowed")

        # Check if original path contains null bytes or other dangerous characters
        if '\0' in path:
            errors.append("Path contains null byte characters")

        # Check for other unsafe patterns
        for pattern in self.unsafe_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                if not errors:  # Only add if not already added a traversal error
                    errors.append(f"Unsafe pattern detected in path: {path}")
                break

        return ValidationResult(
            is_valid=(len(errors) == 0),
            errors=tuple(errors)
        )
    
    def sanitize_path(self, path: str) -> SecurePath:
        """Sanitize and validate a path, returning a SecurePath object"""
        # Validate the original path
        original_validation = self.validate_path(path)

        # Attempt to sanitize the path
        sanitized = self._sanitize_path_string(path)

        # The is_safe should be based on whether the original path was safe
        # If the original path had traversal, it should be considered unsafe
        is_safe = original_validation.is_valid

        # We still validate the sanitized version for additional errors
        final_validation = self.validate_path(sanitized)

        # Combine all errors from both validations
        all_errors = original_validation.errors + final_validation.errors

        return SecurePath(
            raw_path=path,
            sanitized_path=sanitized,
            is_safe=is_safe,
            validation_errors=all_errors
        )
    
    def _sanitize_path_string(self, path: str) -> str:
        """Basic path sanitization"""
        # Remove dangerous characters (but be careful not to over-sanitize)
        # Only remove null bytes and control characters that are clearly dangerous
        sanitized = path.replace('\0', '')  # Remove null bytes
        sanitized = sanitized.strip()  # Remove leading/trailing whitespace

        # Normalize the path to resolve .. and . components
        try:
            # Use os.path.normpath to normalize the path and resolve .. and .
            normalized = os.path.normpath(sanitized)
            return normalized
        except Exception:
            # If normalization fails, return the stripped version
            return sanitized
    
    def check_directory_traversal(self, path: str) -> DirectoryTraversalCheck:
        """Specifically check for directory traversal attempts"""
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
        try:
            normalized = os.path.normpath(path)
            parts = normalized.split(os.sep)
            if '..' in parts or parts[0] == '..':
                violations.append("Normalized path contains parent directory references")
        except Exception:
            violations.append("Error normalizing path for traversal check")
        
        is_safe = len(violations) == 0
        
        return DirectoryTraversalCheck(
            is_safe=is_safe,
            safe_path=normalized if is_safe else path,
            original_path=path,
            violations=tuple(violations)
        )


class SecurityAdapter(ClientFilesystemPort):
    """Adapter that wraps filesystem operations with security validation"""
    
    def __init__(self, filesystem_adapter: ClientFilesystemPort):
        self.filesystem_adapter = filesystem_adapter
        self.path_validator = PathValidator()
    
    async def create_directory(self, path: str) -> bool:
        """Create directory with security validation"""
        secure_path = self.path_validator.sanitize_path(path)

        if not secure_path.is_safe:
            raise ValueError(f"Unsafe path detected: {secure_path.validation_errors}")

        return await self.filesystem_adapter.create_directory(secure_path.sanitized_path)

    async def file_exists(self, path: str) -> bool:
        """Check if file exists with security validation"""
        secure_path = self.path_validator.sanitize_path(path)

        if not secure_path.is_safe:
            raise ValueError(f"Unsafe path detected: {secure_path.validation_errors}")

        return await self.filesystem_adapter.file_exists(secure_path.sanitized_path)

    async def write_file(self, path: str, content: str) -> bool:
        """Write file with security validation"""
        secure_path = self.path_validator.sanitize_path(path)

        if not secure_path.is_safe:
            raise ValueError(f"Unsafe path detected: {secure_path.validation_errors}")

        return await self.filesystem_adapter.write_file(secure_path.sanitized_path, content)

    async def directory_exists(self, path: str) -> bool:
        """Check if directory exists with security validation"""
        secure_path = self.path_validator.sanitize_path(path)

        if not secure_path.is_safe:
            raise ValueError(f"Unsafe path detected: {secure_path.validation_errors}")

        return await self.filesystem_adapter.directory_exists(secure_path.sanitized_path)