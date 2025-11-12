# Ctxfy - MCP Server for Context Engineering 🧠⚡

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-username/ctxfy)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typed: Mypy](https://img.shields.io/badge/mypy-typed-blue.svg)](https://github.com/python/mypy)

**Standardizes and automates developer-AI interaction through the Model Context Protocol (MCP).**

Ctxfy is an enterprise Context Engineering MCP Server that standardizes and automates the interaction between developers and AI agents. By implementing the Model Context Protocol (MCP) specification, Ctxfy transforms ad-hoc prompts into **repeatable, auditable, and scalable** software development processes.

## 🚀 Features

- **Standardized Context Stacks**: 5 structured layers ensuring consistent AI interactions
- **PRP Automation**: Automated generation of Product Requirements Prompts 
- **MCP Protocol Compliance**: Native integration with LLMs via HTTP transport
- **Dynamic RAG Integration**: Real-time updated context with knowledge retrieval
- **Enterprise Security**: Security controls and audit trails

## 🏗️ Architecture

Ctxfy follows a **Functional Core, Imperative Shell** architecture with MCP Protocol compliance:

- **Functional Core**: Pure context transformation logic with no side effects
- **Imperative Shell**: Handles MCP communication and I/O operations
- **Hexagonal Architecture**: Ports and adapters pattern for clean separation
- **Immutable Models**: All data classes are frozen for predictable state

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Framework**: FastMCP for Model Context Protocol implementation
- **Architecture**: Hexagonal with Functional Core, Imperative Shell
- **Tools**: Poetry (dependencies), Ruff (formatting), MyPy (type checking)
- **Protocol**: Model Context Protocol (MCP) with HTTP transport

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**
- **Poetry** (dependency manager)
- **Git**

### Installation

1. **Clone and install:**
   ```bash
   git clone https://github.com/your-username/ctxfy.git
   cd ctxfy
   poetry install
   poetry shell
   ```

2. **Run the server:**
   ```bash
   python -m src.app.main
   ```

### Quick Start

Start the MCP server and integrate with your AI tools:

```bash
# Direct execution
python -m src.app.main

# Or with Poetry
poetry run python -m src.app.main
```

**Alternative: Using Docker**

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -t ctxfy .
docker run -p 8000:8000 ctxfy
```

The server runs on `http://127.0.0.1:8000/mcp` by default.

## 🛠️ Usage

### Main Entrypoint

The primary entrypoint is:
```bash
python -m src.app.main
```

### MCP Integration

The server provides the `generate_context_stack` tool via MCP protocol:
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

Set via environment variables:
- `DEBUG`: Enable debug mode (default: False)
- `SERVER_HOST`: Host address (default: 127.0.0.1)
- `SERVER_PORT`: Port (default: 8000)
- `MCP_TRANSPORT`: Transport protocol (default: http)

## 🔐 Authentication

The Ctxfy MCP Server requires API key authentication for all requests. You can use the following methods to manage API keys:

### Creating API Keys

The server provides the `create-api-key` tool via MCP protocol:
```json
{
  "name": "create-api-key",
  "arguments": {
    "user_id": "your-user-id",
    "scope": "read",  // or "write", "admin"
    "ttl_hours": 24   // optional, time-to-live in hours
  }
}
```

This will return a new API key that you can use for authentication.

### Using API Keys

Include your API key in requests using one of these header formats:
- `Authorization: Bearer <api-key>`
- `X-API-Key: <api-key>`
- `API-Key: <api-key>`

### Default Behavior

If no authentication is provided, the server will reject the request unless configured otherwise.

## 🌐 Qwen Code Integration

1. **Install Qwen Code extension** in VS Code.

2. **Create configuration** (`qwen-config.json`):
   ```json
   {
     "tools": {
       "ctxfy-server": {
         "command": ["poetry", "run", "python", "-m", "src.app.main"],
         "env": {
           "DEBUG": "true"
         },
         "cwd": ".",
         "timeout": 30
       }
     }
   }
   ```

3. **Start the server**:
   ```bash
   poetry run python -m src.app.main
   ```

4. **Use MCP tools** in Qwen Code interface.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following architectural principles
4. Write tests using TDD
5. Run tests: `poetry run pytest`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

Report issues on our [GitHub Issues](https://github.com/your-username/ctxfy/issues) page. Include Python version, OS, MCP client version, and steps to reproduce.