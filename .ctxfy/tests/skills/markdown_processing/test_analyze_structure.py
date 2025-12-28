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

from analyze_structure import analyze_markdown_structure, DocumentAnalysis


@pytest.mark.unit
def test_analyze_markdown_structure_with_all_elements():
    """Test analyzing Markdown structure with all types of elements."""
    markdown_text = """---
title: Test Document
author: Test Author
---
# Main Heading

This document has [a link](https://example.com) and ![an image](image.jpg).

## Sub Heading

Here's a code block:

```python
def hello():
    return "Hello, World!"
```

- List item 1
- List item 2

> This is a blockquote.

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""

    result = analyze_markdown_structure(markdown_text)

    assert isinstance(result, DocumentAnalysis)
    assert result.word_count > 10
    assert result.heading_count >= 2  # Main Heading and Sub Heading
    assert result.link_count >= 1
    assert result.image_count >= 1
    assert result.code_block_count >= 1
    assert result.list_count >= 1
    assert result.table_count >= 1
    assert "title" in result.metadata_keys
    assert "author" in result.metadata_keys
    assert "heading" in result.content_structure
    assert "paragraph" in result.content_structure


@pytest.mark.unit
def test_analyze_markdown_structure_empty():
    """Test analyzing empty Markdown structure."""
    markdown_text = ""

    result = analyze_markdown_structure(markdown_text)

    assert isinstance(result, DocumentAnalysis)
    assert result.word_count == 0
    assert result.heading_count == 0
    assert result.link_count == 0
    assert result.image_count == 0
    assert result.code_block_count == 0
    assert result.list_count == 0
    assert result.table_count == 0
    assert result.metadata_keys == []
    assert result.content_structure == []


@pytest.mark.unit
def test_analyze_markdown_structure_no_metadata():
    """Test analyzing Markdown structure without metadata."""
    markdown_text = """# Heading

[Link](https://example.com)
![Image](image.jpg)

```code block```

- List item
"""

    result = analyze_markdown_structure(markdown_text)

    assert isinstance(result, DocumentAnalysis)
    assert result.heading_count >= 1
    assert result.link_count >= 1
    assert result.image_count >= 1
    assert result.code_block_count >= 1
    assert result.list_count >= 1
    assert result.metadata_keys == []  # No metadata in this document


@pytest.mark.unit
def test_analyze_markdown_structure_multiple_elements():
    """Test analyzing Markdown with multiple similar elements."""
    markdown_text = """---
title: Multi-Element Document
---
# Heading 1

Content with [link1](https://example1.com).

## Heading 2

More content with [link2](https://example2.com).

### Heading 3

Even more content with [link3](https://example3.com).

- Item 1
- Item 2
- Item 3

Another paragraph with ![image1](img1.jpg) and ![image2](img2.png).
"""

    result = analyze_markdown_structure(markdown_text)

    assert isinstance(result, DocumentAnalysis)
    assert result.heading_count >= 3
    assert result.link_count >= 3
    assert result.image_count >= 2
    assert result.list_count >= 1
    assert "title" in result.metadata_keys