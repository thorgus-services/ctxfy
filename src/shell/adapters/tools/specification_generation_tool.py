from typing import Any, Dict

from fastmcp import Context

from src.core.models.specification_workflow import BusinessRequirements
from src.core.ports.specification_ports import SpecificationGenerationCommandPort
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase


class SpecificationGenerationTool(SpecificationGenerationCommandPort):
    def __init__(self, use_case: GenerateSpecificationUseCase):
        self.use_case = use_case

    async def execute(
        self,
        ctx: Context,
        business_requirements: str
    ) -> Dict[str, Any]:
        await ctx.info(f"Iniciando geração de especificação para requisitos: {business_requirements[:50]}...")

        try:
            result = self.use_case.execute(BusinessRequirements(business_requirements))
        except ValueError as e:
            await ctx.error(f"Erro na geração de especificação: {str(e)}")
            raise

        await ctx.info(f"Especificação gerada com ID: {result.id}")

        return {
            "specification_id": result.id,
            "content": result.content,
            "suggested_filename": result.filename
        }