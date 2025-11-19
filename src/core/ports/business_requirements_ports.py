from typing import Protocol, Tuple

from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
    TechnicalSpecification,
    TranslationResult,
    TranslationStatus,
)
from src.core.models.validation_models import ValidationResult


class BusinessRequirementsCommandPort(Protocol):
    """Primary port for business requirements operations - driven by external actor"""
    
    async def translate_business_requirements(self, config: BusinessRequirementConfig) -> TranslationResult:
        """Translate business requirements into technical specifications"""
        ...

    async def generate_technical_specification(self, requirements: BusinessRequirements) -> TechnicalSpecification:
        """Generate technical specification from parsed business requirements"""
        ...

    async def store_technical_specification(self, specification: TechnicalSpecification, output_path: str) -> bool:
        """Store generated technical specification to filesystem"""
        ...


class BusinessRequirementsQueryPort(Protocol):
    """Primary port for business requirements information queries - driven by external actor"""
    
    async def get_translation_status(self, translation_id: str) -> TranslationStatus:
        """Get the current status of a translation operation"""
        ...

    async def validate_requirements(self, requirements: BusinessRequirements) -> ValidationResult:
        """Validate business requirements against defined rules"""
        ...

    async def list_translations(self, limit: int = 10) -> Tuple[str, ...]:
        """List recent translation operations"""
        ...