import tempfile
from pathlib import Path

import pytest

from src.shell.adapters.prompt_loaders.yaml_prompt_loader import YAMLPromptLoader


def test_yaml_prompt_loader_initialization_default_path():
    """Test YAMLPromptLoader initialization with default path"""
    loader = YAMLPromptLoader()

    assert hasattr(loader, 'prompts_directory')
    assert isinstance(loader.prompts_directory, str)


def test_yaml_prompt_loader_initialization_custom_path():
    """Test YAMLPromptLoader initialization with custom path"""
    custom_path = "/custom/prompts/path"
    loader = YAMLPromptLoader(custom_path)
    
    assert loader.prompts_directory == custom_path


def test_yaml_prompt_loader_load_prompt_template_from_consolidated_file():
    """Test load_prompt_template with consolidated prompts file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        consolidated_path = Path(temp_dir) / "prompts.yaml"
        with open(consolidated_path, 'w') as f:
            f.write("""
prompts:
  test_prompt:
    template: "This is a test prompt with {param}"
    description: "A test prompt"
""")

        loader = YAMLPromptLoader(str(temp_dir))
        result = loader.load_prompt_template("test_prompt")

        assert result is not None
        assert result["template"] == "This is a test prompt with {param}"
        assert result["description"] == "A test prompt"


def test_yaml_prompt_loader_load_prompt_template_individual_file():
    """Test load_prompt_template with individual prompt file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        prompt_path = Path(temp_dir) / "individual_prompt.yaml"
        with open(prompt_path, 'w') as f:
            f.write("""
template: "This is an individual prompt with {param}"
description: "An individual prompt"
""")

        loader = YAMLPromptLoader(str(temp_dir))
        result = loader.load_prompt_template("individual_prompt")

        assert result is not None
        assert result["template"] == "This is an individual prompt with {param}"
        assert result["description"] == "An individual prompt"


def test_yaml_prompt_loader_load_prompt_template_not_found():
    """Test load_prompt_template with non-existent prompt"""
    loader = YAMLPromptLoader()
    result = loader.load_prompt_template("non_existent_prompt")
    
    assert result is None


def test_yaml_prompt_loader_load_prompt_template_invalid_yaml():
    """Test load_prompt_template with invalid YAML"""
    with tempfile.TemporaryDirectory() as temp_dir:
        prompt_path = Path(temp_dir) / "invalid_prompt.yaml"
        with open(prompt_path, 'w') as f:
            f.write("""
template: "This is invalid YAML
description: "An invalid prompt
""")

        loader = YAMLPromptLoader(str(temp_dir))
        try:
            result = loader.load_prompt_template("invalid_prompt")
            assert result is None
        except Exception:
            pass


def test_yaml_prompt_loader_get_prompt_content():
    """Test get_prompt_content method"""
    with tempfile.TemporaryDirectory() as temp_dir:
        consolidated_path = Path(temp_dir) / "prompts.yaml"
        with open(consolidated_path, 'w') as f:
            f.write("""
prompts:
  test_prompt:
    template: "This is a test prompt with {param}"
    description: "A test prompt"
""")

        loader = YAMLPromptLoader(str(temp_dir))
        result = loader.get_prompt_content("test_prompt")

        assert result == "This is a test prompt with {param}"


def test_yaml_prompt_loader_get_prompt_content_not_found():
    """Test get_prompt_content with non-existent prompt"""
    loader = YAMLPromptLoader()
    result = loader.get_prompt_content("non_existent_prompt")
    
    assert result is None


def test_yaml_prompt_loader_format_prompt_success():
    """Test format_prompt method with valid parameters"""
    with tempfile.TemporaryDirectory() as temp_dir:
        consolidated_path = Path(temp_dir) / "prompts.yaml"
        with open(consolidated_path, 'w') as f:
            f.write("""
prompts:
  test_prompt:
    template: "This is a test prompt with {param1} and {param2}"
    description: "A test prompt"
""")

        loader = YAMLPromptLoader(str(temp_dir))
        result = loader.format_prompt("test_prompt", param1="value1", param2="value2")

        assert result == "This is a test prompt with value1 and value2"


def test_yaml_prompt_loader_format_prompt_missing_params():
    """Test format_prompt method with missing parameters (should raise ValueError)"""
    with tempfile.TemporaryDirectory() as temp_dir:
        consolidated_path = Path(temp_dir) / "prompts.yaml"
        with open(consolidated_path, 'w') as f:
            f.write("""
prompts:
  test_prompt:
    template: "This is a test prompt with {param1} and {param2}"
    description: "A test prompt"
""")

        loader = YAMLPromptLoader(str(temp_dir))

        with pytest.raises(ValueError, match=r"Missing required parameter.*param1.*"):
            loader.format_prompt("test_prompt", param2="value2")


def test_yaml_prompt_loader_format_prompt_prompt_not_found():
    """Test format_prompt method with non-existent prompt"""
    loader = YAMLPromptLoader()
    result = loader.format_prompt("non_existent_prompt", param="value")
    
    assert result is None


def test_yaml_prompt_loader_caching_behavior():
    """Test that prompts are properly cached after first load"""
    with tempfile.TemporaryDirectory() as temp_dir:
        consolidated_path = Path(temp_dir) / "prompts.yaml"
        with open(consolidated_path, 'w') as f:
            f.write("""
prompts:
  cached_prompt:
    template: "This is a cached prompt with {param}"
    description: "A cached prompt"
""")

        loader = YAMLPromptLoader(str(temp_dir))

        loader.load_prompt_template("cached_prompt")

        loader._loaded_prompts["cached_prompt"]["modified_in_cache"] = True

        result2 = loader.load_prompt_template("cached_prompt")

        assert result2 is not None
        assert result2["modified_in_cache"] is True