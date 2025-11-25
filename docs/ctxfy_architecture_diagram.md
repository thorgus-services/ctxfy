# Ctxfy Architecture - Technical Specification Generation System

This document provides a C4 component diagram visualization of the Ctxfy system architecture based on the Functional Core/Imperative Shell (FCIS) pattern.

## System Context

The Ctxfy system is designed to generate technical specifications from business requirements using a FastMCP-based server. It integrates with external LLM services to process prompts and generate comprehensive technical documentation.

## C4 Component Diagram

```mermaid
C4Component
    title Ctxfy Architecture - Technical Specification Generation System

    Person(user, "Developer/Architect", "User who needs to generate technical specifications from business requirements")

    System_Boundary(ctxfy_system, "Ctxfy Specification Generator") {
        Component(mcp_server, "MCP Server", "FastMCP server that exposes tools and prompts", "FastMCP")

        System_Boundary(core, "Functional Core") {
            Component(use_case, "GenerateSpecificationUseCase", "Business logic for specification generation", "Python")
            Component(workflow, "SpecificationWorkflow", "Workflow for processing specification generation", "Python")
            Component(spec_result, "SpecificationResult", "Immutable result object", "Dataclass")
            Component(spec_types, "Specification Types", "Type definitions", "NewType")
            Component(business_req_type, "BusinessRequirements", "Business requirements type", "Type")
        }

        System_Boundary(shell, "Imperative Shell") {
            Component(spec_tool, "SpecificationGenerationTool", "Implementation of specification generation port", "Python")
            Component(yaml_loader, "YAMLPromptLoader", "Loads prompt templates from YAML files", "Python")
            Component(generic_yaml_prompt, "GenericYAMLPrompt", "Generic YAML-based prompt implementation", "Python")
            Component(orchestrator, "MCPOrchestrator", "Coordinates tool registration and prompt management", "Python")
            Component(tool_registry, "ToolRegistry", "Manages registered tools", "Python")
            Component(dynamic_prompt_registry, "DynamicPromptRegistry", "Dynamically registers prompts from YAML config", "Python")
        }

        Component(prompt_config, "prompts.yaml", "YAML configuration with prompt templates", "YAML")
        Component(external_llm, "External LLM", "Language model that processes prompts", "LLM")
    }

    Rel(user, mcp_server, "Uses", "HTTP/MCP protocol")
    Rel(mcp_server, orchestrator, "Initialized by", "Dependency Injection")

    Rel(orchestrator, tool_registry, "Configures", "Tool Management")
    Rel(orchestrator, dynamic_prompt_registry, "Configures", "Dynamic Prompt Loading")
    Rel(orchestrator, spec_tool, "Registers", "Tool Registration")

    Rel(tool_registry, spec_tool, "Registers", "Tool Registration")
    Rel(spec_tool, use_case, "Delegates to", "Business Logic")
    Rel(spec_tool, business_req_type, "Uses", "Business Requirements Type")

    Rel(use_case, workflow, "Delegates to", "Workflow Logic")
    Rel(workflow, spec_result, "Creates", "SpecificationResult")
    Rel(workflow, business_req_type, "Uses", "Business Requirements Type")

    Rel(yaml_loader, prompt_config, "Loads from", "YAML File")
    Rel(generic_yaml_prompt, yaml_loader, "Uses", "YAML Loading")

    Rel(dynamic_prompt_registry, generic_yaml_prompt, "Creates dynamic functions for", "Generic Prompts")
    Rel(dynamic_prompt_registry, yaml_loader, "Uses", "YAML Loading")

    Rel(mcp_server, external_llm, "Sends prompts to", "API Call")
    Rel(external_llm, mcp_server, "Returns generated specification", "API Response")
```

## Architecture Overview

The Ctxfy system follows the Functional Core/Imperative Shell (FCIS) architectural pattern as defined in the project's architecture rules:

### Functional Core
- **Models**: Immutable data structures and type definitions
- **Use Cases**: Pure business logic functions with no side effects
- **Ports**: Interface definitions (Protocols) defining contracts
- **Workflows**: Pure workflow definitions

### Imperative Shell
- **Adapters**: Implementation of core ports with side effects
- **Orchestrators**: Flow coordinators that manage component interactions
- **Registries**: Dynamic registration and management systems

### Key Design Principles
- Dependencies flow inward: shell → core
- No circular dependencies between packages
- Stable core packages don't depend on unstable shell packages
- Maximum 4 dependencies per orchestrator
- Proper port naming conventions followed

## How to Render

To view the visual diagram, you need to use a Markdown viewer that supports Mermaid diagrams, such as:
- GitHub
- GitLab
- Obsidian
- Mermaid Live Editor
- Any Markdown editor with Mermaid support