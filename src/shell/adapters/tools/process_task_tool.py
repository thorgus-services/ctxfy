import os
from pathlib import Path
from typing import Any, Dict

from fastmcp import Context

from src.core.ports.task_ports import ProcessTaskCommandPort
from src.core.use_cases.process_task_use_case import ProcessTaskUseCase


class ProcessTaskTool(ProcessTaskCommandPort):
    def __init__(self, use_case: ProcessTaskUseCase):
        self.use_case = use_case

    async def execute(
        self,
        ctx: Context,
        file_path: str
    ) -> Dict[str, Any]:
        await ctx.info(f"Starting task processing for file: {file_path}")

        workspace_dir = os.environ.get('WORKSPACE_DIR', os.getcwd())

        full_file_path = self._resolve_file_path(file_path, workspace_dir)

        try:
            task_metadata = self.use_case.execute(full_file_path)
        except Exception as e:
            await ctx.error(f"Error processing task file: {str(e)}")
            raise

        task_dir = self._create_task_directory(workspace_dir, task_metadata.task_directory_path)

        self._save_file_with_standardized_name(full_file_path, task_dir)

        await ctx.info(f"Task processed with ID: {task_metadata.id}")

        return {
            "task_id": task_metadata.id,
            "title": task_metadata.title,
            "summary": task_metadata.summary,
            "original_file_path": task_metadata.original_file_path,
            "task_directory_path": str(task_dir),
            "created_at": task_metadata.created_at
        }

    def _resolve_file_path(self, file_path: str, workspace_dir: str) -> str:
        if not Path(file_path).is_absolute():
            return os.path.join(workspace_dir, file_path)
        return file_path

    def _create_task_directory(self, workspace_dir: str, task_directory_path: str) -> Path:
        task_dir = Path(workspace_dir) / task_directory_path
        task_dir.mkdir(parents=True, exist_ok=True)
        return task_dir

    def _save_file_with_standardized_name(self, source_file_path: str, destination_dir: Path) -> None:
        source_file = Path(source_file_path)
        destination_file = destination_dir / "original-task.md"
        destination_file.write_text(source_file.read_text(encoding='utf-8'), encoding='utf-8')