import json
from typing import Annotated

from fastmcp import Context

from src.core.ports.filesystem_ports import ClientFilesystemPort


class FilesystemAdapter(ClientFilesystemPort):
    """Implementation of filesystem operations using FastMCP Context"""
    
    def __init__(self, ctx: Annotated[Context, "FastMCP context object"]):
        self.ctx = ctx

    async def create_directory(self, path: str) -> bool:
        """Create directory on client filesystem using Context"""
        try:
            result = await self.ctx.sample({
                "action": "create_directory",
                "path": path,
                "description": f"Create directory: {path}"
            })  # type: ignore[arg-type]

            # Parse the result from ctx.sample
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {result}")
                    return False

            # Handle the result which may be a dict-like object
            # Using type: ignore for the union attribute access issue
            success_val = result.get("success", result.get("created", False))  # type: ignore[union-attr]
            return success_val

        except Exception as e:
            await self.ctx.error(f"Error creating directory {path}: {str(e)}")
            return False

    async def file_exists(self, path: str) -> bool:
        """Check if file exists on client filesystem using Context"""
        try:
            result = await self.ctx.sample({
                "action": "check_file_exists",
                "path": path,
                "description": f"Check if file exists: {path}"
            })  # type: ignore[arg-type]

            # Parse the result from ctx.sample
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {result}")
                    return False

            exists_val = result.get("exists", False)  # type: ignore[union-attr]
            return exists_val

        except Exception as e:
            await self.ctx.error(f"Error checking if file exists {path}: {str(e)}")
            return False

    async def write_file(self, path: str, content: str) -> bool:
        """Write content to file on client filesystem using Context"""
        try:
            result = await self.ctx.sample({
                "action": "write_file",
                "path": path,
                "content": content,
                "description": f"Write content to file: {path}"
            })  # type: ignore[arg-type]

            # Parse the result from ctx.sample
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {result}")
                    return False

            success_val = result.get("success", result.get("written", False))  # type: ignore[union-attr]
            return success_val

        except Exception as e:
            await self.ctx.error(f"Error writing file {path}: {str(e)}")
            return False

    async def directory_exists(self, path: str) -> bool:
        """Check if directory exists on client filesystem using Context"""
        try:
            result = await self.ctx.sample({
                "action": "check_directory_exists",
                "path": path,
                "description": f"Check if directory exists: {path}"
            })  # type: ignore[arg-type]

            # Parse the result from ctx.sample
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {result}")
                    return False

            exists_val = result.get("exists", False)  # type: ignore[union-attr]
            return exists_val

        except Exception as e:
            await self.ctx.error(f"Error checking if directory exists {path}: {str(e)}")
            return False