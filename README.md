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

## Current Status

We have successfully implemented:
1. Basic documentation scraping (6 pages verified)
2. Code block extraction and classification
3. Initial relationship mapping
4. Basic validation through test implementations

### Working Test Case
Current validation focuses on a specific test case:
- Creating a VisionOS view with:
  - 2D window content (text and image)
  - 3D content (cylinder with specific transforms)
  - Animation implementation
- Verifying the implementation matches Apple's patterns

### Scraped Documentation
Successfully scraped and analyzed:
- Adding 3D content to your app (6 code blocks)
- Creating your first visionOS app (1 code block)
- Creating fully immersive experiences (3 code blocks)
- Creating an immersive space (7 code blocks)
- BOT-anist sample app (19 code blocks)
- Swift Splash sample app (6 code blocks)

## Data Structure

```
data/
├── extracted/           # JSON files of processed documentation
│   ├── code_blocks/    # Extracted code examples
│   ├── relationships/  # Concept relationships
│   └── validation/     # Test cases and results
├── debug/              # Raw scraped content
└── visualizations/     # Generated relationship graphs
```

## LLM Usage Guide

### Knowledge Access
1. Examine extracted JSON files in `data/extracted/`
2. Review relationship maps in `data/visualizations/`
3. Validate against test cases in `data/validation/`

### Code Generation Process
1. Search extracted patterns for relevant examples
2. Verify framework and API usage
3. Cross-reference with test implementations
4. Validate against Apple's patterns

### Current Limitations
- Limited to successfully scraped documentation
- Must verify patterns against actual examples
- Need to expand test case coverage

## Development

### Running the Scraper
```bash
python -m cli.scraper_cli clean --force
python -m cli.scraper_cli scrape
python -m cli.scraper_cli visualize
```

### Adding Test Cases
1. Identify specific functionality to test
2. Scrape relevant documentation
3. Implement test case
4. Verify against actual device

## Next Steps

1. **Immediate Focus**
   - Expand documentation coverage
   - Improve pattern recognition
   - Add more test cases
   - Enhance LLM accessibility

2. **Validation Improvements**
   - Add automated testing
   - Expand test coverage
   - Improve error detection
   - Track API changes

3. **Documentation Enhancement**
   - Better relationship mapping
   - More detailed pattern analysis
   - Improved context preservation
   - Better error handling

## License

MIT License - see LICENSE for details 