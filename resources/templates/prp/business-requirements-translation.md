🔄 BUSINESS REQUIREMENTS TRANSLATION TEMPLATE
📋 Context & Metadata
Translation ID: {{translation_id}} (e.g., TR-USER-MGMT-001)
Business Requirement: "{{business_requirement}}"
Domain Context: {{domain_context}} (e.g., E-commerce, Healthcare, FinTech)
Stakeholders: {{stakeholders}} (Product Owner: {{po_name}}, Tech Lead: {{tech_lead_name}})
Priority: {{priority}} (High/Medium/Low)
Complexity Level: {{complexity}} (Simple/Standard/Complex)
Last Updated: {{date}}
AI Context: {{ai_context}} (e.g., "Use as basis to generate technical PRP following Hexagonal Architecture")

🔍 Business Requirement Analysis
Original Requirement
{{original_requirement_text}} (e.g., "We need a system that allows users to manage their profiles securely and intuitively, with support for updating personal information, preferences, and privacy settings")

Stakeholder Context
Business owner: {{business_owner}} (e.g., "VP of Product - focused on user retention and NPS")
User perspective: {{user_perspective}} (e.g., "Users want full control over their data without technical complexity")
Market context: {{market_context}} (e.g., "Increasing privacy regulation (GDPR, CCPA) and modern UX expectations")
Strategic importance: {{strategic_importance}} (e.g., "Critical for compliance and churn reduction - direct impact on LTV")

Ambiguities & Assumptions
Ambiguous terms: {{ambiguous_terms}} (e.g., "secure" - needs concrete definition; "intuitive" - needs UX metrics)
Unstated assumptions: {{unstated_assumptions}} (e.g., "Users have valid email", "Mobile devices are primary")
Missing context: {{missing_context}} (e.g., "Which personal information fields are mandatory?", "Granularity level for privacy")
Clarification needed: {{clarification_needed}} (e.g., "Define SLA for profile operations", "Specify accessibility requirements")

🎯 Technical Translation
AI Context Requirements
{{ai_context_requirements}} (e.g.:
- **Model Guidance**: "You are a senior software architect specialized in user systems with 10+ years experience in Hexagonal Architecture and TDD"
- **Context Sources**: "Use official FastAPI documentation, OWASP security guides, and our internal architecture standards at /ai_docs/"
- **Output Format**: "Structure response as complete technical PRP with detailed sections following our templates"
- **Success Criteria**: "Generated PRP should enable implementation without ambiguity by a junior engineer, following TDD and architecture rules")

Technical Objective
{{technical_objective}} (e.g., "Develop a user profile management service that provides secure, performant, and privacy-compliant API with 99.9% availability, following Hexagonal Architecture principles")

Core Capabilities Required
{{capability1}}:
- Description: {{capability1_description}} (e.g., "Complete CRUD for user profile information using immutable value objects")
- User value: {{capability1_value}} (e.g., "Full control over personal data without needing support")
- Technical complexity: {{capability1_complexity}} (e.g., "Medium - requires complex validation and data versioning")
- AI Context: {{capability1_ai_context}} (e.g., "Use @dataclass(frozen=True) for all domain models, validate invariants in __post_init__")

{{capability2}}:
- Description: {{capability2_description}} (e.g., "Granular privacy and data sharing management following Hexagonal Architecture")
- User value: {{capability2_value}} (e.g., "GDPR/CCPA compliance and user consent control")
- Technical complexity: {{capability2_complexity}} (e.g., "High - requires state machine for consents and audit trails")
- AI Context: {{capability2_ai_context}} (e.g., "Define primary ports as UserCommandPort/UserQueryPort, secondary ports as UserRepositoryPort/EmailGatewayPort")

{{capability3}}:
- Description: {{capability3_description}} (e.g., "Real-time synchronization across devices and sessions using event-driven architecture")
- User value: {{capability3_value}} (e.g., "Consistent experience on mobile and web without manual refresh")
- Technical complexity: {{capability3_complexity}} (e.g., "Medium-High - requires WebSockets and conflict resolution")
- AI Context: {{capability3_ai_context}} (e.g., "Implement TDD from the start: write failing acceptance test against primary port before any implementation")

[Continue for all capabilities]

Technical Constraints & Requirements
Performance requirements: {{performance_requirements}} (e.g., "Profile loading < 300ms p95, updates < 500ms")
Security requirements: {{security_requirements}} (e.g., "OWASP ASVS Level 2 compliance, encryption at rest for PII, Ruff and Bandit security scans")
Integration requirements: {{integration_requirements}} (e.g., "Integrate with existing authentication service, events for analytics using RabbitMQ")
Data requirements: {{data_requirements}} (e.g., "Schema versioning, audit trails for all changes, GDPR right to erasure, immutable value objects")
Compliance requirements: {{compliance_requirements}} (e.g., "GDPR, CCPA, SOC2 Type II, internal data handling policies, Mypy strict mode for core")

Architecture Considerations
Pattern recommendations: {{pattern_recommendations}} (e.g., "Hexagonal Architecture with CQRS for separate read/write operations, Event Sourcing for audit")
Component boundaries: {{component_boundaries}} (e.g., "Core package (domain models, pure functions), Adapters package (database, external services), Interfaces package (API, CLI)")
Data flow considerations: {{data_flow_considerations}} (e.g., "Pydantic models only at boundaries, convert to immutable value objects immediately, event-driven updates for cache consistency")
Scalability approach: {{scalability_approach}} (e.g., "Horizontal scaling with load balancer, read replicas for frequent queries, connection pooling configuration")

🔍 RAG Integration & Context Stack Reference
RAG Sources
Primary Documentation: {{rag_primary_docs}} (e.g.:
- https://gdpr-info.eu/art-17-gdpr/ (Right to erasure)
- https://owasp.org/www-project-cheat-sheets/ (Security standards)
- https://fastapi.tiangolo.com/v0.95.0/tutorial/security/ (Implementation guides)
- https://www.cosmicpython.com/ (Hexagonal Architecture patterns))

Internal Knowledge: {{rag_internal_knowledge}} (e.g.:
- /ai_docs/architecture_standards.md (Hexagonal Architecture rules)
- /ai_docs/testing_strategy.md (TDD and testing requirements)
- /ai_docs/security_standards.md (our internal policy)
- /ai_docs/user_profile_patterns.md (approved patterns)
- /examples/profile_service_success.md (previous successful implementations))

Context Stack Reference
{{context_stack_reference}} (e.g.:
- **System Layer**: Follow Hexagonal Architecture principles from /ai_docs/architecture_standards.md
- **Domain Layer**: Include specific user management and privacy compliance context
- **Task Layer**: Focus on security and data governance as primary priorities
- **RAG Integration**: Use documentation sources for current best practices
- **Reference**: PRP-ID: PRP-USER-PROFILE-001)

🛠️ Implementation Strategy
Technical Approach
{{technical_approach_overview}} (e.g., "Develop stateless microservice with RESTful API following TDD process (Red → Green → Refactor), using Hexagonal Architecture with core isolated from infrastructure, immutable value objects for domain models, and real/fake adapters for testing")

Key Technical Decisions
Technology stack: {{technology_stack}} (e.g., "Python 3.13, FastAPI 0.95.0, PostgreSQL 14, Redis 7.0")
Architecture style: {{architecture_style}} (e.g., "Hexagonal Architecture with domain-driven design, primary ports for driving logic, secondary ports for driven infrastructure")
Data model strategy: {{data_model_strategy}} (e.g., "Immutable value objects (@dataclass(frozen=True)) for domain models, Pydantic models only at API boundaries, JSONB for flexible fields with schema versioning")
Error handling approach: {{error_handling_approach}} (e.g., "Problem Details RFC 7807 for consistent errors at boundaries, pure exception handling in core, circuit breakers for external dependencies")
Testing strategy: {{testing_strategy}} (e.g., "TDD mandatory with 70% unit tests (pure functions), 25% integration tests (real/fake adapters), 5% end-to-end tests, Boy Scout Rule refactoring per PR")

Resource Implications
Development effort: {{development_effort}} (e.g., "3-4 weeks for complete MVP with comprehensive tests following TDD")
Infrastructure needs: {{infrastructure_needs}} (e.g., "2 instances for high availability, PostgreSQL cluster with automatic failover, Redis for caching")
Maintenance considerations: {{maintenance_considerations}} (e.g., "Query performance monitoring, alerts for schema drift, regular dependency updates with Safety checks, architecture compliance monitoring")
Team skills required: {{team_skills_required}} (e.g., "Python TDD experience, Hexagonal Architecture implementation, PostgreSQL optimization, security best practices, GDPR compliance, Ruff/Mypy toolchain proficiency")

✅ Validation Protocol
Acceptance Criteria (⭐ = mandatory for simple translations)
Functional criteria:
⭐ {{functional_criterion1}} (e.g., "Users can update name, email, and profile photo using immutable value objects")
⭐ {{functional_criterion2}} (e.g., "Privacy settings can be changed granularly with audit trails")
{{functional_criterionN}} (e.g., "Change history is available for audit with GDPR compliance")

Quality criteria:
⭐ {{quality_criterion1}} (e.g., "Response time < 300ms for 95% of requests, Ruff formatting compliance 100%")
⭐ {{quality_criterion2}} (e.g., "Zero data leaks in security tests, Mypy strict mode passing for core")
{{quality_criterionN}} (e.g., "100% compliance with WCAG 2.1 accessibility checklist, zero package dependency violations")

Verification Approach
Testing approach: {{testing_approach}} (e.g., "TDD process with acceptance tests against primary ports, unit tests for pure functions, integration tests with real/fake adapters")
Performance validation: {{performance_validation}} (e.g., "Locust tests simulating 1000 simultaneous users, connection pooling optimization")
Security validation: {{security_validation}} (e.g., "OWASP ZAP scan, Bandit security scan, Safety dependency check, external penetration testing")
User acceptance process: {{uac_process}} (e.g., "Beta testing with 10% of users, feedback collection via surveys, architecture compliance review")

🔍 Cross-Reference Mapping - AI Enhanced
Requirement Traceability (AI-Generated Matrix)
| Business Requirement | Technical Component | Validation Method | Owner | Risk Level |
|----------------------|---------------------|-------------------|-------|------------|
| {{business_req1}} | {{component1}} | {{validation1}} | {{owner1}} | {{risk1}} |
| {{business_req2}} | {{component2}} | {{validation2}} | {{owner2}} | {{risk2}} |
| {{business_reqN}} | {{componentN}} | {{validationN}} | {{ownerN}} | {{riskN}} |

Dependencies & Impacts
System dependencies: {{system_dependencies}} (e.g., "Authentication service must be stable before deployment, RabbitMQ for event processing")
Data dependencies: {{data_dependencies}} (e.g., "Schema migration must be tested with historical data, GDPR data mapping completed")
Timeline dependencies: {{timeline_dependencies}} (e.g., "Legal approval required before public launch, security audit completed")
Risk factors: {{risk_factors}} (e.g., "High risk of downtime during migration, rollback plan mandatory, architecture compliance risk if TDD not followed")

💔 Past Implementation Failures & Lessons Learned
Previous Failures
{{past_failure1}}:
- What happened: {{failure1_description}} (e.g., "Profile service downtime during launch due to connection pool exhaustion")
- Root cause: {{failure1_root_cause}} (e.g., "Incorrect database connection pool configuration, no load testing")
- Impact: {{failure1_impact}} (e.g., "2 hours downtime, 15% of users affected, $50K revenue loss")
- Lesson learned: {{failure1_lesson}} (e.g., "Always test connection limits in staging with realistic load, implement circuit breakers")

{{past_failure2}}:
- What happened: {{failure2_description}} (e.g., "User email data leak in unredacted logs")
- Root cause: {{failure2_root_cause}} (e.g., "PII logging without automatic sanitization, no security scanning")
- Impact: {{failure2_impact}} (e.g., "Reported security incident, damaged reputation, compliance violation")
- Lesson learned: {{failure2_lesson}} (e.g., "Implement automatic PII masking in all loggers, mandatory Bandit/Safety scans in CI pipeline")

{{past_failure3}}:
- What happened: {{failure3_description}} (e.g., "Architecture degradation over time with circular dependencies")
- Root cause: {{failure3_root_cause}} (e.g., "No package dependency enforcement, core importing infrastructure packages")
- Impact: {{failure3_impact}} (e.g., "20% increase in bug rate, 3x longer development time for new features")
- Lesson learned: {{failure3_lesson}} (e.g., "Enforce package boundaries with import-linter, mandatory architecture reviews for all PRs")

[Continue for relevant past failures]

📝 Implementation Notes
🚀 **Quick Translation Checklist (for Simple Requirements)**:
For simple requirements, focus on these essential points:
- [ ] Clear and measurable Technical Objective following architecture standards
- [ ] 3-5 Core Capabilities with defined user value and TDD approach
- [ ] Basic security and performance requirements with toolchain standards
- [ ] Functional and quality Acceptance Criteria with test distribution ratios
- [ ] Key stakeholders identified with collaboration points

📚 **Comprehensive Process (for Complex Requirements)**:
For complex or critical requirements:
1. Conduct alignment workshop with stakeholders
2. Document all ambiguities and assumptions
3. Research relevant regulations and standards
4. Analyze related past failures and lessons learned
5. Create complete traceability matrix
6. Validate technical translation with team leads
7. Document architecture decisions and trade-offs
8. Define RAG sources for current best practices

🔄 **AI-Assisted Translation Workflow**:
1. **Input Preparation**: 
   - Fill initial sections with business context
   - Identify ambiguous terms and risk areas
   - Define clear success criteria with metrics

2. **AI Context Engineering**:
   - Generate systematic context using Context Stack reference
   - Include relevant RAG sources for specific domain and architecture standards
   - Define clear constraints based on Python toolchain and architecture rules

3. **Generation & Validation**:
   - Execute translation with complete context
   - Validate result against acceptance criteria and architecture standards
   - Check for TDD compliance, immutable value objects usage, package dependencies
   - Iteratively refine context based on feedback

4. **Human Review**:
   - Technical review by senior engineer focusing on architecture compliance
   - Business validation with product owner
   - Security review with security team
   - Final adjustments and approval for implementation

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