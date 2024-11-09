# Extractors API Reference

## CodeBlockExtractor

```python
from extractors.code_extractor import CodeBlockExtractor

extractor = CodeBlockExtractor()
```

### Methods

#### extract_code_blocks
```python
def extract_code_blocks(self, content: str) -> List[Dict[str, Any]]
```
Extracts code blocks from documentation content.

**Parameters:**
- `content`: HTML or markdown content containing code blocks

**Returns:**
- List of code blocks with metadata
  ```python
  [
      {
          "code": str,          # The code content
          "language": str,      # Programming language
          "context": str,       # Surrounding context
          "file_type": str     # File type if specified
      }
  ]
  ```

## DocumentationExtractor

```python
from extractors.doc_extractor import DocumentationExtractor

extractor = DocumentationExtractor()
```

### Methods

#### extract_content
```python
def extract_content(self, html_content: str) -> Dict[str, Any]
```
Extracts structured content from documentation pages.

**Parameters:**
- `html_content`: Raw HTML content

**Returns:**
- Structured documentation content
  ```python
  {
      "title": str,
      "description": str,
      "sections": List[Dict],
      "code_blocks": List[Dict],
      "related_topics": List[str]
  }
  ```

## RelationshipExtractor

```python
from extractors.relationship_extractor import RelationshipExtractor

extractor = RelationshipExtractor()
```

### Methods

#### extract_relationships
```python
def extract_relationships(self, content: str, code_patterns: dict) -> List[ConceptRelationship]
```
Extracts relationships between concepts in documentation.

**Parameters:**
- `content`: Documentation content
- `code_patterns`: Dictionary of code patterns

**Returns:**
- List of concept relationships
  ```python
  [
      ConceptRelationship(
          source="ComponentA",
          target="ComponentB",
          relationship_type="depends_on",
          strength=0.8
      )
  ]
  ```

#### verify_relationships
```python
def verify_relationships(self, doc_cache_path: Path) -> Dict[str, Any]
```
Verifies relationships between samples and documentation.

**Parameters:**
- `doc_cache_path`: Path to documentation cache

**Returns:**
- Verification results
  ```python
  {
      "total_relationships": int,
      "verified": int,
      "broken": int,
      "details": Dict[str, Any]
  }
  ```

## ValidationExtractor

```python
from extractors.validation_extractor import ValidationExtractor

validator = ValidationExtractor()
```

### Methods

#### validate_pattern
```python
def validate_pattern(self, pattern: str, content: str) -> bool
```
Validates a pattern against content.

**Parameters:**
- `pattern`: Pattern to validate
- `content`: Content to check

**Returns:**
- True if pattern is valid, False otherwise 