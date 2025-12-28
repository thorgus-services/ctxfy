---
# 🚀 PRP - BACKEND DEVELOPMENT
## 🏷️ PRP Metadata
PRP ID: PRP-MCP-GEN-001
Type: Backend Development
Domain: Software Architecture & MCP Development
Technology Stack: Python 3.13/FastMCP/Pydantic
Complexity Level: High

## ✨ AI Context Adaptation
Model Compatibility Notes
- Claude 3: Excellent for complex business logic, may need detailed examples of FastMCP patterns
- GPT-4: Better for architectural patterns, but may be more creative than desired
- Llama 3: Good for consistent code, but may need more domain context on MCP specifications
- **Strategy**: Provide concrete examples of FastMCP tool implementations and strict architectural compliance requirements for all models

Context Drift Mitigation
- Include specific dependency versions (e.g., FastMCP, Pydantic)
- Provide current code examples following hexagonal architecture
- Explicitly define what should NOT be done (e.g., no mutable objects in core, no side effects in core functions)
- Test PRP with multiple models before production

## 🎯 Business Context Layer
### Business Objectives
Implement an MCP Server that automatically generates technical specifications from business requirements, reducing time to translate business needs into standardized technical documentation without manual effort, with generation of at least 5 technical specifications per day with 98% architectural compliance and response time under 1.5 seconds.

### SLAs & Performance Requirements
Availability: 99.95% - including maintenance window
Latency: < 1.5 seconds p95 for specification generation
Throughput: 5+ req/day minimum for specification generation
Error Rate: < 0.1% for critical operations

## 👥 Stakeholder Analysis
### Technical Stakeholders
- **Frontend Team**: Needs consistent endpoints for integration with CLI prompts
- **DevOps/SRE**: Requires structured logging through FastMCP Context interface
- **Security Team**: Mandates no sensitive data exposure in generated specifications
- **Data Engineering**: Needs audit trails for generation metrics

### Business Stakeholders
- **Technical Product Managers**: Focus on developer productivity and architecture compliance
- **Engineering Teams**: Need fast conversion of requirements to standardized technical specs
- **Executive Sponsors**: Interested in reduced development time and improved spec consistency

## 📋 Requirement Extraction
### API & Interface Specifications
- MCP Tools following FastMCP framework patterns
- Primary Ports for driving operations (SpecificationGenerationCommandPort, SpecificationSaveInstructionCommandPort)
- Secondary Ports for driven operations (Filesystem operations)
- Context interface for logging and progress reporting

### Data Models & Entities
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
    Immutable value object for technical specification result.
    Follows functional principles: state never changes, operations return new instances.
    """
    id: SpecificationId
    content: SpecificationContent
    filename: SpecificationFilename

    def with_updated_content(self, new_content: str) -> "SpecificationResult":
        """Return new instance with updated content"""
        return SpecificationResult(
            id=self.id,
            content=SpecificationContent(new_content),
            filename=self.filename
        )
```

### External Dependencies
- FastMCP: For MCP server framework (https://gofastmcp.com/llms.txt)
- Pydantic: For data validation
- Python 3.13+: For language features

## 🔍 RAG Integration Section
### Documentation Sources
Primary Sources:
- https://gofastmcp.com/llms.txt (FastMCP framework documentation)
- Python 3.13 documentation for language features
- https://www.cosmicpython.com/ (Hexagonal Architecture patterns)

Internal Knowledge:
- /ai_docs/rules/functional-code-imperative-shell.md (Functional Core Imperative Shell rules)
- /ai_docs/rules/immutable-value-objects.md (Immutable value object requirements)
- /ai_docs/rules/package-and-module-architecture.md (Package architecture standards)
- /ai_docs/rules/testing-strategy.md (TDD and testing requirements)

Retrieval Protocol:
1. For each FastMCP pattern mentioned, search official documentation
2. Validate architecture with Hexagonal Architecture principles
3. Check version compatibility before implementing
4. If conflict between sources, prioritize official documentation + internal standards

## 🔧 Technical Translation
### Architecture Pattern
- Pattern: Hexagonal Architecture with Ports & Adapters (Functional Core & Imperative Shell)
- Primary Ports: SpecificationGenerationCommandPort, SpecificationSaveInstructionCommandPort (driving ports)
- Secondary Ports: FilesystemPort (driven port)
- MCP Integration: FastMCP tool registration following centralized registry pattern
- Component Coordination: SpecificationOrchestrator with ≤4 dependencies

### Technology Specifications
Framework: FastMCP for MCP server implementation
Language: Python 3.13+
Validation: Pydantic for data validation at MCP boundaries
Architecture: Hexagonal Architecture with Functional Core & Imperative Shell
File Operations: Save specifications to ctxfy/specifications/ directory

### Security Specifications
Data Protection: No exposure of sensitive data in generated specifications
File Operations: Proper permissions validation for ctxfy/specifications/ directory
Input Validation: All business requirements validated before processing
JSON Formatting: Business logic for specification formatting in core components

### Performance Considerations
- Response Time: < 1.5 seconds for 95% of requests
- Core Functions: < 100ms each for pure function performance
- File Operations: Asynchronous with proper error handling
- MCP Registration: Efficient registration of tools and prompts

## 📝 Specification Output
### Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ 1. Core Implementation:
- Immutable value objects in core/models/ using @dataclass(frozen=True)
- Pure use cases in core/use_cases/ with no side effects (GenerateSpecificationUseCase containing JSON formatting logic)
- Primary and secondary ports in core/ports/ following naming conventions
- Pure workflows in core/workflows/ without side effects

⭐ 2. Shell Implementation:
- MCP tool adapter implementing SpecificationGenerationCommandPort
- Specification save instruction prompt adapter implementing SpecificationSaveInstructionCommandPort
- Specification orchestrator with ≤4 dependencies
- Centralized tool and prompt registries
- Proper Context interface usage for logging and progress reporting

⭐ 3. Test Suite:
- Unit tests for pure functions (≥70% of suite)
- Integration tests with real/fake adapters (≤25%)
- Acceptance tests against primary ports
- Performance tests validating <1.5s response time

4. MCP Integration:
- Proper tool registration with FastMCP framework
- Context handling for logging and progress
- Error propagation following FastMCP patterns

### Code Structure Guidelines
```
src/
├── core/                  # Pure domain: functions, value objects, exceptions
│   ├── models/            # Immutable value objects (@dataclass(frozen=True))
│   │   ├── specification_result.py
│   │   └── specification_workflow.py
│   ├── use_cases/         # Pure functions implementing business rules
│   │   └── generate_specification.py
│   ├── ports/             # Interfaces only (Protocols)
│   │   └── specification_ports.py
│   └── workflows/         # Pure workflow definitions
│       └── specification_workflow.py
│
├── shell/                 # Infrastructure implementations
│   ├── adapters/
│   │   ├── tools/         # MCP tool implementations
│   │   │   └── specification_generation_tool.py
│   │   └── prompts/       # FastMCP prompt implementations
│   │       └── specification_save_instruction_prompt.py
│   ├── orchestrators/     # Component coordination (≤4 deps)
│   │   └── specification_orchestrator.py
│   └── registry/          # Centralized registration
│       ├── tool_registry.py
│       └── prompt_registry.py
│
└── app.py                 # Composition root for dependency injection
```

## ✅ Validation Framework
### Testing Strategy (⭐ = mandatory for simple tasks)
⭐ TDD Process (mandatory):
- Red: Write failing acceptance test against primary port
- Green: Implement minimal code to pass test (no refactoring yet)
- Refactor: Improve structure while keeping tests green

⭐ Unit Tests:
- Target Functional Core only
- No mocking of core logic (e.g., mock.patch('core.calculate_total'))
- All tests pass in <100ms each
- Test naming: test_<function>_<scenario>_<expectation>

⭐ Integration Tests:
- Test Core + Shell adapter combinations
- Use real or fake adapters, never mocks for core
- Validate MCP tool registration and execution

Acceptance Tests:
- Validate against primary ports to ensure architectural compliance
- Performance validation for <1.5s response time
- End-to-end validation of specification generation and file saving

### Architecture Compliance:
- All domain models immutable using @dataclass(frozen=True)
- Core functions pure (no I/O, no mutation, no time/random)
- Dependencies flow inward: shell → core
- Maximum 4 dependencies per orchestrator
- No side effects in core functions
- JSON formatting logic implemented in core use case as business rule
- Proper port naming conventions followed
- SpecificationSaveInstructionPrompt component implemented for filesystem operations
- File operations occur in ctxfy/specifications/ directory as specified