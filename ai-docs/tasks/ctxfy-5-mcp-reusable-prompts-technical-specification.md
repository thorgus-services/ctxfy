# TECHNICAL SPECIFICATION: ctxfy MCP Reusable Prompts Implementation with @mcp.prompt

## 1. Overview

This document provides the complete technical specification for implementing reusable prompts using the `@mcp.prompt` decorator within the ctxfy MCP Server, with integration of `ctx.sample()` for dynamic processing. The implementation follows Hexagonal Architecture and Functional Core & Imperative Shell patterns as specified in the project rules.

### 1.1 Purpose
- Implement a system for registering and reusing prompts via `@mcp.prompt` decorator
- Integrate `ctx.sample()` as the central mechanism for processing dynamic prompts with variable substitution
- Enable prompt sharing between clients through standardized template registration
- Provide comprehensive testing and documentation for the prompt system

### 1.2 Scope
- Server-side `@mcp.prompt` implementation for prompt template registration
- Dynamic prompt processing with `ctx.sample()`
- Variable substitution and template rendering
- Performance requirements (<200ms per request)
- Unit tests for prompt functionality
- OpenAPI documentation for registered prompts

## 2. Architecture

### 2.1 Hexagonal Architecture Structure

```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── prompt_models.py     # PromptRequest, PromptTemplate, etc.
│   │   └── variable_models.py   # Variable, VariableSubstitution
│   ├── use_cases/        # Pure functions implementing business rules  
│   │   └── prompt_use_cases.py  # Prompt processing logic
│   └── ports/            # Interfaces only (Protocols)
│       └── prompt_ports.py      # PromptCommandPort, PromptQueryPort
├── adapters/             # Implementations of core ports
│   ├── mcp_prompts/      # @mcp.prompt decorator implementation
│   ├── prompt_registry/  # Prompt template registration system
│   ├── template_engine/  # Template rendering and variable substitution
│   ├── llm_sampling/     # ctx.sample() adapter implementation
│   └── openapi_docs/     # OpenAPI documentation for prompts
└── app/                  # Application composition and configuration
```

### 2.2 Core Components

#### 2.2.1 Core Ports (`src/core/ports/prompt_ports.py`)
- `PromptCommandPort`: Primary port for registering and executing prompts
  - `register_prompt_template(template_id: str, template: PromptTemplate) -> bool`
  - `execute_prompt(prompt_id: str, variables: Dict[str, Any]) -> PromptResponse`
- `PromptQueryPort`: Primary port for retrieving prompt information
  - `get_registered_prompts() -> List[PromptTemplate]`
  - `get_prompt_template(prompt_id: str) -> Optional[PromptTemplate]`

#### 2.2.2 Core Models (`src/core/models/prompt_models.py`, `src/core/models/variable_models.py`)
- `PromptTemplate`: Immutable value object for MCP prompt templates
  - `template_id: str` - Unique identifier for the template
  - `template_content: str` - Template string with variable placeholders (e.g. `{variable_name}`)
  - `variables: Tuple[Variable, ...]` - List of expected variables for the template
  - `description: str` - Description of what the prompt does
  - `model_name: str` - LLM model to use for sampling
- `PromptRequest`: Immutable value object for prompt execution requests
  - `template_id: str` - ID of the template to use
  - `variables: Dict[str, Any]` - Values to substitute into template
  - `request_id: str` - Unique request identifier for logging
- `PromptResponse`: Immutable value object for prompt execution responses
  - `request_id: str` - Request identifier
  - `template_id: str` - Template that was used
  - `result: str` - Result of the LLM sampling operation
  - `execution_time_ms: float` - Time taken for execution
- `Variable`: Immutable value object representing template variables
  - `name: str` - Variable name
  - `type_hint: str` - Expected type (e.g. "string", "number", "boolean")
  - `default_value: Optional[Any]` - Default value if not provided
  - `description: str` - Description of the variable's purpose
  - `required: bool` - Whether the variable is required

#### 2.2.3 Core Use Cases (`src/core/use_cases/prompt_use_cases.py`)
- `register_prompt_template(template: PromptTemplate) -> bool`: Pure function to register a prompt template
- `execute_prompt_request(request: PromptRequest) -> PromptResponse`: Pure function to process a prompt request
- `substitute_variables(template: str, variables: Dict[str, Any]) -> str`: Pure function for template variable substitution
- `validate_prompt_template(template: PromptTemplate) -> List[ValidationError]`: Pure function for template validation
- `validate_prompt_request(request: PromptRequest, template: PromptTemplate) -> List[ValidationError]`: Pure function for request validation

### 2.3 Adapters

#### 2.3.1 MCP Prompts Adapter (`src/adapters/mcp_prompts/prompt_decorator.py`)
- Implements `@mcp.prompt` decorator following FastMCP specifications
- Integrates with FastMCP's prompt registration system
- Provides automatic serialization of arguments for client consumption
- Maps registered functions to `@mcp.prompt` format with proper metadata

#### 2.3.2 Prompt Registry (`src/adapters/prompt_registry/prompt_registry.py`)
- Maintains in-memory registry of available prompt templates
- Thread-safe access to registered templates
- Provides lookup functionality for templates by ID
- Implements template lifecycle management (register, update, remove)

#### 2.3.3 Template Engine (`src/adapters/template_engine/template_renderer.py`)
- Handles template rendering with variable substitution
- Supports complex variable substitution patterns
- Validates required variables are provided
- Implements safe string formatting to prevent injection attacks
- Supports nested variable substitution and complex templates

#### 2.3.4 LLM Sampling Adapter (`src/adapters/llm_sampling/llm_sampler.py`)
- Provides `ctx.sample()` interface wrapper
- Handles LLM sampling requests with proper error handling
- Implements performance monitoring and logging
- Manages model configuration and timeouts
- Includes circuit breaker patterns for resilience

#### 2.3.5 OpenAPI Documentation (`src/adapters/openapi_docs/prompt_docs.py`)
- Generates OpenAPI documentation for registered prompts
- Documents available prompt templates with parameters
- Provides example requests and responses
- Integrates with FastAPI's documentation system

## 3. Implementation Details

### 3.1 Prompt Registration System
- Use `@mcp.prompt` decorator to register server-side prompt templates
- Each registered prompt should include:
  - Unique identifier following FastMCP naming conventions (e.g., "ctxfy.user-context.summary")
  - Parameterized template with variable placeholders
  - Metadata describing required and optional parameters
- Registration occurs at server startup
- Templates are validated for proper variable substitution syntax

### 3.2 Variable Substitution Mechanism
- Template strings use Python's `str.format()` with named placeholders (e.g., `"Hello {name}, your balance is {balance}"`)
- Variables are validated against the expected schema before substitution
- Missing required variables raise `MissingVariableError`
- Extra variables not defined in the template are ignored
- Type checking occurs during substitution to prevent runtime errors

### 3.3 ctx.sample() Integration
- `ctx.sample()` is called after variable substitution is completed
- Parameters passed to `ctx.sample()`:
  - `prompt`: The fully substituted prompt string
  - `model`: Model name specified in the template (fallback to default)
  - `temperature`: Configurable parameter for creativity control
  - `max_tokens`: Maximum response length limit
- Error handling includes LLM provider failures, timeouts, and model unavailability
- Response is captured and returned through the prompt system

### 3.4 Performance Requirements
- Individual prompt requests complete within <200ms (p95)
- System supports concurrent prompt execution
- Caching mechanisms for frequently used templates
- Optimized variable substitution to prevent bottlenecks
- Memory management to prevent accumulation of unused templates

### 3.5 Error Handling & Validation
- Validate template syntax during registration
- Validate variable types during substitution
- Handle LLM sampling errors gracefully
- Provide detailed error messages for debugging
- Implement circuit breaker pattern for resilient operations

## 4. ctx.sample() Implementation for Dynamic Prompts

The system enables dynamic prompt processing through variable substitution:

```python
@server.prompt("ctxfy.summarize.text")
async def summarize_text_prompt(ctx, 
                               text: str, 
                               max_length: int = 100,
                               style: str = "concise"):
    """
    Summarizes text using configurable parameters
    """
    # Core logic is in the use case, this is the shell
    from src.core.use_cases.prompt_use_cases import execute_prompt_request
    
    request = PromptRequest(
        template_id="ctxfy.summarize.text",
        variables={
            "text": text,
            "max_length": max_length,
            "style": style
        },
        request_id=uuid.uuid4().hex
    )
    
    # The actual processing happens in the core
    result = await execute_prompt_request(request)
    return result
```

## 5. Testing Strategy

### 5.1 Unit Tests (≥70% of test suite)
- Test all core functions in isolation without external dependencies
- Verify prompt template validation logic
- Test variable substitution with various inputs
- Validate error conditions and edge cases
- Performance testing to ensure <200ms response time

### 5.2 Integration Tests (≤25% of test suite)
- Test core with real/fake adapters
- Verify `@mcp.prompt` registration with FastMCP framework
- Test complete prompt execution pipeline
- Validate ctx.sample() integration with mock responses

### 5.3 Test Coverage Requirements
- 90%+ test coverage for core domain logic
- Performance tests for response time validation
- Error handling tests for all failure scenarios
- Security tests for template injection prevention

### 5.4 Specific Test Scenarios
```python
# Test variable substitution
def test_variable_substitution_with_valid_input():
    template = "Hello {name}, your score is {score}"
    variables = {"name": "Alice", "score": 95}
    result = substitute_variables(template, variables)
    assert result == "Hello Alice, your score is 95"

# Test missing variable error
def test_missing_required_variable_raises_error():
    template = "Hello {name}, your score is {score}"
    variables = {"name": "Alice"}  # missing score
    with pytest.raises(MissingVariableError):
        substitute_variables(template, variables)

# Test performance requirement
def test_prompt_execution_performance():
    # Execute prompt multiple times and verify p95 < 200ms
    times = []
    for _ in range(100):
        start = time.time()
        result = execute_prompt_request(test_request)
        times.append((time.time() - start) * 1000)
    
    p95_time = np.percentile(times, 95)
    assert p95_time < 200.0
```

## 6. OpenAPI Documentation

### 6.1 Automatic Documentation Generation
- Automatically document all registered prompts
- Include parameter validation schema
- Provide example requests and responses
- Generate interactive documentation endpoint

### 6.2 API Schema for Prompts
```yaml
openapi: 3.0.1
info:
  title: ctxfy MCP Prompt API
  description: API for registered prompt templates
  version: 1.0.0
paths:
  /prompts/{prompt_id}/execute:
    post:
      summary: Execute a registered prompt with variables
      parameters:
        - name: prompt_id
          in: path
          required: true
          description: ID of the registered prompt template
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                variables:
                  type: object
                  description: Variables to substitute into the template
                  additionalProperties: true
      responses:
        '200':
          description: Successfully executed prompt
          content:
            application/json:
              schema:
                type: object
                properties:
                  request_id:
                    type: string
                  result:
                    type: string
                  execution_time_ms:
                    type: number
```

## 7. Files to be Created

### 7.1 Core Components
- `src/core/models/prompt_models.py` - Immutable prompt-related value objects
- `src/core/models/variable_models.py` - Variable-related value objects
- `src/core/ports/prompt_ports.py` - Core prompt protocols
- `src/core/use_cases/prompt_use_cases.py` - Pure prompt processing functions

### 7.2 Adapters
- `src/adapters/mcp_prompts/prompt_decorator.py` - @mcp.prompt implementation
- `src/adapters/prompt_registry/prompt_registry.py` - Template registry
- `src/adapters/template_engine/template_renderer.py` - Template processing
- `src/adapters/llm_sampling/llm_sampler.py` - ctx.sample() wrapper
- `src/adapters/openapi_docs/prompt_docs.py` - OpenAPI documentation

### 7.3 Tests
- `tests/unit/test_prompt_models.py` - Value object tests
- `tests/unit/test_prompt_use_cases.py` - Core logic tests
- `tests/integration/test_prompt_execution.py` - Integration tests
- `tests/performance/test_prompt_performance.py` - Performance tests

### 7.4 Documentation
- `docs/prompts-guide.md` - User guide for creating and using prompts
- `docs/api-reference.md` - API documentation for prompt endpoints

## 8. Compliance with Rules

This implementation follows all specified architectural rules:

✅ **Hexagonal Architecture**: Proper boundaries between core, adapters, and application layer
✅ **Functional Core & Imperative Shell**: Pure functions in core, side effects in shell
✅ **Immutable Value Objects**: All domain models use `@dataclass(frozen=True)`
✅ **Protocol-based Ports**: Proper naming and separation of primary/secondary ports
✅ **Testing Strategy**: TDD approach with required test distribution
✅ **Package Architecture**: Clear separation following domain → application → infrastructure → interfaces
✅ **Structured Logging**: All operations include required fields (prompt_id, latency_ms, model)

## 9. Expected Outcomes

Upon successful implementation:

1. **Prompt Registration**: Developers can define reusable prompts using `@mcp.prompt` decorator
2. **Dynamic Processing**: ctx.sample() processes prompts with variable substitution
3. **Performance**: <200ms response time for prompt execution (p95)
4. **Error Handling**: Comprehensive error handling with meaningful messages
5. **Documentation**: OpenAPI documentation for all registered prompts
6. **Test Coverage**: ≥90% coverage for core logic with performance verification
7. **Security**: Protected against template injection and other vulnerabilities
8. **Scalability**: Support for concurrent prompt execution with proper resource management

## 10. Success Criteria

- [ ] All prompts defined with `@mcp.prompt` process through `ctx.sample()` successfully
- [ ] Variable substitution works correctly with required/optional parameters
- [ ] Performance requirements (<200ms) are met consistently
- [ ] Unit tests cover all core functionality with >90% coverage
- [ ] Integration tests verify complete prompt execution pipeline
- [ ] OpenAPI documentation is generated for all registered prompts
- [ ] Error handling covers all failure scenarios appropriately
- [ ] Implementation follows all architectural rules and patterns
- [ ] System supports prompt sharing between different MCP clients