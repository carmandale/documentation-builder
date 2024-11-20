# VisionOS Documentation Builder - Project Manifest

## Core Principles
1. **Framework Agnostic**: System must handle ALL VisionOS frameworks equally, not just RealityKit
2. **Pattern First**: Focus on identifying and validating patterns before generating code
3. **Documentation Driven**: All knowledge must be derived from official Apple documentation
4. **Validation Centric**: Every generated piece must be validated against known patterns
5. **Sample Code Driven**: All patterns must be validated against real, working Apple sample projects

## System Architecture
1. Documentation Collection
   - URL Discovery (url_sources.py)
   - Content Scraping (scraper.py)
   - Cache Management (24-hour validity)

2. Analysis System
   - Pattern Detection
   - Relationship Mapping
   - Framework Coverage
   - Code Validation

3. Knowledge Base
   - Pattern Storage
   - Relationship Tracking
   - Framework Documentation
   - Best Practices

## Implementation Rules
1. **No Framework Bias**: Never prioritize one framework over others
2. **Pattern Validation**: All new patterns must be validated against Apple samples
3. **Relationship Preservation**: Maintain all cross-framework relationships
4. **Cache Respect**: Honor the 24-hour cache duration
5. **Documentation First**: No assumed knowledge - everything must come from docs
6. **Working Code Only**: Only extract patterns from compilable, running sample projects

## Development Guidelines
1. Use existing extractors for new content types
2. Maintain the current validation hierarchy
3. Keep the modular analyzer structure
4. Respect the established caching system
5. Follow the pattern evolution tracking

## Critical Paths
1. Pattern Analysis System completion
2. Knowledge Base population
3. Validation System enhancement
4. LLM Integration framework
5. Metrics and monitoring implementation

## Do Not Change
1. Core architecture layout
2. Cache duration (24 hours)
3. Validation hierarchy
4. Pattern detection methodology
5. Documentation collection flow
