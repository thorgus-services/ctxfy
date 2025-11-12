"""Unit tests for authentication models following TDD principles."""

from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from src.core.models.auth_models import ApiKeyInfo, ApiKeyRequest, AuthResult


class TestApiKeyInfo:
    """Test API key info value object."""

    def test_api_key_info_creation(self):
        """Test creating a valid ApiKeyInfo."""
        now = datetime.now()
        key_info = ApiKeyInfo(
            key_id="test-key-id",
            api_key_hash="test-hash",
            user_id="test-user",
            created_at=now,
            scope="read"
        )

        assert key_info.key_id == "test-key-id"
        assert key_info.api_key_hash == "test-hash"
        assert key_info.user_id == "test-user"
        assert key_info.created_at == now
        assert key_info.scope == "read"
        assert key_info.last_used_at is None
        assert key_info.expires_at is None

    def test_api_key_info_immutable(self):
        """Test that ApiKeyInfo is immutable."""
        key_info = ApiKeyInfo(
            key_id="test-key-id",
            api_key_hash="test-hash",
            user_id="test-user",
            created_at=datetime.now(),
            scope="read"
        )

        with pytest.raises(FrozenInstanceError):
            key_info.key_id = "new-key-id"

    def test_api_key_info_validation_key_id(self):
        """Test validation of key_id."""
        with pytest.raises(ValueError):
            ApiKeyInfo(
                key_id="",  # Empty key_id should fail
                api_key_hash="test-hash",
                user_id="test-user",
                created_at=datetime.now(),
                scope="read"
            )

        with pytest.raises(ValueError):
            ApiKeyInfo(
                key_id=123,  # Non-string key_id should fail
                api_key_hash="test-hash",
                user_id="test-user",
                created_at=datetime.now(),
                scope="read"
            )

    def test_api_key_info_validation_api_key_hash(self):
        """Test validation of api_key_hash."""
        with pytest.raises(ValueError):
            ApiKeyInfo(
                key_id="test-key-id",
                api_key_hash="",  # Empty hash should fail
                user_id="test-user",
                created_at=datetime.now(),
                scope="read"
            )

        with pytest.raises(ValueError):
            ApiKeyInfo(
                key_id="test-key-id",
                api_key_hash=123,  # Non-string hash should fail
                user_id="test-user",
                created_at=datetime.now(),
                scope="read"
            )

    def test_api_key_info_validation_user_id(self):
        """Test validation of user_id."""
        with pytest.raises(ValueError):
            ApiKeyInfo(
                key_id="test-key-id",
                api_key_hash="test-hash",
                user_id="",  # Empty user_id should fail
                created_at=datetime.now(),
                scope="read"
            )

        with pytest.raises(ValueError):
            ApiKeyInfo(
                key_id="test-key-id",
                api_key_hash="test-hash",
                user_id=123,  # Non-string user_id should fail
                created_at=datetime.now(),
                scope="read"
            )

    def test_api_key_info_validation_scope(self):
        """Test validation of scope."""
        valid_scopes = ["read", "write", "admin"]
        for scope in valid_scopes:
            key_info = ApiKeyInfo(
                key_id="test-key-id",
                api_key_hash="test-hash",
                user_id="test-user",
                created_at=datetime.now(),
                scope=scope
            )
            assert key_info.scope == scope

        with pytest.raises(ValueError):
            ApiKeyInfo(
                key_id="test-key-id",
                api_key_hash="test-hash",
                user_id="test-user",
                created_at=datetime.now(),
                scope="invalid-scope"  # Invalid scope should fail
            )


class TestApiKeyRequest:
    """Test API key request value object."""

    def test_api_key_request_creation(self):
        """Test creating a valid ApiKeyRequest."""
        request = ApiKeyRequest(
            user_id="test-user",
            scope="read",
            ttl_hours=24
        )

        assert request.user_id == "test-user"
        assert request.scope == "read"
        assert request.ttl_hours == 24
        assert isinstance(request.request_id, str)
        assert len(request.request_id) > 0

    def test_api_key_request_optional_ttl(self):
        """Test creating a ApiKeyRequest with optional ttl_hours."""
        request = ApiKeyRequest(
            user_id="test-user",
            scope="write"
            # ttl_hours is optional and defaults to None
        )

        assert request.user_id == "test-user"
        assert request.scope == "write"
        assert request.ttl_hours is None

    def test_api_key_request_immutable(self):
        """Test that ApiKeyRequest is immutable."""
        request = ApiKeyRequest(
            user_id="test-user",
            scope="read"
        )

        with pytest.raises(FrozenInstanceError):
            request.user_id = "new-user"

    def test_api_key_request_validation_user_id(self):
        """Test validation of user_id."""
        with pytest.raises(ValueError):
            ApiKeyRequest(
                user_id="",  # Empty user_id should fail
                scope="read"
            )

        with pytest.raises(ValueError):
            ApiKeyRequest(
                user_id=123,  # Non-string user_id should fail
                scope="read"
            )

    def test_api_key_request_validation_scope(self):
        """Test validation of scope."""
        with pytest.raises(ValueError):
            ApiKeyRequest(
                user_id="test-user",
                scope="invalid-scope"  # Invalid scope should fail
            )

    def test_api_key_request_validation_ttl_hours(self):
        """Test validation of ttl_hours."""
        # Valid positive TTL
        request = ApiKeyRequest(
            user_id="test-user",
            scope="read",
            ttl_hours=1  # Valid positive number
        )
        assert request.ttl_hours == 1

        # Invalid zero TTL
        with pytest.raises(ValueError):
            ApiKeyRequest(
                user_id="test-user",
                scope="read",
                ttl_hours=0  # Zero should fail
            )

        # Invalid negative TTL
        with pytest.raises(ValueError):
            ApiKeyRequest(
                user_id="test-user",
                scope="read",
                ttl_hours=-1  # Negative should fail
            )

        # Valid None TTL (should not raise error)
        request_none = ApiKeyRequest(
            user_id="test-user",
            scope="read",
            ttl_hours=None
        )
        assert request_none.ttl_hours is None


class TestAuthResult:
    """Test authentication result value object."""

    def test_auth_result_creation_success(self):
        """Test creating a successful AuthResult."""
        result = AuthResult(
            is_authenticated=True,
            user_id="test-user",
            scope="read",
            request_id="test-request-id"
        )

        assert result.is_authenticated is True
        assert result.user_id == "test-user"
        assert result.scope == "read"
        assert result.error_message is None
        assert result.request_id == "test-request-id"

    def test_auth_result_creation_failure(self):
        """Test creating a failed AuthResult."""
        result = AuthResult(
            is_authenticated=False,
            error_message="Invalid credentials",
            request_id="test-request-id"
        )

        assert result.is_authenticated is False
        assert result.user_id is None
        assert result.scope is None
        assert result.error_message == "Invalid credentials"
        assert result.request_id == "test-request-id"

    def test_auth_result_immutable(self):
        """Test that AuthResult is immutable."""
        result = AuthResult(is_authenticated=True)

        with pytest.raises(FrozenInstanceError):
            result.is_authenticated = False

    def test_auth_result_validation_is_authenticated(self):
        """Test validation of is_authenticated."""
        with pytest.raises(ValueError):
            AuthResult(
                is_authenticated="true"  # String instead of boolean should fail
            )

        with pytest.raises(ValueError):
            AuthResult(
                is_authenticated=1  # Integer instead of boolean should fail
            )

    def test_auth_result_validation_scope(self):
        """Test validation of scope."""
        # Valid scopes
        for scope in ["read", "write", "admin"]:
            result = AuthResult(
                is_authenticated=True,
                scope=scope
            )
            assert result.scope == scope

        # No scope (valid)
        result = AuthResult(is_authenticated=True)
        assert result.scope is None

        # Invalid scope when provided
        with pytest.raises(ValueError):
            AuthResult(
                is_authenticated=True,
                scope="invalid-scope"  # Invalid scope should fail
            )

    def test_auth_result_validation_request_id(self):
        """Test validation of request_id."""
        with pytest.raises(ValueError):
            AuthResult(
                is_authenticated=True,
                request_id=""  # Empty request_id should fail
            )

        with pytest.raises(ValueError):
            AuthResult(
                is_authenticated=True,
                request_id=123  # Non-string request_id should fail
            )