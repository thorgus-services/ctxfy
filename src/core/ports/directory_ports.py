from abc import abstractmethod
from typing import Protocol

from src.core.models.directory_models import (
    DirectoryConfig,
    DirectoryStatus,
    ValidationResult,
)


class DirectoryCommandPort(Protocol):
    """Primary port for directory management operations"""

    @abstractmethod
    async def ensure_directories_exist(self, config: DirectoryConfig) -> bool:
        """Ensure directory structure exists using Context filesystem operations"""
        ...

    @abstractmethod
    async def create_readme(self, content: str, directory_path: str) -> bool:
        """Create README file in the specified directory using Context"""
        ...


class DirectoryQueryPort(Protocol):
    """Primary port for directory information queries"""

    @abstractmethod
    async def get_directory_status(self, path: str) -> DirectoryStatus:
        """Get status of a directory using Context operations"""
        ...

    @abstractmethod
    async def validate_directory_path(self, path: str) -> ValidationResult:
        """Validate directory path safety and structure"""
        ...