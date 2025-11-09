# Ctxfy - MCP Server for Context Engineering 🧠⚡

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-username/ctxfy)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typed: Mypy](https://img.shields.io/badge/mypy-typed-blue.svg)](https://github.com/python/mypy)

**Standardizes and automates developer-AI interaction through the Model Context Protocol (MCP).**

Ctxfy is an enterprise Context Engineering MCP Server that standardizes and automates the interaction between developers and AI agents. By implementing the Model Context Protocol (MCP) specification, Ctxfy eliminates rework, ambiguity, and AI model variation, transforming ad-hoc prompts into **repeatable, auditable, and scalable** software development processes.

## 🚀 Features

- **Standardized Context Stacks**: 5 structured layers (System, Domain, Task, Interaction, Response Context) ensuring consistent AI interactions
- **PRP Automation**: Automated generation of Product Requirements Prompts as minimum viable packages for features
- **MCP Protocol Compliance**: Native integration with LLMs via STDIO transport following Model Context Protocol specification
- **Dynamic RAG Integration**: Real-time updated context with knowledge retrieval capabilities
- **Enterprise Security**: Security controls with confirmations for critical operations and PII detection
- **Context Versioning**: Full audit trail and governance for all context modifications

## 🏗️ Architecture

Ctxfy implements a **Functional Core, Imperative Shell** architecture with MCP Protocol compliance following Hexagonal Architecture principles:

### Core Design Principles
- **Strangler Fig Pattern**: Incrementally replace ad-hoc prompt engineering with structured context delivery
- **Functional Core, Imperative Shell**: Pure context transformation logic + side-effect management
- **Protocol First**: Compliant MCP implementation with full lifecycle management
- **Zero-Trust Context Handling**: All context sources are validated and sandboxed

### System Components
| Layer | Technologies | Responsibilities |
|-------|--------------|------------------|
| **MCP Transport Layer** | FastMCP (Python), STDIO/Streamable HTTP | Connection management, protocol encoding/decoding |
| **Context Orchestration** | Pydantic, LangChain Core | Context stack assembly, validation, compression |
| **PRP Engine** | Jinja2, YAML, JSON Schema | PRP template execution, resource injection |
| **Dynamic Context Sources** | LlamaIndex, ChromaDB | RAG integration, knowledge retrieval, caching |
| **Audit & Observability** | OpenTelemetry, Prometheus | Context versioning, usage metrics, drift detection |

### Directory Structure
```
src/
├── core/                 # Pure domain: context transformation, PRP generation
│   ├── models.py         # Immutable context value objects and entities
│   ├── use_cases.py      # Pure functions for context operations
│   └── ports/            # MCP protocol interfaces only (Protocols)
│       ├── mcp_ports.py
│       └── context_ports.py
│
├── shell/               # Imperative shell: MCP communication, file I/O
│   ├── orchestrators/   # MCP workflow coordinators with no business logic
│   └── adapters/        # MCP protocol implementations
│       ├── mcp/
│       ├── context_sources/
│       └── external/
│
└── mcp_server.py        # Main MCP server implementation
```

### MCP Protocol Implementation
- **Transport**: STDIO (primary) with Streamable HTTP support
- **Protocol Version**: 2025-06-18 (latest stable)
- **Capabilities**: Tools, Resources, Prompts, Elicitation
- **Lifecycle**: Full JSON-RPC handshake with capability negotiation

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Architecture**: Functional Core, Imperative Shell with Hexagonal Architecture
- **Toolchain**: Poetry (dependency management), Ruff (formatting), MyPy (type checking)
- **MCP Protocol**: Model Context Protocol implementation with FastMCP
- **Context Processing**: Pydantic, LangChain Core for context orchestration
- **RAG Integration**: LlamaIndex, ChromaDB for dynamic knowledge retrieval
- **Testing**: Pytest with TDD (Test Driven Development) practices
- **Observability**: OpenTelemetry, Prometheus for audit and monitoring

## 🏗️ Architecture Principles

This project follows architectural principles defined in [ai-docs/rules](ai-docs/rules/):

### Core Architecture Principles
- **Hexagonal Architecture**: Application core depends only on abstract ports, and adapters implement them
- **Port Naming Convention**:
  - Primary (driving) ports: `*CommandPort`, `*QueryPort` (e.g., `MCPCommandPort`, `ContextQueryPort`)
  - Secondary (driven) ports: `*GatewayPort`, `*RepositoryPort`, `*PublisherPort` (e.g., `ContextRepositoryPort`)

### Functional Core & Imperative Shell
- **Core Functions**: Pure functions with no I/O, small size (≤15 lines; ≤3 parameters), named with clear verb + domain object
- **Shell Functions**: Thin wrappers (≤25 lines) responsible for I/O, error translation, logging, retries
- **Separation**: Core handles business logic, Shell handles side effects

### Immutable Value Objects
- All core data classes are immutable using `@dataclass(frozen=True)`
- Validation occurs in `__post_init__` or dedicated factory methods
- Type-safe structures preferred over primitive types
- Transformation methods return new instances instead of mutation

### Orchestrator Pattern
- Orchestrators contain no business logic, only workflow coordination
- Maximum 4 dependencies per orchestrator to enforce single responsibility
- Stateless orchestrators with explicit state passing as parameters
- Core defines what needs to happen, orchestrators execute how it happens

### Package Architecture
- Dependencies flow inward: interfaces → application → domain
- No circular dependencies between packages

## 🛠️ Toolchain Configuration

This project follows the [Python Toolchain Standards](ai-docs/rules/python-toolchain-standards.md) for consistent, secure, and maintainable code.

### Key Tools:

- **Dependency Management**: [Poetry](https://python-poetry.org/)
- **Code Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checking**: [Mypy](https://mypy.readthedocs.io/)
- **Security Scanning**: [Bandit](https://bandit.readthedocs.io/), [Safety](https://pypi.org/project/safety/)
- **Testing**: [Pytest](https://docs.pytest.org/)
- **Task Automation**: [Tox](https://tox.wiki/)
- **Configuration**: [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

### Configuration Files:

- `pyproject.toml`: Contains Poetry dependencies, Ruff linting rules, Mypy settings, and Bandit configuration.
- `ruff.toml`: Specific Ruff formatting and linting rules.
- `mypy.ini`: Mypy type-checking configuration.
- `pytest.ini`: Pytest settings.
- `tox.ini`: Tox automation configuration.

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- Poetry (dependency manager)
- Git
- Qwen Code IDE extension (for MCP integration)

### Installation

This application is designed to run as an MCP server. For development:

```bash
git clone https://github.com/your-username/ctxfy.git
cd ctxfy
poetry install
poetry shell
```

Then run the server with:
```bash
python -m src.mcp_server
```

### Quick Start

```bash
# Start the MCP server (uses STDIO transport for MCP protocol)
python -m src.mcp_server

# Or using Poetry (recommended for development)
poetry run python -m src.mcp_server

# The server uses STDIO transport by default for MCP protocol communication
# No HTTP endpoints are exposed - the server communicates directly with MCP clients via STDIO
# This is the standard transport mechanism for MCP protocol integration
```

### Development Setup

For contributors, set up the development environment:

1. Clone the repository: `git clone https://github.com/your-username/ctxfy.git`
2. Navigate to the project directory: `cd ctxfy`
3. Install dependencies with Poetry: `poetry install`
4. Activate virtual environment: `poetry shell`
5. Run tests: `poetry run pytest`
6. Start MCP server: `poetry run ctxfy server`

Alternatively with pip:
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install in development mode: `pip install -e .[dev]`

Note: The application runs as an MCP server using `python -m src.mcp_server` rather than a CLI tool with subcommands. 
The server uses FastMCP with STDIO transport to communicate with MCP-enabled clients like Qwen Code.

## 🌟 The Ctxfy Flow (MCP-Powered Context Engineering)

1. **Context Stack Generation** → Creates structured context across 5 layers (System, Domain, Task, Interaction, Response)
2. **PRP Automation** → Generates Product Requirements Prompts as standardized feature packages  
3. **Context Orchestration** → Assembles complete context stack from multiple sources (workspace, RAG, external APIs)
4. **Validation Framework** → Ensures context quality meets minimum fidelity thresholds
5. **MCP Protocol Handshake** → Establishes secure communication with LLM agents via STDIO/HTTP transport
6. **Dynamic Context Injection** → Delivers real-time updated context during AI interactions
7. **Audit & Compliance** → Logs all context modifications for governance and security

## 🛠️ Usage

### Start MCP Server
```bash
# Run the MCP server with FastMCP and STDIO transport
python -m src.mcp_server

# The server will establish STDIO communication with MCP clients
# such as Qwen Code, enabling context stack generation and PRP workflows
```

### MCP Integration
The server follows the Model Context Protocol specification and provides:
- STDIO transport for direct MCP client integration
- Tool discovery and execution via MCP protocol
- Specifically, the `generate_context_stack` tool for context generation

### Context Operations
The server provides the `generate_context_stack` tool that can be called via the MCP protocol:
```json
{
  "name": "generate_context_stack",
  "arguments": {
    "feature_description": "User authentication feature",
    "target_technologies": ["Python", "MCP"],
    "custom_rules": []
  }
}
```

### Configuration
The server can be configured via environment variables:
- `DEBUG`: Enable debug mode (default: False)
- STDIO transport is used by default for MCP protocol communication

## 🧪 Testing Strategy

Our testing approach follows TDD (Test-Driven Development) with MCP protocol compliance focus:
- **Unit Tests** (≥70% of suite): Target Functional Core context transformation functions, no I/O
- **MCP Integration Tests** (≤25%): Test MCP protocol handshake, tool execution, and resource management
- **End-to-End Tests** (≤5%): Full MCP client-server interaction validation

MCP protocol tests validate full STDIO JSON-RPC communication:
```python
def test_mcp_context_generation_tool():
    # Simulate MCP client requesting context generation
    # The server handles STDIO-based MCP protocol communication
    # FastMCP handles the JSON-RPC message format automatically
    response = mcp_server.handle_request(request)
    assert response["result"]["context_stack"] is not None
```

## 🤝 Contributing

We welcome contributions from the community! Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our architectural principles
4. Write tests for your changes using TDD (≥70% unit tests targeting Functional Core)
5. Run all tests to ensure MCP protocol compliance: `poetry run pytest`
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Architectural Guidelines for Contributions

When contributing code, please ensure compliance with our architectural principles:

- **Functional Core**: All context transformation logic must be pure functions with no side effects
- **MCP Protocol Compliance**: All MCP interactions must follow the Model Context Protocol specification
- **Immutable Value Objects**: Use `@dataclass(frozen=True)` for all context models
- **No Infrastructure Dependencies in Core**: Core must not import infrastructure packages
- **Proper Port Naming**: Follow the naming conventions (CommandPort, QueryPort, GatewayPort, RepositoryPort)
- **Security First**: All context sources must be validated before processing
- **Orchestrator Pattern**: Maximum 4 dependencies per orchestrator, no business logic in shell

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you encounter any issues, please open an issue on our [GitHub Issues](https://github.com/your-username/ctxfy/issues) page. When reporting issues, please include:

- Python version
- Operating system
- MCP client version (if applicable, e.g., Qwen Code)
- Steps to reproduce the issue
- Expected vs actual behavior
- Any relevant logs or error messages
- MCP protocol compliance issues (if any)

## 🙏 Acknowledgments

- Thanks to the open-source community for inspiration and support
- Special thanks to contributors and maintainers
- Built with ❤️ for developers who value standardized and auditable AI interactions
- Inspired by Context Engineering principles by A B Vijay Kumar