"""MCP Server implementation for context stack generation."""

import asyncio
import json
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from src.settings import settings
from src.core.models.context_models import (
    ContextGenerationRequest, ContextGenerationResponse
)
from src.core.use_cases.context_stack_generation import (
    generate_context_stack_functional
)
from src.core.use_cases.validation import validate_context_generation_request
from src.core.ports.context_stack_ports import ContextStackGenerationCommandPort
from src.shell.orchestrators.context_generation_orchestrator import (
    ContextGenerationOrchestrator
)
from src.adapters.in_memory_context_adapter import InMemoryContextGenerationAdapter


class ToolParameter(BaseModel):
    """Represents a parameter for an MCP tool."""
    type: str
    description: str
    required: bool = True


class ToolSchema(BaseModel):
    """Schema for MCP tool definition."""
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPServer:
    """MCP Server that implements the tool discovery and execution interface."""
    
    def __init__(self):
        self.app = FastAPI(title=settings.app_name, version=settings.version)
        self.tools: Dict[str, ToolSchema] = {}
        
        # Initialize the orchestrator and adapter
        self.command_port: ContextStackGenerationCommandPort = InMemoryContextGenerationAdapter()
        self.orchestrator = ContextGenerationOrchestrator(self.command_port)
        
        self._register_routes()
        self._register_tools()
    
    def _register_routes(self):
        """Register the MCP routes."""
        @self.app.get("/tools/list")
        async def list_tools():
            """MCP endpoint for tool discovery."""
            return {
                "tools": [
                    {
                        "name": name,
                        "description": schema.description,
                        "inputSchema": schema.input_schema
                    }
                    for name, schema in self.tools.items()
                ]
            }
        
        @self.app.post("/tools/call")
        async def call_tool(request: Dict[str, Any]):
            """MCP endpoint for tool execution."""
            tool_name = request.get("name")
            tool_arguments = request.get("arguments", {})
            
            if not tool_name:
                raise HTTPException(status_code=400, detail="Tool name is required")
            
            if tool_name not in self.tools:
                raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
            
            # Execute the appropriate function based on the tool name
            if tool_name == "generate_context_stack":
                return await self._execute_generate_context_stack(tool_arguments)
            
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not implemented")
    
    def _register_tools(self):
        """Register available tools with their schemas."""
        self.tools["generate_context_stack"] = ToolSchema(
            name="generate_context_stack",
            description="Generate a context stack for Qwen Code based on a feature description",
            input_schema={
                "type": "object",
                "properties": {
                    "feature_description": {
                        "type": "string",
                        "description": "Description of the feature for which to generate a context stack"
                    },
                    "target_technologies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of target technologies for the context stack",
                        "default": []
                    },
                    "custom_rules": {
                        "type": "array", 
                        "items": {"type": "string"},
                        "description": "Custom rules to include in the context stack",
                        "default": []
                    }
                },
                "required": ["feature_description"]
            }
        )
    
    async def _execute_generate_context_stack(self, arguments: Dict[str, Any]):
        """Execute the generate_context_stack tool."""
        try:
            # Validate arguments
            feature_description = arguments.get("feature_description")
            if not feature_description:
                raise HTTPException(status_code=400, detail="feature_description is required")
            
            target_technologies = arguments.get("target_technologies", [])
            custom_rules = arguments.get("custom_rules", [])
            
            # Create the request object
            request = ContextGenerationRequest(
                feature_description=feature_description,
                target_technologies=target_technologies,
                custom_rules=custom_rules
            )
            
            # Use the orchestrator to handle the request
            result = self.orchestrator.generate_context_stack(request)
            
            # Convert the result to a JSON-serializable format
            if result.success and result.context_stack:
                response_data = {
                    "success": True,
                    "result": {
                        "context_stack": {
                            "system_layer": {
                                "name": result.context_stack.system_layer.name,
                                "description": result.context_stack.system_layer.description,
                                "specifications": result.context_stack.system_layer.specifications,
                                "dependencies": result.context_stack.system_layer.dependencies
                            },
                            "domain_layer": {
                                "name": result.context_stack.domain_layer.name,
                                "description": result.context_stack.domain_layer.description,
                                "specifications": result.context_stack.domain_layer.specifications,
                                "dependencies": result.context_stack.domain_layer.dependencies
                            },
                            "task_layer": {
                                "name": result.context_stack.task_layer.name,
                                "description": result.context_stack.task_layer.description,
                                "specifications": result.context_stack.task_layer.specifications,
                                "dependencies": result.context_stack.task_layer.dependencies
                            },
                            "metadata": {
                                "version": result.context_stack.metadata.version,
                                "creation_date": result.context_stack.metadata.creation_date.isoformat(),
                                "author": result.context_stack.metadata.author,
                                "domain": result.context_stack.metadata.domain,
                                "task_type": result.context_stack.metadata.task_type
                            },
                            "additional_layers": [
                                {
                                    "name": layer.name,
                                    "description": layer.description,
                                    "specifications": layer.specifications,
                                    "dependencies": layer.dependencies
                                }
                                for layer in result.context_stack.additional_layers
                            ]
                        },
                        "processing_time": float(result.processing_time)
                    }
                }
            else:
                response_data = {
                    "success": False,
                    "error": result.error_message
                }
            
            return response_data
            
        except HTTPException:
            raise
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run(self, host: str = None, port: int = None):
        """Run the MCP server."""
        host = host or settings.mcp_server_host
        port = port or settings.mcp_server_port
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            reload=settings.debug
        )


# If running as main, start the server
if __name__ == "__main__":
    server = MCPServer()
    server.run()