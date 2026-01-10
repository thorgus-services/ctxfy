## 📂 PROJECT STRUCTURE RELEVANT TO DOCKER CONTAINERIZATION
src/ (app.py entrypoint with STDIO transport) → pyproject.toml (Poetry deps) → tox.ini (start env) → resources/ (config files)

## 🔍 EXISTING IMPLEMENTATIONS
No direct Docker implementations found; MCP server entrypoint at src/app.py with run_stdio_server() function for STDIO transport

## ⚙️ CONFIGURATION PATHWAYS  
Environment via pydantic-settings (src/settings.py) → .env file → PROMPTS_FILE_PATH variable; Tox start command in tox.ini [testenv:start] section

## 🛡️ CRITICAL RULES & VALIDATION
✅ python-toolchain-standards.md compliance: Poetry dependency management, Tox automation
✅ Token limit compliance: 500/500