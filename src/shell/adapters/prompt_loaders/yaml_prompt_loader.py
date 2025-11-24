import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class YAMLPromptLoader:
    """
    Base class for loading prompts from YAML configuration files.
    """

    def __init__(self, prompts_directory: Optional[str] = None):
        if prompts_directory is None:
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent.parent.parent
            prompts_directory = str(project_root / "prompts")

        self.prompts_directory = prompts_directory
        self._loaded_prompts: Dict[str, Any] = {}
        self._all_prompts_data: Optional[Dict[str, Any]] = None
    
    def load_prompt_template(self, prompt_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a prompt template from YAML file.

        Args:
            prompt_name: Name of the prompt to load

        Returns:
            Dictionary containing the prompt configuration, or None if not found
        """
        if prompt_name in self._loaded_prompts:
            return self._loaded_prompts[prompt_name]  # type: ignore[no-any-return]

        # First, try the consolidated prompts file (most efficient approach)
        if self._all_prompts_data is None:
            # Try the consolidated prompts file
            consolidated_path = os.path.join(self.prompts_directory, "prompts.yaml")
            if not os.path.exists(consolidated_path):
                consolidated_path = os.path.join(self.prompts_directory, "prompts.yml")

            if os.path.exists(consolidated_path):
                with open(consolidated_path, 'r', encoding='utf-8') as file:
                    all_data: Any = yaml.safe_load(file)
                    if isinstance(all_data, dict) and 'prompts' in all_data:
                        self._all_prompts_data = all_data['prompts']
                        # Cache all prompts from the consolidated file
                        for name, config in self._all_prompts_data.items():
                            self._loaded_prompts[name] = config

        # Check if we have the prompt in the consolidated data
        if self._all_prompts_data and prompt_name in self._all_prompts_data:
            self._loaded_prompts[prompt_name] = self._all_prompts_data[prompt_name]
            return self._all_prompts_data[prompt_name]  # type: ignore[no-any-return]

        # If not found in consolidated file, try individual prompt file
        yaml_file_path = os.path.join(self.prompts_directory, f"{prompt_name}.yaml")
        if not os.path.exists(yaml_file_path):
            yaml_file_path = os.path.join(self.prompts_directory, f"{prompt_name}.yml")
            if not os.path.exists(yaml_file_path):
                return None

        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data: Any = yaml.safe_load(file)
            # For individual files, expect the structure to be directly the prompt config
            if isinstance(data, dict):
                result: Dict[str, Any] = data
                self._loaded_prompts[prompt_name] = result
                return result

        return None
    
    def get_prompt_content(self, prompt_name: str) -> Optional[str]:
        """
        Get the prompt template content from YAML configuration.

        Args:
            prompt_name: Name of the prompt to load

        Returns:
            The prompt template string, or None if not found
        """
        prompt_config = self.load_prompt_template(prompt_name)
        if not prompt_config:
            return None

        # Get the template from the prompt configuration
        template = prompt_config.get('template', '')
        return template  # type: ignore[no-any-return]
    
    def format_prompt(self, prompt_name: str, **kwargs: Any) -> Optional[str]:
        """
        Load and format a prompt with the provided keyword arguments.

        Args:
            prompt_name: Name of the prompt to load
            **kwargs: Keyword arguments to format the prompt template

        Returns:
            Formatted prompt string, or None if prompt not found
        """
        template = self.get_prompt_content(prompt_name)
        if template is None:
            return None

        try:
            result: str = template.format(**kwargs)
            return result
        except KeyError as e:
            raise ValueError(f"Missing required parameter {e} for prompt {prompt_name}") from e