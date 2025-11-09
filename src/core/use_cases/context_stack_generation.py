"""Functional core for context stack generation logic."""

import time
from datetime import datetime
from decimal import Decimal
from typing import List

from ..models.context_models import (
    ContextGenerationRequest,
    ContextGenerationResponse,
    ContextLayer,
    ContextStack,
    ContextStackMetadata,
)


def generate_context_stack_functional(request: ContextGenerationRequest) -> ContextGenerationResponse:
    """
    Pure function to generate a context stack based on feature description.
    This function is part of the functional core with no side effects.
    """
    start_time = time.perf_counter()
    
    try:
        # Create system layer
        system_layer = _create_system_layer(request.feature_description)
        
        # Create domain layer
        domain_layer = _create_domain_layer(request.feature_description, request.target_technologies)
        
        # Create task layer
        task_layer = _create_task_layer(request.feature_description)
        
        # Create metadata
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Qwen Code Context Generator",
            domain="Model Context Protocol (MCP) with Qwen Code Integration",
            task_type="Context Stack Generation"
        )
        
        # Create context stack
        context_stack = ContextStack(
            system_layer=system_layer,
            domain_layer=domain_layer,
            task_layer=task_layer,
            metadata=metadata
        )
        
        processing_time = Decimal(str(time.perf_counter() - start_time))
        
        return ContextGenerationResponse(
            success=True,
            context_stack=context_stack,
            error_message=None,
            processing_time=processing_time
        )
    except Exception as e:
        processing_time = Decimal(str(time.perf_counter() - start_time))
        return ContextGenerationResponse(
            success=False,
            context_stack=None,
            error_message=str(e),
            processing_time=processing_time
        )


def _create_system_layer(feature_description: str) -> ContextLayer:
    """Create the system context layer."""
    description = f"""
    Defines the AI's 'personality' and boundaries for implementing {feature_description}.
    
    Role Definition:
    You are a senior software architect specializing in Model Context Protocol (MCP) 
    and AI integration with 10+ years of experience.
    Your mission is to generate comprehensive context stacks for MCP-enabled 
    Qwen Code environments following the principles of hexagonal architecture, 
    functional core with imperative shell, and clean architecture patterns.
    """
    
    specifications = {
        "Tone of Voice": "Technical and precise (e.g., detailed architectural explanations, clear code examples)",
        "Detail Level": "High for architectural decisions, medium for implementation details",
        "Operating Boundaries": "Follow established architectural patterns (Hexagonal Architecture, FCIS), use immutable value objects in core, avoid infrastructure dependencies in core",
        "Security Policies": "No exposure of sensitive project information, follow security best practices from MCP and toolchain standards"
    }
    
    return ContextLayer(
        name="system",
        description=description.strip(),
        specifications=specifications,
        dependencies=["MCP", "Qwen Code"]
    )


def _create_domain_layer(feature_description: str, target_technologies: List[str]) -> ContextLayer:
    """Create the domain context layer."""
    tech_str = ", ".join(target_technologies) if target_technologies else "Python 3.13+, FastAPI, MCP"
    
    description = f"""
    Provides specialized domain knowledge for implementing {feature_description} 
    with {tech_str} technologies.
    """
    
    specifications = {
        "Key Terminology": """
MCP: Model Context Protocol - Standard for connecting AI applications to external systems
MCP Host: AI application that coordinates and manages one or more MCP clients (e.g., Qwen Code)
MCP Client: Component that maintains connection to an MCP server and obtains context
MCP Server: Program that provides context to MCP clients
Hexagonal Architecture: Architecture pattern with core depending only on abstract ports, adapters implement them
FCIS: Functional Core & Imperative Shell - separation of pure logic and side effects
Value Objects: Immutable, self-validating data structures
CQS: Command Query Separation - Queries return data, Commands perform actions
MCP Primitives: Core capabilities - Tools (actions), Resources (data), Prompts (templates)
        """.strip(),
        "Methodologies & Patterns": """
- Apply Hexagonal Architecture with clear port naming (CommandPort, QueryPort, GatewayPort, RepositoryPort)
- Follow Functional Core & Imperative Shell (FCIS) patterns
- Use immutable value objects in functional core
- Implement TDD testing with emphasis on unit tests >70% of suite
- Apply CQS (Command Query Separation) principle
- Follow orchestrator pattern for workflow coordination
- Apply incremental adoption strategy for existing codebases
- Use property-based testing for core functions
        """.strip(),
        "Reference Architecture": """
- Hexagonal Architecture: Core → Ports ← Adapters
- Functional Core & Imperative Shell: Pure functions in core, side effects in shell
- Package Flow: interfaces → application → domain → infrastructure (inward only)
- MCP Integration: Qwen Code as host → MCP clients → MCP servers
- Transport Mechanisms: Stdio, SSE, Streamable HTTP (for MCP communication)
        """.strip()
    }
    
    dependencies = ["MCP", "Hexagonal Architecture", "FCIS", "Value Objects"] + target_technologies
    
    return ContextLayer(
        name="domain",
        description=description.strip(),
        specifications=specifications,
        dependencies=dependencies
    )


def _create_task_layer(feature_description: str) -> ContextLayer:
    """Create the task context layer."""
    description = f"""
    Specifies exactly what to do and success criteria for implementing {feature_description}.
    """
    
    specifications = {
        "Primary Objective": f"""
Generate auto-generated context stacks for Qwen Code using MCP, implementing the technical 
specification for context stack generation for {feature_description} with System, Domain, and Task layers.
The generated context stack should follow architectural principles and integrate with 
Qwen Code's MCP server configuration.
        """.strip(),
        "Success Criteria": """
- Functional: Context stack contains 3 essential layers (System, Domain, Task) with technical specifications
- Non-Functional: Generation completes in under 15 seconds, MCP server returns structured JSON response
- Quality: Context follows architectural patterns (hexagonal architecture, FCIS), uses proper error handling
        """.strip(),
        "Constraints & Requirements": """
- Technologies: Python 3.13+, Pydantic Settings, Ruff linting, Mypy strict type checking
- Architecture: Hexagonal with Core/Ports/Adapters/Shell structure
- MCP Integration: Follow MCP protocol for tool discovery and execution
- Performance: Complete generation in under 15 seconds
- Immutability: Use @dataclass(frozen=True) for all value objects in core
- Dependency Management: Core must never import infrastructure packages
- Testing: ≥70% unit tests, ≥90% coverage in Core, TDD approach
- MCP Server: Must support tools/list, tools/call operations
        """.strip()
    }
    
    return ContextLayer(
        name="task",
        description=description.strip(),
        specifications=specifications,
        dependencies=["MCP", "Context Generation"]
    )


