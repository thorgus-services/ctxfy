from unittest.mock import AsyncMock, Mock

import pytest

from src.adapters.auth import ApiKeyAuthAdapter
from src.adapters.auth.middleware import AuthMiddleware
from src.core.models.auth_models import AuthResult


class TestAuthMiddleware:
    """Tests for AuthMiddleware class."""

    def test_init_with_auth_adapter(self):
        """Test initializing AuthMiddleware with an auth adapter."""
        mock_auth_adapter = Mock(spec=ApiKeyAuthAdapter)
        middleware = AuthMiddleware(mock_auth_adapter)
        
        assert middleware.auth_adapter is mock_auth_adapter

    @pytest.mark.asyncio
    async def test_authenticate_request_with_valid_api_key(self):
        """Test authenticate_request with a valid API key."""
        # Create mocks
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=True,
            user_id="user123",
            scope="read",
            request_id="req123"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        mock_ctx = Mock()
        mock_ctx.headers = {"authorization": "Bearer valid_key_123"}
        mock_next_handler = AsyncMock(return_value="handler_response")
        
        # Call the method
        result = await middleware.authenticate_request(mock_ctx, mock_next_handler)
        
        # Verify calls and result
        mock_auth_adapter.validate_api_key.assert_called_once_with("valid_key_123")
        mock_next_handler.assert_called_once_with(mock_ctx)
        assert result == "handler_response"

    @pytest.mark.asyncio
    async def test_authenticate_request_with_x_api_key_header(self):
        """Test authenticate_request with x-api-key header."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=True,
            user_id="user123",
            scope="read",
            request_id="req123"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        mock_ctx = Mock()
        mock_ctx.headers = {"x-api-key": "valid_key_456"}
        mock_next_handler = AsyncMock(return_value="handler_response")
        
        result = await middleware.authenticate_request(mock_ctx, mock_next_handler)
        
        mock_auth_adapter.validate_api_key.assert_called_once_with("valid_key_456")
        assert result == "handler_response"

    @pytest.mark.asyncio
    async def test_authenticate_request_with_api_key_header(self):
        """Test authenticate_request with api-key header."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=True,
            user_id="user123",
            scope="read",
            request_id="req123"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        mock_ctx = Mock()
        mock_ctx.headers = {"api-key": "valid_key_789"}
        mock_next_handler = AsyncMock(return_value="handler_response")
        
        result = await middleware.authenticate_request(mock_ctx, mock_next_handler)
        
        mock_auth_adapter.validate_api_key.assert_called_once_with("valid_key_789")
        assert result == "handler_response"

    @pytest.mark.asyncio
    async def test_authenticate_request_with_invalid_api_key(self):
        """Test authenticate_request with an invalid API key."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=False,
            user_id=None,
            scope=None,  # Use None instead of empty string
            request_id="req123",
            error_message="Invalid API key"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        mock_ctx = Mock()
        mock_ctx.headers = {"authorization": "Bearer invalid_key"}
        mock_next_handler = AsyncMock()
        
        result = await middleware.authenticate_request(mock_ctx, mock_next_handler)
        
        mock_auth_adapter.validate_api_key.assert_called_once_with("invalid_key")
        # The next handler should NOT be called for invalid keys
        mock_next_handler.assert_not_called()
        
        # Check error response
        assert result["error"] == "Authentication failed"
        assert result["message"] == "Invalid API key"

    @pytest.mark.asyncio
    async def test_authenticate_request_with_missing_api_key(self):
        """Test authenticate_request with missing API key."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=False,
            user_id=None,
            scope=None,  # Use None instead of empty string
            request_id="req123",
            error_message="API key required"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        mock_ctx = Mock()
        mock_ctx.headers = {}  # No headers
        mock_next_handler = AsyncMock()
        
        result = await middleware.authenticate_request(mock_ctx, mock_next_handler)
        
        # Should validate with empty string when no key found
        mock_auth_adapter.validate_api_key.assert_called_once_with("")
        mock_next_handler.assert_not_called()
        
        # Check error response
        assert result["error"] == "Authentication failed"
        assert result["message"] == "API key required"

    @pytest.mark.asyncio
    async def test_authenticate_request_with_context_without_headers(self):
        """Test authenticate_request when context doesn't have headers attribute."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=False,
            user_id=None,
            scope=None,  # Use None instead of empty string
            request_id="req123"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        mock_ctx = Mock()
        # Remove headers attribute
        del mock_ctx.headers
        mock_next_handler = AsyncMock()
        
        result = await middleware.authenticate_request(mock_ctx, mock_next_handler)
        
        # Should validate with empty string when no headers attribute
        mock_auth_adapter.validate_api_key.assert_called_once_with("")
        mock_next_handler.assert_not_called()
        
        # Check error response
        assert result["error"] == "Authentication failed"
        assert result["message"] == "Invalid or missing API key"

    @pytest.mark.asyncio
    async def test_create_auth_decorator_with_valid_key_and_correct_scope(self):
        """Test create_auth_decorator with valid key and correct scope."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=True,
            user_id="user123",
            scope="read",
            request_id="req123"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        auth_decorator = middleware.create_auth_decorator(required_scope="read")
        
        # Create a mock handler function
        mock_handler = AsyncMock(return_value="handler_result")
        decorated_handler = await auth_decorator(mock_handler)
        
        mock_ctx = Mock()
        mock_ctx.headers = {"authorization": "Bearer valid_key"}
        
        result = await decorated_handler(mock_ctx)
        
        mock_auth_adapter.validate_api_key.assert_called_once_with("valid_key")
        mock_handler.assert_called_once_with(mock_ctx)
        assert result == "handler_result"

    @pytest.mark.asyncio
    async def test_create_auth_decorator_with_admin_scope(self):
        """Test create_auth_decorator with admin scope (admin has all permissions)."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=True,
            user_id="admin123",
            scope="admin",
            request_id="req123"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        auth_decorator = middleware.create_auth_decorator(required_scope="write")
        
        mock_handler = AsyncMock(return_value="admin_result")
        decorated_handler = await auth_decorator(mock_handler)
        
        mock_ctx = Mock()
        mock_ctx.headers = {"authorization": "Bearer admin_key"}
        
        result = await decorated_handler(mock_ctx)
        
        mock_handler.assert_called_once_with(mock_ctx)
        assert result == "admin_result"

    @pytest.mark.asyncio
    async def test_create_auth_decorator_with_invalid_scope(self):
        """Test create_auth_decorator with invalid scope."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=True,
            user_id="user123",
            scope="read",
            request_id="req123"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        auth_decorator = middleware.create_auth_decorator(required_scope="write")
        
        mock_handler = AsyncMock()
        decorated_handler = await auth_decorator(mock_handler)
        
        mock_ctx = Mock()
        mock_ctx.headers = {"authorization": "Bearer valid_key"}
        
        result = await decorated_handler(mock_ctx)
        
        # Handler should not be called due to insufficient permissions
        mock_handler.assert_not_called()
        
        # Check error response
        assert result["error"] == "Insufficient permissions"
        assert "write" in result["message"]
        assert "read" in result["message"]

    @pytest.mark.asyncio
    async def test_create_auth_decorator_with_invalid_api_key(self):
        """Test create_auth_decorator with invalid API key."""
        mock_auth_adapter = AsyncMock(spec=ApiKeyAuthAdapter)
        mock_auth_result = AuthResult(
            is_authenticated=False,
            user_id=None,
            scope=None,  # Use None instead of empty string
            request_id="req123",
            error_message="Invalid key"
        )
        mock_auth_adapter.validate_api_key.return_value = mock_auth_result
        
        middleware = AuthMiddleware(mock_auth_adapter)
        auth_decorator = middleware.create_auth_decorator(required_scope="read")
        
        mock_handler = AsyncMock()
        decorated_handler = await auth_decorator(mock_handler)
        
        mock_ctx = Mock()
        mock_ctx.headers = {"authorization": "Bearer invalid_key"}
        
        result = await decorated_handler(mock_ctx)
        
        # Handler should not be called due to auth failure
        mock_handler.assert_not_called()
        
        # Check error response
        assert result["error"] == "Authentication failed"
        assert result["message"] == "Invalid key"