# TECHNICAL SPECIFICATION: ctxfy MCP Server Production Preparation and Observability

## 1. Overview

This document provides the complete technical specification for preparing the ctxfy MCP (Model Context Protocol) Server for production deployment, with a focus on documentation, monitoring, security, and observability. The implementation follows Hexagonal Architecture and Functional Core & Imperative Shell patterns as specified in the project rules.

### 1.1 Purpose
- Prepare the MCP server for production deployment with proper documentation, monitoring, and security
- Implement OpenAPI 3.0 documentation generation for MCP endpoints and prompts
- Establish structured logging with JSON format including request IDs and latency metrics
- Add authentication middleware (API keys) and schema validation for prompt requests
- Create Docker deployment script and CI/CD pipeline integration

### 1.2 Scope
- OpenAPI 3.0 documentation generation at `/docs`
- Advanced JSON logging with request IDs and latency tracking
- Authentication middleware with API key support
- Schema validation for prompt requests
- Docker containerization and deployment pipeline
- Health monitoring and metrics collection

## 2. Architecture

### 2.1 Hexagonal Architecture Structure

```
src/
├── core/                 # Pure domain: functions, value objects, exceptions
│   ├── models/           # Immutable value objects and entities
│   │   ├── prompt_models.py     # PromptRequest, PromptTemplate, etc.
│   │   ├── auth_models.py       # Authentication-related models
│   │   └── monitoring_models.py # Monitoring and logging models
│   ├── use_cases/        # Pure functions implementing business rules
│   │   ├── prompt_use_cases.py  # Prompt processing logic
│   │   ├── auth_use_cases.py    # Authentication logic
│   │   └── monitoring_use_cases.py # Monitoring logic
│   └── ports/            # Interfaces only (Protocols)
│       ├── prompt_ports.py      # PromptCommandPort, PromptQueryPort
│       ├── auth_ports.py        # Authentication ports
│       └── monitoring_ports.py  # Monitoring ports
├── adapters/             # Implementations of core ports
│   ├── mcp_prompts/      # @mcp.prompt decorator implementation
│   ├── auth/             # Authentication middleware and API key management
│   ├── monitoring/       # Logging, metrics, and health monitoring
│   ├── api_docs/         # OpenAPI documentation generation
│   ├── validation/       # Schema validation for prompt requests
│   └── container/        # Docker containerization support
└── app/                  # Application composition and configuration
    ├── main.py           # Main entry point with dependency injection
    ├── config.py         # Configuration management
    └── deployment/       # Deployment scripts and configurations
```

### 2.2 Core Components

#### 2.2.1 Core Ports (`src/core/ports/auth_ports.py`)
- `AuthCommandPort`: Primary port for authentication operations
  - `validate_api_key(api_key: str) -> bool`
  - `create_api_key(user_id: str) -> str`
- `AuthQueryPort`: Primary port for authentication information queries
  - `get_api_key_info(api_key: str) -> Optional[ApiKeyInfo]`
  - `list_user_api_keys(user_id: str) -> List[ApiKeyInfo]`

#### 2.2.2 Core Ports (`src/core/ports/monitoring_ports.py`)
- `LoggingPort`: Primary port for structured logging operations
  - `log_request(request_id: str, endpoint: str, latency_ms: float, user_id: Optional[str]) -> None`
  - `log_error(request_id: str, error: Exception, context: Dict[str, Any]) -> None`
- `MetricsPort`: Primary port for metrics collection
  - `record_prompt_execution(template_id: str, latency_ms: float, success: bool) -> None`
  - `record_api_key_usage(api_key: str, endpoint: str) -> None`

#### 2.2.3 Core Models (`src/core/models/auth_models.py`)
- `ApiKeyInfo`: Immutable value object for API key information
  - `key_id: str` - Unique identifier for the API key
  - `api_key: str` - The actual API key (hashed)
  - `user_id: str` - Associated user ID
  - `created_at: datetime` - Creation timestamp
  - `last_used_at: Optional[datetime]` - Last usage timestamp
  - `expires_at: Optional[datetime]` - Expiration timestamp
  - `scope: str` - Access scope (read, write, admin)
- `ApiKeyRequest`: Immutable value object for API key requests
  - `user_id: str` - Requesting user ID
  - `scope: str` - Desired access scope
  - `ttl_hours: Optional[int]` - Time-to-live in hours

#### 2.2.4 Core Models (`src/core/models/monitoring_models.py`)
- `LogEntry`: Immutable value object for structured logging
  - `timestamp: datetime` - Log entry timestamp
  - `level: str` - Log level (INFO, ERROR, DEBUG, etc.)
  - `message: str` - Log message
  - `request_id: str` - Unique request identifier
  - `latency_ms: float` - Request processing time in milliseconds
  - `user_id: Optional[str]` - Associated user ID
  - `endpoint: str` - Requested endpoint
  - `llm_model: Optional[str]` - LLM model used (if any)
  - `extra: Dict[str, Any]` - Additional context-specific fields
- `Metric`: Immutable value object for metrics collection
  - `name: str` - Metric name
  - `value: float` - Metric value
  - `labels: Dict[str, str]` - Metric labels for dimensioning
  - `timestamp: datetime` - Metric collection timestamp

#### 2.2.5 Core Models (`src/core/models/validation_models.py`)
- `ValidationError`: Immutable value object for validation errors
  - `field: str` - Field that failed validation
  - `message: str` - Error message
  - `code: str` - Error code
- `ValidationResult`: Immutable value object for validation results
  - `is_valid: bool` - Whether validation passed
  - `errors: Tuple[ValidationError, ...]` - List of validation errors

### 2.3 Adapters

#### 2.3.1 Authentication Adapter (`src/adapters/auth/middleware.py`)
- Implements authentication middleware using API keys
- Validates API keys in request headers
- Integrates with FastMCP's authentication system
- Provides token validation and scope checking
- Supports both static API keys and dynamic token validation

#### 2.3.2 Structured Logging Adapter (`src/adapters/monitoring/structured_logger.py`)
- Implements JSON structured logging with required fields
- Includes request_id, latency_ms, and llm_model in logs
- Follows standard log format for observability systems
- Supports correlation IDs across distributed systems
- Integrates with external logging services (ELK, Datadog, etc.)

#### 2.3.3 Metrics Adapter (`src/adapters/monitoring/metrics_collector.py`)
- Collects performance metrics using Prometheus or similar
- Tracks prompt execution times, success rates, and resource usage
- Records API key usage patterns
- Provides health check endpoint with system metrics
- Supports metric export for monitoring dashboards

#### 2.3.4 OpenAPI Documentation Adapter (`src/adapters/api_docs/openapi_generator.py`)
- Generates OpenAPI 3.0 documentation for MCP endpoints
- Documents `@mcp.prompt` endpoints with examples
- Shows available prompts and their parameters
- Provides interactive documentation interface at `/docs`
- Automatically updates based on registered prompts

#### 2.3.5 Schema Validation Adapter (`src/adapters/validation/schema_validator.py`)
- Implements schema validation for prompt requests
- Validates prompt parameters against defined schemas
- Provides detailed error messages for invalid requests
- Integrates with Pydantic for validation logic
- Supports JSON Schema for compatibility with MCP clients

## 3. Implementation Details

### 3.1 Project Dependencies (`pyproject.toml`)
```toml
[tool.poetry.dependencies]
python = "^3.13"
fastmcp = "^2.13.0"
pydantic-settings = "^2.12"
pydantic = "^2.12"
uvicorn = "^0.34.0"
prometheus-client = "^0.22.0"
structlog = "^24.4.0"
cryptography = "^42.0.0"

[tool.poetry.group.dev.dependencies]
ruff = "^0.14"
mypy = "^1.18"
pytest = "^8.4"
pytest-cov = "^5.0"
bandit = "^1.7"
safety = "^2.3"
```

### 3.2 Server Configuration (`fastmcp.json`)
- Server configuration with host, port, CORS settings
- Logging configuration with JSON formatter
- Authentication settings with API key configuration
- Monitoring settings with metrics endpoint
- LLM settings with default model and timeout

### 3.3 Entry Point (`app/main.py`)
- Initializes FastMCP server with authentication middleware
- Sets up health check endpoint at `/health`
- Configures structured logging with request correlation
- Sets up OpenAPI documentation at `/docs`
- Implements example prompts with security validation

### 3.4 Endpoints
- `/mcp`: MCP protocol endpoint (handled automatically by FastMCP)
- `/health`: Health check with metrics and system status
- `/docs`: OpenAPI 3.0 documentation interface
- `/metrics`: Prometheus metrics endpoint
- `/auth/api-keys`: API key management endpoints

## 4. Authentication & Security

### 4.1 API Key Management
- Generation of secure API keys using cryptographic functions
- Support for different scopes (read, write, admin)
- Expiration and rotation mechanisms
- Rate limiting per API key
- Audit logging for key usage

### 4.2 Authentication Middleware
- Middleware that checks for valid API keys in request headers
- Compatible with standard Authorization header format
- Per-route authentication requirements
- Integration with FastMCP's authentication system
- Support for multiple authentication schemes

### 4.3 Security Headers
- Implementation of security headers (CSP, HSTS, etc.)
- CORS configuration with origin restrictions
- Input sanitization and validation
- Protection against common web vulnerabilities
- Secure session management

## 5. Monitoring & Observability

### 5.1 Structured Logging
- JSON-formatted logs with consistent structure
- Required fields: request_id, latency_ms, llm_model, timestamp, level
- Contextual information: user_id, endpoint, method, status_code
- Error logging with stack traces and context
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

### 5.2 Metrics Collection
- Request rate, error rate, and latency histograms
- Prompt execution metrics with model-specific breakdown
- API key usage patterns and resource consumption
- System-level metrics (CPU, memory, disk)
- Custom business metrics as needed

### 5.3 Health Checks
- Application health endpoint with status indicators
- Dependency health checking (databases, external services)
- Performance threshold monitoring
- Automated alerts for health issues
- Graceful degradation when dependencies fail

### 5.4 Tracing
- Request tracing across service boundaries
- Distributed tracing with correlation IDs
- Performance bottleneck identification
- Integration with tracing systems (Jaeger, Zipkin, etc.)

## 6. Documentation

### 6.1 OpenAPI 3.0 Documentation
- Auto-generated API documentation at `/docs`
- Interactive API explorer for testing endpoints
- Example requests and responses for each endpoint
- Documentation of `@mcp.prompt` parameters and examples
- Integration with FastMCP's prompt system

### 6.2 Prompt Documentation
- Automatic documentation generation for registered prompts
- Parameter descriptions and expected types
- Example usage with sample data
- Validation rules and constraints
- Integration guidance for MCP clients

### 6.3 Deployment Documentation
- Step-by-step deployment instructions
- Configuration parameters and environment variables
- Security best practices
- Troubleshooting guide
- Performance tuning recommendations

## 7. Containerization & Deployment

### 7.1 Docker Configuration
- Multi-stage Dockerfile for optimized images
- Security best practices (non-root user, minimal base image)
- Environment-specific configurations
- Health check integration
- Resource limits and constraints

### 7.2 Deployment Pipeline
- Automated testing and validation
- Security scanning (Bandit, Safety)
- Container image building and tagging
- Deployment to staging and production
- Rollback procedures and safeguards

### 7.3 Infrastructure as Code
- Docker Compose for local development
- Kubernetes manifests for production deployment
- Configuration management with environment variables
- Service discovery and load balancing
- Backup and recovery procedures

## 8. Testing Strategy

### 8.1 Unit Tests (≥70% of suite)
- Test core domain models and pure functions
- Validate authentication logic and security checks
- Verify logging and metrics collection
- Focus on pure functions in functional core
- No external dependencies or mocks

### 8.2 Integration Tests (≤25% of suite)
- Test adapter implementations with real/fake dependencies
- Verify authentication middleware functionality
- Validate API documentation generation
- Test metrics collection and export
- Use real adapters, not mocks of core logic

### 8.3 End-to-End Tests (≤5% of suite)
- Full workflow validation for critical paths
- Test complete prompt processing with authentication
- Verify documentation generation and accessibility
- Performance and load testing
- Execute against production-like environment

### 8.4 Security Testing
- API key validation and security checks
- Authentication bypass attempts
- Authorization scope validation
- Input validation and sanitization
- OWASP Top 10 vulnerability scanning

## 9. Performance Requirements

### 9.1 Latency Targets
- Prompt requests: <200ms p95 latency
- Authentication: <50ms p95 latency
- Health checks: <10ms p95 latency
- Documentation endpoints: <100ms p95 latency

### 9.2 Throughput Targets
- Support 1000+ concurrent requests
- Handle 10K+ prompt executions per minute
- Process API key validation at 5K+ requests/second
- Maintain 99.9% availability under load

### 9.3 Resource Utilization
- CPU usage <70% under peak load
- Memory usage <80% under peak load
- Response time consistency under load
- Efficient connection pooling and resource reuse

## 10. Compliance & Security

### 10.1 Security Standards
- OWASP API Security Top 10 compliance
- NIST Cybersecurity Framework alignment
- Data encryption at rest and in transit
- Regular security vulnerability scanning
- Secure configuration management

### 10.2 Audit Requirements
- Comprehensive request logging
- API key usage tracking
- Security event monitoring
- Compliance reporting
- GDPR/CCPA data handling requirements

### 10.3 Data Privacy
- Minimization of collected data
- Encrypted storage of sensitive information
- Right to deletion support
- Data retention policies
- Access control and permissions

## 11. Success Criteria

### 11.1 Technical Metrics
- 100% of endpoints secured with authentication
- OpenAPI documentation available at `/docs` with 100% prompt coverage
- JSON structured logging with all required fields implemented
- 99.9% availability in production environment
- <200ms average latency for prompt requests

### 11.2 Security Metrics
- Zero critical security vulnerabilities
- Successful authentication for all valid API keys
- Proper rate limiting and abuse prevention
- Complete audit trail for all actions
- Secure communication with TLS 1.3

### 11.3 Operational Metrics
- Automated deployment pipeline with staging/production
- Real-time monitoring and alerting
- <5 minute incident response time
- <1 hour recovery time for incidents
- Comprehensive documentation coverage

This technical specification provides a complete roadmap for preparing the ctxfy MCP Server for production deployment with robust monitoring, documentation, and security features.