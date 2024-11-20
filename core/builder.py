"""
Documentation builder module.
"""

from pathlib import Path
import json
from typing import Dict, List, Set, Optional
from datetime import datetime, UTC
from .config import REALITYKIT_SECTIONS, VALIDATION_SETTINGS
from utils.logging import logger

class DocumentationBuilder:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.documentation_dir = cache_dir / 'documentation'
        self.documentation_dir.mkdir(parents=True, exist_ok=True)
        self.relationship_graph = {}
        
    def build_documentation(self):
        """Build documentation with proper relationships."""
        try:
            # Build relationship graph
            self._build_relationship_graph()
            
            # Process each section
            for section_name, section_info in REALITYKIT_SECTIONS.items():
                self._process_section(section_name, section_info)
                
        except Exception as e:
            logger.error(f"Error building documentation: {e}")
            raise
    
    def _build_relationship_graph(self):
        """Build a graph of all documentation relationships."""
        for section_name, section_info in REALITYKIT_SECTIONS.items():
            relationships = section_info.get('relationships', {})
            children = relationships.get('children', {})
            
            # Add section node
            self.relationship_graph[section_name] = {
                'type': 'framework',
                'url': section_info['url'],
                'parent': relationships.get('parent'),
                'children': set(),
                'related': set()
            }
            
            # Add child nodes
            for child_name, child_info in children.items():
                child_type = child_info.get('type', 'unknown')
                child_relationships = child_info.get('relationships', [])
                
                self.relationship_graph[child_name] = {
                    'type': child_type,
                    'parent': section_name,
                    'children': set(),
                    'related': set(child_relationships)
                }
                
                self.relationship_graph[section_name]['children'].add(child_name)
    
    def _process_section(self, section_name: str, section_info: Dict):
        """Process a documentation section and its relationships."""
        try:
            # Create section document
            section_doc = {
                'title': section_name,
                'url': section_info['url'],
                'type': 'framework',
                'parent_pages': [],
                'child_pages': [],
                'related_pages': [],
                'content': {},
                'metadata': {
                    'last_updated': datetime.now(UTC).isoformat(),
                    'version': '1.0'
                }
            }
            
            # Add relationships
            node = self.relationship_graph.get(section_name)
            if node:
                if node['parent']:
                    section_doc['parent_pages'].append(
                        REALITYKIT_SECTIONS[node['parent']]['url']
                    )
                
                for child in node['children']:
                    child_info = self._get_child_info(child)
                    if child_info and child_info.get('url'):
                        section_doc['child_pages'].append(child_info['url'])
                
                for related in node['related']:
                    related_info = self._get_child_info(related)
                    if related_info and related_info.get('url'):
                        section_doc['related_pages'].append(related_info['url'])
            
            # Save document
            doc_path = self.documentation_dir / f"{section_name.lower().replace(' ', '_')}.json"
            with open(doc_path, 'w') as f:
                json.dump(section_doc, f, indent=2)
            
            # Process children
            relationships = section_info.get('relationships', {})
            children = relationships.get('children', {})
            for child_name, child_info in children.items():
                self._process_child(child_name, child_info, section_doc['url'])
                
        except Exception as e:
            logger.error(f"Error processing section {section_name}: {e}")
            raise
    
    def _process_child(self, child_name: str, child_info: Dict, parent_url: str):
        """Process a child document and its relationships."""
        try:
            child_doc = {
                'title': child_name,
                'type': child_info['type'],
                'url': self._generate_url(child_name),
                'parent_pages': [parent_url],
                'child_pages': [],
                'related_pages': [],
                'content': {},
                'metadata': {
                    'last_updated': datetime.now(UTC).isoformat(),
                    'version': '1.0'
                }
            }
            
            # Add relationships
            node = self.relationship_graph.get(child_name)
            if node:
                for related in node['related']:
                    related_info = self._get_child_info(related)
                    if related_info and related_info.get('url'):
                        child_doc['related_pages'].append(related_info['url'])
            
            # Save document
            doc_path = self.documentation_dir / f"{child_name.lower()}.json"
            with open(doc_path, 'w') as f:
                json.dump(child_doc, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error processing child {child_name}: {e}")
            raise
    
    def _get_child_info(self, child_name: str) -> Optional[Dict]:
        """Get information about a child document."""
        # First check in relationship graph
        if child_name in self.relationship_graph:
            return {
                'url': self._generate_url(child_name),
                'type': self.relationship_graph[child_name]['type']
            }
        
        # Then check in sections
        for section_info in REALITYKIT_SECTIONS.values():
            relationships = section_info.get('relationships', {})
            children = relationships.get('children', {})
            if child_name in children:
                return {
                    'url': self._generate_url(child_name),
                    'type': children[child_name].get('type', 'unknown')
                }
        
        return None
    
    def _generate_url(self, name: str) -> str:
        """Generate a documentation URL for a name.
        
        Note: This generates a constructed URL that needs verification against
        the actual Apple documentation structure. These URLs should be validated
        before being used in production.
        """
        # TODO: Replace with actual URL discovery/validation mechanism
        base_url = "https://developer.apple.com/documentation/realitykit"
        return f"{base_url}/{name.lower()}"  # Note: Generated URL needs verification

    def _validate_relationship_type(self, parent_type: str, child_type: str) -> bool:
        """Validate that the relationship between types is valid."""
        valid_child_types = VALIDATION_SETTINGS['relationship_rules'].get(parent_type, set())
        return child_type in valid_child_types
