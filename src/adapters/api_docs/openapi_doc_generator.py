"""OpenAPI documentation generator adapter."""
from typing import Any, Dict, Optional

from src.core.ports.doc_ports import DocumentationPort


class OpenAPIDocGenerator(DocumentationPort):
    """Adapter for OpenAPI documentation generation."""
    
    def __init__(self, mcp_server: Optional[Any] = None, title: str = "API Documentation", 
                 description: str = "API Documentation", version: str = "1.0.0"):
        self.mcp_server = mcp_server
        self.title = title
        self.description = description
        self.version = version
        self.spec: Dict[str, Any] = self._generate_spec()
    
    def _generate_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI specification."""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "description": self.description,
                "version": self.version
            },
            "paths": {}
        }
    
    async def generate_documentation(self) -> Dict[str, Any]:
        """Generate API documentation."""
        return self.spec
    
    async def get_openapi_spec(self) -> Dict[str, Any]:
        """Get the OpenAPI specification."""
        return self.spec