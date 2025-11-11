import pytest

from src.core.models.prompt_models import PromptRequest, PromptResponse, PromptTemplate
from src.core.models.variable_models import Variable
from src.core.use_cases.prompt_use_cases import (
    substitute_variables,
    validate_prompt_request,
    validate_prompt_template,
)


def test_prompt_template_with_valid_data_creates_instance():
    """Test that PromptTemplate can be created with valid data"""
    variables = (Variable("name", "string"),)
    template = PromptTemplate(
        template_id="test.id",
        template_content="Hello {name}",
        variables=variables,
        description="Test template",
        model_name="gpt-4o"
    )
    assert template.template_id == "test.id"
    assert template.template_content == "Hello {name}"
    assert len(template.variables) == 1
    assert template.description == "Test template"
    assert template.model_name == "gpt-4o"


def test_prompt_template_with_invalid_id_raises_error():
    """Test that PromptTemplate with invalid ID raises error"""
    variables = (Variable("name", "string"),)
    with pytest.raises(ValueError):
        PromptTemplate(
            template_id="",  # Invalid - empty
            template_content="Hello {name}",
            variables=variables,
            description="Test template",
            model_name="gpt-4o"
        )


def test_prompt_template_with_invalid_content_raises_error():
    """Test that PromptTemplate with invalid content raises error"""
    variables = (Variable("name", "string"),)
    with pytest.raises(ValueError):
        PromptTemplate(
            template_id="test.id",
            template_content="",  # Invalid - empty
            variables=variables,
            description="Test template",
            model_name="gpt-4o"
        )


def test_prompt_request_with_valid_data_creates_instance():
    """Test that PromptRequest can be created with valid data"""
    request = PromptRequest(
        template_id="test.id",
        variables={"name": "Alice"}
    )
    assert request.template_id == "test.id"
    assert request.variables == {"name": "Alice"}
    assert isinstance(request.request_id, str)
    assert len(request.request_id) > 0


def test_prompt_request_with_invalid_template_id_raises_error():
    """Test that PromptRequest with invalid template ID raises error"""
    with pytest.raises(ValueError):
        PromptRequest(
            template_id="",  # Invalid - empty
            variables={"name": "Alice"}
        )


def test_prompt_request_with_invalid_variables_raises_error():
    """Test that PromptRequest with invalid variables raises error"""
    with pytest.raises(ValueError):
        PromptRequest(
            template_id="test.id",
            variables="invalid"  # Should be dict, not string
        )


def test_prompt_response_with_valid_data_creates_instance():
    """Test that PromptResponse can be created with valid data"""
    response = PromptResponse(
        request_id="req123",
        template_id="test.id",
        result="Test result",
        execution_time_ms=100.0
    )
    assert response.request_id == "req123"
    assert response.template_id == "test.id"
    assert response.result == "Test result"
    assert response.execution_time_ms == 100.0


def test_prompt_response_with_negative_execution_time_raises_error():
    """Test that PromptResponse with negative execution time raises error"""
    with pytest.raises(ValueError):
        PromptResponse(
            request_id="req123",
            template_id="test.id",
            result="Test result",
            execution_time_ms=-10.0  # Invalid - negative
        )


def test_variable_with_valid_data_creates_instance():
    """Test that Variable can be created with valid data"""
    variable = Variable(
        name="test_var",
        type_hint="string",
        description="A test variable",
        required=True
    )
    assert variable.name == "test_var"
    assert variable.type_hint == "string"
    assert variable.description == "A test variable"
    assert variable.required is True


def test_variable_with_invalid_name_raises_error():
    """Test that Variable with invalid name raises error"""
    with pytest.raises(ValueError):
        Variable(
            name="",  # Invalid - empty
            type_hint="string"
        )


def test_variable_with_invalid_type_hint_raises_error():
    """Test that Variable with invalid type hint raises error"""
    with pytest.raises(ValueError):
        Variable(
            name="test_var",
            type_hint=""  # Invalid - empty
        )


def test_substitute_variables_with_valid_input():
    """Test variable substitution with valid input"""
    template = "Hello {name}, your score is {score}"
    variables = {"name": "Alice", "score": 95}
    result = substitute_variables(template, variables)
    assert result == "Hello Alice, your score is 95"


def test_substitute_variables_with_missing_variable_raises_error():
    """Test that missing variables raise error during substitution"""
    template = "Hello {name}, your score is {score}"
    variables = {"name": "Alice"}  # missing score
    with pytest.raises(ValueError):
        substitute_variables(template, variables)


def test_validate_prompt_template_with_valid_template():
    """Test validation of a valid prompt template"""
    variables = (Variable("name", "string"), Variable("score", "number"))
    template = PromptTemplate(
        template_id="test.id",
        template_content="Hello {name}, your score is {score}",
        variables=variables,
        description="Test template",
        model_name="gpt-4o"
    )
    errors = validate_prompt_template(template)
    assert len(errors) == 0


def test_validate_prompt_template_with_invalid_placeholders():
    """Test validation of a template with invalid placeholders"""
    variables = (Variable("name", "string"),)  # Only defines 'name'
    template = PromptTemplate(
        template_id="test.id",
        template_content="Hello {name}, your score is {score}",  # refs 'score' but doesn't define it
        variables=variables,
        description="Test template",
        model_name="gpt-4o"
    )
    errors = validate_prompt_template(template)
    assert len(errors) == 1
    assert "score" in errors[0]


def test_validate_prompt_request_with_required_variables():
    """Test validation of a prompt request with required variables"""
    variables = (Variable("name", "string", required=True),)
    template = PromptTemplate(
        template_id="test.id",
        template_content="Hello {name}",
        variables=variables,
        description="Test template",
        model_name="gpt-4o"
    )
    request = PromptRequest(
        template_id="test.id",
        variables={"name": "Alice"}
    )
    
    errors = validate_prompt_request(request, template)
    assert len(errors) == 0


def test_validate_prompt_request_missing_required_variable():
    """Test validation of a prompt request missing required variables"""
    variables = (Variable("name", "string", required=True),)
    template = PromptTemplate(
        template_id="test.id",
        template_content="Hello {name}",
        variables=variables,
        description="Test template",
        model_name="gpt-4o"
    )
    request = PromptRequest(
        template_id="test.id",
        variables={}  # Missing required 'name' variable
    )
    
    errors = validate_prompt_request(request, template)
    assert len(errors) == 1
    assert "name" in errors[0]