🏷️ PRP METADATA
PRP ID: task_1736282766_a1b2c3
Type: tool-implementation
Domain: markdown-processing
Technology Stack: Python/FastMCP/Markdown-it-py
Complexity Level: Medium

🎯 BUSINESS CONTEXT LAYER
Business Objectives
- [ ] Implement `process_task` tool that receives `task_file_uri` and returns structured data with unique `task_id_str`
- [ ] Create `setup_context_engineering` prompt that guides LLM to create local directory structure `.ctxfy/{task_id_str}/`
- [ ] Enable client-side file management while maintaining server-side processing of task content
- [ ] Support MCP clients (Claude Code, Cursor, Trae) with clear environment setup instructions

SLAs & Performance Requirements
- [ ] Tool `process_task` processes files up to 10MB in under 2 seconds
- [ ] Task ID generation completes with maximum 25 character length for filesystem compatibility
- [ ] Response time for prompt registration under 5 seconds
- [ ] Error handling provides clear messages for invalid URIs, missing files, or permission issues

🔧 TECHNICAL TRANSLATION
Architecture Pattern
- [ ] FCIS architecture: Core business logic in `src/core/`, I/O operations in `src/shell/`
- [ ] Tool implementation in `src/shell/adapters/tools/` following existing pattern from `specification_generation_tool.py`
- [ ] Registration via `src/shell/orchestrators/mcp_orchestrator.py` using `ToolRegistry`
- [ ] Value objects for immutable data structures using `@dataclass(frozen=True)`

Technology Specifications
- [ ] Python 3.9+ with FastMCP framework for MCP tool implementation
- [ ] markdown-it-py for robust CommonMark parsing of task files
- [ ] SHA-256 hashing for unique task ID generation
- [ ] Unix timestamp integration for time-based component of task IDs

Specification Output
📝 Specification Output
Expected Deliverables
- [ ] `src/shell/adapters/tools/task_processing_tool.py` - Implementation of `process_task` tool with URI validation and task ID generation
- [ ] `resources/prompts.yaml` - **ADD** `setup_context_engineering` prompt configuration (see template below)
- [ ] `src/core/models/task_models.py` - Value objects for task data structures (`TaskID`, `TaskContent`)
- [ ] `tests/shell/adapters/tools/test_task_processing_tool.py` - Unit tests for the tool
- [ ] `tests/core/models/test_task_models.py` - Tests for value objects

### Prompt Configuration Template (for resources/prompts.yaml)
```yaml
setup_context_engineering:
  name: "Context Engineering Setup Prompt"
  description: "Guides LLM to prepare local environment for Context Engineering workflow using process_task tool results"
  template: |
    You are a specialized agent in Context Engineering. Your task is to prepare 
    the local environment to process a task using the complete Context Engineering workflow.

    Steps to follow:

    1. First, use the tool 'process_task' with the file URI: {task_file_uri}

    2. With the returned result (which will include task_id_str and file_content), you must:
    
    - Create locally the directory structure: .ctxfy/{task_id_str}/
    - Save the file content as .ctxfy/{task_id_str}/original_task.md

    3. Important: You do not have permission to execute shell code or scripts.
    Use the following approaches (depending on your MCP client capabilities):

    a) If your MCP client supports native file operations:
        - Use your client's file manipulation capabilities
        - Create the directory .ctxfy/{task_id_str}/ using the available commands in your client
        - Save the file content to .ctxfy/{task_id_str}/original_task.md using your client's resources

    b) If your MCP client does not support automatic file operations:
        - Provide clear instructions to the user to create manually:
            
    "Please manually create the following directory structure in your local environment:
            .ctxfy/{task_id_str}/

            Then, save the following content as .ctxfy/{task_id_str}/original_task.md:
            [file content]
    "

    4. After creating the structure, confirm to the user that the environment is prepared and 
    inform the complete path: .ctxfy/{task_id_str}/

    5. Do not proceed to the next steps of Context Engineering yet. Only 
    prepare the initial environment and wait for additional instructions.

    Remember: Your responsibility is to organize locally, not to execute code.
    If you encounter limitations in your client's capabilities, be transparent 
    with the user and offer manual alternatives.
  parameters:
    - name: "task_file_uri"
      type: "TaskFileURI"
      description: "URI of the markdown file containing the task description"
  metadata:
    category: "context-engineering"
    version: "1.0"
    tags:
      - "setup"
      - "environment"
      - "mcp-integration"
```

Code Structure Guidelines
- [ ] Core logic in `src/core/` with pure functions and immutable value objects
- [ ] Shell adapters in `src/shell/adapters/tools/` for MCP integration
- [ ] Registration systems in `src/shell/registry/` for tool/prompt management
- [ ] Follow existing naming conventions from `specification_generation_tool.py`

✅ VALIDATION FRAMEWORK
Testing Strategy
- [ ] Unit tests for `process_task` tool in `tests/shell/adapters/tools/` (70% of test suite)
- [ ] Integration tests for URI processing and file reading functionality (25% of test suite)
- [ ] End-to-end tests for prompt registration and execution (5% of test suite)
- [ ] Architecture compliance tests verifying core/shell separation

Quality Gates
- [ ] Ruff formatting compliance with line-length=88 and select=["E", "F", "I", "B", "C4", "T20"]
- [ ] MyPy strict mode validation for core packages
- [ ] All value objects use `@dataclass(frozen=True)` pattern
- [ ] Tool registration follows existing pattern from `tool_registry.register_tool()`

✨ AI CONTEXT ADAPTATION
Model Compatibility Notes
- [ ] Claude 3: Excellent for complex URI handling and structured data processing
- [ ] GPT-4: Good for multi-step prompt orchestration and error handling
- [ ] Include specific dependency versions (markdown-it-py, python-frontmatter) for consistency

📊 SUCCESS METRICS
Performance Metrics
- [ ] Tool response time under 2 seconds for files up to 10MB
- [ ] Prompt registration completes in under 5 seconds
- [ ] Task ID generation completes in under 50ms
- [ ] URI validation and error handling completes in under 100ms

Quality & Reliability Metrics
- [ ] 100% Ruff formatting compliance across all new files
- [ ] 95% code coverage for new functionality
- [ ] Zero MyPy type errors in core packages
- [ ] All architecture compliance tests pass (core/shell separation)

📋 ARCHITECTURE COMPLIANCE CHECKLIST
- [ ] FCIS patterns properly implemented in src/core/models/task_models.py
- [ ] Port naming conventions followed in src/shell/adapters/tools/task_processing_tool.py
- [ ] Test distribution requirements met in tests/shell/adapters/tools/test_task_processing_tool.py
- [ ] Value objects are immutable in src/core/models/task_models.py
- [ ] Core functions are pure in src/core/use_cases/task_processing.py
- [ ] Token budget under 1000 tokens