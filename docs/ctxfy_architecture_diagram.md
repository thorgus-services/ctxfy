# Ctxfy Architecture - Technical Specification Generation System

This document provides a C4 component diagram visualization of the Ctxfy system architecture based on the Functional Core/Imperative Shell (FCIS) pattern.

## System Context

The Ctxfy system is designed to generate technical specifications from business requirements using a FastMCP-based server. It integrates with external LLM services to process prompts and generate comprehensive technical documentation.

## C4 Component Diagram

```mermaid
C4Component
    title Ctxfy Architecture - Technical Specification Generation System

    Person(user, "Developer/Architect", "User who needs to generate technical specifications from business requirements")
    
    System_Boundary(system, "Ctxfy Specification Generator") {
        Component(mcp_server, "MCP Server", "FastMCP server that exposes tools and prompts", "FastMCP")
        
        System_Boundary(core, "Functional Core (Pure Functions, No Side Effects)") {
            Component(use_case, "GenerateSpecificationUseCase", "Business logic for specification generation", "Python")
            Component(workflow, "SpecificationWorkflow", "Workflow for processing specification generation", "Python")
            
            Container_Boundary(core_models, "Models") {
                Component(spec_result, "SpecificationResult", "Immutable result object with ID, content, and filename", "Dataclass")
                Component(spec_result_types, "Specification Types", "NewType definitions: SpecificationId, Content, Filename, DirectoryPath", "Types")
                Component(spec_workflow_def, "SpecificationWorkflowDefinition", "Defines workflow parameters including requirements and save location", "Dataclass")
                Component(business_req_type, "BusinessRequirements", "NewType for business requirements input", "Type")
            }
            
            Container_Boundary(core_ports, "Ports (Protocols/Interfaces)") {
                Component(spec_generation_port, "SpecificationGenerationCommandPort", "Port for specification generation commands", "Protocol")
                Component(spec_workflow_port, "SpecificationWorkflowPort", "Port for workflow execution", "Protocol")
                Component(generic_prompt_port, "GenericPromptCommandPort", "Generic port for prompt commands", "Protocol")
            }
        }

        System_Boundary(shell, "Imperative Shell (Side Effects & External Dependencies)") {
            System_Boundary(adapters, "Adapters (Port Implementations)") {
                Component(spec_tool, "SpecificationGenerationTool", "Implementation of specification generation port", "Python")
                Component(yaml_loader, "YAMLPromptLoader", "Loads prompt templates from YAML files", "Python")
                Component(generic_yaml_prompt, "GenericYAMLPrompt", "Generic YAML-based prompt implementation", "Python")
            }

            System_Boundary(orchestrators, "Orchestrators") {
                Component(orchestrator, "MCPOrchestrator", "Coordinates tool registration and prompt management", "Python")
            }

            System_Boundary(registries, "Registries") {
                Component(tool_registry, "ToolRegistry", "Manages registered tools", "Python")
                Component(dynamic_prompt_registry, "DynamicPromptRegistry", "Dynamically registers prompts from YAML config", "Python")
            }
        }

        Container_Boundary(prompts, "Prompts Configuration") {
            Component(prompt_config, "prompts.yaml", "YAML configuration with prompt templates", "YAML")
            Component(spec_save_instruction, "Specification Save Instruction", "Prompt template for generating and saving specifications", "YAML Template")
        }
    }

    System_External(external_llm, "External LLM", "Language model that processes prompts and generates specifications")

    ' Core dependencies (dependencies flow inward: shell → core)
    Rel(workflow, spec_workflow_port, "Implements", "Port Contract")
    Rel(workflow, spec_result, "Creates", "SpecificationResult")
    Rel(workflow, spec_result_types, "Uses", "Specification Types")
    Rel(workflow, spec_workflow_def, "Uses", "Workflow Definition")
    Rel(workflow, business_req_type, "Uses", "Business Requirements Type")
    Rel(use_case, workflow, "Delegates to", "Workflow Logic")
    
    ' Shell dependencies
    Rel(spec_tool, spec_generation_port, "Implements", "Port Contract")
    Rel(spec_tool, use_case, "Delegates to", "Business Logic")
    Rel(spec_tool, spec_workflow_def, "Uses", "Workflow Definition")
    Rel(spec_tool, business_req_type, "Uses", "Business Requirements Type")
    
    Rel(generic_yaml_prompt, generic_prompt_port, "Implements", "Port Contract")
    Rel(generic_yaml_prompt, yaml_loader, "Uses", "YAML Loading")
    
    Rel(yaml_loader, prompt_config, "Loads from", "YAML File")
    
    ' Orchestrator dependencies
    Rel(orchestrator, spec_tool, "Registers", "Tool Registration")
    Rel(orchestrator, dynamic_prompt_registry, "Configures", "Dynamic Prompt Loading")
    Rel(orchestrator, tool_registry, "Uses", "Tool Management")
    
    ' Registry dependencies
    Rel(tool_registry, spec_generation_port, "Registers tools implementing", "Port Contract")
    Rel(dynamic_prompt_registry, generic_yaml_prompt, "Creates dynamic functions for", "Generic Prompts")
    Rel(dynamic_prompt_registry, yaml_loader, "Uses", "YAML Loading")
    
    ' System integration
    Rel(user, mcp_server, "Uses", "HTTP/MCP protocol")
    Rel(mcp_server, orchestrator, "Initialized by", "Dependency Injection")
    
    ' External communication
    Rel(mcp_server, external_llm, "Sends prompts to", "API Call")
    Rel(external_llm, mcp_server, "Returns generated specification", "API Response")
    
    UpdateLayout({
        "user": 0,
        "mcp_server": 1,
        "orchestrator": 2,
        "tool_registry": 3,
        "dynamic_prompt_registry": 4,
        "spec_tool": 5,
        "yaml_loader": 6,
        "generic_yaml_prompt": 7,
        "use_case": 8,
        "workflow": 9,
        "spec_result": 10,
        "spec_result_types": 11,
        "spec_workflow_def": 12,
        "business_req_type": 13,
        "spec_generation_port": 14,
        "spec_workflow_port": 15,
        "generic_prompt_port": 16,
        "prompt_config": 17,
        "spec_save_instruction": 18,
        "external_llm": 19
    })
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