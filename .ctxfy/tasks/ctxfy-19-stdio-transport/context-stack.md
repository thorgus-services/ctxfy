### System Context Layer (Static - Project Rules)

**Persona**: MCP Server Developer implementing STDIO transport
**Capabilities**: Access to FastMCP library (v2.13.0), functional core with imperative shell architecture, STDIO transport configuration
**Constraints**: Must follow FCIS pattern, maintain 80%+ test coverage, preserve MCP specification compatibility

### Domain Context Layer (Hybrid)

**Static Project Rules:**
- Package architecture: Functional Core (src/core/) + Imperative Shell (src/shell/)
- Transport logic must stay in shell layer (src/shell/adapters/, src/shell/orchestrators/)
- Python toolchain: FastMCP v2.13.0+, pydantic v2.12+, strict mypy typing
- Core functions remain pure (no I/O), shell handles side effects and transport

**Dynamic Project Context:**
- Current HTTP transport in `src/app.py` using `mcp_server.http_app()`
- Registration flow: `create_mcp_server()` → `MCPOrchestrator(mcp)` → `tool_registry.register_all_to_mcp()`
- FastMCP provides `run()` method for STDIO transport
- Existing MCP orchestrator in `src/shell/orchestrators/mcp_orchestrator.py`

**Active Skills:**
- No specific skills loaded (fallback strategy: proceed_without_skills)

### Task Context Layer (Dynamic)

**Task Description**: Change MCP Server communication transport from HTTP to STDIO to enable `ctx.read_resource(task_file_uri)` functionality with file system URIs and improve client integration efficiency.

**Success Criteria**:
- MCP Server uses STDIO as primary transport instead of HTTP
- `ctx.read_resource(task_file_uri)` works correctly with `file://` and `resource://` URIs
- All registered resources/tools continue functioning after transport change
- Server maintains MCP specification compatibility with clients (Claude Code, Cursor, Trae, etc.)

**Integration Points**:
- Modify `src/app.py` to use FastMCP's STDIO transport via `run()` method
- Update `MCPOrchestrator` registration flow to work with STDIO transport
- Preserve existing tool registration mechanism through `tool_registry.register_all_to_mcp()`