"""Immutable value objects for context stack generation."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from decimal import Decimal

from ..exceptions import ValidationError


@dataclass(frozen=True)
class ContextLayer:
    """Represents a single layer in the context stack."""
    name: str
    description: str
    specifications: Dict[str, str] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate invariants for ContextLayer."""
        if not self.name:
            raise ValidationError("ContextLayer name cannot be empty", "name")
        if not self.description:
            raise ValidationError("ContextLayer description cannot be empty", "description")
    
    def add_dependency(self, dependency: str) -> 'ContextLayer':
        """Return a new ContextLayer with an added dependency."""
        return ContextLayer(
            name=self.name,
            description=self.description,
            specifications=self.specifications,
            dependencies=[*self.dependencies, dependency]
        )
    
    def with_specification(self, key: str, value: str) -> 'ContextLayer':
        """Return a new ContextLayer with an added specification."""
        return ContextLayer(
            name=self.name,
            description=self.description,
            specifications={**self.specifications, key: value},
            dependencies=self.dependencies
        )


@dataclass(frozen=True)
class ContextStackMetadata:
    """Metadata for the entire context stack."""
    version: str
    creation_date: datetime
    author: str
    domain: str
    task_type: str
    
    def __post_init__(self):
        """Validate invariants for ContextStackMetadata."""
        if not self.version:
            raise ValidationError("Metadata version cannot be empty", "version")
        if not self.author:
            raise ValidationError("Metadata author cannot be empty", "author")
        if not self.domain:
            raise ValidationError("Metadata domain cannot be empty", "domain")
        if not self.task_type:
            raise ValidationError("Metadata task_type cannot be empty", "task_type")


@dataclass(frozen=True)
class ContextStack:
    """Represents the complete context stack with all layers."""
    system_layer: ContextLayer
    domain_layer: ContextLayer
    task_layer: ContextLayer
    metadata: ContextStackMetadata
    additional_layers: List[ContextLayer] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate invariants for ContextStack."""
        if self.system_layer.name != "system":
            raise ValidationError("System layer name must be 'system'", "system_layer.name")
        if self.domain_layer.name != "domain":
            raise ValidationError("Domain layer name must be 'domain'", "domain_layer.name")
        if self.task_layer.name != "task":
            raise ValidationError("Task layer name must be 'task'", "task_layer.name")
    
    def add_additional_layer(self, layer: ContextLayer) -> 'ContextStack':
        """Return a new ContextStack with an added layer."""
        return ContextStack(
            system_layer=self.system_layer,
            domain_layer=self.domain_layer,
            task_layer=self.task_layer,
            metadata=self.metadata,
            additional_layers=[*self.additional_layers, layer]
        )
    
    def get_all_layers(self) -> List[ContextLayer]:
        """Return all layers in the stack."""
        return [
            self.system_layer,
            self.domain_layer,
            self.task_layer,
            *self.additional_layers
        ]


@dataclass(frozen=True)
class ContextGenerationRequest:
    """Request object for context stack generation."""
    feature_description: str
    target_technologies: List[str] = field(default_factory=list)
    custom_rules: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate invariants for ContextGenerationRequest."""
        if not self.feature_description:
            raise ValidationError("Feature description cannot be empty", "feature_description")


@dataclass(frozen=True)
class ContextGenerationResponse:
    """Response object for context stack generation."""
    success: bool
    context_stack: Optional[ContextStack]
    error_message: Optional[str]
    processing_time: Decimal  # in seconds
    
    def __post_init__(self):
        """Validate invariants for ContextGenerationResponse."""
        if self.success and not self.context_stack:
            raise ValidationError("Success response must include context stack", "context_stack")
        if not self.success and self.context_stack:
            raise ValidationError("Error response cannot include context stack", "context_stack")
        if not self.success and not self.error_message:
            raise ValidationError("Error response must include error message", "error_message")