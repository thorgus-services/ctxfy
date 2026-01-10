import sys
from io import StringIO
from unittest.mock import patch

from src.app import create_mcp_server, run_stdio_server


def test_create_mcp_server_returns_fastmcp_instance():
    from fastmcp import FastMCP

    server = create_mcp_server()

    assert isinstance(server, FastMCP)
    assert server.name == "ctxfy-specification-server"
    assert server.version == "1.0.0"


def test_create_mcp_server_registers_orchestrator():
    with patch('src.app.MCPOrchestrator') as mock_orchestrator_class:
        create_mcp_server()
        mock_orchestrator_class.assert_called_once()


def test_run_stdio_server_calls_run_method():
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    try:
        sys.stdin = StringIO("")
        sys.stdout = StringIO()

        with patch('src.app.mcp_server') as mock_server:
            run_stdio_server()
            mock_server.run.assert_called_once()
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout


def test_main_execution_logic():
    import src.app

    assert hasattr(src.app, 'run_stdio_server')
    assert callable(src.app.run_stdio_server)

    assert True