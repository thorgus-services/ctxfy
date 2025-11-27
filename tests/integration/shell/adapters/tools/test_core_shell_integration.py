from datetime import datetime, timezone

import pytest

from src.core.models.specification_result import SaveDirectoryPath
from src.core.models.specification_workflow import (
    BusinessRequirements,
    SpecificationWorkflowDefinition,
)
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase
from src.core.workflows.specification_workflow import execute_specification_workflow
from src.shell.adapters.prompt_loaders.yaml_prompt_loader import YAMLPromptLoader
from src.shell.adapters.tools.specification_generation_tool import (
    SpecificationGenerationTool,
)


class TestCoreShellIntegration:
    """Integration tests for core use cases and workflows with shell adapters"""

    def test_specification_generation_use_case_with_real_timestamp_handling(self):
        """Integration test: Use case works with real timestamp flow from shell"""
        # Arrange
        use_case = GenerateSpecificationUseCase()
        created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        # Act
        result = use_case.execute(
            BusinessRequirements("Create a dashboard for user metrics"),
            created_at
        )

        # Assert
        assert result.id is not None
        assert result.filename.startswith("spec_")
        assert result.filename.endswith(".json")
        assert created_at in result.content
        assert result.content.startswith('{')
        assert "dashboard" in result.content.lower()
        assert "metrics" in result.content.lower()

    def test_specification_workflow_with_real_components(self):
        """Integration test: Workflow execution with real components"""
        # Arrange
        created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        workflow_def = SpecificationWorkflowDefinition(
            requirements=BusinessRequirements("User needs a comprehensive API for user management"),
            save_directory=SaveDirectoryPath("test/specifications/")
        )

        # Act
        result = execute_specification_workflow(workflow_def, created_at)

        # Assert
        assert result.id is not None
        assert result.filename.startswith("spec_")
        assert result.filename.endswith(".json")
        assert created_at in result.content
        assert "api" in result.content.lower()
        assert "user" in result.content.lower()
        assert "test/specifications/" in result.content

    @pytest.mark.asyncio
    async def test_specification_generation_tool_with_real_use_case(self):
        """Integration test: Shell tool with real use case"""
        # This test needs to be async as the tool's execute method is async
        from unittest.mock import AsyncMock

        # Arrange
        use_case = GenerateSpecificationUseCase()
        tool = SpecificationGenerationTool(use_case)
        mock_ctx = AsyncMock()

        # Act
        result = await tool.execute(mock_ctx, "Build an API for task management")

        # Assert
        assert "specification_id" in result
        assert "content" in result
        assert "suggested_filename" in result
        assert result["suggested_filename"].startswith("spec_")
        assert result["suggested_filename"].endswith(".json")
        assert result["content"].startswith("{")
        assert "api" in result["content"].lower()
        assert "task" in result["content"].lower()

        # Verify context calls
        assert mock_ctx.info.called
        assert any("Iniciando geração" in str(call) for call in mock_ctx.info.call_args_list)
        assert any("gerada com ID" in str(call) for call in mock_ctx.info.call_args_list)

    def test_yaml_prompt_loader_basic_file_operations(self):
        """Integration test: Basic file operations with YAML loader"""
        # Test that the YAML loader can handle the case when the file doesn't exist
        # without throwing exceptions in the critical path
        loader = YAMLPromptLoader()

        # This should handle gracefully (return None) rather than crash
        result = loader.load_prompt_template("non_existent_prompt")

        # The result might be None, but the important thing is no exception occurred
        # during the file operations
        assert result is None or isinstance(result, dict)  # Either way, no exception
            
    def test_specification_generation_end_to_end_flow(self):
        """Integration test: Full workflow from use case through to result"""
        # Arrange: Simulate what would happen in shell layer
        created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Act: This mimics the shell-to-core flow
        use_case = GenerateSpecificationUseCase()
        result = use_case.execute(
            BusinessRequirements("Create a comprehensive user dashboard"), 
            created_at
        )
        
        # Additional core workflow processing (simulating what would happen in real system)
        # This verifies that the whole data flow works properly
        workflow_def = SpecificationWorkflowDefinition(
            requirements=BusinessRequirements("Create a comprehensive user dashboard"),
            save_directory=SaveDirectoryPath("ctxfy/specifications/")
        )
        
        workflow_result = execute_specification_workflow(workflow_def, created_at)
        
        # Both results should have the timestamp properly embedded
        assert created_at in result.content
        assert created_at in workflow_result.content
        
        # Both should have similar characteristics
        assert result.filename.startswith("spec_")
        assert workflow_result.filename.startswith("spec_")
        
        assert "dashboard" in result.content.lower()
        assert "dashboard" in workflow_result.content.lower()