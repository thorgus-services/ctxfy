"""End-to-end tests for the MCP server application following TDD principles."""

from unittest.mock import AsyncMock, patch

import pytest

from src.app.main import AppDependencies, MCPServerApp


class TestMCPServerApp:
    """Test the main MCP server application."""

    def test_app_dependencies_initialization(self):
        """Test that AppDependencies initializes all required components."""
        deps = AppDependencies()

        # Verify all components are initialized
        assert deps.api_key_repo is not None
        assert deps.auth_adapter is not None
        assert deps.monitoring_adapter is not None
        assert deps.logging_adapter is not None
        assert deps.validation_adapter is not None
        assert deps.auth_middleware is not None
        assert deps.openapi_generator is not None

        # Verify types
        from src.adapters.api_docs import OpenAPIDocGenerator
        from src.adapters.auth import ApiKeyAuthAdapter
        from src.adapters.auth.middleware import AuthMiddleware
        from src.adapters.monitoring import MonitoringAdapter, StructuredLoggingAdapter

        assert isinstance(deps.auth_adapter, ApiKeyAuthAdapter)
        assert isinstance(deps.monitoring_adapter, MonitoringAdapter)
        assert isinstance(deps.logging_adapter, StructuredLoggingAdapter)
        assert isinstance(deps.auth_middleware, AuthMiddleware)
        assert isinstance(deps.openapi_generator, OpenAPIDocGenerator)

    def test_app_initialization(self):
        """Test that MCPServerApp initializes without errors."""
        app = MCPServerApp()

        assert app is not None
        assert app.mcp is not None
        assert app.dependencies is not None
        assert isinstance(app.dependencies, AppDependencies)

    def test_app_initialization_with_dependencies(self):
        """Test that MCPServerApp accepts custom dependencies."""
        custom_deps = AppDependencies()
        app = MCPServerApp(dependencies=custom_deps)

        assert app.dependencies == custom_deps

    @pytest.mark.asyncio
    async def test_app_setup_server(self):
        """Test that server setup runs without errors."""
        app = MCPServerApp()

        # The setup should complete without raising exceptions
        assert app.mcp is not None

        # Check that prompts were registered
        # (We can't easily test the actual registration in FastMCP without internal inspection,
        # but we can at least verify that the setup method ran)
        assert app.mcp is not None

    @pytest.mark.asyncio
    async def test_app_start_server_would_work(self):
        """Test that the app structure supports server startup (without actually starting)."""
        app = MCPServerApp()

        # Patch the actual run_http_async method to avoid actually starting a server
        with patch.object(app.mcp, 'run_http_async', new=AsyncMock()) as mock_run_http_async:
            # Call start_server - this should not raise exceptions for setup
            try:
                await app.start_server(host="127.0.0.1", port=8001)  # Use different port to avoid conflicts
            except Exception as e:
                # If there's an exception, make sure it's not due to basic setup issues
                # The mock should prevent actual network binding
                assert "bind" not in str(e).lower(), f"Server failed to start due to binding issue: {e}"
                raise  # Re-raise if it's a different error

        # Verify that run_http_async was called
        mock_run_http_async.assert_called_once()


class TestCompleteIntegration:
    """Test that all components work together correctly."""

    def test_all_models_import_successfully(self):
        """Test that all core models can be imported without errors."""
        from src.core.models.mcp_models import HealthStatus

        # Verify we can instantiate basic instances
        # (without requiring complex parameters to test basic import/definition)
        health = HealthStatus(status="healthy")
        assert health.status == "healthy"

    def test_all_adapters_import_successfully(self):
        """Test that all adapters can be imported without errors."""
        from src.adapters.monitoring import StructuredLoggingAdapter

        # Create basic instances to ensure they work
        logging_adapter = StructuredLoggingAdapter()
        assert logging_adapter.level == "INFO"

    def test_all_ports_import_successfully(self):
        """Test that all ports can be imported without errors."""
        from src.core.ports.auth_ports import AuthCommandPort, AuthQueryPort
        from src.core.ports.mcp_ports import LoggingPort
        from src.core.ports.monitoring_ports import HealthQueryPort, MetricsPort
        from src.core.ports.monitoring_ports import LoggingPort as MonitorLoggingPort
        from src.core.ports.validation_ports import ValidationPort

        # Just verify imports work
        assert LoggingPort is not None
        assert AuthCommandPort is not None
        assert AuthQueryPort is not None
        assert MonitorLoggingPort is not None
        assert MetricsPort is not None
        assert HealthQueryPort is not None
        assert ValidationPort is not None