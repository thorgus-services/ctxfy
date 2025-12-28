import inspect
from unittest.mock import Mock, patch, MagicMock, PropertyMock
import pytest
import asyncio

from fastmcp import FastMCP, Context

from src.shell.registry.dynamic_prompt_registry import DynamicPromptRegistry
from src.core.models.specification_result import SaveDirectoryPath
from src.core.models.specification_workflow import BusinessRequirements


class TestDynamicPromptRegistry:
    def test_initialization(self):
        """Test that the DynamicPromptRegistry initializes correctly."""
        registry = DynamicPromptRegistry()
        
        assert registry._prompts == {}
        assert registry._registered_functions == {}
        assert registry._yaml_loader is not None

    @patch('src.shell.registry.dynamic_prompt_registry.YAMLPromptLoader')
    def test_load_and_register_all_prompts_with_no_data_initially(self, mock_yaml_loader_class):
        """Test loading and registering prompts when data is initially None."""
        # Create a mock instance
        mock_instance = Mock()
        mock_yaml_loader_class.return_value = mock_instance
        
        # Set up the property to return different values on first and subsequent access
        # We'll use side_effect to control the behavior
        def all_prompts_data_property():
            if not hasattr(self, '_access_count'):
                self._access_count = 0
            self._access_count += 1
            if self._access_count == 1:
                return None  # First access returns None
            else:
                return {
                    'test-prompt': {
                        'description': 'A test prompt',
                        'template': 'Hello {name}',
                        'parameters': [
                            {'name': 'name', 'type': 'str', 'default': 'World'}
                        ]
                    }
                }
        
        # Use PropertyMock to control the property behavior
        type(mock_instance).all_prompts_data = PropertyMock(side_effect=all_prompts_data_property)
        
        registry = DynamicPromptRegistry()
        mcp = FastMCP()
        
        registry.load_and_register_all_prompts(mcp)
        
        # Verify that load_prompt_template was called
        mock_instance.load_prompt_template.assert_called_once_with("specification_save_instruction")
        # Verify that _create_and_register_prompt was called
        assert len(registry._registered_functions) == 1

    @patch('src.shell.registry.dynamic_prompt_registry.YAMLPromptLoader')
    def test_load_and_register_all_prompts_with_existing_data(self, mock_yaml_loader_class):
        """Test loading and registering prompts when data exists initially."""
        mock_instance = Mock()
        mock_yaml_loader_class.return_value = mock_instance
        
        # Set up the property to return data immediately
        type(mock_instance).all_prompts_data = PropertyMock(
            return_value={
                'test-prompt': {
                    'description': 'A test prompt',
                    'template': 'Hello {name}',
                    'parameters': [
                        {'name': 'name', 'type': 'str', 'default': 'World'}
                    ]
                }
            }
        )

        registry = DynamicPromptRegistry()
        mcp = FastMCP()
        
        registry.load_and_register_all_prompts(mcp)
        
        # Verify that load_prompt_template was NOT called since data exists
        mock_instance.load_prompt_template.assert_not_called()
        # Verify that _create_and_register_prompt was called
        assert len(registry._registered_functions) == 1

    @patch('src.shell.registry.dynamic_prompt_registry.YAMLPromptLoader')
    def test_load_and_register_all_prompts_with_empty_data(self, mock_yaml_loader_class):
        """Test loading and registering prompts when data is empty."""
        mock_instance = Mock()
        mock_yaml_loader_class.return_value = mock_instance
        
        # Set up the property to return empty dict
        type(mock_instance).all_prompts_data = PropertyMock(return_value={})

        registry = DynamicPromptRegistry()
        mcp = FastMCP()
        
        registry.load_and_register_all_prompts(mcp)
        
        # Verify that no functions were registered
        assert len(registry._registered_functions) == 0

    def test_create_and_register_prompt(self):
        """Test the _create_and_register_prompt method."""
        registry = DynamicPromptRegistry()
        mcp = FastMCP()
        
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name}',
            'parameters': [
                {'name': 'name', 'type': 'str', 'default': 'World'}
            ]
        }
        
        # Call the private method
        registry._create_and_register_prompt(mcp, 'test-prompt', prompt_config)
        
        # Check that the function was registered
        assert 'test-prompt' in registry._registered_functions
        func = registry._registered_functions['test-prompt']
        assert func.__name__ == 'test_prompt'
        assert func.__doc__ == 'A test prompt'

    def test_create_dynamic_function(self):
        """Test the _create_dynamic_function method."""
        registry = DynamicPromptRegistry()
        
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name}',
            'parameters': [
                {'name': 'name', 'type': 'str', 'default': 'World'}
            ]
        }
        
        parameters = prompt_config['parameters']
        
        # Call the private method
        func = registry._create_dynamic_function('test-prompt', prompt_config, parameters)
        
        # Check that the function was created with proper signature and annotations
        sig = func.__signature__
        assert len(sig.parameters) == 2  # ctx + name
        assert 'ctx' in sig.parameters
        assert 'name' in sig.parameters
        
        annotations = func.__annotations__
        assert annotations['ctx'] == Context  # Fixed: use Context from fastmcp
        assert annotations['return'] == str
        assert annotations['name'] == str

    @pytest.mark.asyncio
    async def test_create_prompt_implementation_with_args(self):
        """Test the _create_prompt_implementation method with positional args."""
        registry = DynamicPromptRegistry()
        
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name}',
            'parameters': [
                {'name': 'name', 'type': 'str'}
            ]
        }
        
        parameters = prompt_config['parameters']
        
        # Call the private method
        func = registry._create_prompt_implementation('test-prompt', 'Hello {name}', parameters)
        
        # Mock the context
        mock_ctx = Mock()
        
        # Call the async function with a positional argument
        result = await func(mock_ctx, 'Alice')
        
        assert result == 'Hello Alice'

    @pytest.mark.asyncio
    async def test_create_prompt_implementation_with_kwargs(self):
        """Test the _create_prompt_implementation method with keyword args."""
        registry = DynamicPromptRegistry()
        
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name}',
            'parameters': [
                {'name': 'name', 'type': 'str'}
            ]
        }
        
        parameters = prompt_config['parameters']
        
        # Call the private method
        func = registry._create_prompt_implementation('test-prompt', 'Hello {name}', parameters)
        
        # Mock the context
        mock_ctx = Mock()
        
        # Call the async function with a keyword argument
        result = await func(mock_ctx, name='Bob')
        
        assert result == 'Hello Bob'

    @pytest.mark.asyncio
    async def test_create_prompt_implementation_with_default_value(self):
        """Test the _create_prompt_implementation method with default values."""
        registry = DynamicPromptRegistry()
        
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name}',
            'parameters': [
                {'name': 'name', 'type': 'str', 'default': 'DefaultName'}
            ]
        }
        
        parameters = prompt_config['parameters']
        
        # Call the private method
        func = registry._create_prompt_implementation('test-prompt', 'Hello {name}', parameters)
        
        # Mock the context
        mock_ctx = Mock()
        
        # Call the async function without providing the parameter (should use default)
        result = await func(mock_ctx)
        
        assert result == 'Hello DefaultName'

    @pytest.mark.asyncio
    async def test_create_prompt_implementation_missing_required_parameter(self):
        """Test the _create_prompt_implementation method raises error for missing required parameter."""
        registry = DynamicPromptRegistry()
        
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name}',
            'parameters': [
                {'name': 'name', 'type': 'str'}  # No default value
            ]
        }
        
        parameters = prompt_config['parameters']
        
        # Call the private method
        func = registry._create_prompt_implementation('test-prompt', 'Hello {name}', parameters)
        
        # Mock the context
        mock_ctx = Mock()
        
        # Call the async function without providing the required parameter should raise ValueError
        with pytest.raises(ValueError, match="Missing required parameter 'name' for prompt test-prompt"):
            await func(mock_ctx)

    @pytest.mark.asyncio
    async def test_create_prompt_implementation_missing_template_parameter(self):
        """Test the _create_prompt_implementation method raises error for missing template parameter."""
        registry = DynamicPromptRegistry()
        
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name} and {other}',
            'parameters': [
                {'name': 'name', 'type': 'str', 'default': 'Default'}
            ]
        }
        
        parameters = prompt_config['parameters']
        
        # Call the private method
        func = registry._create_prompt_implementation('test-prompt', 'Hello {name} and {other}', parameters)
        
        # Mock the context
        mock_ctx = Mock()
        
        # Call the async function without providing 'other' parameter should raise ValueError
        with pytest.raises(ValueError, match="Missing required parameter 'other' for prompt test-prompt"):
            await func(mock_ctx)

    def test_build_signature_with_various_types(self):
        """Test the _build_signature method with various parameter types."""
        registry = DynamicPromptRegistry()
        
        parameters = [
            {'name': 'name', 'type': 'str'},
            {'name': 'count', 'type': 'int'},
            {'name': 'rate', 'type': 'float'},
            {'name': 'active', 'type': 'bool'},
            {'name': 'path', 'type': 'SaveDirectoryPath'},
            {'name': 'requirements', 'type': 'BusinessRequirements'},
            {'name': 'optional_str', 'type': 'str', 'default': 'default_value'},
            {'name': 'optional_int', 'type': 'int', 'default': 42}
        ]
        
        sig = registry._build_signature(parameters)
        
        # Check that all parameters are present
        assert len(sig.parameters) == 9  # ctx + 8 other parameters
        assert 'ctx' in sig.parameters
        assert 'name' in sig.parameters
        assert 'count' in sig.parameters
        assert 'rate' in sig.parameters
        assert 'active' in sig.parameters
        assert 'path' in sig.parameters
        assert 'requirements' in sig.parameters
        assert 'optional_str' in sig.parameters
        assert 'optional_int' in sig.parameters
        
        # Check types
        assert sig.parameters['name'].annotation == str
        assert sig.parameters['count'].annotation == int
        assert sig.parameters['rate'].annotation == float
        assert sig.parameters['active'].annotation == bool
        assert sig.parameters['path'].annotation == SaveDirectoryPath
        assert sig.parameters['requirements'].annotation == BusinessRequirements
        assert sig.parameters['optional_str'].annotation == str
        assert sig.parameters['optional_int'].annotation == int
        
        # Check defaults
        assert sig.parameters['optional_str'].default == 'default_value'
        assert sig.parameters['optional_int'].default == 42

    def test_build_annotations_with_various_types(self):
        """Test the _build_annotations method with various parameter types."""
        registry = DynamicPromptRegistry()
        
        parameters = [
            {'name': 'name', 'type': 'str'},
            {'name': 'count', 'type': 'int'},
            {'name': 'rate', 'type': 'float'},
            {'name': 'active', 'type': 'bool'},
            {'name': 'path', 'type': 'SaveDirectoryPath'},
            {'name': 'requirements', 'type': 'BusinessRequirements'}
        ]
        
        annotations = registry._build_annotations(parameters)
        
        # Check that all annotations are present
        assert annotations['ctx'] == Context  # Fixed: use Context from fastmcp
        assert annotations['return'] == str
        assert annotations['name'] == str
        assert annotations['count'] == int
        assert annotations['rate'] == float
        assert annotations['active'] == bool
        assert annotations['path'] == SaveDirectoryPath
        assert annotations['requirements'] == BusinessRequirements

    def test_build_signature_with_invalid_default_conversion(self):
        """Test the _build_signature method handles invalid default value conversions."""
        registry = DynamicPromptRegistry()
        
        parameters = [
            {'name': 'count', 'type': 'int', 'default': 'not_a_number'},
            {'name': 'rate', 'type': 'float', 'default': 'not_a_float'},
            {'name': 'active', 'type': 'bool', 'default': 'maybe'}
        ]
        
        # This should not raise an exception, but use the original default value
        sig = registry._build_signature(parameters)
        
        # Check that defaults are handled gracefully
        assert sig.parameters['count'].default == 'not_a_number'
        assert sig.parameters['rate'].default == 'not_a_float'
        # For bool, it should convert string values properly
        assert sig.parameters['active'].default in (True, False)  # Could be True due to string conversion logic

    @pytest.mark.asyncio
    async def test_dynamic_prompt_implementation_with_format_error(self):
        """Test that format errors in the template are properly handled."""
        registry = DynamicPromptRegistry()
        
        # Template with a parameter that's not provided
        prompt_config = {
            'description': 'A test prompt',
            'template': 'Hello {name} and {missing_param}',
            'parameters': [
                {'name': 'name', 'type': 'str', 'default': 'World'}
            ]
        }
        
        parameters = prompt_config['parameters']
        
        # Call the private method
        func = registry._create_prompt_implementation('test-prompt', 'Hello {name} and {missing_param}', parameters)
        
        # Mock the context
        mock_ctx = Mock()
        
        # Call the async function - this should raise a ValueError due to missing parameter in template
        with pytest.raises(ValueError, match="Missing required parameter 'missing_param' for prompt test-prompt"):
            await func(mock_ctx)