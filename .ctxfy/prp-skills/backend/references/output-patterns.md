# Output Patterns for PRP Generation

## Template Pattern

### For Strict Requirements (Architecture-Critical Sections)

```markdown
## 📋 STATIC PROJECT RULES
**Architecture Pattern:**
- Functional Core & Imperative Shell
- Hexagonal Architecture with Ports & Adapters

**Toolchain Standards:**
- Ruff: line-length=88, select=["E", "F", "I", "B", "C4", "T20"]
- Mypy: strict=true for core packages
```

### For Flexible Requirements (Business Context)

```markdown
## 🎯 Business Context Layer
**Business Objectives:**
{{business_objectives}}

**SLAs & Performance Requirements:**
{{sla_requirements}}
```

## Examples Pattern

### Commit Message Pattern for PRP Updates

**Example 1:**
Input: Added security validation to user authentication PRP
Output:
feat(prp): enhance security requirements in authentication PRP
Add OWASP ASVS compliance requirements and brute force protection specifications

**Example 2:**
Input: Fixed token validation requirements in backend PRP template
Output:
fix(prp): correct JWT validation requirements in backend template
Specify exact algorithm requirements and key rotation policies

### PRP Structure Examples

**Example 1: Simple Task (⭐)**
```markdown
🏷️ PRP Metadata
PRP ID: PRP-USER-001
Type: Backend Development
Domain: User Management
Technology Stack: Python/FastAPI/PostgreSQL
Complexity Level: Low

🎯 Business Context Layer
Business Objectives
Implement user CRUD operations with proper authentication

🔧 Technical Translation
Architecture Pattern
Hexagonal Architecture with Ports & Adapters
Technology Specifications
Framework: FastAPI 0.95.0
Database: PostgreSQL 14

✅ Validation Framework
Testing Strategy (⭐)
⭐ TDD Process (mandatory):
Red: Write failing acceptance test against primary port
Green: Implement minimal code to pass test
Refactor: Improve structure while keeping tests green
```

**Example 2: Complex Task**
```markdown
🏷️ PRP Metadata
PRP ID: PRP-AUTH-002
Type: Backend Development
Domain: Authentication & Authorization
Technology Stack: Python/FastAPI/PostgreSQL/Redis
Complexity Level: High

🎯 Business Context Layer
Business Objectives
Implement secure authentication service reducing fraud by 30% while maintaining fluid UX
SLAs & Performance Requirements
Availability: 99.95% (including maintenance window)
Latency: < 150ms p95 for login, < 50ms for token refresh
Throughput: 1500 req/sec peak, 300 req/sec average

[... more sections ...]
```

## Narrative Structure Patterns

### Status Quo → Problem → Solution (Recommended for Architecture Changes)

**Example:**
```
Status Quo: Current authentication service has monolithic architecture
Problem: Cannot scale independently, high coupling between components
Solution: Implement Hexagonal Architecture with ports and adapters pattern
```

### What → Why → How (Recommended for New Technical Concepts)

**Example:**
```
What: Value Objects with @dataclass(frozen=True)
Why: Ensures data integrity and referential transparency in functional core
How: Define immutable objects with transformation methods that return new instances
```

### What → So What → What Now (Recommended for Business Impact)

**Example:**
```
What: Implementing proper TDD process for backend development
So What: 40% reduction in production bugs and 30% faster feature delivery
What Now: Start with failing acceptance test against primary port before implementation
```

## Anti-Patterns to Avoid

❌ **Overly Verbose PRPs**
- Problem: Exceeds 1000 token budget, loses focus
- Solution: Use progressive disclosure, keep only essential information

❌ **Vague Requirements**
- Problem: "Make it fast", "Ensure security" without concrete metrics
- Solution: Specify exact latency requirements, security standards (OWASP ASVS Level 2)

❌ **Missing Context Integration**
- Problem: PRP doesn't reference current project context or static rules
- Solution: Always include RAG integration section with current project structure

❌ **Ignoring Model Limitations**
- Problem: No guidance for different LLM capabilities
- Solution: Include model compatibility notes for Claude, GPT-4, Llama 3

## Success Patterns

✅ **Concrete Examples**
- Include specific code examples for critical patterns
- Example: `@dataclass(frozen=True)` value object implementation

✅ **Measurable Criteria**
- Define success with specific metrics
- Example: "Login latency: < 150ms p95"

✅ **Progressive Complexity**
- Start with simple requirements, add complexity sections as needed
- Use ⭐ notation for mandatory sections in simple tasks

✅ **Architecture Compliance First**
- Lead with architecture patterns and validation requirements
- Example: "Core package has no dependencies on infrastructure packages"