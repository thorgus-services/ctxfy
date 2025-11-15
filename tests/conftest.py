import pytest

# This file can be used to add pytest configuration for the entire test suite
# Contains shared test utilities, fixtures, and common test helpers


class MockContext:
    """Mock Context for testing purposes"""

    def __init__(self, fail_operations=False):
        self.log_entries = []
        self.fail_operations = fail_operations

    async def info(self, message):
        self.log_entries.append(("info", message))

    async def warning(self, message):
        self.log_entries.append(("warning", message))

    async def error(self, message):
        self.log_entries.append(("error", message))

    async def sample(self, request):
        # Mock the sample method behavior based on the request
        if self.fail_operations:
            # Return failure for all operations if configured to do so
            if isinstance(request, dict):
                action = request.get("action", "")
                path = request.get("path", "")
                return {"success": False, "path": path, "error": "Simulated failure"}
            else:
                return {"success": False, "error": "Simulated failure"}

        if isinstance(request, dict):
            action = request.get("action", "")
            path = request.get("path", "")

            if action == "create_directory":
                return {"success": True, "path": path, "created": True}
            elif action == "write_file":
                return {"success": True, "path": path, "written": True}
            elif action == "check_file_exists":
                return {"exists": False}
            elif action == "check_directory_exists":
                return {"exists": False}

        # For string requests that follow the old format
        if "Create main directory" in str(request):
            return {"success": True, "path": "ctxfy", "created": True}
        elif "Create subdirectory" in str(request):
            return {"success": True, "path": "ctxfy/specifications", "created": True}
        elif "Create README.md" in str(request):
            return {"success": True, "path": "ctxfy/README.md", "written": True}

        return {"success": False}


@pytest.fixture
def sample_directory_config():
    """Sample DirectoryConfig for testing"""
    from src.core.models.directory_models import DirectoryConfig
    return DirectoryConfig(
        base_path="ctxfy",
        subdirectories=("specifications", "models"),
        readme_content="# Test README",
        validation_rules=("no_traversal", "valid_chars")
    )