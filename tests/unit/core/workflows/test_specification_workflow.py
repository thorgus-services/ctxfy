from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from src.core.models.specification_result import SaveDirectoryPath
from src.core.models.specification_workflow import (
    BusinessRequirements,
    SpecificationWorkflowDefinition,
)
from src.core.workflows.specification_workflow import execute_specification_workflow


def test_execute_specification_workflow_with_valid_requirements_and_timestamp():
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("User needs dashboard for metrics"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = execute_specification_workflow(workflow_def, created_at)

    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert result.content.startswith('{')
    assert "dashboard" in result.content.lower()
    assert created_at in result.content


def test_execute_specification_workflow_with_empty_requirements():
    """Test the specification workflow with empty requirements"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements(""),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    with pytest.raises(ValueError):
        execute_specification_workflow(workflow_def, created_at)


def test_execute_specification_workflow_with_api_requirements():
    """Test the workflow with API requirements"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("System needs REST API for user management"),
        save_directory=SaveDirectoryPath("custom/path/")
    )
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = execute_specification_workflow(workflow_def, created_at)

    assert "api" in result.content.lower()
    assert "REST API" in result.content
    assert "user" in result.content or "users" in result.content
    assert "custom/path/" in result.content
    assert created_at in result.content


def test_execute_specification_workflow_result_immutability():
    """Verify that the result value object is immutable"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("Test requirements"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = execute_specification_workflow(workflow_def, created_at)

    with pytest.raises(FrozenInstanceError):
        result.content = "new content"


def test_execute_specification_workflow_filename_generation():
    """Test meaningful filename generation by the workflow"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("System for financial reports"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    result = execute_specification_workflow(workflow_def, created_at)

    assert result.filename.startswith("spec_")
    assert result.filename.endswith(".json")
    assert "financial" in result.filename or "reports" in result.filename


def test_execute_specification_workflow_with_empty_timestamp():
    """Test workflow works with empty timestamp (fallback behavior)"""
    workflow_def = SpecificationWorkflowDefinition(
        requirements=BusinessRequirements("Simple requirements"),
        save_directory=SaveDirectoryPath("ctxfy/specifications/")
    )

    result = execute_specification_workflow(workflow_def, "")  # Empty timestamp

    assert result.id is not None
    assert result.filename.startswith("spec_")
    assert result.content.startswith('{')