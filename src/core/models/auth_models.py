"""Immutable value objects for authentication operations following our core architecture principles."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ApiKeyInfo:
    """Immutable value object for API key information following our core architecture principles."""
    key_id: str
    api_key_hash: str  # Hashed API key for security
    user_id: str
    scope: str  # read, write, admin
    created_at: datetime
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.key_id or not isinstance(self.key_id, str):
            raise ValueError("Key ID must be a valid string")
        if not self.api_key_hash or not isinstance(self.api_key_hash, str):
            raise ValueError("API key hash must be a valid string")
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("User ID must be a valid string")
        if self.scope not in ['read', 'write', 'admin']:
            raise ValueError("Scope must be 'read', 'write', or 'admin'")


@dataclass(frozen=True)
class ApiKeyRequest:
    """Immutable value object for API key requests following our core architecture principles."""
    user_id: str
    scope: str  # read, write, admin
    ttl_hours: Optional[int] = None  # Time-to-live in hours
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("User ID must be a valid string")
        if self.scope not in ['read', 'write', 'admin']:
            raise ValueError("Scope must be 'read', 'write', or 'admin'")
        if self.ttl_hours is not None and (not isinstance(self.ttl_hours, int) or self.ttl_hours <= 0):
            raise ValueError("TTL hours must be a positive integer if provided")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")


@dataclass(frozen=True)
class AuthResult:
    """Immutable value object for authentication results following our core architecture principles."""
    is_authenticated: bool
    user_id: Optional[str] = None
    scope: Optional[str] = None  # read, write, admin
    error_message: Optional[str] = None
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        """Validate invariants immediately after construction."""
        if not isinstance(self.is_authenticated, bool):
            raise ValueError("is_authenticated must be a boolean")
        if self.scope is not None and self.scope not in ['read', 'write', 'admin']:
            raise ValueError("Scope must be 'read', 'write', or 'admin' if provided")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")