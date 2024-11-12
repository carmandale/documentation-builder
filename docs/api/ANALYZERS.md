# Analyzers API Reference

## ComponentAnalyzer

```python
from analyzers.component_analyzer import ComponentAnalyzer

analyzer = ComponentAnalyzer(samples_dir: Path = Path('data/projects'))
```

### Current Implementation ✅
- Regex-based pattern detection
- Framework and import analysis
- Basic relationship tracking
- File-based processing

### Methods

#### analyze_samples ✅
```python
def analyze_samples(self, samples_dir: Optional[Path] = None) -> Dict[str, Any]
```
Current Capabilities:
- Swift file scanning
- Basic pattern detection
- Import analysis
- Simple relationship tracking

⚠️ Limitations:
- Regex-based only
- No semantic analysis
- Basic relationship detection
- Limited validation

## PatternRefiner

```python
from analyzers.pattern_refiner import PatternRefiner

refiner = PatternRefiner(knowledge_dir: Path = Path('data/knowledge'))
```

### Current Implementation ✅
- Basic pattern refinement
- Simple confidence scoring
- File-based storage
- Basic validation rules

### Methods

#### analyze_existing_patterns ✅
```python
def analyze_existing_patterns(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]
```
Current Capabilities:
- Pattern categorization
- Basic confidence scoring
- Simple validation
- Framework detection

⚠️ Limitations:
- No semantic analysis
- Basic pattern matching
- Limited validation
- Simple scoring system

#### validate_pattern ✅
```python
def validate_pattern(self, pattern_type: str, content: str) -> float
```
Current Capabilities:
- Basic pattern validation
- Simple confidence scoring
- Framework checking
- Required term validation

⚠️ Limitations:
- Simple validation rules
- No context awareness
- Basic scoring only
- Limited validation depth

## RelationshipTracker

```python
from analyzers.relationship_tracker import RelationshipTracker

tracker = RelationshipTracker(knowledge_dir: Path)
```

### Current Implementation ✅
- Basic relationship tracking
- Simple relationship types
- File-based storage
- Basic validation

### Methods

#### track_relationship ✅
```python
def track_relationship(self, source: str, target: str, relationship_type: str)
```
Current Capabilities:
- Basic relationship recording
- Simple type tracking
- File-based storage
- Basic validation

⚠️ Limitations:
- No complex relationships
- Limited relationship types
- Basic storage only
- Simple validation

## Best Practices

### Currently Supported ✅
1. Pattern Analysis:
   ```python
   analyzer = ComponentAnalyzer()
   results = analyzer.analyze_samples(project_path)
   ```

2. Error Handling:
   ```python
   try:
       results = refiner.analyze_existing_patterns(patterns)
   except Exception as e:
       logger.error(f"Pattern analysis error: {e}")
   ```

3. Relationship Tracking:
   ```python
   tracker.track_relationship(source, target, "depends_on")
   ```

### Development Guidelines ✅
1. Always validate inputs
2. Handle analysis failures gracefully
3. Log analysis operations
4. Check file paths before access

🚧 Planned Features:
- Semantic analysis
- Deep relationship tracking
- Advanced validation
- Pattern evolution tracking
