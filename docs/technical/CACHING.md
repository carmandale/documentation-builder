# Cache System Documentation

## Current Cache Structure
```
data/
  cache/              # URL and download caches
    *.json           # Cache metadata
    downloads/       # Downloaded files
  
  documentation/     # Processed documentation
    *.json          # Extracted documentation
    
  extracted/        # Extracted patterns/content
    extracted_*.json # Pattern data
    
  knowledge/        # Refined knowledge
    patterns.json   # Pattern definitions
    refined_patterns.json # Validated patterns
    
  projects/         # Sample projects
    */             # Individual project directories
```

## Cache Touchpoints
- DocumentationURLCollector: Downloads and caches samples
- DocumentationAnalyzer: Caches processed documentation
- PatternRefiner: Caches refined patterns
- ProjectAnalyzer: Uses cached projects

## Current Cache Validation
- Basic file existence checks
- Simple timestamp comparisons
- Basic hash checking

## Missing Centralized Features
- No unified cache interface
- No centralized expiry management
- No cache invalidation strategy
- No cache size management
- No cross-cache consistency checks

## Future Centralization Notes
- Current scattered cache management needs consolidation
- Inconsistent cache validation needs standardization
- No centralized expiry/refresh system
- Potential for duplicate downloads
- Limited cache status reporting