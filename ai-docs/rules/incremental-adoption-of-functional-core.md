## Purpose
Provide a structured, metrics-driven approach to incrementally adopt the Functional Core & Imperative Shell paradigm in existing Python codebases without disruption.

## Guidelines
Three-phase adoption strategy:
1. Island creation: Implement new features using FCIS pattern
   - Start with high-business-value, low-I/O modules
   - Establish metrics baseline before implementation
   - Create exemplar modules to demonstrate patterns

2. Strangler pattern: Gradually extract Core from existing modules
   - Route new features through FCIS structure
   - Legacy code remains but receives no new features
   - Extract pure functions first, followed by effect isolation

3. Systematic migration: Refactor remaining modules
   - Prioritize by business value and bug frequency
   - Follow the 3-step extraction process for each module
   - Enforce architectural boundaries progressively

3-step extraction process for legacy modules:
Step 1: Identify pure functions
- Use static analysis to find functions with no external dependencies
- Mark candidate functions with @core_candidate decorator
- Focus on calculation-heavy, stateless functions first

Step 2: Move to Core with comprehensive tests
- Create src/core/<domain>.py module
- Write property-based tests covering all edge cases
- Ensure 100% test coverage before proceeding

Step 3: Create Shell adapters for remaining impure code
- Implement interfaces in src/shell/adapters/
- Update legacy code to use new Core through adapters
- Gradually route all execution paths through FCIS structure

Measurement and governance:
Track key metrics before and after adoption:
- Bug rates (especially regression bugs)
- Test coverage (Core must maintain >90% coverage)
- Mean time to fix defects
- Developer onboarding time

Architectural enforcement:
- Progressive static analysis rules (warning → error)
- Pre-commit hooks to prevent boundary violations
- Dependency visualization in CI pipeline
- Monthly architecture review sessions

Team enablement strategy:
Week 1: Fundamentals and simple Core modules
- Functional programming fundamentals workshop
- Pair programming on pure function extraction
- Writing property-based tests for Core functions

Week 2: Shell implementation and boundaries
- Implementing adapters for existing Core functions
- Boundary enforcement in code reviews
- Fixing boundary violations in legacy code

Week 3+: Leadership and mentoring
- Lead extraction of small modules using 3-step process
- Present architectural decisions to team
- Mentor other developers on FCIS concepts

## Violation Example:
```
# ❌ Bad - Big bang rewrite with no metrics
"""
Team decision:
- Rewrite entire monolith to FCIS in 3 months
- No measurements of current system
- No gradual migration path
- No enforcement mechanisms
"""
```

## Correct Example:
```
# ✅ Good - Incremental adoption with metrics
"""
Adoption roadmap:
1. Month 1: New Payment Service using FCIS
   - Baseline: 15% bug rate, 40% test coverage
   - Target: <5% bug rate, >85% coverage at 3 months

2. Month 2-3: Extract User Profile Core
   - Strangler pattern: new features through FCIS
   - Legacy remains but frozen for new features

3. Month 4-6: Migrate high-value modules
   - Priority: Order processing > Inventory > Reporting
   - Each follows the 3-step extraction process
"""
```

## Verification
```python
# scripts/validate_adoption_progress.py
def calculate_adoption_metrics():
    """Measure FCIS adoption progress across codebase"""
    metrics = {
        "modules_converted": count_fcis_modules(),
        "boundary_violations": count_boundary_violations(),
        "core_test_coverage": get_core_coverage(),
        "bug_rate_improvement": calculate_bug_improvement()
    }
    return metrics

def generate_adoption_report(metrics):
    """Generate executive summary for stakeholders"""
    progress = metrics["modules_converted"] / total_modules()
    report = f"""
    FCIS Adoption Progress
    ======================
    Overall Progress: {progress:.1%}
    
    Quality Metrics:
    - Core Test Coverage: {metrics['core_test_coverage']:.1f}%
    - Boundary Violations: {metrics['boundary_violations']} (target: 0)
    - Bug Rate Improvement: {metrics['bug_rate_improvement']:.1%}
    """
    return report
```

## Anti-Patterns
❌ Big-bang rewrites without metrics or incremental approach
❌ No measurement of current system to compare against
❌ All developers required to learn functional programming simultaneously
❌ No enforcement mechanisms to prevent boundary violations
❌ Extracting modules without comprehensive test coverage
❌ Mixing orchestrator logic with business rules during migration