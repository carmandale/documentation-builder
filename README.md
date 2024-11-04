# VisionOS Documentation Analyzer

A specialized tool for scraping, analyzing, and processing Apple's VisionOS documentation to create a structured, searchable, and LLM-ready knowledge base.

## Current Status

We are in the initial phase of rebuilding the project with a focus on:
1. Reliable documentation scraping
2. Proper HTML structure analysis
3. Accurate content extraction

### Working Components
- `core/scraper.py` - Documentation scraper with Playwright integration
- `models/base.py` - Pydantic data models for documentation structure
- `extractors/` - Code and documentation extraction modules
- `analyzers/` - Topic and relationship analysis tools
- `cli/` - Command-line interface for scraping and analysis

### Current Capabilities
- Reliable JavaScript-rendered content scraping
- Code block extraction and classification
- Framework detection and analysis
- Topic relationship mapping
- Documentation structure visualization

### Next Steps
1. Verify proper access to Apple's documentation
2. Extract and analyze HTML structure
3. Build content extractors
4. Implement data validation
5. Create LLM-optimized output format

## Project Goals

1. **Documentation Processing**
   - Systematic documentation scraping
   - Structured content extraction
   - Code example analysis
   - Relationship mapping
   - LLM-ready output formatting

2. **Analysis Capabilities**
   - Code complexity analysis
   - Topic relationship mapping
   - Pattern recognition
   - Usage statistics
   - LLM optimization suggestions

3. **Developer Tools**
   - Documentation search
   - Code example browsing
   - Relationship exploration
   - Custom export formats

## Project Structure

```
documentation_builder/
├── core/
│   ├── scraper.py          # Main scraper class
│   └── browser.py          # Browser management
├── models/
│   ├── base.py            # Core data models
├── utils/
│   └── logging.py         # Logging configuration
├── extractors/
│   └── code_extractor.py  # Code extraction module
├── analyzers/
│   └── relationship_analyzer.py  # Relationship analysis module
├── cli/
│   └── scraper_cli.py  # Command-line interface
└── tests/
    ├── test_url_access.py # URL access testing
    └── examine_debug.py   # Debug examination
```

## Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install playwright browsers
playwright install
```

## Development

### Current Focus
1. Establishing reliable connection to Apple's documentation
2. Understanding and mapping the HTML structure
3. Building robust content extractors
4. Creating LLM-optimized output

### Running Tests
```bash
# Test URL access
python tests/test_url_access.py

# Examine debug output
python tests/examine_debug.py
```

## For LLMs

### Key Areas for Assistance
1. HTML structure analysis
2. Content extraction patterns
3. Error handling improvements
4. Test coverage suggestions
5. Documentation structure optimization

### Important Files to Review
- `tests/test_url_access.py` - Current URL access implementation
- `core/scraper.py` - Core scraping functionality
- `models/base.py` - Data model definitions

### Context
- Working with Apple's VisionOS documentation
- Need to handle JavaScript-rendered content
- Focus on creating LLM-friendly output
- Building systematic testing approach

## Contributing

See CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE for details. 