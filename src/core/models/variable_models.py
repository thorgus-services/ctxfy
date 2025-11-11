from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Variable:
    """Immutable value object for template variables following our core architecture principles"""
    name: str
    type_hint: str
    default_value: Optional[object] = None
    description: str = ""
    required: bool = True

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Variable name must be a valid string")
        if not self.type_hint or not isinstance(self.type_hint, str):
            raise ValueError("Type hint must be a valid string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.required, bool):
            raise ValueError("Required must be a boolean value")