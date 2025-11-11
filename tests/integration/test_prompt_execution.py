import asyncio
from unittest.mock import AsyncMock

import pytest

from src.adapters.llm_sampling.llm_sampler import LLMSampler
from src.adapters.prompt_registry.prompt_registry import PromptRegistryAdapter
from src.adapters.template_engine.template_renderer import TemplateRenderer
from src.core.models.prompt_models import PromptTemplate
from src.core.models.variable_models import Variable
from src.core.use_cases.prompt_use_cases import substitute_variables


@pytest.fixture
def sample_template():
    """Fixture for a sample prompt template"""
    variables = (Variable("name", "string"), Variable("score", "number"))
    return PromptTemplate(
        template_id="test.summary",
        template_content="Student {name} has a score of {score}",
        variables=variables,
        description="A test template for student summary",
        model_name="gpt-4o"
    )


@pytest.fixture
def sample_registry():
    """Fixture for a sample prompt registry"""
    return PromptRegistryAdapter()


def test_template_renderer_integration(sample_template):
    """Integration test for template rendering with variable substitution"""
    variables = {"name": "Alice", "score": 95}
    
    # Render the template using the adapter
    result = TemplateRenderer.render_template(sample_template, variables)
    
    # Verify the result
    assert result == "Student Alice has a score of 95"
    
    # Verify that the template validation is working
    validation_errors = TemplateRenderer.validate_template_syntax(sample_template.template_content)
    assert len(validation_errors) == 0


def test_prompt_registry_integration(sample_template, sample_registry):
    """Integration test for prompt registry operations"""
    # Register a template
    result = asyncio.run(
        sample_registry.register_prompt_template(sample_template.template_id, sample_template)
    )
    assert result is True
    
    # Retrieve the template
    retrieved = asyncio.run(
        sample_registry.get_prompt_template(sample_template.template_id)
    )
    assert retrieved is not None
    assert retrieved.template_id == sample_template.template_id
    assert retrieved.template_content == sample_template.template_content
    
    # Get all templates
    all_templates = asyncio.run(
        sample_registry.get_registered_prompts()
    )
    assert len(all_templates) == 1
    assert all_templates[0].template_id == sample_template.template_id


def test_template_engine_with_registry_integration(sample_template):
    """Integration test between template engine and registry"""
    # First register the template
    registry = PromptRegistryAdapter()
    asyncio.run(
        registry.register_prompt_template(sample_template.template_id, sample_template)
    )
    
    # Then retrieve and use it with the template engine
    retrieved_template = asyncio.run(
        registry.get_prompt_template(sample_template.template_id)
    )
    
    assert retrieved_template is not None
    
    # Use the template engine to render the retrieved template
    variables = {"name": "Bob", "score": 87}
    result = TemplateRenderer.render_template(retrieved_template, variables)
    
    assert result == "Student Bob has a score of 87"


def test_substitute_variables_use_case_with_template_engine():
    """Integration test between use case and template engine for variable substitution"""
    template_content = "Process {task} with priority {priority}"
    
    # Use the core use case directly
    variables_dict = {"task": "data processing", "priority": "high"}
    result = substitute_variables(template_content, variables_dict)
    
    assert result == "Process data processing with priority high"
    
    # Also test with the template engine adapter
    variables_obj = (Variable("task", "string"), Variable("priority", "string"))
    template_obj = PromptTemplate(
        template_id="test.process",
        template_content=template_content,
        variables=variables_obj,
        description="Process task template",
        model_name="gpt-4o"
    )
    
    renderer_result = TemplateRenderer.render_template(template_obj, variables_dict)
    assert renderer_result == result


def test_llm_sampler_mock_integration():
    """Integration test for LLM sampler with mocked ctx"""
    # Create a mock context for testing
    mock_ctx = AsyncMock()
    mock_ctx.sample = AsyncMock(return_value="Mocked LLM response")
    
    sampler = LLMSampler(ctx=mock_ctx)
    
    # Test the sample_prompt method
    result = asyncio.run(
        sampler.sample_prompt(
            prompt="Test prompt",
            model="gpt-4o",
            temperature=0.7,
            max_tokens=100
        )
    )
    
    assert result == "Mocked LLM response"
    mock_ctx.sample.assert_called_once_with(
        prompt="Test prompt",
        model="gpt-4o",
        temperature=0.7,
        max_tokens=100
    )


class TestPromptExecutionIntegration:
    """Integration tests for complete prompt execution flow"""
    
    def test_full_prompt_execution_flow(self, sample_template):
        """Test the complete flow from template registration to rendering"""
        # 1. Register template
        registry = PromptRegistryAdapter()
        asyncio.run(
            registry.register_prompt_template(sample_template.template_id, sample_template)
        )
        
        # 2. Retrieve template
        retrieved_template = asyncio.run(
            registry.get_prompt_template(sample_template.template_id)
        )
        assert retrieved_template is not None
        
        # 3. Prepare variables and render template
        input_variables = {"name": "Charlie", "score": 92}
        
        # Render the template with variables
        rendered_content = TemplateRenderer.render_template(retrieved_template, input_variables)
        expected_content = "Student Charlie has a score of 92"
        assert rendered_content == expected_content
        
        # 4. Validate the rendered content has correct syntax
        validation_errors = TemplateRenderer.validate_template_syntax(rendered_content)
        assert len(validation_errors) == 0
        
        # 5. Extract placeholders to ensure they match expected variables
        placeholders = TemplateRenderer.get_template_placeholders(sample_template.template_content)
        assert set(placeholders) == {"name", "score"}


def test_performance_with_multiple_templates():
    """Test performance with multiple templates and variables"""
    registry = PromptRegistryAdapter()
    
    # Create multiple templates
    templates = []
    for i in range(5):
        variables = (Variable("item", "string"), Variable("count", "number"))
        template = PromptTemplate(
            template_id=f"test.template.{i}",
            template_content=f"Item {{item}} has count {{count}} for template {i}",
            variables=variables,
            description=f"Template {i}",
            model_name="gpt-4o"
        )
        templates.append(template)
        
        # Register each template
        result = asyncio.run(
            registry.register_prompt_template(template.template_id, template)
        )
        assert result is True
    
    # Verify all templates are registered
    all_templates = asyncio.run(registry.get_registered_prompts())
    assert len(all_templates) == 5
    
    # Test rendering for each template
    for i, template in enumerate(templates):
        result = TemplateRenderer.render_template(
            template, 
            {"item": f"item_{i}", "count": i * 10}
        )
        expected = f"Item item_{i} has count {i * 10} for template {i}"
        assert result == expected