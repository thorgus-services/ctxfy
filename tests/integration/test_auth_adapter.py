"""Integration tests for authentication adapter following TDD principles."""

from datetime import datetime, timedelta

import pytest

from src.adapters.auth import ApiKeyAuthAdapter, InMemoryApiKeyRepository
from src.core.models.auth_models import ApiKeyRequest


class TestApiKeyAuthAdapter:
    """Test the API key authentication adapter."""

    @pytest.fixture
    def auth_adapter(self):
        """Create a fresh auth adapter for each test."""
        repo = InMemoryApiKeyRepository()
        return ApiKeyAuthAdapter(repo)

    @pytest.mark.asyncio
    async def test_create_api_key(self, auth_adapter):
        """Test creating a new API key."""
        api_key_request = ApiKeyRequest(
            user_id="test-user",
            scope="read"
        )

        api_key = await auth_adapter.create_api_key(api_key_request)

        # Verify that the API key was created and is non-empty
        assert api_key is not None
        assert isinstance(api_key, str)
        assert len(api_key) > 0

    @pytest.mark.asyncio
    async def test_validate_api_key_success(self, auth_adapter):
        """Test validating a correct API key."""
        # Create an API key first
        api_key_request = ApiKeyRequest(
            user_id="test-user",
            scope="read"
        )
        api_key = await auth_adapter.create_api_key(api_key_request)

        # Validate the API key
        result = await auth_adapter.validate_api_key(api_key)

        # Verify the result
        assert result.is_authenticated is True
        assert result.user_id == "test-user"
        assert result.scope == "read"
        assert result.error_message is None

    @pytest.mark.asyncio
    async def test_validate_api_key_failure_invalid_key(self, auth_adapter):
        """Test validating an invalid API key."""
        # Try to validate a non-existent API key
        result = await auth_adapter.validate_api_key("invalid-api-key")

        # Verify the result
        assert result.is_authenticated is False
        assert result.user_id is None
        assert result.scope is None
        assert result.error_message is not None

    @pytest.mark.asyncio
    async def test_validate_api_key_failure_empty_key(self, auth_adapter):
        """Test validating an empty API key."""
        result = await auth_adapter.validate_api_key("")

        # Verify the result
        assert result.is_authenticated is False
        assert result.user_id is None
        assert result.scope is None
        assert result.error_message is not None

    @pytest.mark.asyncio
    async def test_revoke_api_key(self, auth_adapter):
        """Test revoking an API key."""
        # Create an API key first
        api_key_request = ApiKeyRequest(
            user_id="test-user",
            scope="read"
        )
        api_key = await auth_adapter.create_api_key(api_key_request)

        # Verify the key works before revocation
        result_before = await auth_adapter.validate_api_key(api_key)
        assert result_before.is_authenticated is True

        # Get the key info to find the key_id
        key_info = await auth_adapter.get_api_key_info(api_key)
        assert key_info is not None

        # Revoke the API key
        revoked = await auth_adapter.revoke_api_key(key_info.key_id)
        assert revoked is True

        # Verify the key no longer works after revocation
        result_after = await auth_adapter.validate_api_key(api_key)
        assert result_after.is_authenticated is False

    @pytest.mark.asyncio
    async def test_api_key_with_expiration(self, auth_adapter):
        """Test creating and validating an API key with expiration."""
        # Create an API key with 1 hour TTL
        api_key_request = ApiKeyRequest(
            user_id="test-user",
            scope="write",
            ttl_hours=1
        )
        api_key = await auth_adapter.create_api_key(api_key_request)

        # Verify the key works initially
        result = await auth_adapter.validate_api_key(api_key)
        assert result.is_authenticated is True
        assert result.scope == "write"

        # Get the key info to check expiration
        key_info = await auth_adapter.get_api_key_info(api_key)
        assert key_info is not None
        assert key_info.expires_at is not None

    @pytest.mark.asyncio
    async def test_expired_api_key(self, auth_adapter):
        """Test that expired API keys are rejected."""
        # Create a repository and manually insert an expired key
        repo = InMemoryApiKeyRepository()
        auth = ApiKeyAuthAdapter(repo)

        import hashlib

        from src.core.models.auth_models import ApiKeyInfo

        # Create an expired key
        raw_key = "expired-key-test"
        api_key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        expired_key_info = ApiKeyInfo(
            key_id="expired-test-key",
            api_key_hash=api_key_hash,
            user_id="test-user",
            created_at=datetime.now() - timedelta(hours=2),  # Created 2 hours ago
            expires_at=datetime.now() - timedelta(minutes=30),  # Expired 30 minutes ago
            scope="read"
        )

        await repo.store_api_key(expired_key_info, raw_key)

        # Try to validate the expired key
        result = await auth.validate_api_key(raw_key)
        assert result.is_authenticated is False
        assert "expired" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_get_api_key_info(self, auth_adapter):
        """Test retrieving API key information."""
        # Create an API key first
        api_key_request = ApiKeyRequest(
            user_id="test-user",
            scope="admin",
            ttl_hours=24
        )
        api_key = await auth_adapter.create_api_key(api_key_request)

        # Get the key info
        key_info = await auth_adapter.get_api_key_info(api_key)

        # Verify the key info
        assert key_info is not None
        assert key_info.user_id == "test-user"
        assert key_info.scope == "admin"
        assert key_info.expires_at is not None

    @pytest.mark.asyncio
    async def test_list_user_api_keys(self, auth_adapter):
        """Test listing API keys for a user."""
        # Create multiple API keys for the same user
        user_id = "test-user-multiple"
        scopes = ["read", "write", "admin"]

        created_keys = []
        for scope in scopes:
            api_key_request = ApiKeyRequest(
                user_id=user_id,
                scope=scope
            )
            api_key = await auth_adapter.create_api_key(api_key_request)
            created_keys.append(api_key)

        # List the user's API keys
        user_keys = await auth_adapter.list_user_api_keys(user_id)

        # Verify that all keys for the user were returned
        assert len(user_keys) == len(scopes)
        returned_scopes = [key.scope for key in user_keys]
        for scope in scopes:
            assert scope in returned_scopes

        # Verify that keys for a different user are not returned
        other_key_request = ApiKeyRequest(
            user_id="other-user",
            scope="read"
        )
        await auth_adapter.create_api_key(other_key_request)

        user_keys_after = await auth_adapter.list_user_api_keys(user_id)
        assert len(user_keys_after) == len(scopes)  # Should still be the same count

    @pytest.mark.asyncio
    async def test_last_used_tracking(self, auth_adapter):
        """Test that API key last used timestamp is updated on validation."""
        # Create an API key
        api_key_request = ApiKeyRequest(
            user_id="test-user",
            scope="read"
        )
        api_key = await auth_adapter.create_api_key(api_key_request)

        # Get initial key info
        initial_key_info = await auth_adapter.get_api_key_info(api_key)
        initial_last_used = initial_key_info.last_used_at

        # Validate the key (this should update last_used_at)
        result = await auth_adapter.validate_api_key(api_key)
        assert result.is_authenticated is True

        # Get key info again to check if last_used_at was updated
        updated_key_info = await auth_adapter.get_api_key_info(api_key)
        updated_last_used = updated_key_info.last_used_at

        # The last_used_at should now be set (or updated if it was already set)
        if initial_last_used is None:
            # If it was None before, it should now be set to a datetime
            assert updated_last_used is not None
        else:
            # If it wasn't None, the new value should be >= the old value
            # (allowing for potential same timestamp due to precision)
            assert updated_last_used >= initial_last_used