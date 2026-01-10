🏷️ PRP METADATA
PRP ID: PRP-DOCKER-CTXFY-20
Type: Backend Development
Domain: Containerization
Technology Stack: Python 3.13/FastMCP/Docker
Complexity Level: Medium

🎯 BUSINESS CONTEXT LAYER
Business Objectives
- [ ] Docker image of ctxfy MCP server available in registry for consistent deployment
- [ ] Container supports STDIO transport for MCP client communication
- [ ] Isolated runtime environment with dependency management
- [ ] Support for file volume mounting for local workspace access
- [ ] Secure handling of sensitive environment variables (API keys, tokens)

SLAs & Performance Requirements
- Image size: ≤ 500MB for fast downloads
- Startup time: < 5 seconds on standard hardware
- Concurrency: Support 10+ simultaneous requests without degradation
- Registry availability: 100% during development cycles

🔧 TECHNICAL TRANSLATION
Architecture Pattern
- Follow existing src/core and src/shell separation in containerized environment
- Maintain FCIS principles with pure core functions and thin shell adapters
- Preserve existing port naming conventions (*CommandPort, *RepositoryPort)

Technology Specifications
- Base image: python:3.13-slim for minimal footprint
- Dependencies: Managed via Poetry with lock file
- Entrypoint: src/app.py with run_stdio_server() function
- Configuration: Environment variables via pydantic-settings

Specification Output
📝 SPECIFICATION OUTPUT
Expected Deliverables
- [ ] Dockerfile in project root with multi-stage build
- [ ] .dockerignore file mirroring .gitignore patterns
- [ ] docker-compose.yml for local development
- [ ] Documentation with usage examples in README.md
- [ ] Health check endpoint implementation

Code Structure Guidelines
- Multi-stage build: builder stage for dependencies, runtime stage for execution
- Copy only necessary files (pyproject.toml, poetry.lock, src/, resources/)
- Use non-root user for security (UID/GID 1000)
- Volume mount points for /workspace and /config

✅ VALIDATION FRAMEWORK
Testing Strategy
- [ ] Unit tests passing inside container environment
- [ ] Integration tests validating STDIO communication
- [ ] Size validation ensuring image stays under 500MB
- [ ] Startup time measurement under 5 seconds
- [ ] Functionality validation: all MCP server capabilities work in container

Quality Gates
- [ ] Ruff formatting compliance (line-length=88) maintained
- [ ] MyPy strict type checking passes in container
- [ ] Security scan with Bandit passes in container
- [ ] Dependency vulnerability scan with Safety passes

✨ AI CONTEXT ADAPTATION
Model Compatibility Notes
- Claude 3: Excellent for Dockerfile optimization and multi-stage builds
- Include specific Python version (3.13) and FastMCP dependency requirements

📊 SUCCESS METRICS
Performance Metrics
- Image build time: < 5 minutes on standard hardware
- Image size: ≤ 500MB compressed
- Startup time: < 5 seconds from docker run

Quality & Reliability Metrics
- 100% of existing tests pass in containerized environment
- Zero security vulnerabilities detected by Bandit/Safety scans
- Proper isolation: container cannot affect host system

📋 ARCHITECTURE COMPLIANCE CHECKLIST
- [ ] FCIS patterns properly implemented in src/core and src/shell separation in container
- [ ] Port naming conventions followed in src/core/ports implementations
- [ ] Test distribution requirements met with 70/25/5 ratio maintained in container
- [ ] Value objects are immutable in src/core/models with @dataclass(frozen=True)
- [ ] Core functions are pure in src/core/ with no I/O operations
- [ ] Token budget under 1000 tokens