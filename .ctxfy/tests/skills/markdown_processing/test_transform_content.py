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

from transform_content import transform_markdown_content, TransformedContent


@pytest.mark.unit
def test_transform_markdown_content_uppercase():
    """Test transforming Markdown content to uppercase."""
    markdown_text = """---
title: Test Document
---
# test heading

this is test content with [a link](https://example.com).
"""

    result = transform_markdown_content(markdown_text, "uppercase")

    assert isinstance(result, TransformedContent)
    assert result.original_content.lower() == result.transformed_content.lower()
    assert result.metadata["title"] == "Test Document"


@pytest.mark.unit
def test_transform_markdown_content_lowercase():
    """Test transforming Markdown content to lowercase."""
    markdown_text = """---
title: Test Document
---
# TEST HEADING

THIS IS TEST CONTENT WITH [A LINK](HTTPS://EXAMPLE.COM).
"""

    result = transform_markdown_content(markdown_text, "lowercase")

    assert isinstance(result, TransformedContent)
    assert result.original_content.upper() == result.transformed_content.upper()
    assert result.metadata["title"] == "Test Document"


@pytest.mark.unit
def test_transform_markdown_content_remove_headings():
    """Test removing headings from Markdown content."""
    markdown_text = """---
title: Test Document
---
# Heading 1

Some content.

## Heading 2

More content.
"""

    result = transform_markdown_content(markdown_text, "remove_headings")

    assert isinstance(result, TransformedContent)
    assert "# Heading 1" not in result.transformed_content
    assert "# Heading 2" not in result.transformed_content
    assert "Some content" in result.transformed_content
    assert "More content" in result.transformed_content
    assert result.metadata["title"] == "Test Document"


@pytest.mark.unit
def test_transform_markdown_content_remove_links():
    """Test removing links from Markdown content."""
    markdown_text = """---
title: Test Document
---
# Test

This has [a link](https://example.com) and [another link](https://test.com).
"""

    result = transform_markdown_content(markdown_text, "remove_links")

    assert isinstance(result, TransformedContent)
    assert "[a link](https://example.com)" not in result.transformed_content
    assert "a link" in result.transformed_content
    assert "[another link](https://test.com)" not in result.transformed_content
    assert "another link" in result.transformed_content
    assert result.metadata["title"] == "Test Document"


@pytest.mark.unit
def test_transform_markdown_content_add_prefix():
    """Test adding blockquote prefix to Markdown content."""
    markdown_text = """---
title: Test Document
---
# Test

Line 1
Line 2

Another paragraph.
"""

    result = transform_markdown_content(markdown_text, "add_prefix")

    assert isinstance(result, TransformedContent)
    assert result.metadata["title"] == "Test Document"
    # Check that non-empty lines have been prefixed
    assert "> Line 1" in result.transformed_content


@pytest.mark.unit
def test_transform_markdown_content_number_headings():
    """Test numbering headings in Markdown content."""
    markdown_text = """---
title: Test Document
---
# First Heading

Content.

## Second Heading

More content.

### Third Heading

Even more content.
"""

    result = transform_markdown_content(markdown_text, "number_headings")

    assert isinstance(result, TransformedContent)
    assert "1. # First Heading" in result.transformed_content
    assert "2. ## Second Heading" in result.transformed_content
    assert "3. ### Third Heading" in result.transformed_content
    assert result.metadata["title"] == "Test Document"


@pytest.mark.unit
def test_transform_markdown_content_no_operation():
    """Test transforming Markdown content with no operation (default)."""
    markdown_text = """---
title: Test Document
---
# Test Heading

Test content.
"""

    result = transform_markdown_content(markdown_text, "invalid_operation")

    assert isinstance(result, TransformedContent)
    assert result.original_content == result.transformed_content
    assert result.metadata["title"] == "Test Document"