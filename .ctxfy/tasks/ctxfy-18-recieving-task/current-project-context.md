## 📂 PROJECT STRUCTURE RELEVANT TO TASK PROCESSING & MCP SERVER
src/
├── core/                 # Functional Core (pure business logic)
│   ├── models/           # Immutable value objects
│   ├── use_cases/        # Pure functions with business rules
│   ├── ports/            # Interfaces (Protocols)
│   └── utils/            # Pure utility functions
└── shell/                # Imperative Shell (handles MCP, I/O)
    ├── adapters/
    │   └── tools/        # MCP tool implementations
    ├── orchestrators/    # MCP registration & coordination
    └── registry/         # Tool/prompt registration systems

## 🔍 EXISTING IMPLEMENTATIONS
- **Concrete file path:** `src/shell/adapters/tools/specification_generation_tool.py`
- **Registration pattern:** `tool_registry.register_tool("generate_specification", tool)`
- **Configuration example:** `mcp.tool(name="generate_specification", description="...")(tool.execute)`

## ⚙️ CONFIGURATION PATHWAYS  
- **Tool Registration:** `src/shell/orchestrators/mcp_orchestrator.py` registers tools via `ToolRegistry`
- **MCP Integration:** `src/app.py` creates FastMCP server with registered tools and prompts
- **Prompt Registration:** `src/shell/registry/dynamic_prompt_registry.py` handles prompt loading

## 🛡️ CRITICAL RULES & VALIDATION
✅ package-and-module-architecture.md compliance: FCIS architecture maintained
✅ functional-code-imperative-shell.md compliance: Pure core, side-effectful shell
✅ immutable-value-objects.md compliance: Value objects are frozen dataclasses
✅ python-toolchain-standards.md compliance: Poetry, Ruff, MyPy, Pytest standards
✅ testing-strategy.md compliance: TDD with unit/integration tests
✅ Token limit compliance: 500/500