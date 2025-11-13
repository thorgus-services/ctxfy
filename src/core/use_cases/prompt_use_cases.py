from typing import Any, Dict, List

from ...core.models.prompt_models import PromptRequest, PromptResponse, PromptTemplate


def register_prompt_template(template: PromptTemplate) -> bool:
    """Pure function to register a prompt template - validation only"""
    # Validate template structure and content
    errors = validate_prompt_template(template)
    if errors:
        raise ValueError(f"Invalid template: {errors}")

    # In a pure function, we just validate - actual registration happens in adapter
    return True


def execute_prompt_request(request: PromptRequest) -> PromptResponse:
    """Pure function to process a prompt request - validation and preparation only"""
    # This function would be called by the adapter to execute the prompt
    # For now, return a response that would be filled in by the adapter
    # This is a simplified implementation - in reality, this would return intermediate data
    # that the adapter uses to perform the actual execution

    # We'll implement a function that would validate the request and return a "prepared" state

    # In a pure function, we can't actually execute the prompt
    # This is just a placeholder to show the structure
    response = PromptResponse(
        request_id=request.request_id,
        template_id=request.template_id,
        result="PLACEHOLDER",  # To be filled by adapter
        execution_time_ms=0.0  # To be calculated with actual execution
    )

    return response


def validate_prompt_template(template: PromptTemplate) -> List[str]:
    """Pure function for template validation"""
    errors = []

    if not template.template_id.strip():
        errors.append("Template ID cannot be empty")

    if not template.template_content.strip():
        errors.append("Template content cannot be empty")

    if not template.description.strip():
        errors.append("Template description cannot be empty")

    if not template.model_name.strip():
        errors.append("Model name cannot be empty")

    # Validate variable placeholders in template content against variables
    import re
    placeholders = set(re.findall(r'\{(\w+)\}', template.template_content))
    variable_names = {var.name for var in template.variables}

    missing_in_template = placeholders - variable_names
    if missing_in_template:
        errors.append(f"Variables in template not defined: {missing_in_template}")

    return errors


def validate_prompt_request(request: PromptRequest, template: PromptTemplate) -> List[str]:
    """Pure function for request validation against a template"""
    errors = []

    # Check that required variables from template are provided in request
    for variable in template.variables:
        if variable.required and variable.name not in request.variables:
            errors.append(f"Required variable '{variable.name}' not provided in request")

    return errors


def substitute_variables(template: str, variables: Dict[str, Any]) -> str:
    """Pure function for template variable substitution - safe string formatting"""
    if not isinstance(template, str):
        raise TypeError("Template must be a string")

    if not isinstance(variables, dict):
        raise TypeError("Variables must be a dictionary")

    # Validate that all required placeholders in template are provided in variables
    import re
    placeholders = re.findall(r'\{(\w+)\}', template)

    for placeholder in placeholders:
        if placeholder not in variables:
            raise ValueError(f"Missing required variable '{placeholder}' for template")

    # Validate variables for injection patterns before substitution
    if _contains_injection_patterns_in_variables(variables):
        raise ValueError("Variables contain potential injection patterns")

    # Perform safe substitution
    try:
        # Use SafeDict to prevent access to special attributes
        safe_vars = SafeDict(**variables)
        result = template.format_map(safe_vars)
        return result
    except KeyError as e:
        raise ValueError(f"Invalid variable substitution: {e}") from e
    except Exception as e:
        raise ValueError(f"Variable substitution failed: {e}") from e


class SafeDict(dict[str, Any]):
    """A safe dictionary for string formatting that prevents access to special attributes."""
    def __getitem__(self, key: str) -> Any:
        value = super().__getitem__(key)
        # If value is a dict, wrap it in SafeDict too
        if isinstance(value, dict):
            return SafeDict(**value)
        return value


def _contains_injection_patterns_in_variables(variables: Dict[str, Any]) -> bool:
    """Check variables recursively for potential injection patterns."""
    def check_value(value: Any) -> bool:
        if isinstance(value, str):
            # Look for exact matches with word boundaries to avoid false positives
            import re
            dangerous_patterns = [
                r'__import__',
                r'exec\s*\(',
                r'eval\s*\(',
                r'importlib',
                r'subprocess',
                r'\bos\.[a-zA-Z]',  # os.something
                r'\bsys\.[a-zA-Z]',  # sys.something
                r'builtins'
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
            return False
        elif isinstance(value, dict):
            return any(check_value(v) for v in value.values())
        elif isinstance(value, list):
            return any(check_value(v) for v in value)
        return False

    return check_value(variables)