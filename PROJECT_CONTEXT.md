# Project Context Document

## Project Purpose
This project serves as a practical tool for generating accurate and Apple-compliant visionOS code. Its primary goals are to:

1. Combat Common LLM Issues:
   - Prevent generation of incorrect iOS-to-visionOS translations
   - Avoid non-compliant code patterns
   - Ensure proper use of visionOS-specific features

2. Ensure Best Practices:
   - Use real Apple sample code as reference
   - Follow official visionOS design patterns
   - Implement proper SwiftUI patterns for spatial computing
   - Maintain compliance with Apple's visionOS guidelines

3. Practical Applications:
   - Generate proper visionOS SwiftUI code
   - Provide accurate framework and API usage examples
   - Guide developers in proper spatial computing patterns
   - Reference real-world, working implementations

## Current Working Features

### Project Management ✅
- Create new visionOS projects
- Continue existing projects
- List available projects
- Basic project configuration

### Documentation Collection ✅
- URL discovery and validation
- Sample project downloading
- Basic content caching
- Documentation page scraping
- File organization

### Pattern Detection ✅
Currently supports detection of:
- UI Components (SwiftUI views, navigation, controls)
- 3D Content (RealityKit entities, scenes)
- State Management (property wrappers, bindings)
- Lifecycle Patterns (view lifecycle, updates)
- Reality Composer Pro Integration

### Cache System ✅
- Basic file-based caching
- Timestamp-based validation
- Simple error recovery
- Cache inspection tools

### SwiftUI View Management ✅
- Create new SwiftUI views
- List existing views
- Basic view template generation

## Current Limitations

### LLM Integration 🚧
- Basic prompt template system only
- No actual LLM provider integration
- Limited code generation capabilities
- Basic pattern application

### Pattern Analysis 🚧
- Regex-based pattern matching only
- Limited semantic understanding
- Basic relationship tracking
- Simple validation rules

### Code Generation 🚧
- Template-based generation only
- Limited pattern application
- Basic validation
- No advanced context awareness

## Getting Started

### Prerequisites
- Python 3.8+
- Playwright
- BeautifulSoup4
- Required Python packages: `pip install -r requirements.txt`

### Basic Usage
```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run the project manager
python -m cli.project_manager
```

### Common Operations
1. Create a new project:
   ```
   > python -m cli.project_manager new
   ```

2. Continue an existing project:
   ```
   > python -m cli.project_manager continue
   ```

3. List existing projects:
   ```
   > python -m cli.project_manager list-projects
   ```

## Project Structure

### Core Components
- `cli/project_manager.py`: Project management interface
- `core/xcode_manager.py`: Xcode project interactions
- `core/url_sources.py`: Documentation collection
- `core/scraper.py`: Content scraping
- `analyzers/`: Pattern analysis
- `extractors/`: Content extraction
- `models/`: Data structures

### Data Storage
- `projects/`: Individual project data
- `data/cache/`: Cached content
- `data/projects/`: Downloaded samples
- `data/knowledge/`: Analyzed patterns

## Technical Documentation
For detailed technical information, see:
- [Core Functionality](docs/CORE_FUNCTIONALITY.md)
- [Architecture Overview](docs/technical/ARCHITECTURE.md)
- [Pattern System](docs/technical/PATTERNS.md)
- [Cache System](docs/technical/CACHING.md)

## Development Status

### Working Features
1. Project Management
   - Project creation and continuation
   - SwiftUI view management
   - Basic project structure setup

2. Documentation Collection
   - URL discovery and validation
   - Sample project downloading
   - Basic content caching

3. Pattern Detection
   - UI component patterns
   - State management patterns
   - Lifecycle patterns
   - Basic relationship tracking

4. Cache Management
   - File-based caching
   - Basic validation
   - Simple recovery

### In Development
1. LLM Integration
   - Code generation
   - Pattern application
   - Context management

2. Advanced Analysis
   - Semantic understanding
   - Deep relationship analysis
   - Pattern validation

3. Code Generation
   - Template system
   - Pattern application
   - Validation rules

## Best Practices
1. Always validate cache before operations
2. Use logging for tracking operations
3. Handle network failures gracefully
4. Verify file paths before access
5. Validate content before processing

## Troubleshooting

### Common Issues
1. Project Creation Problems
   - Verify Xcode project path
   - Check file permissions
   - Ensure valid project name

2. View Creation Issues
   - Verify Views directory exists
   - Check for naming conflicts
   - Ensure valid SwiftUI structure

3. Pattern Detection Issues
   - Review pattern definitions
   - Check log files
   - Validate sample code

4. Cache Problems
   - Clear cache: Delete contents of `projects/<project_name>/cache/`
   - Force refresh: Add `--force-refresh` flag (if implemented)