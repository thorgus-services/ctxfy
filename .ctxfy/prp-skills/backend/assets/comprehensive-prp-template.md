# COMPREHENSIVE PRP TEMPLATE

## 🏷️ PRP Metadata
PRP ID: {{prp_id}} (e.g., PRP-SYSTEM-001)
Type: Backend Development
Domain: {{domain}} (e.g., Payment Processing, Order Management)
Technology Stack: {{technology_stack}} (e.g., Python/FastAPI/PostgreSQL/RabbitMQ/Redis)
Complexity Level: High
✨ AI Context Adaptation
Model Compatibility Notes
{{model_compatibility}} (e.g., "Claude 3: Excellent for complex business logic, needs detailed examples for state machines")
Context Drift Mitigation
{{drift_mitigation}} (e.g., "Include specific dependency versions: FastAPI==0.95.0, Pydantic==2.12")

## 🎯 Business Context Layer
Business Objectives
{{business_objectives}} (e.g., "Implement PCI-DSS compliant payment processing system with multiple payment methods and fraud detection")
SLAs & Performance Requirements
Availability: {{availability}} (e.g., "99.99% - no maintenance window")
Latency: {{latency}} (e.g., "< 500ms p95 for payment processing")
Throughput: {{throughput}} (e.g., "5000 transactions/second peak")
Data Freshness: {{data_freshness}} (e.g., "< 5 seconds for transaction status updates")
Error Rate: {{error_rate}} (e.g., "< 0.001% for payment processing failures")

## 👥 Stakeholder Analysis
Technical Stakeholders
{{technical_stakeholders}} (e.g., "Frontend Team: Needs idempotent API endpoints, DevOps/SRE: Requires comprehensive metrics")
Business Stakeholders
{{business_stakeholders}} (e.g., "Product Managers: Focus on payment method coverage, Finance Team: Requires reconciliation capabilities")

## 📋 Requirement Extraction
API & Interface Specifications
{{interface_specifications}} (e.g., "RESTful endpoints with OpenAPI 3.1, Webhook callbacks with signature verification")
Data Models & Entities
{{data_models}} (e.g., "Immutable value objects for Payment, PaymentIntent with transformation methods")
External Dependencies
{{external_dependencies}} (e.g., "Stripe API (SLA 99.99%), Redis 7.0 (SLA 99.95%), RabbitMQ 3.12 (SLA 99.9%)")

## 🔍 RAG Integration Section
Documentation Sources
Primary Sources: {{primary_sources}} (e.g., "Stripe API docs v2023-10-16, PostgreSQL 14 pgcrypto docs")
Internal Knowledge: {{internal_sources}} (e.g., "/ai_docs/pci_dss_requirements.md, /ai_docs/fraud_detection_patterns.md")
Retrieval Protocol
{{retrieval_protocol}} (e.g., "For each PCI-DSS requirement mentioned, search official documentation, validate against OWASP cheat sheets")

## 🔧 Technical Translation
Architecture Pattern
{{architecture_pattern}} (e.g., "Hexagonal Architecture with Event Sourcing, Primary Ports: PaymentCommandPort/PaymentQueryPort")
Technology Specifications
Framework: {{framework}} (e.g., "FastAPI 0.95.0 with async support")
Database: {{database}} (e.g., "PostgreSQL 14 with pgcrypto extension")
Caching: {{caching}} (e.g., "Redis 7.0 with dynamic TTL for payment states")
Messaging: {{messaging}} (e.g., "RabbitMQ 3.12 for event processing")
Observability: {{observability}} (e.g., "OpenTelemetry + Datadog + ELK stack")

Security Specifications
Authentication: {{authentication}} (e.g., "JWT with MFA for admin operations")
Authorization: {{authorization}} (e.g., "RBAC with payment-specific permissions")
Data Protection: {{data_protection}} (e.g., "AES-256 encryption for PII, tokenization for card data")
Audit Logging: {{audit_logging}} (e.g., "Immutable logs for all payment events, 7-year retention")
Compliance: {{compliance}} (e.g., "PCI-DSS Level 1, GDPR right to erasure, SOC2 Type II")

Performance Considerations
{{performance_considerations}} (e.g., "Connection Pooling: 100-500 PostgreSQL connections, Caching Strategy: L1/L2 cache with TTL, Async Processing: webhook notifications in background workers")

## 📝 Specification Output
Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ 1. API Implementation:
- Complete endpoints with Pydantic validation
- Idempotency key handling for duplicate prevention
- Rate limiting by customer ID and IP
- Webhook signature verification
⭐ 2. Test Suite:
- Unit tests for business logic (90%+ coverage)
- Integration tests with real/fake adapters
- Security tests for common vulnerabilities
- Load tests with production-level traffic
⭐ 3. Infrastructure as Code:
- Kubernetes deployment with auto-scaling
- PostgreSQL cluster with read replicas
- Redis cluster with failover
- Monitoring dashboards and alert definitions
Documentation:
- OpenAPI specification with examples
- Architecture Decision Record (ADR)
- Compliance documentation
- Disaster recovery procedures

Code Structure Guidelines
{{code_structure}} (e.g., "src/core/ for pure domain logic, src/shell/ for infrastructure adapters, strict package boundaries")

Environment Configuration
{{environment_config}} (e.g., ".env.example with security best practices, database pooling configuration, external service credentials")

## ✅ Validation Framework
Testing Strategy (⭐ = mandatory for simple tasks)
⭐ TDD Process (mandatory):
1. Red: Write failing acceptance test against primary port
2. Green: Implement minimal code to pass test
3. Refactor: Improve structure while keeping tests green
⭐ Unit Testing (≥70% of suite):
Target Functional Core only (pure functions, no dependencies)
Must pass in <100ms each
Test edge cases: declined cards, timeout scenarios, duplicate payments
⭐ Integration Testing (≤25%):
Test Core + Adapter combinations with real/fake adapters
Validate integration with external services
Test failure scenarios: network timeouts, API rate limits
⭐ Acceptance Testing:
Call primary ports directly with end-to-end scenarios
Execute against production-like environment

Quality Gates (⭐ = mandatory for simple tasks)
⭐ Code Quality:
- 0 critical/high issues in SonarQube
- Ruff formatting compliance (line length 88)
- Mypy strict mode passing for core packages
- 85%+ general test coverage, 95%+ for critical code
⭐ Security Gates:
- Zero high/critical vulnerabilities in SAST/DAST scan
- All dependencies updated (no known CVEs)
- Secrets management validated (no hardcoded credentials)
- Compliance checklist completed (PCI-DSS, GDPR, etc.)
⭐ Architecture Compliance:
- Core package has no dependencies on infrastructure packages
- No circular dependencies between packages
- Primary ports named as *CommandPort, *QueryPort
- Value objects are immutable (@dataclass(frozen=True))
- Package dependency violations: 0

Security Requirements (⭐ = mandatory for simple tasks)
⭐ Input Validation:
All endpoints validate input with Pydantic models (boundary only)
Data sanitization to prevent XSS/SQL injection
Rate limiting by IP and user ID
⭐ Authentication/Authorization:
JWT validation on all protected endpoints
Role-based access control for administrative operations
MFA requirement for critical changes
⭐ Data Protection:
Sensitive data encrypted at rest and in transit
Never expose mutable collections (convert to tuple/frozenset)
Audit logging with retention policies

## ⚠️ Known Gotchas & Risk Mitigation
Common Pitfalls (⭐ = mandatory for simple tasks)
⭐ TDD Violations:
Pitfall: Writing implementation before tests "to explore the problem"
Mitigation: Start with failing acceptance test against primary port
⭐ Architecture Violations:
Pitfall: Domain/core objects importing infrastructure packages
Mitigation: Enforce package boundaries with dependency tests
Detection: Use import-linter to prevent illegal imports
⭐ Immutability Violations:
Pitfall: Direct mutation of value objects (user.email = "new@ex.com")
Mitigation: Use transformation methods that return new instances
Detection: Unit tests that attempt to modify frozen dataclasses

Risk Areas & Mitigation Strategies
{{risk_areas}} (e.g., "High Risk: Payment data breach - Mitigation: Tokenization for card data, end-to-end encryption")

## 🔄 Execution Context
Prerequisites (⭐ = mandatory for simple tasks)
⭐ Development Setup:
Python 3.13+, PostgreSQL 14, Redis 7.0 installed
Poetry environment configured with dependencies
Ruff, Mypy, Bandit, and Safety tools installed
⭐ Knowledge Requirements:
TDD process (Red → Green → Refactor)
Hexagonal Architecture principles and port naming conventions
Immutable value objects pattern with @dataclass(frozen=True)

Development Process (⭐ = mandatory for simple tasks)
⭐ Core Implementation (follow TDD strictly):
1. Write failing acceptance test against primary port interface
2. Define immutable value objects for domain models
3. Implement core business logic as pure functions
4. Create port interfaces (Protocols) for dependencies
5. Implement adapter classes that satisfy port interfaces
6. Compose application with dependency injection in app.py
⭐ Testing & Validation:
7. Write unit tests for all pure functions (100% branch coverage)
8. Implement integration tests with real/fake adapters
9. Perform security testing with Bandit and manual review
10. Execute performance tests and optimize hotspots
11. Apply Boy Scout Rule: refactor at least one item per PR
⭐ Documentation & Deployment:
12. Update OpenAPI spec and technical documentation
13. Create Architecture Decision Record for significant choices
14. Prepare deployment scripts and configuration
15. Code review focusing on architecture compliance
16. Merge to main branch and deploy to staging
17. Final validation and production deployment

Collaboration Points
{{collaboration_points}} (e.g., "Security Team Review: Before any code is written, validate security architecture")

## 📊 Success Metrics
Performance Metrics (⭐ = mandatory for simple tasks)
⭐ {{performance_metric1}}: {{target1}} (e.g., "Payment processing latency: < 500ms p95")
⭐ {{performance_metric2}}: {{target2}} (e.g., "Throughput: 5000+ transactions/second at peak")
Availability:
Uptime: {{uptime_target}} (e.g., "99.99% monthly")
Mean Time To Recovery (MTTR): < {{mttr_target}} minutes
Incident rate: < {{incident_target}} critical incidents per month

Quality & Reliability Metrics (⭐ = mandatory for simple tasks)
⭐ Code Quality:
Ruff formatting compliance: 100%
Mypy strict mode passing for core: 100%
Test coverage: 85%+ general, 95%+ for critical code
Architecture Health:
Package dependency violations: 0
Core package import violations: 0
TDD adherence score: 95%+ (tests before implementation)
⭐ Security Posture:
Zero high/critical vulnerabilities in security scans
Average time to fix vulnerabilities: < 24h for critical
Compliance score: 100% with internal standards

Business Impact Metrics
{{business_metrics}} (e.g., "Payment success rate: > 99.5%, Checkout conversion rate: > 85%, Revenue impact: $0.0015 per successful transaction")

## 🔧 Template Usage Guidelines
### Full Process for Complex Tasks
For complex or critical tasks, complete ALL sections with specific details. Use the provided examples as a guide.

### Iterative Refinement Protocol
1. Start with ⭐ version (basic) for MVP
2. Execute and evaluate result
3. Refine context based on feedback
4. Add additional sections as needed
5. Repeat until success metrics are met

### Validation Checklist Before Execution
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
- [ ] Risk mitigation strategies are documented for critical paths
- [ ] Compliance requirements are explicitly addressed (PCI-DSS, GDPR, etc.)