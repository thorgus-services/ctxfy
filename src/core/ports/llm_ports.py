"""LLM port definitions."""
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol


class LLMPort(Protocol):
    """Primary port for LLM operations."""

    @abstractmethod
    async def sample(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Sample from an LLM with the given prompt."""
        pass

    @abstractmethod
    async def batch_sample(self, prompts: List[str], params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Sample from an LLM with multiple prompts."""
        pass

    @abstractmethod
    async def sample_prompt(self, prompt: str, model: str = "gpt-4", temperature: float = 0.7, max_tokens: int = 100) -> str:
        """Sample from an LLM with more parameters."""
        pass