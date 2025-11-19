from src.core.models.directory_models import DirectoryConfig
from src.core.use_cases.directory_use_cases import (
    validate_directory_config,
    validate_path_security,
)


def prepare_specification_directory_config(output_directory: str = "ctxfy/specifications") -> DirectoryConfig:
    """Prepare directory configuration for storing technical specifications
    
    Args:
        output_directory: Base directory path where specifications will be stored
        
    Returns:
        DirectoryConfig: Configuration for creating the specifications directory
    """
    # Ensure the output directory is secure
    path_validation = validate_path_security(output_directory)
    if not path_validation.is_valid:
        raise ValueError(f"Unsafe output directory path: {path_validation.errors}")
    
    # Split the path to get base path and subdirectories
    path_parts = output_directory.strip('/').split('/')
    base_path = path_parts[0]  # e.g., "ctxfy"
    subdirs = tuple(path_parts[1:]) if len(path_parts) > 1 else ("specifications",)
    
    config = DirectoryConfig(
        base_path=base_path,
        subdirectories=subdirs,
        readme_content="""# Specifications Directory
This directory contains technical specifications generated from business requirements.

## Structure
- All `.md` files in this directory are auto-generated technical specifications
- Each file corresponds to a business requirements translation operation

## Security Notice
This directory and its contents are managed by the ctxfy MCP server.
""",
        validation_rules=("no_traversal", "valid_chars", "safe_path")
    )
    
    # Validate the configuration
    validation_result = validate_directory_config(config)
    if not validation_result.is_valid:
        raise ValueError(f"Invalid directory configuration: {validation_result.errors}")
    
    return config