"""Unit tests for context generation orchestrator."""

import pytest
from unittest.mock import Mock
from datetime import datetime
from decimal import Decimal
from src.core.models.context_models import (
    ContextLayer, ContextStackMetadata, 
    ContextStack, ContextGenerationRequest,
    ContextGenerationResponse
)
from src.shell.orchestrators.context_generation_orchestrator import (
    ContextGenerationOrchestrator
)
from src.core.ports.context_stack_ports import ContextStackGenerationCommandPort
from src.core.exceptions import ValidationError


class TestContextGenerationOrchestrator:
    """Test cases for ContextGenerationOrchestrator."""
    
    @pytest.fixture
    def mock_command_port(self):
        """Fixture providing a mock command port."""
        return Mock(spec=ContextStackGenerationCommandPort)
    
    @pytest.fixture
    def orchestrator(self, mock_command_port):
        """Fixture providing an orchestrator instance."""
        return ContextGenerationOrchestrator(mock_command_port)
    
    def test_generate_context_stack_calls_port_with_valid_request(self, orchestrator, mock_command_port):
        """Test that orchestrator calls the command port with a valid request."""
        # Create a valid request
        request = ContextGenerationRequest(
            feature_description="Test feature description that is at least 5 characters",
            target_technologies=["Python", "FastAPI"],
            custom_rules=[]
        )
        
        # Mock the port to return a successful response
        mock_response = ContextGenerationResponse(
            success=True,
            context_stack=Mock(),  # Mock context stack
            error_message=None,
            processing_time=Decimal("0.1")
        )
        mock_command_port.generate_context_stack.return_value = mock_response
        
        # Call the orchestrator
        result = orchestrator.generate_context_stack(request)
        
        # Verify the port was called with the request
        mock_command_port.generate_context_stack.assert_called_once_with(request)
        assert result is mock_response
    
    def test_generate_context_stack_handles_validation_error(self, orchestrator, mock_command_port):
        """Test that orchestrator handles validation errors properly."""
        # Create a request with a feature description that's too short to meet validation requirements in the validate_and_raise function
        request = ContextGenerationRequest(
            feature_description="test",  # Valid for construction but too short for validation
            target_technologies=["Python", "FastAPI"],
            custom_rules=[]
        )
        
        # Call the orchestrator
        result = orchestrator.generate_context_stack(request)
        
        # Verify the port was NOT called
        mock_command_port.generate_context_stack.assert_not_called()
        
        # Verify that result is an error response
        assert result.success is False
        assert result.context_stack is None
        assert result.error_message is not None
        assert result.processing_time >= 0
    
    def test_generate_context_stack_propagates_port_error(self, orchestrator, mock_command_port):
        """Test that orchestrator propagates errors from the command port."""
        # Create a valid request
        request = ContextGenerationRequest(
            feature_description="Valid feature description that meets requirements",
            target_technologies=["Python", "FastAPI"],
            custom_rules=[]
        )
        
        # Mock the port to return an error response
        error_response = ContextGenerationResponse(
            success=False,
            context_stack=None,
            error_message="Port error occurred",
            processing_time=Decimal("0.05")
        )
        mock_command_port.generate_context_stack.return_value = error_response
        
        # Call the orchestrator
        result = orchestrator.generate_context_stack(request)
        
        # Verify the port was called
        mock_command_port.generate_context_stack.assert_called_once_with(request)
        assert result is error_response
    
    def test_generate_context_stack_handles_unexpected_exception(self, orchestrator, mock_command_port):
        """Test that orchestrator handles unexpected exceptions."""
        # Create a valid request
        request = ContextGenerationRequest(
            feature_description="Valid feature description that meets requirements",
            target_technologies=["Python", "FastAPI"],
            custom_rules=[]
        )
        
        # Mock the port to raise an exception
        mock_command_port.generate_context_stack.side_effect = Exception("Unexpected error")
        
        # Call the orchestrator
        result = orchestrator.generate_context_stack(request)
        
        # Verify that result is an error response
        assert result.success is False
        assert result.context_stack is None
        assert result.error_message is not None
        assert "Unexpected error" in result.error_message
        assert result.processing_time >= 0