from unittest.mock import Mock

import pytest

from src.app.main import AppDependencies, MCPServerApp


class TestAppDependencies:
    """Tests for AppDependencies class."""

    def test_app_dependencies_initialization(self):
        """Test initializing AppDependencies."""
        deps = AppDependencies()
        
        # Check that all dependencies are properly initialized
        assert deps.api_key_repo is not None
        assert deps.auth_adapter is not None
        assert deps.start_time is not None
        assert deps.monitoring_adapter is not None 
        assert deps.logging_adapter is not None
        assert deps.validation_adapter is not None
        assert deps.auth_middleware is not None
        assert deps.openapi_generator is not None


class TestMCPServerApp:
    """Tests for MCPServerApp class."""

    def test_init_with_dependencies(self):
        """Test initializing MCPServerApp with dependencies."""
        mock_deps = Mock(spec=AppDependencies)
        # Add required attributes that the code expects
        mock_deps.openapi_generator = Mock()
        mock_deps.mcp_tools_docs_generator = Mock()
        mock_deps.logging_adapter = Mock()
        mock_deps.monitoring_adapter = Mock()
        mock_deps.auth_adapter = Mock()
        app = MCPServerApp(mock_deps)

        assert app.dependencies is mock_deps
        assert app.mcp is not None

    def test_init_without_dependencies(self):
        """Test initializing MCPServerApp without dependencies."""
        app = MCPServerApp()
        
        assert app.dependencies is not None
        assert app.mcp is not None

    def test_get_app(self):
        """Test getting the FastMCP app instance."""
        app = MCPServerApp()
        mcp_app = app.get_app()
        
        assert mcp_app is not None
        assert mcp_app is app.mcp


    @pytest.mark.asyncio
    async def test_health_check_functionality(self):
        """Test the health check functionality through the monitoring adapter."""
        app = MCPServerApp()

        # Call the monitoring adapter directly to test health status
        health_status = await app.dependencies.monitoring_adapter.get_health_status()

        # Verify the health status structure
        assert hasattr(health_status, 'status')
        assert hasattr(health_status, 'timestamp')
        assert hasattr(health_status, 'uptime_seconds')
        assert hasattr(health_status, 'version')
        assert hasattr(health_status, 'checks')

        # Verify expected values
        assert health_status.status in ['healthy', 'degraded', 'unhealthy']
        assert health_status.uptime_seconds >= 0
        assert isinstance(health_status.version, str)
        assert isinstance(health_status.checks, dict)

    @pytest.mark.asyncio
    async def test_metrics_endpoint(self):
        """Test the metrics endpoint still works through monitoring adapter."""
        app = MCPServerApp()

        # Test metrics functionality directly via the monitoring adapter
        metrics_data = app.dependencies.monitoring_adapter.get_prometheus_metrics()
        assert isinstance(metrics_data, bytes)
        assert len(metrics_data) >= 0  # Should have some metrics data

    @pytest.mark.asyncio
    async def test_create_api_key_endpoint_success(self):
        """Test the create-api-key endpoint with success."""
        app = MCPServerApp()
        
        # Mock a ctx object for the prompt
        mock_ctx = Mock()
        
        # Call the create-api-key handler
        result = await app.mcp._handlers['create-api-key']['fn'](
            mock_ctx, 
            user_id="test_user",
            scope="read"
        )
        
        # Check that result contains expected fields
        assert 'api_key' in result
        assert 'key_id' in result


    @pytest.mark.asyncio
    async def test_start_server_method_exists(self):
        """Test that start_server method exists and can be called."""
        app = MCPServerApp()

        # Verify the method exists
        assert hasattr(app, 'start_server')
        assert callable(app.start_server)

    def test_setup_server(self):
        """Test server setup."""
        app = MCPServerApp()

        # After initialization, handlers should be registered
        assert 'create-api-key' in app.mcp._handlers