## 📂 PROJECT STRUCTURE RELEVANT TO MCP TRANSPORT
src/
├── app.py                 # Current HTTP transport implementation
├── core/                  # Functional Core (business logic)
│   ├── models/
│   ├── ports/
│   ├── use_cases/
│   └── workflows/
└── shell/                 # Imperative Shell (I/O coordination)
    ├── adapters/
    ├── orchestrators/
    │   └── mcp_orchestrator.py
    └── registry/

## 🔍 EXISTING IMPLEMENTATIONS
- **Concrete file path**: `src/app.py` - current HTTP transport using `mcp_server.http_app()`
- **Registration pattern**: `MCPOrchestrator(mcp)` registers tools/prompts via `tool_registry.register_all_to_mcp(mcp)`

## ⚙️ CONFIGURATION PATHWAYS  
- **Transport mechanism**: FastMCP provides `run()` method for STDIO transport
- **Registration flow**: `create_mcp_server()` → `MCPOrchestrator(mcp)` → `tool_registry.register_all_to_mcp()`

## 🛡️ CRITICAL RULES & VALIDATION
✅ package-and-module-architecture.md compliance: Following FCIS pattern with core/shell separation
✅ functional-code-imperative-shell.md compliance: Transport logic stays in shell layer
✅ immutable-value-objects.md compliance: Value objects remain immutable in core
✅ python-toolchain-standards.md compliance: Using FastMCP library properly
✅ Token limit compliance: 500/500