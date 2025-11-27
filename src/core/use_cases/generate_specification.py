from src.core.models.specification_result import SpecificationResult
from src.core.models.specification_workflow import BusinessRequirements

from ..workflows.specification_workflow import execute_specification_generation


class GenerateSpecificationUseCase:
    def execute(self, business_requirements: BusinessRequirements, created_at: str = "") -> SpecificationResult:
        return execute_specification_generation(business_requirements, created_at=created_at)