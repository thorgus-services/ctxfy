"""Documentation handlers for the ctxfy MCP Server."""

from typing import TYPE_CHECKING, Any

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

if TYPE_CHECKING:
    pass


def register_documentation_handlers(
    mcp: FastMCP,
    dependencies: Any
) -> dict[str, Any]:
    """Register documentation endpoints with the FastMCP server."""
    handlers: dict[str, Any] = {}

    @mcp.custom_route("/openapi.json", methods=["GET"])
    async def openapi_spec(request: Request) -> JSONResponse:
        """Endpoint to serve the OpenAPI specification."""
        spec = await dependencies.openapi_generator.get_openapi_spec()
        return JSONResponse(spec)

    @mcp.custom_route("/docs", methods=["GET"])
    async def api_docs(request: Request) -> Response:
        """Endpoint to serve interactive API documentation."""
        swagger_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ctxfy MCP Server API Documentation</title>
            <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.11.0/swagger-ui.css">
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.11.0/swagger-ui-bundle.js"></script>
            <script>
            const ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.presets.standalone
                ]
            });
            </script>
        </body>
        </html>
        """
        return Response(content=swagger_html, media_type="text/html")

    @mcp.custom_route("/mcp-tools", methods=["GET"])
    async def mcp_tools_spec(request: Request) -> JSONResponse:
        """Endpoint to serve MCP tools specification."""
        tools_spec = await dependencies.mcp_tools_docs_generator.get_mcp_tools_docs()
        return JSONResponse(tools_spec)

    return handlers