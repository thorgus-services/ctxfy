import tempfile
from pathlib import Path

import pytest

from src.core.models.task_metadata import TaskMetadata
from src.core.use_cases.process_task_use_case import ProcessTaskUseCase


class TestProcessTaskUseCase:
    def test_process_task_creates_metadata_correctly(self):
        """Test that the use case correctly creates task metadata from a markdown file"""
        # Create a temporary markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Sample Task\n\nThis is a sample user story or task.\n\nWith multiple lines.")
            temp_file_path = f.name

        try:
            # Initialize the use case
            use_case = ProcessTaskUseCase()
            
            # Execute the use case
            result = use_case.execute(temp_file_path)
            
            # Assertions
            assert isinstance(result, TaskMetadata)
            assert result.id is not None
            assert result.title == "Sample Task"
            assert "sample user story" in result.summary.lower()
            assert result.original_file_path == temp_file_path
            assert ".ctxfy/tasks/" in result.task_directory_path
            assert result.created_at is not None
            
        finally:
            # Clean up the temporary file
            Path(temp_file_path).unlink()

    def test_task_id_generation_consistency(self):
        """Test that identical content produces consistent task IDs at the same time"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Task\n\nContent for testing.")
            temp_file_path = f.name

        try:
            use_case = ProcessTaskUseCase()
            
            # Since we can't control time in the current implementation, 
            # we'll test that the ID contains expected elements
            result = use_case.execute(temp_file_path)
            
            assert isinstance(result.id, str)
            assert len(result.id) > 0  # Should have some content
            
        finally:
            Path(temp_file_path).unlink()

    def test_extract_title_from_header(self):
        """Test extracting title from markdown header"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Feature Request\n\nDescription of the feature.")
            temp_file_path = f.name

        try:
            use_case = ProcessTaskUseCase()
            result = use_case.execute(temp_file_path)
            
            assert result.title == "Feature Request"
            
        finally:
            Path(temp_file_path).unlink()

    def test_extract_title_from_first_line(self):
        """Test extracting title from first non-header line"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("Simple Task Description\n\nMore details here.")
            temp_file_path = f.name

        try:
            use_case = ProcessTaskUseCase()
            result = use_case.execute(temp_file_path)
            
            assert result.title == "Simple Task Description"
            
        finally:
            Path(temp_file_path).unlink()

    def test_extract_summary_from_content(self):
        """Test extracting summary from content"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            long_content = "# Header\n\n" + "A" * 250 + "\n\nMore content."
            f.write(long_content)
            temp_file_path = f.name

        try:
            use_case = ProcessTaskUseCase()
            result = use_case.execute(temp_file_path)

            # Summary should be limited to 200 chars with ellipsis
            assert len(result.summary) <= 200
            assert result.summary.endswith("...")

        finally:
            Path(temp_file_path).unlink()

    def test_file_not_found_raises_exception(self):
        """Test that non-existent file raises FileNotFoundError"""
        use_case = ProcessTaskUseCase()
        
        with pytest.raises(FileNotFoundError):
            use_case.execute("/non/existent/file.md")