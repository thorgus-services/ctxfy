from fastmcp import FastMCP

from .shell.orchestrators.specification_orchestrator import SpecificationOrchestrator


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        name="ctxfy-specification-server",
        version="1.0.0",
    )

    SpecificationOrchestrator(mcp)

    return mcp

mcp_server = create_mcp_server()
app = mcp_server.http_app()