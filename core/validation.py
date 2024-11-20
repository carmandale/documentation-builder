"""
Documentation coverage validation and reporting.
"""

from pathlib import Path
import json
import re
from typing import Dict, Set, List, Optional
from datetime import datetime, UTC
from .config import REALITYKIT_SECTIONS, VALIDATION_SETTINGS
from utils.logging import logger

class DocumentationValidator:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.documentation_dir = cache_dir / 'documentation'
        self.validation_results = {
            'timestamp': datetime.now(UTC).isoformat(),
            'coverage': {},
            'issues': [],
            'statistics': {}
        }

    def validate_framework_coverage(self) -> Dict:
        """Validate coverage of framework documentation."""
        coverage_report = {}
        
        for section_name, section_info in REALITYKIT_SECTIONS.items():
            section_coverage = {
                'url': section_info['url'],
                'found': False,
                'children_found': [],
                'children_missing': [],
                'issues': []
            }
            
            # Check if main section exists
            section_file = self._get_cached_file(section_info['url'])
            if section_file and section_file.exists():
                section_coverage['found'] = True
                
                # Validate required children
                for child in section_info['required_children']:
                    if self._validate_child_exists(child):
                        section_coverage['children_found'].append(child)
                    else:
                        section_coverage['children_missing'].append(child)
                        section_coverage['issues'].append(f"Missing required child: {child}")
            else:
                section_coverage['issues'].append("Main section documentation not found")
            
            coverage_report[section_name] = section_coverage
        
        self.validation_results['coverage'] = coverage_report
        return coverage_report

    def validate_documentation_quality(self) -> Dict:
        """Validate the quality of cached documentation."""
        quality_report = {
            'code_examples': {},
            'section_coverage': {},
            'relationship_validation': {},
            'broken_links': set()
        }
        
        for doc_file in self.documentation_dir.glob('*.json'):
            try:
                with open(doc_file) as f:
                    content = json.load(f)
                
                # Validate code examples
                if 'code_blocks' in content:
                    num_examples = len(content['code_blocks'])
                    if num_examples < VALIDATION_SETTINGS['min_code_examples']:
                        quality_report['code_examples'][doc_file.stem] = {
                            'found': num_examples,
                            'required': VALIDATION_SETTINGS['min_code_examples']
                        }
                
                # Validate required sections
                missing_sections = []
                for required_section in VALIDATION_SETTINGS['required_sections']:
                    if required_section.lower() not in str(content).lower():
                        missing_sections.append(required_section)
                
                if missing_sections:
                    quality_report['section_coverage'][doc_file.stem] = {
                        'missing_sections': missing_sections
                    }
                
                # Validate relationships if enabled
                if VALIDATION_SETTINGS['verify_relationships']:
                    self._validate_relationships(content, quality_report, doc_file.stem)
                
                # Check for broken links if enabled
                if VALIDATION_SETTINGS['check_broken_links']:
                    self._check_broken_links(content, quality_report)
                    
            except Exception as e:
                logger.error(f"Error validating {doc_file}: {e}")
                quality_report['errors'] = quality_report.get('errors', []) + [str(e)]
        
        self.validation_results['quality'] = quality_report
        return quality_report

    def generate_coverage_report(self) -> Dict:
        """Generate a comprehensive coverage report."""
        framework_coverage = self.validate_framework_coverage()
        quality_report = self.validate_documentation_quality()
        
        # Calculate statistics
        total_sections = len(REALITYKIT_SECTIONS)
        covered_sections = len([s for s in framework_coverage.values() if s['found']])
        total_children = sum(len(s['required_children']) for s in REALITYKIT_SECTIONS.values())
        covered_children = sum(len(s['children_found']) for s in framework_coverage.values())
        
        statistics = {
            'section_coverage_percentage': (covered_sections / total_sections) * 100,
            'child_coverage_percentage': (covered_children / total_children) * 100,
            'total_sections': total_sections,
            'covered_sections': covered_sections,
            'total_children': total_children,
            'covered_children': covered_children,
            'quality_issues': len(quality_report.get('code_examples', {})) + 
                            len(quality_report.get('section_coverage', {}))
        }
        
        self.validation_results['statistics'] = statistics
        return self.validation_results

    def _get_cached_file(self, url: str) -> Optional[Path]:
        """Get the cached file path for a URL."""
        filename = url.split('/')[-1].lower()
        if not filename.endswith('.json'):
            filename += '.json'
        return self.documentation_dir / filename

    def _validate_child_exists(self, child_name: str) -> bool:
        """Check if a child document exists in the cache."""
        child_file = self.documentation_dir / f"{child_name}.json"
        return child_file.exists()

    def _validate_relationships(self, content: Dict, report: Dict, doc_name: str):
        """Validate document relationships.
        
        Performs comprehensive relationship validation:
        1. Verifies relationships exist in cache
        2. Validates bi-directional relationships
        3. Checks relationship types and metadata
        """
        relationships = {
            'child_pages': content.get('child_pages', []),
            'related_pages': content.get('related_pages', []),
            'parent_pages': content.get('parent_pages', [])
        }
        invalid_relationships = []
        
        for rel_type, rel_list in relationships.items():
            for relationship in rel_list:
                rel_file = self._get_cached_file(relationship)
                
                # Check if relationship target exists
                if not rel_file or not rel_file.exists():
                    invalid_relationships.append({
                        'url': relationship,
                        'error': 'Target document not found',
                        'type': rel_type
                    })
                    continue
                
                # Validate bi-directional relationship
                try:
                    with open(rel_file) as f:
                        rel_content = json.load(f)
                        
                    # Get the current document's URL
                    current_url = content.get('url', '')
                    
                    # Check reverse relationship
                    if rel_type == 'child_pages':
                        if current_url not in rel_content.get('parent_pages', []):
                            invalid_relationships.append({
                                'url': relationship,
                                'error': 'Missing reverse parent relationship',
                                'type': rel_type
                            })
                    elif rel_type == 'parent_pages':
                        if current_url not in rel_content.get('child_pages', []):
                            invalid_relationships.append({
                                'url': relationship,
                                'error': 'Missing reverse child relationship',
                                'type': rel_type
                            })
                    elif rel_type == 'related_pages':
                        if current_url not in rel_content.get('related_pages', []):
                            invalid_relationships.append({
                                'url': relationship,
                                'error': 'Missing reverse related relationship',
                                'type': rel_type
                            })
                    
                    # Validate relationship metadata
                    if not self._validate_relationship_metadata(content, rel_content, rel_type):
                        invalid_relationships.append({
                            'url': relationship,
                            'error': 'Invalid relationship metadata',
                            'type': rel_type
                        })
                        
                except Exception as e:
                    logger.error(f"Error validating relationship {relationship}: {e}")
                    invalid_relationships.append({
                        'url': relationship,
                        'error': f'Validation error: {str(e)}',
                        'type': rel_type
                    })
        
        if invalid_relationships:
            report['relationship_validation'][doc_name] = invalid_relationships

    def _validate_relationship_metadata(self, source: Dict, target: Dict, rel_type: str) -> bool:
        """Validate relationship metadata between two documents."""
        try:
            # Validate basic metadata
            required_fields = {'title', 'type', 'url'}
            if not all(field in source for field in required_fields) or \
               not all(field in target for field in required_fields):
                return False
            
            # Validate type compatibility
            if rel_type == 'child_pages':
                # Child should be a subtype or related type
                if not self._is_compatible_type(source['type'], target['type']):
                    return False
            
            # Add more metadata validation as needed
            return True
            
        except Exception as e:
            logger.error(f"Error validating relationship metadata: {e}")
            return False
    
    def _is_compatible_type(self, parent_type: str, child_type: str) -> bool:
        """Check if two documentation types are compatible for parent-child relationship."""
        # Define type compatibility rules
        type_hierarchy = {
            'framework': {'class', 'protocol', 'struct', 'enum'},
            'class': {'method', 'property', 'enum'},
            'protocol': {'method', 'property'},
            'struct': {'method', 'property', 'enum'},
            'enum': {'case', 'method', 'property'}
        }
        
        return child_type in type_hierarchy.get(parent_type, set())

    def _check_broken_links(self, content: Dict, report: Dict):
        """Check for broken documentation links."""
        def extract_links(text: str) -> Set[str]:
            return set(re.findall(r'https?://developer\.apple\.com/[^\s\'"]+', text))
        
        all_text = json.dumps(content)
        for link in extract_links(all_text):
            cached_file = self._get_cached_file(link)
            if not cached_file or not cached_file.exists():
                report['broken_links'].add(link)
