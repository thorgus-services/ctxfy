from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def get_project_root(marker_files: tuple[str, ...] = ('pyproject.toml', '.git', 'Pipfile', 'setup.py')) -> Path:
    current_path = Path(__file__).resolve()

    for parent in [current_path] + list(current_path.parents):
        for marker in marker_files:
            if (parent / marker).exists():
                return parent

    raise RuntimeError(
        f"Could not find project root. Looked for: {', '.join(marker_files)}. "
        f"Started from: {current_path}"
    )