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

3. **LLM Optimization**
   - Structured data format optimized for LLM consumption
   - Clear relationships between concepts and implementations
   - Validation examples for each pattern
   - Context preservation for accurate code generation
   - Pattern-based learning from discovered content

## Features

### URL Discovery and Management
- Automatic discovery of documentation URLs
- Categorization of discovered content
- Metadata tracking for each URL
- Deduplication and validation
- Persistent storage of discovered URLs

### Relationship Mapping
The tool automatically identifies and tracks relationships between VisionOS concepts:
- **Section Relationships**: Hierarchical relationships in documentation
- **Framework Dependencies**: Which frameworks are used together
- **Pattern Dependencies**: How different code patterns relate
- **Concept Dependencies**: Links between features and implementations
- **Implementation Patterns**: Common code patterns and their usage

### Pattern Recognition
Identifies common VisionOS patterns across:
- 2D Views and Controls
- 3D Volumetric Content
- Immersive Experiences
- Mixed Reality Features
- ARKit Integration
- Reality Composer Usage
- Spatial Audio
- RealityKit Components
- Gesture Handling
- Windows and Ornaments

### Knowledge Base Evolution
- Learns from discovered content
- Updates pattern definitions
- Suggests new categories
- Tracks relationship strengths
- Identifies common implementations

## Project Structure

```
data/
├── urls/
│   ├── discovered_urls.json    # Discovered URLs database
│   └── metadata.json          # URL metadata
├── knowledge/
│   ├── patterns.json         # Discovered patterns
│   ├── concepts.json        # Concept relationships
│   └── frameworks.json     # Framework relationships
├── extracted/
│   ├── code_blocks/       # Extracted code examples
│   └── relationships/    # Mapped relationships
├── projects/           # Downloaded sample projects
└── debug/            # Debug information and raw content
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
- Test project subset
- Analysis parameters

### For LLM Training
1. Access extracted patterns in `data/knowledge/`
2. Use relationship data in `data/extracted/relationships/`
3. Reference implementations in `data/projects/`
4. Learn from discovered patterns in `data/knowledge/patterns.json`

## Current Status

Successfully:
- Discovering documentation URLs
- Downloading sample projects
- Analyzing code patterns
- Mapping relationships
- Learning from discovered content
- Evolving knowledge base
- Generating insights

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