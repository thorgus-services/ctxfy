from typing import Any, Dict, List, Optional, Protocol

from ...core.models.prompt_models import PromptResponse, PromptTemplate


class PromptCommandPort(Protocol):
    """Primary port for registering and executing prompts - driving port"""
    
    async def register_prompt_template(self, template_id: str, template: PromptTemplate) -> bool:
        """Register a new prompt template"""
        ...
    
    async def execute_prompt(self, prompt_id: str, variables: Dict[str, Any]) -> PromptResponse:
        """Execute a registered prompt with given variables"""
        ...


class PromptQueryPort(Protocol):
    """Primary port for retrieving prompt information - driving port"""
    
    async def get_registered_prompts(self) -> List[PromptTemplate]:
        """Get all registered prompt templates"""
        ...
    
    async def get_prompt_template(self, prompt_id: str) -> Optional[PromptTemplate]:
        """Get a specific prompt template by ID"""
        ...