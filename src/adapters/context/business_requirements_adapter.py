import json
from typing import Annotated, Tuple

from fastmcp import Context

from src.adapters.security.business_requirements_security import (
    build_secure_output_path,
    sanitize_requirements_text,
    validate_business_requirements_security,
    validate_specification_content,
)
from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
    TechnicalSpecification,
    TranslationResult,
    TranslationStatus,
)
from src.core.models.validation_models import ValidationError, ValidationResult
from src.core.ports.business_requirements_ports import (
    BusinessRequirementsCommandPort,
    BusinessRequirementsQueryPort,
)


class BusinessRequirementsAdapter(BusinessRequirementsCommandPort, BusinessRequirementsQueryPort):
    """Implementation of business requirements ports using FastMCP Context"""

    def __init__(self, ctx: Annotated[Context, "FastMCP context object"]):
        self.ctx = ctx

    async def translate_business_requirements(self, config: BusinessRequirementConfig) -> TranslationResult:
        """Translate business requirements into technical specifications using Context"""
        try:
            # Validate security for requirements and output path
            security_validation = validate_business_requirements_security(
                config.requirements_text,
                config.output_directory
            )
            if not security_validation.is_valid:
                error_messages = tuple(error.message for error in security_validation.errors)
                await self.ctx.error(f"Security validation failed: {error_messages}")
                return TranslationResult(
                    success=False,
                    errors=error_messages
                )

            # Sanitize requirements text
            sanitized_requirements_text = sanitize_requirements_text(config.requirements_text)

            # Prepare the prompt for LLM with sanitized text
            prompt = f"Convert the following business requirements into a detailed technical specification:\n\n{sanitized_requirements_text}\n\nProvide a comprehensive technical specification with implementation details, system architecture, API endpoints, data models, security considerations, and testing strategy."

            result = await self.ctx.sample({
                "prompt": prompt,
                "description": "Translate business requirements to technical specification",
                "model_preferences": {
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
            })  # type: ignore[arg-type]

            # Handle the result from ctx.sample - could be string or dict
            if isinstance(result, str):
                # If it's already a string, use it directly as the content
                technical_content = result
            elif isinstance(result, dict):
                # If it's a dict, extract the content
                technical_content = result.get("content", result.get("text", str(result)))
            else:
                # For any other type, convert to string
                technical_content = str(result)

            # Validate the generated specification content for security
            content_validation = validate_specification_content(technical_content)
            if not content_validation.is_valid:
                error_messages = tuple(error.message for error in content_validation.errors)
                await self.ctx.error(f"Specification content validation failed: {error_messages}")
                return TranslationResult(
                    success=False,
                    errors=error_messages
                )

            # Create the technical specification
            specification = TechnicalSpecification(
                content=technical_content,
                format="SPEC"
            )

            # Store the specification in the filesystem
            success = await self.store_technical_specification(specification, config.output_directory)

            if success:
                return TranslationResult(
                    success=True,
                    specification=specification
                )
            else:
                return TranslationResult(
                    success=False,
                    errors=("Failed to store technical specification",)
                )

        except Exception as e:
            await self.ctx.error(f"Error translating business requirements: {str(e)}")
            return TranslationResult(
                success=False,
                errors=(f"Error in translation: {str(e)}",)
            )

    async def generate_technical_specification(self, requirements: BusinessRequirements) -> TechnicalSpecification:
        """Generate technical specification from parsed business requirements using Context"""
        try:
            # Sanitize requirements content
            sanitized_content = sanitize_requirements_text(requirements.content)

            prompt = f"Create a detailed technical specification based on these business requirements:\n\n{sanitized_content}\n\nInclude system architecture, implementation details, data models, security considerations, and testing approach."

            result = await self.ctx.sample({
                "prompt": prompt,
                "description": f"Generate technical specification for requirements ID: {requirements.id}",
                "model_preferences": {
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
            })  # type: ignore[arg-type]

            # Parse the result from ctx.sample
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {result}")
                    # Return a default specification with error details
                    return TechnicalSpecification(
                        content="Error generating specification: Could not parse LLM response",
                        format="SPEC"
                    )

            # Extract the technical specification content from result
            if isinstance(result, dict):
                technical_content = result.get("content", result.get("text", str(result)))
            else:
                technical_content = str(result)

            # Validate the generated specification content for security
            content_validation = validate_specification_content(technical_content)
            if not content_validation.is_valid:
                error_messages = tuple(error.message for error in content_validation.errors)
                await self.ctx.error(f"Generated specification content validation failed: {error_messages}")
                # Return a specification with validation error details
                return TechnicalSpecification(
                    content=f"Specification rejected for security reasons: {error_messages}",
                    format="SPEC"
                )

            return TechnicalSpecification(
                content=technical_content,
                format="SPEC",
                source_requirements_id=requirements.id
            )

        except Exception as e:
            await self.ctx.error(f"Error generating technical specification: {str(e)}")
            return TechnicalSpecification(
                content=f"Error generating specification: {str(e)}",
                format="SPEC"
            )

    async def store_technical_specification(self, specification: TechnicalSpecification, output_path: str) -> bool:
        """Store generated technical specification to filesystem using Context"""
        try:
            # Build secure output path
            spec_filename = f"spec_{specification.spec_id[:8]}.md"
            try:
                secure_output_path = build_secure_output_path(output_path, spec_filename)
            except ValueError as e:
                await self.ctx.error(f"Failed to build secure output path: {str(e)}")
                return False

            # Use the filesystem adapter via Context to write the file
            result = await self.ctx.sample({
                "action": "write_file",
                "path": secure_output_path,
                "content": specification.content,
                "description": f"Store technical specification: {specification.spec_id}"
            })  # type: ignore[arg-type]

            # Parse the result from ctx.sample
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    await self.ctx.error(f"Could not parse result from ctx.sample: {result}")
                    return False

            success_val = result.get("success", result.get("written", False))  # type: ignore[union-attr]
            return success_val

        except Exception as e:
            await self.ctx.error(f"Error storing technical specification {output_path}: {str(e)}")
            return False

    async def get_translation_status(self, translation_id: str) -> TranslationStatus:
        """Get the current status of a translation operation using Context"""
        try:
            # For this implementation, we'll return a completed status
            # In a real system, this would track actual ongoing operations
            return TranslationStatus(
                translation_id=translation_id,
                status="completed",
                progress=1.0
            )
        except Exception as e:
            await self.ctx.error(f"Error getting translation status: {str(e)}")
            return TranslationStatus(
                translation_id=translation_id,
                status="failed",
                progress=0.0
            )

    async def validate_requirements(self, requirements: BusinessRequirements) -> ValidationResult:
        """Validate business requirements against defined rules using Context"""
        try:
            # This validation would typically be done in core logic
            # Using Context here for logging purposes
            errors = []

            if len(requirements.content.strip()) < 10:
                errors.append(ValidationError(
                    field="content",
                    message="Business requirements content too short, minimum 10 characters",
                    code="CONTENT_TOO_SHORT"
                ))

            # Validate context
            if not isinstance(requirements.context, dict):
                errors.append(ValidationError(
                    field="context",
                    message="Context must be a dictionary",
                    code="INVALID_CONTEXT_TYPE"
                ))

            # Validate metadata
            if not isinstance(requirements.metadata, dict):
                errors.append(ValidationError(
                    field="metadata",
                    message="Metadata must be a dictionary",
                    code="INVALID_METADATA_TYPE"
                ))

            # Check for potentially sensitive information
            sensitive_indicators = ["password", "secret", "key", "token", "credential"]
            content_lower = requirements.content.lower()
            for indicator in sensitive_indicators:
                if indicator in content_lower:
                    errors.append(ValidationError(
                        field="content",
                        message=f"Potentially sensitive information detected: {indicator}",
                        code="SENSITIVE_INFO_DETECTED"
                    ))

            is_valid = len(errors) == 0

            if not is_valid:
                error_messages = [error.message for error in errors]
                await self.ctx.log(f"Validation failed for requirements {requirements.id}: {error_messages}")

            return ValidationResult(
                is_valid=is_valid,
                errors=tuple(errors)
            )

        except Exception as e:
            await self.ctx.error(f"Error validating requirements: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=(ValidationError(
                    field="validation",
                    message=f"Error in validation: {str(e)}",
                    code="VALIDATION_ERROR"
                ),)
            )

    async def list_translations(self, limit: int = 10) -> Tuple[str, ...]:
        """List recent translation operations using Context"""
        try:
            # This is a simplified implementation - in a real system, 
            # this would query a database or filesystem to get actual translation IDs
            # For now, we return an empty tuple since we're not tracking operations yet
            await self.ctx.log(f"Requested list of translations (limit: {limit})")
            return ()
        except Exception as e:
            await self.ctx.error(f"Error listing translations: {str(e)}")
            return ()