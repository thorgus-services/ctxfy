#!/usr/bin/env python3
"""
Example script to demonstrate the MCP Context Stack Generator.

This script shows how to run the MCP server that generates context stacks
for Qwen Code based on feature descriptions.
"""

from src.mcp_server import MCPServer

def main():
    print("Starting MCP Context Stack Generator Server...")
    print("Server will be available at http://127.0.0.1:8000")
    print("\nAvailable endpoints:")
    print("  GET  /tools/list  - List available tools")
    print("  POST /tools/call  - Call a tool")
    print("\nThe server implements the Model Context Protocol (MCP) standard.")
    print("Available tool: generate_context_stack")
    print("\nTo test the server, you can use curl:")
    print("  curl -X POST http://127.0.0.1:8000/tools/call \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"name\": \"generate_context_stack\", \"arguments\": {\"feature_description\": \"User authentication system\"}}'")
    
    server = MCPServer()
    server.run()

if __name__ == "__main__":
    main()