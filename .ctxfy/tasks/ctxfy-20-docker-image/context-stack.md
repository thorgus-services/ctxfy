### System Context Layer (Static - Project Rules)
This project follows the Functional Core, Imperative Shell (FCIS) architecture with strict dependency boundaries. The toolchain uses Poetry for dependency management, Ruff for linting, MyPy for type checking, and Tox for task automation. The codebase implements immutable value objects in the core with imperative shell handling side effects. All development must comply with these architectural and toolchain standards.

### Domain Context Layer (Hybrid)
**Static Project Rules:**
Python toolchain standards require Poetry-managed dependencies with specific version constraints, Ruff formatting with 88-character line limits, MyPy strict type checking, and Tox-automated testing. Package architecture enforces inward-flowing dependencies (shell → core) with hexagonal architecture adapters in `src/shell/adapters/`. Security scanning and CI validation happen through Tox automation.

**Dynamic Project Context:**
The project has an MCP server entry point at `src/app.py` with `run_stdio_server()` function for STDIO transport. Configuration uses pydantic-settings with `.env` file support for `PROMPTS_FILE_PATH` variable. The project structure includes `resources/` for config files and uses Tox for start environment automation.

**Active Skills:**
No specific skills loaded due to fallback strategy (proceed_without_skills).

#### Task Context Layer (Dynamic)
**Task Description:** Create a Docker image for the MCP Server that runs consistently across environments with dependency isolation and standardized client integration. The image should accept environment variable configuration, support file volume mounting, handle STDIO connections, include all necessary dependencies, and securely manage sensitive variables.

**Success Criteria:**
- Docker image available in configured registry
- Container accepts environment variable configuration for ports, tokens, timeouts
- Container mounts host volumes for file URI access
- Container supports STDIO connections per specification
- Image includes all runtime dependencies
- Secure handling of sensitive environment variables
- Image size ≤500MB with startup time <5 seconds
- 100% functionality tests pass inside container
- Documentation includes examples for 3+ MCP clients
- Automatic rebuilds on main branch merges

**Integration Points:**
- Entry point: `src/app.py` with STDIO transport
- Configuration: pydantic-settings via `.env` file
- Dependencies: Poetry-managed in `pyproject.toml`
- Build automation: Tox validation tasks
- Volume mounting: File access via `file://` URIs