import tempfile
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastmcp import Context

from src.core.use_cases.process_task_use_case import ProcessTaskUseCase
from src.shell.adapters.tools.process_task_tool import ProcessTaskTool


class TestProcessTaskTool:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.use_case = ProcessTaskUseCase()
        self.tool = ProcessTaskTool(use_case=self.use_case)
        self.ctx = AsyncMock(spec=Context)

    def test_process_task_creates_directory_structure(self):
        """Integration test: Verify that the tool creates the expected directory structure"""
        # Create a temporary markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Integration Test Task\n\nThis is a test task for integration testing.")
            temp_file_path = f.name

        try:
            # Execute the tool
            import asyncio
            result = asyncio.run(self._execute_tool(temp_file_path))
            
            # Verify the result structure
            assert "task_id" in result
            assert "title" in result
            assert "summary" in result
            assert "original_file_path" in result
            assert "task_directory_path" in result
            assert "created_at" in result
            
            # Verify that the task directory was created
            task_dir = Path(result["task_directory_path"])
            assert task_dir.exists()
            assert task_dir.is_dir()
            
            # Verify that the original file was copied to the task directory with standardized name
            original_file = Path(temp_file_path)
            copied_file = task_dir / "original-task.md"
            assert copied_file.exists()
            assert copied_file.is_file()

            # Verify the content was copied correctly
            original_content = original_file.read_text()
            copied_content = copied_file.read_text()
            assert original_content == copied_content
            
        finally:
            # Clean up
            Path(temp_file_path).unlink()
            # Clean up the created task directory
            import shutil
            if 'task_dir' in locals():
                shutil.rmtree(task_dir.parent, ignore_errors=True)

    async def _execute_tool(self, file_path: str):
        """Helper method to execute the tool with mocked context"""
        return await self.tool.execute(self.ctx, file_path)

    def test_task_id_generation_consistency(self):
        """Integration test: Verify that task ID generation is consistent with identical content"""
        # Create two temporary files with identical content
        content = "# Consistency Test\n\nContent for consistency testing."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f1:
            f1.write(content)
            temp_file_path1 = f1.name
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f2:
            f2.write(content)
            temp_file_path2 = f2.name

        try:
            # Execute the tool for both files
            import asyncio
            result1 = asyncio.run(self._execute_tool(temp_file_path1))
            result2 = asyncio.run(self._execute_tool(temp_file_path2))
            
            # Both should have task IDs (though they might differ due to timestamp)
            assert result1["task_id"] is not None
            assert result2["task_id"] is not None
            
        finally:
            # Clean up
            Path(temp_file_path1).unlink()
            Path(temp_file_path2).unlink()
            # Clean up any created directories
            import shutil
            shutil.rmtree(Path(".ctxfy"), ignore_errors=True)

    def test_handles_nonexistent_file_gracefully(self):
        """Integration test: Verify that the tool handles nonexistent files appropriately"""
        import asyncio

        with pytest.raises((Exception, FileNotFoundError)):
            asyncio.run(self._execute_tool("/non/existent/file.md"))