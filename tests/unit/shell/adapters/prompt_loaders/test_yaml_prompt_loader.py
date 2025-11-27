from src.shell.adapters.prompt_loaders.yaml_prompt_loader import YAMLPromptLoader


def test_yaml_prompt_loader_initialization():
    loader = YAMLPromptLoader()

    assert hasattr(loader, 'prompts_directory')
    assert isinstance(loader.prompts_directory, str)
    assert "resources" in loader.prompts_directory




def test_yaml_prompt_loader_load_existing_prompt():
    loader = YAMLPromptLoader()
    result = loader.load_prompt_template("specification_save_instruction")

    assert result is not None
    assert "template" in result
    assert "description" in result
    assert result["name"] == "Specification Generation and Save Instruction Prompt"




def test_yaml_prompt_loader_load_prompt_template_not_found():
    loader = YAMLPromptLoader()
    result = loader.load_prompt_template("non_existent_prompt")

    assert result is None










def test_yaml_prompt_loader_caching_behavior():
    loader = YAMLPromptLoader()

    # Load a real prompt from resources/prompts.yaml
    loader.load_prompt_template("specification_save_instruction")

    # Modify the cached version
    original_template = loader._loaded_prompts["specification_save_instruction"]["template"]
    loader._loaded_prompts["specification_save_instruction"]["modified_in_cache"] = True

    # Load again and verify it's from cache
    result2 = loader.load_prompt_template("specification_save_instruction")

    assert result2 is not None
    assert result2["modified_in_cache"] is True
    # Restore original value
    loader._loaded_prompts["specification_save_instruction"]["template"] = original_template