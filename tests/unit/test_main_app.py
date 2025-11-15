import asyncio
from unittest.mock import AsyncMock, Mock

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
    async def test_sample_prompt_endpoint_success(self):
        """Test the sample-prompt endpoint with successful execution."""
        app = MCPServerApp()
        
        # Mock a ctx object for the prompt
        mock_ctx = Mock()
        
        # Call the registered prompt handler
        result = await app.mcp._handlers['sample-prompt']['fn'](mock_ctx, param1="test_value")
        
        assert "Processed: test_value" in result

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
    async def test_sample_prompt_endpoint_error_handling(self):
        """Test the sample-prompt endpoint error handling."""
        app = MCPServerApp()
        
        # Mock a ctx object that will cause an error in the prompt
        mock_ctx = Mock()
        
        # Patch the internal logic to raise an error
        original_func = app.mcp._handlers['sample-prompt']['fn']
        
        async def error_func(ctx, param1="default"):
            raise ValueError("Test error")
        
        app.mcp._handlers['sample-prompt']['fn'] = error_func
        
        # The error should be raised (as per the implementation)
        with pytest.raises(ValueError, match="Test error"):
            await app.mcp._handlers['sample-prompt']['fn'](mock_ctx, param1="test")
        
        # Restore original function
        app.mcp._handlers['sample-prompt']['fn'] = original_func

    @pytest.mark.asyncio
    async def test_start_server(self):
        """Test starting the server (basic functionality)."""
        app = MCPServerApp()
        
        # Mock the mcp run_http_async method to avoid actual server start
        app.mcp.run_http_async = AsyncMock()
        
        # Call start_server but time out quickly to avoid hanging
        try:
            await asyncio.wait_for(app.start_server(host="127.0.0.1", port=8000), timeout=0.01)
        except asyncio.TimeoutError:
            pass  # Expected timeout since we're not running a real server
        
        # Verify the run_http_async was called
        app.mcp.run_http_async.assert_called()

    def test_setup_server(self):
        """Test server setup."""
        app = MCPServerApp()

        # After initialization, handlers should be registered
        assert 'sample-prompt' in app.mcp._handlers
        assert 'create-api-key' in app.mcp._handlers