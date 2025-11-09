"""In-memory adapter for context stack generation."""

from typing import Dict

from ..core.models.context_models import (
    ContextGenerationRequest,
    ContextGenerationResponse,
    ContextStack,
)
from ..core.ports.context_stack_ports import ContextStackGenerationCommandPort
from ..core.use_cases.context_stack_generation import generate_context_stack_functional


class InMemoryContextGenerationAdapter(ContextStackGenerationCommandPort):
    """In-memory implementation of the context stack generation command port."""
    
    def __init__(self) -> None:
        # In a real implementation, this might store generated context stacks
        self._generated_stacks: Dict[str, ContextStack] = {}
    
    def generate_context_stack(self, request: ContextGenerationRequest) -> ContextGenerationResponse:
        """Generate a context stack using the functional core."""
        # In this simple implementation, we directly call the functional core
        # In a more complex system, this adapter might handle additional
        # infrastructure concerns like caching, logging, or metrics
        result = generate_context_stack_functional(request)
        
        # Store the result if it was successful (for potential later retrieval)
        if result.success and result.context_stack:
            # Generate a simple ID based on the request and timestamp
            import time
            stack_id = f"stack_{int(time.time())}_{hash(request.feature_description) % 10000}"
            self._generated_stacks[stack_id] = result.context_stack
        
        return result