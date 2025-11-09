#!/usr/bin/env python3
"""
Example script to demonstrate the MCP Context Stack Generator.

This script shows how to run the MCP server that generates context stacks
for Qwen Code based on feature descriptions using HTTP transport.
"""

from src.mcp_server import ContextStackServer

def main():
    print("Starting MCP Context Stack Generator Server...")
    print("Server will be available via HTTP transport")
    print("\nThe server implements the Model Context Protocol (MCP) standard.")
    print("Available tools: generate_context_stack, execute_prp_workflow")
    print("\nThe server uses HTTP transport for production-ready deployments.")
    
    server = ContextStackServer()
    server.run()

if __name__ == "__main__":
    main()