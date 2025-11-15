# 🔄 BUSINESS REQUIREMENTS TRANSLATION - SERVER OUTPUT DIRECTORY WITH FASTMCP CONTEXT

## 📋 Context & Metadata
Translation ID: TR-SERVER-OUTPUT-DIR-001
Business Requirement: "Sistema de Output com Diretório Gerenciado pelo Servidor usando Context do FastMCP"
Domain Context: AI Infrastructure & Model Context Protocol
Stakeholders:
- Product Owner: Fernando Jr
- Tech Lead: AI Infrastructure Team
Priority: High
Complexity Level: Complex
Last Updated: November 14, 2025
AI Context: Use as basis to generate technical implementation following Hexagonal Architecture and Functional Core principles

## 🔍 Business Requirement Analysis

### Original Requirement
Sistema de Output com Diretório Gerenciado pelo Servidor usando Context do FastMCP

**Summary**: Como Product Manager,  
quero implementar um sistema onde o diretório ctxfy/ é criado e gerenciado exclusivamente pelo MCP server para armazenamento de outputs gerados,  
para que o client tenha uma área de resultados previsível enquanto mantém flexibilidade total para referenciar arquivos de entrada de qualquer local do filesystem.

Atualização Crítica Baseada no Context do FastMCP:
⚠️ Análise do Context do FastMCP:
- As operações de filesystem precisam ser executadas do lado do client, não do servidor
- O objeto Context do FastMCP fornece acesso às capacidades do client através de ctx.sample()
- A documentação confirma: "Context is only available during a request; attempting to use context methods outside a request will raise errors"
- O ctx.sample() permite solicitar ao LLM do client que realize operações no filesystem local
- Métodos como pathlib e operações diretas de filesystem não funcionarão pois o servidor MCP não tem acesso ao filesystem do client

### Stakeholder Context
Business owner: Fernando Jr (focused on reliable output management and system architecture)
User perspective: Development team needs predictable output locations while maintaining flexibility for input files
Market context: Growing adoption of Model Context Protocol across AI/LLM platforms (Claude Desktop, Cursor, ChatGPT, etc.)
Strategic importance: Critical for implementing proper output management in MCP services while respecting client-server boundaries

### Ambiguities & Assumptions
Ambiguous terms:
- "Gerenciado exclusivamente pelo servidor" - needs concrete definition (server controls workflow but client executes filesystem operations)
- "Área de resultados previsível" - specific directory structure and naming conventions need to be defined
- "Flexibilidade total" - specific constraints and boundaries need to be established

Unstated assumptions:
- FastMCP Context is available and stable
- LLM sampling through ctx.sample() is the primary mechanism for client-side operations
- Clients support MCP protocol and Context methods

Missing context:
- Specific performance requirements for directory operations
- Security requirements for output file management
- Integration requirements with existing infrastructure

Clarification needed:
- Define exact authentication mechanisms required
- Specify compliance requirements for file handling
- Clarify monitoring and observability requirements

## 🎯 Technical Translation

### AI Context Requirements
- **Model Guidance**: You are a senior software architect specialized in MCP systems with 10+ years experience in Hexagonal Architecture, Functional Core & Imperative Shell patterns, and TDD
- **Context Sources**: Use official FastMCP documentation (https://gofastmcp.com/), MCP protocol specifications, and internal architecture standards at /ai_docs/
- **Output Format**: Structure response as complete technical PRP with detailed sections following our templates
- **Success Criteria**: Generated PRP should enable implementation without ambiguity by a junior engineer, following TDD and architecture rules

### Technical Objective
Develop a server-managed output directory system that provides predictable, secure, and standardized output management using FastMCP Context for client-side filesystem operations, following Hexagonal Architecture principles with proper separation of concerns between server logic and client filesystem access.

### Core Capabilities Required

**Capability 1: Context-Based Directory Management**
- Description: Complete implementation of directory creation and management using FastMCP Context methods (ctx.sample) to execute filesystem operations on the client side
- User value: Reliable output directory structure without requiring server access to client filesystem
- Technical complexity: Complex - requires deep understanding of MCP Context, FastMCP framework, and client-server filesystem operation patterns
- AI Context: Use hexagonal architecture with primary ports for directory management interactions and secondary ports for client filesystem operations; implement with Functional Core & Imperative Shell pattern

**Capability 2: ctx.sample() Integration for Client-Side Operations**
- Description: Comprehensive implementation of client-side filesystem operations using ctx.sample() for all directory and file operations (create, read, write, validate)
- User value: Secure and reliable filesystem operations that respect client-server boundaries
- Technical complexity: Medium-High - requires understanding of Context-based operations, parameter serialization, and client-server operation exchange protocols
- AI Context: All domain models must be immutable using @dataclass(frozen=True); implement validation in __post_init__; create transformation methods that return new instances

**Capability 3: README Generation and Documentation**
- Description: Automatic generation of README.md in the root ctxfy/ directory with clear instructions about server management and client responsibilities
- User value: Clear documentation for users about directory structure and usage boundaries
- Technical complexity: Medium - requires understanding of markdown generation and client-side file creation
- AI Context: Implement TDD from the start: write failing acceptance test against primary port before any implementation

**Capability 4: Input/Output Separation with Flexible References**
- Description: Maintain clear separation between server-managed output directories and client-controlled input files with flexible reference capabilities
- User value: Maximum flexibility for input management while ensuring reliable output storage
- Technical complexity: Medium - requires proper path validation and reference management without filesystem confusion
- AI Context: Define primary ports as OutputCommandPort/OutputQueryPort, secondary ports as ClientFilesystemPort/ClientDirectoryPort; use orchestrators for filesystem workflows

**Capability 5: Validation and Error Handling**
- Description: Comprehensive validation of directory operations, error handling, and user communication through Context methods
- User value: Operational visibility for debugging, proper error communication, and system reliability
- Technical complexity: Medium - requires integration with Context logging, error reporting, and structured validation
- AI Context: Implement orchestrators with maximum 4 dependencies; maintain strict separation between business logic and validation concerns

### Technical Constraints & Requirements
Performance requirements: Directory operations < 500ms p95, consistent directory availability with 99.9% reliability, ability to create and manage all required directory structures
Security requirements: MCP protocol compliance, proper path validation to prevent directory traversal, structured logging in JSON format, Ruff and Bandit security scans
Integration requirements: FastMCP Context integration, MCP client compatibility (Claude Desktop, Cursor, ChatGPT), ctx.sample() for client-side operations
Data requirements: Immutable value objects for all domain models, proper path serialization for client-side operations, structured logging for audit trails
Compliance requirements: MCP protocol standards, internal security policies, Mypy strict mode for core packages, proper error handling and validation

### Architecture Considerations
Pattern recommendations: Hexagonal Architecture with CQRS for separate read/write operations for directory management, Functional Core & Imperative Shell for business logic isolation
Component boundaries: Core package (domain models, pure functions), Adapters package (Context operations, client filesystem), Interfaces package (API, CLI)
Data flow considerations: Pydantic models only at boundaries (if needed for validation), convert to immutable value objects immediately, validation before client-side operations
Scalability approach: Stateless directory management service, client-side execution of filesystem operations, server-side coordination and validation

## 🔍 RAG Integration & Context Stack Reference

### RAG Sources
Primary Documentation:
- https://gofastmcp.com/servers/context.md (Context object and methods)
- https://gofastmcp.com/servers/sampling.md (ctx.sample method)
- https://gofastmcp.com/servers/server.md (Server implementation patterns)
- https://www.cosmicpython.com/ (Hexagonal Architecture patterns)

Internal Knowledge:
- /ai_docs/architecture_standards.md (Hexagonal Architecture rules)
- /ai_docs/testing_strategy.md (TDD and testing requirements)
- /ai_docs/security_standards.md (internal policy)
- /ai_docs/mcp_context_patterns.md (Context usage patterns)
- /examples/directory_management_success.md (previous successful implementations)

### Context Stack Reference
- **System Layer**: Follow Hexagonal Architecture principles from /ai_docs/architecture_standards.md
- **Domain Layer**: Include specific output management and client-server filesystem boundaries
- **Task Layer**: Focus on security and filesystem governance as primary priorities
- **RAG Integration**: Use documentation sources for current best practices
- **Reference**: PRP-ID: PRP-SERVER-OUTPUT-DIR-001

## 🛠️ Implementation Strategy

### Technical Approach
Develop stateless microservice with directory management capabilities following TDD process (Red → Green → Refactor), using Hexagonal Architecture with core isolated from infrastructure, immutable value objects for domain models, and Context-based client adapters for filesystem operations.

### Key Technical Decisions
Technology stack: Python 3.13, FastMCP 2.0, Context object for client-side operations, proper dependency injection
Architecture style: Hexagonal Architecture with domain-driven design, primary ports for driving logic, secondary ports for client filesystem operations
Data model strategy: Immutable value objects (@dataclass(frozen=True)) for domain models, validation in __post_init__, Context-based operations for filesystem
Error handling approach: Proper exception handling with Context methods for communication, validation before client operations, structured error reporting
Testing strategy: TDD mandatory with 70% unit tests (pure functions), 25% integration tests (Context adapters), 5% end-to-end tests, Boy Scout Rule refactoring per PR

### Resource Implications
Development effort: 2-3 weeks for complete MVP with comprehensive tests following TDD
Infrastructure needs: MCP server instance, compatible clients that support Context operations
Maintenance considerations: Path validation monitoring, Context operation logging, regular dependency updates with Safety checks, architecture compliance monitoring
Team skills required: Python TDD experience, Hexagonal Architecture implementation, MCP Context usage, security best practices, Ruff/Mypy toolchain proficiency

## 📁 Architecture Implementation

### Core Components

#### Functional Core (Domain Logic)
```python
# src/core/models.py
from dataclasses import dataclass, field
from typing import NewType, Tuple
from pathlib import PurePath

OutputPath = NewType("OutputPath", str)
InputPath = NewType("InputPath", str)

@dataclass(frozen=True)
class OutputDirectory:
    """Server-managed output directory configuration"""
    base_path: str
    subdirectories: Tuple[str, ...]
    readme_content: str

    def __post_init__(self):
        if not self.base_path.strip():
            raise ValueError("Base path cannot be empty")
        if not self.subdirectories:
            raise ValueError("Must specify at least one subdirectory")
```

#### Primary Ports (Server Commands/Queries)
```python
# src/core/ports/output_ports.py
from typing import Protocol
from .models import OutputDirectory

class OutputCommandPort(Protocol):
    async def ensure_directory_structure(self, output_config: OutputDirectory) -> bool:
        """Ensure server-managed directory structure exists on client"""
        ...

class OutputQueryPort(Protocol):
    async def get_output_path(self, directory_name: str) -> str | None:
        """Get path for a specific managed output directory"""
        ...
```

#### Imperative Shell (Context Operations)
```python
# src/shell/orchestrators/output_orchestrator.py
from typing import Annotated
from fastmcp.context import Context
from src.core.ports.output_ports import OutputCommandPort, OutputQueryPort
from src.core.models import OutputDirectory

class OutputOrchestrator(OutputCommandPort, OutputQueryPort):
    """Orchestrator for server-managed output directory operations using Context"""
    
    def __init__(self, ctx: Annotated[Context, "FastMCP context object"]):
        self.ctx = ctx

    async def ensure_directory_structure(self, output_config: OutputDirectory) -> bool:
        """Ensure directory structure exists using client Context"""
        try:
            # Create main directory
            directory_result = await self.ctx.sample(f"""
            Ação: Criar estrutura de diretórios para o MCP server
            Diretório base: {output_config.base_path}
            Subdiretórios necessários: {list(output_config.subdirectories)}
            
            Instruções:
            1. Verifique se o diretório base já existe
            2. Se não existir, crie-o com permissões adequadas
            3. Para cada subdiretório, verifique se existe e crie se necessário
            4. Retorne um JSON com o status da operação e caminhos criados/env
            5. Se falhar, retorne o erro específico
            
            Formato de resposta esperado:
            {{
              "success": true/false,
              "created_directories": ["caminho1", "caminho2"],
              "error": "mensagem de erro se aplicável"
            }}
            """)
            
            if not directory_result.get("success", False):
                error_msg = directory_result.get("error", "Falha desconhecida na criação de diretórios")
                await self.ctx.error(f"Erro ao criar diretórios: {error_msg}")
                return False

            # Create README in base directory
            readme_result = await self._create_readme(output_config)
            
            await self.ctx.info(f"✅ Estrutura de diretórios criada com sucesso: {output_config.base_path}")
            return readme_result
            
        except Exception as e:
            await self.ctx.error(f"Exceção ao criar estrutura de diretórios: {str(e)}")
            return False

    async def _create_readme(self, output_config: OutputDirectory) -> bool:
        """Create README.md in the base directory using Context"""
        try:
            readme_result = await self.ctx.sample(f"""
            Ação: Criar arquivo README.md na raiz do diretório de output
            Caminho: {output_config.base_path}/README.md
            Conteúdo:
            {output_config.readme_content}
            
            Instruções:
            1. Verifique se o arquivo já existe
            2. Se existir, faça backup antes de sobrescrever (opcional)
            3. Crie/Atualize o arquivo com o conteúdo fornecido
            4. Use codificação UTF-8
            5. Retorne status da operação
            
            Formato de resposta esperado:
            {{
              "success": true/false,
              "file_path": "{output_config.base_path}/README.md",
              "bytes_written": 1234,
              "error": "mensagem de erro se aplicável"
            }}
            """)
            
            if readme_result.get("success", False):
                await self.ctx.info(f"✅ README.md criado em {output_config.base_path}/README.md")
                return True
            else:
                error_msg = readme_result.get("error", "Falha desconhecida na criação do README")
                await self.ctx.warning(f"⚠️ README.md não criado: {error_msg}")
                return False
                
        except Exception as e:
            await self.ctx.warning(f"⚠️ Falha ao criar README.md: {str(e)}")
            return False

    async def get_output_path(self, directory_name: str) -> str | None:
        """Get path for a specific managed output directory"""
        # Implementation would return the correct path based on configuration
        base_path = f"{self.ctx.sample.__module__}/ctxfy"  # Simplified for example
        return f"{base_path}/{directory_name}"
```

### Implementation Details

#### Core Capabilities (Following FastMCP Context)

✅ **Alinhamento com Documentação**: Usa ctx.sample() conforme documentação oficial para operações no client-side

✅ **Acesso ao Filesystem do Client**: Reconhece que o servidor MCP não tem acesso direto ao filesystem do client

✅ **Injeção de Dependência**: Segue o padrão da documentação usando Annotated[Context, "description"]

✅ **Segurança**: Valida todas as operações através do client e trata erros adequadamente

✅ **Logging**: Usa ctx.info(), ctx.warning(), ctx.error() para feedback contínuo

✅ **README na raiz**: Cria README.md em ctxfy/README.md conforme solicitado

#### Client-side Configuration (MCP Server)

```
{
  "mcpServers": {
    "context-engineering": {
      "httpUrl": "http://127.0.0.1:8000/mcp",
      "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      },
      "timeout": 30000,
      "trust": false
    }
  }
}
```

#### Critérios de Aceitação Atualizados

✅ **Criação de diretórios via Context**: O servidor solicita ao client que crie ctxfy/ e ctxfy/specifications/ usando ctx.sample()

✅ **README na raiz via Context**: Arquivo ctxfy/README.md criado na raiz do diretório usando solicitações ao client

✅ **Separação clara de responsabilidades**: Client executa operações de filesystem, servidor gerencia a lógica

✅ **Flexibilidade de inputs**: Arquivos de entrada podem ser referenciados de qualquer local do filesystem

✅ **Segurança validada**: Todas as operações são validadas através do Context antes de executar

✅ **Documentação clara**: README.md na raiz explica todas as responsabilidades e limitações

✅ **Testes completos**: Verifica operações de filesystem através do Context, tratamento de erros e validações

✅ **Logging contínuo**: Usa métodos de logging do Context (ctx.info(), ctx.error()) para monitoramento em tempo real

## 🚀 Vantagens da Implementação com Context do FastMCP

### 1. Alinhamento com Arquitetura MCP

✅ **Modelo Correto**: Segue o princípio de que o client possui o filesystem, o servidor gerencia a lógica

✅ **Progressive Disclosure**: Carrega apenas o contexto necessário quando necessário

✅ **Segurança por Design**: Nunca assume acesso direto ao filesystem do client

### 2. Robustez e Confiabilidade

✅ **Tratamento de Erros**: Captura e relata todos os erros através do Context

✅ **Validação Contínua**: Verifica existência de diretórios antes de operações

✅ **Feedback em Tempo Real**: Usa logging do Context para monitorar progresso

### 3. Escalabilidade Futura

✅ **Base para Funcionalidades**: Estrutura preparada para implementação de funcionalidades reutilizáveis

✅ **State persistence**: Pode evoluir para persistência de estado através de operações no client

✅ **Multi-client support**: Funciona com qualquer client que suporte o protocolo MCP

### 4. Facilidade de Manutenção

✅ **Código Limpo**: Separação clara entre lógica de negócio e operações de filesystem

✅ **Documentação Automática**: O Context fornece logs detalhados para troubleshooting

✅ **Testabilidade**: Funções podem ser testadas com mocks do Context

## 🧪 Testing Strategy

Following the testing strategy rules:

- **Unit tests (≥70% of suite)**: Target Functional Core with pure functions
  * Pure functions → no mocks, no setup
  * Must pass in <100ms each
  * Name pattern: `test_<function>_<scenario>_<expectation>`

- **Integration tests (≤25%)**: Test Core + Context Adapter combinations
  * Use real/fake Context adapters — no mocks of domain logic
  * Test boundaries between components

- **End-to-end tests (≤5%)**: Full workflow validation
  * Test critical paths only
  * Execute against production-like environment

### Acceptance Tests Example
```python
def test_create_output_directory_with_context():
    # Create in-memory Context mock to test the orchestrator
    mock_ctx = MockContext()
    orchestrator = OutputOrchestrator(mock_ctx)
    
    output_config = OutputDirectory(
        base_path="./ctxfy",
        subdirectories=("specifications", "skills", "cache"),
        readme_content="# Generated by MCP Server..."
    )
    
    success = await orchestrator.ensure_directory_structure(output_config)
    assert success is True
    # Additional assertions for expected operations
```

## 🏗️ Package Architecture

Following package architecture principles:
```
src/
├── core/                 # Most stable: models, exceptions, pure services
│   ├── models.py         # Immutable value objects and entities
│   ├── use_cases.py      # Pure functions implementing business rules
│   └── ports/            # Interfaces only (Protocols)
│       ├── output_ports.py
│       └── filesystem_ports.py
├── shell/               # Orchestrators coordinating workflows
│   ├── workflows/       # Pure workflow definitions
│   └── orchestrators/   # Imperative workflow coordinators
│       └── output_orchestrator.py
├── adapters/            # Context implementations of core ports
│   └── context/         # FastMCP Context operations
│       └── filesystem_adapter.py
└── app.py               # Composition root for dependency injection
```

## 🔒 Immutable Value Objects

All core data classes must be immutable:
- Use `@dataclass(frozen=True)` for all value objects
- Validate invariants in `__post_init__` or dedicated factory methods
- Never expose mutable collections — convert to `tuple`, `frozenset` or return defensive copies

## 🔄 Functional Core & Imperative Shell

### Core functions must be:
- Pure (no I/O, no mutation of inputs, no time/random)
- Small (≤15 lines; ≤3 parameters)
- Named with clear verb + domain object
- Follow CQS: Queries vs. Commands — never both

### Shell functions must be:
- Thin wrappers (≤25 lines) around core logic
- Responsible for: Context I/O, error translation, logging, client operations
- Contain `try/except` blocks only — extracted into helpers

This implementation ensures the server can manage output directories through client-side operations using FastMCP Context, maintaining proper architectural boundaries while providing the required functionality.