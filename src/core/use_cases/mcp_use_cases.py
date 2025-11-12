"""Pure functions implementing business rules for MCP operations.

All functions in the core are pure - no side effects, no I/O operations, no mutation.
Following Functional Core & Imperative Shell pattern.
"""

from datetime import datetime
from typing import Any, Dict

from src.core.models.mcp_models import HealthStatus, PromptRequest, PromptResponse


def process_prompt_request(
    name: str, 
    parameters: Dict[str, Any], 
    start_time: datetime,
    llm_model: str
) -> PromptRequest:
    """Pure function to create and validate a prompt request.
    
    Args:
        name: Name of the prompt
        parameters: Parameters for the prompt
        start_time: Time when processing started
        llm_model: Model used for processing
    
    Returns:
        PromptRequest: Validated prompt request object
    """
    # Create the prompt request
    prompt_request = PromptRequest(
        name=name,
        parameters=parameters
    )
    
    return prompt_request


def create_prompt_response(
    request_id: str,
    result: str,
    start_time: datetime,
    llm_model: str
) -> PromptResponse:
    """Pure function to create a prompt response with calculated latency.
    
    Args:
        request_id: ID of the request
        result: Response result
        start_time: Time when processing started
        llm_model: Model used for processing
        
    Returns:
        PromptResponse: Validated prompt response object with latency calculation
    """
    end_time = datetime.now()
    latency_ms = (end_time - start_time).total_seconds() * 1000
    
    response = PromptResponse(
        request_id=request_id,
        result=result,
        latency_ms=latency_ms,
        llm_model=llm_model
    )
    
    return response


def calculate_health_status(
    start_time: datetime,
    version: str = "1.0.0"
) -> HealthStatus:
    """Pure function to calculate health status based on uptime.
    
    Args:
        start_time: When the server started
        version: Current version of the service
        
    Returns:
        HealthStatus: Health status with calculated uptime
    """
    current_time = datetime.now()
    uptime = current_time - start_time
    uptime_seconds = uptime.total_seconds()
    
    # For now, always return healthy - in a real system this would check
    # actual system health indicators
    status = HealthStatus(
        status="healthy",
        uptime_seconds=uptime_seconds,
        version=version
    )
    
    return status