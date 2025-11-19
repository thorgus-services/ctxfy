from datetime import datetime
from typing import Tuple

from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
    TechnicalSpecification,
    TranslationResult,
)
from src.core.models.validation_models import ValidationError, ValidationResult
from src.core.use_cases.directory_use_cases import validate_path_security


def parse_business_requirements(config: BusinessRequirementConfig) -> BusinessRequirements:
    """Pure function to parse and validate business requirements from configuration"""
    # Sanitize and validate the requirements text
    content = config.requirements_text.strip()
    if not content:
        raise ValueError("Business requirements content cannot be empty")
    
    # Prepare context and metadata
    context = {
        "output_directory": config.output_directory,
        "security_context": config.security_context,
        "parsed_at": datetime.now().isoformat()
    }
    
    metadata = {
        "validation_rules_applied": config.validation_rules,
        "character_count": len(content),
        "word_count": len(content.split()),
        "parsed_from_config": True
    }
    
    return BusinessRequirements(
        content=content,
        context=context,
        metadata=metadata
    )


def validate_business_requirements(requirements: BusinessRequirements) -> ValidationResult:
    """Pure function to validate business requirements against defined rules"""
    errors = []

    # Check content length
    if len(requirements.content.strip()) < 10:
        errors.append(ValidationError(
            field="content",
            message="Business requirements content too short, minimum 10 characters",
            code="CONTENT_TOO_SHORT"
        ))

    # Check for basic structure (must contain at least a few words)
    words = requirements.content.split()
    if len(words) < 3:
        errors.append(ValidationError(
            field="content",
            message="Business requirements must contain at least 3 words",
            code="CONTENT_TOO_SIMPLE"
        ))

    # Validate context
    if not isinstance(requirements.context, dict):
        errors.append(ValidationError(
            field="context",
            message="Context must be a dictionary",
            code="INVALID_CONTEXT_TYPE"
        ))

    # Validate metadata
    if not isinstance(requirements.metadata, dict):
        errors.append(ValidationError(
            field="metadata",
            message="Metadata must be a dictionary",
            code="INVALID_METADATA_TYPE"
        ))

    # Check for potentially sensitive information
    sensitive_indicators = ["password", "secret", "key", "token", "credential"]
    content_lower = requirements.content.lower()
    for indicator in sensitive_indicators:
        if indicator in content_lower:
            errors.append(ValidationError(
                field="content",
                message=f"Potentially sensitive information detected: {indicator}",
                code="SENSITIVE_INFO_DETECTED"
            ))

    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )


def translate_to_technical_specification(requirements: BusinessRequirements) -> TechnicalSpecification:
    """Pure function to transform business requirements into technical specifications"""
    # This is a simplified example - in a real system this would call LLM APIs
    # For now, we simulate the transformation
    technical_content = f"""# Technical Specification

## Based on Business Requirements

{requirements.content}

## Implementation Approach

This specification outlines the technical implementation needed to fulfill the above business requirements.

## Technical Components

1. **System Architecture**: [To be defined based on requirements]
2. **Data Models**: [To be defined based on requirements]
3. **API Endpoints**: [To be defined based on requirements]
4. **Security Considerations**: [To be defined based on requirements]
5. **Testing Strategy**: [To be defined based on requirements]

## Dependencies

- [List of technical dependencies]

## Implementation Timeline

- Phase 1: [Initial setup]
- Phase 2: [Core features]
- Phase 3: [Advanced features]
- Phase 4: [Testing and deployment]

## Success Metrics

- [Define success metrics for the technical implementation]
"""
    
    return TechnicalSpecification(
        content=technical_content,
        format="SPEC",
        source_requirements_id=requirements.id,
        generated_at=datetime.now()
    )


def validate_translation_config(config: BusinessRequirementConfig) -> ValidationResult:
    """Pure function to validate the translation configuration"""
    errors = []

    # Validate requirements text
    if not config.requirements_text or not config.requirements_text.strip():
        errors.append(ValidationError(
            field="requirements_text",
            message="Requirements text cannot be empty",
            code="EMPTY_REQUIREMENTS"
        ))

    # Validate output directory using existing security validation
    path_validation = validate_path_security(config.output_directory)
    if not path_validation.is_valid:
        # Convert string errors to ValidationError objects
        for error_str in path_validation.errors:
            errors.append(ValidationError(
                field="output_directory",
                message=error_str,
                code="PATH_SECURITY_ERROR"
            ))

    # Validate security context
    if not isinstance(config.security_context, dict):
        errors.append(ValidationError(
            field="security_context",
            message="Security context must be a dictionary",
            code="INVALID_SECURITY_CONTEXT"
        ))

    # Validate validation rules
    if not isinstance(config.validation_rules, tuple):
        errors.append(ValidationError(
            field="validation_rules",
            message="Validation rules must be a tuple",
            code="INVALID_VALIDATION_RULES_TYPE"
        ))

    for rule in config.validation_rules:
        if not isinstance(rule, str):
            errors.append(ValidationError(
                field="validation_rules",
                message=f"Validation rule '{rule}' must be a string",
                code="INVALID_RULE_TYPE"
            ))

    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )


def create_translation_result(
    requirements: BusinessRequirements,
    specification: TechnicalSpecification,
    errors: Tuple[str, ...] = ()
) -> TranslationResult:
    """Pure function to create a translation result with given parameters"""
    success = len(errors) == 0 and specification is not None
    
    return TranslationResult(
        success=success,
        specification=specification if success else None,
        errors=errors,
        warnings=()  # Could add warnings based on business logic if needed
    )