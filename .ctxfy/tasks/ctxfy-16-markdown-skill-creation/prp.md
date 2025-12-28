---
name: "prp-markdown-skill-creation"
description: "Product Requirements Prompt for creating a markdown-processing skill with Python scripts for parsing, extracting, transforming, and analyzing Markdown files with proper documentation and validation."
license: "Internal Use Only"
task_id: "ctxfy-16-markdown-skill-creation"
---

# Backend PRP: Markdown Processing Skill Creation

## 🏷️ PRP Metadata
PRP ID: PRP-MD-001
Type: Backend Development
Domain: Documentation Processing & Content Manipulation
Technology Stack: Python 3.13+/Poetry, markdown-it-py, python-frontmatter, pyyaml
Complexity Level: Medium
⚠️ PRP skill fallback used - verify architecture compliance manually

## 🎯 Business Context Layer
Business Objectives
- Create a specialized skill for processing Markdown files with Python
- Enable automation of documentation processing, content transformation and analysis
- Support CommonMark compatibility with frontmatter handling
- Provide structured content manipulation capabilities

SLAs & Performance Requirements
Availability: 100% (local execution)
Latency: <30 seconds for files up to 10MB
Throughput: Process multiple files in batch mode

## 🔧 Technical Translation
Architecture Pattern
Hexagonal Architecture with Ports & Adapters, following Functional Core & Imperative Shell (FCIS) principles

Technology Specifications
Framework: Python 3.13+ with Poetry dependency management
Markdown Library: markdown-it-py for robust CommonMark parsing
Frontmatter: python-frontmatter for YAML metadata handling
YAML: pyyaml for metadata processing

Security Specifications
File Access: Validate file paths to prevent path traversal attacks
Input Validation: Sanitize Markdown content to prevent injection attacks

## 📝 Specification Output
Expected Deliverables (⭐ = mandatory for simple tasks)
⭐ Directory structure: markdown-processing/SKILL.md, scripts/, references/, assets/
⭐ 5 Python scripts: extract_elements.py, transform_content.py, merge_documents.py, analyze_structure.py, parse_content.py
⭐ SKILL.md with frontmatter containing name and description
⭐ API reference documentation in references/
⭐ Template assets in assets/templates/

Code Structure Guidelines
- Core functions in scripts/ should be pure (no I/O operations)
- Shell functions handle file I/O, error handling, and logging
- Use Value Objects with @dataclass(frozen=True) for structured data
- Follow naming conventions: *CommandPort, *RepositoryPort for ports

## ✅ Validation Framework
Testing Strategy (⭐ = mandatory for simple tasks)
⭐ Unit Testing: Test core parsing and transformation functions (≥70% of test suite)
⭐ Integration Testing: Test file I/O operations and script combinations (≤25% of test suite)
⭐ Acceptance Testing: Validate complete skill functionality with skills-ref validate

Quality Gates (⭐ = mandatory for simple tasks)
⭐ Code Quality: Pass Ruff linting with line-length=88
⭐ Type Safety: Pass MyPy strict mode checking
⭐ Architecture Compliance: Verify FCIS patterns and port naming conventions
⭐ Documentation: 100% of functions documented with examples

## ✨ AI Context Adaptation
Model Compatibility Notes
Claude 3: Excellent for structured skill creation with specific file layouts
GPT-4: Good for understanding complex Markdown parsing requirements
Gemini: Adequate for basic skill structure generation

Context Drift Mitigation
Include specific dependency versions (markdown-it-py, python-frontmatter, pyyaml)
Specify exact directory structure requirements
Define clear success criteria with measurable metrics

## 📋 STATIC PROJECT RULES
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

## 🔄 CURRENT PROJECT CONTEXT
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

## 📊 Success Metrics
Performance Metrics (⭐ = mandatory for simple tasks)
- Process files up to 10MB in <30 seconds
- 95% success rate on test cases with different Markdown formats

Quality & Reliability Metrics (⭐ = mandatory for simple tasks)
- 100% of functions documented with examples
- Skill passes skills-ref validation without errors
- 80% test coverage minimum maintained

Business Impact Metrics
- Skill adoption rate by other developers
- Time saved in documentation processing workflows

## ✅ Architecture Compliance Checklist
- [ ] Core functions are pure (no I/O operations)
- [ ] Shell functions are thin wrappers (≤25 lines)
- [ ] Value objects use @dataclass(frozen=True)
- [ ] Primary ports named as *CommandPort, *QueryPort
- [ ] Secondary ports named as *GatewayPort, *RepositoryPort
- [ ] Test distribution: 70% unit, 25% integration, 5% e2e
- [ ] Dependencies specified explicitly in pyproject.toml
- [ ] Ruff and MyPy configurations included
- [ ] Success criteria are measurable with specific metrics
- [ ] Architecture compliance validated against static rules