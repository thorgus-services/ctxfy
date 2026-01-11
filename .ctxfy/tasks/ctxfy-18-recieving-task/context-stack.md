### System Context Layer (Static - Project Rules)

**Persona:** Context Engineering Agent specializing in task reception and processing workflows
**Capabilities:** Process markdown files containing user stories/tasks, generate unique task IDs, create directory structures, manage workspace organization
**Constraints:** Follow functional core & imperative shell pattern, maintain 800-token budget, use Poetry for dependency management, implement proper error handling

### Domain Context Layer (Hybrid)

**Static Project Rules:**
- Functional Core & Imperative Shell: Core logic in `src/core/use_cases/`, I/O operations in `src/shell/adapters/tools/`
- Python Toolchain: Use Poetry for dependencies, Ruff for linting, MyPy for type checking
- File operations must be in shell layer with proper error handling and validation
- Core functions must be pure (no I/O, no mutation of inputs, no time/random)

**Dynamic Project Context:**
- Concrete file path: `src/shell/adapters/tools/specification_generation_tool.py` as reference implementation
- Registration pattern: `tool_registry.register_tool("generate_specification", tool)` in `MCPOrchestrator._setup_tools()`
- Workspace detection: `os.environ.get('WORKSPACE_DIR', '/workspace')` for Docker vs STDIO environment detection
- Tool registration system in `src/shell/registry/tool_registry.py` using decorator pattern

**Active Skills:**
- markdown-processing (score: 85) - Directly relevant for processing markdown files containing user stories or tasks

### Task Context Layer (Dynamic)

- Task description: Receiving and processing markdown files containing user stories or tasks, organizing directory structures, and initiating automated Context Engineering workflows
- Success criteria: Server receives markdown file path, generates unique task ID, creates directory structure `.ctxfy/tasks/{task_id_str}/`, saves original file, returns structured response with task details
- Integration points: FastMCP server tool registration, dynamic prompt system, workspace management based on execution environment