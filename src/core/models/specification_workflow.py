from dataclasses import dataclass
from typing import NewType

from .specification_result import SaveDirectoryPath

BusinessRequirements = NewType('BusinessRequirements', str)

@dataclass(frozen=True)
class SpecificationWorkflowDefinition:
    requirements: BusinessRequirements
    save_directory: SaveDirectoryPath = SaveDirectoryPath("ctxfy/specifications/")

    def with_updated_requirements(self, new_requirements: str) -> "SpecificationWorkflowDefinition":
        return SpecificationWorkflowDefinition(
            requirements=BusinessRequirements(new_requirements),
            save_directory=self.save_directory
        )

    def with_updated_save_directory(self, new_directory: str) -> "SpecificationWorkflowDefinition":
        return SpecificationWorkflowDefinition(
            requirements=self.requirements,
            save_directory=SaveDirectoryPath(new_directory)
        )