# TASK SPECIFICATION: Business Requirements Translation System with FastMCP Context

## 1. Overview

This document provides the complete technical task specification for implementing a business requirements translation system using FastMCP Context object. The implementation will create a function that translates business requirements into technical specifications following Hexagonal Architecture and Functional Core principles.

### 1.1 Purpose
- Implement `translate_business_requirements` function using FastMCP Context for client-side operations
- Reuse existing security, validation, and filesystem components from previous tasks
- Follow Hexagonal Architecture patterns with proper separation of concerns
- Ensure security and proper path validation to prevent directory traversal

### 1.2 Scope
- Business requirements translation using FastMCP Context object
- Integration with existing directory management and filesystem components
- Reuse of security and validation components
- Implementation following Functional Core and Imperative Shell patterns
- Generation of technical specifications in the ctxfy directory

## 2. Architecture

### 2.1 Hexagonal Architecture Structure

```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── directory_models.py        # (existing) DirectoryConfig, DirectoryOperation, etc.
│   │   ├── filesystem_models.py       # (existing) Path validation, security models
│   │   └── business_requirements_models.py  # NEW: Business requirements models
│   ├── use_cases/        # Pure functions implementing business rules
│   │   ├── directory_use_cases.py     # (existing) Directory creation logic
│   │   └── business_requirements_use_cases.py  # NEW: Business requirements translation logic
│   └── ports/            # Interfaces only (Protocols)
│       ├── directory_ports.py         # (existing) DirectoryCommandPort, DirectoryQueryPort
│       └── business_requirements_ports.py     # NEW: Business requirements ports
├── shell/                # Imperative Shell orchestrators (no business logic)
│   └── orchestrators/    # Workflow coordination without business rules
│       ├── directory_orchestrator.py  # (existing) Coordinates directory operations using Context
│       └── business_requirements_orchestrator.py # NEW: Coordinates business requirements operations
├── adapters/             # Implementations of core ports
│   ├── context/          # FastMCP Context operations
│   │   ├── filesystem_adapter.py      # (existing) Client-side filesystem operations via ctx.sample()
│   │   └── business_requirements_adapter.py  # NEW: Business requirements adapter reusing filesystem
│   ├── security/         # (existing) Path validation and security checks
│   └── validation/       # (existing) Schema validation for requirements
└── app/                  # Application composition and configuration
```

### 2.2 Core Components

#### 2.2.1 Core Ports (`src/core/ports/business_requirements_ports.py`)
- `BusinessRequirementsCommandPort`: Primary port for business requirements operations
  - `translate_business_requirements(config: BusinessRequirementConfig) -> TranslationResult`
  - `generate_technical_specification(requirements: BusinessRequirements) -> TechnicalSpecification`
- `BusinessRequirementsQueryPort`: Primary port for business requirements information queries
  - `get_translation_status(translation_id: str) -> TranslationStatus`
  - `validate_requirements(requirements: BusinessRequirements) -> ValidationResult`

#### 2.2.2 Core Models (`src/core/models/business_requirements_models.py`)
- `BusinessRequirementConfig`: Immutable value object for business requirements configuration
  - `requirements_text: str` - Raw business requirements text to translate
  - `output_directory: str` - Directory to store generated specifications (default: "ctxfy/specifications")
  - `security_context: Dict[str, Any]` - Security context for operations
  - `validation_rules: Tuple[str, ...]` - Validation rules to enforce
- `BusinessRequirements`: Immutable value object for parsed business requirements
  - `id: str` - Unique identifier for requirements set
  - `content: str` - Parsed and validated requirements content
  - `context: Dict[str, Any]` - Context information for requirements
  - `metadata: Dict[str, Any]` - Additional metadata about requirements
- `TechnicalSpecification`: Immutable value object for generated technical specifications
  - `spec_id: str` - Unique identifier for specification
  - `content: str` - Technical specification content
  - `format: str` - Specification format (e.g., "PRP", "TASK", "SPEC")
  - `generated_at: datetime` - Timestamp of generation
- `TranslationResult`: Immutable value object for translation results
  - `success: bool` - Whether translation was successful
  - `specification: Optional[TechnicalSpecification]` - Generated specification if successful
  - `errors: Tuple[str, ...]` - Errors encountered during translation
  - `warnings: Tuple[str, ...]` - Warnings during translation

## 3. Implementation Details

### 3.1 Reuse of Existing Components

This implementation will reuse the following components from existing tasks:

✅ **Security Components**:
- Use `validate_path_security()` from `src.core.use_cases.directory_use_cases` for all path validations
- Use `SecurePath` from `src.core.models.filesystem_models` for secure path representation
- Use `ValidationResult` for consistent validation results
- Implement directory traversal prevention using existing mechanisms

✅ **Infrastructure and Adapters**:
- Use `FilesystemAdapter` from `src/adapters/context/filesystem_adapter` for all filesystem operations
- Use `DirectoryCommandPort` from `src/core/ports/directory_ports` for directory operations
- Use `PathValidator` from security modules for path validation
- Integrate with same logging mechanism using `ctx.info()`, `ctx.warning()`, `ctx.error()`

✅ **Models and Value Objects**:
- Use `DirectoryConfig` for consistent directory configuration
- Use `DirectoryOperation` to represent directory operations
- Use `ValidationResult` for standardized validation results
- Create new value objects following same immutability pattern (`@dataclass(frozen=True)`)

### 3.2 Core Implementation (`src/core/use_cases/business_requirements_use_cases.py`)

```python
from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
    TechnicalSpecification,
    TranslationResult
)
from src.core.models.directory_models import DirectoryConfig, ValidationResult
from src.core.use_cases.directory_use_cases import validate_path_security

def validate_business_requirements_config(config: BusinessRequirementConfig) -> ValidationResult:
    """Pure function to validate business requirements configuration"""
    errors = []
    
    if not config.requirements_text.strip():
        errors.append("Requirements text cannot be empty")
    
    path_validation = validate_path_security(config.output_directory)
    if not path_validation.is_valid:
        errors.extend(path_validation.errors)
    
    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )

def parse_business_requirements(text: str) -> BusinessRequirements:
    """Pure function to parse business requirements into structured format"""
    # Implementation to parse business requirements
    return BusinessRequirements(
        id="REQ_" + str(hash(text))[:8],  # Simple ID generation
        content=text,
        context={},
        metadata={}
    )

def generate_technical_specification(requirements: BusinessRequirements) -> TechnicalSpecification:
    """Pure function to generate technical specification from business requirements"""
    # Implementation to convert business requirements to technical specification
    # This would typically involve translating business language to technical implementation details
    
    spec_content = f"""# TECHNICAL SPECIFICATION: {requirements.id}

## Business Requirements
{requirements.content}

## Technical Implementation
Based on the business requirements, the following technical implementation is recommended:

### Architecture
- Follow Hexagonal Architecture patterns
- Implement Functional Core & Imperative Shell
- Use immutable value objects
- Ensure proper separation of concerns

### Implementation Notes
- Reuse existing validation and security components
- Integrate with existing directory management
- Follow project coding standards and conventions

### Dependencies
- FastMCP Context for client-side operations
- Existing security and validation components
- Directory management functionality

## Validation
- All paths must pass security validation
- Output must match technical specification format
- Generated artifacts must be properly stored in ctxfy directory
"""
    
    return TechnicalSpecification(
        spec_id=f"SPEC_{requirements.id}",
        content=spec_content,
        format="PRP",
        generated_at=datetime.now()
    )

def translate_business_requirements(config: BusinessRequirementConfig) -> TranslationResult:
    """Pure function to translate business requirements to technical specifications"""
    # Validate configuration
    validation_result = validate_business_requirements_config(config)
    if not validation_result.is_valid:
        return TranslationResult(
            success=False,
            specification=None,
            errors=validation_result.errors,
            warnings=()
        )
    
    # Parse requirements
    requirements = parse_business_requirements(config.requirements_text)
    
    # Generate specification
    specification = generate_technical_specification(requirements)
    
    return TranslationResult(
        success=True,
        specification=specification,
        errors=(),
        warnings=()
    )
```

### 3.3 Shell Orchestrator (`src/shell/orchestrators/business_requirements_orchestrator.py`)

```python
import json
from datetime import datetime
from typing import Any

from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
    TechnicalSpecification
)
from src.core.models.directory_models import DirectoryConfig
from src.core.use_cases.business_requirements_use_cases import (
    translate_business_requirements,
    validate_business_requirements_config
)
from src.core.use_cases.directory_use_cases import validate_path_security
from src.core.models.filesystem_models import FilesystemOperation, FileOperationResult


class BusinessRequirementsOrchestrator:
    """Orchestrator for business requirements translation using FastMCP Context implementing the Imperative Shell pattern."""

    def __init__(
        self,
        ctx: Any,
        filesystem_adapter: Any,
        directory_orchestrator: Any
    ) -> None:
        if len(locals()) > 4:  # self + 3 dependencies
            raise ValueError("Orchestrator should have maximum 3 dependencies (4 including self)")

        self.ctx = ctx
        self.filesystem_adapter = filesystem_adapter
        self.directory_orchestrator = directory_orchestrator

    async def translate_business_requirements(self, config: BusinessRequirementConfig) -> bool:
        """Translate business requirements to technical specifications using Context"""
        try:
            await self.ctx.info(f"Starting business requirements translation for: {config.requirements_text[:50]}...")
            
            # Validate the business requirements configuration
            config_validation = validate_business_requirements_config(config)
            if not config_validation.is_valid:
                await self.ctx.error(f"Invalid business requirements configuration: {config_validation.errors}")
                return False

            # Validate security for output directory
            security_validation = validate_path_security(config.output_directory)
            if not security_validation.is_valid:
                await self.ctx.error(f"Security validation failed for output directory: {security_validation.errors}")
                return False

            # Use core function to perform the translation
            from src.core.use_cases.business_requirements_use_cases import translate_business_requirements
            translation_result = translate_business_requirements(config)
            
            if not translation_result.success:
                await self.ctx.error(f"Translation failed: {translation_result.errors}")
                return False
                
            if not translation_result.specification:
                await self.ctx.error("Translation completed but no specification was generated")
                return False

            # Ensure the output directory exists using existing directory orchestrator
            dir_config = DirectoryConfig(
                base_path=config.output_directory,
                subdirectories=()
            )
            dir_exists = await self.directory_orchestrator.ensure_directories_exist(dir_config)
            if not dir_exists:
                await self.ctx.error(f"Failed to ensure output directory exists: {config.output_directory}")
                return False

            # Write the technical specification to file
            spec_filename = f"{translation_result.specification.spec_id}.md"
            spec_path = f"{config.output_directory}/{spec_filename}"
            
            write_result = await self.filesystem_adapter.write_file(spec_path, translation_result.specification.content)
            if not write_result:
                await self.ctx.error(f"Failed to write technical specification to: {spec_path}")
                return False

            await self.ctx.info(f"Successfully translated business requirements to technical specification: {spec_path}")
            return True

        except Exception as e:
            await self.ctx.error(f"Unexpected error in translate_business_requirements: {str(e)}")
            return False

    async def process_requirements_with_context(self, business_requirements: str, ctx_context: Any) -> bool:
        """Process business requirements with additional context information"""
        try:
            # Create configuration with context information
            config = BusinessRequirementConfig(
                requirements_text=business_requirements,
                output_directory="ctxfy/specifications",
                security_context={"origin": "user_input", "timestamp": datetime.now().isoformat()},
                validation_rules=("no_traversal", "valid_chars", "content_security")
            )
            
            # Perform the translation
            return await self.translate_business_requirements(config)
            
        except Exception as e:
            await self.ctx.error(f"Error processing requirements with context: {str(e)}")
            return False
```

### 3.4 FastMCP Integration (`src/adapters/context/business_requirements_adapter.py`)

```python
from typing import Annotated

from fastmcp import Context

from src.core.ports.business_requirements_ports import BusinessRequirementsCommandPort
from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    TranslationResult
)


class BusinessRequirementsAdapter(BusinessRequirementsCommandPort):
    """Implementation of business requirements operations using FastMCP Context"""

    def __init__(self, ctx: Annotated[Context, "FastMCP context object"]):
        self.ctx = ctx
        # Note: Dependencies for filesystem operations will be passed through the orchestrator

    async def translate_business_requirements(self, config: BusinessRequirementConfig) -> TranslationResult:
        """Translate business requirements using Context sampling"""
        # This adapter will coordinate with the orchestrator that handles the actual implementation
        # Implementation will be handled by the shell orchestrator
        raise NotImplementedError("This method should be implemented through the orchestrator pattern")
```

### 3.5 Project Dependencies (`pyproject.toml`)

No additional dependencies required beyond existing FastMCP setup from previous tasks.

### 3.6 Testing Requirements

#### 3.6.1 Unit Tests (≥70% of suite)
- Test core business requirements translation functions in isolation
- Validate security checks and path validation functions
- Test value object creation and validation

#### 3.6.2 Integration Tests (≤25%)
- Test orchestrator integration with filesystem adapter
- Validate end-to-end business requirements translation flow
- Test directory creation and file writing integration

#### 3.6.3 End-to-End Tests (≤5%)
- Full workflow validation of business requirements to technical specification generation
- Test with actual FastMCP context in realistic environment

## 4. Security Considerations

### 4.1 Path Security
- All paths must pass security validation using existing `validate_path_security` function
- Prevent directory traversal attacks using existing security mechanisms
- Validate output directory paths before any filesystem operations

### 4.2 Content Security
- Validate business requirements content for malicious content
- Sanitize generated technical specifications before file writing
- Implement content filtering if necessary based on requirements

### 4.3 Context Security
- Operations will be performed through FastMCP Context to maintain security boundaries
- Client-side operations only through `ctx.sample()` method
- No direct filesystem access from server side

## 5. Performance Requirements

### 5.1 Execution Time
- Business requirements translation should complete in <500ms
- Individual validation operations should complete in <100ms
- File writing operations should complete in <200ms

### 5.2 Resource Usage
- Memory usage should be proportional to input size
- No unnecessary caching of intermediate results
- Efficient stream processing for large requirements documents

## 6. Validation and Quality Assurance

### 6.1 Input Validation
- All business requirements must be validated before processing
- Path validation must pass security checks
- Content validation for format and structure

### 6.2 Output Validation
- Generated technical specifications must match required format
- File writing operations must be verified for completeness
- Directory structure must be validated after creation

## 7. Implementation Plan

### 7.1 Phase 1: Core Models and Use Cases
1. Create `business_requirements_models.py` with all required value objects
2. Implement core use case functions for business requirements translation
3. Write unit tests for all core functions

### 7.2 Phase 2: Shell Implementation
1. Create business requirements orchestrator that reuses existing components
2. Implement adapter integration with FastMCP Context
3. Add integration tests for orchestrator functionality

### 7.3 Phase 3: Integration and Testing
1. Integrate with existing directory and filesystem components
2. Implement end-to-end tests
3. Performance and security validation
4. Documentation and deployment

## 8. Success Criteria

- Business requirements can be successfully translated to technical specifications
- All security validations pass before any filesystem operations
- Generated specifications follow required format and structure
- Implementation follows Hexagonal Architecture and Functional Core principles
- All existing components are properly reused without duplication
- Performance requirements are met
- Comprehensive test coverage (>80% for critical paths)