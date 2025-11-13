import pytest

from src.adapters.template_engine.template_renderer import TemplateRenderer
from src.core.models.prompt_models import PromptTemplate
from src.core.models.variable_models import Variable


class TestTemplateRenderer:
    """Tests for TemplateRenderer class."""

    def test_render_template_with_valid_data(self):
        """Test rendering a template with valid data."""
        variables = (Variable("name", "string"), Variable("city", "string"))
        template = PromptTemplate(
            template_id="welcome-template",
            template_content="Hello {name}, welcome to {city}!",
            variables=variables,
            description="Welcome message template",
            model_name="gpt-4o"
        )
        
        result = TemplateRenderer.render_template(template, {"name": "Alice", "city": "Paris"})
        assert result == "Hello Alice, welcome to Paris!"

    def test_render_template_with_missing_required_variable(self):
        """Test rendering a template with missing required variables."""
        variables = (Variable("name", "string", required=True), Variable("city", "string", required=True))
        template = PromptTemplate(
            template_id="welcome-template",
            template_content="Hello {name}, welcome to {city}!",
            variables=variables,
            description="Welcome message template",
            model_name="gpt-4o"
        )
        
        with pytest.raises(ValueError, match="Validation errors"):
            TemplateRenderer.render_template(template, {"name": "Alice"})  # Missing city

    def test_render_template_with_undefined_template_variable(self):
        """Test rendering with placeholder in template content but not in provided variables."""
        variables = (Variable("name", "string"),)  # Only defines 'name' in template definition
        template = PromptTemplate(
            template_id="test-template",
            template_content="Hello {name}, your score is {score}",  # Contains 'score' placeholder
            variables=variables,
            description="Test template",
            model_name="gpt-4o"
        )
        
        # This should pass validation (name is provided as required variable) but fail during substitution
        # because 'score' placeholder in template content is not in provided variables
        with pytest.raises(ValueError, match=r"Template rendering failed: Missing required variable 'score' for template"):
            TemplateRenderer.render_template(template, {"name": "Alice"})

    def test_validate_template_syntax_valid(self):
        """Test validating template syntax with valid content."""
        errors = TemplateRenderer.validate_template_syntax("Hello {name}, welcome to {place}!")
        assert len(errors) == 0

    def test_validate_template_syntax_unbalanced_braces(self):
        """Test validating template syntax with unbalanced braces."""
        errors = TemplateRenderer.validate_template_syntax("Hello {name}, welcome to {place!")
        assert len(errors) > 0
        assert "Unbalanced braces" in errors[0]

    def test_validate_template_syntax_balanced_braces(self):
        """Test validating template syntax with actually balanced braces."""
        # Test with balanced actual braces (not just template placeholders)
        errors = TemplateRenderer.validate_template_syntax("Hello {name}, welcome to {place}")
        assert len(errors) == 0
        
        # This has unbalanced braces - 2 opening but 3 closing
        errors = TemplateRenderer.validate_template_syntax("Hello {name}, welcome to {place}}")
        assert len(errors) > 0
        assert "Unbalanced braces" in errors[0]

    def test_get_template_placeholders(self):
        """Test extracting placeholders from template content."""
        placeholders = TemplateRenderer.get_template_placeholders("Hello {name}, welcome to {place} in {year}!")
        assert set(placeholders) == {"name", "place", "year"}

    def test_get_template_placeholders_empty(self):
        """Test extracting placeholders from template with no placeholders."""
        placeholders = TemplateRenderer.get_template_placeholders("Hello world!")
        assert placeholders == []

    def test_get_template_placeholders_duplicate(self):
        """Test extracting placeholders with duplicates (should return unique)."""
        placeholders = TemplateRenderer.get_template_placeholders("Hello {name}, meet {name} again!")
        assert placeholders == ["name"]  # Should return list of unique placeholders

    def test_render_template_with_special_characters(self):
        """Test rendering template with special characters."""
        variables = (Variable("text", "string"),)
        template = PromptTemplate(
            template_id="special-template",
            template_content="Special chars: {text}",
            variables=variables,
            description="Test special chars",
            model_name="gpt-4o"
        )
        
        result = TemplateRenderer.render_template(template, {"text": "Line1\nLine2\tTab"})
        assert "Line1" in result
        assert "Line2" in result
        assert "Tab" in result