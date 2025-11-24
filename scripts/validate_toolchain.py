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