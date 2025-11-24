import pytest

from src.core.models.specification_result import SaveDirectoryPath, SpecificationResult
from src.core.models.specification_workflow import (
    BusinessRequirements,
    SpecificationWorkflowDefinition,
)
from src.core.workflows.specification_workflow import SpecificationWorkflow


def test_specification_workflow_protocol_implementation():
    """Test the SpecificationWorkflow class that implements the protocol"""
    workflow = SpecificationWorkflow()
    
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("User needs dashboard for metrics"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )
    
    result = workflow.execute(workflow_def)

    assert isinstance(result, SpecificationResult)
    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert result.content.startswith('{')
    assert "dashboard" in result.content.lower()


def test_specification_workflow_with_empty_requirements():
    """Test the SpecificationWorkflow with empty requirements raises error"""
    workflow = SpecificationWorkflow()
    
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements(""),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )
    
    with pytest.raises(ValueError, match="Business requirements cannot be empty or invalid"):
        workflow.execute(workflow_def)