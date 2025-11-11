import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .variable_models import Variable


@dataclass(frozen=True)
class PromptRequest:
    """Immutable value object for prompt execution requests following our core architecture principles"""
    template_id: str
    variables: dict[str, object]
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.template_id or not isinstance(self.template_id, str):
            raise ValueError("Template ID must be a valid string")
        if not isinstance(self.variables, dict):
            raise ValueError("Variables must be a dictionary")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")


@dataclass(frozen=True)
class PromptResponse:
    """Immutable value object for prompt execution responses following our core architecture principles"""
    request_id: str
    template_id: str
    result: str
    execution_time_ms: float

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")
        if not self.template_id or not isinstance(self.template_id, str):
            raise ValueError("Template ID must be a valid string")
        if not isinstance(self.result, str):
            raise ValueError("Result must be a string")
        if not isinstance(self.execution_time_ms, (int, float)) or self.execution_time_ms < 0:
            raise ValueError("Execution time must be a non-negative number")


@dataclass(frozen=True)
class PromptTemplate:
    """Immutable value object for MCP prompt templates following our core architecture principles"""
    template_id: str
    template_content: str
    variables: tuple["Variable", ...]  # Tuple of Variable objects
    description: str
    model_name: str

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.template_id or not isinstance(self.template_id, str):
            raise ValueError("Template ID must be a valid string")
        if not self.template_content or not isinstance(self.template_content, str):
            raise ValueError("Template content must be a valid string")
        if not isinstance(self.variables, tuple):
            raise ValueError("Variables must be a tuple")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Description must be a valid string")
        if not self.model_name or not isinstance(self.model_name, str):
            raise ValueError("Model name must be a valid string")