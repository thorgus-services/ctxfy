🏗️ CONTEXT STACK: Business Requirements Translation System with FastMCP Context

📋 Metadata
Creation Date: Tuesday, November 18, 2025
Author: Qwen Code
Domain: AI/LLM Integration & MCP Protocol
Task Type: Implementation
Context Category: feature

🎯 System Context Layer
AI Role & Boundaries
Role Definition
You are a senior Python/AI integration specialist with deep expertise in FastMCP framework, Model Context Protocol (MCP), and Hexagonal Architecture. Your primary mission is to implement the Business Requirements Translation System using FastMCP Context object for client-side operations while adhering to quality standards and following our **Hexagonal Architecture principles**.

Behavioral Constraints
Tone: Technical and collaborative
Detail Level: High - provide detailed technical implementation guidance
Boundaries: Do not modify critical production files without proper review; follow established architectural patterns
Security: Never expose sensitive data; follow security best practices for AI/LLM integrations and directory traversal prevention
Decision Authority: Can make technical decisions for implementation details, but needs approval for architecture changes

📚 Domain Context Layer
Specialized Knowledge Required

Domain Terminology
MCP: Model Context Protocol - Standard for connecting AI tools and models to development environments
FastMCP Context: FastMCP's context object that provides capabilities like logging, progress, resources, and LLM sampling during tool execution
@MCP.prompt: FastMCP decorator for registering server-side prompt templates with parameterized variables
ctx.sample(): Function for executing LLM sampling with structured input and output, allowing servers to request LLM completions from the client
Client Roots: MCP concept providing local context and resource boundaries to MCP servers, establishing security perimeters for filesystem operations
Hexagonal Architecture: Architectural pattern with domain core isolated from infrastructure concerns
Functional Core & Imperative Shell: Pattern separating pure business logic from side-effectful operations
Value Object: Immutable data structure with validation invariants in the functional core
Primary Port: Input port driven by external actor (e.g., `BusinessRequirementsCommandPort`, `BusinessRequirementsQueryPort`)
Secondary Port: Output port driving external systems (e.g., `FilesystemGatewayPort`, `LLMSamplingPort`)
Directory Traversal: Security vulnerability allowing access to files outside intended directories
Context Object: FastMCP object providing access to MCP capabilities during tool execution
Business Requirements Translation: Process of converting high-level business specifications into technical implementations
Technical Specifications: Detailed documentation describing how business requirements will be implemented
LLM Sampling: Requesting text generation from a language model through the MCP protocol

Methodologies & Patterns
Core patterns applicable to this domain: Hexagonal Architecture, Functional Core & Imperative Shell, Command-Query Separation (CQS), Immutable Value Objects, Orchestrator Pattern
Reference architectures: Hexagonal Architecture, Clean Architecture
Quality attributes: Security (directory traversal prevention), Performance (sub-200ms response time), Scalability, Error Resilience, Testability

Business Context
Business goals: Enable automatic translation of business requirements into technical specifications using FastMCP Context for client-side LLM operations to support project development and documentation
User needs: Developers can automatically convert business requirements into structured technical specifications via MCP server prompts with proper validation and security
Compliance requirements: Proper path validation, security against directory traversal attacks, structured logging, and comprehensive test coverage for business logic

🎯 Task Context Layer
Specific Task Definition

Objective
Implement business requirements translation functionality using FastMCP Context object that translates business requirements into technical specifications, stores them in the client's filesystem, and follows structured validation and security patterns, following Hexagonal Architecture principles in the ctxfy framework.

Success Criteria
Functional:
- FastMCP Context object successfully translates business requirements using ctx.sample() for LLM processing
- `translate_business_requirements()` function processes requirements and generates technical specifications
- Generated specifications are properly stored in `ctxfy/specifications/` directory on client filesystem
- Input validation thoroughly validates business requirements against defined schemas and security constraints
- Context-aware security validation prevents directory traversal and unauthorized filesystem access
- System returns properly formatted responses with execution metrics and translation status

Non-Functional:
- Individual translation requests complete within <200ms (p95 performance requirement)
- System provides security validation to prevent directory traversal attacks using client roots
- Proper error handling with meaningful messages for debugging
- 90%+ test coverage for core domain logic
- OpenAPI documentation generated automatically for all registered translation endpoints

Constraints
Technology constraints: Must use FastMCP 2.13.0 framework, Python 3.13+, and follow Hexagonal Architecture patterns
Resource constraints: Implementation should follow FCIS patterns with pure core functions and thin shells
Timeline constraints: Complete implementation with proper testing and security validation
Quality constraints: 90%+ test coverage, proper validation against business rules, zero critical security vulnerabilities

Architecture & Implementation Details

## 1. Overview

The Business Requirements Translation System implementation uses FastMCP 2.13.0 framework and follows Hexagonal Architecture and Functional Core & Imperative Shell patterns to translate business requirements into technical specifications using client-side LLM capabilities.

### 1.1 Purpose
- Enable automatic translation of business requirements into technical specifications using FastMCP Context
- Process requirements through ctx.sample() for LLM-powered translation
- Ensure security through client roots and path validation
- Generate structured technical specifications in standardized format

### 1.2 Scope
- Business requirements translation using FastMCP Context object and LLM sampling
- Integration with existing directory management and filesystem components
- Reuse of security and validation components from previous implementations
- Implementation following Functional Core and Imperative Shell patterns
- Generation of technical specifications in the ctxfy directory structure

## 2. Architecture

### 2.1 Hexagonal Architecture Structure

```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── directory_models.py                 # (existing) DirectoryConfig, DirectoryOperation, etc.
│   │   ├── filesystem_models.py                # (existing) Path validation, security models
│   │   ├── business_requirements_models.py     # NEW: Business requirements models
│   │   └── translation_models.py               # NEW: Translation result models
│   ├── use_cases/        # Pure functions implementing business rules
│   │   ├── directory_use_cases.py              # (existing) Directory creation logic
│   │   └── business_requirements_use_cases.py  # NEW: Business requirements translation logic
│   └── ports/            # Interfaces only (Protocols)
│       ├── directory_ports.py                  # (existing) DirectoryCommandPort, DirectoryQueryPort
│       └── business_requirements_ports.py      # NEW: Business requirements ports
├── shell/                # Imperative Shell orchestrators (no business logic)
│   └── orchestrators/    # Workflow coordination without business rules
│       ├── directory_orchestrator.py           # (existing) Coordinates directory operations using Context
│       └── business_requirements_orchestrator.py # NEW: Coordinates business requirements operations
├── adapters/             # Implementations of core ports
│   ├── context/          # FastMCP Context operations
│   │   ├── filesystem_adapter.py               # (existing) Client-side filesystem operations via ctx.sample()
│   │   └── business_requirements_adapter.py    # NEW: Business requirements adapter reusing filesystem
│   ├── security/         # (existing) Path validation and security checks
│   └── validation/       # (existing) Schema validation for requirements
└── app/                  # Application composition and configuration
```

### 2.2 Core Components

#### 2.2.1 Core Ports (`src/core/ports/business_requirements_ports.py`)
- `BusinessRequirementsCommandPort`: Primary port for business requirements operations
  - `translate_business_requirements(config: BusinessRequirementConfig) -> TranslationResult`
  - `generate_technical_specification(requirements: BusinessRequirements) -> TechnicalSpecification`
- `BusinessRequirementsQueryPort`: Primary port for business requirements information queries
  - `get_translation_status(translation_id: str) -> TranslationStatus`
  - `validate_requirements(requirements: BusinessRequirements) -> ValidationResult`

#### 2.2.2 Core Models (`src/core/models/business_requirements_models.py`)
- `BusinessRequirementConfig`: Immutable value object for business requirements configuration
  - `requirements_text: str` - Raw business requirements text to translate
  - `output_directory: str` - Directory to store generated specifications (default: "ctxfy/specifications")
  - `security_context: Dict[str, Any]` - Security context for operations
  - `validation_rules: Tuple[str, ...]` - Validation rules to enforce
- `BusinessRequirements`: Immutable value object for parsed business requirements
  - `content: str` - The business requirements text
  - `format_type: str` - Format of the requirements (e.g., "markdown", "plain")
  - `metadata: Dict[str, Any]` - Additional metadata about the requirements
- `TechnicalSpecification`: Immutable value object for technical specifications
  - `content: str` - The generated technical specification
  - `format_type: str` - Output format (e.g., "markdown", "json")
  - `translation_metadata: Dict[str, Any]` - Information about the translation process
- `TranslationResult`: Immutable value object for translation outcomes
  - `specification: TechnicalSpecification` - The translated specification
  - `status: str` - Translation status ("success", "error", "partial")
  - `metrics: Dict[str, Any]` - Performance and quality metrics

#### 2.2.3 Core Use Cases (`src/core/use_cases/business_requirements_use_cases.py`)
- `translate_business_requirements(requirements: BusinessRequirements, config: BusinessRequirementConfig) -> TranslationResult`
  - Pure function that orchestrates the translation process
  - Validates requirements and configuration
  - Performs security checks
  - Returns translation result

### 2.3 Shell Orchestrators (`src/shell/orchestrators/business_requirements_orchestrator.py`)
- `BusinessRequirementsOrchestrator`: Coordinates business requirements operations using Context
  - Implements the BusinessRequirementsCommandPort and BusinessRequirementsQueryPort
  - Handles FastMCP Context operations for LLM sampling and filesystem access
  - Coordinates with directory orchestrator for output directory management
  - Manages error handling and logging

### 2.4 Adapters (`src/adapters/context/business_requirements_adapter.py`)
- `BusinessRequirementsAdapter`: Implementation of business requirements ports using FastMCP Context
  - Uses ctx.sample() for LLM-powered translation
  - Implements filesystem operations within client roots boundaries
  - Applies security and validation checks

## 3. Security Implementation

### 3.1 Client Roots Integration
- Client roots define the allowed filesystem boundaries for operations
- All file operations are validated against client roots to prevent directory traversal
- Path normalization prevents bypass attempts with `../` sequences

### 3.2 Path Validation
- All directory and file paths are validated before operations
- Absolute paths are resolved relative to client roots
- Symbolic links are properly handled to prevent unauthorized access

### 3.3 Context Security
- FastMCP Context operations are restricted to allowed boundaries
- LLM sampling is performed with security context validation
- Translation operations are validated against security policies

## 4. FastMCP Context Integration

### 4.1 LLM Sampling
- Uses `ctx.sample()` to perform business requirements translation
- Passes requirements through secure messaging to prevent injection
- Applies system prompts to guide translation quality

### 4.2 Filesystem Operations
- Uses Context for client-side file operations within allowed roots
- Implements proper error handling for filesystem access
- Maintains security boundaries during file operations

## 5. Implementation Guidelines

### 5.1 Core Functions (Functional Core)
- All business rules in pure functions with no side effects
- Input validation in value objects via `__post_init__`
- Maximum 15 lines per function, ≤3 parameters
- Strict separation from I/O operations

### 5.2 Shell Functions (Imperative Shell)
- Thin wrappers around core logic for I/O operations
- Error handling, logging, and retry mechanisms
- Context and dependency injection management
- Maximum 25 lines per function

### 5.3 Testing Requirements
- 90%+ coverage for core domain logic
- Unit tests for all pure functions
- Integration tests for Core + Adapter combinations
- End-to-end tests for critical translation workflows

💬 Interaction Context Layer
Communication Protocol
Interaction Style
Feedback frequency: Report progress on major implementation milestones and immediately if encountering security concerns
Error handling approach: Report all security vulnerabilities immediately, group functional issues by component
Clarification protocol: Stop and ask for clarification if architectural pattern interpretation exceeds 10% ambiguity