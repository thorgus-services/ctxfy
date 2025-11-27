from datetime import datetime, timezone
from typing import Any, Dict

from fastmcp import Context

from src.core.models.specification_result import SpecificationResult
from src.core.models.specification_workflow import BusinessRequirements
from src.core.ports.specification_ports import SpecificationGenerationCommandPort
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase

from ...utils.retry_utils import execute_with_retry


class SpecificationGenerationTool(SpecificationGenerationCommandPort):
    def __init__(self, use_case: GenerateSpecificationUseCase):
        self.use_case = use_case

    async def execute(
        self,
        ctx: Context,
        business_requirements: str
    ) -> Dict[str, Any]:
        await ctx.info(f"Iniciando geração de especificação para requisitos: {business_requirements[:50]}...")

        # Generate timestamp in the shell (imperative part)
        created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        def execute_generation() -> SpecificationResult:
            return self.use_case.execute(BusinessRequirements(business_requirements), created_at)

        try:
            result = execute_with_retry(execute_generation)
        except ValueError as e:
            await ctx.error(f"Erro na geração de especificação: {str(e)}")
            raise

        await ctx.info(f"Especificação gerada com ID: {result.id}")

        return {
            "specification_id": result.id,
            "content": result.content,
            "suggested_filename": result.filename
        }