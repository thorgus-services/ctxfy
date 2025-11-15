"""Documentation port definitions."""
from abc import abstractmethod
from typing import Any, Dict, Protocol


class DocumentationPort(Protocol):
    """Primary port for documentation operations."""
    
    @abstractmethod
    async def generate_documentation(self) -> Dict[str, Any]:
        """Generate API documentation."""
        pass
    
    @abstractmethod
    async def get_openapi_spec(self) -> Dict[str, Any]:
        """Get the OpenAPI specification."""
        pass