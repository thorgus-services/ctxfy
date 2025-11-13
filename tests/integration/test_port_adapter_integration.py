import asyncio
from unittest.mock import AsyncMock

import pytest

from src.adapters.llm_sampling.llm_sampler import LLMSampler
from src.adapters.template_engine.template_renderer import TemplateRenderer
from src.adapters.validation import SchemaValidationAdapter
from src.core.models.prompt_models import PromptRequest, PromptTemplate
from src.core.models.variable_models import Variable
from src.core.use_cases.prompt_use_cases import (
    substitute_variables,
    validate_prompt_request,
    validate_prompt_template,
)


class TestPortAdapterIntegration:
    """Integration tests for core use cases with adapters."""

    def test_prompt_template_validation_with_adapter_integration(self):
        """Test prompt template validation from core to validation adapter."""
        # Create a valid template with proper variables
        variables = (Variable("name", "string"), Variable("city", "string"))
        template = PromptTemplate(
            template_id="welcome-template",
            template_content="Hello {name}, welcome to {city}!",
            variables=variables,
            description="Welcome message template",
            model_name="gpt-4o"
        )
        
        # Validate using core function
        errors = validate_prompt_template(template)
        assert len(errors) == 0
        
        # Test with invalid template (undefined placeholder)
        invalid_template = PromptTemplate(
            template_id="invalid-template",
            template_content="Hello {name}, welcome to {city}! Your age is {age}",  # age not in variables
            variables=variables,  # Only defines 'name' and 'city'
            description="Invalid template",
            model_name="gpt-4o"
        )
        
        errors = validate_prompt_template(invalid_template)
        assert len(errors) > 0
        assert "age" in errors[0]  # Error should mention the undefined placeholder

    def test_prompt_request_validation_with_template_integration(self):
        """Test prompt request validation against a template."""
        # Define template with required variables
        variables = (Variable("name", "string", required=True), Variable("role", "string", required=False))
        template = PromptTemplate(
            template_id="user-greeting",
            template_content="Hello {name}, your role is {role}.",
            variables=variables,
            description="User greeting template",
            model_name="gpt-4o"
        )
        
        # Valid request with all required variables
        valid_request = PromptRequest(
            template_id="user-greeting",
            variables={"name": "Alice", "role": "admin"}
        )
        
        errors = validate_prompt_request(valid_request, template)
        assert len(errors) == 0
        
        # Invalid request missing required variable
        invalid_request = PromptRequest(
            template_id="user-greeting", 
            variables={"role": "admin"}  # Missing 'name'
        )
        
        errors = validate_prompt_request(invalid_request, template)
        assert len(errors) == 1
        assert "name" in errors[0]

    def test_template_rendering_with_validation(self):
        """Test complete template rendering with validation."""
        # Create template and request
        variables = (Variable("name", "string"), Variable("city", "string"))
        template = PromptTemplate(
            template_id="welcome-template",
            template_content="Hello {name}, welcome to {city}!",
            variables=variables,
            description="Welcome message template",
            model_name="gpt-4o"
        )
        
        # Render with valid variables
        rendered = TemplateRenderer.render_template(template, {"name": "Alice", "city": "Wonderland"})
        assert rendered == "Hello Alice, welcome to Wonderland!"
        
        # Test with missing variables
        with pytest.raises(ValueError, match="Validation errors"):
            TemplateRenderer.render_template(template, {"name": "Alice"})  # Missing 'city'

    def test_variable_substitution_with_injection_prevention(self):
        """Test variable substitution with injection prevention."""
        # Valid substitution should work
        result = substitute_variables("Hello {name}", {"name": "Alice"})
        assert result == "Hello Alice"
        
        # Injection attempt should be blocked
        with pytest.raises(ValueError, match="Variables contain potential injection patterns"):
            substitute_variables("Hello {name}", {"name": "__import__('os')"})
        
        # Nested injection attempt should be blocked
        with pytest.raises(ValueError, match="Variables contain potential injection patterns"):
            substitute_variables("Hello {user[name]}", {"user": {"name": "exec('bad_code')"}})

    def test_schema_validation_adapter_integration(self):
        """Test schema validation adapter integration."""
        # Valid data should pass validation
        valid_data = {
            "name": "test_prompt",
            "parameters": {"param1": "value1"},
            "request_id": "req-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(valid_data)
        assert result.is_valid is True
        assert len(result.errors) == 0
        
        # Invalid data should fail validation
        invalid_data = {
            "name": "",  # Empty name
            "parameters": "not_a_dict",  # Wrong type
            "request_id": "req-123"
        }
        
        result = SchemaValidationAdapter.validate_prompt_request(invalid_data)
        assert result.is_valid is False
        assert len(result.errors) > 0
        
        # Check that errors are properly structured
        for error in result.errors:
            assert hasattr(error, 'field')
            assert hasattr(error, 'message')
            assert hasattr(error, 'code')

    def test_template_syntax_validation(self):
        """Test template syntax validation."""
        # Valid template should pass
        errors = TemplateRenderer.validate_template_syntax("Hello {name}, welcome to {place}!")
        assert len(errors) == 0
        
        # Template with unbalanced braces should fail
        errors = TemplateRenderer.validate_template_syntax("Hello {name}, welcome to {place!")
        assert len(errors) > 0
        assert "Unbalanced braces" in errors[0]
        
        # Get placeholders should work correctly
        placeholders = TemplateRenderer.get_template_placeholders("Hello {name}, welcome to {place} in {year}!")
        assert set(placeholders) == {"name", "place", "year"}

    def test_llm_sampler_integration(self):
        """Test LLM sampler with mocked ctx to ensure it works properly."""
        async def run_test():
            # Create a mock ctx object
            mock_ctx = AsyncMock()
            mock_ctx.sample.return_value = "Generated response"
            
            # Create sampler and execute
            sampler = LLMSampler(ctx=mock_ctx)
            result = await sampler.sample_prompt(
                prompt="Test prompt",
                model="gpt-4o",
                temperature=0.7,
                max_tokens=100
            )
            
            # Verify the result and ctx sample was called
            assert result == "Generated response"
            mock_ctx.sample.assert_called_once_with(
                prompt="Test prompt",
                model="gpt-4o",
                temperature=0.7,
                max_tokens=100
            )
        
        # Run the async test
        asyncio.run(run_test())

    def test_complete_prompt_flow_integration(self):
        """Test complete flow: validation -> rendering -> potential sampling."""
        # Create template
        variables = (Variable("user", "string"), Variable("task", "string"))
        template = PromptTemplate(
            template_id="task-assignment",
            template_content="Dear {user}, please complete the {task}.",
            variables=variables,
            description="Task assignment template",
            model_name="gpt-4o"
        )
        
        # Create request with variables
        request = PromptRequest(
            template_id="task-assignment",
            variables={"user": "Alice", "task": "report"}
        )
        
        # Validate request against template
        validation_errors = validate_prompt_request(request, template)
        assert len(validation_errors) == 0
        
        # Render the template
        rendered = TemplateRenderer.render_template(template, request.variables)
        assert rendered == "Dear Alice, please complete the report."
        
        # Validate the rendered template has valid syntax
        syntax_errors = TemplateRenderer.validate_template_syntax(rendered)
        assert len(syntax_errors) == 0