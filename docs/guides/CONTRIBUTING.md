# Contributing Guide

## Getting Started

1. **Fork the Repository**
   - Fork on GitHub
   - Clone your fork locally
   - Set up development environment

2. **Development Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## Development Workflow

### 1. Creating New Features

a. **Branch Naming**
- `feature/` - For new features
- `fix/` - For bug fixes
- `docs/` - For documentation
- `refactor/` - For code refactoring

b. **Development Process**
1. Create branch
2. Write tests
3. Implement feature
4. Update documentation
5. Submit PR

### 2. Pattern Development

When adding new patterns:

1. **Define Pattern**
```python
# In core/config.py
PATTERN_TYPES = [
    'existing_pattern',
    'your_new_pattern'
]
```

2. **Add Detection Rules**
```python
# In analyzers/pattern_refiner.py
def _extract_pattern_terms(self, content: str, pattern_type: str):
    if pattern_type == "your_new_pattern":
        terms.update(re.findall(r'pattern_regex', content))
```

3. **Add Tests**
```python
# In tests/test_pattern_refiner.py
def test_new_pattern():
    # Test cases
```

4. **Update Documentation**
- Add pattern to PATTERNS.md
- Update examples
- Document relationships

### 3. Testing Requirements

1. **Test Coverage**
- Unit tests required
- Integration tests for features
- Documentation tests
- Minimum 80% coverage

2. **Running Tests**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific tests
pytest tests/test_pattern_refiner.py
```

## Documentation

### 1. Code Documentation
- Use docstrings
- Include type hints
- Document exceptions
- Add usage examples

### 2. Documentation Files
- Update relevant .md files
- Add new guides if needed
- Include code examples
- Document API changes

## Pull Request Process

1. **Before Submitting**
- Run all tests
- Update documentation
- Check code style
- Verify examples

2. **PR Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Added unit tests
- [ ] Updated existing tests
- [ ] All tests passing

## Documentation
- [ ] Updated relevant docs
- [ ] Added examples
- [ ] Updated API docs
```

## Code Style

1. **Python Guidelines**
- Follow PEP 8
- Use type hints
- Document functions
- Keep functions focused

2. **Documentation Style**
- Clear and concise
- Include examples
- Link related docs
- Keep updated

## Questions?
- Open an issue
- Join discussions
- Check existing docs 