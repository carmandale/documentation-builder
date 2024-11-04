from bs4 import BeautifulSoup
from models.base import ConceptRelationship, CodePattern
from typing import List
import logging

logger = logging.getLogger(__name__)

class RelationshipExtractor:
    """Extracts relationships between concepts in documentation"""
    
    def extract_relationships(self, soup: BeautifulSoup, code_patterns: dict) -> List[ConceptRelationship]:
        relationships = []
        
        # Extract relationships from section hierarchy
        section_relationships = self._extract_section_relationships(soup)
        relationships.extend(section_relationships)
        
        # Extract relationships from code pattern dependencies
        code_relationships = self._extract_code_relationships(code_patterns)
        relationships.extend(code_relationships)
        
        return relationships
    
    def _extract_section_relationships(self, soup: BeautifulSoup) -> List[ConceptRelationship]:
        relationships = []
        sections = soup.find_all(['h2', 'h3', 'h4'])
        
        for i, section in enumerate(sections[:-1]):
            next_section = sections[i + 1]
            if next_section.name > section.name:  # Child relationship
                relationships.append(
                    ConceptRelationship(
                        source=section.get_text(strip=True),
                        target=next_section.get_text(strip=True),
                        relationship_type="parent_child",
                        strength=1.0
                    )
                )
        
        return relationships
    
    def _extract_code_relationships(self, code_patterns: dict) -> List[ConceptRelationship]:
        relationships = []
        
        # Add framework dependencies
        for pattern_id, pattern in code_patterns.items():
            for framework in pattern.frameworks:
                relationships.append(
                    ConceptRelationship(
                        source=framework,
                        target=pattern_id,
                        relationship_type="framework_dependency",
                        strength=1.0
                    )
                )
                
            # Track pattern dependencies
            if 'RealityKit' in pattern.frameworks:
                self._analyze_realitykit_dependencies(pattern, relationships)
        
        return relationships
    
    def _analyze_realitykit_dependencies(self, pattern: CodePattern, relationships: List[ConceptRelationship]):
        """Analyze RealityKit specific dependencies"""
        if 'ModelEntity' in pattern.code:
            relationships.append(
                ConceptRelationship(
                    source='3d_content',
                    target=pattern.pattern_type,
                    relationship_type="concept_dependency",
                    strength=0.9
                )
            )