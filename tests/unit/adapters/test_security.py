import pytest

from src.adapters.security.path_validator import PathValidator, SecurityAdapter


class MockFilesystemAdapter:
    """Mock filesystem adapter for testing"""
    
    def __init__(self):
        self.created_directories = []
        self.written_files = []
        self.checked_files = []
        self.checked_directories = []
    
    async def create_directory(self, path: str) -> bool:
        self.created_directories.append(path)
        return True
    
    async def file_exists(self, path: str) -> bool:
        self.checked_files.append(path)
        return path in [f[0] for f in self.written_files]
    
    async def write_file(self, path: str, content: str) -> bool:
        self.written_files.append((path, content))
        return True
    
    async def directory_exists(self, path: str) -> bool:
        self.checked_directories.append(path)
        return path in self.created_directories


class TestPathValidator:
    @pytest.fixture
    def path_validator(self):
        return PathValidator()
    
    def test_validate_path_safe_path(self, path_validator):
        """Test validation passes for a safe path"""
        result = path_validator.validate_path("ctxfy/specifications")
        
        assert result.is_valid is True
        assert result.errors == ()
    
    def test_validate_path_directory_traversal(self, path_validator):
        """Test validation fails for directory traversal"""
        result = path_validator.validate_path("ctxfy/../dangerous")
        
        assert result.is_valid is False
        assert any("traversal" in error.lower() for error in result.errors)
    
    def test_sanitize_path_safe(self, path_validator):
        """Test sanitizing a safe path"""
        secure_path = path_validator.sanitize_path("ctxfy/specifications")
        
        assert secure_path.is_safe is True
        assert secure_path.raw_path == "ctxfy/specifications"
        assert secure_path.sanitized_path == "ctxfy/specifications"
    
    def test_sanitize_path_unsafe(self, path_validator):
        """Test sanitizing an unsafe path"""
        secure_path = path_validator.sanitize_path("ctxfy/../dangerous")
        
        assert secure_path.is_safe is False
        assert secure_path.raw_path == "ctxfy/../dangerous"
        assert "traversal" in str(secure_path.validation_errors)
    
    def test_check_directory_traversal_safe(self, path_validator):
        """Test directory traversal check for safe path"""
        check = path_validator.check_directory_traversal("ctxfy/specifications")
        
        assert check.is_safe is True
        assert check.violations == ()
    
    def test_check_directory_traversal_unsafe(self, path_validator):
        """Test directory traversal check for unsafe path"""
        check = path_validator.check_directory_traversal("ctxfy/../dangerous")
        
        assert check.is_safe is False
        assert len(check.violations) > 0


class TestSecurityAdapter:
    @pytest.fixture
    def mock_filesystem_adapter(self):
        return MockFilesystemAdapter()
    
    @pytest.fixture
    def security_adapter(self, mock_filesystem_adapter):
        return SecurityAdapter(mock_filesystem_adapter)
    
    @pytest.mark.asyncio
    async def test_create_directory_safe(self, security_adapter):
        """Test creating a safe directory"""
        result = await security_adapter.create_directory("ctxfy/specifications")
        
        assert result is True
        assert "ctxfy/specifications" in security_adapter.filesystem_adapter.created_directories
    
    @pytest.mark.asyncio
    async def test_create_directory_unsafe_raises_error(self, security_adapter):
        """Test creating an unsafe directory raises an error"""
        with pytest.raises(ValueError):
            await security_adapter.create_directory("ctxfy/../dangerous")
    
    @pytest.mark.asyncio
    async def test_write_file_safe(self, security_adapter):
        """Test writing a safe file"""
        result = await security_adapter.write_file("ctxfy/README.md", "# Test")
        
        assert result is True
        assert ("ctxfy/README.md", "# Test") in security_adapter.filesystem_adapter.written_files
    
    @pytest.mark.asyncio
    async def test_write_file_unsafe_raises_error(self, security_adapter):
        """Test writing an unsafe file path raises an error"""
        with pytest.raises(ValueError):
            await security_adapter.write_file("ctxfy/../dangerous/file.txt", "# Test")
    
    @pytest.mark.asyncio
    async def test_file_exists_safe(self, security_adapter):
        """Test checking existence of safe file"""
        # First write a file so it exists
        await security_adapter.write_file("ctxfy/README.md", "# Test")
        
        result = await security_adapter.file_exists("ctxfy/README.md")
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_file_exists_unsafe_raises_error(self, security_adapter):
        """Test checking existence of unsafe file path raises an error"""
        with pytest.raises(ValueError):
            await security_adapter.file_exists("ctxfy/../dangerous/file.txt")
    
    @pytest.mark.asyncio
    async def test_directory_exists_safe(self, security_adapter):
        """Test checking existence of safe directory"""
        # First create a directory so it exists
        await security_adapter.create_directory("ctxfy/specifications")
        
        result = await security_adapter.directory_exists("ctxfy/specifications")
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_directory_exists_unsafe_raises_error(self, security_adapter):
        """Test checking existence of unsafe directory path raises an error"""
        with pytest.raises(ValueError):
            await security_adapter.directory_exists("ctxfy/../dangerous")