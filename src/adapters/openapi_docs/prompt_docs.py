from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

from ...core.models.prompt_models import PromptTemplate


class PromptExecutionRequest(BaseModel):
    """Pydantic model for prompt execution request in OpenAPI docs"""
    variables: Dict[str, Any]


class PromptExecutionResponse(BaseModel):
    """Pydantic model for prompt execution response in OpenAPI docs"""
    request_id: str
    result: str
    execution_time_ms: float


class OpenAPIDocsGenerator:
    """Generates OpenAPI documentation for registered prompts"""
    
    def __init__(self, app: FastAPI):
        self.app = app
    
    def register_prompt_endpoints(self, templates: List[PromptTemplate]) -> None:
        """Register OpenAPI endpoints for all registered prompts"""
        for template in templates:
            self._register_prompt_endpoint(template)
    
    def _register_prompt_endpoint(self, template: PromptTemplate) -> Dict[str, Any]:
        """Register a single prompt endpoint with OpenAPI documentation"""
        # This would normally register the actual endpoint
        # For now we'll just return the documentation structure
        endpoint_info = {
            "path": f"/prompts/{template.template_id}/execute",
            "summary": f"Execute {template.template_id} prompt",
            "description": template.description,
            "request_body": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/PromptExecutionRequest"
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Successfully executed prompt",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PromptExecutionResponse"
                            }
                        }
                    }
                }
            }
        }
        return endpoint_info
    
    def generate_prompt_schema(self, template: PromptTemplate) -> Dict[str, Any]:
        """Generate OpenAPI schema for a specific prompt template"""
        # Create a schema based on the template's variables
        properties = {}
        required = []
        
        for variable in template.variables:
            var_type = self._map_type_to_openapi(variable.type_hint)
            properties[variable.name] = {
                "type": var_type,
                "description": variable.description
            }
            
            if variable.required:
                required.append(variable.name)
        
        schema = {
            "type": "object",
            "properties": properties,
            "required": required if required else []
        }
        
        return schema
    
    def _map_type_to_openapi(self, type_hint: str) -> str:
        """Map Python type hints to OpenAPI types"""
        type_mapping = {
            "string": "string",
            "str": "string",
            "int": "integer",
            "float": "number",
            "bool": "boolean",
            "number": "number",
            "array": "array",
            "object": "object"
        }
        
        return type_mapping.get(type_hint.lower(), "string")
    
    def add_component_schemas(self) -> None:
        """Add reusable component schemas to the OpenAPI spec"""
        # Add the common schemas to the FastAPI app
        # FastAPI component schemas need to be handled differently
        # This is a workaround for mypy since FastAPI doesn't have this attribute defined
        # In real implementation, schemas could be registered in the FastAPI app
        pass