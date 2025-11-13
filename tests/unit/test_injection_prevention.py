import pytest

from src.core.models.prompt_models import PromptRequest, PromptTemplate
from src.core.models.variable_models import Variable
from src.core.use_cases.prompt_use_cases import (
    SafeDict,
    _contains_injection_patterns_in_variables,
    substitute_variables,
)


def test_substitute_variables_with_injection_patterns_raises_error():
    """Test that substitute_variables raises error for injection patterns in variables"""
    template = "Hello {name}"
    variables = {"name": "test {os.system('rm -rf /')}"}  # Contains injection attempt
    
    with pytest.raises(ValueError, match="Variables contain potential injection patterns"):
        substitute_variables(template, variables)


def test_substitute_variables_with_nested_injection_patterns_raises_error():
    """Test that substitute_variables raises error for nested injection patterns in variables"""
    template = "Hello {user[name]}"
    variables = {"user": {"name": "__import__('os')"}}  # Contains injection attempt
    
    with pytest.raises(ValueError, match="Variables contain potential injection patterns"):
        substitute_variables(template, variables)


def test_safe_dict_basic_functionality():
    """Test that SafeDict works for basic dictionary operations"""
    safe_dict = SafeDict(test="value", another="data")
    
    # Should work for normal access
    assert safe_dict["test"] == "value"
    assert safe_dict["another"] == "data"
    
    # Should wrap nested dict
    nested_data = {"outer": {"inner": "value"}}
    safe_dict = SafeDict(**nested_data)
    assert isinstance(safe_dict["outer"], SafeDict)
    assert safe_dict["outer"]["inner"] == "value"


def test_contains_injection_patterns_in_variables_detects_dangerous_content():
    """Test that _contains_injection_patterns_in_variables detects dangerous patterns"""
    # Test string with dangerous pattern
    variables = {"name": "__import__('os')"}
    assert _contains_injection_patterns_in_variables(variables) is True
    
    # Test another dangerous pattern
    variables = {"input": "exec('code')"}
    assert _contains_injection_patterns_in_variables(variables) is True
    
    # Test nested dict with dangerous pattern
    variables = {"user": {"input": "eval('code')"}}
    assert _contains_injection_patterns_in_variables(variables) is True
    
    # Test nested list with dangerous pattern
    variables = {"items": ["safe", "importlib.import_module('os')"]}
    assert _contains_injection_patterns_in_variables(variables) is True


def test_contains_injection_patterns_in_variables_safe_content():
    """Test that _contains_injection_patterns_in_variables allows safe content"""
    variables = {"name": "Alice", "age": 30}
    assert _contains_injection_patterns_in_variables(variables) is False
    
    # Test with common words that might look like injection but aren't
    variables = {"text": "evaluate this process"}
    assert _contains_injection_patterns_in_variables(variables) is False
    
    # Test with legitimate uses of similar words
    variables = {"word": "evaluation needed"}
    assert _contains_injection_patterns_in_variables(variables) is False
    
    # Test with word that contains 'exec' but is not a function call
    variables = {"text": "excellent performance"}
    assert _contains_injection_patterns_in_variables(variables) is False


def test_prompt_template_with_injection_patterns_raises_error():
    """Test that PromptTemplate with injection patterns raises error"""
    variables = (Variable("name", "string"),)
    with pytest.raises(ValueError, match="Template content contains potential injection patterns"):
        PromptTemplate(
            template_id="test.id",
            template_content="Hello {name} {__import__('os')}",  # Contains injection
            variables=variables,
            description="Test template",
            model_name="gpt-4o"
        )


def test_prompt_request_with_injection_patterns_raises_error():
    """Test that PromptRequest with injection patterns in variables raises error"""
    with pytest.raises(ValueError, match="Variables contain potential injection values"):
        PromptRequest(
            template_id="test.id",
            variables={"name": "test __import__('os')"}  # Contains injection
        )