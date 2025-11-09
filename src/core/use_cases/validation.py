"""Validation utilities for context stack generation."""

from typing import List

from ..exceptions import ValidationError
from ..models.context_models import ContextGenerationRequest


def validate_feature_description(description: str) -> List[str]:
    """Validate a feature description and return a list of errors."""
    errors = []
    
    if not description or len(description.strip()) == 0:
        errors.append("Feature description cannot be empty")
    elif len(description.strip()) < 5:
        errors.append("Feature description should be at least 5 characters long")
    
    return errors


def validate_target_technologies(technologies: List[str]) -> List[str]:
    """Validate target technologies and return a list of errors."""
    errors = []
    
    # In a real implementation, you might want to check against a list
    # of supported technologies
    for tech in technologies:
        if not tech or len(tech.strip()) == 0:
            errors.append("Technology names cannot be empty")
    
    return errors


def validate_context_generation_request(request: ContextGenerationRequest) -> List[str]:
    """Validate a context generation request and return a list of validation errors."""
    errors = []
    
    # Validate feature description
    errors.extend(validate_feature_description(request.feature_description))
    
    # Validate target technologies
    errors.extend(validate_target_technologies(request.target_technologies))
    
    # Additional validation can be added here
    
    return errors


def validate_and_raise(request: ContextGenerationRequest) -> None:
    """Validate a context generation request and raise an exception if invalid."""
    errors = validate_context_generation_request(request)
    
    if errors:
        raise ValidationError(f"Validation failed: {'; '.join(errors)}")