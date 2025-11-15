from src.core.models.directory_models import DirectoryConfig
from src.core.use_cases.directory_use_cases import (
    build_directory_operation,
    check_directory_traversal,
    generate_default_readme,
    validate_directory_config,
    validate_path_security,
)


class TestValidateDirectoryConfig:
    def test_validate_directory_config_valid(self):
        """Test validation of a valid DirectoryConfig"""
        config = DirectoryConfig(
            base_path="ctxfy",
            subdirectories=("specifications",),
            readme_content="# Test README"
        )

        result = validate_directory_config(config)

        assert result.is_valid is True
        assert result.errors == ()

    def test_validate_directory_config_invalid_subdirectory_chars(self):
        """Test validation fails for invalid characters in subdirectory names"""
        # Create a config with a valid base path but invalid subdirectory
        config = DirectoryConfig(
            base_path="ctxfy",
            subdirectories=("specifications", "../dangerous"),
            readme_content="# Test README"
        )

        result = validate_directory_config(config)

        assert result.is_valid is False
        assert any("Invalid character" in error for error in result.errors)


class TestGenerateDefaultReadme:
    def test_generate_default_readme(self):
        """Test generating default README content"""
        config = DirectoryConfig(
            base_path="ctxfy",
            subdirectories=("specifications", "models"),
            readme_content=""
        )
        
        readme_content = generate_default_readme(config)
        
        assert "# ctxfy/ Directory" in readme_content
        assert "ctxfy/" in readme_content
        assert "ctxfy/specifications/" in readme_content
        assert "Server" in readme_content
        assert "Client" in readme_content
        assert "Security Notice" in readme_content


class TestBuildDirectoryOperation:
    def test_build_directory_operation(self):
        """Test building a directory operation"""
        operation = build_directory_operation("ctxfy/specifications", "create")
        
        assert operation.operation_type == "create"
        assert operation.target_path == "ctxfy/specifications"


class TestValidatePathSecurity:
    def test_validate_path_security_safe_path(self):
        """Test validation passes for a safe path"""
        result = validate_path_security("ctxfy/specifications")
        
        assert result.is_valid is True
        assert result.errors == ()
    
    def test_validate_path_security_directory_traversal(self):
        """Test validation fails for directory traversal attempt"""
        result = validate_path_security("ctxfy/../dangerous")
        
        assert result.is_valid is False
        assert any("Directory traversal" in error for error in result.errors)


class TestCheckDirectoryTraversal:
    def test_check_directory_traversal_safe_path(self):
        """Test directory traversal check passes for safe path"""
        check = check_directory_traversal("ctxfy/specifications")
        
        assert check.is_safe is True
        assert check.violations == ()
        assert check.original_path == "ctxfy/specifications"
    
    def test_check_directory_traversal_unsafe_path(self):
        """Test directory traversal check fails for unsafe path"""
        check = check_directory_traversal("ctxfy/../dangerous")
        
        assert check.is_safe is False
        assert len(check.violations) > 0
        assert check.original_path == "ctxfy/../dangerous"