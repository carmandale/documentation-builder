# VisionOS Documentation Analyzer

A tool for building an LLM-optimized knowledge base from Apple's VisionOS documentation, focused on enabling AI assistants to provide accurate, working code examples.

## Project Goals

1. **Primary Objective**
   - Create a knowledge base that enables LLMs to generate, modify, and debug working VisionOS code
   - Ensure AI suggestions are based on actual Apple documentation rather than training data
   - Validate suggestions through working test cases
   - Learn and evolve from discovered patterns and relationships

2. **Documentation Processing**
   - Systematic documentation scraping with validation
   - Dynamic content handling using Playwright
   - Pattern recognition in Apple's code examples
   - Relationship mapping between concepts
   - Test case extraction and verification
   - Automatic discovery of sample projects
   - Content caching with validation

3. **LLM Optimization**
   - Structured data format optimized for LLM consumption
   - Clear relationships between concepts and implementations
   - Validation examples for each pattern
   - Context preservation for accurate code generation
   - Pattern-based learning from discovered content

## Features

### Caching System
- **URL Cache**: Stores discovered documentation URLs
- **Samples Cache**: Maintains list of found sample projects
- **Documentation Cache**: Stores extracted content and relationships
- **Analysis Cache**: Preserves pattern analysis results
- **Cache Validation**: Age-based checks and content verification
- **Auto-Update**: Refreshes stale cache entries

### URL Discovery and Management
- Automatic discovery of documentation URLs
- Categorization of discovered content
- Metadata tracking for each URL
- Deduplication and validation
- Persistent storage of discovered URLs

### Documentation Content Extraction
- Structured content extraction from pages
- Code sample collection with context
- API reference documentation
- Related topics and concepts
- Key implementation patterns
- Automatic content caching

### Relationship Mapping
The tool automatically identifies and tracks relationships between VisionOS concepts:
- **Section Relationships**: Hierarchical relationships in documentation
- **Framework Dependencies**: Which frameworks are used together
- **Pattern Dependencies**: How different code patterns relate
- **Concept Dependencies**: Links between features and implementations
- **Implementation Patterns**: Common code patterns and their usage

### Pattern Recognition
Currently implemented patterns:
- UI Components
- Animation
- Gestures
- 3D Content
- Spatial Audio
- Immersive Spaces
- ARKit Integration
- RealityKit Components

### Knowledge Base Evolution
- Learns from discovered content
- Updates pattern definitions
- Suggests new categories
- Tracks relationship strengths
- Identifies common implementations

## Project Structure
Current implementation:

```
.
├── analyzers/               # Analysis modules
│   ├── documentation_analyzer.py
│   ├── pattern_evolution.py
│   ├── project_analyzer.py
│   └── relationship_tracker.py
├── core/                   # Core functionality
│   ├── config.py          # Configuration settings
│   ├── scraper.py         # Main scraping logic
│   └── url_sources.py     # URL management
├── data/                  # Data storage
│   ├── cache/           # Cache storage
│   ├── debug/           # Debug output
│   ├── docs/           # Documentation cache
│   ├── extracted/      # Extracted patterns
│   ├── knowledge/     # Knowledge base
│   ├── logs/         # Application logs
│   └── projects/     # Downloaded projects
├── extractors/      # Content extraction
│   ├── code_extractor.py
│   ├── doc_extractor.py
│   └── relationship_extractor.py
├── models/        # Data models
├── tests/        # Test suite
└── utils/       # Utility functions
    └── logging.py
```

## Usage

### Basic Usage
```bash
# Run in test mode (3 sample projects)
python run_scraper.py

# Run full analysis (all discovered projects)
# Edit core/config.py and set TESTING_MODE = False
python run_scraper.py
```

### Configuration
Edit `core/config.py` to configure:
- Test mode vs full analysis
- Base documentation URLs
- Cache settings and timeouts
- Test project subset
- Analysis parameters

### Cache Management
```bash
# Clear all caches
rm -rf data/cache/*

# Clear specific cache
rm data/cache/url_cache.json

# Force cache refresh
touch data/cache/samples_cache.json
```

### For LLM Training
1. Access extracted patterns in `data/knowledge/`
2. Use relationship data in `data/extracted/relationships/`
3. Reference implementations in `data/projects/`
4. Learn from discovered patterns in `data/knowledge/patterns.json`
5. Access cached documentation in `data/cache/documentation_cache.json`

## Requirements

- Python 3.8+
- Playwright for dynamic content
- BeautifulSoup4 for parsing
- aiohttp for async requests
- Rich for console output

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## License

MIT License - see LICENSE for details 