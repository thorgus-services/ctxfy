import threading
from typing import Any, Dict, List, Optional

from ...core.models.prompt_models import PromptResponse, PromptTemplate
from ...core.ports.prompt_ports import PromptCommandPort, PromptQueryPort


class PromptRegistry:
    """Maintains in-memory registry of available prompt templates with thread-safe access"""
    
    def __init__(self) -> None:
        self._templates: Dict[str, PromptTemplate] = {}
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        
    def register_template(self, template: PromptTemplate) -> bool:
        """Register a new prompt template"""
        with self._lock:
            self._templates[template.template_id] = template
            return True
    
    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """Get a specific prompt template by ID"""
        with self._lock:
            return self._templates.get(template_id)
    
    def get_all_templates(self) -> List[PromptTemplate]:
        """Get all registered prompt templates"""
        with self._lock:
            return list(self._templates.values())
    
    def update_template(self, template_id: str, template: PromptTemplate) -> bool:
        """Update an existing template"""
        with self._lock:
            if template_id in self._templates:
                self._templates[template_id] = template
                return True
            return False
    
    def remove_template(self, template_id: str) -> bool:
        """Remove a template"""
        with self._lock:
            if template_id in self._templates:
                del self._templates[template_id]
                return True
            return False


class PromptRegistryAdapter(PromptCommandPort, PromptQueryPort):
    """Implementation of prompt ports using the in-memory registry"""
    
    def __init__(self) -> None:
        self._registry = PromptRegistry()
    
    async def register_prompt_template(self, template_id: str, template: PromptTemplate) -> bool:
        """Register a new prompt template"""
        return self._registry.register_template(template)
    
    async def execute_prompt(self, prompt_id: str, variables: Dict[str, Any]) -> PromptResponse:
        """Execute a registered prompt with given variables - simplified implementation"""
        # This method would typically coordinate with other adapters
        # For now, this is a placeholder that would be implemented fully
        # with the integration of template engine and llm sampling
        raise NotImplementedError("Execution logic requires integration with template engine and LLM sampler")
    
    async def get_registered_prompts(self) -> List[PromptTemplate]:
        """Get all registered prompt templates"""
        return self._registry.get_all_templates()
    
    async def get_prompt_template(self, prompt_id: str) -> Optional[PromptTemplate]:
        """Get a specific prompt template by ID"""
        return self._registry.get_template(prompt_id)