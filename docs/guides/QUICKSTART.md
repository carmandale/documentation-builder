# Quick Start Guide

## Installation

1. **Clone the Repository**
```bash
git clone <repository-url>
cd documentation_builder
```

2. **Set Up Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

## Basic Usage

1. **Run the Scraper**
```bash
python run_scraper.py
```

2. **View Results**
- Check `data/knowledge/` for analyzed patterns
- View `data/projects/` for downloaded samples
- See `data/cache/` for cached data

## Common Tasks

### Analyzing New Patterns
```python
# In your script
from analyzers.pattern_refiner import PatternRefiner

# Initialize refiner
refiner = PatternRefiner()

# Analyze patterns
refined_patterns = refiner.analyze_existing_patterns(pattern_data)
```

### Using the Knowledge Base
```python
from core.knowledge_base import VisionOSKnowledgeBase

# Initialize knowledge base
kb = VisionOSKnowledgeBase()

# Query patterns
pattern = kb.query_pattern("ui_components")
```

## Troubleshooting

1. **Cache Issues**
   - Clear cache: Delete contents of `data/cache/`
   - Force refresh: Add `--force-refresh` flag

2. **Download Problems**
   - Check network connection
   - Verify Apple Developer access
   - Check disk space

3. **Pattern Detection Issues**
   - Review pattern definitions
   - Check log files
   - Validate sample code 