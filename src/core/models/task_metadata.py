import hashlib
from dataclasses import dataclass
from typing import NewType

TaskId = NewType('TaskId', str)
TaskTitle = NewType('TaskTitle', str)
TaskSummary = NewType('TaskSummary', str)
TaskFilePath = NewType('TaskFilePath', str)
TaskDirectoryPath = NewType('TaskDirectoryPath', str)


@dataclass(frozen=True)
class TaskMetadata:
    """Immutable value object for task metadata"""
    id: TaskId
    title: TaskTitle
    summary: TaskSummary
    original_file_path: TaskFilePath
    task_directory_path: TaskDirectoryPath
    created_at: str

    def with_updated_summary(self, new_summary: str) -> "TaskMetadata":
        """Create a new instance with updated summary"""
        return TaskMetadata(
            id=self.id,
            title=self.title,
            summary=TaskSummary(new_summary),
            original_file_path=self.original_file_path,
            task_directory_path=self.task_directory_path,
            created_at=self.created_at
        )

    @staticmethod
    def generate_task_id(content: str, timestamp: str) -> TaskId:
        """Generate unique task ID using timestamp and content hash"""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        task_id_str = f"{timestamp}_{content_hash}"
        return TaskId(task_id_str)