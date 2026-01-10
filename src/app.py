from fastmcp import FastMCP

from src.shell.orchestrators.mcp_orchestrator import MCPOrchestrator


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        name="ctxfy-specification-server",
        version="1.0.0",
    )

    MCPOrchestrator(mcp)

    return mcp


mcp_server = create_mcp_server()


def run_stdio_server() -> None:
    mcp_server.run()


if __name__ == "__main__":
    run_stdio_server()