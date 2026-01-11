## 📂 PROJECT STRUCTURE RELEVANT TO task processing and file operations
src/
├── core/                    # Functional core (pure logic)
│   ├── use_cases/           # Business logic for task processing
│   ├── ports/              # Interfaces for task/file operations  
│   └── utils/              # Path utilities for file handling
└── shell/                  # Imperative shell (I/O operations)
    ├── adapters/
    │   ├── tools/          # Tool implementations (e.g., process_task)
    │   └── prompt_loaders/ # Dynamic prompt loading
    ├── orchestrators/      # Component initialization
    └── registry/          # Tool/prompt registration system

## 🔍 EXISTING IMPLEMENTATIONS
- **Concrete file path**: `src/shell/adapters/tools/specification_generation_tool.py`
- **Registration pattern**: `tool_registry.register_tool("generate_specification", tool)` in `MCPOrchestrator._setup_tools()`
- **Configuration example**: `resources/prompts.yaml` defines dynamic prompts with parameters and templates

## ⚙️ CONFIGURATION PATHWAYS
- **Tool Registration**: `src/shell/registry/tool_registry.py` - registers tools with FastMCP using decorator pattern
- **Dynamic Prompts**: `src/shell/registry/dynamic_prompt_registry.py` - loads YAML prompts dynamically without code changes
- **Workspace Detection**: `os.environ.get('WORKSPACE_DIR', '/workspace')` for Docker vs STDIO environment detection

## 🛡️ CRITICAL RULES & VALIDATION
✅ python-toolchain-standards.md compliance: Following Poetry dependency management and type checking standards
✅ functional-code-imperative-shell.md compliance: Separating pure logic (core) from I/O operations (shell)
✅ Token limit compliance: 500/500