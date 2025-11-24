🔄 BUSINESS REQUIREMENTS TRANSLATION TEMPLATE
📋 Context & Metadata
Translation ID: TR-MCP-GEN-001
Business Requirement: "MCP Server for Technical Specification Generation"
Domain Context: Software Architecture & MCP Development
Stakeholders: Technical Product Manager (fernando), Tech Lead (fernando)
Priority: High
Complexity Level: Complex
Last Updated: November 23, 2025
AI Context: "Use as basis to generate technical PRP following Hexagonal Architecture and MCP standards"

🔍 Business Requirement Analysis
Original Requirement
As a Technical Product Manager with 7+ years of experience in high scalability systems, I want an MCP Server that automatically generates technical specifications in the `ctxfy/specifications/` directory of the client through a specialized CLI prompt for code model CLIs, so that I can translate business needs into standardized technical documentation without manual effort, with generation of at least 5 technical specifications per day with 98% architectural compliance and response time under 1.5 seconds, measured by automated code quality auditing, immutability verification of value objects, and performance metrics in staging environment with branch coverage >80% for critical paths before any refactoring.

Stakeholder Context
Business owner: Technical Product Manager - focused on developer productivity and architecture compliance
User perspective: Technical users want fast conversion of business requirements to standardized technical specs without manual work
Market context: Increasing need for AI-assisted development tools and standardized documentation formats
Strategic importance: Critical for reducing development time and improving spec consistency - direct impact on team efficiency

Ambiguities & Assumptions
Ambiguous terms: "specialized CLI prompt" - needs concrete definition of the prompt structure and capabilities; "standardized technical documentation" - needs specific format requirements
Unstated assumptions: MCP server is available and running; User has proper permissions to write to ctxfy/specifications/ directory; Model has knowledge of architectural patterns
Missing context: Specific error handling requirements, authentication mechanisms, backup strategies for generated specs
Clarification needed: Define exact JSON format for specifications, clarify security requirements for the MCP server, specify exact performance SLA for 1.5s response time

🎯 Technical Translation
AI Context Requirements
- **Model Guidance**: "You are a senior software architecture specialist with deep expertise in MCP (Model Context Protocol) development, FastMCP framework, hexagonal architecture, and functional core/imperative shell patterns. Your primary mission is to implement an MCP server that generates technical specifications from business requirements while adhering to quality standards and following our Hexagonal Architecture principles."
- **Context Sources**: "Use official FastMCP documentation at https://gofastmcp.com/llms.txt, Python 3.13 documentation, and our internal architecture standards at /ai_docs/"
- **Output Format**: "Structure response as complete technical PRP with detailed sections following our templates"
- **Success Criteria**: "Generated PRP should enable implementation without ambiguity by a junior engineer, following TDD and architecture rules"

Technical Objective
Develop an MCP server for technical specification generation that provides secure, performant, and architecture-compliant API with sub-1.5s response times, following Hexagonal Architecture principles with functional core and imperative shell patterns.

Core Capabilities Required
Specification Generation:
- Description: Complete generation of technical specifications from business requirements using immutable value objects and functional core principles
- User value: Fast conversion of requirements to standardized documentation without manual effort
- Technical complexity: Medium - requires complex text processing and JSON formatting following architectural rules
- AI Context: "Use @dataclass(frozen=True) for all domain models, validate invariants in __post_init__, implement pure functions in core"

MCP Tool Registration:
- Description: MCP server with proper tool registration following FastMCP framework patterns and architectural constraints
- User value: Standardized integration with MCP ecosystem and model interfaces
- Technical complexity: Medium - requires understanding of FastMCP tool registration and port patterns
- AI Context: "Define primary ports as SpecificationGenerationCommandPort, secondary ports as FilesystemPort, implement registry pattern for tools and prompts"

Specification Persistence:
- Description: Proper saving of specifications to ctxfy/specifications/ directory with proper error handling and validation
- User value: Reliable persistence of generated specifications with proper file naming
- Technical complexity: Medium-High - requires filesystem operations, error handling, and atomic file operations
- AI Context: "Implement TDD from the start: write failing acceptance test against primary port before any implementation"

Technical Constraints & Requirements
Performance requirements: Response time < 1.5 seconds p95, support for 5+ specifications per day
Security requirements: No exposure of sensitive data, follow security policy for file operations, Ruff and Bandit security scans
Integration requirements: Integrate with FastMCP framework, proper context handling for logging and progress
Data requirements: Schema validation for generated JSON specifications, immutable value objects, audit trails for generation
Compliance requirements: 98%+ test coverage of core logic, zero critical bugs, follow architectural rules, Mypy strict mode for core

Architecture Considerations
Pattern recommendations: Hexagonal Architecture with Functional Core for business logic, Imperative Shell for side effects
Component boundaries: Core package (domain models, pure functions), Adapters package (MCP tools, filesystem operations), Ports package (interfaces)
Data flow considerations: Pure functions in core, immutable value objects throughout, proper conversion at boundaries
Scalability approach: Stateless server components, minimal dependencies, configuration-driven behavior

🔍 RAG Integration & Context Stack Reference
RAG Sources
Primary Documentation: 
- https://gofastmcp.com/llms.txt (FastMCP framework documentation)
- Python 3.13 documentation (for language features)
- https://www.cosmicpython.com/ (Hexagonal Architecture patterns)

Internal Knowledge: 
- /ai_docs/rules/functional-code-imperative-shell.md (Functional Core Imperative Shell rules)
- /ai_docs/rules/immutable-value-objects.md (Immutable value object requirements)
- /ai_docs/rules/package-and-module-architecture.md (Package architecture standards)
- /ai_docs/rules/testing-strategy.md (TDD and testing requirements)
- /ai_docs/context/user-stories/mcp-server-specification-generation-context-stack.md (MCP server context)

Context Stack Reference
- **System Layer**: Follow Hexagonal Architecture principles and MCP development patterns
- **Domain Layer**: Include specific MCP and FastMCP framework context
- **Task Layer**: Focus on specification generation and MCP server implementation
- **RAG Integration**: Use FastMCP documentation and architectural rules
- **Reference**: PRP-ID: PRP-MCP-GEN-001

🛠️ Implementation Strategy
Technical Approach
Develop MCP server microservice following TDD process (Red → Green → Refactor), using Hexagonal Architecture with core isolated from infrastructure, immutable value objects for domain models, and MCP-specific adapters for tool integration.

Key Technical Decisions
Technology stack: Python 3.13, FastMCP framework, Pydantic for validation, Ruff for formatting
Architecture style: Hexagonal Architecture with functional core/imperative shell, primary ports for driving logic, secondary ports for infrastructure
Data model strategy: Immutable value objects (@dataclass(frozen=True)) for domain models, Pydantic models only at MCP boundaries, strong typing throughout
Error handling approach: Problem Details RFC 7807 for consistent errors at boundaries, pure exception handling in core, proper MCP error propagation
Testing strategy: TDD mandatory with 70% unit tests (pure functions), 25% integration tests (real/fake adapters), 5% end-to-end tests, Boy Scout Rule refactoring per PR

Resource Implications
Development effort: 4-5 weeks for complete MVP with comprehensive tests following TDD
Infrastructure needs: MCP server connectivity, filesystem access for specification persistence, proper authentication mechanisms
Maintenance considerations: Performance monitoring for response times, architecture compliance monitoring, dependency updates with Safety checks
Team skills required: Python TDD experience, Hexagonal Architecture implementation, MCP framework knowledge, Ruff/Mypy toolchain proficiency

✅ Validation Protocol
Acceptance Criteria (⭐ = mandatory for simple translations)
Functional criteria:
⭐ Users can submit business requirements to generate technical specifications
⭐ Specifications are saved in the ctxfy/specifications/ directory with proper file naming
⭐ Generated specifications follow standardized JSON format with proper schema
⭐ Server provides clear paths to saved specification files and handles errors appropriately
⭐ MCP server registers tools and prompts correctly following FastMCP patterns

Quality criteria:
⭐ Response time < 1.5 seconds for 95% of requests, Ruff formatting compliance 100%
⭐ Zero data integrity issues, Mypy strict mode passing for core, 98%+ test coverage
⭐ 100% compliance with architectural rules (immutable objects, FCIS, package boundaries)

Verification Approach
Testing approach: TDD process with acceptance tests against primary ports, unit tests for pure functions, integration tests with real/fake adapters
Performance validation: Load testing simulating 10 concurrent users, response time measurement, connection handling verification
Security validation: File system permissions validation, input sanitization testing, dependency security scanning
User acceptance process: Beta testing with technical team, architecture compliance review, performance verification

🔍 Cross-Reference Mapping - AI Enhanced
Requirement Traceability (AI-Generated Matrix)
| Business Requirement | Technical Component | Validation Method | Owner | Risk Level |
|----------------------|---------------------|-------------------|-------|------------|
| MCP Server for spec generation | src/core/use_cases/generate_specification.py | Unit tests with TDD | Technical PM | Medium |
| Save to ctxfy/specifications/ | src/shell/adapters/specification_generation_tool.py | Integration tests | Technical PM | Medium |
| Response time < 1.5s | Performance tests | Load testing | Technical PM | High |
| 98% architectural compliance | src/core/models/specification_result.py | Architecture linters | Technical PM | High |
| MCP tool registration | src/shell/registry/ | Integration tests | Technical PM | Medium |

Dependencies & Impacts
System dependencies: FastMCP server framework must be available, proper authentication mechanisms for file system access
Data dependencies: Proper permissions for ctxfy/specifications/ directory, MCP context availability
Timeline dependencies: FastMCP framework setup completed, architectural standards reviewed and approved
Risk factors: High risk of performance issues if architecture not followed, architecture compliance risk if TDD not followed, file system access issues

💔 Past Implementation Failures & Lessons Learned
Previous Failures
Architecture Violations:
- What happened: Core logic mixed with infrastructure concerns causing tight coupling
- Root cause: Developers not following hexagonal architecture principles, mutable objects in core
- Impact: 25% increase in bug rate, longer development time for new features
- Lesson learned: Always verify layers are separated correctly, use @dataclass(frozen=True) for domain objects

Performance Issues:
- What happened: MCP server response times exceeded 1.5s threshold during load testing
- Root cause: Inefficient data processing in core, blocking operations in critical paths
- Impact: Failed performance requirements, delayed deployment
- Lesson learned: Always profile critical paths, implement efficient algorithms for text processing

MCP Framework Misuse:
- What happened: Incorrect tool registration pattern caused MCP server to fail
- Root cause: Lack of understanding of FastMCP framework requirements
- Impact: Server couldn't register properly with MCP ecosystem
- Lesson learned: Follow FastMCP documentation strictly, test registration patterns early

[Continue for relevant past failures]

📝 Implementation Notes
🚀 **Quick Translation Checklist (for Simple Requirements)**:
For simple requirements, focus on these essential points:
- [x] Clear and measurable Technical Objective following architecture standards
- [x] 3 Core Capabilities with defined user value and TDD approach
- [x] Basic security and performance requirements with toolchain standards
- [x] Functional and quality Acceptance Criteria with test distribution ratios
- [x] Key stakeholders identified with collaboration points

📚 **Comprehensive Process (for Complex Requirements)**:
For complex or critical requirements:
1. ✓ Conduct alignment workshop with stakeholders
2. ✓ Document all ambiguities and assumptions
3. ✓ Research relevant regulations and standards
4. ✓ Analyze related past failures and lessons learned
5. ✓ Create complete traceability matrix
6. ✓ Validate technical translation with team leads
7. ✓ Document architecture decisions and trade-offs
8. ✓ Define RAG sources for current best practices

🔄 **AI-Assisted Translation Workflow**:
1. **Input Preparation**:
   - ✓ Fill initial sections with business context
   - ✓ Identify ambiguous terms and risk areas
   - ✓ Define clear success criteria with metrics

2. **AI Context Engineering**:
   - ✓ Generate systematic context using Context Stack reference
   - ✓ Include relevant RAG sources for specific domain and architecture standards
   - ✓ Define clear constraints based on Python toolchain and architecture rules

3. **Generation & Validation**:
   - ✓ Execute translation with complete context
   - ✓ Validate result against acceptance criteria and architecture standards
   - ✓ Check for TDD compliance, immutable value objects usage, package dependencies
   - ✓ Iteratively refine context based on feedback

4. **Human Review**:
   - ✓ Technical review by senior engineer focusing on architecture compliance
   - ✓ Business validation with product owner
   - ✓ Security review with security team
   - ✓ Final adjustments and approval for implementation

⚠️ **Critical Success Factors**:
- **Architecture Compliance**: Hexagonal Architecture principles must be followed from the start
- **TDD Adherence**: Red → Green → Refactor cycle mandatory for all implementations
- **Immutability by Default**: All domain models must be immutable value objects
- **Test Distribution**: 70% unit tests (pure functions), 25% integration tests, 5% e2e tests
- **Toolchain Standards**: Ruff (line length 88), Mypy (strict mode for core), Bandit/Safety
- **Clarity over brevity**: Better to be detailed than ambiguous
- **Measurable criteria**: All requirements should have success metrics
- **Risk transparency**: Explicitly document risks and mitigation
- **Context completeness**: Include implicit knowledge the AI needs
- **Iterative refinement**: Accept that first version is rarely perfect

🔄 **Refinement Protocol**:
When to refine:
- Result doesn't meet 80% of acceptance criteria
- Architecture compliance issues detected (core importing infrastructure, mutable value objects)
- TDD process not followed in the specification
- Stakeholders identify significant gaps
- New compliance or regulatory information emerges
- Security or performance standards aren't met

How to refine:
1. Identify specific layer with problem (System, Domain, Task, etc.)
2. Collect specific feedback from stakeholders
3. Update context with missing or corrected information
4. Re-execute translation with new context
5. Document changes and learnings in the Version History section