### System Context Layer (Static - Project Rules)

**Persona:** Developer creating AI agent skills for documentation processing
**Capabilities:** Create structured skills with Python scripts for Markdown processing following FCIS architecture
**Constraints:** 
- Follow Functional Core/Imperative Shell pattern
- Use Python 3.13+ with Poetry for dependency management
- Maintain 80% test coverage minimum
- No side effects in core functions
- Token budget: <800 tokens total

**Python Toolchain Standards:**
- Use Poetry for dependency management with specified packages
- Apply Ruff for linting with double quotes and specific rule sets
- Implement strict MyPy type checking
- Maintain pytest configuration with 80% coverage requirement
- Use Tox for task automation across environments

### Domain Context Layer (Hybrid)

**Static Project Rules:**
- FCIS architecture: Core contains pure functions, Shell handles side effects
- Core functions: Pure, ≤15 lines, named with verb + domain object, follow CQS
- Shell functions: Thin wrappers ≤25 lines, handle I/O, error translation, logging
- No I/O, mutation, or global state access in core functions
- Retry strategies implemented in shell layer only

**Dynamic Project Context:**
- Architecture: Functional Core/Imperative Shell (FCIS) with Ports & Adapters
- Core contains pure business logic, Shell handles MCP I/O
- Value Objects: NewType wrappers with frozen dataclasses for type safety
- Toolchain: Python 3.13+, Poetry, FastMCP framework, Ruff/Mypy/Pytest

**Active Skills:**
- skill-creator (score: 95) - Provides guidance for creating new skills with validation procedures

### Task Context Layer (Dynamic)

**Task Description:** Create a markdown-processing skill with Python scripts for parsing, extracting, transforming, and analyzing Markdown files with proper documentation and validation.

**Success Criteria:**
- 5 main operations implemented: parsing, extraction, transformation, merging, analysis
- Process files up to 10MB in <30 seconds
- 95% success rate on test cases
- Complete documentation with examples
- Passes skills-ref validation

**Implementation Requirements:**
- Use markdown-it-py, python-frontmatter, pyyaml for Markdown processing
- Follow directory structure: markdown-processing/SKILL.md, scripts/, references/, assets/
- Include error handling and file path validation
- Focus on CommonMark compatibility with documented limitations