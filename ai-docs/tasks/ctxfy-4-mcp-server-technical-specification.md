# TECHNICAL SPECIFICATION: ctxfy MCP Server Base with FastMCP

## 1. Overview

This document provides the complete technical specification for the ctxfy MCP (Model Context Protocol) Server Base implementation using FastMCP 2.0 framework. The implementation follows Hexagonal Architecture and Functional Core & Imperative Shell patterns.

### 1.1 Purpose
- Establish a robust, extensible foundation for MCP services
- Enable prompt-based interactions using FastMCP's `@mcp.prompt` decorator
- Provide a base server that can be extended for various AI/LLM integrations
- Implement structured logging with prompt_id, latency_ms and llm_model for observability

### 1.2 Scope
- MCP server foundation with FastMCP 2.0
- `/mcp` and `/health` endpoints
- Minimal `ctx.sample()` implementation
- Structured logging with required fields
- Basic CI/CD pipeline

## 2. Architecture

### 2.1 Hexagonal Architecture Structure

```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   ├── use_cases/        # Pure functions implementing business rules
│   └── ports/            # Interfaces only (Protocols)
│       └── mcp_ports.py
├── adapters/             # Implementations of core ports
│   ├── mcp_server/       # FastMCP integration
│   ├── logging/          # Structured logging implementation
│   └── llm/              # LLM sampling implementation
└── app/                  # Application composition and configuration
```

### 2.2 Core Components

#### 2.2.1 Core Ports (`src/core/ports/mcp_ports.py`)
- `MCPServerPort`: Primary port for MCP server operations
- `MCPHealthPort`: Secondary port for health check operations

#### 2.2.2 Core Models (`src/core/models/mcp_models.py`)
- `PromptRequest`: Immutable value object for MCP prompt requests
- `PromptResponse`: Immutable value object for MCP prompt responses  
- `HealthStatus`: Immutable value object for health status

#### 2.2.3 Core Use Cases (`src/core/use_cases/mcp_use_cases.py`)
- `process_prompt_request`: Pure function to process prompt requests
- `get_health_status`: Pure function to generate health status

### 2.3 Adapters

#### 2.3.1 FastMCP Server Adapter (`src/infrastructure/mcp_server/fastmcp_adapter.py`)
- Implements MCP server using FastMCP framework
- Registers health check endpoint
- Handles prompt and tool registration

#### 2.3.2 Structured Logger (`src/infrastructure/logging/structured_logger.py`)
- Implements structured JSON logging
- Includes required fields: prompt_id, latency_ms, llm_model
- Logs with consistent format for observability

#### 2.3.3 LLM Adapter (`src/infrastructure/llm/llm_adapter.py`)
- Provides ctx.sample() functionality
- Handles LLM sampling with proper logging

## 3. Implementation Details

### 3.1 Project Dependencies (`pyproject.toml`)
- FastMCP 2.13.0 framework
- Python 3.13+
- Configuration using Poetry

### 3.2 Server Configuration (`fastmcp.json`)
- Server configuration with host, port, CORS settings
- Logging configuration
- LLM settings with default model and timeout

### 3.3 Entry Point (`app/main.py`)
- Initializes FastMCP server
- Sets up health check endpoint at `/health`
- Implements example prompt with ctx.sample functionality
- Starts server on port 8000

### 3.4 Endpoints
- `/mcp`: MCP protocol endpoint (handled automatically by FastMCP)
- `/health`: Health check returning 200 status with server status information

## 4. ctx.sample() Implementation

The minimal ctx.sample() functionality is implemented in the sample prompt:
- Uses FastMCP's `ctx.sample()` for LLM text generation
- Accepts parameters and formats prompts
- Logs all operations with required fields
- Returns structured responses

```python
@server.prompt("ctx.sample.example")
async def sample_prompt(ctx, name: str = "world", topic: str = "general"):
    # Implementation using ctx.sample
    full_prompt = f"Hello {name}! Please provide a brief explanation about {topic}."
    result = await ctx.sample(prompt=full_prompt, model="default")
    return result
```

## 5. Structured Logging

The system implements structured logging with JSON format that includes:
- `prompt_id`: Unique identifier for each prompt request
- `latency_ms`: Processing time in milliseconds
- `llm_model`: Model used for the operation
- Additional fields: timestamp, level, message, module, function, line

## 6. CI/CD Pipeline

GitHub Actions workflow defined in `.github/workflows/ci-cd.yml`:
- Runs on push to main/develop branches and pull requests
- Tests on Python 3.13
- Executes linting, type checking, security scans, and tests
- Uploads coverage reports

## 7. Files Created

### 7.1 Source Code
- `src/core/ports/mcp_ports.py` - Core protocols
- `src/core/models/mcp_models.py` - Immutable value objects
- `src/core/use_cases/mcp_use_cases.py` - Pure business logic functions
- `src/infrastructure/mcp_server/fastmcp_adapter.py` - FastMCP integration adapter
- `src/infrastructure/logging/structured_logger.py` - Structured logging adapter
- `src/infrastructure/llm/llm_adapter.py` - LLM sampling adapter
- `src/interfaces/main.py` - Application entry point

### 7.2 Configuration
- `fastmcp.json` - Server configuration
- `.github/workflows/ci-cd.yml` - CI/CD pipeline

### 7.3 Tests
- `tests/test_server_basic.py` - Basic server functionality tests

## 8. Verification

### 8.1 Health Check
- The `/health` endpoint returns 200 status with server status information
- Includes uptime, timestamp, and health checks

### 8.2 MCP Protocol
- The `/mcp` endpoint is handled by FastMCP framework
- Follows MCP protocol specifications

### 8.3 ctx.sample() Functionality
- Example prompt demonstrates ctx.sample() usage
- Properly integrates with FastMCP context

### 8.4 Logging
- All operations include required fields: prompt_id, latency_ms, llm_model
- JSON structured format for observability

## 9. Compliance with Rules

This implementation follows all specified architectural rules:
- ✅ Hexagonal Architecture with proper boundaries
- ✅ Functional Core & Imperative Shell patterns
- ✅ Immutable value objects with @dataclass(frozen=True)
- ✅ Protocol-based ports for dependency inversion
- ✅ Structured logging with required fields
- ✅ TDD principles (with test coverage)
- ✅ Orchestrator pattern where applicable

## 10. Expected Outcomes

Upon successful deployment and execution:
1. Server responds to `/health` endpoint with 200 status
2. Server handles MCP protocol requests via `/mcp` endpoint
3. ctx.sample() functionality operates as expected
4. All logs include prompt_id, latency_ms, and llm_model
5. CI/CD pipeline executes successfully
6. Server follows Hexagonal Architecture principles