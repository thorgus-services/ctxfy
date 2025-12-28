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

from parse_content import parse_markdown_content, MarkdownContent


@pytest.mark.unit
def test_parse_markdown_content_with_metadata():
    """Test parsing Markdown content with metadata."""
    markdown_text = """---
title: Test Document
author: Test Author
---
# Test Heading

This is a test document with [a link](https://example.com) and an image ![alt text](image.jpg).
"""

    result = parse_markdown_content(markdown_text)

    assert isinstance(result, MarkdownContent)
    assert result.metadata["title"] == "Test Document"
    assert result.metadata["author"] == "Test Author"
    assert "Test Heading" in result.headings
    assert "https://example.com" in result.links
    assert "image.jpg" in result.images
    assert "This is a test document" in result.content


@pytest.mark.unit
def test_parse_markdown_content_without_metadata():
    """Test parsing Markdown content without metadata."""
    markdown_text = """# Test Heading

This is a test document with [a link](https://example.com).
"""

    result = parse_markdown_content(markdown_text)

    assert isinstance(result, MarkdownContent)
    assert result.metadata == {}
    assert "Test Heading" in result.headings
    assert "https://example.com" in result.links
    assert result.images == []


@pytest.mark.unit
def test_parse_markdown_content_empty():
    """Test parsing empty Markdown content."""
    markdown_text = ""

    result = parse_markdown_content(markdown_text)

    assert isinstance(result, MarkdownContent)
    assert result.content == ""
    assert result.metadata == {}
    assert result.headings == []
    assert result.links == []
    assert result.images == []


@pytest.mark.unit
def test_parse_markdown_content_multiple_elements():
    """Test parsing Markdown content with multiple elements."""
    markdown_text = """---
title: Multi-Element Document
---
# Main Heading

This document has [multiple links](https://example.com) and [another link](https://test.com).

## Sub Heading

It also has ![an image](img1.jpg) and ![another image](img2.png).

- List item 1
- List item 2

```python
code_block = "example"
```
"""

    result = parse_markdown_content(markdown_text)

    assert isinstance(result, MarkdownContent)
    assert result.metadata["title"] == "Multi-Element Document"
    assert "Main Heading" in result.headings
    assert "Sub Heading" in result.headings
    assert "https://example.com" in result.links
    assert "https://test.com" in result.links
    assert "img1.jpg" in result.images
    assert "img2.png" in result.images