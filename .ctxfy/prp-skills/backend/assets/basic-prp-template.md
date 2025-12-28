# BASIC PRP TEMPLATE (⭐)

## 🏷️ PRP Metadata
PRP ID: {{prp_id}} (e.g., PRP-FEATURE-001)
Type: Backend Development
Domain: {{domain}} (e.g., Authentication, User Management)
Technology Stack: {{technology_stack}} (e.g., Python/FastAPI/PostgreSQL)
Complexity Level: Low

## 🎯 Business Context Layer
Business Objectives
{{business_objectives}} (e.g., "Implement user profile management with basic CRUD operations")

## 🔧 Technical Translation
Architecture Pattern
{{architecture_pattern}} (e.g., "Hexagonal Architecture with Ports & Adapters")
Technology Specifications
Framework: {{framework}} (e.g., "FastAPI 0.95.0")
Database: {{database}} (e.g., "PostgreSQL 14")

## 📝 Specification Output
Expected Deliverables (⭐ = mandatory)
⭐ 1. API Implementation:
- {{endpoint1}} (e.g., "GET /users/{id} for user profile retrieval")
- {{endpoint2}} (e.g., "PUT /users/{id} for profile updates")
⭐ 2. Test Suite:
- Unit tests for core business logic
- Integration tests for API endpoints
⭐ 3. Infrastructure as Code:
- Dockerfile with basic configuration
- PostgreSQL migration scripts

## ✅ Validation Framework
Testing Strategy (⭐ = mandatory)
⭐ TDD Process (mandatory):
1. Red: Write failing test for core functionality
2. Green: Implement minimal code to pass test
3. Refactor: Improve structure while keeping tests green
⭐ Unit Testing:
def test_{{function}}_{{scenario}}():
    """Test core function with specific scenario"""
    # Setup test data
    # Execute function
    # Verify expected result

Quality Gates (⭐ = mandatory)
⭐ Code Quality:
- Ruff formatting compliance (line length 88)
- 80%+ test coverage for new code
⭐ Architecture Compliance:
- Core functions are pure (no I/O, no mutation)
- Value objects are immutable (@dataclass(frozen=True))

## 📊 Success Metrics
Performance Metrics (⭐ = mandatory)
⭐ {{metric1}}: {{target1}} (e.g., "Response time < 200ms p95")
⭐ {{metric2}}: {{target2}} (e.g., "Error rate < 0.1%")

## 🔧 Template Usage Guidelines
### For Simple Tasks (⭐)
- Use ONLY this template for simple backend tasks
- Focus on ⭐ sections only (mandatory for simple tasks)
- Keep token usage under 600 tokens
- Skip advanced sections like RAG integration and model compatibility notes

### Quick Validation Checklist
- [ ] All placeholders ({{ }}) have been replaced
- [ ] TDD process is explicitly defined
- [ ] Core functions are pure (no I/O, no mutation)
- [ ] Value objects use @dataclass(frozen=True)
- [ ] Ruff and Mypy configurations are included
- [ ] Test coverage requirements are met (80%+)
- [ ] Success metrics are measurable and objective