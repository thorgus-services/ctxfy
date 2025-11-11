"""Immutable value objects for MCP operations following our core architecture principles."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class PromptRequest:
    """Immutable value object for MCP prompt requests following our core architecture principles."""
    prompt_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Prompt name must be a valid string")
        if not isinstance(self.parameters, dict):
            raise ValueError("Parameters must be a dictionary")


@dataclass(frozen=True)
class PromptResponse:
    """Immutable value object for MCP prompt responses following our core architecture principles."""
    prompt_id: str
    content: str
    latency_ms: float
    llm_model: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.prompt_id or not isinstance(self.prompt_id, str):
            raise ValueError("Prompt ID must be a valid string")
        if not isinstance(self.content, str):
            raise ValueError("Content must be a string")
        if not isinstance(self.latency_ms, (int, float)) or self.latency_ms < 0:
            raise ValueError("Latency must be a non-negative number")
        if not self.llm_model or not isinstance(self.llm_model, str):
            raise ValueError("LLM model must be a valid string")


@dataclass(frozen=True)
class HealthStatus:
    """Immutable value object for health status following our core architecture principles."""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    timestamp: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0
    version: str = "1.0.0"

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if self.status not in ['healthy', 'degraded', 'unhealthy']:
            raise ValueError("Status must be 'healthy', 'degraded', or 'unhealthy'")
        if self.uptime_seconds < 0:
            raise ValueError("Uptime must be non-negative")