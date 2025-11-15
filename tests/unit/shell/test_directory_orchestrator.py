import pytest

from src.core.models.directory_models import DirectoryConfig
from src.shell.orchestrators.directory_orchestrator import DirectoryOrchestrator
from tests.conftest import MockContext


class MockFilesystemAdapter:
    """Mock filesystem adapter for testing"""

    def __init__(self):
        self.created_directories = []
        self.written_files = []

    async def create_directory(self, path: str) -> bool:
        self.created_directories.append(path)
        return True

    async def file_exists(self, path: str) -> bool:
        return path in [f[0] for f in self.written_files]

    async def write_file(self, path: str, content: str) -> bool:
        self.written_files.append((path, content))
        return True

    async def directory_exists(self, path: str) -> bool:
        return path in self.created_directories


class TestDirectoryOrchestrator:
    @pytest.fixture
    def mock_context(self):
        return MockContext()

    @pytest.fixture
    def mock_filesystem_adapter(self):
        return MockFilesystemAdapter()

    @pytest.fixture
    def orchestrator(self, mock_context, mock_filesystem_adapter):
        return DirectoryOrchestrator(mock_context, mock_filesystem_adapter)

    @pytest.mark.asyncio
    async def test_ensure_directories_exist_success(self, orchestrator, mock_context):
        """Test successful directory creation"""
        config = DirectoryConfig(
            base_path="ctxfy",
            subdirectories=("specifications",),
            readme_content="# Test README"
        )

        result = await orchestrator.ensure_directories_exist(config)

        assert result is True
        assert len(mock_context.log_entries) == 0  # No errors logged

    @pytest.mark.asyncio
    async def test_create_readme_success(self, orchestrator, mock_context):
        """Test successful README creation"""
        result = await orchestrator.create_readme("# Test README", "ctxfy")

        assert result is True
        assert len(mock_context.log_entries) == 0  # No errors logged

    @pytest.mark.asyncio
    async def test_ensure_directories_exist_filesystem_failure(self):
        """Test directory creation fails when filesystem operations fail"""
        # Create a mock context that will return failure
        failing_context = MockContext(fail_operations=True)

        # Create a mock filesystem adapter (though it won't be used directly in current implementation)
        class MockFilesystemAdapter:
            async def create_directory(self, path: str) -> bool:
                return True

            async def file_exists(self, path: str) -> bool:
                return False

            async def write_file(self, path: str, content: str) -> bool:
                return True

            async def directory_exists(self, path: str) -> bool:
                return False

        filesystem_adapter = MockFilesystemAdapter()
        orchestrator = DirectoryOrchestrator(failing_context, filesystem_adapter)

        config = DirectoryConfig(
            base_path="ctxfy",  # Valid base path
            subdirectories=("specifications",),  # Valid subdirectories
            readme_content="# Test README"
        )

        result = await orchestrator.ensure_directories_exist(config)

        assert result is False