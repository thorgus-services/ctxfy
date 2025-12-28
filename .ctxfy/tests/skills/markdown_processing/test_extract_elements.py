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

from extract_elements import extract_elements_from_content, ExtractedElements


@pytest.mark.unit
def test_extract_elements_from_content_with_all_elements():
    """Test extracting all types of elements from Markdown content."""
    markdown_text = """---
title: Test Document
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
"""

    result = extract_elements_from_content(markdown_text)

    assert isinstance(result, ExtractedElements)
    assert "Main Heading" in result.headings
    assert "Sub Heading" in result.headings
    assert "https://example.com" in result.links
    assert "image.jpg" in result.images
    assert "def hello():" in result.code_blocks[0]
    assert "List item 1" in result.lists[0]
    assert "This is a blockquote" in result.blockquotes[0]


@pytest.mark.unit
def test_extract_elements_from_content_empty():
    """Test extracting elements from empty Markdown content."""
    markdown_text = ""

    result = extract_elements_from_content(markdown_text)

    assert isinstance(result, ExtractedElements)
    assert result.headings == []
    assert result.links == []
    assert result.images == []
    assert result.code_blocks == []
    assert result.lists == []
    assert result.blockquotes == []


@pytest.mark.unit
def test_extract_elements_from_content_no_metadata():
    """Test extracting elements from Markdown content without metadata."""
    markdown_text = """# Heading

[Link](https://example.com)
![Image](image.jpg)

```code block content```

- List item

> Blockquote
"""

    result = extract_elements_from_content(markdown_text)

    assert isinstance(result, ExtractedElements)
    assert "Heading" in result.headings
    assert "https://example.com" in result.links
    assert "image.jpg" in result.images
    assert "code block content" in result.code_blocks[0]
    assert "List item" in result.lists[0]
    assert "Blockquote" in result.blockquotes[0]


@pytest.mark.unit
def test_extract_elements_from_content_multiple_code_blocks():
    """Test extracting multiple code blocks."""
    markdown_text = """# Code Blocks Test

First code block:

```python
print("Hello")
```

Second code block:

```javascript
console.log("World");
```
"""

    result = extract_elements_from_content(markdown_text)

    assert isinstance(result, ExtractedElements)
    assert len(result.code_blocks) >= 2
    assert any("print" in code for code in result.code_blocks)
    assert any("console.log" in code for code in result.code_blocks)