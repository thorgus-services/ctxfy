# Ctxfy 🧠⚡

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-username/ctxfy)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typed: Mypy](https://img.shields.io/badge/mypy-typed-blue.svg)](https://github.com/python/mypy)

**Documentation tools describe what code does. Ctxfy engineers why it should exist and how it evolves.**

Ctxfy is a CLI tool that transforms business requirements into high-quality code through **Context Engineering** - not just generating code, but engineering the context that makes code emerge naturally.

## 🚀 Features

- **Engineered Context, Not Just Prompts**: We create structured context stacks, not just random prompts
- **Full Workspace Awareness**: Complete access to your code, architecture, and existing patterns
- **Quality-First Workflow**: 9 rigorous validation steps before code delivery
- **Zero Cost**: Native integration with Qwen Code using OAuth (2,000 free requests/day)
- **IDE Agnostic**: Works in any terminal, no plugins required

## 🏗️ Architecture

Ctxfy follows a **Functional Core, Imperative Shell** architecture pattern combined with Hexagonal Architecture principles:

### Core Architecture Principles
- **Immutable Value Objects**: All data structures in the functional core are immutable using `@dataclass(frozen=True)`
- **Pure Functions**: Core logic contains no I/O, mutation, or side effects
- **Hexagonal Architecture**: Core depends only on abstract ports, with adapters implementing them
- **Orchestrator Pattern**: Imperative shell coordinates workflow execution without business logic

### Directory Structure
```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models.py         # Immutable value objects and entities
│   ├── use_cases.py      # Pure functions implementing business rules
│   └── ports/            # Interfaces only (Protocols)
│       ├── context_ports.py
│       └── workflow_ports.py
│
├── shell/               # Imperative shell: I/O, error handling, workflow coordination
│   ├── orchestrators/   # Workflow coordinators with no business logic
│   └── adapters/        # Implementations of core ports
│       ├── file_system/
│       ├── api/
│       └── external/
│
└── cli.py               # Composition root for dependency injection
```

### Port Naming Convention
- **Primary (driving) ports**: `*CommandPort`, `*QueryPort` (e.g., `ContextCommandPort`, `TaskQueryPort`)
- **Secondary (driven) ports**: `*GatewayPort`, `*RepositoryPort`, `*PublisherPort` (e.g., `FileSystemRepositoryPort`)

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Toolchain**: Poetry (dependency management), Ruff (formatting), MyPy (type checking)
- **Architecture**: Functional Core, Imperative Shell with Hexagonal Architecture
- **Testing**: Pytest with TDD (Test Driven Development) practices

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- Poetry (dependency manager)
- Git

### Installation

```bash
poetry add ctxfy
```

### Quick Start

```bash
ctxfy init
ctxfy workflow --task "Your first task"
```

### Development Setup

For contributors, set up the development environment:

1. Clone the repository: `git clone https://github.com/your-username/ctxfy.git`
2. Navigate to the project directory: `cd ctxfy`
3. Install dependencies with Poetry: `poetry install`
4. Activate virtual environment: `poetry shell`
5. Run tests: `poetry run pytest`

Alternatively with pip:
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install in development mode: `pip install -e .[dev]`

## 🌟 The Ctxfy Flow (7 Steps)

1. **Analyze** → Breaks complex tasks into manageable subtasks
2. **PRP Base** → Translates business requirements to technical specifications
3. **Context Stack** → Creates complete context stack (system, domain, task)
4. **Validate** → Rigorous validation of context stack
5. **PRP Backend** → Details technical specifications for implementation
6. **Execute** → Implements code with complete workspace context
7. **Code Review** → Automated review based on quality criteria

## 🛠️ Usage

### Initialize a Project
```bash
ctxfy init
```

### Run a Workflow
```bash
ctxfy workflow --task "Implement user authentication"
```

### Additional Commands
```bash
ctxfy --help          # Show all available commands
ctxfy config          # Manage configuration
ctxfy context         # Work with context stacks
```

## 🧪 Testing Strategy

Our testing approach follows TDD (Test-Driven Development) with the following distribution:
- **Unit Tests** (≥70% of suite): Target Functional Core only with pure functions, no mocks
- **Integration Tests** (≤25%): Test Core + Adapter combinations using real/fake adapters
- **End-to-End Tests** (≤5%): Critical path validation in production-like environments

Acceptance tests call primary ports directly, bypassing HTTP/CLI layers:
```python
def test_create_context_with_invalid_requirements_fails():
    port = InMemoryContextCommandPort()
    req = CreateContextRequest(requirements="", files=[])
    with pytest.raises(InvalidRequirementsError):
        port.create_context(req)
```

## 🤝 Contributing

We welcome contributions from the community! Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our architectural principles
4. Write tests for your changes using TDD
5. Run all tests to ensure nothing is broken: `poetry run pytest`
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Architectural Guidelines for Contributions

When contributing code, please ensure compliance with our architectural principles:

- **Functional Core**: All business logic must be pure functions with no side effects
- **Immutable Value Objects**: Use `@dataclass(frozen=True)` for all domain models
- **No Infrastructure Dependencies in Core**: Core must not import infrastructure packages
- **Proper Port Naming**: Follow the naming conventions (CommandPort, QueryPort, etc.)
- **Orchestrator Pattern**: Shell code must coordinate workflows, not contain business logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you encounter any issues, please open an issue on our [GitHub Issues](https://github.com/your-username/ctxfy/issues) page. When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Any relevant logs or error messages

## 🙏 Acknowledgments

- Thanks to the open-source community for inspiration and support
- Special thanks to contributors and maintainers
- Built with ❤️ for developers who value context-driven development