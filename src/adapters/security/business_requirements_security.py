
from src.core.models.validation_models import ValidationError, ValidationResult
from src.core.use_cases.directory_use_cases import (
    check_directory_traversal,
    validate_path_security,
)


def validate_business_requirements_security(requirements_text: str, output_path: str) -> ValidationResult:
    """
    Validate that business requirements and output path are secure
    """
    all_errors = []

    # Validate the requirements text doesn't contain malicious patterns
    malicious_indicators = [
        "../",  # Directory traversal
        "..\\",  # Windows directory traversal
        "eval(",  # Code execution
        "exec(",  # Code execution
        "__import__",  # Import execution
        "os.system",  # System command
        "subprocess.",  # Subprocess execution
    ]

    text_lower = requirements_text.lower()
    for indicator in malicious_indicators:
        if indicator in text_lower:
            all_errors.append(ValidationError(
                field="requirements_text",
                message=f"Potentially malicious content detected in requirements: {indicator}",
                code="MALICIOUS_CONTENT_DETECTED"
            ))

    # Validate the output path security
    path_validation = validate_path_security(output_path)
    if not path_validation.is_valid:
        # Convert string errors to ValidationError objects
        for error_str in path_validation.errors:
            all_errors.append(ValidationError(
                field="output_path",
                message=error_str,
                code="PATH_SECURITY_ERROR"
            ))

    # Additional path traversal check
    traversal_check = check_directory_traversal(output_path)
    if not traversal_check.is_safe:
        for violation in traversal_check.violations:
            all_errors.append(ValidationError(
                field="output_path",
                message=violation,
                code="PATH_TRAVERSAL_DETECTED"
            ))

    return ValidationResult(
        is_valid=(len(all_errors) == 0),
        errors=tuple(all_errors)
    )


def validate_specification_content(content: str) -> ValidationResult:
    """
    Validate the content of a technical specification for security issues
    """
    errors = []

    # Check for potentially dangerous content in the specification
    dangerous_patterns = [
        "eval(",
        "exec(",
        "__import__",
        "os.system",
        "subprocess.",
        "import os",
        "import subprocess",
        "rm -rf",
        "del ",
        "delete ",
    ]

    content_lower = content.lower()
    for pattern in dangerous_patterns:
        if pattern in content_lower:
            errors.append(ValidationError(
                field="specification_content",
                message=f"Dangerous pattern detected in specification content: {pattern}",
                code="DANGEROUS_PATTERN_DETECTED"
            ))

    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )


def sanitize_requirements_text(text: str) -> str:
    """
    Sanitize requirements text to remove potentially dangerous content
    """
    # Remove obvious directory traversal attempts
    sanitized = text.replace("../", "").replace("..\\", "")
    
    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()
    
    return sanitized


def build_secure_output_path(base_directory: str, filename: str) -> str:
    """
    Build a secure output path by validating both directory and filename
    """
    # Validate the base directory
    dir_validation = validate_path_security(base_directory)
    if not dir_validation.is_valid:
        raise ValueError(f"Unsafe base directory: {dir_validation.errors}")
    
    # Validate the filename
    filename_validation = validate_path_security(filename)
    if not filename_validation.is_valid:
        raise ValueError(f"Unsafe filename: {filename_validation.errors}")
    
    # Additional check for traversal in the combined path
    full_path = f"{base_directory}/{filename}"
    traversal_check = check_directory_traversal(full_path)
    if not traversal_check.is_safe:
        raise ValueError(f"Directory traversal detected in path: {traversal_check.violations}")
    
    return full_path