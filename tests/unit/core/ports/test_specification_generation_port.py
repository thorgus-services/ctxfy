from unittest.mock import AsyncMock

import pytest

from src.core.models.specification_workflow import BusinessRequirements
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase
from src.shell.adapters.tools.specification_generation_tool import (
    SpecificationGenerationTool,
)


class TestSpecificationGenerationAcceptance:
    """Acceptance tests for specification generation via primary port"""
    
    async def test_generate_specification_with_valid_requirements_via_port(self):
        """Acceptance test: Generate specification with valid requirements via primary port"""
        # Arrange: Use real use case with a timestamp to ensure pure function usage
        use_case = GenerateSpecificationUseCase()
        tool = SpecificationGenerationTool(use_case)

        # Create a mock context for testing
        mock_ctx = AsyncMock()

        business_requirements = "Create a user dashboard for metrics monitoring"

        # Act: Execute via primary port
        result = await tool.execute(mock_ctx, business_requirements)

        # Assert: Verify the expected behavior
        assert "specification_id" in result
        assert "content" in result
        assert "suggested_filename" in result

        # Verify that context logging was called appropriately
        mock_ctx.info.assert_called()
        assert any("Iniciando geração de especificação" in str(call) for call in mock_ctx.info.call_args_list)
        assert any("Especificação gerada com ID" in str(call) for call in mock_ctx.info.call_args_list)

        # Verify content contains expected elements
        assert result["content"].startswith("{")
        assert "dashboard" in result["content"].lower() or "metrics" in result["content"].lower()
        assert result["suggested_filename"].startswith("spec_")
        assert result["suggested_filename"].endswith(".json")


    async def test_generate_specification_with_invalid_requirements_fails_via_port(self):
        """Acceptance test: Generate specification with invalid requirements fails via primary port"""
        # Arrange
        use_case = GenerateSpecificationUseCase()
        tool = SpecificationGenerationTool(use_case)
        
        # Create a mock context for testing
        mock_ctx = AsyncMock()
        
        invalid_requirements = ""  # This should trigger a ValueError based on validation
        
        # Act & Assert: Execute via primary port and expect error
        with pytest.raises(ValueError):
            await tool.execute(mock_ctx, invalid_requirements)
        
        # Verify that error logging was called
        mock_ctx.error.assert_called()


    async def test_generate_specification_empty_requirements_via_port(self):
        """Acceptance test: Generate specification with empty requirements fails via primary port"""
        # Arrange
        use_case = GenerateSpecificationUseCase()
        tool = SpecificationGenerationTool(use_case)
        
        # Create a mock context for testing
        mock_ctx = AsyncMock()
        
        empty_requirements = ""
        
        # Act & Assert: Execute via primary port and expect error
        with pytest.raises(ValueError):
            await tool.execute(mock_ctx, empty_requirements)
        
        # Verify that error logging was called
        mock_ctx.error.assert_called()


    def test_execute_specification_workflow_port_implementation(self):
        """Test the workflow port implementation directly"""
        # This tests the SpecificationWorkflowPort implementation
        from src.core.models.specification_result import SaveDirectoryPath
        from src.core.models.specification_workflow import (
            SpecificationWorkflowDefinition,
        )
        from src.core.workflows.specification_workflow import SpecificationWorkflow

        # Arrange
        workflow_impl = SpecificationWorkflow()

        workflow_def = SpecificationWorkflowDefinition(
            requirements=BusinessRequirements("Create a simple API"),
            save_directory=SaveDirectoryPath("ctxfy/specifications/")
        )

        # Since execute_specification_workflow now requires a timestamp,
        # we need to call it appropriately - but the port just calls execute with one parameter
        # This shows that I need to update the execute method in SpecificationWorkflow class
        # Let me check the current implementation first
        result = workflow_impl.execute(workflow_def)  # This will use the default empty string for created_at

        # Assert
        assert result.id is not None
        assert result.filename.startswith("spec_")
        assert result.filename.endswith(".json")
        assert result.content.startswith("{")