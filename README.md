# Ctxfy - MCP Server for Context Engineering 🧠⚡

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-username/ctxfy)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typed: Mypy](https://img.shields.io/badge/mypy-typed-blue.svg)](https://github.com/python/mypy)

**Standardizes and automates developer-AI interaction through the Model Context Protocol (MCP).**

Ctxfy standardizes and automates interaction between developers and AI agents. It generates technical specifications from business requirements using the Model Context Protocol (MCP) with STDIO transport, transforming ad-hoc prompts into **repeatable, auditable, and scalable** processes.

## 🚀 Features

- **Technical Specification Generation**: AI-powered generation from business requirements
- **YAML-based Prompt Configuration**: Flexible templates in YAML files
- **MCP Protocol Compliance**: Native integration with LLMs via STDIO transport
- **Dynamic Prompt Registration**: Automatic registration from YAML configuration
- **Functional Architecture**: Clean separation of business logic and side effects

## 🏗️ Architecture

**Functional Core, Imperative Shell** architecture with MCP Protocol compliance:

- **Functional Core**: Pure specification generation logic (no side effects)
- **Imperative Shell**: Handles MCP communication, YAML loading, and I/O operations
- **Ports and Adapters**: Protocol-based interfaces for clean separation of concerns

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Framework**: FastMCP for Model Context Protocol
- **Tools**: Poetry, Ruff, MyPy, Tox
- **Protocol**: MCP with STDIO transport

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**, **Docker**, **Poetry**, **Git**

### Installation

1. Clone and install:
   ```bash
   git clone https://github.com/your-username/ctxfy.git
   cd ctxfy
   poetry install
   poetry shell
   ```

2. Configure environment variables:
   ```bash
   cp example.env .env
   # Edit .env with your configuration
   ```

   Available variables:
   - `PROMPTS_FILE_PATH`: Path to prompts config (default: `resources/prompts.yaml`)
   - `DEBUG`: Enable debug mode (default: 0)

### Quick Start

Start the MCP server:

```bash
# Using Tox (recommended)
tox -e start

# Direct execution
python src/app.py
```

Server uses STDIO transport for MCP communication.

### Docker Deployment

Deploy as a container:

1. Build the image:
   ```bash
   docker build -t ctxfy-mcp:latest .
   ```

2. Run with STDIO transport:
   ```bash
   docker run -i --rm -v "$PWD:/workspace:rw" ctxfy-mcp:latest
   ```

3. Using Docker Compose:
   ```bash
   docker-compose up ctxfy-mcp
   ```

## 🧪 Development Commands

Project uses Tox for workflows:

- **Linting**: `tox -e lint`
- **Formatting**: `tox -e format`
- **Type checking**: `tox -e type`
- **Unit tests**: `tox -e unit`
- **Integration tests**: `tox -e integration`
- **Security checks**: `tox -e security`
- **Compliance validation**: `tox -e compliance`
- **Start server**: `tox -e start`
- **All checks**: `tox`

## 🌐 MCP Client Integration

Server communicates via STDIO transport (standard for MCP clients like Claude Code, Cursor). Configure your MCP client to use STDIO transport with Ctxfy server.

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Follow FCIS principles
4. Write tests with TDD
5. Run quality checks: `tox`
6. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🐛 Issues

Report issues on [GitHub Issues](https://github.com/your-username/ctxfy/issues). Include Python version, OS, MCP client version, and reproduction steps.