"""OpenAPI 3.0 documentation generator for FastMCP server endpoints."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastmcp.server import FastMCP


class OpenAPIDocGenerator:
    """OpenAPI 3.0 documentation generator for FastMCP server."""

    def __init__(self, mcp_server: Optional[FastMCP], title: str = "ctxfy MCP Server API",
                 description: str = "API documentation for ctxfy MCP Server with authentication and monitoring",
                 version: str = "1.0.0"):
        self.mcp_server = mcp_server
        self.title = title
        self.description = description
        self.version = version

    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI 3.0 specification for the server."""
        # Basic OpenAPI structure
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "description": self.description,
                "version": self.version,
                "contact": {
                    "name": "ctxfy API Support",
                    "email": "support@ctxfy.dev"
                }
            },
            "servers": [
                {
                    "url": "http://localhost:8000",
                    "description": "Development server"
                }
            ],
            "paths": self._generate_paths(),
            "components": self._generate_components()
        }

        return openapi_spec

    def _generate_paths(self) -> Dict[str, Any]:
        """Generate path definitions for all registered endpoints."""
        paths: Dict[str, Any] = {
            "/health": {
                "get": {
                    "summary": "Health check endpoint",
                    "description": "Returns the health status of the server",
                    "responses": {
                        "200": {
                            "description": "Server is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HealthStatus"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/metrics": {
                "get": {
                    "summary": "Metrics endpoint",
                    "description": "Returns Prometheus metrics",
                    "responses": {
                        "200": {
                            "description": "Metrics in Prometheus format",
                            "content": {
                                "text/plain": {
                                    "schema": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        # Add API key management endpoints
        paths["/auth/api-keys"] = {
            "post": {
                "summary": "Create API key",
                "description": "Create a new API key for a user",
                "security": [{"BearerAuth": []}],  # Empty array means no specific scopes required
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ApiKeyRequest"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "API key created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "api_key": {"type": "string", "description": "The newly created API key"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        return paths

    def _generate_components(self) -> Dict[str, Any]:
        """Generate component definitions for schemas and security."""
        return {
            "schemas": {
                "HealthStatus": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["healthy", "degraded", "unhealthy"],
                            "description": "Current health status"
                        },
                        "timestamp": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Timestamp of the health check"
                        },
                        "uptime_seconds": {
                            "type": "number",
                            "description": "Uptime in seconds"
                        },
                        "version": {
                            "type": "string",
                            "description": "API version"
                        },
                        "checks": {
                            "type": "object",
                            "description": "Detailed health check results",
                            "additionalProperties": True
                        }
                    },
                    "required": ["status", "timestamp", "uptime_seconds", "version"]
                },
                "ApiKeyRequest": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user requesting the API key"
                        },
                        "scope": {
                            "type": "string",
                            "enum": ["read", "write", "admin"],
                            "description": "Access scope for the API key"
                        },
                        "ttl_hours": {
                            "type": "integer",
                            "minimum": 1,
                            "description": "Time-to-live in hours (optional)"
                        }
                    },
                    "required": ["user_id", "scope"]
                },
                "AuthResult": {
                    "type": "object",
                    "properties": {
                        "is_authenticated": {
                            "type": "boolean",
                            "description": "Whether the authentication was successful"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID if authenticated"
                        },
                        "scope": {
                            "type": "string",
                            "enum": ["read", "write", "admin"],
                            "description": "Access scope if authenticated"
                        },
                        "error_message": {
                            "type": "string",
                            "description": "Error message if authentication failed"
                        }
                    },
                    "required": ["is_authenticated"]
                }
            },
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "API Key",
                    "description": "API key authentication using Bearer token scheme"
                }
            }
        }

    def register_docs_endpoint(self, app: Any) -> None:
        """Register the documentation endpoint with the FastAPI app."""
        try:
            # If FastAPI is available, register the docs endpoint
            from fastapi import FastAPI
            if isinstance(app, FastAPI):
                @app.get("/docs", tags=["documentation"])
                async def get_openapi_docs() -> Dict[str, Any]:
                    return self.generate_openapi_spec()

                @app.get("/openapi.json", tags=["documentation"])
                async def get_openapi_json() -> Dict[str, Any]:
                    return self.generate_openapi_spec()
        except ImportError:
            # If FastAPI is not available, the method does nothing
            pass