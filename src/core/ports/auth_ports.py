"""Core protocols for authentication operations following our architectural patterns.

Primary ports (driving) are named with *CommandPort/*QueryPort convention.
Secondary ports (driven) are named with *GatewayPort/*RepositoryPort/*PublisherPort convention.
"""

from abc import abstractmethod
from typing import List, Optional

from src.core.models.auth_models import ApiKeyInfo, ApiKeyRequest, AuthResult


class AuthCommandPort:
    """Primary port for authentication operations - driving port following naming convention."""

    @abstractmethod
    async def validate_api_key(self, api_key: str) -> AuthResult:
        """Validate an API key and return authentication information."""
        pass

    @abstractmethod
    async def create_api_key(self, api_key_request: ApiKeyRequest) -> str:
        """Create a new API key and return the key value."""
        pass

    @abstractmethod
    async def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key by key ID."""
        pass


class AuthQueryPort:
    """Primary port for authentication information queries - driving port following naming convention."""

    @abstractmethod
    async def get_api_key_info(self, api_key: str) -> Optional[ApiKeyInfo]:
        """Get information about an API key."""
        pass

    @abstractmethod
    async def list_user_api_keys(self, user_id: str) -> List[ApiKeyInfo]:
        """List all API keys for a specific user."""
        pass