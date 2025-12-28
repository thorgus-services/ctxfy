---
name: "markdown-processing"
description: "A skill for processing Markdown files with Python, implementing operations like reading/parsing, element extraction, content transformation, and document analysis. Supports CommonMark compatibility with frontmatter handling and structured content manipulation."
---

# Markdown Processing Skill

This skill provides a comprehensive set of tools for processing Markdown files with Python. It includes operations for reading/parsing, element extraction, content transformation, and document analysis. The skill supports CommonMark compatibility with frontmatter handling and structured content manipulation.

## Features

- Parse Markdown content with CommonMark compatibility
- Extract specific elements from Markdown files (headings, links, images, code blocks)
- Transform content with various operations
- Merge multiple Markdown documents
- Analyze document structure and content
- Handle YAML frontmatter in Markdown files

## Scripts

- `parse_content.py`: Parse Markdown content and extract structured data
- `extract_elements.py`: Extract specific elements from Markdown files
- `transform_content.py`: Transform Markdown content with various operations
- `merge_documents.py`: Merge multiple Markdown documents into one
- `analyze_structure.py`: Analyze the structure and content of Markdown files

## Usage Examples

### Parse Markdown Content
```bash
python scripts/parse_content.py --file path/to/file.md
```

### Extract Elements
```bash
python scripts/extract_elements.py --file path/to/file.md --element-type heading
```

### Transform Content
```bash
python scripts/transform_content.py --file path/to/file.md --operation uppercase
```

### Merge Documents
```bash
python scripts/merge_documents.py --files file1.md file2.md --output merged.md
```

### Analyze Structure
```bash
python scripts/analyze_structure.py --file path/to/file.md
```

## Dependencies

- markdown-it-py: For robust CommonMark parsing
- python-frontmatter: For YAML metadata handling
- pyyaml: For metadata processing