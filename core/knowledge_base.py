from pathlib import Path
from typing import Dict, Any, List
import json
import logging
from utils.logging import logger
import re

class VisionOSKnowledgeBase:
    def __init__(self, data_dir: Path = Path('data/knowledge')):
        self.data_dir = data_dir
        self.relationships_path = data_dir / 'relationships.json'
        self.patterns_path = data_dir / 'patterns.json'
        self.examples_path = data_dir / 'examples.json'
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def build_from_analysis(self, pattern_data: Dict[str, Any]):
        """Build knowledge base from analysis results"""
        try:
            # Convert pattern data to knowledge structure
            patterns = {}
            for pattern_type, data in pattern_data.items():
                patterns[pattern_type] = {
                    "count": data['count'],
                    "files": list(set(data['files'])),  # Unique files
                    "examples": data.get('examples', []),
                    "relationships": self._extract_relationships(data)
                }
            
            # Save patterns
            self.patterns_path.write_text(
                json.dumps(patterns, indent=2)
            )
            logger.info(f"Saved {len(patterns)} patterns to knowledge base")
            
        except Exception as e:
            logger.error(f"Error building knowledge base: {e}")
    
    def _extract_relationships(self, pattern_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract relationships from pattern data"""
        relationships = {
            "commonly_used_with": [],
            "parent_components": [],
            "child_components": []
        }
        
        # Extract from files and examples
        if 'files' in pattern_data:
            for file in pattern_data['files']:
                # Analyze file content for relationships
                self._analyze_file_relationships(file, relationships)
        
        return relationships
    
    def _analyze_file_relationships(self, file_path: str, relationships: Dict[str, List[str]]):
        """Analyze a file for component relationships"""
        try:
            if Path(file_path).exists():
                content = Path(file_path).read_text()
                
                # Look for import relationships
                imports = re.findall(r'import\s+(\w+)', content)
                relationships["commonly_used_with"].extend(imports)
                
                # Look for parent/child relationships
                # Add more relationship analysis as needed
                
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
    
    def query_pattern(self, pattern_type: str) -> Dict[str, Any]:
        """Get examples and usage patterns for a specific feature"""
        try:
            if self.patterns_path.exists():
                patterns = json.loads(self.patterns_path.read_text())
                return patterns.get(pattern_type, {})
        except Exception as e:
            logger.error(f"Error querying pattern {pattern_type}: {e}")
        return {}
    
    def get_component_relationship(self, component: str) -> Dict[str, Any]:
        """Get relationship data for a component"""
        try:
            if self.relationships_path.exists():
                relationships = json.loads(self.relationships_path.read_text())
                return relationships.get(component, {})
        except Exception as e:
            logger.error(f"Error getting relationships for {component}: {e}")
        return {}