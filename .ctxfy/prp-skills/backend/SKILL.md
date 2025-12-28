---
name: "prp-backend"
description: "Generate comprehensive backend development Product Requirements Prompts (PRPs) following Hexagonal Architecture and Functional Core & Imperative Shell principles. Use when generating backend PRPs for API services, domain logic, and infrastructure integration with strict validation of architecture compliance, test distribution requirements, and context engineering best practices."
license: "Internal Use Only"
allowed-tools: ["python", "git"]
metadata:
  domain: "backend-development"
  complexity: "High"
  activation_criteria: "Task involves backend development requiring PRP generation with architecture compliance validation"
---

# Backend PRP Generator Skill

## Overview

This skill generates rigorously structured Product Requirements Prompts (PRPs) for backend development tasks that maintain strict compliance with Functional Core & Imperative Shell (FCIS) architectural principles. Unlike generic PRP templates, this skill incorporates context-aware validation, progressive disclosure of requirements, and architecture compliance gates to ensure every generated PRP produces production-ready code.

### When to Use This Skill

This skill should be activated when:
- Generating PRPs for backend services, APIs, or domain logic implementations
- Ensuring architecture compliance with FCIS and Hexagonal Architecture patterns
- Validating context stack integration with static rules and dynamic project context
- Tasks requiring strict test distribution ratios (70% unit, 25% integration, 5% e2e)
- Projects following Python toolchain standards with Ruff (line-length=88) and Mypy strict mode

## Core Structure Pattern

Backend PRPs follow this consistent structure to ensure architecture compliance:

1. **PRP Metadata** - Identification and context
2. **Business Context Layer** - Requirements and stakeholder analysis
3. **Technical Translation** - Architecture and implementation specifications
4. **Specification Output** - Deliverables and code structure
5. **Validation Framework** - Testing strategy and quality gates
6. **AI Context Adaptation** - Model-specific guidance

### Progressive Context Integration

The skill integrates dual context layers following Context Engineering principles:

```markdown
## 📋 STATIC PROJECT RULES
{{static_rules_content}}  # From .ctxfy/rules/

## 🔄 CURRENT PROJECT CONTEXT
{{dynamic_context_content}}  # From context-scan output .ctxfy/tasks/{task_id}/current-project-context.md
```

## Skill Execution Workflow

### Step 1: Context Validation
Before generating any PRP content:
- Validate context stack layers exist and are properly formatted
- Check for conflicts between static rules and dynamic context
- Verify skill metadata score ≥ 75 from skill-discovery agent
- Ensure token budget < 1000 tokens for PRP content

### Step 2: PRP Generation Protocol
For each PRP section, follow this execution protocol:

#### PRP Metadata Section
```markdown
🏷️ PRP Metadata
PRP ID: {{prp_id}} (e.g., PRP-AUTH-001)
Type: Backend Development
Domain: {{domain}} (e.g., Authentication, Payment Processing, Data Analytics)
Technology Stack: {{technology_stack}} (e.g., Python/FastAPI/PostgreSQL)
Complexity Level: {{complexity}} (Low/Medium/High)
```

#### Business Context Layer
```markdown
🎯 Business Context Layer
Business Objectives
{{business_objectives}}
SLAs & Performance Requirements
Availability: {{availability}} (e.g., 99.95%)
Latency: {{latency}} (e.g., < 150ms p95)
Throughput: {{throughput}} (e.g., 1500 req/sec)
```

#### Technical Translation Section
```markdown
🔧 Technical Translation
Architecture Pattern
{{architecture_pattern}} (e.g., Hexagonal Architecture with Ports & Adapters)
Technology Specifications
Framework: {{framework}} (e.g., FastAPI 0.95.0)
Database: {{database}} (e.g., PostgreSQL 14)
Security Specifications
Authentication: {{authentication}} (e.g., JWT with short TTL)
Authorization: {{authorization}} (e.g., RBAC with permission inheritance)
```

#### Specification Output Section
```markdown
📝 Specification Output
Expected Deliverables (⭐ = mandatory for simple tasks)
{{deliverables}} (e.g., API Implementation, Test Suite, Infrastructure as Code)
Code Structure Guidelines
{{code_structure}} (e.g., following src/core/ and src/shell/ separation)
```

#### Validation Framework
```markdown
✅ Validation Framework
Testing Strategy (⭐ = mandatory for simple tasks)
{{testing_strategy}} (e.g., TDD Process, Unit Testing, Integration Testing)
Quality Gates (⭐ = mandatory for simple tasks)
{{quality_gates}} (e.g., Code Quality, Security Gates, Architecture Compliance)
```

#### AI Context Adaptation Section
```markdown
✨ AI Context Adaptation
Model Compatibility Notes
{{model_compatibility}} (e.g., "Claude 3: Excellent for complex business logic")
Context Drift Mitigation
{{drift_mitigation}} (e.g., "Include specific dependency versions")
```

### Step 3: Critical Constraints Enforcement
Apply these non-negotiable constraints to every generated PRP:

#### Architecture Compliance Gates
- Core functions must be pure (no I/O, no mutation of inputs)
- Shell functions must be thin wrappers (≤25 lines)
- Value objects must use @dataclass(frozen=True)
- Primary ports named as *CommandPort, *QueryPort
- Secondary ports named as *GatewayPort, *RepositoryPort

#### Test Distribution Requirements
- Unit Testing (≥70% of suite): Target Functional Core only
- Integration Testing (≤25%): Test Core + Adapter combinations
- Acceptance Testing: Call primary ports directly

#### Toolchain Standards
- Ruff configuration: line-length=88, select=["E", "F", "I", "B", "C4", "T20"]
- Mypy configuration: strict=true for core packages
- Dependency versions specified explicitly (e.g., FastAPI==0.95.0)

## Anti-Patterns Detection

The skill actively detects and prevents these common backend PRP anti-patterns:

❌ **Architecture Violations**
- Core functions containing database calls or HTTP requests
- Shell functions containing business rules or calculations
- Mutable domain objects without transformation methods
- Circular dependencies between core and shell packages

❌ **Testing Anti-patterns**
- Mocking core logic (e.g., `mock.patch('core.calculate_total')`)
- Writing implementation before tests "to explore the problem"
- Test coverage without branch coverage requirements
- Security tests without OWASP ZAP scan requirements

❌ **Context Engineering Failures**
- PRP exceeding 1000 token budget
- Missing RAG integration section for current project context
- No context drift mitigation strategies
- No model compatibility notes for multiple LLM backends

## RAG Integration Protocol

For each backend PRP, integrate current project context using this protocol:

```markdown
🔍 RAG Integration Section
Documentation Sources
Primary Sources: {{primary_sources}}
Internal Knowledge: {{internal_sources}}
Retrieval Protocol
{{retrieval_protocol}}
```

### Source Validation Strategy
1. **Primary Documentation**: Official framework/library documentation
2. **Internal Knowledge Base**: `/ai_docs/` directory with architecture standards
3. **Project Rules**: `.ctxfy/rules/` directory with static rules
4. **Current Context**: `.ctxfy/tasks/{task_id}/current-project-context.md`

## Quality Gates and Success Metrics

Every generated backend PRP must pass these quality gates:

### Token Budget Compliance
- PRP must stay within 1000 token budget
- Compression applied strategically to maintain key patterns

### Architecture Test Coverage
- Architecture test requirements must be specified:
  - `def test_core_does_not_depend_on_shell():`
  - `def test_value_object_immutable():`
  - `def test_port_naming_conventions():`

### Success Metrics Template
```markdown
📊 Success Metrics
Performance Metrics (⭐ = mandatory for simple tasks)
{{performance_metrics}} (e.g., Login latency: < 150ms p95)
Quality & Reliability Metrics (⭐ = mandatory for simple tasks)
{{quality_metrics}} (e.g., Ruff formatting compliance: 100%)
Business Impact Metrics
{{business_metrics}} (e.g., User adoption rate: > 90%)
```

## Resources

This skill integrates with the broader context engineering framework through these resource files:

### references/
Core reference documents that inform PRP generation:
- `references/output-patterns.md` - Standardized output patterns for consistent PRP structure
- `references/workflows.md` - Sequential and conditional workflows for complex backend implementations
- `references/backend-prp-examples.md` - Real-world examples of successful backend PRPs

### assets/
Template assets for PRP generation:
- `assets/basic-prp-template.md` - Minimal PRP template for simple tasks (⭐)
- `assets/comprehensive-prp-template.md` - Full PRP template for complex/regulated tasks
- `assets/validation-checklist.md` - PRP validation checklist with architecture compliance gates

### scripts/
**No executable scripts needed** - This skill operates through context engineering principles and prompt generation rather than code execution. All complex logic is contained within the PRP generation protocol.

## Execution Guidelines

### For Simple Tasks (⭐)
Focus on these mandatory sections only:
- PRP Metadata (basic info)
- Business Context Layer (clear objectives)
- Technical Translation (essential technical specifications)
- Specification Output (minimum deliverables)
- Validation Framework (critical tests and quality gates)

### For Complex Tasks
Complete ALL sections with specific details:
- Full Business Context Layer with stakeholder analysis
- Comprehensive Technical Translation with architecture patterns
- Detailed Specification Output with environment configuration
- Complete Validation Framework with security requirements
- Thorough AI Context Adaptation with model compatibility notes
- RAG Integration Section with current project context

### Iterative Refinement Protocol
1. Start with ⭐ version (basic) for MVP
2. Execute and evaluate result
3. Refine context based on feedback
4. Add additional sections as needed
5. Repeat until success metrics are met

## Validation Checklist Before Execution
Every generated PRP must satisfy this checklist:
- [ ] All placeholders ({{ }}) have been replaced with specific values
- [ ] TDD process is explicitly defined with Red → Green → Refactor
- [ ] Hexagonal Architecture principles are followed with port naming conventions
- [ ] Immutable value objects pattern is specified with @dataclass(frozen=True)
- [ ] Ruff and Mypy configurations are included with toolchain standards
- [ ] Test distribution requirements are met (70% unit, 25% integration, 5% e2e)
- [ ] Dependency versions specified explicitly (e.g., FastAPI==0.95.0)
- [ ] Success criteria are measurable and objective with specific metrics
- [ ] RAG sources are up-to-date and accessible with retrieval protocol
- [ ] Architecture compliance gates are validated against static rules

This skill transforms generic backend development tasks into rigorously structured, architecture-compliant PRPs that produce production-ready code through context engineering principles and progressive disclosure of requirements.