# 🚀 PRP - BACKEND DEVELOPMENT

## 🏷️ PRP Metadata
PRP ID: PRP-MCP-SERVER-BASE-001
Type: Backend Development
Domain: AI Infrastructure & Model Context Protocol
Technology Stack: Python 3.13/FastMCP 2.13.0/HTTPX
Complexity Level: High

## ✨ AI Context Adaptation
Model Compatibility Notes
- Claude 3: Excellent for complex business logic, may need detailed examples for MCP protocol implementation
- GPT-4: Better for architectural patterns, but may be more creative than desired with FastMCP specifics
- Llama 3: Good for consistent code, but may need more domain context for MCP protocol
- **Strategy**: Provide concrete examples and strict acceptance criteria for all models, particularly for FastMCP integration and MCP protocol compliance

Context Drift Mitigation
- Include specific dependency versions (e.g., FastMCP==2.13.0, Python==3.13)
- Provide current code examples instead of generic patterns
- Explicitly define what should NOT be done (e.g., direct LLM API access without ctx.sample())
- Test PRP with multiple models before production

## 🎯 Business Context Layer
### Business Objectives
Implement a robust, extensible MCP server base using FastMCP framework with emphasis on prompt-based interactions and structured logging, enabling scalable AI/LLM integrations with standardized architecture patterns while ensuring operational visibility and security compliance.

### SLAs & Performance Requirements
Availability: 99.9% - including maintenance window
Latency: < 200ms p95 for prompt processing, < 50ms for health checks
Throughput: 500 req/sec peak, 100 req/sec average for MCP operations
Data Freshness: < 1s for health status updates
Error Rate: < 0.05% for critical operations

### 👥 Stakeholder Analysis
#### Technical Stakeholders
- **Frontend Team**: Needs consistent MCP endpoints with request/response examples for client implementation
- **DevOps/SRE**: Requires detailed health checks, structured logging, and observability metrics
- **Security Team**: Mandates MCP protocol compliance, audit of all LLM operations
- **AI/ML Engineering**: Needs ctx.sample() integration for LLM processing workflows

#### Business Stakeholders
- **Product Managers**: Focus on launch time and scalability for future MCP services
- **Engineering Leadership**: Interested in standardized MCP implementations and extensibility
- **Executive Sponsors**: Interested in ROI through prompt reusability and operational efficiency
- **Compliance Team**: Requires audit trails and structured logging for all operations

### 📋 Requirement Extraction
#### API & Interface Specifications
- MCP protocol endpoints with FastMCP automatic handling
- `/health` endpoint for server health monitoring
- `@mcp.prompt` decorator functionality for prompt registration
- ctx.sample() integration for LLM text generation

#### Data Models & Entities
```python
from dataclasses import dataclass, field
from typing import Optional
import uuid
from datetime import datetime

@dataclass(frozen=True)
class PromptRequest:
    """Immutable value object for MCP prompt requests following our core architecture principles"""
    prompt_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    parameters: dict
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Prompt name must be a valid string")
        if not isinstance(self.parameters, dict):
            raise ValueError("Parameters must be a dictionary")

@dataclass(frozen=True)
class PromptResponse:
    """Immutable value object for MCP prompt responses following our core architecture principles"""
    prompt_id: str
    content: str
    latency_ms: float
    llm_model: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.prompt_id or not isinstance(self.prompt_id, str):
            raise ValueError("Prompt ID must be a valid string")
        if not isinstance(self.content, str):
            raise ValueError("Content must be a string")
        if not isinstance(self.latency_ms, (int, float)) or self.latency_ms < 0:
            raise ValueError("Latency must be a non-negative number")

@dataclass(frozen=True)
class HealthStatus:
    """Immutable value object for health status following our core architecture principles"""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    timestamp: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0
    version: str = "1.0.0"

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if self.status not in ['healthy', 'degraded', 'unhealthy']:
            raise ValueError("Status must be 'healthy', 'degraded', or 'unhealthy'")
        if self.uptime_seconds < 0:
            raise ValueError("Uptime must be non-negative")
```

#### External Dependencies
- FastMCP: For MCP protocol implementation (version 2.13.0) - SLA 99.9%
- HTTPX: For asynchronous HTTP operations - version 0.27+
- Structured logging: For operational visibility and monitoring

### 🔍 RAG Integration Section
#### Documentation Sources
Primary Sources:
- https://gofastmcp.com/llms.txt (FastMCP framework documentation)
- https://modelcontextprotocol.com/ (MCP protocol specifications)
- https://docs.pydantic.dev/latest/ (Pydantic validation framework)
- https://www.cosmicpython.com/book/chapter_06_cqrs.html (Hexagonal Architecture patterns)

Internal Knowledge:
- /ai_docs/core-architecture-principles.md (Hexagonal Architecture rules)
- /ai_docs/functional-code-imperative-shell.md (FCIS pattern implementation)
- /ai_docs/immutable-value-objects.md (Value object standards)
- /ai_docs/testing-strategy.md (TDD and testing requirements)
- /ai_docs/orchestrator-pattern-for-imperative-shell.md (Workflow coordination patterns)

#### Retrieval Protocol
1. For each technical term mentioned, search official FastMCP documentation
2. Validate MCP protocol compliance with spec
3. Check version compatibility before implementing
4. If conflict between sources, prioritize official documentation + internal standards

## 🔧 Technical Translation
### Architecture Pattern
- Pattern: Hexagonal Architecture with Ports & Adapters
- Primary Ports: MCPServerPort, MCPHealthPort (driving ports)
- Secondary Ports: LoggingPort, LLMAdapterPort (driven ports)
- MCP Integration: FastMCP framework for protocol handling
- Logging Strategy: Structured JSON logging with prompt_id, latency_ms, llm_model

### Technology Specifications
Framework: FastMCP 2.13.0 with async support
Runtime: Python 3.13+
Configuration: Poetry for dependency management
Messaging: FastMCP internal messaging for MCP protocol
Observability: Structured JSON logging for operational visibility

### Security Specifications
Authentication: MCP protocol native authentication
Authorization: MCP client verification
Data Protection: No sensitive data stored, all data in memory
Audit Logging: Structured logs for all MCP operations with required fields

### Performance Considerations
- Async Processing: All MCP operations handled asynchronously
- Connection Management: FastMCP manages client connections
- Memory Management: Efficient handling of concurrent requests
- Response Caching: No caching for prompt responses to maintain freshness

### 📝 Specification Output
#### Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ 1. Core Implementation:
- Complete MCP server foundation with FastMCP integration
- `/health` endpoint with proper status reporting
- Example prompt implementation with ctx.sample functionality
- Proper error handling with appropriate HTTP codes

⭐ 2. Test Suite:
- Unit tests for business logic (85%+ coverage, pure functions only)
- Integration tests for complete MCP flows (real/fake adapters, no mocks of core logic)
- Health check verification tests
- ctx.sample() functionality tests

⭐ 3. Architecture Implementation:
- Hexagonal architecture with proper boundaries
- Immutable value objects with @dataclass(frozen=True)
- Protocol-based ports for dependency inversion
- Functional Core & Imperative Shell patterns

4. Configuration:
- Complete fastmcp.json configuration
- Environment configuration for deployment
- CI/CD pipeline with linting, type checking, and security scans

#### Code Structure Guidelines
```
src/
├── core/                  # Pure domain: functions, value objects, exceptions
│   ├── models/            # Immutable value objects (@dataclass(frozen=True))
│   │   └── mcp_models.py
│   ├── use_cases/         # Pure functions implementing business rules
│   │   └── mcp_use_cases.py
│   └── ports/             # Interfaces only (Protocols)
│       └── mcp_ports.py
├── adapters/              # Implementations of core ports
│   ├── mcp_server/        # FastMCP integration adapter
│   │   └── fastmcp_adapter.py
│   ├── logging/           # Structured logging implementation
│   │   └── structured_logger.py
│   └── llm/               # LLM sampling implementation
│       └── llm_adapter.py
└── app/                   # Application composition and configuration
    └── main.py            # Application entry point
```

#### Environment Configuration
```env
# fastmcp.json - FastMCP server configuration
{
  "server": {
    "name": "ctxfy-mcp-server",
    "version": "1.0.0",
    "description": "ctxfy MCP Server Base with FastMCP"
  },
  "host": "0.0.0.0",
  "port": 8000,
  "logging": {
    "level": "INFO",
    "format": "json",
    "required_fields": ["prompt_id", "latency_ms", "llm_model"]
  },
  "llm": {
    "default_model": "default",
    "timeout": 30,
    "max_retries": 3
  },
  "cors": {
    "origins": ["*"],
    "allow_credentials": true,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
  }
}
```

## ✅ Validation Framework
### Testing Strategy (⭐ = mandatory for simple tasks)
⭐ TDD Process (mandatory):
- Red: Write failing acceptance test against primary port
- Green: Implement minimal code to pass test (no refactoring yet)
- Refactor: Improve structure while keeping tests green

Unit Testing:
- 100% of core logic functions tested
- Pure functions in core/use_cases tested without infrastructure dependencies
- Value object validation thoroughly tested

Integration Testing:
- FastMCP adapter integration
- Health check functionality
- ctx.sample() workflow validation

Acceptance Criteria:
- Server responds to `/health` endpoint with 200 status
- Server handles MCP protocol requests via `/mcp` endpoint
- ctx.sample() functionality operates as expected with proper logging
- All logs include required fields: prompt_id, latency_ms, llm_model
- CI/CD pipeline executes successfully
- Server follows Hexagonal Architecture principles

### Success Metrics
Technical Metrics:
- 100% of endpoints responding with HTTP 200 for valid requests
- Average latency < 200ms for simple prompt operations
- 100% of prompts defined with @mcp.prompt are registerable and reusable
- Test coverage > 85% for prompt handling layer
- Proper structured logging with all required fields

Architectural Compliance:
- Hexagonal architecture boundaries maintained with zero violations
- All domain models immutable with @dataclass(frozen=True)
- Functional Core & Imperative Shell separation maintained
- TDD process followed with 70% unit tests in functional core
- Proper primary and secondary port implementations

Business Outcomes:
- Extensible foundation for future MCP services
- Standardized prompt sharing and reuse across teams
- Secure, authenticated access to MCP services
- Operational visibility through comprehensive monitoring
- Scalable architecture supporting multiple MCP clients