## 📂 CURRENT PROJECT STRUCTURE
ctxfy/
├── src/
│   ├── core/ (functional core: models, ports, use_cases, workflows)
│   │   ├── models/ (frozen dataclasses, value objects)
│   │   ├── ports/ (protocol definitions)
│   │   ├── use_cases/ (business logic)
│   │   └── workflows/ (orchestration logic)
│   └── shell/ (imperative shell: adapters, orchestrators, registry)
│       ├── adapters/ (external integrations)
│       ├── orchestrators/ (MCP integration)
│       └── registry/ (dynamic tool/prompt registration)
├── tests/
├── resources/
├── .ctxfy/ (MCP-specific configurations)
└── config files (pyproject.toml, tox.ini, etc.)

## 🎨 OBSERVED PATTERNS
- Architecture: Functional Core/Imperative Shell (FCIS) with Ports & Adapters - src/core contains pure business logic, src/shell handles MCP I/O
- Naming: Domain-driven with suffix conventions (Port, UseCase, Workflow, Tool, Registry) and NewType for value objects (SpecificationId, BusinessRequirements)
- Value Objects: NewType wrappers with frozen dataclasses (SpecificationResult) enabling type safety and immutability
- Ports/Adapters: Protocol-based interfaces in core/ports, concrete implementations in shell/adapters with dependency injection
- Toolchain: Python 3.13+, Poetry, FastMCP framework, Ruff/Mypy/Pytest with 80% coverage requirement
- Anti-patterns: Mixed sync/async patterns in specification_ports.py (execute method signatures differ)

## ⚠️ CONTEXT VALIDATION
✅ FCIS architecture alignment: Core contains pure functions, shell handles side effects
✅ Token limit compliance: 500/500