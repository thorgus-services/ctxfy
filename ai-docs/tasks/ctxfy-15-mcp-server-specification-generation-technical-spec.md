# 🔄 TECHNICAL SPECIFICATION: MCP SERVER FOR SPECIFICATION GENERATION

## 📋 Overview and Metadata

**Document ID**: SPEC-MCP-GEN-001  
**Title**: MCP Server for Technical Specification Generation  
**Domain**: Software Architecture & MCP Development  
**Author**: Technical Product Manager  
**Creation Date**: November 23, 2025  
**Status**: Technical Specification  
**Stakeholders**: Technical Product Manager (fernando), Tech Lead (fernando)  
**Priority**: High  
**Complexity Level**: Complex  

## 🎯 Business Requirements Analysis

### Original Business Requirement
As a Technical Product Manager with 7+ years of experience in high scalability systems, I want an MCP Server that automatically generates technical specifications in the `ctxfy/specifications/` directory of the client through a specialized CLI prompt for code model CLIs, so that I can translate business needs into standardized technical documentation without manual effort, with generation of at least 5 technical specifications per day with 98% architectural compliance and response time under 1.5 seconds, measured by automated code quality auditing, immutability verification of value objects, and performance metrics in staging environment with branch coverage >80% for critical paths before any refactoring.

### Business Context
- **Business Owner**: Technical Product Manager focused on developer productivity and architecture compliance
- **User Perspective**: Technical users want fast conversion of business requirements to standardized technical specs without manual work
- **Market Context**: Increasing need for AI-assisted development tools and standardized documentation formats
- **Strategic Importance**: Critical for reducing development time and improving spec consistency - direct impact on team efficiency

## 🏗️ Technical Architecture

### System Architecture Pattern
Implementing Hexagonal Architecture with Functional Core & Imperative Shell (FCIS) pattern:
- **Core Package**: Contains domain models, use cases, ports, and workflows
- **Shell Package**: Contains adapters, orchestrators, and registry components
- **Dependency Direction**: All dependencies flow inward toward the core

### Package Structure
```
src/
├── core/
│   ├── models/
│   │   ├── specification_result.py    # Value objects imutáveis com NewType
│   │   └── specification_workflow.py  # Value object para workflow
│   ├── use_cases/
│   │   └── generate_specification.py  # Lógica de negócio pura
│   ├── ports/
│   │   └── specification_ports.py     # Interfaces por domínio (não por tipo)
│   └── workflows/
│       └── specification_workflow.py  # Definição pura do fluxo
│
├── shell/
│   ├── adapters/
│   │   ├── tools/
│   │   │   └── specification_generation_tool.py  # Implementação de command port
│   │   └── prompts/
│   │       └── specification_save_instruction_prompt.py # Implementação de command port
│   ├── registry/
│   │   ├── tool_registry.py           # Registry centralizado
│   │   └── prompt_registry.py         # Registry centralizado
│   └── orchestrators/
│       └── specification_orchestrator.py # Coordenador com ≤4 dependências
│
└── app.py                            # Composition root
```

## 🧱 Technical Components

### 1. Value Objects (core/models/specification_result.py)
```python
from dataclasses import dataclass
from typing import NewType

SpecificationId = NewType('SpecificationId', str)
SpecificationContent = NewType('SpecificationContent', str)
SpecificationFilename = NewType('SpecificationFilename', str)
SaveDirectoryPath = NewType('SaveDirectoryPath', str)

@dataclass(frozen=True)
class SpecificationResult:
    """
    Value object imutável para resultado da especificação técnica.
    Segue princípios funcionais: estado nunca muda, operações retornam novas instâncias.
    """
    id: SpecificationId
    content: SpecificationContent
    filename: SpecificationFilename

    def with_updated_content(self, new_content: str) -> "SpecificationResult":
        """Retorna nova instância com conteúdo atualizado"""
        return SpecificationResult(
            id=self.id,
            content=SpecificationContent(new_content),
            filename=self.filename
        )
```

### 2. Domain Workflow (core/models/specification_workflow.py)
```python
from typing import NewType
from dataclasses import dataclass
from .specification_result import SaveDirectoryPath

BusinessRequirements = NewType('BusinessRequirements', str)

@dataclass(frozen=True)
class SpecificationWorkflowDefinition:
    """
    Definição pura do fluxo de trabalho para geração de especificações.
    Não contém efeitos colaterais, apenas define as etapas do processo.
    Segue princípio de Workflow como value object imutável.
    """
    requirements: BusinessRequirements
    save_directory: SaveDirectoryPath = SaveDirectoryPath("ctxfy/specifications/")

    def with_updated_requirements(self, new_requirements: str) -> "SpecificationWorkflowDefinition":
        """Retorna nova instância com requisitos atualizados"""
        return SpecificationWorkflowDefinition(
            requirements=BusinessRequirements(new_requirements),
            save_directory=self.save_directory
        )

    def with_updated_save_directory(self, new_directory: str) -> "SpecificationWorkflowDefinition":
        """Retorna nova instância com diretório de salvamento atualizado"""
        return SpecificationWorkflowDefinition(
            requirements=self.requirements,
            save_directory=SaveDirectoryPath(new_directory)
        )
```

### 3. Ports (core/ports/specification_ports.py)
```python
from typing import Protocol, Dict, Any
from fastmcp import Context
from ..models.specification_result import SpecificationResult, SaveDirectoryPath
from ..models.specification_workflow import BusinessRequirements

class SpecificationGenerationCommandPort(Protocol):
    """
    Primary (driving) port para geração de especificações técnicas.
    Segue convenção de nomenclatura *CommandPort para ports primários.
    Localizado em arquivo por domínio conforme regra de arquitetura.
    """
    async def execute(self, ctx: Context, business_requirements: BusinessRequirements) -> Dict[str, Any]:
        """Gera especificação técnica a partir de requisitos de negócio"""
        ...

class SpecificationSaveInstructionCommandPort(Protocol):
    """
    Primary (driving) port para geração de instruções de salvamento de especificações.
    Segue convenção de nomenclatura *CommandPort para ports primários.
    """
    async def generate(self, ctx: Context, business_requirements: BusinessRequirements, save_directory: SaveDirectoryPath) -> str:
        """Gera instruções para salvar especificação no filesystem"""
        ...
```

### 4. Use Case (core/use_cases/generate_specification.py)
```python
import json
import hashlib
import re
from datetime import datetime
from typing import List
from src.core.models.specification_result import (
    SpecificationResult,
    SpecificationId,
    SpecificationContent,
    SpecificationFilename
)
from src.core.models.specification_workflow import BusinessRequirements

class GenerateSpecificationUseCase:
    """
    Caso de uso puro para geração de especificações técnicas.
    Não tem dependências externas e não causa efeitos colaterais.
    Segue princípio de Functional Core: funções puras sem side effects.
    CONTÉM TODA A LÓGICA DE NEGÓCIO, INCLUINDO FORMATAÇÃO JSON.
    """

    def execute(self, business_requirements: BusinessRequirements) -> SpecificationResult:
        """
        Processa requisitos de negócio e gera um resultado estruturado.

        Args:
            business_requirements: Requisitos de negócio em formato textual

        Returns:
            SpecificationResult: Value object imutável com o resultado

        Raises:
            ValueError: Se requisitos estiverem vazios ou inválidos
        """
        # Verificação de pré-condições (parte da lógica de negócio)
        if not self._validate_input(business_requirements):
            raise ValueError("Requisitos de negócio não podem estar vazios ou inválidos")

        # Lógica pura de parsing e formatação
        cleaned_requirements = self._clean_input(business_requirements)
        spec_id = self._generate_id(cleaned_requirements)
        filename = self._generate_filename(cleaned_requirements)
        formatted_content = self._format_json_specification(cleaned_requirements)

        return SpecificationResult(
            id=SpecificationId(spec_id),
            content=SpecificationContent(formatted_content),
            filename=SpecificationFilename(filename)
        )

    def _validate_input(self, text: str) -> bool:
        """Valida entrada antes do processamento"""
        return bool(text and text.strip())

    def _clean_input(self, text: str) -> str:
        """Remove caracteres especiais e normaliza o texto"""
        if not text:
            return ""
        return re.sub(r'[^\w\s\.\,\:\;\-\(\)]', '', text).strip()

    def _generate_id(self, content: str) -> str:
        """Gera ID único baseado no conteúdo"""
        return hashlib.sha256(content.encode()).hexdigest()[:8]

    def _extract_important_words(self, text: str, max_words: int = 3, min_length: int = 4) -> List[str]:
        """Extrai palavras importantes para nome de arquivo"""
        if not text:
            return ["spec"]
        words = text.lower().split()
        return [w for w in words if len(w) >= min_length][:max_words]

    def _generate_filename(self, content: str) -> str:
        """Gera nome de arquivo significativo"""
        important_words = self._extract_important_words(content)
        slug = "_".join(important_words) if important_words else "spec"
        return f"spec_{slug[:20]}.json"

    def _format_json_specification(self, requirements: str) -> str:
        """
        Formata a especificação como JSON válido - LÓGICA DE NEGÓCIO NO CORE.
        Esta é uma regra de negócio e não pertence ao shell ou prompt.
        """
        # Análise dos requisitos para extrair componentes
        components = self._extract_components_from_requirements(requirements)

        return json.dumps({
            "title": "Especificação Técnica Gerada",
            "description": self._generate_description(requirements),
            "business_requirements": requirements,
            "architecture": "Seguindo padrões do projeto ctxfy",
            "components": components,
            "interfaces": ["REST API", "Message Queue"],
            "security": ["Authentication", "Authorization", "Data Encryption"],
            "acceptance_criteria": self._generate_acceptance_criteria(requirements),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }, indent=2, ensure_ascii=False)

    def _extract_components_from_requirements(self, requirements: str) -> list[str]:
        """Extrai componentes dos requisitos de negócio"""
        components = ["ctxfy/specifications/"]
        if "dashboard" in requirements.lower():
            components.extend(["frontend/dashboard", "backend/metrics-service"])
        if "api" in requirements.lower() or "interface" in requirements.lower():
            components.append("api/gateway")
        return components

    def _generate_description(self, requirements: str) -> str:
        """Gera descrição resumida dos requisitos"""
        words = requirements.split()
        return " ".join(words[:15]) + ("..." if len(words) > 15 else "")

    def _generate_acceptance_criteria(self, requirements: str) -> list[str]:
        """Gera critérios de aceitação baseados nos requisitos"""
        criteria = [
            "Especificação gerada no formato JSON válido",
            "Arquivo salvo no diretório ctxfy/specifications/",
            "Conteúdo acessível para geração de código automatizada"
        ]
        if "métricas" in requirements.lower() or "metrics" in requirements.lower():
            criteria.append("Dashboard exibe métricas em tempo real")
        return criteria
```

### 5. MCP Tool Adapter (shell/adapters/tools/specification_generation_tool.py)
```python
from fastmcp import Context
from src.core.ports.specification_ports import SpecificationGenerationCommandPort
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase
from src.core.models.specification_workflow import BusinessRequirements
from typing import Dict, Any

class SpecificationGenerationTool(SpecificationGenerationCommandPort):
    """
    Adapter para a tool de geração de especificações.
    Implementa SpecificationGenerationCommandPort e gerencia efeitos colaterais.
    Segue padrão Imperative Shell - Core puro, Shell imperativo.
    LÓGICA DE NEGÓCIO MÍNIMA NO SHELL.
    """

    def __init__(self, use_case: GenerateSpecificationUseCase):
        self.use_case = use_case

    async def execute(
        self,
        ctx: Context,
        business_requirements: str
    ) -> Dict[str, Any]:
        """
        Executa a tool de geração de especificações.
        Coordena efeitos colaterais (LLM sampling) e delega para o core.
        """
        # Log início da operação (efeito colateral)
        await ctx.info(f"Iniciando geração de especificação para requisitos: {business_requirements[:50]}...")

        # Execução do core funcional (sem efeitos colaterais)
        try:
            result = self.use_case.execute(BusinessRequirements(business_requirements))
        except ValueError as e:
            await ctx.error(f"Erro na geração de especificação: {str(e)}")
            raise

        # Log conclusão (efeito colateral)
        await ctx.info(f"Especificação gerada com ID: {result.id}")

        return {
            "specification_id": result.id,
            "content": result.content,
            "suggested_filename": result.filename
        }
```

### 6. Specification Save Prompt Adapter (shell/adapters/prompts/specification_save_instruction_prompt.py)
```python
from fastmcp import Context
from src.core.ports.specification_ports import SpecificationSaveInstructionCommandPort
from src.core.models.specification_result import SaveDirectoryPath
from src.core.models.specification_workflow import BusinessRequirements
from typing import Any

class SpecificationSaveInstructionPrompt(SpecificationSaveInstructionCommandPort):
    """
    Adapter para o prompt de especificação com instruções de salvamento.
    Implementa SpecificationSaveInstructionCommandPort.
    CONTÉM APENAS FORMATAÇÃO DE MENSAGEM, SEM LÓGICA DE NEGÓCIO.
    """

    async def generate(
        self,
        ctx: Context,
        business_requirements: BusinessRequirements,
        save_directory: SaveDirectoryPath = SaveDirectoryPath("ctxfy/specifications/")
    ) -> str:
        """
        Gera o conteúdo do prompt com instruções claras de salvamento.
        Esta é uma operação pura de formatação de string no core, adaptada para o shell.
        SEM LÓGICA DE NEGÓCIO - apenas instruções de formato fixo.
        """
        # Formatação simples de string com parâmetros
        return f"""
Você é um Technical Product Manager especialista em arquitetura de software.
Sua tarefa é salvar a especificação técnica no local correto seguindo EXATAMENTE as instruções abaixo.

## INSTRUÇÕES DE SALVAMENTO EXPLÍCITAS
1. Crie o diretório '{save_directory}' se ele não existir
2. Use o nome de arquivo sugerido pela especificação gerada
3. Salve o arquivo completo no caminho: {save_directory}<nome_arquivo>
4. Retorne apenas o caminho completo do arquivo salvo

## IMPORTANTE PARA CLIENTS DE LLM CODE
O arquivo DEVE ser salvo exatamente no diretório '{save_directory}' com permissões de leitura adequadas.
NÃO modifique o conteúdo da especificação - salve EXATAMENTE como recebido.

Responda SOMENTE com o caminho completo do arquivo salvo no formato:
{save_directory}spec_<descrição_curta>.json
"""
```

### 7. Registry Pattern (shell/registry/)

```python
# src/shell/registry/tool_registry.py
from typing import Dict
from fastmcp import FastMCP
from src.core.ports.specification_ports import SpecificationGenerationCommandPort

class ToolRegistry:
    """
    Registry para todas as tools do sistema.
    Único lugar onde o código interage diretamente com FastMCP.tool().
    Segue padrão Registry centralizado para manutenibilidade.
    """

    def __init__(self):
        self._tools: Dict[str, SpecificationGenerationCommandPort] = {}

    def register_tool(self, name: str, tool: SpecificationGenerationCommandPort) -> None:
        """Registra uma tool no registry"""
        self._tools[name] = tool

    def register_all_to_mcp(self, mcp: FastMCP) -> None:
        """Registra todas as tools no servidor MCP"""
        for name, tool in self._tools.items():
            mcp.tool(
                name=name,
                description="Gera especificações técnicas a partir de requisitos de negócio"
            )(tool.execute)

# Singleton para uso no composition root
tool_registry = ToolRegistry()

# src/shell/registry/prompt_registry.py
from typing import Dict
from fastmcp import FastMCP
from src.core.ports.specification_ports import SpecificationSaveInstructionCommandPort

class PromptRegistry:
    """
    Registry para todos os prompts do sistema.
    Único lugar onde o código interage diretamente com FastMCP.prompt().
    Segue padrão Registry centralizado para manutenibilidade.
    """

    def __init__(self):
        self._prompts: Dict[str, SpecificationSaveInstructionCommandPort] = {}

    def register_prompt(self, name: str, prompt: SpecificationSaveInstructionCommandPort) -> None:
        """Registra um prompt no registry"""
        self._prompts[name] = prompt

    def register_all_to_mcp(self, mcp: FastMCP) -> None:
        """Registra todos os prompts no servidor MCP"""
        for name, prompt in self._prompts.items():
            mcp.prompt(
                name=name,
                description="Gera instruções explícitas para salvar especificação no filesystem"
            )(prompt.generate)

# Singleton para uso no composition root
prompt_registry = PromptRegistry()
```

### 8. Orchestrator (shell/orchestrators/specification_orchestrator.py)

```python
from src.core.use_cases.generate_specification import GenerateSpecificationUseCase
from src.shell.adapters.tools.specification_generation_tool import SpecificationGenerationTool
from src.shell.adapters.prompts.specification_save_instruction_prompt import SpecificationSaveInstructionPrompt
from src.shell.registry.tool_registry import tool_registry
from src.shell.registry.prompt_registry import prompt_registry
from fastmcp import FastMCP

class SpecificationOrchestrator:
    """
    Orchestrator para o fluxo de geração de especificações.
    Máximo de 4 dependências conforme regra do projeto (apenas FastMCP).
    Segue padrão Orchestrator Pattern para coordenação de fluxos.
    """

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self._initialize_components()

    def _initialize_components(self) -> None:
        """Inicializa todos os componentes do fluxo"""
        # Core dependencies - Functional Core
        use_case = GenerateSpecificationUseCase()

        # Shell adapters - Imperative Shell
        tool = SpecificationGenerationTool(use_case=use_case)
        prompt = SpecificationSaveInstructionPrompt()

        # Register components - Registry Pattern
        tool_registry.register_tool("generate_technical_specification", tool)
        prompt_registry.register_prompt("generate_technical_specification_with_save_path", prompt)

        # Register to MCP server - Infrastructure layer
        tool_registry.register_all_to_mcp(self.mcp)
        prompt_registry.register_all_to_mcp(self.mcp)
```

### 9. Composition Root (app.py)

```python
from fastmcp import FastMCP
from src.shell.orchestrators.specification_orchestrator import SpecificationOrchestrator

def create_mcp_server() -> FastMCP:
    """
    Composition root seguindo dependency inversion.
    Único lugar onde as dependências são injetadas.
    Segue padrão de Dependency Injection explícita.
    """
    # FastMCP server setup
    mcp = FastMCP(
        name="ctxfy-specification-server",
        version="1.0.0",
        bearer_token_auth_enabled=True,
        on_duplicate_prompts="error",  # Fail fast on duplicate prompts
        on_duplicate_tools="error"
    )

    # Initialize orchestrator (máximo 4 dependências)
    SpecificationOrchestrator(mcp)

    return mcp

# ASGI application
mcp_server = create_mcp_server()
app = mcp_server.http_app(
    path="/mcp",
    transport="streamable-http"
)
```

## 🧪 Testing Strategy

### Test Coverage Requirements
- **Unit Tests**: 70% targeting Functional Core only (pure functions)
- **Integration Tests**: 25% using real/fake adapters
- **End-to-End Tests**: 5% for critical paths
- **Branch Coverage**: >80% for critical paths before any refactoring

### Test Examples

```python
# src/core/use_cases/test_generate_specification.py
def test_generate_specification_with_valid_requirements():
    """Testa geração de especificação com requisitos válidos"""
    use_case = GenerateSpecificationUseCase()
    result = use_case.execute(BusinessRequirements("User precisa de dashboard para métricas"))
    
    assert result.id is not None
    assert "dashboard" in result.filename
    assert result.content.startswith('{')
    assert "dashboard" in result.content.lower()

def test_generate_specification_with_empty_requirements():
    """Testa tratamento de requisitos vazios"""
    use_case = GenerateSpecificationUseCase()
    with pytest.raises(ValueError):
        use_case.execute(BusinessRequirements(""))

def test_specification_result_immutability():
    """Verifica que o value object é imutável"""
    result = SpecificationResult(
        id=SpecificationId("test-123"),
        content=SpecificationContent("conteúdo original"),
        filename=SpecificationFilename("test.json")
    )
    with pytest.raises(FrozenInstanceError):
        result.content = "novo conteúdo"
```

## 🚀 Implementation Process

### TDD Process (Red → Green → Refactor)
1. Write failing acceptance test against primary port
2. Implement minimal code to pass test
3. Refactor following architecture rules
4. Verify architecture compliance before each refactoring

### Quality Gates
- All tests pass
- Lint without errors (Ruff formatting)
- Follow architectural rules (immutable objects, FCIS, package boundaries)
- Mypy strict mode passing for core
- Zero critical bugs
- 98%+ test coverage of core logic

## ⚙️ Technical Constraints and Requirements

### Performance Requirements
- Response time < 1.5 seconds p95
- Support for 5+ specifications per day
- Branch coverage >80% for critical paths

### Security Requirements
- No exposure of sensitive data
- Follow security policy for file operations
- Ruff and Bandit security scans
- Proper authentication mechanisms for file system access

### Integration Requirements
- Integrate with FastMCP framework
- Proper context handling for logging and progress
- HTTP deployment support with authentication

### Data Requirements
- Schema validation for generated JSON specifications
- Immutable value objects throughout the core
- Audit trails for generation operations

## ✅ Validation Protocol

### Functional Criteria
- [ ] Users can submit business requirements to generate technical specifications
- [ ] Specifications are saved in the ctxfy/specifications/ directory with proper file naming
- [ ] Generated specifications follow standardized JSON format with proper schema
- [ ] Server provides clear paths to saved specification files and handles errors appropriately
- [ ] MCP server registers tools and prompts correctly following FastMCP patterns

### Quality Criteria
- [ ] Response time < 1.5 seconds for 95% of requests, Ruff formatting compliance 100%
- [ ] Zero data integrity issues, Mypy strict mode passing for core, 98%+ test coverage
- [ ] 100% compliance with architectural rules (immutable objects, FCIS, package boundaries)

### Verification Approach
- **Testing**: TDD process with acceptance tests against primary ports, unit tests for pure functions, integration tests with real/fake adapters
- **Performance**: Load testing simulating 10 concurrent users, response time measurement, connection handling verification
- **Security**: File system permissions validation, input sanitization testing, dependency security scanning
- **User Acceptance**: Beta testing with technical team, architecture compliance review, performance verification

## 📊 Cross-Reference Mapping

| Business Requirement | Technical Component | Validation Method | Owner | Risk Level |
|----------------------|---------------------|-------------------|-------|------------|
| MCP Server for spec generation | src/core/use_cases/generate_specification.py | Unit tests with TDD | Technical PM | Medium |
| Save to ctxfy/specifications/ | src/shell/adapters/specification_generation_tool.py | Integration tests | Technical PM | Medium |
| Response time < 1.5s | Performance tests | Load testing | Technical PM | High |
| 98% architectural compliance | src/core/models/specification_result.py | Architecture linters | Technical PM | High |
| MCP tool registration | src/shell/registry/ | Integration tests | Technical PM | Medium |

## 🚨 Risk Factors and Mitigation

| Risk Factor | Impact | Mitigation Strategy |
|-------------|--------|-------------------|
| Performance issues if architecture not followed | High | Profile critical paths, implement efficient algorithms for text processing |
| Architecture compliance issues if TDD not followed | High | Regular architecture reviews, automated compliance checks |
| File system access issues | Medium | Proper authentication mechanisms, permissions validation |
| MCP framework misuse | Medium | Strict adherence to FastMCP documentation, early testing |

## 📝 Implementation Notes

### Critical Success Factors
- **Architecture Compliance**: Hexagonal Architecture principles must be followed from the start
- **TDD Adherence**: Red → Green → Refactor cycle mandatory for all implementations
- **Immutability by Default**: All domain models must be immutable value objects
- **Toolchain Standards**: Ruff (line length 88), Mypy (strict mode for core), Bandit/Safety

### Boy Scout Refactoring Checklist
- [ ] Reduced function length: Methods kept < 15 lines
- [ ] Improved naming: Descriptive variable names
- [ ] Extracted pure functions: Business logic separated from infrastructure
- [ ] Verified immutability: All value objects are frozen
- [ ] Added error case tests: Coverage for edge cases
- [ ] Lowered cyclomatic complexity: Simple, focused functions

### Architecture Verification
- [ ] Core does not depend on shell
- [ ] Orchestrator has ≤4 dependencies
- [ ] Port naming conventions followed
- [ ] No infrastructure leakage into core
- [ ] Immutable value objects used throughout

## 🔚 Conclusion

This technical specification outlines a comprehensive implementation of an MCP Server for Technical Specification Generation following Hexagonal Architecture principles with Functional Core & Imperative Shell. The implementation provides secure, performant, and architecture-compliant API with sub-1.5s response times while maintaining 98%+ architectural compliance. The system is designed with proper testing coverage, immutability guarantees, and clear separation of concerns to ensure maintainability and scalability.