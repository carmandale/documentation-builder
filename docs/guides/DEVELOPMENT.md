# Development Guide

## Project Structure

```
documentation_builder/
├── analyzers/          # Analysis modules
│   ├── pattern_refiner.py
│   ├── project_analyzer.py
│   └── relationship_tracker.py
├── core/              # Core functionality
│   ├── scraper.py
│   ├── knowledge_base.py
│   └── url_sources.py
├── extractors/        # Content extraction
│   ├── code_extractor.py
│   └── doc_extractor.py
└── tests/            # Test suite
```

## Development Workflow

1. **Setting Up Development Environment**
```bash
# Create development environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt
```

2. **Running Tests**
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_pattern_refiner.py

# Run with coverage
pytest --cov=.
```

3. **Adding New Features**

a. **New Pattern Type**
```python
# 1. Add to core/config.py
PATTERN_TYPES = [
    'existing_pattern',
    'your_new_pattern'
]

# 2. Add detection in pattern_refiner.py
def _extract_pattern_terms(self, content: str, pattern_type: str):
    if pattern_type == "your_new_pattern":
        terms.update(re.findall(r'pattern_regex', content))

# 3. Add tests
def test_new_pattern():
    # Add test cases
```

b. **New Analyzer**
```python
# 1. Create new analyzer
class NewAnalyzer:
    def analyze(self):
        pass

# 2. Add tests
# 3. Update documentation
```

## Code Style

1. **Python Style**
- Follow PEP 8
- Use type hints
- Document functions

2. **Documentation**
- Update relevant docs
- Add examples
- Include type information

## Testing Guidelines

1. **Test Categories**
- Unit tests for components
- Integration tests
- Pattern validation tests

2. **Test Data**
- Use real samples when possible
- Create minimal test cases
- Document test data

3. **Coverage Requirements**
- Maintain 80%+ coverage
- Test error cases
- Validate edge cases 