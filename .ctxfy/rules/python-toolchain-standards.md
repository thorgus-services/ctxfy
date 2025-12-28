# Project Rules

## 5. Python Toolchain Standards

### Dependency Management with Poetry

This rule standardizes dependency management:

```toml
[tool.poetry.dependencies]
python = "^3.13"
pydantic-settings = "^2.12"
fastmcp = "^2.13.0"
uvicorn = "^0.34.0"
cryptography = "^44.0.1"
pydantic = "^2.12"

[tool.poetry.group.dev.dependencies]
ruff = "^0.14"
mypy = "^1.18"
pytest = "^9.0"
pytest-asyncio = "^0.25.0"
pytest-cov = "^7.0"
bandit = "^1.8"
safety = "^3.7"
tox = "^4.32.0"
```

Anti-patterns to avoid:
❌ Unversioned dependencies in pyproject.toml
❌ Manual dependency installation outside Poetry workflow

### Code Formatting and Linting

This rule standardizes code formatting. Configuration should be in pyproject.toml under [tool.ruff] section to avoid format conflicts:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "B", "C4", "T20"]
ignore = ["E501"]

[tool.ruff.lint.flake8-quotes]
inline-quotes = "double"

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__ for namespace exports
```

Common issues to address during implementation:
- Import order and grouping will be automatically fixed by Ruff
- Unused imports will be automatically removed by Ruff
- String quote styles will be enforced as double quotes

Anti-patterns to avoid:
❌ Mixing tabs and spaces (enforced by Ruff)
❌ Different formatting rules between developer machines

### Type Checking Strategy

This rule standardizes type checking:

```ini
[mypy]
strict = true
warn_unused_configs = true
disallow_any_generics = true
check_untyped_defs = true

[mypy-tests.*]
strict = false
disallow_untyped_defs = false
```

Common issues to address during implementation:
- Class constructors (`__init__`) must have explicit return type annotation (`-> None`)
- Optional parameters with default values of data types should use types from typing module (e.g., `Optional[MyType]`)
- Variables with default parameter values that are function calls should be moved to module level to avoid B008 error

Anti-patterns to avoid:
❌ Type ignores without justification comments

### Testing and Coverage

This rule standardizes testing and code coverage. Configuration should be in pyproject.toml:

```toml
[tool.pytest.ini_options]
python_files = ["test_*.py"]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=html --strict-markers"
markers = [
    "unit: Unit tests (no external dependencies)",
    "integration: Integration tests (with real/fake adapters)",
    "slow: Tests that take more than 1 second"
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true
```

Coverage requirements:
- Core packages must maintain ≥80% coverage
- No new code without tests (enforced by PR checks)
- Coverage reports published to team dashboard

### Task Automation with Tox

This rule standardizes task automation while complementing Poetry:

```ini
[tox]
envlist = lint, type, unit, security, compliance

[testenv:lint]
deps = ruff
commands = ruff check src tests

[testenv:type]
deps = mypy
commands = mypy src

[testenv:unit]
deps =
    pytest
    pytest-cov
    pytest-asyncio
commands = pytest tests/unit {posargs}

[testenv:integration]
deps =
    pytest
    pytest-cov
    pytest-asyncio
commands = pytest tests/shell {posargs}

[testenv:security]
deps =
    bandit
    safety
commands =
    bandit -c pyproject.toml -r src
    safety check --full-report

[testenv:compliance]
deps =
    requests
commands =
    python scripts/validate_toolchain.py
```

**Note:** Tox is complementary to Poetry in this workflow:
- Poetry manages dependencies and packages
- Tox automates testing across multiple environments
- Tox ≥ 4 is fully compatible with Poetry's PEP 517 build system
- Tox creates isolated environments for each validation task
- All validation tasks (including security and compliance) should be executed through Tox for consistency between local and CI environments

### Security and CI Pipeline

This rule standardizes CI validation using Tox as the single execution point:

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'

    - name: Cache Poetry dependencies
      uses: actions/cache@v3
      with:
        path: |
          ~/.cache/pypoetry/virtualenvs
          ~/.cache/pypoetry/cache
        key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}

    - name: Install Poetry
      run: pip install poetry

    - name: Install dependencies
      run: poetry install --no-interaction

    - name: Run all validations with Tox
      run: tox

    - name: Build Package
      run: poetry build
```

Security scanning configuration:
```toml
[tool.bandit]
skips = ["B101"]  # Skip assert checks in tests
exclude_dirs = ["tests", "venv"]
```

Anti-patterns to avoid:
❌ Security vulnerabilities with known CVEs
❌ Configuration values hardcoded in source files

### Toolchain Compliance Verification

This rule ensures toolchain configurations are properly maintained:

```python
# scripts/validate_toolchain.py
import os
import sys

def check_toolchain_compliance() -> tuple[bool, dict]:
    """Verifica se todas as configurações de toolchain estão presentes e corretas"""
    checks = {
        "pyproject.toml exists": os.path.exists("pyproject.toml"),
        "mypy.ini exists": os.path.exists("mypy.ini"),
        "tox.ini exists": os.path.exists("tox.ini"),
        "CI pipeline configured": os.path.exists(".github/workflows/ci.yml")
    }
    all_passed = all(checks.values())
    return all_passed, checks

if __name__ == "__main__":
    all_passed, checks = check_toolchain_compliance()
    print("Toolchain Compliance Check:")
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")

    if not all_passed:
        sys.exit(1)
```