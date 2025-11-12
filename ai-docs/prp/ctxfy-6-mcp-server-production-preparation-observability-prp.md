# 🚀 PRP - BACKEND DEVELOPMENT

## 🏷️ PRP Metadata
PRP ID: PRP-MCP-SERVER-PROD-PREP-001
Type: Backend Development
Domain: AI Infrastructure & Model Context Protocol
Technology Stack: Python 3.13/FastMCP 2.13.0/HTTPX
Complexity Level: High

## ✨ AI Context Adaptation
### Model Compatibility Notes
- Claude 3: Excellent for complex business logic, may need detailed examples for MCP protocol implementation and observability features
- GPT-4: Better for architectural patterns, but may be more creative than desired with FastMCP specifics
- Llama 3: Good for consistent code, but may need more domain context for MCP protocol and monitoring
- **Strategy**: Provide concrete examples and strict acceptance criteria for all models, particularly for FastMCP integration, OpenAPI documentation, structured logging, and authentication systems

### Context Drift Mitigation
- Include specific dependency versions (e.g., FastMCP==2.13.0, structlog==24.4.0, prometheus-client==0.22.0)
- Provide current code examples instead of generic patterns
- Explicitly define what should NOT be done (e.g., direct LLM API access without ctx.sample(), mutable value objects in core, unstructured logging)
- Test PRP with multiple models before production

## 🎯 Business Context Layer
### Business Objectives
Implement production preparation and observability features for the ctxfy MCP Server including OpenAPI documentation, structured logging with request IDs and latency metrics, authentication middleware with API keys, schema validation, and Docker containerization, following Hexagonal Architecture patterns to enable robust, secure MCP server deployment with comprehensive monitoring and documentation for production environments. The system must meet <200ms p95 performance requirement and achieve 99.9% availability.

### SLAs & Performance Requirements
Availability: 99.9% - including maintenance window
Latency: < 200ms p95 for prompt processing, < 50ms for health checks and metrics endpoints
Throughput: 500 req/sec peak, 100 req/sec average for MCP operations with authentication
Data Freshness: < 1s for health status updates and metrics collection
Error Rate: < 0.05% for critical operations

### 👥 Stakeholder Analysis
#### Technical Stakeholders
- **Frontend Team**: Needs consistent MCP endpoints with request/response examples for client implementation
- **DevOps/SRE**: Requires detailed health checks, structured logging (JSON format), observability metrics at `/metrics`, and Docker containerization for deployment
- **Security Team**: Mandates MCP protocol compliance, audit of all LLM operations, API key validation with different scopes, and injection prevention through schema validation
- **AI/ML Engineering**: Needs ctx.sample() integration for LLM processing workflows with performance metrics and request tracking

#### Business Stakeholders
- **Product Managers**: Focus on launch time and scalability for MCP services with comprehensive documentation at `/docs`
- **Engineering Leadership**: Interested in standardized MCP implementations with proper monitoring and security
- **Executive Sponsors**: Interested in operational efficiency through comprehensive observability and security compliance
- **Compliance Team**: Requires audit trails and structured logging for all operations with request correlation

### 📋 Requirement Extraction
#### API & Interface Specifications
- MCP protocol endpoints with FastMCP automatic handling
- `/health` endpoint for server health monitoring
- `/docs` endpoint for OpenAPI 3.0 documentation of all registered prompts
- `/metrics` endpoint for Prometheus metrics collection
- `@mcp.prompt` decorator functionality for prompt registration with parameterized variables
- ctx.sample() integration for LLM text generation with structured input/output
- API key validation in request headers with scope-based authorization

#### Data Models & Entities
```python
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, Any
import uuid
from datetime import datetime

@dataclass(frozen=True)
class PromptRequest:
    """Immutable value object for MCP prompt requests following our core architecture principles"""
    prompt_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    parameters: dict
    api_key: Optional[str] = None
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Prompt name must be a valid string")
        if not isinstance(self.parameters, dict):
            raise ValueError("Parameters must be a dictionary")
        if self.api_key is not None and (not isinstance(self.api_key, str) or len(self.api_key) == 0):
            raise ValueError("API key must be a non-empty string if provided")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")

@dataclass(frozen=True)
class PromptResponse:
    """Immutable value object for MCP prompt responses following our core architecture principles"""
    request_id: str
    result: str
    latency_ms: float
    llm_model: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")
        if not isinstance(self.result, str):
            raise ValueError("Result must be a string")
        if not isinstance(self.latency_ms, (int, float)) or self.latency_ms < 0:
            raise ValueError("Latency must be a non-negative number")
        if not self.llm_model or not isinstance(self.llm_model, str):
            raise ValueError("LLM model must be a valid string")

@dataclass(frozen=True)
class HealthStatus:
    """Immutable value object for health status following our core architecture principles"""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    timestamp: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0
    version: str = "1.0.0"
    checks: Dict[str, Any] = field(default_factory=dict)  # Detailed health checks

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if self.status not in ['healthy', 'degraded', 'unhealthy']:
            raise ValueError("Status must be 'healthy', 'degraded', or 'unhealthy'")
        if self.uptime_seconds < 0:
            raise ValueError("Uptime must be non-negative")
        if not self.version or not isinstance(self.version, str):
            raise ValueError("Version must be a valid string")

@dataclass(frozen=True)
class ApiKeyInfo:
    """Immutable value object for API key information following our core architecture principles"""
    key_id: str
    api_key_hash: str  # Hashed API key for security
    user_id: str
    created_at: datetime
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    scope: str  # read, write, admin

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.key_id or not isinstance(self.key_id, str):
            raise ValueError("Key ID must be a valid string")
        if not self.api_key_hash or not isinstance(self.api_key_hash, str):
            raise ValueError("API key hash must be a valid string")
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("User ID must be a valid string")
        if self.scope not in ['read', 'write', 'admin']:
            raise ValueError("Scope must be 'read', 'write', or 'admin'")

@dataclass(frozen=True)
class LogEntry:
    """Immutable value object for structured logging following our core architecture principles"""
    timestamp: datetime
    level: str  # INFO, ERROR, DEBUG, WARNING
    message: str
    request_id: str
    latency_ms: float
    user_id: Optional[str] = None
    endpoint: Optional[str] = None
    llm_model: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if self.level not in ['INFO', 'ERROR', 'DEBUG', 'WARNING']:
            raise ValueError("Log level must be INFO, ERROR, DEBUG, or WARNING")
        if not self.message or not isinstance(self.message, str):
            raise ValueError("Message must be a valid string")
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("Request ID must be a valid string")
        if not isinstance(self.latency_ms, (int, float)) or self.latency_ms < 0:
            raise ValueError("Latency must be a non-negative number")
        if self.extra is None:
            raise ValueError("Extra fields must be a dictionary")

@dataclass(frozen=True)
class Metric:
    """Immutable value object for metrics collection following our core architecture principles"""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Metric name must be a valid string")
        if not isinstance(self.value, (int, float)):
            raise ValueError("Metric value must be a number")
        if not isinstance(self.labels, dict):
            raise ValueError("Labels must be a dictionary")

@dataclass(frozen=True)
class ValidationResult:
    """Immutable value object for validation results following our core architecture principles"""
    is_valid: bool
    errors: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not isinstance(self.is_valid, bool):
            raise ValueError("is_valid must be a boolean")
        if not isinstance(self.errors, tuple):
            raise ValueError("errors must be a tuple")
```

#### External Dependencies
- FastMCP: For MCP protocol implementation (version 2.13.0) - SLA 99.9%
- HTTPX: For asynchronous HTTP operations - version 0.27+
- structlog: For structured JSON logging with consistent format
- prometheus-client: For metrics collection and exposition
- cryptography: For secure API key generation and handling
- pydantic: For schema validation of prompt requests
- uvicorn: For serving the application with OpenAPI documentation

### 🔍 RAG Integration Section
#### Documentation Sources
Primary Sources:
- https://gofastmcp.com/llms.txt (FastMCP framework documentation)
- https://modelcontextprotocol.com/ (MCP protocol specifications)
- https://docs.pydantic.dev/latest/ (Pydantic validation framework)
- https://www.structlog.org/ (Structured logging with JSON format)
- https://prometheus.io/docs/instrumenting/clientlibs/ (Prometheus metrics collection)

Internal Knowledge:
- /ai_docs/core-architecture-principles.md (Hexagonal Architecture rules)
- /ai_docs/functional-code-imperative-shell.md (FCIS pattern implementation)
- /ai_docs/immutable-value-objects.md (Value object standards)
- /ai_docs/testing-strategy.md (TDD and testing requirements)
- /ai_docs/orchestrator-pattern-for-imperative-shell.md (Workflow coordination patterns)
- /ai_docs/tasks/ctxfy-6-mcp-server-production-preparation-observability.md (Technical specification)

#### Retrieval Protocol
1. For each technical term mentioned, search official FastMCP documentation
2. Validate MCP protocol compliance with spec
3. Check version compatibility before implementing
4. If conflict between sources, prioritize official documentation + internal standards

## 🔧 Technical Translation
### Architecture Pattern
- Pattern: Hexagonal Architecture with Ports & Adapters
- Primary Ports: MCPServerPort, MCPHealthPort, AuthCommandPort, LoggingPort, MetricsPort (driving ports)
- Secondary Ports: LoggingPort, LLMAdapterPort, AuthRepositoryPort, MetricsCollectorPort (driven ports)
- MCP Integration: FastMCP framework for protocol handling with authentication middleware
- Logging Strategy: Structured JSON logging with request_id, latency_ms, llm_model, and user_id for operational visibility and audit trails

### Technology Specifications
Framework: FastMCP 2.13.0 with async support and OpenAPI documentation
Runtime: Python 3.13+
Configuration: Poetry for dependency management
Messaging: FastMCP internal messaging for MCP protocol
Observability: Structured JSON logging (structlog) with request tracking, Prometheus metrics collection
Documentation: OpenAPI 3.0 generation at `/docs` endpoint
Containerization: Docker with security best practices and health checks

### Security Specifications
Authentication: API key validation middleware with different access scopes (read/write/admin)
Authorization: MCP client verification with scope-based permissions
Data Protection: API keys stored as hashes, encrypted at rest, secure generation
Audit Logging: Structured logs for all MCP operations with required fields (request_id, latency_ms, user_id)
Schema Validation: Input validation for prompt requests to prevent injection attacks

### Performance Considerations
- Async Processing: All MCP operations handled asynchronously with proper connection management
- Connection Management: FastMCP manages client connections with proper resource cleanup
- Memory Management: Efficient handling of concurrent requests with request ID correlation
- Response Caching: Selective caching for health checks and metrics endpoints only
- Metrics Collection: Efficient collection without impacting request performance

### 📝 Specification Output
#### Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ 1. Core Implementation:
- Complete MCP server foundation with FastMCP integration and production-ready features
- OpenAPI 3.0 documentation available at `/docs` endpoint with comprehensive prompt documentation

⭐ 2. Authentication & Security:
- API key validation middleware supporting different scopes (read, write, admin)
- Secure API key generation and storage with proper hashing
- Schema validation for all prompt requests to prevent injection attacks

⭐ 3. Monitoring & Observability:
- JSON structured logging with required fields: request_id, latency_ms, llm_model, timestamp, level, user_id
- Metrics collection available at `/metrics` endpoint in Prometheus format
- Health monitoring endpoint with detailed system status

⭐ 4. Documentation & Deployment:
- Docker containerization with security best practices and health checks
- Complete OpenAPI documentation including request/response examples for all endpoints
- Configuration management for different environments (dev, staging, prod)

⭐ 5. Quality Assurance:
- Comprehensive test coverage (>85% for core domain logic) with unit, integration, and E2E tests
- Performance testing to ensure <200ms p95 response time requirement
- Security testing and validation of authentication mechanisms
- Proper error handling with meaningful error messages for debugging

## 🧱 Architecture Structure
```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── prompt_models.py     # PromptRequest, PromptResponse, etc.
│   │   ├── auth_models.py       # Authentication-related models (ApiKeyInfo, etc.)
│   │   └── monitoring_models.py # Monitoring and logging models (LogEntry, Metric)
│   ├── use_cases/        # Pure functions implementing business rules
│   │   ├── prompt_use_cases.py  # Prompt processing logic
│   │   ├── auth_use_cases.py    # Authentication logic
│   │   └── monitoring_use_cases.py # Monitoring logic
│   └── ports/            # Interfaces only (Protocols)
│       ├── prompt_ports.py      # PromptCommandPort, PromptQueryPort
│       ├── auth_ports.py        # Authentication ports (AuthCommandPort, etc.)
│       └── monitoring_ports.py  # Monitoring ports (LoggingPort, MetricsPort)
├── adapters/             # Implementations of core ports
│   ├── mcp_prompts/      # @mcp.prompt decorator implementation
│   ├── auth/             # Authentication middleware and API key management
│   ├── monitoring/       # Logging, metrics, and health monitoring
│   ├── api_docs/         # OpenAPI documentation generation
│   ├── validation/       # Schema validation for prompt requests
│   └── container/        # Docker containerization support
└── app/                  # Application composition and configuration
    ├── main.py           # Main entry point with dependency injection
    ├── config.py         # Configuration management
    └── deployment/       # Deployment scripts and configurations
```

## 📦 Dependency Specifications
### Project Dependencies (`pyproject.toml`)
```toml
[tool.poetry.dependencies]
python = "^3.13"
fastmcp = "^2.13.0"
pydantic-settings = "^2.12"
pydantic = "^2.12"
uvicorn = "^0.34.0"
prometheus-client = "^0.22.0"
structlog = "^24.4.0"
cryptography = "^42.0.0"

[tool.poetry.group.dev.dependencies]
ruff = "^0.14"
mypy = "^1.18"
pytest = "^8.4"
pytest-asyncio = "^0.23.0"
factory-boy = "^3.3.0"
```

## 🚀 Implementation Phases
### Phase 1: Core Infrastructure
1. Implement authentication middleware with API key validation
2. Set up structured logging with required fields
3. Add schema validation for prompt requests

### Phase 2: Observability
1. Implement metrics collection for prompt execution
2. Add health monitoring endpoint
3. Integrate with monitoring systems

### Phase 3: Documentation & Deployment
1. Generate OpenAPI documentation
2. Create Docker containerization
3. Set up deployment pipeline

### Phase 4: Testing & Validation
1. Implement comprehensive test suite
2. Conduct performance testing
3. Validate security features