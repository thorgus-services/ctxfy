import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class BusinessRequirementConfig:
    """Immutable value object for business requirements configuration following our core architecture principles"""
    requirements_text: str
    output_directory: str = "ctxfy/specifications"
    security_context: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Tuple[str, ...] = field(default_factory=lambda: ("no_traversal", "safe_chars", "requirements_format"))

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.requirements_text or not isinstance(self.requirements_text, str):
            raise ValueError("Requirements text must be a valid string")
        if not self.output_directory or not isinstance(self.output_directory, str):
            raise ValueError("Output directory must be a valid string")
        if not isinstance(self.security_context, dict):
            raise ValueError("Security context must be a dictionary")
        if not isinstance(self.validation_rules, tuple):
            raise ValueError("Validation rules must be a tuple")


@dataclass(frozen=True)
class BusinessRequirements:
    """Immutable value object for parsed business requirements following our core architecture principles"""
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Content must be a valid string")
        if not self.id or not isinstance(self.id, str):
            raise ValueError("ID must be a valid string")
        if not isinstance(self.context, dict):
            raise ValueError("Context must be a dictionary")
        if not isinstance(self.metadata, dict):
            raise ValueError("Metadata must be a dictionary")


@dataclass(frozen=True)
class TechnicalSpecification:
    """Immutable value object for generated technical specifications"""
    content: str
    format: str
    spec_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: datetime = field(default_factory=datetime.now)
    source_requirements_id: str = ""

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Content must be a valid string")
        if not self.format or not isinstance(self.format, str):
            raise ValueError("Format must be a valid string")
        if not self.spec_id or not isinstance(self.spec_id, str):
            raise ValueError("Spec ID must be a valid string")
        if not isinstance(self.generated_at, datetime):
            raise ValueError("Generated at must be a datetime object")
        if not isinstance(self.source_requirements_id, str):
            raise ValueError("Source requirements ID must be a string")


@dataclass(frozen=True)
class TranslationResult:
    """Immutable value object for translation results"""
    success: bool
    specification: Optional[TechnicalSpecification] = None
    errors: Tuple[str, ...] = field(default_factory=tuple)
    warnings: Tuple[str, ...] = field(default_factory=tuple)
    execution_time_ms: float = 0.0

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not isinstance(self.success, bool):
            raise ValueError("Success must be a boolean")
        if self.specification is not None and not isinstance(self.specification, TechnicalSpecification):
            raise ValueError("Specification must be a TechnicalSpecification object or None")
        if not isinstance(self.errors, tuple):
            raise ValueError("Errors must be a tuple")
        if not isinstance(self.warnings, tuple):
            raise ValueError("Warnings must be a tuple")
        if not isinstance(self.execution_time_ms, (int, float)) or self.execution_time_ms < 0:
            raise ValueError("Execution time must be a non-negative number")


@dataclass(frozen=True)
class TranslationStatus:
    """Immutable value object for translation status"""
    translation_id: str
    status: str  # "pending", "in_progress", "completed", "failed"
    progress: float = 0.0  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.translation_id or not isinstance(self.translation_id, str):
            raise ValueError("Translation ID must be a valid string")
        valid_statuses = ("pending", "in_progress", "completed", "failed")
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        if not 0.0 <= self.progress <= 1.0:
            raise ValueError("Progress must be between 0.0 and 1.0")
        if not isinstance(self.created_at, datetime):
            raise ValueError("Created at must be a datetime object")
        if self.completed_at is not None and not isinstance(self.completed_at, datetime):
            raise ValueError("Completed at must be a datetime object or None")