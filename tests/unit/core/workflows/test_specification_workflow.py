from dataclasses import FrozenInstanceError

import pytest

from src.core.models.specification_result import SaveDirectoryPath
from src.core.models.specification_workflow import (
    BusinessRequirements,
    SpecificationWorkflowDefinition,
)
from src.core.workflows.specification_workflow import execute_specification_workflow


def test_specification_workflow_process_with_valid_requirements():
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("User needs dashboard for metrics"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )

    result = execute_specification_workflow(workflow_def)

    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert result.content.startswith('{')
    assert "dashboard" in result.content.lower()


def test_specification_workflow_process_with_empty_requirements():
    """Test the specification workflow with empty requirements"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements(""),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )

    with pytest.raises(ValueError):
        execute_specification_workflow(workflow_def)


def test_specification_workflow_process_with_api_requirements():
    """Test the workflow with API requirements"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("System needs REST API for user management"),
        save_directory=SaveDirectoryPath("custom/path/")
    )

    result = execute_specification_workflow(workflow_def)

    assert "api" in result.content.lower()
    assert "REST API" in result.content
    assert "user" in result.content or "users" in result.content
    assert "custom/path/" in result.content


def test_specification_workflow_result_immutability():
    """Verify that the result value object is immutable"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("Test requirements"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )

    result = execute_specification_workflow(workflow_def)

    with pytest.raises(FrozenInstanceError):
        result.content = "new content"


def test_specification_workflow_process_filename_generation():
    """Test meaningful filename generation by the workflow"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("System for financial reports"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )

    result = execute_specification_workflow(workflow_def)

    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert "financial" in result.filename or "reports" in result.filename