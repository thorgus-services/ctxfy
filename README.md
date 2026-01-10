# Ctxfy - MCP Server for Context Engineering 🧠⚡

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-username/ctxfy)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typed: Mypy](https://img.shields.io/badge/mypy-typed-blue.svg)](https://github.com/python/mypy)

**Standardizes and automates developer-AI interaction through the Model Context Protocol (MCP).**

Ctxfy is an enterprise Context Engineering MCP Server that standardizes and automates the interaction between developers and AI agents. Currently focused on technical specification generation from business requirements, with a roadmap to implement the full vision of context engineering. By implementing the Model Context Protocol (MCP) specification with STDIO transport, Ctxfy transforms ad-hoc prompts into **repeatable, auditable, and scalable** software development processes.

## 🚀 Current Features

- **Technical Specification Generation**: AI-powered generation of technical specifications from business requirements
- **YAML-based Prompt Configuration**: Flexible prompt templates defined in YAML files
- **MCP Protocol Compliance**: Native integration with LLMs via STDIO transport
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
- **Protocol**: Model Context Protocol (MCP) with STDIO transport

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+** (for development)
- **Docker** (for containerized deployment)
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

### Docker Deployment

Ctxfy can be deployed as a Docker container for consistent environments and easy deployment:

1. **Build the Docker image:**
   ```bash
   docker build -t ctxfy-mcp:latest .
   ```

2. **Run the container with STDIO transport:**
   ```bash
   docker run -i --rm -v "$PWD:/workspace:rw" -e WORKSPACE_DIR=/workspace ctxfy-mcp:latest
   ```

3. **Using Docker Compose:**
   ```bash
   # Set environment variables
   export WORKSPACE_DIR=$(pwd)/workspace

   # Start the service
   docker-compose up ctxfy-mcp
   ```

4. **Development with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

## 🧪 Development Commands

The project uses Tox for development workflows:

- **Run linting**: `tox -e lint`
- **Apply code formatting**: `tox -e format`
- **Run type checking**: `tox -e type`
- **Run unit tests**: `tox -e unit`
- **Run integration tests**: `tox -e integration`
- **Run security checks**: `tox -e security`
- **Run compliance validation**: `tox -e compliance`
- **Run MCP server with STDIO transport**: `tox -e start`
- **Run all checks**: `tox`

### Quick Start

Start the MCP server and integrate with your AI tools:

```bash
# Using Tox (recommended for development)
tox -e start

# Direct execution
python src/app.py

# Using Docker (production-like environment)
docker run -i --rm -v "$PWD:/workspace:rw" -e WORKSPACE_DIR=/workspace ctxfy-mcp:latest
```

The server uses STDIO transport for MCP communication.

## 🛠️ Current Usage

### Main Entrypoint

The primary entrypoint is:
```bash
python src/app.py
```

### Configuration

Set via environment variables:
- `DEBUG`: Enable debug mode (default: False)

## 🌐 MCP Client Integration

The server communicates via STDIO transport, which is the standard for MCP clients like Claude Code, Cursor, and other AI development tools. Both local and containerized deployments are supported:

### Local Deployment
1. **Configure your MCP client** to use the STDIO transport with the Ctxfy server executable.

2. **Start the server** using Tox:
   ```bash
   tox -e start
   ```

3. **Or run directly**:
   ```bash
   python src/app.py
   ```

4. **Use MCP tools** in your AI development environment.

### Containerized Deployment
1. **Build and run the container** with STDIO forwarding:
   ```bash
   docker run -i --rm -v "$PWD:/workspace:rw" -e WORKSPACE_DIR=/workspace ctxfy-mcp:latest
   ```

2. **Configure your MCP client** to use the containerized executable with proper volume mounts for file access.

3. **Use MCP tools** in your AI development environment with containerized server.

### Volume Mounting for File Access
For MCP clients that need to access project files, mount your workspace directory:
```bash
docker run -i --rm -v "$PWD:/workspace:rw" -e WORKSPACE_DIR=/workspace ctxfy-mcp:latest
```

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