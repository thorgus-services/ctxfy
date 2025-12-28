# Backend PRP Examples

## Example 1: Simple User Authentication (⭐)

```markdown
🏷️ PRP Metadata
PRP ID: PRP-AUTH-001
Type: Backend Development
Domain: Authentication
Technology Stack: Python/FastAPI/PostgreSQL
Complexity Level: Low

🎯 Business Context Layer
Business Objectives
Implement secure user authentication for mobile app with session management
SLAs & Performance Requirements
Availability: 99.9% (including maintenance window)
Latency: < 100ms p95 for login operations
Error Rate: < 0.01% for authentication failures

🔧 Technical Translation
Architecture Pattern
Hexagonal Architecture with Ports & Adapters
Technology Specifications
Framework: FastAPI 0.95.0
Database: PostgreSQL 14
Security Specifications
Authentication: JWT with short TTL (15 minutes)
Authorization: RBAC with basic roles (user, admin)

📝 Specification Output
Expected Deliverables (⭐)
⭐ 1. API Implementation:
- POST /login endpoint with email/password validation
- POST /refresh endpoint for token refresh
- GET /me endpoint for user profile
⭐ 2. Test Suite:
- Unit tests for authentication core logic
- Integration tests for complete login flow
⭐ 3. Infrastructure as Code:
- Dockerfile with multi-stage build
- PostgreSQL migration scripts

✅ Validation Framework
Testing Strategy (⭐)
⭐ TDD Process (mandatory):
Red: Write failing test for login with invalid credentials
Green: Implement minimal validation logic
Refactor: Extract pure functions and improve structure
⭐ Unit Testing (≥70% of suite):
def test_login_fails_with_invalid_email():
    with pytest.raises(InvalidEmailError):
        login_user(email="invalid-email", password="pass123")
```

## Example 2: Payment Processing System (Complex)

```markdown
🏷️ PRP Metadata
PRP ID: PRP-PAY-002
Type: Backend Development
Domain: Payment Processing
Technology Stack: Python/FastAPI/PostgreSQL/RabbitMQ/Redis
Complexity Level: High
✨ AI Context Adaptation
Model Compatibility Notes
Claude 3: Excellent for complex business logic, needs concrete examples for payment state machines
GPT-4: Good for architectural patterns but may need strict validation gates to prevent creative payment flows
Llama 3: Reliable for consistent code generation but needs explicit state transition definitions
Context Drift Mitigation
- Include specific dependency versions: FastAPI==0.95.0, Pydantic==2.12
- Reference current payment service structure in src/core/payments/
- Explicitly forbid direct database calls in core layer

🎯 Business Context Layer
Business Objectives
Implement PCI-DSS compliant payment processing system with multiple payment methods, fraud detection, and webhook notifications while maintaining 99.99% uptime for transaction processing
SLAs & Performance Requirements
Availability: 99.99% (24/7 with no maintenance window)
Latency: < 500ms p95 for payment processing, < 100ms for status checks
Throughput: 5000 transactions/second peak, 1000/second average
Data Freshness: < 5 seconds for transaction status updates
Error Rate: < 0.001% for payment processing failures
Compliance: PCI-DSS Level 1, SOC2 Type II, GDPR

👥 Stakeholder Analysis
Technical Stakeholders
- Frontend Team: Needs idempotent API endpoints with clear error codes
- DevOps/SRE: Requires comprehensive metrics, alerts, and auto-scaling capabilities
- Security Team: Mandates PCI-DSS compliance, audit trails, and encryption requirements
- Data Engineering: Needs transaction events for analytics and fraud pattern detection
Business Stakeholders
- Product Managers: Focus on payment method coverage and checkout conversion rates
- Finance Team: Requires reconciliation capabilities and settlement reports
- Legal/Compliance: Enforces regulatory requirements and data retention policies
- Executive Sponsors: Interested in payment success rates and revenue impact

📋 Requirement Extraction
API & Interface Specifications
- RESTful endpoints with OpenAPI 3.1 specification
- Webhook callbacks for payment status updates
- Idempotency keys for duplicate transaction prevention
- WebSockets for real-time payment status monitoring
Data Models & Entities
```python
from dataclasses import dataclass, field
from typing import NewType, Optional
from decimal import Decimal

PaymentId = NewType('PaymentId', str)
Amount = NewType('Amount', Decimal)
CurrencyCode = NewType('CurrencyCode', str)

@dataclass(frozen=True)
class Payment:
    """Immutable value object for payment transactions"""
    id: PaymentId
    amount: Amount
    currency: CurrencyCode
    status: str  # enum: pending, completed, failed, refunded
    created_at: float
    customer_id: str
    
    def with_status(self, new_status: str) -> "Payment":
        """Return new instance with updated status (immutability)"""
        return Payment(
            id=self.id,
            amount=self.amount,
            currency=self.currency,
            status=new_status,
            created_at=self.created_at,
            customer_id=self.customer_id
        )

@dataclass(frozen=True)
class PaymentIntent:
    """Value object for payment intent creation"""
    amount: Amount
    currency: CurrencyCode
    customer_id: str
    payment_method: str  # credit_card, bank_transfer, etc.
    description: str
    metadata: dict = field(default_factory=dict)
```
External Dependencies
- Stripe: Primary payment processor (SLA 99.99%)
- Redis 7.0: Caching and rate limiting (SLA 99.95%)
- RabbitMQ: Event processing for notifications (SLA 99.9%)
- Datadog: Monitoring and alerting (SLA 99.9%)

🔍 RAG Integration Section
Documentation Sources
Primary Sources:
- https://stripe.com/docs/api (v2023-10-16)
- https://www.postgresql.org/docs/14/pgcrypto.html
- https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
Internal Knowledge:
- /ai_docs/pci_dss_requirements.md
- /ai_docs/fraud_detection_patterns.md
- /examples/payment_service_success_cases.md
Retrieval Protocol
- For each PCI-DSS requirement mentioned, search official documentation
- Validate security patterns against OWASP cheat sheets
- Check version compatibility before implementing payment integrations
- If conflict between sources, prioritize Stripe API documentation + PCI-DSS requirements

🔧 Technical Translation
Architecture Pattern
Pattern: Hexagonal Architecture with Event Sourcing
Primary Ports:
- PaymentCommandPort (driving port for payment commands)
- PaymentQueryPort (driving port for payment queries)
Secondary Ports:
- PaymentGatewayPort (driven port for payment processor integration)
- TransactionRepositoryPort (driven port for transaction storage)
- NotificationPublisherPort (driven port for event publishing)
Payment Flow:
1. Create payment intent (command)
2. Process payment with selected method (command)
3. Record transaction events (events)
4. Send webhook notifications (events)
5. Generate settlement reports (query)
Security Layers:
- Idempotency keys for duplicate prevention
- Rate limiting by customer ID and IP
- Sensitive data encryption at rest and in transit
- Real-time fraud detection with risk scoring

Technology Specifications
Framework: FastAPI 0.95.0 with async support
Database: PostgreSQL 14 with pgcrypto extension
Caching: Redis 7.0 with dynamic TTL for payment states
Messaging: RabbitMQ 3.12 for event processing
Observability: OpenTelemetry + Datadog + ELK stack

Security Specifications
Authentication: JWT with MFA for admin operations
Authorization: RBAC with payment-specific permissions
Data Protection: AES-256 encryption for PII, tokenization for card data
Audit Logging: Immutable logs for all payment events, 7-year retention
Compliance: PCI-DSS Level 1, GDPR right to erasure, SOC2 Type II

Performance Considerations
Connection Pooling: 100 minimum connections, 500 maximum for PostgreSQL
Caching Strategy:
- L1: In-memory cache for payment states (TTL 1min)
- L2: Redis cache for customer payment history (TTL 30min)
Async Processing:
- Webhook notifications in background workers
- Settlement report generation in scheduled jobs
Load Testing:
- Simulate 2x expected peak (10,000 tps) with Locust
- Chaos testing with payment processor failures

📝 Specification Output
Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ 1. API Implementation:
- Complete endpoints with Pydantic validation
- Idempotency key handling for all payment commands
- Rate limiting by customer ID and IP address
- Webhook signature verification
⭐ 2. Test Suite:
- Unit tests for business logic (90%+ coverage)
- Integration tests with real/fake payment gateways
- Security tests for common vulnerabilities
- Load tests with 5000+ transactions/second
⭐ 3. Infrastructure as Code:
- Kubernetes deployment with auto-scaling
- PostgreSQL cluster with read replicas
- Redis cluster with failover
- Monitoring dashboards and alert definitions
Documentation:
- OpenAPI specification with examples
- Architecture Decision Record (ADR)
- PCI-DSS compliance checklist
- Disaster recovery procedures

Code Structure Guidelines
src/
├── core/                  # Pure domain logic
│   ├── models/            # Immutable value objects
│   │   ├── payment.py     # Payment value object
│   │   └── payment_intent.py
│   ├── use_cases/         # Pure business functions
│   │   ├── process_payment.py
│   │   └── handle_refund.py
│   └── ports/             # Interfaces only
│       ├── payment_command_port.py
│       ├── payment_query_port.py
│       └── payment_gateway_port.py
├── shell/                 # Infrastructure adapters
│   ├── adapters/
│   │   ├── stripe/
│   │   │   └── stripe_payment_adapter.py
│   │   ├── db/
│   │   │   └── transaction_repository.py
│   │   └── messaging/
│   │       └── payment_event_publisher.py
│   └── orchestrators/
│       └── payment_orchestrator.py  # ≤4 dependencies
└── app.py                 # Composition root

Environment Configuration
# .env.example
SERVICE_NAME=payment-service
ENVIRONMENT=production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/payments
DATABASE_POOL_MIN=100
DATABASE_POOL_MAX=500

# Security
JWT_SECRET_KEY=your_64_char_random_secret_here
JWT_ALGORITHM=HS512
PAYMENT_WEBHOOK_SECRET=webhook_secret_here

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PAYMENT_STATE_TTL=60

# External Services
STRIPE_API_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_secret_here
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

✅ Validation Framework
Testing Strategy (⭐ = mandatory for simple tasks)
⭐ TDD Process (mandatory):
1. Red: Write failing acceptance test against PaymentCommandPort
2. Green: Implement minimal code to process payment intent
3. Refactor: Extract pure functions and improve structure
⭐ Unit Testing (≥70% of suite):
Target Functional Core only (pure functions, no dependencies)
Must pass in <100ms each
Test edge cases: declined cards, timeout scenarios, duplicate payments
Example:
```python
def test_payment_fails_with_insufficient_funds():
    payment_intent = PaymentIntent(
        amount=Amount(Decimal('1000.00')),
        currency=CurrencyCode('USD'),
        customer_id='cust_123',
        payment_method='credit_card'
    )
    with pytest.raises(InsufficientFundsError):
        process_payment(
            payment_intent=payment_intent,
            customer_balance=Amount(Decimal('500.00'))
        )
```
⭐ Integration Testing (≤25%):
Test Core + Adapter combinations with real/fake adapters
Validate integration with Stripe API and database
Test failure scenarios: network timeouts, API rate limits
⭐ Acceptance Testing:
Call primary ports directly with end-to-end scenarios
Execute against production-like environment with live payment sandbox

Quality Gates (⭐ = mandatory for simple tasks)
⭐ Code Quality:
- 0 critical/high issues in SonarQube
- Ruff formatting compliance (line length 88)
- Mypy strict mode passing for core packages
- 85%+ general test coverage, 95%+ for critical code
⭐ Security Gates:
- Zero high/critical vulnerabilities in Bandit/Safety scans
- All dependencies updated (no known CVEs)
- Secrets management validated (no hardcoded credentials)
- PCI-DSS compliance checklist completed
⭐ Architecture Compliance:
- Core package has no dependencies on infrastructure packages
- No circular dependencies between packages
- Primary ports named as *CommandPort, *QueryPort
- Value objects are immutable (@dataclass(frozen=True))

⚠️ Known Gotchas & Risk Mitigation
Common Pitfalls (⭐ = mandatory for simple tasks)
⭐ TDD Violations:
Pitfall: Writing implementation before tests "to explore the problem"
Mitigation: Start with failing acceptance test against primary port
⭐ Architecture Violations:
Pitfall: Domain/core objects importing infrastructure packages
Mitigation: Enforce package boundaries with dependency tests
Detection: Run import-linter before each commit
⭐ Immutability Violations:
Pitfall: Direct mutation of payment objects (payment.status = "completed")
Mitigation: Use transformation methods that return new instances
Detection: Unit tests that attempt to modify frozen dataclasses

Risk Areas & Mitigation Strategies
High Risk: Payment data breach
Mitigation: Tokenization for card data, end-to-end encryption
Detection: Real-time monitoring for anomalous access patterns
Testing: Security penetration testing by third party
Medium Risk: Payment processing failures during peak
Mitigation: Circuit breakers, fallback payment methods
Detection: Alerts for failed payment rate > 1%
Testing: Chaos engineering with simulated payment processor failures
Low Risk: Settlement report discrepancies
Mitigation: Daily reconciliation jobs with automatic alerts
Detection: Automated reconciliation checks
Testing: End-to-end settlement testing with sample data

📊 Success Metrics
Performance Metrics (⭐ = mandatory for simple tasks)
⭐ Core Performance:
Payment processing latency: < 500ms p95
Status check latency: < 100ms p95
Throughput: 5000+ transactions/second at peak
Error rate: < 0.001% for payment processing
⭐ Resource Utilization:
CPU usage: < 70% under normal load
Memory usage: < 1GB per instance
Database connections: < 80% of maximum pool
Cache hit ratio: > 95% for payment states

Quality & Reliability Metrics (⭐ = mandatory for simple tasks)
⭐ Code Quality:
Ruff formatting compliance: 100%
Mypy strict mode passing for core: 100%
Test coverage: 85%+ general, 95%+ for critical code
Architecture compliance score: 100%
⭐ Security Posture:
PCI-DSS compliance score: 100%
Zero high/critical vulnerabilities in security scans
Average time to fix security issues: < 4 hours for critical

Business Impact Metrics
Payment success rate: > 99.5% of transactions
Checkout conversion rate: > 85% completion rate
Fraud detection accuracy: 95% true positive rate
Support ticket reduction: 60% fewer payment-related tickets
Revenue impact: $0.0015 per successful transaction (vs $0.0022 previous)
```

## Example 3: Legacy System Refactoring

```markdown
🏷️ PRP Metadata
PRP ID: PRP-REF-003
Type: Code Refactoring & Migration
Domain: Order Processing
Technology Stack: Python/FastAPI/PostgreSQL (migration from PHP/Laravel)
Complexity Level: Medium
✨ AI Context Adaptation
Model Compatibility Notes
Claude 3: Excellent for understanding legacy code patterns and suggesting clean refactoring approaches
GPT-4: Good for architectural migration strategies but needs explicit boundaries to prevent scope creep
Llama 3: Reliable for consistent code patterns but may need more examples of legacy-to-modern transformation
Context Drift Mitigation
- Reference current legacy system structure in /legacy/order_processing/
- Include specific PHP function patterns to be migrated
- Define explicit boundaries between legacy and new code
- Use feature flags for gradual migration path

🎯 Business Context Layer
Business Objectives
Refactor legacy PHP/Laravel order processing system to modern Python/FastAPI architecture while maintaining 99.95% uptime and zero data loss during migration
SLAs & Performance Requirements
Availability: 99.95% during migration (including maintenance windows)
Latency: < 200ms p95 for order creation (improvement from 500ms)
Throughput: 200 orders/second peak (improvement from 50 orders/second)
Data Consistency: 100% data integrity during migration
Zero Downtime: No customer-visible downtime during migration
Risk Level: High - impacts core revenue system

📋 Analysis Requirement Extraction
Current State Analysis
- Monolithic PHP/Laravel application with MVC pattern
- Order processing logic scattered across controllers and helpers
- Heavy coupling between business logic and database access
- No comprehensive test coverage (estimated 15%)
- Technical debt score: 85/100 (high risk)
Problem Areas Identification
1. God classes with 500+ lines of mixed responsibilities
2. Database queries embedded in controller methods
3. Business rules duplicated across multiple files
4. No clear separation between core logic and infrastructure concerns
5. Poor testability due to tight coupling

Technical Debt Assessment
Principal: 120 hours of refactoring effort
Interest: 8 hours/week of maintenance overhead
Deadline: Must be completed within 3 sprints (6 weeks)
Risk: High - system failure would impact 100% of revenue

🛠️ Implementation Strategy
Technical Approach
Strangler Fig Pattern:
1. Identify bounded contexts within order processing
2. Create new Python service for each bounded context
3. Implement adapter layer for legacy integration
4. Gradually route traffic to new service
5. Decommission legacy components

Key Technical Decisions
Technology stack: Python 3.13, FastAPI 0.95.0, PostgreSQL 14
Architecture style: Hexagonal Architecture with domain-driven design
Data model strategy: Event sourcing for order state transitions
Migration approach: Dual-write with reconciliation jobs
Testing strategy: TDD for new code, characterization tests for legacy behavior

✅ Validation Framework
Analysis Validation Criteria
- Order processing time reduced by 60% (500ms → 200ms)
- Test coverage increased to > 80% for critical code
- Zero functional regressions during migration
- Architecture compliance score > 90% (core/shell separation)

Risk Mitigation Strategy
Phase 1: Low-risk refactorings (1 week)
- Extract helper functions into service classes
- Create database repository interfaces
- Add characterization tests for critical paths
Phase 2: Structural refactorings (2 weeks)
- Implement Hexagonal Architecture for core domain
- Create adapter layer for legacy database
- Implement feature flags for gradual rollout
Phase 3: Migration & optimization (3 weeks)
- Dual-write implementation with reconciliation
- Performance optimization and load testing
- Final validation and legacy decommissioning

🔧 Template Usage Guidelines
🚀 Quick Start for Simple Tasks:
For simple tasks (⭐), focus on these mandatory sections:
- PRP Metadata (basic info)
- Business Context Layer (clear objectives)
- Technical Translation (essential technical specifications)
- Validation Framework (critical tests and quality gates)
📚 Full Process for Complex Tasks:
For complex or critical tasks, complete ALL sections with specific details. Use the provided examples as a guide.
🔄 Iterative Refinement:
Start with ⭐ version (basic) for MVP
Execute and evaluate result
Refine context based on feedback
Add additional sections as needed
Repeat until success metrics are met