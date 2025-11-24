from dataclasses import dataclass
from typing import NewType

SpecificationId = NewType('SpecificationId', str)
SpecificationContent = NewType('SpecificationContent', str)
SpecificationFilename = NewType('SpecificationFilename', str)
SaveDirectoryPath = NewType('SaveDirectoryPath', str)

@dataclass(frozen=True)
class SpecificationResult:
    id: SpecificationId
    content: SpecificationContent
    filename: SpecificationFilename

    def with_updated_content(self, new_content: str) -> "SpecificationResult":
        return SpecificationResult(
            id=self.id,
            content=SpecificationContent(new_content),
            filename=self.filename
        )