import json
from typing import Any

from src.core.models.directory_models import (
    DirectoryConfig,
)
from src.core.use_cases.directory_use_cases import (
    validate_directory_config,
    validate_path_security,
)


class DirectoryOrchestrator:
    """Orchestrator for directory operations using FastMCP Context implementing the Imperative Shell pattern."""

    def __init__(
        self,
        ctx: Any,
        filesystem_adapter: Any
    ) -> None:
        if len(locals()) > 4:  # self + 2 dependencies
            raise ValueError("Orchestrator should have maximum 3 dependencies (4 including self)")

        self.ctx = ctx
        self.filesystem_adapter = filesystem_adapter

    async def ensure_directories_exist(self, config: DirectoryConfig) -> bool:
        """Create ctxfy/ and ctxfy/specifications/ using Context's sample method"""
        try:
            # Validate the directory configuration
            config_validation = validate_directory_config(config)
            if not config_validation.is_valid:
                await self.ctx.error(f"Invalid directory configuration: {config_validation.errors}")
                return False

            # Validate security for base path
            security_validation = validate_path_security(config.base_path)
            if not security_validation.is_valid:
                await self.ctx.error(f"Security validation failed for base path: {security_validation.errors}")
                return False

            # Create main directory using Context sampling
            main_dir_result = await self.ctx.sample({
                "action": "create_directory",
                "path": config.base_path,
                "description": f"Create main directory for ctxfy server: {config.base_path}"
            })

            # Parse the result from ctx.sample - it might return a dict or a string
            if isinstance(main_dir_result, str):
                try:
                    main_dir_result = json.loads(main_dir_result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {main_dir_result}")
                    return False

            if not main_dir_result.get("success", main_dir_result.get("created", False)):
                error_msg = main_dir_result.get("error", "Unknown error creating main directory")
                await self.ctx.error(f"Failed to create main directory: {error_msg}")
                return False

            # Create subdirectories
            for subdir in config.subdirectories:
                full_path = f"{config.base_path}/{subdir}"

                # Validate security for each subdirectory path
                subdir_security = validate_path_security(full_path)
                if not subdir_security.is_valid:
                    await self.ctx.error(f"Security validation failed for subdirectory: {subdir_security.errors}")
                    return False

                subdir_result = await self.ctx.sample({
                    "action": "create_directory", 
                    "path": full_path,
                    "description": f"Create subdirectory: {full_path}"
                })

                # Parse the result from ctx.sample
                if isinstance(subdir_result, str):
                    try:
                        subdir_result = json.loads(subdir_result)
                    except json.JSONDecodeError:
                        await self.ctx.error(f"Could not parse result from ctx.sample: {subdir_result}")
                        return False

                if not subdir_result.get("success", subdir_result.get("created", False)):
                    error_msg = subdir_result.get("error", "Unknown error creating subdirectory")
                    await self.ctx.error(f"Failed to create subdirectory {full_path}: {error_msg}")
                    return False

            return True

        except Exception as e:
            await self.ctx.error(f"Unexpected error in ensure_directories_exist: {str(e)}")
            return False

    async def create_readme(self, content: str, directory_path: str) -> bool:
        """Create README file in the specified directory using Context"""
        try:
            # Validate path security
            security_validation = validate_path_security(directory_path)
            if not security_validation.is_valid:
                await self.ctx.error(f"Security validation failed for README path: {security_validation.errors}")
                return False

            # Create the README file path
            readme_path = f"{directory_path}/README.md"

            # Write the README file content using Context sampling
            result = await self.ctx.sample({
                "action": "write_file",
                "path": readme_path,
                "content": content,
                "description": f"Create README.md in {directory_path}"
            })

            # Parse the result from ctx.sample
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {result}")
                    return False

            if not result.get("success", result.get("written", False)):
                error_msg = result.get("error", "Unknown error creating README file")
                await self.ctx.error(f"Failed to create README file: {error_msg}")
                return False

            return True

        except Exception as e:
            await self.ctx.error(f"Unexpected error in create_readme: {str(e)}")
            return False