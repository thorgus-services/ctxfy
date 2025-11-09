"""Orchestrator for context stack generation workflow."""

import logging
import time
from decimal import Decimal
from typing import Any, Dict, List, Optional

from ...core.models.context_models import (
    ContextGenerationRequest,
    ContextGenerationResponse,
)
from ...core.ports.context_stack_ports import ContextStackGenerationCommandPort
from ...core.use_cases.validation import validate_and_raise


class ContextGenerationOrchestrator:
    """Orchestrator that coordinates the context stack generation workflow.

    Following the orchestrator pattern, this class handles workflow coordination
    without containing business logic, which resides in the Functional Core.
    """

    def __init__(self, command_port: ContextStackGenerationCommandPort):
        self.command_port = command_port
        self.logger = logging.getLogger(__name__)

    def generate_context_stack(self, request: ContextGenerationRequest) -> ContextGenerationResponse:
        """Orchestrate the context stack generation process."""
        start_time = time.perf_counter()

        try:
            self.logger.info(f"Starting context stack generation for feature: {request.feature_description}")

            # Validate the incoming request
            try:
                validate_and_raise(request)
            except Exception as e:
                self.logger.error(f"Validation failed: {str(e)}")
                processing_time = Decimal(str(time.perf_counter() - start_time))
                return ContextGenerationResponse(
                    success=False,
                    context_stack=None,
                    error_message=str(e),
                    processing_time=processing_time
                )

            # Call the command port to generate the context stack
            result = self.command_port.generate_context_stack(request)

            # Log the result
            if result.success:
                self.logger.info(f"Context stack generated successfully in {result.processing_time} seconds")
            else:
                self.logger.error(f"Context stack generation failed: {result.error_message}")

            return result

        except Exception as e:
            processing_time = Decimal(str(time.perf_counter() - start_time))
            error_msg = f"Unexpected error during context stack generation: {str(e)}"
            self.logger.error(error_msg, exc_info=True)

            return ContextGenerationResponse(
                success=False,
                context_stack=None,
                error_message=error_msg,
                processing_time=processing_time
            )

    def generate_context_stack_for_mcp(self, 
                                     feature_description: str,
                                     target_technologies: Optional[List[str]] = None,
                                     custom_rules: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate context stack and format response for MCP protocol."""
        if target_technologies is None:
            target_technologies = []
        if custom_rules is None:
            custom_rules = []

        if not feature_description:
            return {"success": False, "error": "feature_description is required"}

        request = ContextGenerationRequest(
            feature_description=feature_description,
            target_technologies=target_technologies,
            custom_rules=custom_rules
        )

        result = self.generate_context_stack(request)

        if result.success and result.context_stack:
            context_stack = result.context_stack
            return {
                "success": True,
                "result": {
                    "context_stack": {
                        "system_layer": {
                            "name": context_stack.system_layer.name,
                            "description": context_stack.system_layer.description,
                            "specifications": context_stack.system_layer.specifications,
                            "dependencies": context_stack.system_layer.dependencies
                        },
                        "domain_layer": {
                            "name": context_stack.domain_layer.name,
                            "description": context_stack.domain_layer.description,
                            "specifications": context_stack.domain_layer.specifications,
                            "dependencies": context_stack.domain_layer.dependencies
                        },
                        "task_layer": {
                            "name": context_stack.task_layer.name,
                            "description": context_stack.task_layer.description,
                            "specifications": context_stack.task_layer.specifications,
                            "dependencies": context_stack.task_layer.dependencies
                        },
                        "metadata": {
                            "version": context_stack.metadata.version,
                            "creation_date": context_stack.metadata.creation_date.isoformat(),
                            "author": context_stack.metadata.author,
                            "domain": context_stack.metadata.domain,
                            "task_type": context_stack.metadata.task_type
                        },
                        "additional_layers": [
                            {
                                "name": layer.name,
                                "description": layer.description,
                                "specifications": layer.specifications,
                                "dependencies": layer.dependencies
                            }
                            for layer in context_stack.additional_layers
                        ]
                    },
                    "processing_time": float(result.processing_time)
                }
            }
        else:
            return {"success": False, "error": result.error_message}