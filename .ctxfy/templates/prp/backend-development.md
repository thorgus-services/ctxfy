🚀 PRP - BACKEND DEVELOPMENT
🏷️ PRP Metadata
PRP ID: {{prp_id}} (e.g., PRP-AUTH-001)
Type: Backend Development
Domain: {{domain}} (e.g., Authentication, Payment Processing, Data Analytics)
Technology Stack: {{technology_stack}} (e.g., Python/FastAPI/PostgreSQL, Node.js/Express/MongoDB)
Complexity Level: {{complexity}} (Low/Medium/High)

✨ AI Context Adaptation
Model Compatibility Notes
{{model_compatibility}} (e.g.:
- Claude 3: Excellent for complex business logic, may need detailed examples
- GPT-4: Better for architectural patterns, but may be more creative than desired
- Llama 3: Good for consistent code, but may need more domain context
- **Strategy**: Provide concrete examples and strict acceptance criteria for all models)

Context Drift Mitigation
{{drift_mitigation}} (e.g.:
- Include specific dependency versions (e.g., FastAPI==0.95.0)
- Provide current code examples instead of generic patterns
- Explicitly define what should NOT be done
- Test PRP with multiple models before production)

🎯 Business Context Layer
Business Objectives
{{business_objectives}} (e.g., "Implement secure authentication for mobile app, reducing fraud by 30% while maintaining fluid UX")

SLAs & Performance Requirements
Availability: {{availability}} (e.g., 99.95% - including maintenance window)
Latency: {{latency}} (e.g., < 150ms p95 for login, < 50ms for token refresh)
Throughput: {{throughput}} (e.g., 1500 req/sec peak, 300 req/sec average)
Data Freshness: {{data_freshness}} (e.g., < 1s for suspicious account blocking)
Error Rate: {{error_rate}} (e.g., < 0.05% for critical operations)

👥 Stakeholder Analysis
Technical Stakeholders
{{technical_stakeholders}} (e.g.:
- **Frontend Team**: Needs consistent endpoints with request/response examples
- **DevOps/SRE**: Requires detailed health checks, Prometheus metrics, structured logging
- **Security Team**: Mandates OWASP ASVS compliance, audit of all sensitive operations
- **Data Engineering**: Needs audit events for usage pattern analysis)

Business Stakeholders
{{business_stakeholders}} (e.g.:
- **Product Managers**: Focus on launch time and adoption metrics
- **Customer Support**: Needs clear error messages and problem codes for troubleshooting
- **Legal/Compliance**: Requires GDPR compliance (right to be forgotten), CCPA, and internal policies
- **Executive Sponsors**: Interested in ROI and operational cost reduction through automation)

📋 Requirement Extraction
API & Interface Specifications
{{interface_specifications}} (e.g.:
- RESTful endpoints with OpenAPI 3.1 specification and examples
- WebSockets for real-time session status updates
- gRPC for internal microservice communication
- Webhooks with retry mechanism for external notifications)

Data Models & Entities
{{data_models}} (e.g.:
```python
from dataclasses import dataclass, field
from typing import Tuple
from decimal import Decimal

@dataclass(frozen=True)
class UserAuth:
    """Immutable value object following our core architecture principles"""
    user_id: str  # UUID format
    email: str    # Validated email format
    password_hash: str  # Argon2 hash, never plaintext
    mfa_enabled: bool = False
    failed_attempts: int = 0
    locked_until: float | None = None  # Unix timestamp
    
    def __post_init__(self):
        """Validate invariants immediately after construction"""
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")
        if self.failed_attempts < 0:
            raise ValueError("Failed attempts cannot be negative")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Simple email validation - replace with proper validation in production"""
        return "@" in email and "." in email.split("@")[-1]
    
    def with_failed_attempt(self) -> "UserAuth":
        """Return new instance with incremented failed attempts (immutability)"""
        return UserAuth(
            user_id=self.user_id,
            email=self.email,
            password_hash=self.password_hash,
            mfa_enabled=self.mfa_enabled,
            failed_attempts=self.failed_attempts + 1,
            locked_until=self.locked_until
        )
```

External Dependencies
{{external_dependencies}} (e.g.:
- Auth0: For social authentication (Google, Facebook) - SLA 99.9%
- Redis: For session caching and rate limiting - version 7.0+
- SendGrid: For verification and recovery emails - fallback to SES
- Cloudflare: For DDoS mitigation and public endpoint protection)

🔍 RAG Integration Section
Documentation Sources
Primary Sources: {{primary_sources}} (e.g.:

- https://fastapi.tiangolo.com/v0.95.0/security/oauth2-jwt/
- https://www.postgresql.org/docs/14/pgcrypto.html
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html )

Internal Knowledge: {{internal_sources}} (e.g.:
- /ai_docs/security_standards.md (our internal policy)
- /ai_docs/auth_patterns.md (approved team patterns)
- /examples/auth_success_cases.md (previous successful implementations))

Retrieval Protocol
{{retrieval_protocol}} (e.g.:
1. For each technical term mentioned, search official documentation
2. Validate security with OWASP Cheat Sheets
3. Check version compatibility before implementing
4. If conflict between sources, prioritize official documentation + internal standards)

🔧 Technical Translation
Architecture Pattern
{{architecture_pattern}} (e.g.:
- Pattern: Hexagonal Architecture with Ports & Adapters
- Primary Ports: UserCommandPort, UserQueryPort (driving ports)
- Secondary Ports: UserRepositoryPort, EmailGatewayPort (driven ports)
- Authentication Flow: OAuth2.0 Authorization Code flow for web, Client Credentials for internal services
- Session Management: Stateless JWT with rotating refresh tokens
- Security Layers: Rate limiting, IP whitelisting, anomaly detection)

Technology Specifications
Framework: {{framework}} (e.g., FastAPI 0.95.0 with async support)
Database: {{database}} (e.g., PostgreSQL 14 with pgcrypto extension for encryption)
Caching: {{caching}} (e.g., Redis 7.0 with dynamic TTL based on criticality)
Messaging: {{messaging}} (e.g., RabbitMQ for audit events and notifications)
Observability: {{observability}} (e.g., OpenTelemetry + Prometheus/Grafana + ELK stack)

Security Specifications
Authentication: {{authentication}} (e.g., Multi-factor authentication for admin operations, JWT with short TTL)
Authorization: {{authorization}} (e.g., RBAC with permission inheritance, ABAC for data-level security)
Data Protection: {{data_protection}} (e.g., AES-256 encryption at rest, TLS 1.3+ in transit, HSM for key management)
Audit Logging: {{audit_logging}} (e.g., Immutable logs for all authentication events, GDPR-compliant retention)

Performance Considerations
{{performance_considerations}} (e.g.:
- Connection Pooling: 50 minimum connections, 200 maximum for PostgreSQL
- Caching Strategy:
  - L1: In-memory cache for active tokens (TTL 5min)
  - L2: Redis cache for user data (TTL 30min)
  - Cache invalidation on password change/account lock
- Async Processing: Email and notification operations in background workers
- Load Testing: Simulate 2x expected peak with Locust before production)

📝 Specification Output
Expected Deliverables (⭐ = mandatory for simple tasks)
{{deliverables}} (e.g.:
⭐ 1. API Implementation:
- Complete endpoints with Pydantic validation
- Consistent error handling with appropriate HTTP codes
- Examples of request/response in documentation

⭐ 2. Test Suite:
- Unit tests for business logic (90%+ coverage, pure functions only)
- Integration tests for complete flows (real/fake adapters, no mocks of core logic)
- Security tests for common vulnerabilities (SQLi, XSS, CSRF)
- Load tests with 1000+ req/sec simulated

⭐ 3. Infrastructure as Code:
- Optimized Dockerfile with multi-stage build
- Kubernetes deployment manifests with liveness/readiness probes
- Terraform scripts for cloud resource provisioning

4. Documentation:
- Complete OpenAPI specification with examples
- Architecture Decision Record (ADR) explaining choices
- Deployment guide with rollback procedure
- Troubleshooting section with common scenarios)

Code Structure Guidelines
{{code_structure}} (e.g.:
```
src/
├── core/                  # Pure domain: functions, value objects, exceptions
│   ├── models.py          # Immutable value objects (@dataclass(frozen=True))
│   ├── use_cases.py       # Pure functions implementing business rules
│   └── ports/             # Interfaces only (Protocols)
│       ├── user_ports.py
│       └── auth_ports.py
│
├── adapters/              # Implementations of core ports
│   ├── db/                # Database implementations
│   │   └── user_repository.py
│   ├── api/               # API/handler implementations
│   │   └── auth_routes.py
│   └── external/          # Third-party service integrations
│       └── email_service.py
│
├── interfaces/            # System boundaries
│   ├── api/               # FastAPI routers and controllers
│   └── cli/               # Command-line interface
│
└── app.py                 # Composition root for dependency injection
```

Environment Configuration
{{environment_config}} (e.g.:
```env
# .env.example - NEVER commit actual .env file
SERVICE_NAME=auth-service
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
DATABASE_POOL_MIN=5
DATABASE_POOL_MAX=20

# Security
JWT_SECRET_KEY=your_strong_secret_here  # ⚠️ Must be 32+ chars random
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_SESSION_TTL=300  # 5 minutes

# External Services
AUTH0_DOMAIN=your-domain.auth0.com
SENDGRID_API_KEY=your_sendgrid_api_key
CLOUDFLARE_API_TOKEN=your_cloudflare_token

# Observability
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn
PROMETHEUS_PORT=9090
```

✅ Validation Framework
Testing Strategy (⭐ = mandatory for simple tasks)
{{testing_strategy}} (e.g.:
⭐ TDD Process (mandatory):
- Red: Write failing acceptance test against primary port
- Green: Implement minimal code to pass test (no refactoring yet)
- Refactor: Improve structure while keeping tests green

⭐ Unit Testing (≥70% of suite):
- Target Functional Core only (pure functions, no dependencies)
- Must pass in <100ms each
- Test edge cases: expired tokens, locked users, attack attempts
- Name pattern: test_<function>_<scenario>_<expectation>
- Example:
```python
def test_user_auth_with_invalid_email_raises_error():
    with pytest.raises(ValueError):
        UserAuth(user_id="123", email="invalid-email", password_hash="hash")
```

⭐ Integration Testing (≤25%):
- Test Core + Adapter combinations (real/fake adapters, no mocks of domain logic)
- Test boundaries between components
- Validate integration with database and external services
- Test failure scenarios: email service unavailable, database overload

⭐ Acceptance Testing:
- Call primary ports directly (bypassing HTTP/CLI)
- Test critical paths only
- Execute against production-like environment

Security Testing:
- OWASP ZAP scan for common vulnerabilities
- Test brute force protection (lock after 5 failed attempts)
- Validate that passwords are never exposed in logs or responses

Performance Testing:
- Load test with 1000 req/sec for 5 minutes
- Chaos engineering: simulate database and cache failures
- Monitor for memory leaks during prolonged execution)

Quality Gates (⭐ = mandatory for simple tasks)
{{quality_gates}} (e.g.:
⭐ Code Quality:
- 0 critical/high issues in SonarQube
- Ruff formatting compliance (line length 88, no unused imports)
- Mypy strict mode passing for core packages
- 85%+ general test coverage, 95%+ for critical code
- Code review by at least 2 senior people

⭐ Security Gates:
- Zero high/critical vulnerabilities in SAST/DAST scan (Bandit + Safety)
- All dependencies updated (no known CVEs in Safety check)
- Secrets management validated (no hardcoded credentials)
- Pydantic models used ONLY at boundaries, not in core logic

⭐ Architecture Compliance:
- Core package has no dependencies on infrastructure packages
- No circular dependencies between packages
- Primary ports named as `*CommandPort`, `*QueryPort`
- Secondary ports named as `*GatewayPort`, `*RepositoryPort`, `*PublisherPort`
- Value objects are immutable (`@dataclass(frozen=True)`)

Documentation Gates:
- OpenAPI spec validated with Spectral
- Architecture Decision Record updated
- User guide with real usage examples)

Security Requirements (⭐ = mandatory for simple tasks)
{{security_requirements}} (e.g.:
⭐ Input Validation:
- All endpoints validate input with Pydantic models (boundary only)
- Data sanitization to prevent XSS/SQL injection
- Rate limiting by IP and user ID (token bucket algorithm)

⭐ Authentication/Authorization:
- JWT validation on all protected endpoints
- Role-based access control for administrative operations
- MFA requirement for critical changes (password change, account deletion)

⭐ Data Protection:
- Passwords stored with Argon2 hashing + salt
- Sensitive data encrypted at rest (PII, access tokens)
- TLS 1.3+ mandatory for all communications
- Never expose mutable collections (convert to tuple/frozenset)

Audit & Monitoring:
- Logging of all authentication operations
- Real-time alerts for suspicious patterns (many failed logins)
- Log retention for 90 days for compliance)

⚠️ Known Gotchas & Risk Mitigation
Common Pitfalls (⭐ = mandatory for simple tasks)
{{common_pitfalls}} (e.g.:
⭐ TDD Violations:
- Pitfall: Writing implementation before tests "to explore the problem"
- Mitigation: Start with failing acceptance test against primary port

⭐ Architecture Violations:
- Pitfall: Domain/core objects importing infrastructure packages
- Mitigation: Enforce package boundaries with dependency tests
- Detection: Use import-linter to prevent illegal imports

⭐ Immutability Violations:
- Pitfall: Direct mutation of value objects (user.email = "new@ex.com")
- Mitigation: Use transformation methods that return new instances
- Detection: Unit tests that attempt to modify frozen dataclasses

Testing Anti-patterns:
- Pitfall: Mocking core logic (mock.patch('core.calculate_total'))
- Mitigation: Test pure functions directly, use real/fake adapters for integration
- Detection: Code review checklist for test anti-patterns)

Risk Areas & Mitigation Strategies
{{risk_areas}} (e.g.:
- High Risk: JWT key compromise
  - Mitigation: Automatic key rotation, HSM for storage
  - Detection: Monitoring for anomalous token usage
  - Testing: Security tests for key rotation scenarios
- Medium Risk: Brute force attacks on login endpoints
  - Mitigation: Adaptive rate limiting, CAPTCHA after multiple failures
  - Detection: Alerts for suspicious access patterns
  - Testing: Load tests with malicious traffic simulation
- Low Risk: Downtime during deployment
  - Mitigation: Blue-green deployment, feature flags for quick rollback
  - Detection: Automated health checks pre and post-deploy
  - Testing: Chaos engineering for deployment failure scenarios)

🔄 Execution Context
Prerequisites (⭐ = mandatory for simple tasks)
{{prerequisites}} (e.g.:
⭐ Development Setup:
- Python 3.13+, PostgreSQL 14, Redis 7.0 installed
- Poetry environment configured with dependencies from pyproject.toml
- Ruff, Mypy, Bandit, and Safety tools installed
- Ruff configuration: line-length=88, select=["E", "F", "I", "B", "C4", "T20"]
- Mypy configuration: strict=true for core packages

⭐ Knowledge Requirements:
- TDD process (Red → Green → Refactor)
- Hexagonal Architecture principles and port naming conventions
- Immutable value objects pattern with @dataclass(frozen=True)
- Python toolchain standards (Poetry, Ruff, Mypy, etc.)

Tooling:
- Docker and Kubernetes for local development
- Postman/Insomnia for manual API testing
- Locust for performance testing
- import-linter for package boundary enforcement)

Development Process (⭐ = mandatory for simple tasks)
{{development_process}} (e.g.:
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
17. Final validation and production deployment)

Collaboration Points
{{collaboration_points}} (e.g.:
- Security Team Review: Before any code is written, validate security architecture
- Architecture Review: Validate Hexagonal Architecture compliance and port design
- TDD Pair Programming: Work with senior developer on complex business logic
- Code Review Checklist: Include architecture compliance, TDD adherence, and Boy Scout Rule items
- Legal/Compliance Check: Validate personal data handling and retention policies)

📊 Success Metrics
Performance Metrics (⭐ = mandatory for simple tasks)
{{performance_metrics}} (e.g.:
⭐ Core Performance:
- Login latency: < 150ms p95
- Token refresh latency: < 50ms p95
- Throughput: 1500+ req/sec at peak
- Error rate: < 0.05% for critical operations

⭐ Resource Utilization:
- CPU usage: < 60% under normal load
- Memory usage: < 500MB per instance
- Database connections: < 80% of maximum pool
- Cache hit ratio: > 95% for frequently accessed data

Availability:
- Uptime: 99.95% monthly
- Mean Time To Recovery (MTTR): < 5 minutes
- Incident rate: < 1 critical incident per month)

Quality & Reliability Metrics (⭐ = mandatory for simple tasks)
{{quality_metrics}} (e.g.:
⭐ Code Quality:
- Ruff formatting compliance: 100%
- Mypy strict mode passing for core: 100%
- Test coverage: 85%+ general, 95%+ for critical code
- Code quality score: A in SonarQube
- Boy Scout Rule items per PR: ≥1

⭐ Security Posture:
- Zero high/critical vulnerabilities in Bandit/Safety scans
- Average time to fix vulnerabilities: < 24h for critical
- Compliance score: 100% with internal standards

Architecture Health:
- Package dependency violations: 0
- Core package import violations: 0
- Immutable value objects usage: 100% for domain models
- TDD adherence score: 95%+ (tests before implementation))

Business Impact Metrics
{{business_metrics}} (e.g.:
- User adoption rate: > 90% of users migrating to new system in 30 days
- Fraud reduction: 30% decrease in compromised accounts
- Support ticket reduction: 40% fewer tickets related to login issues
- Cost efficiency: $0.005 per successful authentication (vs $0.008 previous)
- Development velocity: 40% faster feature delivery with fewer bugs

🔧 Template Usage Guidelines
🚀 Quick Start for Simple Tasks:
For simple tasks (⭐), focus on these mandatory sections:
1. PRP Metadata (basic info)
2. Business Context Layer (clear objectives)
3. Technical Translation (essential technical specifications)
4. Specification Output (minimum deliverables)
5. Validation Framework (critical tests and quality gates)

📚 Full Process for Complex Tasks:
For complex or critical tasks, complete ALL sections with specific details. Use the provided examples as a guide.

🔄 Iterative Refinement:
- Start with ⭐ version (basic) for MVP
- Execute and evaluate result
- Refine context based on feedback
- Add additional sections as needed
- Repeat until success metrics are met

✅ Validation Checklist Before Execution:
- All placeholders ({{ }}) have been replaced
- TDD process is explicitly defined
- Hexagonal Architecture principles are followed
- Immutable value objects pattern is specified
- Ruff and Mypy configurations are included
- Test distribution requirements are met (70% unit, 25% integration, 5% e2e)
- Dependency versions specified explicitly
- Success criteria are measurable and objective
- Relevant Known Gotchas have been documented
- RAG sources are up-to-date and accessible