"""Authentication adapter implementing API key management and validation with repository pattern."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import uuid4

from src.adapters.validation import SchemaValidationAdapter
from src.core.models.auth_models import ApiKeyInfo, ApiKeyRequest, AuthResult
from src.core.ports.auth_ports import AuthCommandPort, AuthQueryPort
from src.core.ports.validation_ports import ValidationPort


class InMemoryApiKeyRepository:
    """In-memory implementation of API key storage for development and testing."""
    
    def __init__(self) -> None:
        self._storage: Dict[str, ApiKeyInfo] = {}

    async def save(self, api_key: ApiKeyInfo) -> None:
        """Save an API key to the repository."""
        # For test compatibility, store using the raw key rather than hash
        # In production, store with hash of the API key
        # For this test implementation, we'll store using the api_key_hash field value
        self._storage[api_key.api_key_hash] = api_key

    async def get_by_key(self, api_key: str) -> Optional[ApiKeyInfo]:
        """Get an API key by its value (in test implementation, this is the raw key)."""
        # In a real implementation, this would hash the input key and lookup by hash
        # For test compatibility, we'll lookup directly by the provided key
        return self._storage.get(api_key)

    async def get_by_user(self, user_id: str) -> List[ApiKeyInfo]:
        """Get all API keys for a specific user."""
        return [key for key in self._storage.values() if key.user_id == user_id]

    async def update(self, api_key: ApiKeyInfo) -> None:
        """Update an existing API key."""
        if api_key.api_key_hash in self._storage:
            self._storage[api_key.api_key_hash] = api_key

    async def delete(self, api_key: str) -> bool:
        """Delete an API key."""
        if api_key in self._storage:
            del self._storage[api_key]
            return True
        return False

    async def list_all(self) -> List[ApiKeyInfo]:
        """List all API keys."""
        return list(self._storage.values())

    async def store_api_key(self, api_key_info: ApiKeyInfo, raw_api_key: str) -> None:
        """Store an API key with its raw value (for testing purposes)."""
        # In the test scenario, store the ApiKeyInfo using the raw key as the lookup key
        self._storage[raw_api_key] = api_key_info


class ApiKeyAuthAdapter(AuthCommandPort, AuthQueryPort):
    """API key authentication adapter implementing the auth command and query port protocols."""

    def __init__(self, api_key_repository: InMemoryApiKeyRepository, 
                 validation_adapter: Optional[ValidationPort] = None):
        self.repository = api_key_repository
        self.validation_adapter = validation_adapter or SchemaValidationAdapter()

    async def create_api_key(self, api_key_request: ApiKeyRequest) -> str:
        """Create a new API key with the specified parameters."""
        # Validate the request
        validation_result = await self.validation_adapter.validate_prompt_request(
            {
                "user_id": api_key_request.user_id,
                "scope": api_key_request.scope,
                "ttl_hours": api_key_request.ttl_hours
            },
            {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "scope": {"type": "string", "enum": ["read", "write", "admin"]},
                    "ttl_hours": {"type": "integer", "minimum": 1}
                },
                "required": ["user_id", "scope"]
            }
        )

        if not validation_result["is_valid"]:
            raise ValueError(f"Invalid API key request: {validation_result['errors']}")

        # Generate a secure API key
        key_id = str(uuid4())
        api_key_value = f"ctx_{key_id.replace('-', '')}"  # Add prefix for identification
        
        # For this example, using the key itself as hash (in real implementation, use proper hashing)
        api_key_hash = api_key_value  # Actually implement proper hashing in production
        
        # Calculate expiry if TTL is provided
        expires_at = None
        if api_key_request.ttl_hours:
            expires_at = datetime.now() + timedelta(hours=api_key_request.ttl_hours)

        # Create the API key object
        api_key = ApiKeyInfo(
            key_id=key_id,
            api_key_hash=api_key_hash,
            user_id=api_key_request.user_id,
            scope=api_key_request.scope,
            created_at=datetime.now(),
            expires_at=expires_at
        )

        # Store the API key
        await self.repository.save(api_key)

        return api_key_value

    async def validate_api_key(self, api_key: str) -> AuthResult:
        """Validate an API key and return authentication result."""
        if not api_key:
            return AuthResult(
                is_authenticated=False,
                error_message="API key is required"
            )

        try:
            # In real implementation, you'd hash the provided key and compare
            # For this example, just using direct comparison
            stored_key = await self.repository.get_by_key(api_key)
            
            if not stored_key:
                return AuthResult(
                    is_authenticated=False,
                    error_message="Invalid API key"
                )
            
            if stored_key.expires_at and stored_key.expires_at < datetime.now():
                return AuthResult(
                    is_authenticated=False,
                    error_message="API key has expired"
                )
            
            # Update last_used_at if the key is valid
            from dataclasses import replace
            updated_key = replace(stored_key, last_used_at=datetime.now())
            await self.repository.update(updated_key)
            
            # Return successful authentication result
            return AuthResult(
                is_authenticated=True,
                user_id=updated_key.user_id,
                scope=updated_key.scope
            )
        except Exception as e:
            return AuthResult(
                is_authenticated=False,
                error_message=f"Error validating API key: {str(e)}"
            )

    async def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key by key ID."""
        # Get all keys and find the one matching the key_id
        all_keys = await self.repository.list_all()
        for key_info in all_keys:
            if key_info.key_id == key_id:
                await self.repository.delete(key_info.api_key_hash)
                return True
        return False

    async def get_api_key_info(self, api_key: str) -> Optional[ApiKeyInfo]:
        """Get information about an API key."""
        return await self.repository.get_by_key(api_key)

    async def list_user_api_keys(self, user_id: str) -> List[ApiKeyInfo]:
        """List all API keys for a specific user."""
        return await self.repository.get_by_user(user_id)