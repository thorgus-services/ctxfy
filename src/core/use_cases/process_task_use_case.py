from datetime import datetime, timezone
from pathlib import Path

from ..models.task_metadata import (
    TaskDirectoryPath,
    TaskFilePath,
    TaskMetadata,
    TaskSummary,
    TaskTitle,
)


class ProcessTaskUseCase:
    def execute(self, file_path: str) -> TaskMetadata:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")

        content = path.read_text(encoding='utf-8')
        title = self._extract_title(content)
        summary = self._extract_summary(content)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        task_id = TaskMetadata.generate_task_id(content, timestamp)
        task_dir_path = TaskDirectoryPath(f".ctxfy/tasks/{task_id}/")

        return TaskMetadata(
            id=task_id,
            title=title,
            summary=summary,
            original_file_path=TaskFilePath(file_path),
            task_directory_path=task_dir_path,
            created_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        )

    def _extract_title(self, content: str) -> TaskTitle:
        lines = content.strip().split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                title = stripped.lstrip('# ').strip()
                return TaskTitle(title)
            elif stripped:
                return TaskTitle(stripped[:100])

        return TaskTitle("Untitled Task")

    def _extract_summary(self, content: str) -> TaskSummary:
        lines = content.strip().split('\n')
        content_lines = []

        for i, line in enumerate(lines):
            if i == 0 and line.strip().startswith('#'):
                continue
            content_lines.append(line)

        content_body = '\n'.join(content_lines).strip()
        paragraphs = content_body.split('\n\n')
        first_paragraph = paragraphs[0].strip() if paragraphs and paragraphs[0].strip() else content_body[:200]

        if len(first_paragraph) > 197:
            summary = first_paragraph[:197] + "..."
        else:
            summary = first_paragraph

        return TaskSummary(summary)