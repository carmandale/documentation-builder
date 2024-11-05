# VisionOS Documentation Analyzer

A tool for building an LLM-optimized knowledge base from Apple's VisionOS documentation, focused on enabling AI assistants to provide accurate, working code examples.

## Project Goals

1. **Primary Objective**
   - Create a knowledge base that enables LLMs to generate, modify, and debug working VisionOS code
   - Ensure AI suggestions are based on actual Apple documentation rather than training data
   - Validate suggestions through working test cases

2. **Documentation Processing**
   - Systematic documentation scraping with validation
   - Pattern recognition in Apple's code examples
   - Relationship mapping between concepts
   - Test case extraction and verification

3. **LLM Optimization**
   - Structured data format optimized for LLM consumption
   - Clear relationships between concepts and implementations
   - Validation examples for each pattern
   - Context preservation for accurate code generation

## Features

### Relationship Mapping
The tool automatically identifies and tracks relationships between VisionOS concepts:
- **Section Relationships**: Hierarchical relationships in documentation
- **Framework Dependencies**: Which frameworks are used together
- **Pattern Dependencies**: How different code patterns relate
- **Concept Dependencies**: Links between features and implementations

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

## Data Structure

```
data/
├── extracted/
│   ├── code_blocks/    # Extracted code examples
│   ├── relationships/  # Concept relationships
│   │   └── relationships.json  # Mapped relationships
│   └── validation/    # Test cases and results
├── debug/            # Raw scraped content
└── visualizations/   # Generated relationship graphs
```

## Usage

### For LLM Training
1. Access extracted patterns in `data/extracted/code_blocks/`
2. Use relationship data in `data/extracted/relationships/`
3. Reference test implementations in `data/validation/`

### For Development
```bash
python -m cli.scraper_cli scrape  # Scrape and analyze docs
python -m cli.scraper_cli analyze # Generate relationship maps
```

## Current Status

Successfully analyzing:
- Documentation structure and hierarchy
- Code pattern relationships
- Framework dependencies
- Feature relationships
- Implementation patterns

## License

MIT License - see LICENSE for details 