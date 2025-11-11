# 🚀 PRP - BACKEND DEVELOPMENT

## 🏷️ PRP Metadata
PRP ID: PRP-MCP-PROMPTS-CTXFY-001
Type: Backend Development
Domain: AI/LLM Integration & Model Context Protocol
Technology Stack: Python 3.13/FastMCP 2.13.0/HTTPX
Complexity Level: High

## ✨ AI Context Adaptation
### Model Compatibility Notes
- Claude 3: Excellent for complex business logic, may need detailed examples for MCP protocol implementation and `@mcp.prompt` decorator
- GPT-4: Better for architectural patterns, but may be more creative than desired with FastMCP specifics
- Llama 3: Good for consistent code, but may need more domain context for MCP protocol and variable substitution
- **Strategy**: Provide concrete examples and strict acceptance criteria for all models, particularly for FastMCP integration and MCP protocol compliance

### Context Drift Mitigation
- Include specific dependency versions (e.g., FastMCP==2.13.0, Python==3.13)
- Provide current code examples instead of generic patterns
- Explicitly define what should NOT be done (e.g., direct LLM API access without ctx.sample(), mutable value objects in core)
- Test PRP with multiple models before production

## 🎯 Business Context Layer
### Business Objectives
Implement a robust, extensible prompt system using FastMCP framework with emphasis on reusable prompt templates and variable substitution through `@mcp.prompt` decorator and `ctx.sample()` integration, enabling scalable AI/LLM integrations with standardized architecture patterns while ensuring performance and security compliance.

### SLAs & Performance Requirements
Availability: 99.9% - including maintenance window
Latency: < 200ms p95 for prompt processing, < 50ms for health checks
Throughput: 500 req/sec peak, 100 req/sec average for prompt operations
Data Freshness: < 1s for health status updates
Error Rate: < 0.05% for critical operations

### 👥 Stakeholder Analysis
#### Technical Stakeholders
- **Frontend Team**: Needs consistent MCP endpoints with request/response examples for client implementation
- **DevOps/SRE**: Requires detailed health checks, structured logging, and observability metrics for prompt operations
- **Security Team**: Mandates MCP protocol compliance, audit of all LLM operations and injection prevention
- **AI/ML Engineering**: Needs ctx.sample() integration for LLM processing workflows with performance metrics

#### Business Stakeholders
- **Product Managers**: Focus on launch time and scalability for prompt-based services
- **Engineering Leadership**: Interested in standardized MCP implementations and extensibility
- **Executive Sponsors**: Interested in ROI through prompt reusability and operational efficiency
- **Compliance Team**: Requires audit trails and structured logging for all operations

### 📋 Requirement Extraction
#### API & Interface Specifications
- MCP protocol endpoints with FastMCP automatic handling
- `/health` endpoint for server health monitoring
- `@mcp.prompt` decorator functionality for prompt registration with variable substitution
- ctx.sample() integration for LLM text generation with structured input/output
- OpenAPI documentation for all registered prompts

#### Data Models & Entities
```python
from dataclasses import dataclass, field
from typing import Optional, Tuple
import uuid
from datetime import datetime

@dataclass(frozen=True)
class PromptTemplate:
    """Immutable value object for MCP prompt templates following our core architecture principles"""
    template_id: str
    template_content: str
    variables: Tuple['Variable', ...]
    description: str
    model_name: str

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.template_id or not isinstance(self.template_id, str):
            raise ValueError("Template ID must be a valid string")
        if not self.template_content or not isinstance(self.template_content, str):
            raise ValueError("Template content must be a valid string")
        if not isinstance(self.variables, tuple):
            raise ValueError("Variables must be a tuple")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Description must be a valid string")
        if not self.model_name or not isinstance(self.model_name, str):
            raise ValueError("Model name must be a valid string")

@dataclass(frozen=True)
class PromptRequest:
    """Immutable value object for MCP prompt requests following our core architecture principles"""
    template_id: str
    variables: dict
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.template_id or not isinstance(self.template_id, str):
            raise ValueError("Template ID must be a valid string")
        if not isinstance(self.variables, dict):
            raise ValueError("Variables must be a dictionary")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")

@dataclass(frozen=True)
class PromptResponse:
    """Immutable value object for MCP prompt responses following our core architecture principles"""
    request_id: str
    template_id: str
    result: str
    execution_time_ms: float

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")
        if not self.template_id or not isinstance(self.template_id, str):
            raise ValueError("Template ID must be a valid string")
        if not isinstance(self.result, str):
            raise ValueError("Result must be a string")
        if not isinstance(self.execution_time_ms, (int, float)) or self.execution_time_ms < 0:
            raise ValueError("Execution time must be a non-negative number")

@dataclass(frozen=True)
class Variable:
    """Immutable value object for template variables following our core architecture principles"""
    name: str
    type_hint: str
    default_value: Optional[object] = None
    description: str = ""
    required: bool = True

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Variable name must be a valid string")
        if not self.type_hint or not isinstance(self.type_hint, str):
            raise ValueError("Type hint must be a valid string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.required, bool):
            raise ValueError("Required must be a boolean value")
```

#### External Dependencies
- FastMCP: For MCP protocol implementation (version 2.13.0) - SLA 99.9%
- HTTPX: For asynchronous HTTP operations - version 0.27+
- Structured logging: For operational visibility and monitoring
- FastAPI: For OpenAPI documentation generation

### 🔍 RAG Integration Section
#### Documentation Sources
Primary Sources:
- https://gofastmcp.com/servers/prompts.md (FastMCP prompts documentation)
- https://gofastmcp.com/servers/sampling.md (FastMCP sampling documentation)
- https://modelcontextprotocol.com/ (MCP protocol specifications)
- https://docs.pydantic.dev/latest/ (Pydantic validation framework)

Internal Knowledge:
- /ai_docs/core-architecture-principles.md (Hexagonal Architecture rules)
- /ai_docs/functional-code-imperative-shell.md (FCIS pattern implementation)
- /ai_docs/immutable-value-objects.md (Value object standards)
- /ai_docs/testing-strategy.md (TDD and testing requirements)
- /ai_docs/orchestrator-pattern-for-imperative-shell.md (Workflow coordination patterns)
- /ai_docs/tasks/ctxfy-5-mcp-reusable-prompts-technical-specification.md (Technical specification)

#### Retrieval Protocol
1. For each technical term mentioned, search official FastMCP documentation
2. Validate MCP protocol compliance with spec
3. Check version compatibility before implementing
4. If conflict between sources, prioritize official documentation + internal standards

## 🔧 Technical Translation
### Architecture Pattern
- Pattern: Hexagonal Architecture with Ports & Adapters
- Primary Ports: PromptCommandPort, PromptQueryPort (driving ports)
- Secondary Ports: PromptRegistryPort, LLMAdapterPort, TemplateEnginePort (driven ports)
- MCP Integration: FastMCP framework for protocol handling and @mcp.prompt decorator
- Logging Strategy: Structured JSON logging with prompt_id, execution_time_ms, model_name

### Technology Specifications
Framework: FastMCP 2.13.0 with async support
Runtime: Python 3.13+
Configuration: Poetry for dependency management
Messaging: FastMCP internal messaging for MCP protocol
Observability: Structured JSON logging for operational visibility

### Security Specifications
Authentication: MCP protocol native authentication
Authorization: MCP client verification
Data Protection: Template injection prevention through safe variable substitution
Audit Logging: Structured logs for all prompt operations with required fields

### Performance Considerations
- Async Processing: All MCP operations handled asynchronously
- Connection Management: FastMCP manages client connections
- Memory Management: Efficient handling of concurrent prompt requests
- Response Caching: Optional caching for frequently used template substitutions
- Variable Substitution: Optimized to prevent bottlenecks under load

### 📝 Specification Output
#### Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ 1. Core Implementation:
- Complete prompt system with FastMCP integration
- `@mcp.prompt` decorator functionality with variable substitution
- Immutable value objects for prompt templates and requests
- Proper error handling with appropriate HTTP codes

⭐ 2. Test Suite:
- Unit tests for business logic (90%+ coverage, pure functions only)
- Integration tests for complete prompt flows (real/fake adapters, no mocks of core logic)
- ctx.sample() functionality tests with performance validation
- Template injection security tests

⭐ 3. Architecture Implementation:
- Hexagonal architecture with proper boundaries
- Immutable value objects with @dataclass(frozen=True)
- Protocol-based ports for dependency inversion
- Functional Core & Imperative Shell patterns

4. Documentation:
- Complete OpenAPI specification for registered prompts
- Architecture Decision Record (ADR) explaining choices
- User guide for creating and using prompt templates
- Troubleshooting section with common scenarios

#### Code Structure Guidelines
```
src/
├── core/                  # Pure domain: functions, value objects, exceptions
│   ├── models/            # Immutable value objects (@dataclass(frozen=True))
│   │   ├── prompt_models.py     # Prompt related models
│   │   └── variable_models.py   # Variable related models
│   ├── use_cases/         # Pure functions implementing business rules
│   │   └── prompt_use_cases.py  # Prompt processing logic
│   └── ports/             # Interfaces only (Protocols)
│       └── prompt_ports.py      # PromptCommandPort, PromptQueryPort
├── adapters/              # Implementations of core ports
│   ├── mcp_prompts/       # @mcp.prompt decorator implementation
│   │   └── prompt_decorator.py
│   ├── prompt_registry/   # Prompt template registry
│   │   └── prompt_registry.py
│   ├── template_engine/   # Template rendering and variable substitution
│   │   └── template_renderer.py
│   ├── llm_sampling/      # ctx.sample() adapter implementation
│   │   └── llm_sampler.py
│   └── openapi_docs/      # OpenAPI documentation for prompts
│       └── prompt_docs.py
└── app/                   # Application composition and configuration
```

## ✅ Validation Framework
### Testing Strategy (⭐ = mandatory for simple tasks)
⭐ TDD Process (mandatory):
- Red: Write failing acceptance test against primary port
- Green: Implement minimal code to pass test (no refactoring yet)
- Refactor: Improve structure while keeping tests green

⭐ Unit Testing (≥70% of suite):
- Target Functional Core only (pure functions, no dependencies)
- Must pass in <100ms each
- Test edge cases: invalid templates, missing variables, performance limits
- Name pattern: test_<function>_<scenario>_<expectation>
- Example:
```python
def test_prompt_template_with_valid_data_creates_instance():
    variables = (Variable("name", "string"),)
    template = PromptTemplate(
        template_id="test.id",
        template_content="Hello {name}",
        variables=variables,
        description="Test template",
        model_name="gpt-4o"
    )
    assert template.template_id == "test.id"
    assert template.template_content == "Hello {name}"
```

⭐ Integration Testing (≤25%):
- Test Core + Adapter combinations (real/fake adapters, no mocks of domain logic)
- Test boundaries between components
- Validate integration with FastMCP framework and ctx.sample() functionality
- Test failure scenarios: LLM unavailable, template parsing errors

⭐ Acceptance Testing:
- Call primary ports directly (bypassing HTTP/CLI)
- Test critical paths only
- Execute against production-like environment

Security Testing:
- Test template injection prevention
- Validate that all user input is properly sanitized
- Verify that malicious templates cannot execute arbitrary code

Performance Testing:
- Load test with 500 req/sec for 5 minutes
- Verify p95 response time < 200ms for prompt execution
- Monitor for memory leaks during prolonged execution

### Quality Gates (⭐ = mandatory for simple tasks)
⭐ Code Quality:
- 0 critical/high issues in SonarQube
- Ruff formatting compliance (line length 88, no unused imports)
- Mypy strict mode passing for core packages
- 90%+ general test coverage, 95%+ for critical code
- Code review by at least 2 senior people

⭐ Security Gates:
- Zero high/critical vulnerabilities in SAST/DAST scan (Bandit + Safety)
- All dependencies updated (no known CVEs in Safety check)
- Secrets management validated (no hardcoded credentials)
- Pydantic models used ONLY at boundaries, not in core logic

⭐ Architecture Compliance:
- Core package has no dependencies on infrastructure packages
- No circular dependencies between packages
- Primary ports named as `*CommandPort`, `*QueryPort`
- Secondary ports named as `*GatewayPort`, `*RepositoryPort`, `*PublisherPort`
- Value objects are immutable (`@dataclass(frozen=True)`)

Documentation Gates:
- OpenAPI spec validated with Spectral
- Architecture Decision Record updated
- User guide with real usage examples

### Security Requirements (⭐ = mandatory for simple tasks)
⭐ Input Validation:
- All prompt registration validates templates with proper syntax checking
- Data sanitization to prevent template injection
- Rate limiting by IP and user ID (token bucket algorithm)

⭐ Authentication/Authorization:
- MCP protocol validation on all protected endpoints
- Proper client authentication for prompt registration
- Authorization for prompt execution based on MCP client permissions

⭐ Data Protection:
- Template variables are validated before substitution
- Sensitive data never exposed in logs or responses
- TLS 1.3+ mandatory for all communications
- Never expose mutable collections (convert to tuple/frozenset)

Audit & Monitoring:
- Logging of all prompt registration and execution operations
- Real-time alerts for suspicious patterns (many failed prompts)
- Log retention for 90 days for compliance)

### ⚠️ Known Gotchas & Risk Mitigation
#### Common Pitfalls (⭐ = mandatory for simple tasks)
⭐ TDD Violations:
- Pitfall: Writing implementation before tests "to explore the problem"
- Mitigation: Start with failing acceptance test against primary port

⭐ Architecture Violations:
- Pitfall: Domain/core objects importing infrastructure packages
- Mitigation: Enforce package boundaries with dependency tests
- Detection: Use import-linter to prevent illegal imports

⭐ Immutability Violations:
- Pitfall: Direct mutation of value objects (template.content = "new")
- Mitigation: Use transformation methods that return new instances
- Detection: Unit tests that attempt to modify frozen dataclasses

Testing Anti-patterns:
- Pitfall: Mocking core logic (mock.patch('core.substitute_variables'))
- Mitigation: Test pure functions directly, use real/fake adapters for integration
- Detection: Code review checklist for test anti-patterns)

## 🔄 Execution Context
### Prerequisites (⭐ = mandatory for simple tasks)
⭐ Development Setup:
- Python 3.13+, FastMCP 2.13.0 installed
- Poetry environment configured with dependencies from pyproject.toml
- Ruff, Mypy, Bandit, and Safety tools installed
- Ruff configuration: line-length=88, select=["E", "F", "I", "B", "C4", "T20"]
- Mypy configuration: strict=true for core packages

⭐ Knowledge Requirements:
- TDD process (Red → Green → Refactor)
- Hexagonal Architecture principles and port naming conventions
- Immutable value objects pattern with @dataclass(frozen=True)
- Python toolchain standards (Poetry, Ruff, Mypy, etc.)
- FastMCP framework and MCP protocol knowledge

Tooling:
- Docker for local development
- Postman/Insomnia for manual API testing
- Locust for performance testing
- import-linter for package boundary enforcement

### Development Process (⭐ = mandatory for simple tasks)
⭐ Core Implementation (follow TDD strictly):
1. Write failing acceptance test against primary port interface
2. Define immutable value objects for domain models
3. Implement core business logic as pure functions
4. Create port interfaces (Protocols) for dependencies
5. Implement adapter classes that satisfy port interfaces
6. Compose application with dependency injection in app.py

⭐ Testing & Validation:
7. Write unit tests for all pure functions (100% branch coverage)
8. Implement integration tests with real/fake adapters
9. Perform security testing with Bandit and manual review
10. Execute performance tests and optimize hotspots
11. Apply Boy Scout Rule: refactor at least one item per PR

⭐ Documentation & Deployment:
12. Update OpenAPI spec and technical documentation
13. Create Architecture Decision Record for significant choices
14. Prepare deployment scripts and configuration
15. Code review focusing on architecture compliance
16. Merge to main branch and deploy to staging
17. Final validation and production deployment

### Collaboration Points
- Security Team Review: Before any code is written, validate security architecture for template injection
- Architecture Review: Validate Hexagonal Architecture compliance and port design
- TDD Pair Programming: Work with senior developer on complex variable substitution logic
- Code Review Checklist: Include architecture compliance, TDD adherence, and Boy Scout Rule items
- Legal/Compliance Check: Validate LLM usage and data handling policies

## 📊 Success Metrics
### Performance Metrics (⭐ = mandatory for simple tasks)
⭐ Core Performance:
- Prompt execution latency: < 200ms p95
- Template registration latency: < 50ms p95
- Throughput: 500+ req/sec at peak
- Error rate: < 0.05% for critical operations

⭐ Resource Utilization:
- CPU usage: < 60% under normal load
- Memory usage: < 500MB per instance
- Database connections: < 80% of maximum pool
- Cache hit ratio: > 95% for frequently used templates

Availability:
- Uptime: 99.9% monthly
- Mean Time To Recovery (MTTR): < 5 minutes
- Incident rate: < 1 critical incident per month)

### Quality & Reliability Metrics (⭐ = mandatory for simple tasks)
⭐ Code Quality:
- Ruff formatting compliance: 100%
- Mypy strict mode passing for core: 100%
- Test coverage: 90%+ general, 95%+ for critical code
- Code quality score: A in SonarQube
- Boy Scout Rule items per PR: ≥1

⭐ Security Posture:
- Zero high/critical vulnerabilities in Bandit/Safety scans
- Average time to fix vulnerabilities: < 24h for critical
- Compliance score: 100% with internal standards

Architecture Health:
- Package dependency violations: 0
- Core package import violations: 0
- Immutable value objects usage: 100% for domain models
- TDD adherence score: 95%+ (tests before implementation))