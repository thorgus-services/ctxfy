from datetime import datetime

import pytest

from src.core.models.directory_models import (
    DirectoryConfig,
    DirectoryOperation,
    DirectoryStatus,
    SecurePath,
    ValidationResult,
)
from src.core.models.filesystem_models import (
    DirectoryTraversalCheck,
    FileOperationResult,
    FilesystemOperation,
)


class TestDirectoryConfig:
    def test_directory_config_creation(self):
        """Test creating a valid DirectoryConfig"""
        config = DirectoryConfig(
            base_path="ctxfy",
            subdirectories=("specifications", "models"),
            readme_content="# Test README",
            validation_rules=("no_traversal", "valid_chars")
        )
        
        assert config.base_path == "ctxfy"
        assert config.subdirectories == ("specifications", "models")
        assert config.readme_content == "# Test README"
        assert config.validation_rules == ("no_traversal", "valid_chars")
    
    def test_directory_config_validation_empty_base_path(self):
        """Test that DirectoryConfig raises error for empty base path"""
        with pytest.raises(ValueError):
            DirectoryConfig(base_path="", subdirectories=("spec",))
    
    def test_directory_config_validation_empty_subdirectories(self):
        """Test that DirectoryConfig raises error for empty subdirectories"""
        with pytest.raises(ValueError):
            DirectoryConfig(base_path="ctxfy", subdirectories=())
    
    def test_directory_config_subdirectories_conversion(self):
        """Test that subdirectories are converted to tuple if not already"""
        config = DirectoryConfig(base_path="ctxfy", subdirectories=["spec1", "spec2"])
        assert isinstance(config.subdirectories, tuple)
        assert config.subdirectories == ("spec1", "spec2")


class TestSecurePath:
    def test_secure_path_creation(self):
        """Test creating a valid SecurePath"""
        secure_path = SecurePath(
            raw_path="ctxfy/specifications",
            sanitized_path="ctxfy/specifications",
            is_safe=True,
            validation_errors=()
        )
        
        assert secure_path.raw_path == "ctxfy/specifications"
        assert secure_path.sanitized_path == "ctxfy/specifications"
        assert secure_path.is_safe is True
        assert secure_path.validation_errors == ()
    
    def test_secure_path_validation_empty_raw_path(self):
        """Test that SecurePath raises error for empty raw path"""
        with pytest.raises(ValueError):
            SecurePath(raw_path="", sanitized_path="", is_safe=True, validation_errors=())
    
    def test_secure_path_validation_safe_without_sanitized_path(self):
        """Test that SecurePath raises error for safe path without sanitized path"""
        with pytest.raises(ValueError):
            SecurePath(raw_path="ctxfy", sanitized_path="", is_safe=True, validation_errors=())


class TestDirectoryOperation:
    def test_directory_operation_creation(self):
        """Test creating a valid DirectoryOperation"""
        operation = DirectoryOperation(
            operation_type="create",
            target_path="ctxfy/specifications",
            parameters={"mode": "0o755"}
        )
        
        assert operation.operation_type == "create"
        assert operation.target_path == "ctxfy/specifications"
        assert operation.parameters == {"mode": "0o755"}
    
    def test_directory_operation_validation_invalid_type(self):
        """Test that DirectoryOperation raises error for invalid operation type"""
        with pytest.raises(ValueError):
            DirectoryOperation(operation_type="invalid", target_path="ctxfy")


class TestDirectoryStatus:
    def test_directory_status_creation(self):
        """Test creating a valid DirectoryStatus"""
        created_at = datetime.now()
        status = DirectoryStatus(
            path="ctxfy/specifications",
            exists=True,
            permissions="0o755",
            created_at=created_at
        )
        
        assert status.path == "ctxfy/specifications"
        assert status.exists is True
        assert status.permissions == "0o755"
        assert status.created_at == created_at
    
    def test_directory_status_validation_empty_path(self):
        """Test that DirectoryStatus raises error for empty path"""
        with pytest.raises(ValueError):
            DirectoryStatus(path="", exists=False)


class TestValidationResult:
    def test_validation_result_creation_valid(self):
        """Test creating a valid ValidationResult"""
        result = ValidationResult(is_valid=True, errors=(), warnings=())
        
        assert result.is_valid is True
        assert result.errors == ()
        assert result.warnings == ()
    
    def test_validation_result_creation_invalid_with_errors(self):
        """Test creating an invalid ValidationResult with errors"""
        result = ValidationResult(
            is_valid=False, 
            errors=("Error 1", "Error 2"), 
            warnings=()
        )
        
        assert result.is_valid is False
        assert result.errors == ("Error 1", "Error 2")
    
    def test_validation_result_validation_error_with_errors_and_valid(self):
        """Test that ValidationResult raises error when valid but has errors"""
        with pytest.raises(ValueError):
            ValidationResult(is_valid=True, errors=("Error 1",), warnings=())


class TestFilesystemOperation:
    def test_filesystem_operation_creation(self):
        """Test creating a valid FilesystemOperation"""
        operation = FilesystemOperation(
            operation_type="create_dir",
            path="ctxfy/specifications",
            content="",
            metadata={"mode": "0o755"}
        )
        
        assert operation.operation_type == "create_dir"
        assert operation.path == "ctxfy/specifications"
        assert operation.content == ""
        assert operation.metadata == {"mode": "0o755"}
    
    def test_filesystem_operation_validation_invalid_type(self):
        """Test that FilesystemOperation raises error for invalid operation type"""
        with pytest.raises(ValueError):
            FilesystemOperation(operation_type="invalid", path="ctxfy")
    
    def test_filesystem_operation_validation_empty_path(self):
        """Test that FilesystemOperation raises error for empty path"""
        with pytest.raises(ValueError):
            FilesystemOperation(operation_type="create_dir", path="")


class TestFileOperationResult:
    def test_file_operation_result_creation(self):
        """Test creating a valid FileOperationResult"""
        result = FileOperationResult(
            success=True,
            path="ctxfy/specifications",
            message="Directory created successfully",
            operation_details={"mode": "0o755"}
        )
        
        assert result.success is True
        assert result.path == "ctxfy/specifications"
        assert result.message == "Directory created successfully"
        assert result.operation_details == {"mode": "0o755"}
    
    def test_file_operation_result_validation_empty_path(self):
        """Test that FileOperationResult raises error for empty path"""
        with pytest.raises(ValueError):
            FileOperationResult(success=True, path="", message="Test")
    
    def test_file_operation_result_validation_invalid_success_type(self):
        """Test that FileOperationResult raises error for non-boolean success"""
        with pytest.raises(ValueError):
            FileOperationResult(success="true", path="ctxfy", message="Test")


class TestDirectoryTraversalCheck:
    def test_directory_traversal_check_creation(self):
        """Test creating a valid DirectoryTraversalCheck"""
        check = DirectoryTraversalCheck(
            is_safe=True,
            safe_path="ctxfy/specifications",
            original_path="ctxfy/specifications",
            violations=()
        )
        
        assert check.is_safe is True
        assert check.safe_path == "ctxfy/specifications"
        assert check.original_path == "ctxfy/specifications"
        assert check.violations == ()
    
    def test_directory_traversal_check_validation_invalid_is_safe_type(self):
        """Test that DirectoryTraversalCheck raises error for non-boolean is_safe"""
        with pytest.raises(ValueError):
            DirectoryTraversalCheck(
                is_safe="true",  # Should be boolean
                safe_path="ctxfy",
                original_path="ctxfy",
                violations=()
            )
    
    def test_directory_traversal_check_validation_empty_original_path(self):
        """Test that DirectoryTraversalCheck raises error for empty original path"""
        with pytest.raises(ValueError):
            DirectoryTraversalCheck(
                is_safe=True,
                safe_path="",
                original_path="",
                violations=()
            )