from typing import Any, Dict, Protocol

from fastmcp import Context


class ProcessTaskCommandPort(Protocol):
    async def execute(self, ctx: Context, file_path: str) -> Dict[str, Any]:
        ...