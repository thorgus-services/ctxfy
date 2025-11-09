"""Orchestrator for context stack generation workflow."""

from datetime import datetime
from decimal import Decimal
import time
import logging

from ...core.models.context_models import (
    ContextGenerationRequest, ContextGenerationResponse
)
from ...core.ports.context_stack_ports import ContextStackGenerationCommandPort
from ...core.use_cases.context_stack_generation import (
    generate_context_stack_functional
)
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