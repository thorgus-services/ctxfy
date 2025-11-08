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
| **MCP Transport Layer** | FastMCP (Python), Streamable HTTP | Connection management, protocol encoding/decoding |
| **Context Orchestration** | Pydantic, LangChain Core | Context stack assembly, validation, compression |
| **PRP Engine** | Jinja2, YAML, JSON Schema | PRP template execution, resource injection |
| **Dynamic Context Sources** | LlamaIndex, ChromaDB, FastAPI | RAG integration, knowledge retrieval, caching |
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
└── cli.py               # Composition root for dependency injection
```

### MCP Protocol Implementation
- **Transport**: STDIO (PoC phase) → Streamable HTTP (production)
- **Protocol Version**: 2025-06-18 (latest stable)
- **Capabilities**: Tools, Resources, Prompts, Elicitation
- **Lifecycle**: Full JSON-RPC handshake with capability negotiation

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Toolchain**: Poetry (dependency management), Ruff (formatting), MyPy (type checking)
- **Architecture**: Functional Core, Imperative Shell with Hexagonal Architecture
- **MCP Protocol**: Model Context Protocol implementation with FastMCP
- **Context Processing**: Pydantic, LangChain Core for context orchestration
- **RAG Integration**: LlamaIndex, ChromaDB for dynamic knowledge retrieval
- **Testing**: Pytest with TDD (Test Driven Development) practices
- **Observability**: OpenTelemetry, Prometheus for audit and monitoring

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- Poetry (dependency manager)
- Git
- Qwen Code IDE extension (for MCP integration)

### Installation

```bash
poetry add ctxfy
```

### Quick Start

```bash
# Start the MCP server
ctxfy server --port 8000

# Or integrate with Qwen Code via STDIO transport
ctxfy mcp --stdio
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
ctxfy server --port 8000
```

### MCP Integration (STDIO Transport)
```bash
ctxfy mcp --stdio  # For integration with Qwen Code or other MCP clients
```

### Context Operations
```bash
ctxfy context generate --story "User authentication feature"  # Generate context stack from requirements
ctxfy prp create --context-stack path/to/context.json       # Create PRP from context
ctxfy validate --context-stack path/to/context.json         # Validate context quality
```

### Additional Commands
```bash
ctxfy --help          # Show all available commands
ctxfy config          # Manage server configuration
ctxfy context         # Work with context stacks
ctxfy server --help   # Show server-specific options
```

## 🧪 Testing Strategy

Our testing approach follows TDD (Test-Driven Development) with MCP protocol compliance focus:
- **Unit Tests** (≥70% of suite): Target Functional Core context transformation functions, no I/O
- **MCP Integration Tests** (≤25%): Test MCP protocol handshake, tool execution, and resource management
- **End-to-End Tests** (≤5%): Full MCP client-server interaction validation

MCP protocol tests validate full JSON-RPC communication:
```python
def test_mcp_context_generation_tool():
    # Simulate MCP client requesting context generation
    request = {
        "method": "tools/call",
        "params": {
            "name": "generate_context_stack",
            "arguments": {"story": "User authentication feature"}
        }
    }
    response = mcp_server.handle_request(request)
    assert response["result"]["context_stack"] is not None
```

## 🤝 Contributing

We welcome contributions from the community! Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our architectural principles
4. Write tests for your changes using TDD
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
- **Proper Port Naming**: Follow the naming conventions (MCPCommandPort, MCPQueryPort, etc.)
- **Security First**: All context sources must be validated before processing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you encounter any issues, please open an issue on our [GitHub Issues](https://github.com/your-username/ctxfy/issues) page. When reporting MCP-related issues, please include:

- Python version
- Operating system
- MCP client version (if applicable)
- Steps to reproduce the issue
- Expected vs actual behavior
- Any relevant logs or error messages
- MCP protocol compliance issues (if any)

## 🙏 Acknowledgments

- Thanks to the open-source community for inspiration and support
- Special thanks to contributors and maintainers
- Built with ❤️ for developers who value standardized and auditable AI interactions
- Inspired by Context Engineering principles by A B Vijay Kumar