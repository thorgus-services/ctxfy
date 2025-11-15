# 🚀 PRP - BACKEND DEVELOPMENT

## 🏷️ PRP Metadata
PRP ID: PRP-MCP-SERVER-DIR-CREATION-001
Type: Backend Development
Domain: AI Infrastructure & Model Context Protocol
Technology Stack: Python 3.13/FastMCP 2.13.0/HTTPX
Complexity Level: High

## ✨ AI Context Adaptation
### Model Compatibility Notes
- Claude 3: Excellent for complex business logic and directory operations, may need detailed examples for FastMCP Context usage
- GPT-4: Better for architectural patterns, but may be more creative than desired with FastMCP specifics
- Llama 3: Good for consistent code, but may need more domain context for MCP protocol and client-side filesystem operations
- **Strategy**: Provide concrete examples and strict acceptance criteria for all models, particularly for FastMCP integration and MCP protocol compliance with client-side Context operations

### Context Drift Mitigation
- Include specific dependency versions (e.g., FastMCP==2.13.0, Python==3.13)
- Provide current code examples instead of generic patterns
- Explicitly define what should NOT be done (e.g., direct filesystem access from server, mutable value objects in core, path traversal without validation)
- Test PRP with multiple models before production

## 🎯 Business Context Layer
### Business Objectives
Implement a robust directory creation system using FastMCP Context object that creates `ctxfy/` and `ctxfy/specifications/` directories in the client's filesystem and generates a `README.md` file with clear instructions about responsibilities and usage, following Hexagonal Architecture patterns in the ctxfy framework. The system must execute filesystem operations on the client side using Context methods while maintaining proper security validation to prevent directory traversal attacks.

### SLAs & Performance Requirements
Availability: 99.9% - including maintenance window  
Latency: < 500ms p95 for directory operations, < 50ms for health checks  
Throughput: 200 req/sec peak, 50 req/sec average for directory creation operations  
Data Freshness: < 1s for directory status updates  
Error Rate: < 0.05% for critical directory operations

### 👥 Stakeholder Analysis
#### Technical Stakeholders
- **Frontend Team**: Needs consistent MCP endpoints with request/response examples for directory creation
- **DevOps/SRE**: Requires detailed health checks, structured logging, and observability metrics for directory operations
- **Security Team**: Mandates MCP protocol compliance, audit of all filesystem operations, directory traversal prevention
- **AI/ML Engineering**: Needs ctx.sample() integration for client-side operations with security validation

#### Business Stakeholders
- **Product Managers**: Focus on launch time and scalability for directory management services
- **Engineering Leadership**: Interested in standardized MCP implementations and extensibility
- **Executive Sponsors**: Interested in operational efficiency through standardized directory structures and documentation
- **Compliance Team**: Requires audit trails and structured logging for all filesystem operations

### 📋 Requirement Extraction
#### API & Interface Specifications
- MCP protocol endpoints with FastMCP automatic handling
- `/health` endpoint for server health monitoring
- `@mcp.prompt` decorator functionality for directory creation prompts
- ctx.sample() integration for client-side filesystem operations
- OpenAPI documentation for all registered directory management endpoints
- Context-aware logging for directory operations with appropriate metadata

#### Data Models & Entities
```python
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, Any
import uuid
from datetime import datetime
import re

@dataclass(frozen=True)
class DirectoryConfig:
    """Immutable value object for directory configuration following our core architecture principles"""
    base_path: str = "ctxfy"
    subdirectories: Tuple[str, ...] = field(default_factory=lambda: ("specifications",))
    readme_content: str = ""
    validation_rules: Tuple[str, ...] = field(default_factory=lambda: ("no_traversal", "safe_chars"))

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.base_path or not isinstance(self.base_path, str):
            raise ValueError("Base path must be a valid string")
        if not isinstance(self.subdirectories, tuple):
            raise ValueError("Subdirectories must be a tuple")
        if not isinstance(self.readme_content, str):
            raise ValueError("README content must be a string")
        if not isinstance(self.validation_rules, tuple):
            raise ValueError("Validation rules must be a tuple")

@dataclass(frozen=True)
class DirectoryOperation:
    """Immutable value object for directory operations following our core architecture principles"""
    operation_type: str  # "create", "validate", "check"
    target_path: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if self.operation_type not in ["create", "validate", "check"]:
            raise ValueError("Operation type must be 'create', 'validate', or 'check'")
        if not self.target_path or not isinstance(self.target_path, str):
            raise ValueError("Target path must be a valid string")
        if not isinstance(self.parameters, dict):
            raise ValueError("Parameters must be a dictionary")

@dataclass(frozen=True)
class SecurePath:
    """Immutable value object for path validation following our core architecture principles"""
    raw_path: str
    sanitized_path: str
    is_safe: bool
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.raw_path or not isinstance(self.raw_path, str):
            raise ValueError("Raw path must be a valid string")
        if not isinstance(self.sanitized_path, str):
            raise ValueError("Sanitized path must be a string")
        if not isinstance(self.is_safe, bool):
            raise ValueError("Is_safe must be a boolean")
        if not isinstance(self.validation_errors, tuple):
            raise ValueError("Validation errors must be a tuple")

@dataclass(frozen=True)
class DirectoryStatus:
    """Immutable value object for directory status following our core architecture principles"""
    path: str
    exists: bool
    permissions: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self.path or not isinstance(self.path, str):
            raise ValueError("Path must be a valid string")
        if not isinstance(self.exists, bool):
            raise ValueError("Exists must be a boolean")
        if not isinstance(self.permissions, str):
            raise ValueError("Permissions must be a string")
        if self.created_at is not None and not isinstance(self.created_at, datetime):
            raise ValueError("Created_at must be a datetime or None")

@dataclass(frozen=True)
class ValidationResult:
    """Immutable value object for validation results following our core architecture principles"""
    is_valid: bool
    errors: Tuple[str, ...] = field(default_factory=tuple)
    warnings: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not isinstance(self.is_valid, bool):
            raise ValueError("Is_valid must be a boolean")
        if not isinstance(self.errors, tuple):
            raise ValueError("Errors must be a tuple")
        if not isinstance(self.warnings, tuple):
            raise ValueError("Warnings must be a tuple")
```

#### External Dependencies
- FastMCP: For MCP protocol implementation and Context object (version 2.13.0) - SLA 99.9%
- HTTPX: For client-side operations (version 0.25.0+)
- Python pathlib: For path operations (standard library)

## 🔍 RAG Integration Section
### Documentation Sources
Primary Sources:
- https://gofastmcp.com/llms.txt (FastMCP framework documentation)
- https://modelcontextprotocol.com/ (MCP protocol specifications)
- https://docs.pydantic.dev/latest/ (Pydantic validation framework)

### Context Stack References
- @ai-docs/context/ctxfy-10-mcp-server-output-directory-creation-context-stack.md
- @ai-docs/tasks/ctxfy-10-server-output-directory-creation-task.md

## 🏗️ Architecture Design
### Hexagonal Architecture Structure
```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── directory_models.py       # DirectoryConfig, DirectoryOperation, etc.
│   │   └── filesystem_models.py      # Path validation, security models
│   ├── use_cases/        # Pure functions implementing business rules
│   │   └── directory_use_cases.py    # Directory creation logic
│   └── ports/            # Interfaces only (Protocols)
│       └── directory_ports.py        # DirectoryCommandPort, DirectoryQueryPort
├── shell/                # Imperative Shell orchestrators (no business logic)
│   └── orchestrators/    # Workflow coordination without business rules
│       └── directory_orchestrator.py # Coordinates directory operations using Context
├── adapters/             # Implementations of core ports
│   ├── context/          # FastMCP Context operations
│   │   └── filesystem_adapter.py     # Client-side filesystem operations via ctx.sample()
│   ├── logging/          # Context-aware logging implementation
│   └── security/         # Path validation and security checks
└── app/                  # Application composition and configuration
```

### Primary Ports (Domain Interfaces)
```python
from abc import abstractmethod
from typing import Protocol

class DirectoryCommandPort(Protocol):
    """Primary port for directory management operations"""
    
    @abstractmethod
    async def ensure_directories_exist(self, config: DirectoryConfig) -> bool:
        """Ensure directory structure exists using Context filesystem operations"""
        ...
    
    @abstractmethod
    async def create_readme(self, content: str, directory_path: str) -> bool:
        """Create README file in the specified directory using Context"""
        ...

class DirectoryQueryPort(Protocol):
    """Primary port for directory information queries"""
    
    @abstractmethod
    async def get_directory_status(self, path: str) -> DirectoryStatus:
        """Get status of a directory using Context operations"""
        ...
    
    @abstractmethod
    async def validate_directory_path(self, path: str) -> ValidationResult:
        """Validate directory path safety and structure"""
        ...
```

### Secondary Ports (Infrastructure Interfaces)
```python
from typing import Protocol, Optional

class ClientFilesystemPort(Protocol):
    """Secondary port for client-side filesystem operations"""
    
    @abstractmethod
    async def create_directory(self, path: str) -> bool:
        """Create directory on client filesystem using Context"""
        ...
    
    @abstractmethod
    async def file_exists(self, path: str) -> bool:
        """Check if file exists on client filesystem using Context"""
        ...
    
    @abstractmethod
    async def write_file(self, path: str, content: str) -> bool:
        """Write content to file on client filesystem using Context"""
        ...
```

## 🧪 Quality Assurance
### Testing Strategy
- Unit tests for all pure functions in core package (>95% coverage)
- Integration tests for Context-based filesystem operations
- Security-focused tests for path validation and directory traversal prevention
- Performance tests for directory operations under load
- End-to-end tests for complete directory creation workflows

### Security Validation
- Path traversal prevention testing with `../` sequences
- Input validation for directory names and file content
- Context permission verification for filesystem operations
- Validation of Context object availability during operations

## 📊 Performance & Monitoring
### Key Metrics
- Directory creation latency (target: <500ms p95)
- Context operation success rate (target: >99.9%)
- Failed path validation rate (target: <0.01%)
- Concurrent operation throughput

### Observability
- Structured logging of all directory operations with request correlation
- Context-aware metrics collection during filesystem operations
- Alerting on directory creation failures
- Performance dashboards for directory management operations

## 🚀 Implementation Plan
### Phase 1: Core Models & Validation
1. Implement immutable value objects using @dataclass(frozen=True)
2. Create path validation and security models
3. Implement validation functions with security checks

### Phase 2: Core Use Cases & Ports
1. Develop pure functions for directory operations
2. Define primary and secondary ports
3. Implement Context-aware orchestration logic

### Phase 3: Adapters & Integration
1. Implement Context-based filesystem adapter
2. Create security adapter with path validation
3. Connect core to Context operations

### Phase 4: Testing & Validation
1. Write comprehensive unit and integration tests
2. Perform security validation and penetration testing
3. Conduct performance testing with load scenarios

## ✅ Success Criteria
### Functional Requirements
- [ ] FastMCP Context object successfully creates directories on client filesystem
- [ ] `ensure_directories_exist()` function verifies and creates directory structure
- [ ] `ctxfy/README.md` file is generated with clear instructions about responsibilities
- [ ] Directory creation follows security best practices with path validation
- [ ] Context-aware logging records directory operations with appropriate metadata
- [ ] System returns properly formatted responses with execution metrics

### Non-Functional Requirements
- [ ] Individual directory creation requests complete within <500ms (p95 performance)
- [ ] System provides security validation to prevent directory traversal attacks
- [ ] Proper error handling with meaningful messages for debugging
- [ ] 95%+ test coverage for core domain logic
- [ ] Structured logging with appropriate context information