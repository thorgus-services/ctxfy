from abc import abstractmethod
from typing import Protocol


class ClientFilesystemPort(Protocol):
    """Secondary port for client-side filesystem operations"""

    @abstractmethod
    async def create_directory(self, path: str) -> bool:
        """Create directory on client filesystem using Context"""
        ...

    @abstractmethod
    async def file_exists(self, path: str) -> bool:
        """Check if file exists on client filesystem using Context"""
        ...

    @abstractmethod
    async def write_file(self, path: str, content: str) -> bool:
        """Write content to file on client filesystem using Context"""
        ...

    @abstractmethod
    async def directory_exists(self, path: str) -> bool:
        """Check if directory exists on client filesystem using Context"""
        ...