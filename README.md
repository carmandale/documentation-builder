# VisionOS Documentation Analyzer

A specialized tool for scraping, analyzing, and processing Apple's VisionOS documentation to create a structured, searchable, and LLM-ready knowledge base.

## Overview

This project provides tools to:
- Scrape VisionOS documentation systematically
- Extract code examples, parameters, and technical descriptions
- Analyze relationships between different API concepts
- Generate LLM-optimized documentation output
- Provide developer-friendly search and navigation

## Features

### Documentation Scraping
- Extracts structured content from Apple's VisionOS documentation
- Preserves code examples with context
- Maintains hierarchical relationships between topics
- Handles parameter definitions and API specifications

### Content Analysis
- Identifies relationships between different API features
- Tracks code example patterns and common usage
- Analyzes documentation coverage and completeness
- Generates usage statistics and insights

### Developer Tools
- Search through documentation with context
- View related code examples and parameters
- Navigate topic relationships
- Export documentation in various formats

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/visionos-doc-analyzer.git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Scraping Documentation
```bash
python run_scraper.py
```

### Viewing Documentation
```bash
# View all entries
python content_viewer.py view

# Search documentation
python content_viewer.py view -s "window"

# View specific entry with examples and parameters
python content_viewer.py view 0 --examples --params

# View documentation statistics
python content_viewer.py stats
```

### Analyzing Documentation
```bash
python documentation_analyzer.py
```

## Project Structure

```
.
├── documentation_scraper.py  # Core scraping functionality
├── content_viewer.py         # CLI for viewing documentation
├── documentation_analyzer.py # Analysis and insights
├── run_scraper.py           # Scraper entry point
├── data/                    # Scraped documentation storage
└── debug/                   # Debug files and raw HTML
```

## Future Enhancements

- [ ] LLM-optimized output formatting
- [ ] Enhanced relationship mapping
- [ ] PDF documentation support
- [ ] Interactive documentation browser
- [ ] API integration capabilities
- [ ] Custom documentation export formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Apple Developer Documentation
- Beautiful Soup
- Playwright
- Rich CLI
- Typer

## Disclaimer

This tool is not affiliated with, authorized, maintained, sponsored, or endorsed by Apple Inc. or any of its affiliates or subsidiaries. 