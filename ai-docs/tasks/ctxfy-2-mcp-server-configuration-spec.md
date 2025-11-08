# Technical Specification: MCP Server Configuration for Qwen Code

## 1. Overview

### 1.1 Purpose
This document specifies the technical implementation of MCP (Model Context Protocol) Server Configuration in Qwen Code with STDIO transport. The specification aims to enable system administrators to configure MCP Servers easily, allowing developers to connect external tools and data sources with minimal setup effort.

### 1.2 Scope
This specification covers:
- Configuration template for MCP servers in `.qwen/settings.json`
- STDIO transport implementation
- Cross-platform compatibility (macOS and Linux)
- Connection validation mechanism
- Integration with Qwen Code's tool discovery system

### 1.3 Context
The Model Context Protocol provides a standardized way for AI applications to connect to external systems. MCP servers expose capabilities to AI applications through three main types of features: Tools, Resources, and Prompts. This specification focuses on enabling STDIO transport for MCP servers in Qwen Code, allowing seamless integration with various external systems.

## 2. Architecture Overview

### 2.1 Core Components
Based on the architectural principles defined in the project rules, the MCP Server Configuration will implement a clear separation between:

**Functional Core**:
- Configuration validation logic
- Template generation functions
- Connection validation algorithms

**Imperative Shell**:
- File I/O operations for settings.json
- Process management for STDIO transport
- Error handling and logging

### 2.2 Integration Points
The MCP Server Configuration integrates with Qwen Code at the following points:
- `packages/core/src/tools/mcp-client.ts` - Discovery and connection management
- `packages/core/src/tools/mcp-tool.ts` - Tool execution wrapper
- Qwen Code settings system for `.qwen/settings.json` configuration

### 2.3 Transport Mechanism
The specification implements STDIO transport, which:
- Spawns MCP server processes as subprocesses
- Communicates via stdin/stdout using JSON-RPC protocol
- Maintains one-to-one connection between client and server

## 3. Functional Requirements

### 3.1 Configuration Template
**Requirement**: System shall provide a template configuration in `.qwen/settings.json` for MCP Servers

**Implementation**:
- Create default configuration structure with all required fields
- Include examples and documentation within the template
- Support multiple MCP server configurations in a single settings file

**Technical Details**:
```json
{
  "mcpServers": {
    "example-server": {
      "command": "path/to/server-executable",
      "args": ["--arg1", "value1"],
      "env": {
        "API_KEY": "$MY_API_TOKEN"
      },
      "cwd": "./server-directory",
      "timeout": 30000,
      "trust": false
    }
  }
}
```

### 3.2 STDIO Transport Support
**Requirement**: System shall support STDIO transport for MCP server connections

**Implementation**:
- Implement process spawning mechanism for server executables
- Establish bidirectional communication via stdin/stdout
- Handle JSON-RPC message framing and parsing
- Implement connection lifecycle management (connect, disconnect, reconnect)

**Technical Details**:
- Use subprocess module to spawn server processes
- Implement non-blocking I/O for stdin/stdout communication
- Handle JSON-RPC 2.0 protocol compliance
- Include timeout and error handling mechanisms

### 3.3 Connection Validation
**Requirement**: System shall provide a validation mechanism using `/mcp` command

**Implementation**:
- Create `/mcp` verification command in Qwen Code
- Implement server discovery and health check
- Display connection status and server information
- Provide troubleshooting diagnostics

**Technical Details**:
- Query MCP client registry for active connections
- Check connection status and server responsiveness
- Report discovered tools and capabilities
- Display error messages for failed connections

## 4. Non-Functional Requirements

### 4.1 Cross-Platform Compatibility
**Requirement**: Configuration must work on macOS and Linux environments

**Implementation Strategy**:
- Use cross-platform path handling
- Implement shell-agnostic command execution
- Account for platform-specific environment variables
- Test configuration on both platform types

### 4.2 Security
**Requirement**: Ensure secure connection mechanisms

**Implementation Strategy**:
- Isolate MCP server processes with limited permissions
- Validate server trust settings
- Handle sensitive environment variables securely
- Implement connection validation and authentication

### 4.3 Performance
**Requirement**: Efficient discovery and connection establishment

**Implementation Strategy**:
- Implement connection pooling for active servers
- Cache discovered tool schemas
- Optimize startup time for server connections
- Provide async connection establishment

## 5. Implementation Details

### 5.1 Configuration Structure
The configuration system will implement the following structure:

**Settings Template** (`~/.qwen/settings.json` or `./.qwen/settings.json`):
```json
{
  "mcpServers": {
    "serverName": {
      "command": "path/to/server",
      "args": ["--arg1", "value1"],
      "env": {
        "API_KEY": "$MY_API_TOKEN"
      },
      "cwd": "./server-directory",
      "timeout": 30000,
      "trust": false
    }
  }
}
```

### 5.2 Discovery Process
The discovery process will follow these steps:

1. Read `mcpServers` configuration from settings
2. For each configured server:
   - Validate configuration structure
   - Spawn server process using `command` and `args`
   - Establish STDIO communication channel
   - Send `tools/list` request to discover available tools
   - Validate tool schemas for compatibility
   - Register tools in global tool registry
3. Handle connection errors and retries

### 5.3 Execution Layer
Each discovered MCP tool is wrapped in a `DiscoveredMCPTool` instance that:

- Handles confirmation logic based on server trust settings
- Manages tool execution by calling the MCP server with proper parameters
- Processes responses for both LLM context and user display
- Maintains connection state and handles timeouts

## 6. Setup Process

The implementation provides a simple 5-step setup process:

### Step 1: Install MCP Server
```bash
# Install your MCP server executable
npm install -g your-mcp-server
# or download the appropriate binary for your platform
```

### Step 2: Create Configuration File
Create or edit `.qwen/settings.json` in your project root:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "/path/to/your/server",
      "args": ["--port", "8080"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Step 3: Validate Configuration
Use the `/mcp` command in Qwen Code to verify the connection:

```bash
/mcp
```

### Step 4: Test Connection
The system will:
- Establish connection to configured MCP servers
- Discover available tools
- Report successful connections

### Step 5: Begin Usage
The configured tools will be available for use in Qwen Code conversations.

## 7. Testing Strategy

### 7.1 Unit Tests (≥70% of suite)
- Test configuration validation functions
- Validate template generation logic
- Test connection establishment algorithms

### 7.2 Integration Tests (≤25%)
- Test Core + Adapter combinations
- Verify file I/O operations
- Test process spawning and communication

### 7.3 End-to-End Tests (≤5%)
- Full workflow validation
- Cross-platform compatibility verification
- Connection validation command testing

## 8. Validation Criteria

### 8.1 Acceptance Criteria Verification
- [ ] Template configuration exists in `.qwen/settings.json` for MCP Server
- [ ] Configuration includes only necessary command and arguments for STDIO transport
- [ ] Connection validation possible with `/mcp` command in Qwen Code
- [ ] Configuration works in macOS and Linux environments
- [ ] Documentation provides clear setup steps (maximum 5 steps)

### 8.2 Metrics Implementation
- **Setup Time**: Track average configuration setup time
- **Failure Rate**: Monitor configuration failure rate in 10 attempts
- **User Satisfaction**: Collect NPS for installation experience

## 9. Risk Assessment

### 9.1 Security Risks
- Risk: Unauthorized MCP server execution
- Mitigation: Implement trust verification and user consent mechanisms

### 9.2 Compatibility Risks
- Risk: Platform-specific implementation issues
- Mitigation: Thorough testing across supported platforms

### 9.3 Performance Risks
- Risk: Slow connection establishment affecting user experience
- Mitigation: Asynchronous connection handling and connection caching

## 10. Implementation Timeline

Phase 1 (Days 1-2): Core configuration and template system
Phase 2 (Day 3): STDIO transport implementation
Phase 3 (Day 4): Connection validation and testing
Phase 4 (Day 5): Documentation and validation