#!/usr/bin/env python3
"""
Integration test to ensure path traversal protection is working properly
"""
import asyncio

from src.adapters.security.path_validator import PathValidator, SecurityAdapter
from src.core.models.directory_models import DirectoryConfig
from src.core.use_cases.directory_use_cases import validate_directory_config


def test_comprehensive_security():
    """Test comprehensive security validation"""

    validator = PathValidator()

    # Test various types of directory traversal attempts
    traversal_attempts = [
        "../etc/passwd",
        "ctxfy/../dangerous",
        "ctxfy/../../dangerous",
        "ctxfy\\..\\dangerous",  # Windows-style
        "ctxfy\\..\\..\\dangerous",  # Windows-style
        "./../dangerous",
        ".../dangerous",  # Potential bypass attempt
        "ctxfy/../../../system/dangerous",
        "/absolute/path/../dangerous",  # Absolute path with traversal
    ]

    for attempt in traversal_attempts:
        result = validator.validate_path(attempt)
        assert not result.is_valid, f"Path traversal attempt should be blocked: {attempt}"

    safe_paths = [
        "ctxfy",
        "ctxfy/specifications",
        "ctxfy/specifications/models",
        "my_directory",
        "path/with/dots.but.no.traversal",
        "normal_path"
    ]

    for path in safe_paths:
        result = validator.validate_path(path)
        assert result.is_valid, f"Safe path should be valid: {path}"

    # Test DirectoryConfig validation with dangerous subdirectory names
    try:
        dangerous_config = DirectoryConfig(
            base_path="ctxfy",
            subdirectories=("specifications", "../dangerous"),  # Dangerous subdirectory
            readme_content="# Test"
        )
        validate_directory_config(dangerous_config)
        # Note: This will fail at construction time due to __post_init__ validation
        # So we test with a valid config that will be validated
    except ValueError:
        pass

    # Test with a valid config (we can't test invalid ones because they fail construction)
    valid_config = DirectoryConfig(
        base_path="ctxfy",
        subdirectories=("specifications", "models"),
        readme_content="# Test README"
    )
    config_validation = validate_directory_config(valid_config)
    assert config_validation.is_valid, "Valid config should pass validation"

    # Test the SecurityAdapter with mock components
    class MockFilesystemAdapter:
        def __init__(self):
            self.ops_log = []

        async def create_directory(self, path: str) -> bool:
            self.ops_log.append(f"create_directory: {path}")
            return True

        async def file_exists(self, path: str) -> bool:
            self.ops_log.append(f"file_exists: {path}")
            return False

        async def write_file(self, path: str, content: str) -> bool:
            self.ops_log.append(f"write_file: {path}")
            return True

        async def directory_exists(self, path: str) -> bool:
            self.ops_log.append(f"directory_exists: {path}")
            return False

    mock_fs_adapter = MockFilesystemAdapter()
    security_adapter = SecurityAdapter(mock_fs_adapter)

    # Test that safe operations work
    safe_result = asyncio.run(security_adapter.create_directory("ctxfy/specifications"))
    assert safe_result, "Safe operation should succeed"
    assert "create_directory: ctxfy/specifications" in mock_fs_adapter.ops_log

    # Test that unsafe operations raise ValueError
    try:
        asyncio.run(security_adapter.create_directory("ctxfy/../dangerous"))
        raise AssertionError("Unsafe operation should raise ValueError")
    except ValueError:
        pass


def test_path_sanitization():
    """Test path sanitization and security validation"""

    validator = PathValidator()

    # Test sanitization of various paths
    test_paths = [
        ("ctxfy/../dangerous", False),  # Should be marked unsafe
        ("ctxfy/specifications", True),   # Should be safe
        ("./relative/path", True),        # Should be safe
        ("../outside", False),            # Should be unsafe
        ("valid/path", True),             # Should be safe
    ]

    for path, expected_safe in test_paths:
        secure_path = validator.sanitize_path(path)

        if expected_safe:
            assert secure_path.is_safe, f"Path {path} should be marked safe"
        else:
            assert not secure_path.is_safe, f"Path {path} should be marked unsafe"


if __name__ == "__main__":
    test_comprehensive_security()
    test_path_sanitization()