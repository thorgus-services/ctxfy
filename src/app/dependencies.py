"""Dependency injection container following hexagonal architecture principles."""

from datetime import datetime

from src.adapters.api_docs import MCPToolsDocsGenerator, OpenAPIDocGenerator
from src.adapters.auth import ApiKeyAuthAdapter, InMemoryApiKeyRepository
from src.adapters.auth.middleware import AuthMiddleware
from src.adapters.monitoring import StructuredLoggingAdapter
from src.adapters.monitoring.monitoring import MonitoringAdapter
from src.adapters.validation import SchemaValidationAdapter
from src.core.ports.auth_ports import AuthCommandPort
from src.core.ports.monitoring_ports import HealthQueryPort, MetricsPort
from src.core.ports.validation_ports import ValidationPort


class AppDependencies:
    """Container for application dependencies following hexagonal architecture."""

    def __init__(self) -> None:
        self.api_key_repo = InMemoryApiKeyRepository()
        self.auth_adapter = ApiKeyAuthAdapter(self.api_key_repo)
        self.auth_middleware = AuthMiddleware(self.auth_adapter)

        self.start_time = datetime.now()
        self.monitoring_adapter = MonitoringAdapter(self.start_time)
        self.logging_adapter = StructuredLoggingAdapter()
        self.validation_adapter = SchemaValidationAdapter()

        self.auth_command_port: AuthCommandPort = self.auth_adapter
        self.health_query_port: HealthQueryPort = self.monitoring_adapter
        self.monitoring_port: MetricsPort = self.monitoring_adapter
        self.validation_port: ValidationPort = self.validation_adapter

        self.openapi_generator = OpenAPIDocGenerator(
            mcp_server=None,
            title="ctxfy MCP Server API",
            description="Production-ready ctxfy MCP Server with authentication, monitoring, and documentation",
            version="1.0.0"
        )

        self.mcp_tools_docs_generator = MCPToolsDocsGenerator()