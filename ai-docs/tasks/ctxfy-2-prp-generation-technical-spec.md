# Technical Specification: PRP Generation for MCP Client

## 1. Overview

This document provides the technical specification for implementing an automatic PRP (Product Requirements Prompt) generation feature for the MCP Client in Qwen Code. The feature addresses the manual overhead developers face when creating structured technical specifications from user stories.

## 2. Requirements Analysis

### 2.1 User Story
As an MCP Client in Qwen Code,
I want to receive a template PRP with explicit execution instructions
So that I can generate detailed technical specifications from simple user stories

### 2.2 Acceptance Criteria
- 100% of template variables {{}} are replaced with concrete values
- Response contains clear instructions for execution with absolute paths
- Generated prompt size is <= 2000 tokens
- PRP is generated in under 3 seconds
- Output file is placed in the correct directory (@ai-docs/tasks/**)

### 2.3 Validation Metrics
- Template variable substitution accuracy (100%)
- Response time (under 3 seconds)
- Token count compliance (≤2000 tokens)
- File generation success rate

## 3. Architecture Design

### 3.1 System Architecture
Following the Hexagonal Architecture principles outlined in the rules:

- **Core Domain**: PRP template processing and variable substitution logic
- **Primary Ports**: Command interfaces for PRP generation requests
- **Secondary Ports**: Interfaces for template file access, rules directory access, and output writing
- **Adapters**: Implementations for file system access, template parsing, and path resolution

### 3.2 Component Structure

```
src/
├── core/
│   ├── prp_generation/
│   │   ├── models.py             # PRP value objects
│   │   ├── processors.py         # Core generation logic
│   │   └── ports/                # Abstract interfaces
│   │       ├── template_ports.py
│   │       └── generation_ports.py
├── shell/
│   └── orchestrators/
│       └── prp_generation_orchestrator.py
└── adapters/
    ├── template_processing/
    │   ├── file_loader.py
    │   └── variable_substitutor.py
    └── mcp_integration/
        └── prp_generation_adapter.py
```

## 4. Detailed Design

### 4.1 Core Domain Model

Following the immutable value objects pattern:

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from decimal import Decimal
import json

@dataclass(frozen=True)
class PRPTemplate:
    """Immutable representation of a PRP template"""
    id: str
    content: str
    variables: List[str]
    
    def __post_init__(self):
        if not self.id or not self.content:
            raise ValueError("PRP template must have id and content")
    
    def substitute_variables(self, values: Dict[str, str]) -> 'PRPTemplate':
        """Return new template with variables substituted"""
        substituted_content = self.content
        for var, value in values.items():
            placeholder = f"{{{{{var}}}}}"
            substituted_content = substituted_content.replace(placeholder, value)
        
        return PRPTemplate(
            id=self.id,
            content=substituted_content,
            variables=[v for v in self.variables if v not in values.keys()]
        )

@dataclass(frozen=True)
class PRPGenerationRequest:
    """Request parameters for PRP generation"""
    user_story: str
    template_path: str
    rules_directory: str
    output_directory: str
    prp_id: str
    
    def __post_init__(self):
        if not self.user_story or not self.template_path:
            raise ValueError("User story and template path are required")

@dataclass(frozen=True)
class PRPGenerationResult:
    """Result of PRP generation process"""
    success: bool
    output_path: Optional[str]
    token_count: int
    error_message: Optional[str]
    
    def __post_init__(self):
        if self.success and not self.output_path:
            raise ValueError("Successful generation must include output path")
```

### 4.2 Core Business Logic

Following the functional code, imperative shell pattern:

```python
def process_prp_template(template: PRPTemplate, request: PRPGenerationRequest) -> str:
    """Pure function that processes PRP template with provided values"""
    # Substitute template variables with concrete values
    substitutions = {
        'prp_id': request.prp_id,
        'business_problem': request.user_story,
        'creation_date': '2025-11-10',  # This would come from actual timestamp in the shell
        'rules_directory': request.rules_directory,
        'output_directory': request.output_directory,
        'user_story': request.user_story,
        'prerequisites': f'- Access to template directory: {request.template_path}\n- Access to rules directory: {request.rules_directory}\n- Write access to output directory: {request.output_directory}'
    }
    
    substituted_template = template.substitute_variables(substitutions)
    return substituted_template.content

def validate_token_count(content: str) -> bool:
    """Check if content token count is within limits"""
    # Simple approximation: tokens are roughly 4 characters each
    approximate_tokens = len(content) / 4
    return approximate_tokens <= 2000

def extract_variables_from_template(content: str) -> List[str]:
    """Extract all {{variable_name}} patterns from template content"""
    import re
    pattern = r'\{\{(\w+)\}\}'
    matches = re.findall(pattern, content)
    return matches
```

### 4.3 Port Definitions

Following the core architecture principles:

```python
# src/core/prp_generation/ports/template_ports.py
from typing import Protocol
from ..models import PRPTemplate

class TemplateLoaderPort(Protocol):
    """Primary port for loading templates - driven by external actor"""
    def load_template(self, path: str) -> PRPTemplate: ...

class PRPGenerationPort(Protocol):
    """Primary port for PRP generation - driven by external actor"""
    def generate_prp(self, request: PRPGenerationRequest) -> PRPGenerationResult: ...

# src/core/prp_generation/ports/generation_ports.py
from typing import Protocol
from ..models import PRPGenerationRequest, PRPGenerationResult

class OutputWriterPort(Protocol):
    """Secondary port for writing output - app drives external system"""
    def write_prp_file(self, content: str, output_path: str) -> bool: ...

class RulesAccessorPort(Protocol):
    """Secondary port for accessing rules - app drives external system"""
    def get_rules_directory_path(self) -> str: ...
```

### 4.4 Orchestrator Implementation

Following the orchestrator pattern:

```python
# src/shell/orchestrators/prp_generation_orchestrator.py
from src.core.prp_generation.models import PRPGenerationRequest, PRPGenerationResult
from src.core.prp_generation.ports.template_ports import TemplateLoaderPort, PRPGenerationPort
from src.core.prp_generation.ports.generation_ports import OutputWriterPort
from src.core.prp_generation.processors import process_prp_template, validate_token_count

class PRPGenerationOrchestrator:
    """Coordinates PRP generation workflow without containing business logic"""

    def __init__(
        self, 
        template_loader: TemplateLoaderPort, 
        output_writer: OutputWriterPort,
        logger
    ):
        # Maximum 4 dependencies enforced by orchestrator pattern
        self.template_loader = template_loader
        self.output_writer = output_writer
        self.logger = logger

    def generate_prp(self, request: PRPGenerationRequest) -> PRPGenerationResult:
        """Orchestrate the complete PRP generation workflow"""
        try:
            # 1. Load the template from file system
            template = self.template_loader.load_template(request.template_path)
            
            # 2. Process the template with business logic (in core)
            processed_content = process_prp_template(template, request)
            
            # 3. Validate token count
            if not validate_token_count(processed_content):
                return PRPGenerationResult(
                    success=False,
                    output_path=None,
                    token_count=len(processed_content) // 4,
                    error_message="Generated PRP exceeds 2000 token limit"
                )
            
            # 4. Generate output filename
            import os
            output_filename = f"{request.prp_id}-spec.md"
            output_path = os.path.join(request.output_directory, output_filename)
            
            # 5. Write the processed content to file
            write_success = self.output_writer.write_prp_file(processed_content, output_path)
            
            if not write_success:
                return PRPGenerationResult(
                    success=False,
                    output_path=None,
                    token_count=len(processed_content) // 4,
                    error_message="Failed to write PRP file to output directory"
                )
            
            return PRPGenerationResult(
                success=True,
                output_path=output_path,
                token_count=len(processed_content) // 4,
                error_message=None
            )
            
        except Exception as e:
            self.logger.error(f"Error during PRP generation: {str(e)}")
            return PRPGenerationResult(
                success=False,
                output_path=None,
                token_count=0,
                error_message=str(e)
            )
```

### 4.5 Adapter Implementations

```python
# src/adapters/template_processing/file_loader.py
import os
from typing import List
from src.core.prp_generation.models import PRPTemplate
from src.core.prp_generation.ports.template_ports import TemplateLoaderPort
from src.core.prp_generation.processors import extract_variables_from_template

class FileSystemTemplateLoader(TemplateLoaderPort):
    """Implementation of template loading from file system"""
    
    def load_template(self, path: str) -> PRPTemplate:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Template file not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        variables = extract_variables_from_template(content)
        template_id = os.path.basename(path).replace('.md', '')
        
        return PRPTemplate(
            id=template_id,
            content=content,
            variables=variables
        )

# src/adapters/mcp_integration/prp_generation_adapter.py
from src.core.prp_generation.models import PRPGenerationRequest
from src.core.prp_generation.ports.template_ports import PRPGenerationPort

class MCPServiceAdapter(PRPGenerationPort):
    """MCP server adapter that handles PRP generation requests"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    
    def generate_prp(self, request: PRPGenerationRequest) -> PRPGenerationResult:
        """Handle MCP request and trigger PRP generation"""
        return self.orchestrator.generate_prp(request)
```

## 5. Implementation Guidelines

### 5.1 Code Standards
- Follow PEP8 for Python code
- Use type hints consistently
- Write docstrings for all functions
- Apply functional programming principles for core logic
- Implement proper error handling in shell layer

### 5.2 Testing Strategy
Following the testing strategy rules:

```python
# tests/unit/test_prp_generation.py
import pytest
from src.core.prp_generation.models import PRPTemplate, PRPGenerationRequest
from src.core.prp_generation.processors import process_prp_template, validate_token_count

def test_process_prp_template_substitutes_variables():
    template = PRPTemplate(
        id="test-template",
        content="This is a {{variable}} in the template",
        variables=["variable"]
    )
    
    request = PRPGenerationRequest(
        user_story="test user story",
        template_path="/template/path",
        rules_directory="/rules/path",
        output_directory="/output/path",
        prp_id="test-id"
    )
    
    result = process_prp_template(template, request)
    
    assert "test user story" in result
    assert "{{variable}}" not in result

def test_validate_token_count_within_limit():
    content = "A" * 8000  # Approximately 2000 tokens
    assert validate_token_count(content) is True

def test_validate_token_count_exceeds_limit():
    content = "A" * 9000  # More than 2000 tokens
    assert validate_token_count(content) is False
```

## 6. Performance Requirements

### 6.1 Response Time
- PRP generation must complete in under 3 seconds
- Template loading should take <500ms
- Variable substitution should take <100ms
- File writing should take <200ms

### 6.2 Memory Usage
- Keep memory usage under 100MB during processing
- Avoid loading unnecessary files into memory
- Use streaming for large template files if needed

## 7. Security Considerations

### 7.1 Input Validation
- Validate all file paths to prevent directory traversal
- Sanitize user story input to prevent injection
- Validate template variable values

### 7.2 File Access
- Ensure proper permissions for reading templates and rules
- Validate output directory write permissions before processing
- Prevent writing to unauthorized directories

## 8. Deployment Considerations

### 8.1 Environment Setup
- Ensure template directory is accessible
- Verify rules directory contains required files
- Validate output directory permissions

### 8.2 Configuration
- Template paths configured through environment variables
- Rules directory path validation during startup
- Output directory creation if it doesn't exist

This technical specification defines the complete implementation of the PRP generation feature following the architectural principles and constraints specified in the project rules.