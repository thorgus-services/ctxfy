import hashlib
import json
import re
from datetime import datetime, timezone
from typing import List

from ..models.specification_result import (
    SaveDirectoryPath,
    SpecificationContent,
    SpecificationFilename,
    SpecificationId,
    SpecificationResult,
)
from ..models.specification_workflow import (
    BusinessRequirements,
    SpecificationWorkflowDefinition,
)
from ..ports.specification_ports import SpecificationWorkflowPort


class SpecificationWorkflow(SpecificationWorkflowPort):
    def execute(self, workflow_definition: SpecificationWorkflowDefinition) -> SpecificationResult:
        created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        return execute_specification_workflow(workflow_definition, created_at)


def execute_specification_workflow(
    workflow_definition: SpecificationWorkflowDefinition,
    created_at: str = ""
) -> SpecificationResult:
    if not _validate_business_requirements(workflow_definition.requirements):
        raise ValueError("Business requirements cannot be empty or invalid")

    cleaned_requirements = _clean_business_requirements(workflow_definition.requirements)
    spec_id = _generate_specification_id(cleaned_requirements)
    filename = _generate_specification_filename(cleaned_requirements)
    content = _format_specification_content(cleaned_requirements, str(workflow_definition.save_directory), created_at)

    return SpecificationResult(
        id=spec_id,
        content=content,
        filename=filename
    )


def _validate_business_requirements(requirements: BusinessRequirements) -> bool:
    return bool(requirements and str(requirements).strip())


def _clean_business_requirements(requirements: BusinessRequirements) -> str:
    if not requirements:
        return ""
    return re.sub(r'[^\w\s\.\,\:\;\-\(\)]', '', str(requirements)).strip()


def _extract_important_words(text: str, max_words: int = 3, min_length: int = 4) -> List[str]:
    if not text:
        return ["spec"]
    words = text.lower().split()
    return [w for w in words if len(w) >= min_length][:max_words]


def _generate_specification_id(content: str) -> SpecificationId:
    return SpecificationId(hashlib.sha256(content.encode()).hexdigest()[:8])


def _generate_specification_filename(content: str) -> SpecificationFilename:
    important_words = _extract_important_words(content)
    slug = "_".join(important_words) if important_words else "spec"
    return SpecificationFilename(f"spec_{slug[:20]}.json")


def _extract_components_from_requirements(requirements: str, save_directory: str = "ctxfy/specifications/") -> list[str]:
    components = [save_directory]
    if "dashboard" in requirements.lower():
        components.extend(["frontend/dashboard", "backend/metrics-service"])
    if "api" in requirements.lower() or "interface" in requirements.lower():
        components.append("api/gateway")
    return components


def _generate_description(requirements: str) -> str:
    words = requirements.split()
    return " ".join(words[:15]) + ("..." if len(words) > 15 else "")


def _generate_acceptance_criteria(requirements: str) -> list[str]:
    criteria = [
        "Especificação gerada no formato JSON válido",
        "Arquivo salvo no diretório ctxfy/specifications/",
        "Conteúdo acessível para geração de código automatizada"
    ]
    if "metrics" in requirements.lower() or "métricas" in requirements.lower():
        criteria.append("Dashboard exibe métricas em tempo real")
    return criteria


def _format_specification_content(requirements: str, save_directory: str = "ctxfy/specifications/", created_at: str = "") -> SpecificationContent:
    components = _extract_components_from_requirements(requirements, save_directory)

    content_str = json.dumps({
        "title": "Especificação Técnica Gerada",
        "description": _generate_description(requirements),
        "business_requirements": requirements,
        "architecture": "Seguindo padrões do projeto ctxfy",
        "components": components,
        "interfaces": ["REST API", "Message Queue"],
        "security": ["Authentication", "Authorization", "Data Encryption"],
        "acceptance_criteria": _generate_acceptance_criteria(requirements),
        "created_at": created_at
    }, indent=2, ensure_ascii=False)

    return SpecificationContent(content_str)


def execute_specification_generation(
    requirements: BusinessRequirements,
    save_directory: str = "ctxfy/specifications/",
    created_at: str = ""
) -> SpecificationResult:
    workflow_def = SpecificationWorkflowDefinition(
        requirements=requirements,
        save_directory=SaveDirectoryPath(save_directory)
    )
    return execute_specification_workflow(workflow_def, created_at)