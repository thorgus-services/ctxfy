"""Validation port definitions."""
from abc import abstractmethod
from typing import Any, Dict, Protocol


class ValidationPort(Protocol):
    """Primary port for validation operations."""
    
    @abstractmethod
    async def validate_schema(self, data: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """Validate data against a named schema."""
        pass
    
    @abstractmethod
    async def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an incoming request."""
        pass
        
    @abstractmethod
    async def validate_prompt_request(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a prompt request against a schema."""
        pass