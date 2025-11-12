"""Core protocols for validation operations following our architectural patterns.

Primary ports (driving) are named with *CommandPort/*QueryPort convention.
Secondary ports (driven) are named with *GatewayPort/*RepositoryPort/*PublisherPort convention.
"""

from abc import abstractmethod
from typing import Any, Dict, Optional

from src.core.models.validation_models import ValidationResult


class ValidationPort:
    """Primary port for validation operations - driving port following naming convention."""

    @abstractmethod
    def validate_prompt_request(self, data: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate a prompt request against a schema."""
        pass