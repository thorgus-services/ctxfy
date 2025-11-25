from fastmcp import FastMCP

from .shell.orchestrators.mcp_orchestrator import MCPOrchestrator


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        name="ctxfy-specification-server",
        version="1.0.0",
    )

    MCPOrchestrator(mcp)

    return mcp

mcp_server = create_mcp_server()
app = mcp_server.http_app()