import time
from typing import Any

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
from src.core.use_cases.business_requirements_use_cases import (
    parse_business_requirements,
    validate_business_requirements,
    validate_translation_config,
)


class BusinessRequirementsOrchestrator:
    """Orchestrator for business requirements operations using FastMCP Context implementing the Imperative Shell pattern."""

    def __init__(
        self,
        ctx: Any,
        filesystem_adapter: Any
    ) -> None:
        if len(locals()) > 3:  # self + 2 dependencies
            raise ValueError("Orchestrator should have maximum 2 dependencies (3 including self)")

        self.ctx = ctx
        self.filesystem_adapter = filesystem_adapter

    async def translate_business_requirements(self, config: BusinessRequirementConfig) -> TranslationResult:
        """Main orchestrator function to translate business requirements using FastMCP Context"""
        start_time = time.time()

        try:
            # Validate the translation configuration
            config_validation = validate_translation_config(config)
            if not config_validation.is_valid:
                error_messages = tuple(error.message for error in config_validation.errors)
                await self.ctx.error(f"Invalid translation configuration: {error_messages}")
                return TranslationResult(
                    success=False,
                    errors=error_messages,
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Additional security validation for requirements and output path
            security_validation = validate_business_requirements_security(
                config.requirements_text,
                config.output_directory
            )
            if not security_validation.is_valid:
                error_messages = tuple(error.message for error in security_validation.errors)
                await self.ctx.error(f"Security validation failed: {error_messages}")
                return TranslationResult(
                    success=False,
                    errors=error_messages,
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Sanitize requirements text
            sanitized_requirements_text = sanitize_requirements_text(config.requirements_text)

            # Parse the business requirements from config using sanitized text
            requirements = parse_business_requirements(
                BusinessRequirementConfig(
                    requirements_text=sanitized_requirements_text,
                    output_directory=config.output_directory,
                    security_context=config.security_context,
                    validation_rules=config.validation_rules
                )
            )

            # Validate the parsed business requirements
            req_validation = validate_business_requirements(requirements)
            if not req_validation.is_valid:
                error_messages = tuple(error.message for error in req_validation.errors)
                await self.ctx.error(f"Business requirements validation failed: {error_messages}")
                return TranslationResult(
                    success=False,
                    errors=error_messages,
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Use Context to call LLM for translation (simulated through ctx.sample)
            llm_prompt = f"Convert the following business requirements into a technical specification:\n\n{requirements.content}\n\nFormat as a structured technical specification."

            llm_result = await self.ctx.sample({
                "prompt": llm_prompt,
                "description": "Translate business requirements to technical specification",
                "model_preferences": {
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
            })

            # Handle the LLM result - could be string or dict
            if isinstance(llm_result, str):
                # If it's already a string, use it directly as the content
                technical_content = llm_result
            elif isinstance(llm_result, dict):
                # If it's a dict, extract the content with defaults to avoid None
                content_val = llm_result.get("content", None)
                if content_val is None:
                    content_val = llm_result.get("text", None)
                if content_val is None:
                    content_val = str(llm_result)
                technical_content = str(content_val)
            else:
                # For any other type, convert to string
                technical_content = str(llm_result)

            # Validate the generated technical specification content for security
            content_validation = validate_specification_content(technical_content)
            if not content_validation.is_valid:
                error_messages = tuple(error.message for error in content_validation.errors)
                await self.ctx.error(f"Specification content validation failed: {error_messages}")
                return TranslationResult(
                    success=False,
                    errors=error_messages,
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Create technical specification
            technical_spec = TechnicalSpecification(
                content=technical_content,
                format="SPEC",
                source_requirements_id=requirements.id
            )

            # Store the specification to the client filesystem
            spec_filename = f"spec_{requirements.id[:8]}.md"
            try:
                output_path = build_secure_output_path(config.output_directory, spec_filename)
            except ValueError as e:
                await self.ctx.error(f"Failed to build secure output path: {str(e)}")
                return TranslationResult(
                    success=False,
                    errors=(f"Failed to create secure output path: {str(e)}",),
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Ensure the output directory exists first
            dir_exists = await self.filesystem_adapter.directory_exists(config.output_directory)
            if not dir_exists:
                dir_created = await self.filesystem_adapter.create_directory(config.output_directory)
                if not dir_created:
                    await self.ctx.error(f"Failed to create output directory: {config.output_directory}")
                    return TranslationResult(
                        success=False,
                        errors=(f"Failed to create output directory: {config.output_directory}",),
                        execution_time_ms=(time.time() - start_time) * 1000
                    )

            # Write the specification to file
            file_written = await self.filesystem_adapter.write_file(output_path, technical_spec.content)
            if not file_written:
                await self.ctx.error(f"Failed to write specification to file: {output_path}")
                return TranslationResult(
                    success=False,
                    errors=(f"Failed to write specification to file: {output_path}",),
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Create and return successful translation result
            result = TranslationResult(
                success=True,
                specification=technical_spec,
                execution_time_ms=(time.time() - start_time) * 1000
            )

            await self.ctx.log(f"Business requirements successfully translated and stored at {output_path}")
            return result

        except Exception as e:
            await self.ctx.error(f"Unexpected error in translate_business_requirements: {str(e)}")
            return TranslationResult(
                success=False,
                errors=(f"Unexpected error: {str(e)}",),
                execution_time_ms=(time.time() - start_time) * 1000
            )

    async def get_translation_status(self, translation_id: str) -> TranslationStatus:
        """Get the current status of a translation operation"""
        # For now, this is a simplified implementation
        # In a real system, this would check the status of ongoing operations
        return TranslationStatus(
            translation_id=translation_id,
            status="completed",
            progress=1.0
        )

    async def validate_requirements(self, requirements: BusinessRequirements) -> bool:
        """Validate business requirements using core validation logic"""
        try:
            validation_result = validate_business_requirements(requirements)
            return validation_result.is_valid
        except Exception as e:
            await self.ctx.error(f"Error validating requirements: {str(e)}")
            return False