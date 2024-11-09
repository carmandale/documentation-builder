# Models API Reference

## ProjectResource

```python
from models.base import ProjectResource

project = ProjectResource(
    title: str,
    url: str,
    download_url: str,
    documentation_url: Optional[str] = None,
    documentation_title: Optional[str] = None,
    local_path: Optional[Path] = None,
    downloaded: bool = False
)
```

Base model for project resources.

### Attributes
- `title`: Project title
- `url`: Source URL
- `download_url`: URL for downloading project
- `documentation_url`: Related documentation URL
- `documentation_title`: Documentation page title
- `local_path`: Path to downloaded project
- `downloaded`: Download status

### Methods

#### mark_downloaded
```python
def mark_downloaded(self, path: Path)
```
Marks project as downloaded and sets local path.

## ConceptRelationship

```python
from models.base import ConceptRelationship

relationship = ConceptRelationship(
    source: str,
    target: str,
    relationship_type: str,
    strength: float = 1.0
)
```

Model for relationships between concepts.

### Attributes
- `source`: Source concept
- `target`: Target concept
- `relationship_type`: Type of relationship
- `strength`: Relationship strength (0.0-1.0)

## CodePattern

```python
from models.base import CodePattern

pattern = CodePattern(
    pattern_type: str,
    content: str,
    context: Optional[str] = None,
    frameworks: List[str] = [],
    confidence: float = 0.0
)
```

Model for code patterns.

### Attributes
- `pattern_type`: Type of pattern
- `content`: Pattern code content
- `context`: Surrounding context
- `frameworks`: Required frameworks
- `confidence`: Detection confidence

## Usage Examples

### Working with Projects
```python
# Create a project resource
project = ProjectResource(
    title="Sample Project",
    url="https://example.com/project",
    download_url="https://example.com/project.zip"
)

# Mark as downloaded
project.mark_downloaded(Path("data/projects/sample"))
```

### Tracking Relationships
```python
# Create a relationship
relationship = ConceptRelationship(
    source="SwiftUI",
    target="RealityKit",
    relationship_type="framework_dependency",
    strength=0.8
)
```

### Pattern Detection
```python
# Create a code pattern
pattern = CodePattern(
    pattern_type="ui_components",
    content="struct ContentView: View { ... }",
    frameworks=["SwiftUI"],
    confidence=0.9
)
``` 