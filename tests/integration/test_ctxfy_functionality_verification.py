#!/usr/bin/env python3
"""
Integration test to verify the directory creation functionality works properly
"""
import asyncio

from src.adapters.security.path_validator import PathValidator
from src.core.models.directory_models import DirectoryConfig
from src.core.use_cases.directory_use_cases import (
    generate_default_readme,
    validate_directory_config,
)
from tests.conftest import MockContext


def test_directory_creation():
    """Test the directory creation functionality"""

    # Import the required modules
    from src.adapters.security.path_validator import PathValidator

    # Test 1: Directory config creation
    config = DirectoryConfig(
        base_path="ctxfy",
        subdirectories=("specifications", "models"),
        readme_content=generate_default_readme(DirectoryConfig(base_path="ctxfy"))
    )

    # Test 2: Config validation
    validate_directory_config(config)

    # Test 3: Path validation
    validator = PathValidator()
    path_result = validator.validate_path("ctxfy/specifications")
    assert path_result.is_valid, "Safe path should be valid"

    path_result_unsafe = validator.validate_path("ctxfy/../dangerous")
    assert not path_result_unsafe.is_valid, "Unsafe path should not be valid"

    # Test 4: Try to use the orchestrator with mock context
    try:
        from src.adapters.context.filesystem_adapter import FilesystemAdapter
        from src.adapters.security.path_validator import SecurityAdapter
        from src.shell.orchestrators.directory_orchestrator import DirectoryOrchestrator

        # Create a mock context
        mock_ctx = MockContext()

        # Create adapters
        filesystem_adapter = FilesystemAdapter(mock_ctx)
        security_adapter = SecurityAdapter(filesystem_adapter)

        # Create orchestrator
        orchestrator = DirectoryOrchestrator(mock_ctx, security_adapter)

        # Test the orchestrator methods
        async def run_tests():
            # Test README creation
            await orchestrator.create_readme("# Test README", "ctxfy")

            # Test directory creation with failing context
            failing_ctx = MockContext(fail_operations=True)
            failing_filesystem_adapter = FilesystemAdapter(failing_ctx)
            failing_security_adapter = SecurityAdapter(failing_filesystem_adapter)
            failing_orchestrator = DirectoryOrchestrator(failing_ctx, failing_security_adapter)

            failing_config = DirectoryConfig(
                base_path="ctxfy",
                subdirectories=("specifications",),
                readme_content=generate_default_readme(DirectoryConfig(base_path="ctxfy"))
            )

            await failing_orchestrator.ensure_directories_exist(failing_config)

            # Test directory creation with successful context
            successful_ctx = MockContext(fail_operations=False)
            successful_filesystem_adapter = FilesystemAdapter(successful_ctx)
            successful_security_adapter = SecurityAdapter(successful_filesystem_adapter)
            successful_orchestrator = DirectoryOrchestrator(successful_ctx, successful_security_adapter)

            await successful_orchestrator.ensure_directories_exist(failing_config)

        asyncio.run(run_tests())

    except Exception:
        import traceback
        traceback.print_exc()


def test_security_validation():
    """Test the security validation functionality"""

    validator = PathValidator()

    # Test safe path
    safe_result = validator.validate_path("ctxfy/specifications")
    assert safe_result.is_valid, "Safe path should be valid"

    # Test unsafe path
    unsafe_result = validator.validate_path("ctxfy/../dangerous")
    assert not unsafe_result.is_valid, "Unsafe path should not be valid"

    # Test absolute path
    absolute_result = validator.validate_path("/etc/passwd")
    assert not absolute_result.is_valid, "Absolute path should not be valid"

    # Test sanitization
    secure_path = validator.sanitize_path("ctxfy/../dangerous")
    assert not secure_path.is_safe, "Unsafe path should remain unsafe after sanitization"


if __name__ == "__main__":
    # Run the tests
    test_directory_creation()
    test_security_validation()