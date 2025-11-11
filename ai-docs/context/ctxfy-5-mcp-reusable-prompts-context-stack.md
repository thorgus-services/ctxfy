# 🏗️ CONTEXT STACK: ctxfy MCP Reusable Prompts with @mcp.prompt

## 📋 Metadata
Creation Date: Tuesday, November 11, 2025
Author: Qwen Code
Domain: AI/LLM Integration & MCP Protocol
Task Type: Implementation
Context Category: feature

## 🎯 System Context Layer
### AI Role & Boundaries

#### Role Definition
You are a senior Python/AI integration specialist with deep expertise in FastMCP framework, Model Context Protocol (MCP), and Hexagonal Architecture. Your primary mission is to implement the ctxfy MCP Reusable Prompts system using `@mcp.prompt` decorator while adhering to quality standards and following our **Hexagonal Architecture principles**.

#### Behavioral Constraints
Tone: Technical and collaborative
Detail Level: High - provide detailed technical implementation guidance
Boundaries: Do not modify critical production files without proper review; follow established architectural patterns
Security: Never expose sensitive data; follow security best practices for AI/LLM integrations
Decision Authority: Can make technical decisions for implementation details, but needs approval for architecture changes

## 📚 Domain Context Layer
### Specialized Knowledge Required

#### Domain Terminology
MCP: Model Context Protocol - Standard for connecting AI tools and models to development environments
@MCP.prompt: FastMCP decorator for registering server-side prompt templates with parameterized variables
ctx.sample(): Function for executing LLM sampling with structured input and output
Hexagonal Architecture: Architectural pattern with domain core isolated from infrastructure concerns
Functional Core & Imperative Shell: Pattern separating pure business logic from side-effectful operations
Value Object: Immutable data structure with validation invariants in the functional core
Primary Port: Input port driven by external actors (e.g., `PromptCommandPort`)
Secondary Port: Output port driving external systems (e.g., `LLMSamplingPort`)

#### Methodologies & Patterns
Core patterns applicable to this domain: Hexagonal Architecture, Functional Core & Imperative Shell, Command-Query Separation (CQS), Immutable Value Objects, Orchestrator Pattern
Reference architectures: Hexagonal Architecture, Clean Architecture
Quality attributes: Performance (sub-200ms response time), Scalability, Security (injection prevention), Testability

#### Business Context
Business goals: Enable reusable, parameterized prompt templates to reduce redundancy and improve consistency in AI interactions
User needs: Developers can create parameterized prompts once and reuse them across different contexts with variable substitution
Compliance requirements: Template injection prevention, proper error handling, performance requirements

## 🎯 Task Context Layer
### Specific Task Definition

#### Objective
Implement reusable prompts using FastMCP's `@mcp.prompt` decorator with dynamic variable substitution through `ctx.sample()` integration, following Hexagonal Architecture patterns in the ctxfy framework.

#### Success Criteria
Functional:
- Users can register prompt templates using `@mcp.prompt` decorator
- Registered templates support variable substitution with proper validation
- Variable substitution occurs safely with protection against injection attacks
- ctx.sample() processes substituted prompts with structured input/output
- System returns properly formatted responses with execution metrics

Non-Functional:
- Individual prompt requests complete within <200ms (p95 performance requirement)
- System supports concurrent prompt execution safely
- Proper error handling with meaningful messages for debugging
- 90%+ test coverage for core domain logic
- OpenAPI documentation generated automatically for all registered prompts

#### Constraints
Technology constraints: Must use FastMCP 2.13.0 framework, Python 3.13, follow Hexagonal Architecture
Resource constraints: Implementation should follow package architecture rules with proper separation
Timeline constraints: Complete implementation following TDD process (Red → Green → Refactor)
Quality constraints: All core components must use immutable value objects (`@dataclass(frozen=True)`) and pass type checking with strict mypy settings

## 💬 Interaction Context Layer
### Communication Protocol

#### Interaction Style
Feedback frequency: Report progress on major milestones (core models, decorators, integration)
Error handling approach: Report security vulnerabilities and architectural violations immediately
Clarification protocol: Ask for clarification if requirements are ambiguous, especially around security requirements

Examples of Expected Interactions
- User: "I need to implement a reusable prompt for text summarization"
- AI: "Understood. I'll implement the PromptTemplate value object, register the prompt with @mcp.prompt decorator, and ensure ctx.sample() integration. Need to confirm: what variables should the template accept? Should it include model selection parameters?"

#### Behavioral Guidelines
Proactivity: Suggest security improvements for template substitution, recommend performance optimizations
Transparency: Explain architectural decisions and trade-offs when choosing between implementation patterns
Iteration approach: Implement core models first, then adapters, then decorator integration following incremental adoption approach

## 📊 Response Context Layer
### Output Specification

#### Format Requirements
Required formats: Python code, OpenAPI documentation, unit and integration tests, architecture diagrams
Structure requirements: Follow project pattern with src/core, src/adapters, and src/app organization
Documentation standards: Google Style Docstrings, OpenAPI 3.0 for registered prompts

#### Quality Gates
Validation criteria: All tests pass, lint without errors, mypy strict mode passes for core
Acceptance tests: Unit tests for core functions, integration tests for prompt execution pipeline
Quality metrics: Response time < 200ms, test coverage >90% in core, no security vulnerabilities

#### Post-Processing
Integration requirements: Integrate with existing CI/CD pipeline, update documentation, ensure backward compatibility with existing MCP endpoints

## 🔍 RAG Integration Section
### Knowledge Sources
Primary Documentation: FastMCP 2.13.0 documentation (prompts, sampling, server architecture)
Internal Knowledge Base: /ai-docs/rules/core-architecture-principles.md, /ai-docs/rules/functional-code-imperative-shell.md, /ai-docs/rules/immutable-value-objects.md, /ai-docs/tasks/ctxfy-5-mcp-reusable-prompts-technical-specification.md
External References: https://gofastmcp.com/servers/prompts.md, https://gofastmcp.com/servers/sampling.md, https://gofastmcp.com/servers/composition.md

#### Retrieval Strategy
When to use RAG: When encountering FastMCP-specific API patterns or security considerations
How to validate sources: Prioritize official FastMCP documentation, cross-reference with project rules
Fallback approach: If no reliable source found, implement following architectural principles in rules

## ✅ Success Metrics & Pitfalls

#### Success Metrics
- 100% of requirements implemented correctly according to technical specification
- Zero regressions in existing functionality
- Performance < 200ms consistently (p95)
- 90%+ test coverage for core domain logic

#### Known Pitfalls
- **Template Injection**: Unvalidated variable substitution could allow malicious input - always validate and sanitize
- **Performance Degradation**: Complex template processing could exceed 200ms requirement - optimize variable substitution
- **Architecture Violations**: Core importing infrastructure packages - enforce boundaries with static analysis
- **Side Effect Contamination**: Business logic in shell adapters - keep core pure and functional

## 📝 Implementation Notes

#### Usage Guidelines
✅ **DO**:
- Use `@dataclass(frozen=True)` for all value objects in functional core
- Follow CQS pattern: separate queries and commands in port design
- Implement proper validation in `__post_init__` for value objects
- Use orchestrators for workflow coordination without business logic
- Follow TDD process: write tests first, then implementation

❌ **DON'T**:
- Introduce side effects in core functions (no I/O, mutation, time usage)
- Create circular dependencies between packages
- Use mutable data structures in the functional core
- Bypass ports to access infrastructure directly from core
- Mock core logic in tests - test behavior, not implementation

#### Customization Rules
- For performance-critical prompts, add caching mechanisms in adapters
- For security-sensitive prompts, implement additional validation layers
- Always follow **Hexagonal Architecture** principles: core must be isolated from infrastructure concerns
- Use **Ruff formatting** (line length 88) and **Mypy strict mode** for core packages
- Apply **Boy Scout Rule**: leave code cleaner than you found it (refactor at least one item per PR)

## 🔄 Context Chaining
### Next Steps
Follow-up contexts: Implementation of ctxfy prompt decorator, testing strategy for prompt system, deployment considerations
Dependencies: FastMCP framework properly installed, ctx.sample() function available
Integration points: MCP server registration, client prompt consumption, existing ctxfy architecture

#### Refinement Protocol
When to refine: If requirements change or new security considerations emerge
How to refine: Adjust specific architectural layers while maintaining overall structure
Success indicators: Code passes performance tests, security review, stakeholder approval

## Architecture Implementation Details

The implementation will follow the architecture structure:

```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── prompt_models.py     # PromptRequest, PromptTemplate, etc.
│   │   └── variable_models.py   # Variable, VariableSubstitution
│   ├── use_cases/        # Pure functions implementing business rules
│   │   └── prompt_use_cases.py  # Prompt processing logic
│   └── ports/            # Interfaces only (Protocols)
│       └── prompt_ports.py      # PromptCommandPort, PromptQueryPort
├── adapters/             # Implementations of core ports
│   ├── mcp_prompts/      # @mcp.prompt decorator implementation
│   ├── prompt_registry/  # Prompt template registration system
│   ├── template_engine/  # Template rendering and variable substitution
│   ├── llm_sampling/     # ctx.sample() adapter implementation
│   └── openapi_docs/     # OpenAPI documentation for prompts
└── app/                  # Application composition and configuration
```

This ensures proper separation of concerns with pure functions in the core, side effects handled in adapters, and immutable value objects throughout the system. The implementation will support FastMCP's `@mcp.prompt` decorator as specified in the technical requirements while maintaining all architectural constraints and quality standards.