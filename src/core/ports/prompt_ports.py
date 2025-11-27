from typing import Any, Dict, Optional, Protocol


class PromptLoaderPort(Protocol):
    def load_prompt_template(self, prompt_name: str) -> Optional[Dict[str, Any]]:
        ...