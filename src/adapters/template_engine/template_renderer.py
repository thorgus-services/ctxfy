import re
from typing import Any, Dict, List

from ...core.models.prompt_models import PromptTemplate
from ...core.use_cases.prompt_use_cases import (
    substitute_variables,
    validate_prompt_request,
)


class TemplateRenderer:
    """Handles template rendering with variable substitution and validation"""
    
    @staticmethod
    def render_template(template: PromptTemplate, variables: Dict[str, Any]) -> str:
        """Render a template with the provided variables"""
        # Validate the variables against the template requirements
        from ...core.models.prompt_models import PromptRequest
        request = PromptRequest(
            template_id=template.template_id,
            variables=variables
        )
        
        validation_errors = validate_prompt_request(request, template)
        if validation_errors:
            raise ValueError(f"Validation errors: {validation_errors}")
        
        # Perform variable substitution
        try:
            result = substitute_variables(template.template_content, variables)
            return result
        except Exception as e:
            raise ValueError(f"Template rendering failed: {e}") from e
    
    @staticmethod
    def validate_template_syntax(template_content: str) -> List[str]:
        """Validate template syntax for proper placeholder formatting"""
        errors = []
        
        # Check for common syntax errors
        # Look for placeholders like {variable_name} but not {{escaped}} or {variable_name}
        # We want to detect issues like unbalanced braces
        
        # Check for unbalanced braces
        open_braces = template_content.count('{')
        close_braces = template_content.count('}')
        
        if open_braces != close_braces:
            errors.append(f"Unbalanced braces: {open_braces} opening, {close_braces} closing")
        
        # Check for placeholders with spaces or special characters (simplified validation)
        placeholders = re.findall(r'\{(\w+)\}', template_content)
        invalid_placeholders = [p for p in placeholders if not p.replace('_', '').replace('-', '').isalnum() or p.startswith('_')]
        
        if invalid_placeholders:
            errors.append(f"Invalid placeholder names: {invalid_placeholders}")
        
        return errors
    
    @staticmethod
    def get_template_placeholders(template_content: str) -> List[str]:
        """Extract all placeholders from template content"""
        # Find all {placeholder} patterns
        placeholders = re.findall(r'\{(\w+)\}', template_content)
        return list(set(placeholders))  # Return unique placeholders