"""Structured logging adapter implementing the LoggingPort protocol.

This adapter provides structured JSON logging with required fields:
- prompt_id
- latency_ms
- llm_model
"""

import json
from datetime import datetime

from src.core.ports.mcp_ports import LoggingPort


class StructuredLogger(LoggingPort):
    """Structured logging adapter with JSON format and required fields."""
    
    def __init__(self, level: str = "INFO"):
        """Initialize the structured logger.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.level = level.upper()
    
    def log_prompt_request(
        self, 
        prompt_id: str, 
        name: str, 
        latency_ms: float, 
        llm_model: str
    ) -> None:
        """Log a prompt request with required fields in JSON format.
        
        Args:
            prompt_id: Unique identifier for the prompt
            name: Name of the prompt
            latency_ms: Processing time in milliseconds
            llm_model: Model used for the operation
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": f"Processed prompt: {name}",
            "prompt_id": prompt_id,
            "latency_ms": latency_ms,
            "llm_model": llm_model,
            "module": "structured_logger",
            "function": "log_prompt_request"
        }
        
        print(json.dumps(log_entry))  # noqa: T201
    
    def log_error(
        self, 
        prompt_id: str, 
        name: str, 
        error: Exception, 
        llm_model: str = "unknown"
    ) -> None:
        """Log an error with required fields in JSON format.
        
        Args:
            prompt_id: Unique identifier for the prompt
            name: Name of the prompt
            error: The exception that occurred
            llm_model: Model used for the operation
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "message": f"Error processing prompt '{name}': {str(error)}",
            "prompt_id": prompt_id,
            "latency_ms": 0,  # No latency for errors
            "llm_model": llm_model,
            "module": "structured_logger",
            "function": "log_error",
            "error_type": type(error).__name__
        }
        
        print(json.dumps(log_entry))  # noqa: T201
    
    def log_health_check(
        self,
        status: str,
        uptime_seconds: float
    ) -> None:
        """Log a health check with required fields.
        
        Args:
            status: Health status ('healthy', 'degraded', 'unhealthy')
            uptime_seconds: Uptime in seconds
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": f"Health check status: {status}",
            "prompt_id": "N/A",  # Health check doesn't have a prompt ID
            "latency_ms": 0,
            "llm_model": "N/A",
            "module": "structured_logger",
            "function": "log_health_check",
            "uptime_seconds": uptime_seconds
        }
        
        print(json.dumps(log_entry))  # noqa: T201