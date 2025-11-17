# Tool vs Prompt Evaluation Criteria

## Purpose
Define clear, actionable criteria for determining whether functionality should be implemented as an MCP tool or an MCP prompt in the context of the FastMCP framework and functional core architecture.

## Definitions

### MCP Tools
- Execute server-side operations with side effects
- Perform actions that change system state or interact with external systems
- Return structured results of operations performed
- Follow the Imperative Shell pattern for coordination
- Examples: Create API keys, manage directories, execute database operations

### MCP Prompts
- Provide parameterized, reusable prompt templates
- Generate text or structured content using LLMs
- Follow the template-substitution pattern with variable injection
- Return LLM-generated content based on template + variables
- Examples: Code generation templates, documentation templates, analysis prompts

## Decision Matrix

| Factor | Choose Tool | Choose Prompt |
|--------|-------------|---------------|
| **Primary Function** | Perform an operation/action | Generate text/content with LLM |
| **Side Effects** | Modifies system state, external calls | No system state changes |
| **Return Value** | Results of operation performed | LLM-generated content |
| **Architecture Layer** | Imperative Shell (orchestration) | Imperative Shell (LLM interaction) |
| **Core Integration** | Calls Command Ports for operations | Calls LLM Ports for generation |

## Detailed Criteria

### Use MCP Tools When:
- **System Operations**: Functionality performs system operations (file I/O, database changes, network requests)
- **State Modification**: Functionality needs to modify system state or external resources
- **Multiple Operations**: Functionality orchestrates multiple steps or services
- **Security Context**: Functionality requires authentication, authorization, or audit logging
- **Transaction Boundaries**: Functionality represents a logical transaction boundary
- **Service Orchestration**: Functionality coordinates between multiple services or ports

**Examples of Tool Use Cases:**
```python
# Directory creation - modifies filesystem state
@tool(name="create-ctxfy-directories")
async def create_ctxfy_directories(base_path: str, subdirectories: list[str]) -> Dict[str, Any]:
    # Performs filesystem operations

# API key generation - modifies authentication state
@tool(name="create-api-key")
async def create_api_key(user_id: str, scope: str) -> Dict[str, Any]:
    # Performs authentication operations
```

### Use MCP Prompts When:
- **Template-Based Generation**: Functionality generates content based on templates + variables
- **LLM Interaction**: Primary purpose is to call LLMs with specific inputs
- **Content Creation**: Functionality creates documentation, code, or text content
- **Parameter Substitution**: Functionality takes variables and combines them into LLM requests
- **Reusable Patterns**: Functionality represents a repeatable prompting pattern

**Examples of Prompt Use Cases:**
```python
# Code generation from template
@prompt(name="generate-unit-test")
async def generate_unit_test(code: str, language: str) -> str:
    # Uses template + LLM to generate content

# Documentation generation
@prompt(name="generate-class-doc")
async def generate_class_doc(class_code: str) -> str:
    # Uses template + LLM to generate documentation
```

## Architecture Compliance

### Tools Architecture:
- Imperative Shell orchestrates operations
- Core provides Command Ports for business logic
- Adapters implement external integrations
- Functionality is idempotent where possible
- Proper error handling and audit logging

### Prompts Architecture:
- Imperative Shell coordinates LLM requests
- Core provides LLM Ports for interaction
- Template validation happens in Core
- Variable injection is properly sanitized
- Response handling follows functional patterns

## Validation Checklist

Before implementing as a tool:
- [ ] Does this perform an operation rather than content generation?
- [ ] Does this change system state or interact with external systems?
- [ ] Is this better modeled as a service call/command?
- [ ] Does this require authentication/authorization?
- [ ] Should this be audited for compliance/security?

Before implementing as a prompt:
- [ ] Is the primary function content generation using an LLM?
- [ ] Does this follow the template + variables pattern?
- [ ] Is this idempotent (same input always produces same type of content)?
- [ ] Are there variable injection risks that need mitigation?
- [ ] Will this be reused across multiple contexts?

## Current Project Examples Analysis

### Current Tools (Correctly Implemented):
1. `create-api-key` - System operation that modifies auth state ✓

### Potential Prompt Candidates:
The project architecture shows support for MCP prompts but currently has no actual prompt implementations.

## Migration Guidelines

### Promoting Operations to Tools:
- Use `@mcp.tool` decorator
- Implement in Imperative Shell orchestrator
- Validate inputs through Core use cases
- Handle errors with structured responses

### Creating Prompt Templates:
- Use `@mcp.prompt` decorator (via MCPPromptAdapter)
- Implement template validation in Core
- Sanitize variable injection in Core
- Coordinate LLM calls through LLM Ports in Shell

## Anti-Patterns

### ❌ Tool Anti-Patterns:
- Containing business logic in the Imperative Shell instead of Core
- Performing content generation that should be handled by LLM Ports
- Implementing idempotent content generation as tools

### ❌ Prompt Anti-Patterns:
- Implementing system state changes in prompts
- Performing direct database/file operations in prompts
- Bypassing Core validation for variable parameters
- Creating prompts with dangerous template injection vulnerabilities