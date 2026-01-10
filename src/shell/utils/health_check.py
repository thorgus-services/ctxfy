import json
import os
import tempfile
from datetime import datetime, timezone
from typing import Any, Dict, Optional

HEALTH_STATUS_FILE = os.path.join(tempfile.gettempdir(), "ctxfy_health_status.json")


def update_health_status(status: str = "healthy", checks: Optional[Dict[str, Any]] = None, mcp_uptime: float = 0.0) -> None:
    if checks is None:
        checks = {}

    health_data = {
        "status": status,
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mcp_uptime": mcp_uptime,
        "checks": checks
    }

    try:
        with open(HEALTH_STATUS_FILE, 'w') as f:
            json.dump(health_data, f)
    except Exception as e:
        import logging
        logging.error(f"Error writing health status file: {e}")


def read_health_status() -> Dict[str, Any]:
    try:
        with open(HEALTH_STATUS_FILE, 'r') as f:
            result: Dict[str, Any] = json.load(f)
            return result
    except FileNotFoundError:
        error_result: Dict[str, Any] = {
            "status": "unhealthy",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mcp_uptime": 0.0,
            "checks": {"file": "missing"}
        }
        return error_result
    except Exception as e:
        exception_result: Dict[str, Any] = {
            "status": "unhealthy",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mcp_uptime": 0.0,
            "checks": {"error": str(e)}
        }
        return exception_result


def perform_health_checks() -> Dict[str, str]:
    checks = {}

    try:
        prompt_path = os.environ.get('PROMPTS_FILE_PATH', 'resources/prompts.yaml')
        checks["dependencies"] = "ok" if os.path.exists(prompt_path) else "missing_prompts"
    except Exception as e:
        checks["dependencies"] = f"error: {str(e)}"

    try:
        from src.settings import Settings
        Settings()  # Validate that settings can be loaded
        checks["configuration"] = "ok"
    except ImportError:
        checks["configuration"] = "missing_settings_module"
    except Exception as e:
        checks["configuration"] = f"invalid_configuration: {str(e)}"

    try:
        import importlib.util
        if importlib.util.find_spec("src.core") is not None:
            checks["core_import"] = "ok"
        else:
            checks["core_import"] = "missing"
    except ImportError:
        checks["core_import"] = "failed"
    except Exception as e:
        checks["core_import"] = f"error: {str(e)}"

    try:
        import importlib.util
        if importlib.util.find_spec("src.shell") is not None:
            checks["shell_import"] = "ok"
        else:
            checks["shell_import"] = "missing"
    except ImportError:
        checks["shell_import"] = "failed"
    except Exception as e:
        checks["shell_import"] = f"error: {str(e)}"

    try:
        workspace_dir = os.environ.get('WORKSPACE_DIR', '/workspace')
        checks["workspace_access"] = "ok" if os.path.exists(workspace_dir) else "workspace_missing"
    except Exception as e:
        checks["workspace_access"] = f"error: {str(e)}"

    return checks


def get_overall_status(checks: Dict[str, str]) -> str:
    overall_status = "healthy"
    for _, check_result in checks.items():
        if check_result != "ok":
            overall_status = "degraded" if overall_status == "healthy" else "unhealthy"
            break
    return overall_status