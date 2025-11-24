from typing import Any, Dict, Protocol

from fastmcp import Context

from ..models.specification_result import SpecificationResult
from ..models.specification_workflow import (
    BusinessRequirements,
    SpecificationWorkflowDefinition,
)


class SpecificationGenerationCommandPort(Protocol):
    async def execute(self, ctx: Context, business_requirements: BusinessRequirements) -> Dict[str, Any]:
        ...

class SpecificationWorkflowPort(Protocol):
    def execute(self, workflow_definition: SpecificationWorkflowDefinition) -> SpecificationResult:
        ...
