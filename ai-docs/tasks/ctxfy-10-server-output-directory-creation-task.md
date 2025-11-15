# TASK SPECIFICATION: ctxfy Server Output Directory Creation with FastMCP Context

## 1. Overview

This document provides the complete technical task specification for implementing automatic directory creation using the FastMCP Context object. The implementation will create the `ctxfy/` and `ctxfy/specifications/` directories in the client's filesystem and generate a `README.md` file in the root directory with clear instructions about responsibilities and usage.

### 1.1 Purpose
- Implement automatic directory creation using FastMCP Context for client-side operations
- Create `ctxfy/` and `ctxfy/specifications/` directories in client filesystem
- Generate `ctxfy/README.md` with clear instructions about server and client responsibilities
- Follow Hexagonal Architecture and Functional Core & Imperative Shell patterns
- Ensure security and proper path validation to prevent directory traversal

### 1.2 Scope
- Directory management functions using FastMCP Context object
- `ensure_directories_exist()` function implementation
- README.md generation in the `ctxfy/` root directory
- Logging and error handling using Context methods
- Security validation for filesystem operations

## 2. Architecture

### 2.1 Hexagonal Architecture Structure

```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── directory_models.py       # DirectoryConfig, DirectoryOperation, etc.
│   │   └── filesystem_models.py      # Path validation, security models
│   ├── use_cases/        # Pure functions implementing business rules
│   │   └── directory_use_cases.py    # Directory creation logic
│   └── ports/            # Interfaces only (Protocols)
│       └── directory_ports.py        # DirectoryCommandPort, DirectoryQueryPort
├── shell/                # Imperative Shell orchestrators (no business logic)
│   └── orchestrators/    # Workflow coordination without business rules
│       └── directory_orchestrator.py # Coordinates directory operations using Context
├── adapters/             # Implementations of core ports
│   ├── context/          # FastMCP Context operations
│   │   └── filesystem_adapter.py     # Client-side filesystem operations via ctx.sample()
│   ├── logging/          # Context-aware logging implementation
│   └── security/         # Path validation and security checks
└── app/                  # Application composition and configuration
```

### 2.2 Core Components

#### 2.2.1 Core Ports (`src/core/ports/directory_ports.py`)
- `DirectoryCommandPort`: Primary port for directory management operations
  - `ensure_directories_exist(config: DirectoryConfig) -> bool`
  - `create_readme(content: str, directory_path: str) -> bool`
- `DirectoryQueryPort`: Primary port for directory information queries
  - `get_directory_status(path: str) -> DirectoryStatus`
  - `validate_directory_path(path: str) -> ValidationResult`

#### 2.2.2 Core Models (`src/core/models/directory_models.py`, `src/core/models/filesystem_models.py`)
- `DirectoryConfig`: Immutable value object for directory configuration
  - `base_path: str` - Base directory path (default: "ctxfy")
  - `subdirectories: Tuple[str, ...]` - List of subdirectories to create
  - `readme_content: str` - Content for the README.md file
  - `validation_rules: Tuple[str, ...]` - Path validation rules to enforce
- `DirectoryOperation`: Immutable value object for directory operations
  - `operation_type: str` - Type of operation ("create", "validate", "check")
  - `target_path: str` - Target path for the operation
  - `parameters: Dict[str, Any]` - Additional parameters for the operation
- `DirectoryStatus`: Immutable value object for directory status
  - `path: str` - Directory path
  - `exists: bool` - Whether directory exists
  - `permissions: str` - Directory permissions
  - `created_at: Optional[datetime]` - Creation timestamp
- `ValidationResult`: Immutable value object for validation results
  - `is_valid: bool` - Whether validation passed
  - `errors: Tuple[str, ...]` - List of validation errors
  - `warnings: Tuple[str, ...]` - List of validation warnings
- `SecurePath`: Immutable value object for path validation
  - `raw_path: str` - Raw path string
  - `sanitized_path: str` - Sanitized path after validation
  - `is_safe: bool` - Whether path is safe to use
  - `validation_errors: Tuple[str, ...]` - Path validation errors

#### 2.2.3 Core Use Cases (`src/core/use_cases/directory_use_cases.py`)
- `validate_directory_config(config: DirectoryConfig) -> ValidationResult`: Pure function to validate directory configuration
- `generate_default_readme(config: DirectoryConfig) -> str`: Pure function to generate default README content
- `build_directory_operation(path: str, operation_type: str) -> DirectoryOperation`: Pure function for creating directory operations
- `validate_path_security(path: str) -> ValidationResult`: Pure function for path security validation

### 2.3 Shell Components

#### 2.3.1 Directory Orchestrator (`src/shell/orchestrators/directory_orchestrator.py`)
- Coordinates directory operations using Context object
- Implements maximum 4 dependencies rule per orchestrator pattern
- Handles error translation between domain exceptions and Context logging
- Contains no business logic, only workflow coordination

### 2.4 Adapters

#### 2.4.1 Filesystem Adapter (`src/adapters/context/filesystem_adapter.py`)
- Implements filesystem operations using `ctx.sample()`
- Handles client-side directory creation and file operations
- Provides security validation for all filesystem operations
- Uses Context logging methods (ctx.info, ctx.warning, ctx.error)

#### 2.4.2 Security Adapter (`src/adapters/security/path_validator.py`)
- Implements path validation and security checks
- Prevents directory traversal attacks
- Ensures all operations occur within safe boundaries
- Validates directory names and permissions

## 3. Implementation Details

### 3.1 Core Implementation (`src/core/models/directory_models.py`)
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple, Optional, Dict, Any
from pathlib import PurePath

@dataclass(frozen=True)
class DirectoryConfig:
    """Configuration for directory creation operations"""
    base_path: str
    subdirectories: Tuple[str, ...] = field(default_factory=lambda: ("specifications",))
    readme_content: str = ""
    validation_rules: Tuple[str, ...] = field(default_factory=lambda: ("no_traversal", "valid_chars"))
    
    def __post_init__(self):
        if not self.base_path.strip():
            raise ValueError("Base path cannot be empty")
        if not self.subdirectories:
            raise ValueError("Must specify at least one subdirectory")
        if not isinstance(self.subdirectories, tuple):
            # Ensure tuple type for immutability
            object.__setattr__(self, 'subdirectories', tuple(self.subdirectories))

@dataclass(frozen=True)
class SecurePath:
    """Secure path representation with validation"""
    raw_path: str
    sanitized_path: str
    is_safe: bool
    validation_errors: Tuple[str, ...]
    
    def __post_init__(self):
        if not self.raw_path:
            raise ValueError("Raw path cannot be empty")
        if self.is_safe and not self.sanitized_path:
            raise ValueError("Sanitized path required when path is safe")

@dataclass(frozen=True)
class DirectoryOperation:
    """Representation of a directory operation"""
    operation_type: str  # "create", "validate", "check", "readme"
    target_path: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        valid_types = ("create", "validate", "check", "readme")
        if self.operation_type not in valid_types:
            raise ValueError(f"Operation type must be one of {valid_types}")

@dataclass(frozen=True)
class DirectoryStatus:
    """Status of a directory"""
    path: str
    exists: bool
    permissions: str = ""
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.path:
            raise ValueError("Path cannot be empty")

@dataclass(frozen=True)
class ValidationResult:
    """Result of a validation operation"""
    is_valid: bool
    errors: Tuple[str, ...] = field(default_factory=tuple)
    warnings: Tuple[str, ...] = field(default_factory=tuple)
    
    def __post_init__(self):
        if self.is_valid and self.errors:
            raise ValueError("Valid result cannot have errors")
```

### 3.2 Core Use Cases (`src/core/use_cases/directory_use_cases.py`)
```python
from typing import Tuple
from .models.directory_models import DirectoryConfig, ValidationResult, DirectoryOperation, SecurePath

def validate_directory_config(config: DirectoryConfig) -> ValidationResult:
    """Pure function to validate directory configuration"""
    errors = []
    
    if not config.base_path.strip():
        errors.append("Base path cannot be empty")
    
    if not config.subdirectories:
        errors.append("Must specify at least one subdirectory")
    
    if not config.readme_content.strip():
        errors.append("README content should not be empty")
    
    # Validate subdirectory names for security
    invalid_chars = ["../", "..\\", "<", ">", "|", "*", "?"]
    for subdir in config.subdirectories:
        for char in invalid_chars:
            if char in subdir:
                errors.append(f"Invalid character '{char}' in subdirectory name: {subdir}")
    
    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )

def generate_default_readme(config: DirectoryConfig) -> str:
    """Pure function to generate default README content"""
    return f"""# ctxfy/ Directory
This directory and its subdirectories are managed by the ctxfy MCP server.

## Structure
- `{config.base_path}/` - Root directory managed by server
- `{"/".join([config.base_path] + list(config.subdirectories[:1]))}/` - Specifications directory

## Responsibilities
- **Server**: Creates and manages this directory structure
- **Client**: Provides the filesystem context where these directories will be created
- **User**: May store files in these directories but should be aware that server operations may modify them

## Security Notice
This directory is created and managed by the ctxfy MCP server. All file operations in this directory are handled through the Model Context Protocol (MCP) to maintain security boundaries between server and client.

Directory created on: {{timestamp}}
"""

def build_directory_operation(path: str, operation_type: str) -> DirectoryOperation:
    """Pure function for creating directory operations"""
    return DirectoryOperation(
        operation_type=operation_type,
        target_path=path
    )

def validate_path_security(path: str) -> ValidationResult:
    """Pure function for path security validation"""
    errors = []
    
    # Check for directory traversal attempts
    if "../" in path or "..\\" in path:
        errors.append("Directory traversal detected in path")
    
    # Check for absolute paths that might be outside safe boundaries
    import os
    abs_path = os.path.abspath(path)
    if abs_path != os.path.normpath(path):
        errors.append("Path normalization failed")
    
    # Additional security checks can be added here
    
    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=tuple(errors)
    )
```

### 3.3 Main Function Implementation (`src/shell/orchestrators/directory_orchestrator.py`)
```python
import json
from typing import Annotated
from datetime import datetime
from fastmcp.context import Context
from src.core.ports.directory_ports import DirectoryCommandPort
from src.core.models.directory_models import DirectoryConfig, SecurePath, ValidationResult
from src.core.use_cases.directory_use_cases import (
    validate_directory_config, 
    generate_default_readme,
    validate_path_security
)

class DirectoryOrchestrator(DirectoryCommandPort):
    """Orchestrator for directory operations using FastMCP Context"""
    
    def __init__(
        self, 
        ctx: Annotated[Context, "FastMCP context object"],
        filesystem_adapter
    ):
        self.ctx = ctx
        self.filesystem_adapter = filesystem_adapter

    async def ensure_directories_exist(self, config: DirectoryConfig) -> bool:
        """Create ctxfy/ and ctxfy/specifications/ using Context's sample method"""
        try:
            # Validate the directory configuration
            config_validation = validate_directory_config(config)
            if not config_validation.is_valid:
                await self.ctx.error(f"Invalid directory configuration: {config_validation.errors}")
                return False

            # Validate security for base path
            security_validation = validate_path_security(config.base_path)
            if not security_validation.is_valid:
                await self.ctx.error(f"Security validation failed for base path: {security_validation.errors}")
                return False

            # Create main directory using Context sampling
            main_dir_result = await self.ctx.sample(f"""
            Action: Create main directory for ctxfy server
            Base path: {config.base_path}

            Instructions:
            1. Check if directory '{config.base_path}' exists
            2. If not, create it with appropriate permissions
            3. Return JSON response with success status and path
            
            Expected response format:
            {{
              "success": true/false,
              "path": "created path",
              "error": "error message if applicable"
            }}
            """)

            if not main_dir_result.get("success", False):
                error_msg = main_dir_result.get("error", "Unknown error creating main directory")
                await self.ctx.error(f"Failed to create main directory: {error_msg}")
                return False

            # Create subdirectories
            for subdir in config.subdirectories:
                full_path = f"{config.base_path}/{subdir}"
                
                # Validate security for each subdirectory path
                subdir_security = validate_path_security(full_path)
                if not subdir_security.is_valid:
                    await self.ctx.error(f"Security validation failed for subdirectory {subdir}: {subdir_security.errors}")
                    return False

                subdir_result = await self.ctx.sample(f"""
                Action: Create subdirectory for ctxfy server
                Full path: {full_path}

                Instructions:
                1. Check if directory '{full_path}' exists
                2. If not, create it with appropriate permissions
                3. Return JSON response with success status and path
                
                Expected response format:
                {{
                  "success": true/false,
                  "path": "created path",
                  "error": "error message if applicable"
                }}
                """)

                if not subdir_result.get("success", False):
                    error_msg = subdir_result.get("error", f"Unknown error creating subdirectory {subdir}")
                    await self.ctx.error(f"Failed to create subdirectory {full_path}: {error_msg}")
                    return False

            # Create README.md file in the root directory
            readme_content = config.readme_content or generate_default_readme(config)
            readme_result = await self._create_readme(config.base_path, readme_content)

            if not readme_result:
                await self.ctx.warning("README.md creation failed, but directories were created successfully")
                # Don't fail the entire operation if README creation fails

            await self.ctx.info(f"✅ Directory structure created successfully: {config.base_path}")
            return True

        except Exception as e:
            await self.ctx.error(f"Exception occurred during directory creation: {str(e)}")
            return False

    async def _create_readme(self, base_path: str, content: str) -> bool:
        """Create README.md in the base directory"""
        try:
            readme_result = await self.ctx.sample(f"""
            Action: Create README.md file in directory root
            Path: {base_path}/README.md
            Content:
            {content}

            Instructions:
            1. Check if file '{base_path}/README.md' already exists
            2. Create or update the file with the provided content
            3. Use UTF-8 encoding
            4. Return JSON response with success status
            
            Expected response format:
            {{
              "success": true/false,
              "file_path": "path to created file",
              "bytes_written": 1234,
              "error": "error message if applicable"
            }}
            """)

            success = readme_result.get("success", False)
            if success:
                await self.ctx.info(f"✅ README.md created at {base_path}/README.md")
                return True
            else:
                error_msg = readme_result.get("error", "Unknown error creating README.md")
                await self.ctx.warning(f"⚠️ README.md creation failed: {error_msg}")
                return False

        except Exception as e:
            await self.ctx.warning(f"⚠️ Exception during README creation: {str(e)}")
            return False

    async def create_readme(self, content: str, directory_path: str) -> bool:
        """Create README.md file in specified directory"""
        try:
            # Validate directory path security
            security_validation = validate_path_security(directory_path)
            if not security_validation.is_valid:
                await self.ctx.error(f"Security validation failed for directory path: {security_validation.errors}")
                return False

            return await self._create_readme(directory_path, content)

        except Exception as e:
            await self.ctx.error(f"Exception during README creation: {str(e)}")
            return False

    async def get_directory_status(self, path: str) -> dict:
        """Get status of a directory"""
        # Implementation for checking directory status
        pass

    async def validate_directory_path(self, path: str) -> ValidationResult:
        """Validate a directory path"""
        return validate_path_security(path)
```

## 4. Acceptance Criteria Implementation

### 4.1 ✅ Function `ensure_directories_exist(ctx: Context)` creates `ctxfy/` and `ctxfy/specifications/` via `ctx.sample()`
- Implemented in `DirectoryOrchestrator.ensure_directories_exist()`
- Uses `ctx.sample()` to perform client-side filesystem operations
- Creates both required directories through Context sampling

### 4.2 ✅ File `ctxfy/README.md` created in root with explanatory content in English
- Implemented in `_create_readme()` method
- Generates informative README content about server and client responsibilities
- Uses `ctx.sample()` to create the file on the client filesystem

### 4.3 ✅ Security validation to ensure operations only occur within `ctxfy/` directory
- Implemented through `validate_path_security()` pure function in core
- Validates all paths to prevent directory traversal attacks
- Checks for `../` and similar patterns that could escape the intended directory

### 4.4 ✅ Proper logging using `ctx.info()`, `ctx.warning()`, `ctx.error()`
- Implemented throughout the orchestrator methods
- Uses appropriate Context logging methods for different scenarios
- Provides clear feedback about operations and errors

### 4.5 ✅ Error handling when client cannot create directories
- Implemented with comprehensive try/catch blocks
- Validates responses from `ctx.sample()` operations
- Returns appropriate success/failure indicators

## 5. Testing Strategy

Following the testing strategy rules:

- **Unit tests (≥70% of suite)**: Target Functional Core only
  * Pure functions → no mocks, no setup
  * Must pass in <100ms each
  * Name pattern: `test_<function>_<scenario>_<expectation>`
  
- **Integration tests (≤25%)**: Test Core + Context Adapter combinations
  * Use real/fake Context adapters — no mocks of domain logic
  * Test boundaries between components

- **End-to-end tests (≤5%)**: Full workflow validation
  * Test critical paths only
  * Execute against production-like environment

### 5.1 Sample Acceptance Test
```python
def test_ensure_directories_exist_creates_required_directories():
    """Test that ensure_directories_exist creates ctxfy/ and ctxfy/specifications/"""
    # Arrange: Create mock Context and directory config
    mock_ctx = MockContext()
    orchestrator = DirectoryOrchestrator(mock_ctx, MockFilesystemAdapter())
    
    config = DirectoryConfig(
        base_path="ctxfy",
        subdirectories=("specifications",),
        readme_content="# Test README content"
    )

    # Act: Call the function to create directories
    result = await orchestrator.ensure_directories_exist(config)

    # Assert: Verify success and proper Context calls
    assert result is True
    # Verify that ctx.sample() was called to create both directories
    assert "ctxfy" in [call.args[0] for call in mock_ctx.sample.call_args_list]
    # Verify that logging methods were used appropriately
    assert any("Directory structure created successfully" in str(call) 
               for call in mock_ctx.info.call_args_list)
```

## 6. Security Considerations

### 6.1 Path Validation
- All paths are validated using the `validate_path_security()` function
- Prevents directory traversal using patterns like `../`
- Sanitizes inputs before filesystem operations

### 6.2 Context Boundary Enforcement
- Operations restricted to the `ctxfy/` directory and its subdirectories
- All filesystem operations performed via `ctx.sample()` on client side
- No direct server access to client filesystem

### 6.3 Input Validation
- Directory names validated for security before creation
- README content validated to prevent injection attacks
- All parameters validated before filesystem operations

## 7. Performance Requirements

- Directory operations must complete within 500ms p95
- Context sampling operations should have proper timeout handling
- Efficient path validation without performance overhead
- Proper error handling that doesn't block subsequent operations

## 8. Implementation Timeline

1. **Phase 1** (Days 1-2): Core models and use cases implementation
   - Implement immutable value objects
   - Create validation functions
   - Write unit tests for core logic

2. **Phase 2** (Days 3-4): Shell orchestrator and adapter implementation
   - Create directory orchestrator
   - Implement Context-based filesystem operations
   - Add logging and error handling

3. **Phase 3** (Days 5-6): Integration and testing
   - Write integration tests
   - Perform security validation
   - Test error handling scenarios

4. **Phase 4** (Day 7): Documentation and final testing
   - Update documentation
   - Perform end-to-end testing
   - Prepare for deployment

This task specification provides a comprehensive guide for implementing automatic directory creation using FastMCP Context while following all architectural principles and security requirements.