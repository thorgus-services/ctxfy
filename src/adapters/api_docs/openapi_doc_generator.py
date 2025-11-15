"""OpenAPI documentation generator adapter."""
import inspect
from typing import Annotated, Any, Dict, Optional, get_args, get_origin

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
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "description": self.description,
                "version": self.version
            },
            "paths": {}
        }

        # If MCP server is available, add documentation for MCP endpoints
        if self.mcp_server and hasattr(self.mcp_server, '_handlers'):
            spec["paths"] = self._generate_mcp_paths()

        return spec

    def _generate_mcp_paths(self) -> Dict[str, Any]:
        """Generate OpenAPI paths for MCP endpoints."""
        paths: Dict[str, Any] = {}

        if self.mcp_server is None or not hasattr(self.mcp_server, '_handlers') or not self.mcp_server._handlers:
            return paths

        for prompt_name, handler_info in self.mcp_server._handlers.items():
            if 'fn' in handler_info:
                handler_fn = handler_info['fn']

                # Extract function signature for parameters
                # Check if handler_fn is a FunctionTool or similar object that is not callable
                if callable(handler_fn):
                    sig = inspect.signature(handler_fn)
                elif hasattr(handler_fn, 'fn') and callable(handler_fn.fn):
                    # Handle FunctionTool objects that have a callable 'fn' attribute
                    sig = inspect.signature(handler_fn.fn)
                else:
                    # If handler_fn is not callable and doesn't have a callable fn attribute, skip
                    continue
                properties = {}
                required_params = []

                for param_name, param in sig.parameters.items():
                    if param_name != 'ctx':  # Skip the context parameter which is internal to MCP
                        param_schema: Dict[str, Any] = {
                            "type": "string",  # Default type
                            "description": f"Parameter {param_name} for the {prompt_name} prompt"
                        }

                        # Check if parameter is Annotated and extract type info from Field
                        if hasattr(param.annotation, '__metadata__') and get_origin(param.annotation) is Annotated:
                            # Extract the actual type from Annotated
                            actual_type = get_args(param.annotation)[0]

                            # Extract Field metadata
                            field_info = None
                            for metadata_item in get_args(param.annotation)[1:]:
                                if hasattr(metadata_item, 'description') or hasattr(metadata_item, 'default'):
                                    field_info = metadata_item
                                    break

                            # Determine type from actual_type
                            if actual_type is str:
                                param_schema["type"] = "string"
                            elif actual_type is int:
                                param_schema["type"] = "integer"
                            elif actual_type is bool:
                                param_schema["type"] = "boolean"
                            elif actual_type is float:
                                param_schema["type"] = "number"
                            elif actual_type is list or get_origin(actual_type) is list:
                                param_schema["type"] = "array"
                                param_schema["items"] = {"type": "string"}
                            elif actual_type is dict or get_origin(actual_type) is dict:
                                param_schema["type"] = "object"
                            elif hasattr(actual_type, '__origin__') and actual_type.__origin__ is list:
                                param_schema["type"] = "array"
                                if hasattr(actual_type, '__args__') and actual_type.__args__:
                                    inner_type = actual_type.__args__[0]
                                    if inner_type is str:
                                        param_schema["items"] = {"type": "string"}
                                    elif inner_type is int:
                                        param_schema["items"] = {"type": "integer"}
                                    elif inner_type is bool:
                                        param_schema["items"] = {"type": "boolean"}
                                    elif inner_type is float:
                                        param_schema["items"] = {"type": "number"}
                                    else:
                                        param_schema["items"] = {"type": "string"}
                            elif hasattr(actual_type, '__origin__') and actual_type.__origin__ is dict:
                                param_schema["type"] = "object"

                            # Extract description from Field metadata
                            if field_info and hasattr(field_info, 'description'):
                                param_schema["description"] = field_info.description

                            # Handle default values
                            if param.default != inspect.Parameter.empty:
                                if hasattr(param.default, 'default'):
                                    # For Field instances
                                    default_val = param.default.default
                                    if default_val != ... and default_val is not None:
                                        param_schema["default"] = default_val
                                else:
                                    # For regular defaults
                                    param_schema["default"] = param.default
                                    param_schema["required"] = False
                            else:
                                param_schema["required"] = True

                        else:
                            # Handle non-Annotated parameters
                            # Determine parameter type from annotations
                            if param.annotation != inspect.Parameter.empty:
                                annotation = param.annotation
                                if annotation is str:
                                    param_schema["type"] = "string"
                                elif annotation is int:
                                    param_schema["type"] = "integer"
                                elif annotation is bool:
                                    param_schema["type"] = "boolean"
                                elif annotation is float:
                                    param_schema["type"] = "number"
                                elif annotation is list:
                                    param_schema["type"] = "array"
                                    param_schema["items"] = {"type": "string"}
                                elif annotation is dict:
                                    param_schema["type"] = "object"
                                elif get_origin(annotation) is list:
                                    param_schema["type"] = "array"
                                    args = get_args(annotation)
                                    if args:
                                        inner_type = args[0]
                                        if inner_type is str:
                                            param_schema["items"] = {"type": "string"}
                                        elif inner_type is int:
                                            param_schema["items"] = {"type": "integer"}
                                        elif inner_type is bool:
                                            param_schema["items"] = {"type": "boolean"}
                                        elif inner_type is float:
                                            param_schema["items"] = {"type": "number"}
                                        else:
                                            param_schema["items"] = {"type": "string"}

                            # Add default value if available
                            if param.default != inspect.Parameter.empty and "default" not in param_schema:
                                param_schema["default"] = param.default

                        # Mark as required if no default value
                        if param.default == inspect.Parameter.empty:
                            required_params.append(param_name)

                        properties[param_name] = param_schema

                # Create path for the prompt
                # Using a standard MCP format: /mcp/{prompt_name}
                path = f"/mcp/{prompt_name}"

                # Get function docstring for description
                description = handler_fn.__doc__ or f"Execute the {prompt_name} prompt"

                # Extract examples from docstring
                examples = self._extract_examples_from_docstring(handler_fn.__doc__ or "")

                paths[path] = {
                    "post": {
                        "summary": f"Execute {prompt_name} prompt",
                        "description": description,
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": properties,
                                        "required": required_params
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Prompt executed successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "description": "Response from the prompt execution"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                # Add examples if available
                if examples:
                    paths[path]["post"]["requestBody"]["content"]["application/json"]["examples"] = examples

        return paths

    def _extract_examples_from_docstring(self, docstring: str) -> Dict[str, Any]:
        """Extract examples from function docstring."""
        import json
        import re

        examples: Dict[str, Any] = {}
        if not docstring:
            return examples

        # Enhanced regex patterns to capture examples more effectively
        # Pattern to match "Input:" followed by JSON content
        input_pattern = r'(?:Input|Example Input|Request):\s*\n?(?:```(?:json)?\n?)?({.*?})(?:\n?```)?'
        output_pattern = r'(?:Output|Example Output|Response):\s*\n?(?:```(?:json)?\n?)?({.*?})(?:\n?```)?'

        # Try to extract examples using the enhanced patterns
        input_matches = re.findall(input_pattern, docstring, re.DOTALL | re.IGNORECASE)
        output_matches = re.findall(output_pattern, docstring, re.DOTALL | re.IGNORECASE)

        # Also try for basic inline patterns
        if not input_matches:
            input_match = re.search(r'Input:\s*(\{.*?\})', docstring, re.DOTALL)
            if input_match:
                input_matches = [input_match.group(1)]
        if not output_matches:
            output_match = re.search(r'Output:\s*(\{.*?\})', docstring, re.DOTALL)
            if output_match:
                output_matches = [output_match.group(1)]

        # Process input examples
        for i, input_text in enumerate(input_matches):
            try:
                # Clean up the example string to make it valid JSON
                cleaned_input = input_text.strip()
                # Replace Python literals with JSON equivalents
                cleaned_input = cleaned_input.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
                input_data = json.loads(cleaned_input)
                examples[f"example_input_{i+1}"] = {"value": input_data}
            except json.JSONDecodeError:
                # If direct JSON parsing fails, try with more cleaning
                try:
                    # Remove potential extra whitespace or comments
                    cleaned_input = re.sub(r',\s*([}\]])', r'\1', input_text.strip())
                    cleaned_input = cleaned_input.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
                    input_data = json.loads(cleaned_input)
                    examples[f"example_input_{i+1}"] = {"value": input_data}
                except json.JSONDecodeError:
                    continue  # Skip this example if parsing fails

        # Process output examples
        for i, output_text in enumerate(output_matches):
            try:
                # Clean up the example string to make it valid JSON
                cleaned_output = output_text.strip()
                # Replace Python literals with JSON equivalents
                cleaned_output = cleaned_output.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
                output_data = json.loads(cleaned_output)
                examples[f"example_output_{i+1}"] = {"value": output_data}
            except json.JSONDecodeError:
                # If direct JSON parsing fails, try with more cleaning
                try:
                    # Remove potential extra whitespace or comments
                    cleaned_output = re.sub(r',\s*([}\]])', r'\1', output_text.strip())
                    cleaned_output = cleaned_output.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
                    output_data = json.loads(cleaned_output)
                    examples[f"example_output_{i+1}"] = {"value": output_data}
                except json.JSONDecodeError:
                    continue  # Skip this example if parsing fails

        return examples

    async def generate_documentation(self) -> Dict[str, Any]:
        """Generate API documentation."""
        # Regenerate spec to capture any new endpoints
        self.spec = self._generate_spec()
        return self.spec

    async def get_openapi_spec(self) -> Dict[str, Any]:
        """Get the OpenAPI specification."""
        # Regenerate spec to capture any new endpoints
        self.spec = self._generate_spec()
        return self.spec

    def update_mcp_server(self, mcp_server: Any) -> None:
        """Update the MCP server reference and regenerate documentation."""
        self.mcp_server = mcp_server
        self.spec = self._generate_spec()