from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    prompts_file_path: str = Field(
        default="resources/prompts.yaml",
        description="Full path to the prompts YAML file"
    )

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }