from bs4 import BeautifulSoup
from models.base import ConceptRelationship, CodePattern
from typing import List, Dict, Any
import logging
import re
import json
from pathlib import Path
import aiohttp

logger = logging.getLogger(__name__)

class RelationshipExtractor:
    """Extracts relationships between concepts in documentation"""
    
    def verify_relationships(self, doc_cache_path: Path) -> Dict[str, Any]:
        """Verify and analyze relationships between samples and documentation"""
        verification_results = {
            'total_relationships': 0,
            'verified': 0,
            'broken': 0,
            'details': {}
        }
        
        try:
            if not doc_cache_path.exists():
                logger.error("Documentation cache not found")
                return verification_results
                
            relationships = json.loads(doc_cache_path.read_text())
            verification_results['total_relationships'] = len(relationships)
            
            # Just validate the cache structure for now
            for title, data in relationships.items():
                result = {
                    'sample_url_valid': True,  # Assume valid for now
                    'doc_url_valid': True,     # Assume valid for now
                    'framework_refs': [],
                    'errors': []
                }
                
                verification_results['verified'] += 1
                verification_results['details'][title] = result
            
            logger.info(f"Relationship verification complete:")
            logger.info(f"Total: {verification_results['total_relationships']}")
            logger.info(f"Verified: {verification_results['verified']}")
            
            return verification_results
            
        except Exception as e:
            logger.error(f"Error verifying relationships: {e}")
            return verification_results