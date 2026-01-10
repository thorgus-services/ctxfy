### System Context Layer (Static - Project Rules)

**Persona:** Context Engineering System following Functional Core & Imperative Shell (FCIS) architecture
**Capabilities:** Process markdown task files via MCP server, generate unique task IDs, register tools and prompts
**Constraints:** 
- Core functions must be pure (no I/O, mutation, time/random)
- Value objects must be immutable (@dataclass(frozen=True))
- Dependencies flow inward: shell → core only
- Token budget: <800 tokens total

### Domain Context Layer (Hybrid)

**Static Project Rules:**
- FCIS: Core=pure logic, Shell=side effects coordination
- Value Objects: Immutable with @dataclass(frozen=True)
- Architecture: Core(models/use_cases/ports/workflows) → Shell(adapters/orchestrators)
- Python standards: Poetry, Ruff, MyPy, Pytest with strict typing

**Dynamic Project Context:**
- Task processing via `process_task` tool with URI handling
- Context engineering setup through `setup_context_engineering` prompt
- MCP server integration with FastMCP framework
- File structure on client side: .ctxfy/{task_id_str}/ for task isolation

**Active Skills:**
- markdown-processing (score: 90) - Core capability for processing markdown files

### Task Context Layer (Dynamic)

**Task Description:** Implement `process_task` tool to read markdown files from URI, generate unique task_id, and return structured data. Create `setup_context_engineering` prompt with LLM instructions for environment setup.

**Success Criteria:** 
- Tool processes files <10MB in <2sec with proper error handling
- Unique task_id format: task_{timestamp}_{hash_short}
- Prompt guides LLM to create .ctxfy/{task_id_str}/ directory structure
- MCP integration with URI validation and resource reading

**Integration Points:** 
- FastMCP server registration
- ctx.read_resource() for URI handling
- ToolRegistry for process_task registration