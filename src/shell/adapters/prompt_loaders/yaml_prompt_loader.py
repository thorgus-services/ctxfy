import os
from typing import Any, Dict, Optional

import yaml

from src.core.ports.prompt_ports import PromptLoaderPort
from src.core.settings import Settings
from src.core.utils.path_utils import get_project_root


class YAMLPromptLoader(PromptLoaderPort):
    def __init__(self) -> None:
        settings = Settings()

        project_root = get_project_root()
        self.prompts_file_path = str(project_root / settings.prompts_file_path)
        self._loaded_prompts: Dict[str, Any] = {}
        self._all_prompts_data: Optional[Dict[str, Any]] = None

    @property
    def prompts_directory(self) -> str:
        from pathlib import Path
        return str(Path(self.prompts_file_path).parent)

    def load_prompt_template(self, prompt_name: str) -> Optional[Dict[str, Any]]:
        if prompt_name in self._loaded_prompts:
            return self._loaded_prompts[prompt_name]  # type: ignore[no-any-return]

        if self._all_prompts_data is None:
            if not os.path.exists(self.prompts_file_path):
                return None

            with open(self.prompts_file_path, 'r', encoding='utf-8') as file:
                all_data: Any = yaml.safe_load(file)
                if isinstance(all_data, dict) and 'prompts' in all_data:
                    self._all_prompts_data = all_data['prompts']
                    for name, config in self._all_prompts_data.items():
                        self._loaded_prompts[name] = config

        if self._all_prompts_data and prompt_name in self._all_prompts_data:
            self._loaded_prompts[prompt_name] = self._all_prompts_data[prompt_name]
            return self._all_prompts_data[prompt_name]  # type: ignore[no-any-return]

        return None

    @property
    def all_prompts_data(self) -> Optional[Dict[str, Any]]:
        return self._all_prompts_data
