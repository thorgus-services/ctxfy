# 🚀 PRP - BACKEND DEVELOPMENT

## 🏷️ PRP Metadata
PRP ID: PRP-MCP-SERVER-QA-001
Type: Backend Development
Domain: AI Infrastructure & Model Context Protocol
Technology Stack: Python 3.13/FastMCP 2.13.0/HTTPX
Complexity Level: High

## ✨ AI Context Adaptation
### Model Compatibility Notes
- Claude 3: Excellent for complex business logic, may need detailed examples for MCP protocol implementation and quality aspects (testing, validation, error handling)
- GPT-4: Better for architectural patterns, but may be more creative than desired with FastMCP specifics and quality requirements
- Llama 3: Good for consistent code, but may need more domain context for MCP protocol and quality assurance practices
- **Strategy**: Provide concrete examples and strict acceptance criteria for all models, particularly for FastMCP integration, comprehensive testing (>90% coverage), structured error handling, and robust input validation

### Context Drift Mitigation
- Include specific dependency versions (e.g., FastMCP==2.13.0, Python==3.13, pytest==8.0+, mypy==1.8+)
- Provide current code examples instead of generic patterns
- Explicitly define what should NOT be done (e.g., direct LLM API access without ctx.sample(), mutable value objects in core, unstructured error responses, missing input validation)
- Test PRP with multiple models before production

## 🎯 Business Context Layer
### Business Objectives
Implement comprehensive testing coverage (>90%), structured error handling, and robust input validation for the ctxfy MCP Server while maintaining Hexagonal Architecture principles and performance requirements (<200ms response time). The system must provide secure, reliable prompt processing with proper injection prevention and meaningful error responses to ensure operational stability and security compliance.

### SLAs & Performance Requirements
Availability: 99.9% - including maintenance window
Latency: < 200ms p95 for prompt processing, < 50ms for health checks
Throughput: 500 req/sec peak, 100 req/sec average for MCP operations
Data Freshness: < 1s for health status updates
Error Rate: < 0.05% for critical operations
Test Coverage: >90% for critical code paths

### 👥 Stakeholder Analysis
#### Technical Stakeholders
- **Frontend Team**: Needs consistent MCP endpoints with properly handled error responses and well-tested functionality for reliable client implementations
- **DevOps/SRE**: Requires comprehensive test coverage (>90%), structured error logging, and observability metrics for operational stability
- **Security Team**: Mandates MCP protocol compliance, audit of all LLM operations, injection prevention through robust input validation, and secure error responses that don't expose internals
- **AI/ML Engineering**: Needs ctx.sample() integration for LLM processing workflows with proper error handling and performance metrics

#### Business Stakeholders
- **Product Managers**: Focus on reliability and security of prompt processing with comprehensive test coverage to prevent production issues
- **Engineering Leadership**: Interested in quality standards, standardized MCP implementations, and maintainable code with proper error handling
- **Executive Sponsors**: Interested in operational efficiency through comprehensive testing and security compliance to prevent vulnerabilities
- **Compliance Team**: Requires audit trails, structured logging for all operations, and proper input validation to prevent injection attacks

### 📋 Requirement Extraction
#### API & Interface Specifications
- MCP protocol endpoints with FastMCP automatic handling and comprehensive testing
- `/health` endpoint for server health monitoring with detailed error reporting
- `@mcp.prompt` decorator functionality for prompt registration with parameterized variables and validation
- ctx.sample() integration for LLM text generation with structured error handling
- OpenAPI documentation for all registered prompts with proper validation examples

#### Data Models & Entities
```python
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, Any
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
        # Injection prevention: validate template content doesn't contain dangerous patterns
        if self._contains_injection_patterns(self.template_content):
            raise ValueError("Template content contains potential injection patterns")
        if not isinstance(self.variables, tuple):
            raise ValueError("Variables must be a tuple")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Description must be a valid string")
        if not self.model_name or not isinstance(self.model_name, str):
            raise ValueError("Model name must be a valid string")

    def _contains_injection_patterns(self, content: str) -> bool:
        """Prevent template injection attacks with validation"""
        dangerous_patterns = ['__import__', 'exec', 'eval', 'importlib', 'subprocess']
        content_lower = content.lower()
        return any(pattern in content_lower for pattern in dangerous_patterns)

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
        # Validate variables don't contain injection patterns
        if self._contains_dangerous_values(self.variables):
            raise ValueError("Variables contain potential injection values")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")

    def _contains_dangerous_values(self, variables: dict) -> bool:
        """Validate variables for potential injection attacks"""
        def check_value(value):
            if isinstance(value, str):
                dangerous_patterns = ['__import__', 'exec', 'eval', 'importlib', 'subprocess']
                value_lower = value.lower()
                return any(pattern in value_lower for pattern in dangerous_patterns)
            elif isinstance(value, dict):
                return any(check_value(v) for v in value.values())
            elif isinstance(value, list):
                return any(check_value(v) for v in value)
            return False
        return check_value(variables)

@dataclass(frozen=True)
class PromptResponse:
    """Immutable value object for MCP prompt responses following our core architecture principles"""
    request_id: str
    template_id: str
    result: str
    execution_time_ms: float
    error_details: Optional[str] = None

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
        if self.error_details is not None and not isinstance(self.error_details, str):
            raise ValueError("Error details must be a string if provided")

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

@dataclass(frozen=True)
class ValidationError:
    """Immutable value object for validation errors following our core architecture principles"""
    error_code: str
    message: str
    field_name: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.error_code or not isinstance(self.error_code, str):
            raise ValueError("Error code must be a valid string")
        if not self.message or not isinstance(self.message, str):
            raise ValueError("Message must be a valid string")
        if self.field_name is not None and not isinstance(self.field_name, str):
            raise ValueError("Field name must be a string if provided")

@dataclass(frozen=True)
class HealthStatus:
    """Immutable value object for health status following our core architecture principles"""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    timestamp: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0
    version: str = "1.0.0"
    checks: Dict[str, Any] = field(default_factory=dict)  # Detailed health checks
    error_details: Optional[str] = None

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if self.status not in ['healthy', 'degraded', 'unhealthy']:
            raise ValueError("Status must be 'healthy', 'degraded', or 'unhealthy'")
        if self.uptime_seconds < 0:
            raise ValueError("Uptime must be non-negative")
        if not self.version or not isinstance(self.version, str):
            raise ValueError("Version must be a valid string")
        if self.error_details is not None and not isinstance(self.error_details, str):
            raise ValueError("Error details must be a string if provided")
```

#### External Dependencies
- FastMCP: For MCP protocol implementation (version 2.13.0) - SLA 99.9%
- HTTPX: For asynchronous HTTP operations - version 0.27+
- pytest: For comprehensive test coverage (>90%)
- mypy: For static type checking with strict settings
- Structured logging: For operational visibility and monitoring
- FastAPI: For OpenAPI documentation generation

### 🔍 RAG Integration Section
#### Documentation Sources
Primary Sources:
- https://gofastmcp.com/servers/prompts.md (FastMCP prompts documentation)
- https://gofastmcp.com/servers/sampling.md (FastMCP sampling documentation)
- https://modelcontextprotocol.com/ (MCP protocol specifications)
- https://docs.pydantic.dev/latest/ (Pydantic validation framework)
- https://docs.pytest.org/en/8.0.x/ (pytest testing framework)
- https://mypy.readthedocs.io/en/stable/ (mypy static type checker)

Internal Knowledge:
- /ai_docs/core-architecture-principles.md (Hexagonal Architecture rules)
- /ai_docs/functional-code-imperative-shell.md (FCIS pattern implementation)
- /ai_docs/immutable-value-objects.md (Value object standards)
- /ai_docs/testing-strategy.md (TDD and testing requirements)
- /ai_docs/orchestrator-pattern-for-imperative-shell.md (Workflow coordination patterns)
- @ai-docs/context/ctxfy-review-1-mcp-server-context-stack-testing-error-validation.md (Current context stack)

#### Retrieval Protocol
1. For each technical term mentioned, search official FastMCP documentation and testing best practices
2. Validate MCP protocol compliance with spec
3. Check version compatibility before implementing
4. If conflict between sources, prioritize official documentation + internal standards
5. Review security best practices for input validation and error handling

## 🔧 Technical Translation
### Architecture Pattern
- Pattern: Hexagonal Architecture with Ports & Adapters emphasizing testing, error handling, and validation
- Primary Ports: MCPServerPort, MCPHealthPort (driving ports) with comprehensive testing
- Secondary Ports: LoggingPort, LLMAdapterPort (driven ports) with validation and error handling
- Testing Strategy: TDD with ≥70% unit tests (Functional Core only), ≤25% integration tests, ≤5% end-to-end tests
- Error Handling: Domain exceptions defined in core, shell translates to appropriate response formats
- Input Validation: Performed at system boundaries and in immutable value objects

### Technology Specifications
Framework: FastMCP 2.13.0 with async support and comprehensive testing
Runtime: Python 3.13+
Testing: pytest with >90% coverage, mypy with strict settings
Configuration: Poetry for dependency management with security checks
Messaging: FastMCP internal messaging for MCP protocol with error handling
Observability: Structured JSON logging with error details for operational visibility

### Security Specifications
Authentication: MCP protocol native authentication with comprehensive testing
Authorization: MCP client verification with validation
Data Protection: No sensitive data stored, all data in memory, injection prevention through validation
Audit Logging: Structured logs for all MCP operations with validation and error details

### Performance Considerations
- Async Processing: All MCP operations handled asynchronously with error handling
- Connection Management: FastMCP manages client connections with error isolation
- Memory Management: Efficient handling of concurrent requests with proper error handling
- Response Caching: No caching for prompt responses to maintain freshness while ensuring error handling
- Testing Performance: Unit tests must pass in <100ms each for functional core

### 📝 Specification Output
#### Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ 1. Core Implementation:
- Complete MCP server foundation with FastMCP integration testing
- Comprehensive unit tests (>90% coverage) for core domain logic
- Robust input validation with injection prevention
- Structured error handling with meaningful responses
- Immutable value objects for all domain models with validation

⭐ 2. Testing Implementation:
- Unit tests (≥70% of suite) for functional core only, with pure functions
- Integration tests (≤25%) for Core + Adapter combinations using real/fake adapters
- End-to-end tests (≤5%) for full workflow validation
- Performance tests to verify <200ms response times
- Security tests for injection prevention and error handling

⭐ 3. Input Validation Implementation:
- Injection prevention for template variables and user inputs
- Validation at system boundaries and in value objects
- Secure variable substitution with validation
- Error responses without exposing internal implementation details

⭐ 4. Error Handling Implementation:
- Domain exceptions defined in core (e.g., InvalidTemplateError, ValidationError)
- Shell translates domain exceptions to appropriate response formats
- Structured error responses with consistent format
- Graceful fallbacks for external service failures
- No exception handling in core functions (let exceptions propagate)

⭐ 5. Documentation & Examples:
- Complete API documentation with examples of error scenarios
- Testing strategy documentation with coverage requirements
- Error handling guidelines with examples
- Input validation rules with examples of secure usage

#### Technical Validation Criteria
- [ ] All domain models use immutable value objects (@dataclass(frozen=True))
- [ ] Input validation prevents injection attacks with pattern checks
- [ ] Error handling provides meaningful messages without exposing internals
- [ ] Unit tests pass in <100ms each
- [ ] Test coverage >90% for critical code paths
- [ ] Individual prompt requests complete within <200ms (p95 performance)
- [ ] Proper error isolation in concurrent execution environments
- [ ] No mutable collections exposed from core domain objects
- [ ] Transformation methods return new instances instead of mutation
- [ ] Type checking passes with strict mypy settings

## 🧪 Quality Assurance Requirements
### Testing Strategy
- Unit tests (≥70% of suite): Target Functional Core only
  * Pure functions → no mocks, no setup
  * Must pass in <100ms each
  * Name pattern: `test_<function>_<scenario>_<expectation>`
- Integration tests (≤25%): Test Core + Adapter combinations
  * Use real/fake adapters — no mocks of domain logic
  * Test boundaries between components
- End-to-end tests (≤5%): Full workflow validation

### Error Handling Requirements
- Domain exceptions defined in core (e.g., `InvalidTemplateError`, `ValidationError`)
- Shell translates domain exceptions to appropriate response formats
- No exception handling in core functions (let exceptions propagate)
- Structured error responses without exposing internal implementation details
- Consistent error format across all endpoints

### Input Validation Requirements
- Validate invariants in `__post_init__` or dedicated factory methods
- All core data classes must be immutable using `@dataclass(frozen=True)`
- Never expose mutable collections — convert to `tuple`, `frozenset` or return defensive copies
- Use transformation methods that return new instances instead of mutation
- Injection prevention for template content and variable substitution

## 🎯 Success Criteria
### Functional Requirements
- [ ] Core use cases have >90% test coverage with comprehensive unit and integration tests
- [ ] Input validation thoroughly handles edge cases and prevents template injection attacks
- [ ] Error handling provides meaningful, actionable messages without exposing internal details
- [ ] Variable substitution is secure against injection with proper validation
- [ ] All domain models validate inputs thoroughly as per architecture rules

### Non-Functional Requirements
- [ ] Individual prompt requests complete within <200ms (p95 performance requirement)
- [ ] System supports concurrent prompt execution with proper error isolation
- [ ] Proper error handling with meaningful messages for debugging
- [ ] 90%+ test coverage for core domain logic
- [ ] Zero critical security vulnerabilities related to input validation
- [ ] Comprehensive logging with error details for operational visibility
- [ ] All tests pass in under reasonable time constraints (<100ms for unit tests)