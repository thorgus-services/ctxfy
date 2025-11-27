# Ctxfy - MCP Server for Context Engineering 🧠⚡

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-username/ctxfy)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typed: Mypy](https://img.shields.io/badge/mypy-typed-blue.svg)](https://github.com/python/mypy)

**Standardizes and automates developer-AI interaction through the Model Context Protocol (MCP).**

Ctxfy is an enterprise Context Engineering MCP Server that standardizes and automates the interaction between developers and AI agents. Currently focused on technical specification generation from business requirements, with a roadmap to implement the full vision of context engineering. By implementing the Model Context Protocol (MCP) specification, Ctxfy transforms ad-hoc prompts into **repeatable, auditable, and scalable** software development processes.

## 🚀 Current Features

- **Technical Specification Generation**: AI-powered generation of technical specifications from business requirements
- **YAML-based Prompt Configuration**: Flexible prompt templates defined in YAML files
- **MCP Protocol Compliance**: Native integration with LLMs via HTTP transport
- **Dynamic Prompt Registration**: Automatic registration of prompts from YAML configuration
- **Functional Core/Imperative Shell Architecture**: Clean separation of business logic and side effects

## 🚀 Future Vision

- **Standardized Context Stacks**: 5 structured layers ensuring consistent AI interactions
- **PRP Automation**: Automated generation of Product Requirements Prompts
- **Dynamic RAG Integration**: Real-time updated context with knowledge retrieval
- **Enterprise Security**: Security controls and audit trails

## 🏗️ Architecture

Ctxfy follows a **Functional Core, Imperative Shell** architecture with MCP Protocol compliance:

- **Functional Core**: Pure specification generation logic with no side effects
- **Imperative Shell**: Handles MCP communication, YAML loading, and I/O operations
- **Ports and Adapters**: Protocol-based interfaces for clean separation of concerns
- **Immutable Models**: All data classes are frozen for predictable state

The architecture is visualized in the [C4 Component Diagram](./docs/ctxfy_architecture_diagram.md).

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Framework**: FastMCP for Model Context Protocol implementation
- **Architecture**: Functional Core/Imperative Shell (FCIS) with Ports and Adapters
- **Tools**: Poetry (dependencies), Ruff (formatting), MyPy (type checking), Tox (testing)
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

2. **Configure environment variables:**
   Copy the example environment file and customize it for your needs:
   ```bash
   cp example.env .env
   # Edit .env with your specific configuration
   ```

   The following environment variables are available:
   - `PROMPTS_FILE_PATH`: Path to the prompts configuration file (default: `resources/prompts.yaml`)
   - `DEBUG`: Enable debug mode (set to 1 to enable, default: 0)
   - `SERVER_HOST`: Host address for the server (default: `127.0.0.1`)
   - `SERVER_PORT`: Port number for the server (default: `8000`)
   - `MCP_TRANSPORT`: Transport protocol for MCP (default: `http`)
   - `API_KEY`: Optional API key for authentication (if required)

## 🧪 Development Commands

The project uses Tox for development workflows:

- **Run linting**: `tox -e lint`
- **Apply code formatting**: `tox -e format`
- **Run type checking**: `tox -e type`
- **Run unit tests**: `tox -e unit`
- **Run integration tests**: `tox -e integration`
- **Run security checks**: `tox -e security`
- **Run compliance validation**: `tox -e compliance`
- **Run development server**: `tox -e serve`
- **Run all checks**: `tox`

### Quick Start

Start the MCP server and integrate with your AI tools:

```bash
# Using Tox (recommended for development)
tox -e serve

# Direct execution
python -m src.app
```

The server runs on `http://127.0.0.1:8000` by default.

## 🛠️ Current Usage

### Main Entrypoint

The primary entrypoint is:
```bash
python -m src.app
```

### MCP Integration

The server currently provides the `generate_specification` tool via MCP protocol:
```json
{
  "name": "generate_specification",
  "description": "Generates technical specifications from business requirements",
  "arguments": {
    "business_requirements": "Describe the feature or system to be specified"
  }
}
```

The `specification_save_instruction` prompt is also available for generating comprehensive technical specifications.

### Configuration

Set via environment variables:
- `DEBUG`: Enable debug mode (default: False)
- `SERVER_HOST`: Host address (default: 127.0.0.1)
- `SERVER_PORT`: Port (default: 8000)
- `MCP_TRANSPORT`: Transport protocol (default: http)

## 🌐 Qwen Code Integration

1. **Install Qwen Code extension** in VS Code.

2. **Copy the example configuration** from `examples/qwen-config.json` to your workspace or user settings:
   ```json
   {
     "mcpServers": {
       "context-engineering": {
         "httpUrl": "http://127.0.0.1:8000/mcp",  // MCP protocol endpoint
         "headers": {
           "Content-Type": "application/json",
           "Authorization": "Bearer YOUR_API_KEY_HERE"  // Replace with your actual API key
         },
         "timeout": 30000,
         "trust": false
       }
     }
   }
   ```

3. **Start the server** using Tox:
   ```bash
   tox -e serve
   ```

4. **Use MCP tools** in Qwen Code interface.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following FCIS architectural principles
4. Write tests using TDD
5. Run quality checks: `tox`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

Report issues on our [GitHub Issues](https://github.com/your-username/ctxfy/issues) page. Include Python version, OS, MCP client version, and steps to reproduce.