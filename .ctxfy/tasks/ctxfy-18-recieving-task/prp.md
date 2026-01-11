🏷️ PRP METADATA
PRP ID: ctxfy-18-recieving-task
Type: server-tool-implementation
Domain: backend-development
Technology Stack: Python/FastMCP/Markdown Processing
Complexity Level: Medium

🎯 BUSINESS CONTEXT LAYER
Business Objectives
- [ ] Implement server-side tool `process_task` to receive and process markdown files containing user stories or tasks
- [ ] Automatically generate unique task IDs using timestamp and content hash for traceability
- [ ] Create organized directory structure `.ctxfy/tasks/{task_id}/` for centralized task management
- [ ] Support both Docker and STDIO execution environments with appropriate workspace detection
- [ ] Return structured response with task metadata for client consumption

SLAs & Performance Requirements
- [ ] Tool processes files up to 10MB in under 2 seconds
- [ ] Task ID generation completes in under 50ms
- [ ] Directory creation and file saving completes in under 100ms
- [ ] API response time under 2 seconds for typical task files

🔧 TECHNICAL TRANSLATION
Architecture Pattern
- [ ] Functional Core & Imperative Shell (FCIS) separation with pure logic in core, I/O in shell
- [ ] Hexagonal Architecture with ports and adapters for file operations
- [ ] Value objects for task metadata with immutable properties

Technology Specifications
- [ ] Python 3.13 with type hints
- [ ] FastMCP for tool registration and orchestration
- [ ] Built-in hashlib for content hashing
- [ ] OS environment detection for workspace configuration

Specification Output
📝 SPECIFICATION OUTPUT
Expected Deliverables
- [ ] `src/shell/adapters/tools/process_task_tool.py` - Implementation of the process_task tool
- [ ] `src/core/use_cases/process_task_use_case.py` - Core business logic for task processing
- [ ] `src/core/models/task_metadata.py` - Immutable value object for task metadata
- [ ] `src/shell/orchestrators/mcp_orchestrator.py` - Registration of the new tool
- [ ] `tests/unit/core/test_process_task_use_case.py` - Unit tests for core logic
- [ ] `tests/integration/shell/test_process_task_tool.py` - Integration tests for the tool

Code Structure Guidelines
- [ ] Core functions in `src/core/` must be pure with no I/O operations
- [ ] Shell functions in `src/shell/` handle file operations and environment detection
- [ ] Use `@dataclass(frozen=True)` for value objects in domain models
- [ ] Port naming follows convention: `*CommandPort`, `*RepositoryPort`, etc.

✅ VALIDATION FRAMEWORK
Testing Strategy
- [ ] Unit tests target Functional Core only (≥70% of test suite)
- [ ] Integration tests validate Core + Shell adapter combinations (≤25% of test suite)
- [ ] End-to-end tests validate complete workflow (≤5% of test suite)
- [ ] Test `test_process_task_creates_directory_structure()` with real file operations
- [ ] Test `test_task_id_generation_consistency()` with identical content at different times

Quality Gates
- [ ] Core functions pass in <100ms each
- [ ] Ruff formatting compliance with line-length=88
- [ ] Mypy strict type checking enabled for core packages
- [ ] Code coverage ≥80% for core packages
- [ ] No architecture violations (core depending on shell)

✨ AI CONTEXT ADAPTATION
Model Compatibility Notes
- [ ] Claude 3: Excellent for complex file processing and directory structure management
- [ ] GPT-4: Good for understanding FastMCP tool registration patterns
- [ ] Include specific file paths and class names to prevent context drift

📊 SUCCESS METRICS
Performance Metrics
- [ ] Tool response time: < 2 seconds for files up to 10MB
- [ ] Task ID generation: < 50ms
- [ ] Directory creation: < 100ms
- [ ] Memory usage: < 50MB for processing 10MB file

Quality & Reliability Metrics
- [ ] Ruff formatting compliance: 100%
- [ ] Mypy type checking: 100% success rate
- [ ] Unit test coverage: ≥80% for core packages
- [ ] Architecture compliance: 100% (no core depending on shell)

📋 ARCHITECTURE COMPLIANCE CHECKLIST
- [ ] FCIS patterns properly implemented in src/core/use_cases/process_task_use_case.py
- [ ] Port naming conventions followed in src/core/ports/task_ports.py
- [ ] Test distribution requirements met in tests/unit/core/test_process_task_use_case.py
- [ ] Value objects are immutable in src/core/models/task_metadata.py
- [ ] Core functions are pure in src/core/use_cases/process_task_use_case.py
- [ ] Token budget under 1000 tokens