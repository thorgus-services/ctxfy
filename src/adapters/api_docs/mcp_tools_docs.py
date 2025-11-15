"""MCP Tools documentation generator for FastMCP framework."""
import inspect
import json
from typing import Annotated, Any, Dict, List, Optional, get_args, get_origin

from fastmcp import FastMCP


class MCPToolsDocsGenerator:
    """Generator for MCP tools documentation following MCP protocol specifications."""

    def __init__(self, mcp_server: Optional[FastMCP] = None):
        self.mcp_server = mcp_server

    def set_mcp_server(self, mcp_server: FastMCP) -> None:
        """Set the MCP server instance."""
        self.mcp_server = mcp_server
    
    def generate_mcp_tools_spec(self) -> Dict[str, Any]:
        """Generate MCP tools specification following the protocol."""
        if not self.mcp_server or not hasattr(self.mcp_server, '_handlers'):
            return {"tools": []}

        tools = []

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
                parameters = {}

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
                                param_schema["required"] = False
                            else:
                                param_schema["required"] = True

                        parameters[param_name] = param_schema

                # Create tool definition following MCP protocol
                tool = {
                    "name": prompt_name,
                    "description": handler_fn.__doc__ or f"Execute the {prompt_name} prompt",
                    "inputSchema": {
                        "type": "object",
                        "properties": parameters,
                        "required": [
                            param_name for param_name, param_schema in parameters.items()
                            if param_schema.get("required", True)  # Default to True if not specified
                        ]
                    }
                }

                tools.append(tool)

        return {"tools": tools}
    
    async def get_mcp_tools_docs(self) -> Dict[str, Any]:
        """Get MCP tools documentation."""
        return self.generate_mcp_tools_spec()
    
    def generate_prompts_list(self) -> List[Dict[str, Any]]:
        """Generate a simple list of available prompts with their descriptions."""
        if not self.mcp_server or not hasattr(self.mcp_server, '_handlers'):
            return []

        prompts = []

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
                params: List[Dict[str, Any]] = []

                for param_name, param in sig.parameters.items():
                    if param_name != 'ctx':  # Skip the context parameter
                        param_info: Dict[str, Any] = {
                            "name": param_name,
                            "required": param.default == inspect.Parameter.empty,
                            "type": "string"  # Default
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
                                param_info["type"] = "string"
                            elif actual_type is int:
                                param_info["type"] = "integer"
                            elif actual_type is bool:
                                param_info["type"] = "boolean"
                            elif actual_type is float:
                                param_info["type"] = "number"
                            elif actual_type is list or get_origin(actual_type) is list:
                                param_info["type"] = "array"
                                item_type = "string"
                                if hasattr(actual_type, '__args__') and actual_type.__args__:
                                    inner_type = actual_type.__args__[0]
                                    if inner_type is str:
                                        item_type = "string"
                                    elif inner_type is int:
                                        item_type = "integer"
                                    elif inner_type is bool:
                                        item_type = "boolean"
                                    elif inner_type is float:
                                        item_type = "number"
                                param_info["items"] = {"type": item_type}
                            elif actual_type is dict or get_origin(actual_type) is dict:
                                param_info["type"] = "object"
                            elif hasattr(actual_type, '__origin__') and actual_type.__origin__ is list:
                                param_info["type"] = "array"
                                item_type = "string"
                                if hasattr(actual_type, '__args__') and actual_type.__args__:
                                    inner_type = actual_type.__args__[0]
                                    if inner_type is str:
                                        item_type = "string"
                                    elif inner_type is int:
                                        item_type = "integer"
                                    elif inner_type is bool:
                                        item_type = "boolean"
                                    elif inner_type is float:
                                        item_type = "number"
                                param_info["items"] = {"type": item_type}
                            elif hasattr(actual_type, '__origin__') and actual_type.__origin__ is dict:
                                param_info["type"] = "object"

                            # Extract description from Field metadata
                            if field_info and hasattr(field_info, 'description'):
                                param_info["description"] = field_info.description

                            # Handle default values
                            if param.default != inspect.Parameter.empty:
                                if hasattr(param.default, 'default'):
                                    # For Field instances
                                    default_val = param.default.default
                                    if default_val != ... and default_val is not None:
                                        param_info["default"] = default_val
                                else:
                                    # For regular defaults
                                    param_info["default"] = param.default
                        else:
                            # Handle non-Annotated parameters
                            # Determine type from annotation
                            if param.annotation != inspect.Parameter.empty:
                                annotation = param.annotation
                                if annotation is str:
                                    param_info["type"] = "string"
                                elif annotation is int:
                                    param_info["type"] = "integer"
                                elif annotation is bool:
                                    param_info["type"] = "boolean"
                                elif annotation is float:
                                    param_info["type"] = "number"
                                elif annotation is list:
                                    param_info["type"] = "array"
                                    param_info["items"] = {"type": "string"}
                                elif annotation is dict:
                                    param_info["type"] = "object"
                                elif get_origin(annotation) is list:
                                    param_info["type"] = "array"
                                    args = get_args(annotation)
                                    if args:
                                        inner_type = args[0]
                                        if inner_type is str:
                                            param_info["items"] = {"type": "string"}
                                        elif inner_type is int:
                                            param_info["items"] = {"type": "integer"}
                                        elif inner_type is bool:
                                            param_info["items"] = {"type": "boolean"}
                                        elif inner_type is float:
                                            param_info["items"] = {"type": "number"}
                                        else:
                                            param_info["items"] = {"type": "string"}

                            if param.default != inspect.Parameter.empty:
                                param_info["default"] = param.default

                        params.append(param_info)

                prompt_info = {
                    "name": prompt_name,
                    "description": handler_fn.__doc__ or f"Execute the {prompt_name} prompt",
                    "parameters": params,
                    "examples": self._extract_examples(handler_fn.__doc__ or "")
                }

                prompts.append(prompt_info)

        return prompts
    
    def _extract_examples(self, docstring: str) -> List[Dict[str, Any]]:
        """Extract examples from docstring."""
        import re

        examples: List[Dict[str, Any]] = []
        if not docstring:
            return examples

        # Enhanced regex patterns to capture examples more effectively
        # Pattern to match "Input:" followed by JSON content
        input_pattern = r'(?:Input|Example Input|Request):\s*\n?(?:```(?:json)?\n?)?({.*?})(?:\n?```)?'
        output_pattern = r'(?:Output|Example Output|Response):\s*\n?(?:```(?:json)?\n?)?({.*?})(?:\n?```)?'

        # Try to extract examples using the enhanced patterns
        input_matches = re.findall(input_pattern, docstring, re.DOTALL | re.IGNORECASE)
        output_matches = re.findall(output_pattern, docstring, re.DOTALL | re.IGNORECASE)

        # Also try for basic inline patterns if enhanced patterns don't find anything
        if not input_matches:
            basic_input_matches = re.findall(r'Input:\s*(\{.*?\})', docstring, re.DOTALL)
            input_matches.extend(basic_input_matches)
        if not output_matches:
            basic_output_matches = re.findall(r'Output:\s*(\{.*?\})', docstring, re.DOTALL)
            output_matches.extend(basic_output_matches)

        # Pair up input and output examples
        for i in range(min(len(input_matches), len(output_matches))):
            try:
                # Clean up the example strings to make them valid JSON
                input_str = input_matches[i].strip()
                output_str = output_matches[i].strip()

                # Replace Python literals with JSON equivalents
                input_str = input_str.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
                output_str = output_str.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")

                # Safely evaluate the JSON strings
                input_data = json.loads(input_str)
                output_data = json.loads(output_str)

                examples.append({
                    "input": input_data,
                    "output": output_data
                })
            except json.JSONDecodeError:
                # If direct JSON parsing fails, try with more cleaning
                try:
                    # Remove potential extra whitespace or comments
                    cleaned_input = re.sub(r',\s*([}\]])', r'\1', input_matches[i].strip())
                    cleaned_output = re.sub(r',\s*([}\]])', r'\1', output_matches[i].strip())

                    # Replace Python literals with JSON equivalents
                    cleaned_input = cleaned_input.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
                    cleaned_output = cleaned_output.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")

                    input_data = json.loads(cleaned_input)
                    output_data = json.loads(cleaned_output)

                    examples.append({
                        "input": input_data,
                        "output": output_data
                    })
                except json.JSONDecodeError:
                    # If JSON parsing fails, skip this example
                    continue

        return examples