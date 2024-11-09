# Analyzers API Reference

## PatternRefiner

```python
from analyzers.pattern_refiner import PatternRefiner

refiner = PatternRefiner(knowledge_dir: Path = Path('data/knowledge'))
```

### Methods

#### analyze_existing_patterns
```python
def analyze_existing_patterns(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]
```
Analyzes and refines patterns based on actual usage in code.

**Parameters:**
- `pattern_data`: Dictionary containing pattern analysis data
  ```python
  {
      "pattern_type": {
          "count": int,
          "files": List[str],
          "examples": List[str],
          "validated": bool
      }
  }
  ```

**Returns:**
- Dictionary of refined patterns with confidence scores
  ```python
  {
      "pattern_type": {
          "detection_terms": Set[str],
          "common_imports": Set[str],
          "related_components": Set[str],
          "confidence": float,
          "validation_status": str
      }
  }
  ```

#### validate_pattern
```python
def validate_pattern(self, pattern_type: str, content: str) -> float
```
Validates a pattern match and returns confidence score.

**Parameters:**
- `pattern_type`: Type of pattern to validate
- `content`: Code content to analyze

**Returns:**
- Confidence score between 0.0 and 1.0

## ProjectAnalyzer

```python
from analyzers.project_analyzer import ProjectAnalyzer

analyzer = ProjectAnalyzer()
```

### Methods

#### analyze_project
```python
def analyze_project(self, project_path: Path) -> Dict[str, Any]
```
Analyzes a project for patterns and relationships.

**Parameters:**
- `project_path`: Path to project directory

**Returns:**
- Analysis results including patterns and relationships

## RelationshipTracker

```python
from analyzers.relationship_tracker import RelationshipTracker

tracker = RelationshipTracker(knowledge_dir: Path)
```

### Methods

#### track_relationship
```python
def track_relationship(self, source: str, target: str, relationship_type: str)
```
Tracks a relationship between components.

**Parameters:**
- `source`: Source component
- `target`: Target component
- `relationship_type`: Type of relationship 