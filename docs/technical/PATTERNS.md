# Pattern Detection System

## Pattern Types

### 1. UI Components
```python
"ui_components": {
    "detection_terms": ["View", "NavigationStack", "Text"],
    "validation_rules": {
        "required": ["View"],
        "optional": ["NavigationStack", "Text"],
        "imports": ["SwiftUI"]
    }
}
```

### 2. 3D Content
```python
"3d_content": {
    "detection_terms": ["Entity", "Model3D", "RealityView"],
    "validation_rules": {
        "required": ["Entity", "Model3D"],
        "optional": ["RealityView", "Scene3D"],
        "imports": ["RealityKit"]
    }
}
```

[Continue with other patterns...]

## Adding New Patterns
1. Define Pattern Type:
```python
# In core/config.py
PATTERN_TYPES = [
    'existing_pattern',
    'your_new_pattern'
]
```

2. Add Detection Rules:
```python
# In analyzers/pattern_refiner.py
def _extract_pattern_terms(self, content: str, pattern_type: str):
    if pattern_type == "your_new_pattern":
        terms.update(re.findall(r'pattern_regex', content))
```

3. Add Validation Rules:
```python
validation_rules = {
    "your_new_pattern": {
        "required": ["must_have_terms"],
        "optional": ["nice_to_have_terms"],
        "imports": ["required_imports"]
    }
}
``` 