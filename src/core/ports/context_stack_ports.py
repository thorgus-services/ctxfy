"""Ports for context stack generation following hexagonal architecture."""

from typing import Protocol
from ..models.context_models import ContextGenerationRequest, ContextGenerationResponse


class ContextStackGenerationCommandPort(Protocol):
    """Primary port for generating context stacks."""
    
    def generate_context_stack(self, request: ContextGenerationRequest) -> ContextGenerationResponse:
        """Generate a context stack based on feature description."""
        ...


class ContextStackQueryPort(Protocol):
    """Primary port for querying context stack information."""
    
    def get_context_stack_info(self, stack_id: str) -> str:
        """Get information about a specific context stack."""
        ...