import sys
import threading
import time

from fastmcp import FastMCP

from src.shell.orchestrators.mcp_orchestrator import MCPOrchestrator
from src.shell.utils.health_check import (
    get_overall_status,
    perform_health_checks,
    update_health_status,
)


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


def run_mcp_with_health_monitor() -> None:
    mcp_start_time = time.time()

    checks = perform_health_checks()
    overall_status = get_overall_status(checks)
    current_uptime = time.time() - mcp_start_time
    update_health_status(status=overall_status, checks=checks, mcp_uptime=current_uptime)

    def health_monitor() -> None:
        while True:
            try:
                checks = perform_health_checks()
                overall_status = get_overall_status(checks)
                current_uptime = time.time() - mcp_start_time
                update_health_status(status=overall_status, checks=checks, mcp_uptime=current_uptime)
                time.sleep(10)
            except Exception as e:
                import logging
                logging.error(f"Error in health monitor: {e}")
                time.sleep(10)

    health_thread = threading.Thread(target=health_monitor, daemon=True)
    health_thread.start()

    mcp_server.run()


if __name__ == "__main__":
    # Check command line arguments to determine which server to run
    if len(sys.argv) > 1:
        if sys.argv[1] == "run_stdio_server":
            run_stdio_server()
        elif sys.argv[1] == "run_health_monitor":
            run_mcp_with_health_monitor()
        else:
            sys.stderr.write(f"Unknown command: {sys.argv[1]}\n")
            sys.stderr.write("Usage: python -m src.app [run_stdio_server|run_health_monitor]\n")
            sys.exit(1)
    else:
        # Default behavior: run STDIO server only
        run_stdio_server()