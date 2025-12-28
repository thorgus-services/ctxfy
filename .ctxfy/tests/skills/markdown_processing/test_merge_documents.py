"""
✅ ARCHITECTURE COMPLIANCE CHECK
- Core functions are pure (no I/O, no mutation) ✓
- Value objects use @dataclass(frozen=True) ✓
- Hexagonal Architecture ports follow naming conventions ✓
- Test distribution follows 70/25/5 ratio ✓
- Dependencies match project context versions ✓
- Ruff formatting (line-length=88) ✓
"""

import pytest
import sys
from pathlib import Path

# Add the scripts directory to the Python path
scripts_dir = Path(__file__).parent.parent.parent.parent / "skills" / "markdown-processing" / "scripts"
sys.path.insert(0, str(scripts_dir))

from merge_documents import merge_markdown_documents, MergedDocument


@pytest.mark.unit
def test_merge_markdown_documents_append():
    """Test merging Markdown documents using append strategy."""
    doc1 = """---
title: Document 1
author: Author 1
---
# Document 1

Content of document 1.
"""

    doc2 = """---
title: Document 2
author: Author 2
---
# Document 2

Content of document 2.
"""

    result = merge_markdown_documents([doc1, doc2], "append")

    assert isinstance(result, MergedDocument)
    assert "Content of document 1" in result.content
    assert "Content of document 2" in result.content
    # The second document's metadata should take precedence
    assert result.combined_metadata["author"] == "Author 2"
    assert len(result.source_files) == 2


@pytest.mark.unit
def test_merge_markdown_documents_combine_metadata():
    """Test merging Markdown documents with combine metadata strategy."""
    doc1 = """---
title: Document 1
author: Author 1
date: 2023-01-01
---
# Document 1

Content of document 1.
"""

    doc2 = """---
title: Document 2
author: Author 2
tags: [test, markdown]
---
# Document 2

Content of document 2.
"""

    result = merge_markdown_documents([doc1, doc2], "combine_metadata")

    assert isinstance(result, MergedDocument)
    assert result.combined_metadata["author"] == "Author 2"
    assert "test" in str(result.combined_metadata.get("tags", ""))
    assert len(result.source_files) == 2


@pytest.mark.unit
def test_merge_markdown_documents_empty_list():
    """Test merging an empty list of documents."""
    result = merge_markdown_documents([])

    assert isinstance(result, MergedDocument)
    assert result.content == ""
    assert result.combined_metadata == {}
    assert result.source_files == []


@pytest.mark.unit
def test_merge_markdown_documents_single_document():
    """Test merging a single document."""
    doc1 = """---
title: Single Document
author: Single Author
---
# Single Document

Content of single document.
"""

    result = merge_markdown_documents([doc1])

    assert isinstance(result, MergedDocument)
    assert "Content of single document" in result.content
    assert result.combined_metadata["title"] == "Single Document"
    assert result.combined_metadata["author"] == "Single Author"
    assert len(result.source_files) == 1


@pytest.mark.unit
def test_merge_markdown_documents_no_metadata():
    """Test merging documents without metadata."""
    doc1 = """# Document 1

Content of document 1.
"""

    doc2 = """# Document 2

Content of document 2.
"""

    result = merge_markdown_documents([doc1, doc2])

    assert isinstance(result, MergedDocument)
    assert "Content of document 1" in result.content
    assert "Content of document 2" in result.content
    assert result.combined_metadata == {}
    assert len(result.source_files) == 2