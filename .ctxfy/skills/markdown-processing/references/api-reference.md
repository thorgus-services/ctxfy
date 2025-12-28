# API Reference for Markdown Processing Skill

## Scripts Overview

The markdown-processing skill includes 5 main Python scripts for different operations:

1. `parse_content.py` - Parse Markdown content and extract structured data
2. `extract_elements.py` - Extract specific elements from Markdown files
3. `transform_content.py` - Transform Markdown content with various operations
4. `merge_documents.py` - Merge multiple Markdown documents into one
5. `analyze_structure.py` - Analyze the structure and content of Markdown files

## Core Functions

### parse_content.py

#### `parse_markdown_content(markdown_text: str) -> MarkdownContent`
- **Description**: Parse Markdown content and extract structured data
- **Parameters**: 
  - `markdown_text` (str): Raw Markdown text to parse
- **Returns**: `MarkdownContent` value object with content, metadata, and elements
- **Purity**: Pure function (no I/O operations)

#### `parse_markdown_file(file_path: str) -> MarkdownContent`
- **Description**: Shell function to parse Markdown file with I/O operations
- **Parameters**: 
  - `file_path` (str): Path to the Markdown file to parse
- **Returns**: `MarkdownContent` value object with content, metadata, and elements
- **Purity**: Impure function (performs file I/O)

### extract_elements.py

#### `extract_elements_from_content(markdown_text: str) -> ExtractedElements`
- **Description**: Extract specific elements from Markdown content
- **Parameters**: 
  - `markdown_text` (str): Raw Markdown text to extract elements from
- **Returns**: `ExtractedElements` value object with various content elements
- **Purity**: Pure function (no I/O operations)

#### `extract_elements_from_file(file_path: str, element_type: Optional[str] = None) -> ExtractedElements`
- **Description**: Shell function to extract elements from a Markdown file
- **Parameters**: 
  - `file_path` (str): Path to the Markdown file
  - `element_type` (Optional[str]): Optional type of element to extract specifically
- **Returns**: `ExtractedElements` value object with various content elements
- **Purity**: Impure function (performs file I/O)

### transform_content.py

#### `transform_markdown_content(markdown_text: str, operation: str) -> TransformedContent`
- **Description**: Transform Markdown content with various operations
- **Parameters**: 
  - `markdown_text` (str): Raw Markdown text to transform
  - `operation` (str): Type of transformation to apply
- **Returns**: `TransformedContent` value object with original and transformed content
- **Purity**: Pure function (no I/O operations)

#### `transform_markdown_file(file_path: str, operation: str, output_path: str) -> TransformedContent`
- **Description**: Shell function to transform Markdown file content
- **Parameters**: 
  - `file_path` (str): Path to the input Markdown file
  - `operation` (str): Type of transformation to apply
  - `output_path` (str): Path to save the transformed content
- **Returns**: `TransformedContent` value object with original and transformed content
- **Purity**: Impure function (performs file I/O)

### merge_documents.py

#### `merge_markdown_documents(file_contents: List[str], merge_strategy: str = "append") -> MergedDocument`
- **Description**: Merge multiple Markdown documents into one
- **Parameters**: 
  - `file_contents` (List[str]): List of Markdown content strings to merge
  - `merge_strategy` (str): Strategy for merging ("append", "interleave", "combine_metadata")
- **Returns**: `MergedDocument` value object with merged content
- **Purity**: Pure function (no I/O operations)

#### `merge_markdown_files(file_paths: List[str], output_path: str, merge_strategy: str = "append") -> MergedDocument`
- **Description**: Shell function to merge multiple Markdown files into one
- **Parameters**: 
  - `file_paths` (List[str]): List of paths to Markdown files to merge
  - `output_path` (str): Path to save the merged document
  - `merge_strategy` (str): Strategy for merging ("append", "interleave", "combine_metadata")
- **Returns**: `MergedDocument` value object with merged content
- **Purity**: Impure function (performs file I/O)

### analyze_structure.py

#### `analyze_markdown_structure(markdown_text: str) -> DocumentAnalysis`
- **Description**: Analyze the structure and content of a Markdown document
- **Parameters**: 
  - `markdown_text` (str): Raw Markdown text to analyze
- **Returns**: `DocumentAnalysis` value object with document analysis
- **Purity**: Pure function (no I/O operations)

#### `analyze_markdown_file(file_path: str) -> DocumentAnalysis`
- **Description**: Shell function to analyze the structure of a Markdown file
- **Parameters**: 
  - `file_path` (str): Path to the Markdown file to analyze
- **Returns**: `DocumentAnalysis` value object with document analysis
- **Purity**: Impure function (performs file I/O)

## Value Objects

### `MarkdownContent`
- **Description**: Represents parsed Markdown content
- **Fields**:
  - `content` (str): The main content of the Markdown
  - `metadata` (Dict[str, str]): Key-value pairs of metadata
  - `headings` (List[str]): List of headings in the document
  - `links` (List[str]): List of links in the document
  - `images` (List[str]): List of images in the document

### `ExtractedElements`
- **Description**: Represents extracted elements from Markdown
- **Fields**:
  - `headings` (List[str]): List of headings
  - `links` (List[str]): List of links
  - `images` (List[str]): List of images
  - `code_blocks` (List[str]): List of code blocks
  - `lists` (List[str]): List of lists
  - `blockquotes` (List[str]): List of blockquotes

### `TransformedContent`
- **Description**: Represents transformed Markdown content
- **Fields**:
  - `original_content` (str): The original content before transformation
  - `transformed_content` (str): The content after transformation
  - `metadata` (Dict[str, str]): Key-value pairs of metadata

### `MergedDocument`
- **Description**: Represents merged Markdown document
- **Fields**:
  - `content` (str): The merged content
  - `combined_metadata` (Dict[str, str]): Combined metadata from all documents
  - `source_files` (List[str]): List of source files that were merged

### `DocumentAnalysis`
- **Description**: Represents analysis of Markdown document structure
- **Fields**:
  - `word_count` (int): Number of words in the document
  - `heading_count` (int): Number of headings in the document
  - `link_count` (int): Number of links in the document
  - `image_count` (int): Number of images in the document
  - `code_block_count` (int): Number of code blocks in the document
  - `list_count` (int): Number of lists in the document
  - `table_count` (int): Number of tables in the document
  - `metadata_keys` (List[str]): List of metadata keys
  - `content_structure` (List[str]): List of content types in order

## Dependencies

- `markdown-it-py`: For robust CommonMark parsing
- `python-frontmatter`: For YAML metadata handling
- `pyyaml`: For metadata processing
- `mdit-py-plugins`: For additional Markdown parsing capabilities