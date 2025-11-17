# Ctxfy MCP Server API Reference Guide

This document provides a comprehensive reference for all API endpoints available in the Ctxfy MCP Server, following fastMCP best practices and MCP protocol standards.

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Health Check Endpoint](#health-check-endpoint)
4. [Metrics Endpoint](#metrics-endpoint)
5. [MCP Tools Endpoints](#mcp-tools-endpoints)
6. [API Documentation Endpoints](#api-documentation-endpoints)
7. [Error Handling](#error-handling)
8. [Tool Parameters and Validation](#tool-parameters-and-validation)
9. [Examples and Usage](#examples-and-usage)

## Overview

The Ctxfy MCP Server implements the Model Context Protocol (MCP) to provide standardized interaction between developers and AI agents. This server provides various tools that can be invoked by AI agents to perform specific tasks with rich metadata and complete parameter validation.

The server follows fastMCP patterns with:
- Detailed tool descriptions and metadata
- Annotated parameters with validation constraints
- Structured return types following MCP protocol
- MCP annotations for tool behavior hints

## Authentication

All MCP endpoints require API key authentication. Include your API key in the request headers:

```
Authorization: Bearer YOUR_API_KEY
```

## Health Check Endpoint

### GET /health

Returns the current health status of the server.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-10-10T12:00:00Z",
  "uptime_seconds": 3600,
  "version": "1.0.0",
  "checks": {},
  "service": "ctxfy-mcp-server"
}
```

## Metrics Endpoint

### GET /metrics

Returns Prometheus-formatted metrics for monitoring.

**Response:**
Plain text response in Prometheus format.

## MCP Tools Endpoints

All MCP tools follow the POST pattern to `/mcp/{tool_name}` endpoints and provide rich metadata in the MCP tools specification.


### Create API Key Tool

**Name:** create-api-key
**Title:** Create API Key
**Tags:** {"auth", "security"}
**Annotations:**
- `readOnlyHint`: false
- `destructiveHint`: false

Create a new API key for authentication. This tool generates a new API key that can be used for authenticating requests to the MCP server. The API key can have different scopes and time-to-live settings.

#### Usage
**POST** `/mcp/create-api-key`

**Request Body:**
```json
{
  "user_id": "string",
  "scope": "string",
  "ttl_hours": "integer"
}
```

**Parameters:**
- `user_id` (required): Unique identifier for the user requesting the API key
- `scope` (optional, default: "read"): Access scope for the API key
- `ttl_hours` (optional): Time-to-live in hours for the API key

**Response:**
```json
{
  "api_key": "string",
  "key_id": "string"
}
```

**Example:**
- Input: `{"user_id": "user-123", "scope": "read", "ttl_hours": 24}`
- Output: `{"api_key": "generated_key_value", "key_id": "request_id"}`



## API Documentation Endpoints

### GET /openapi.json
Returns the OpenAPI 3.0 specification for all available endpoints with detailed parameter descriptions, validation constraints, and examples extracted from tool function docstrings.

### GET /docs
Interactive API documentation interface (Swagger UI) with comprehensive tool descriptions and examples.

### GET /mcp-tools
Returns the MCP tools specification following the Model Context Protocol with full metadata including:
- Tool names, descriptions and annotations
- Input schemas with parameter types and constraints
- Tagging information for tool categorization
- Example usage patterns

## Error Handling

All endpoints return structured error responses when something goes wrong:

```json
{
  "success": false,
  "error": {
    "message": "Error message",
    "error_code": "ERROR_CODE",
    "request_id": "request-id"
  }
}
```

## Tool Parameters and Validation

MCP tools follow fastMCP patterns for parameter validation:

- **Annotated Parameters:** All parameters use `Annotated` with `Field` for detailed descriptions
- **Type Safety:** Strong typing with validation constraints (min/max values, patterns, etc.)
- **Default Values:** Optional parameters with sensible defaults clearly documented
- **Required Parameters:** Required parameters clearly marked without defaults

## Examples and Usage

### Using curl to call an MCP tool:

```bash
curl -X POST http://localhost:8000/mcp/create-api-key \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"user_id": "user-123", "scope": "read"}'
```

### Using Python with requests:

```python
import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}

data = {"user_id": "user-123", "scope": "read"}
response = requests.post("http://localhost:8000/mcp/create-api-key", json=data, headers=headers)
print(response.json())
```

### Using MCP Client (fastMCP):

```python
from fastmcp import Client

async with Client("http://localhost:8000") as client:
    # List all available tools
    tools = await client.list_tools()

    # Call a tool
    result = await client.call_tool("create-api-key", {
        "user_id": "user-123",
        "scope": "read",
        "ttl_hours": 24
    })

    print(result.data)
```

## Development Notes

- All MCP tools follow fastMCP patterns with detailed docstrings and metadata
- Tools use `@mcp.tool` decorator with name, description, tags, and annotations
- Parameters are annotated with `Annotated[str, Field(description="...", default="...")]`
- Return types are properly typed for structured content generation
- Tools implement proper error handling with structured error responses
- MCP context is available for logging, progress reporting, and resource access