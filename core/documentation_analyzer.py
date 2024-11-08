from pathlib import Path
import json
import logging
from collections import defaultdict
from typing import Dict, Set, List, Any, Optional
import aiohttp
from bs4 import BeautifulSoup
import re
from datetime import datetime, UTC

logger = logging.getLogger(__name__)

class DocumentationAnalyzer:
    """Analyzes documentation content to discover patterns and categories"""
    
    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.category_patterns = self._load_patterns('category_patterns.json')
        self.discovered_patterns = defaultdict(lambda: defaultdict(int))
        self.topic_clusters = defaultdict(set)
        self.framework_relationships = defaultdict(set)
    
    def analyze_code_patterns(self, content: str, url: str) -> List[Dict]:
        """Analyze code patterns in documentation"""
        patterns = []
        
        # Find code blocks
        soup = BeautifulSoup(content, 'html.parser')
        code_blocks = soup.find_all('code')
        
        for block in code_blocks:
            # Get context
            context = self._get_code_context(block)
            
            # Analyze pattern
            pattern = {
                'code': block.get_text(),
                'context': context,
                'source_url': url,
                'implementation': self._extract_implementation_details(block),
                'related_patterns': self._find_related_patterns(block),
                'frameworks_used': self._extract_frameworks(block),
                'type': self._determine_pattern_type(block)
            }
            
            patterns.append(pattern)
            
            # Record in evolution tracker
            self.pattern_evolution.record_pattern_discovery(pattern)
        
        return patterns

    def _load_patterns(self, filename: str) -> Dict:
        """Load patterns from a JSON file"""
        file_path = self.knowledge_dir / filename
        if file_path.exists():
            return json.loads(file_path.read_text())
        return {}
    
    def _save_patterns(self, filename: str, data: Any):
        """Save patterns to a JSON file"""
        file_path = self.knowledge_dir / filename
        
        # Convert sets to lists for JSON serialization
        if isinstance(data, defaultdict):
            serializable = {k: dict(v) if isinstance(v, defaultdict) else list(v) 
                          for k, v in data.items()}
        elif isinstance(data, dict):
            serializable = {k: list(v) if isinstance(v, set) else v 
                          for k, v in data.items()}
        else:
            serializable = data
        
        file_path.write_text(json.dumps(serializable, indent=2))
    
    def _get_code_context(self, code_block) -> dict:
        """Get the context around a code block with improved structure and error handling
        
        Args:
            code_block: Either a BeautifulSoup element or a string of code
            
        Returns:
            dict: Structured context information containing:
                - section: The section title/header
                - description: Text describing the code
                - related_concepts: Any related concepts mentioned
                - framework_references: Framework references in context
                - implementation_notes: Any implementation details
        """
        try:
            context = {
                'section': '',
                'description': '',
                'related_concepts': [],
                'framework_references': [],
                'implementation_notes': ''
            }
            
            # Handle string input
            if isinstance(code_block, str):
                logger.debug("Received string code block, no context available")
                return context
                
            # Get section context (search up through parents)
            current = code_block
            while current:
                # Look for section header
                header = current.find_previous(['h1', 'h2', 'h3', 'h4'])
                if header:
                    context['section'] = header.get_text(strip=True)
                    break
                current = current.parent
                
            # Get immediate description (previous paragraph or list)
            desc_elem = code_block.find_previous(['p', 'ul', 'ol'])
            if desc_elem:
                context['description'] = desc_elem.get_text(strip=True)
                
            # Find related concepts (links in surrounding context)
            related_links = code_block.find_parent('section').find_all('a') if code_block.find_parent('section') else []
            context['related_concepts'] = [
                link.get_text(strip=True) 
                for link in related_links 
                if link.get('href') and 'documentation' in link.get('href')
            ]
            
            # Look for framework references
            framework_patterns = ['Kit', 'Framework', 'API']
            text_context = ' '.join(
                elem.get_text() 
                for elem in code_block.find_parent('section').find_all(['p', 'li']) 
                if elem
            )
            context['framework_references'] = [
                word for word in text_context.split() 
                if any(pattern in word for pattern in framework_patterns)
            ]
            
            # Get implementation notes (following paragraph)
            notes_elem = code_block.find_next(['p', 'ul', 'ol'])
            if notes_elem:
                context['implementation_notes'] = notes_elem.get_text(strip=True)
                
            return context
            
        except Exception as e:
            logger.error(f"Error getting code context: {str(e)}")
            return {
                'section': '',
                'description': '',
                'related_concepts': [],
                'framework_references': [],
                'implementation_notes': ''
            }
    
    def _extract_implementation_details(self, code_block) -> Dict:
        """Extract implementation details from code"""
        code = code_block.get_text()
        return {
            'frameworks': self._extract_frameworks(code_block),
            'patterns': self._extract_patterns(code),
            'complexity': self._estimate_complexity(code)
        }
    
    def _find_related_patterns(self, code_block) -> List[str]:
        """Find patterns related to this code block"""
        related = []
        code = code_block.get_text()
        
        # Look for related patterns in code and context
        context = self._get_code_context(code_block)
        
        # Add pattern detection logic here
        
        return related
    
    def _extract_frameworks(self, code_block) -> List[str]:
        """Extract framework imports from code"""
        code = code_block.get_text()
        frameworks = []
        
        # Look for import statements
        import_pattern = r'import\s+(\w+)'
        matches = re.finditer(import_pattern, code)
        frameworks.extend(match.group(1) for match in matches)
        
        return frameworks
    
    def _determine_pattern_type(self, code_block) -> str:
        """Determine the type of pattern in a code block"""
        code = code_block.get_text()
        context = self._get_code_context(code_block)
        
        # Look for known patterns
        for pattern_type, indicators in self.pattern_indicators.items():
            if any(re.search(indicator, code) for indicator in indicators):
                return pattern_type
        
        # Look for new patterns
        new_type = self._identify_new_pattern_type(code, context)
        if new_type:
            self._record_new_pattern_type(new_type, code, context)
            return new_type
            
        return 'unknown'
    
    def _extract_patterns(self, code: str) -> List[str]:
        """Extract coding patterns from code"""
        patterns = []
        
        # Add pattern extraction logic here
        
        return patterns
    
    def _estimate_complexity(self, code: str) -> int:
        """Estimate code complexity"""
        # Simple complexity estimation
        return len(code.split('\n'))
    
    def _identify_new_pattern_type(self, code: str, context: str) -> Optional[str]:
        """Identify potential new pattern types"""
        # Add pattern identification logic here
        return None
    
    def _record_new_pattern_type(self, pattern_type: str, code: str, context: str):
        """Record a newly discovered pattern type"""
        if pattern_type not in self.category_patterns:
            self.category_patterns[pattern_type] = {
                'examples': [{'code': code, 'context': context}],
                'first_seen': datetime.now(UTC).isoformat()
            }
            self._save_patterns('category_patterns.json', self.category_patterns) 
    
    def export_llm_knowledge_base(self, output_dir: Path):
        """Export analyzed data in LLM-friendly format"""
        output_dir.mkdir(exist_ok=True)
        
        # Export patterns with examples
        patterns_file = output_dir / 'patterns.json'
        relationships_file = output_dir / 'relationships.json'
        examples_file = output_dir / 'examples.json'
        
        # Structure data for LLM consumption
        knowledge_base = {
            'patterns': self.patterns,
            'examples': self.examples,
            'relationships': self.relationships,
            'metadata': {
                'version': '1.0',
                'generated': datetime.now(UTC).isoformat(),
                'sample_count': len(self.analyzed_samples),
                'pattern_types': list(self.patterns.keys())
            }
        }
        
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, indent=2)

    def _analyze_documentation_structure(self, soup: BeautifulSoup, links: Dict[str, Set[str]]):
        """Add ARKit pattern detection to documentation analysis"""
        try:
            # Existing code...
            
            # Find ARKit references
            arkit_refs = soup.find_all(
                lambda tag: tag.name in ['p', 'div', 'span', 'a'] and 
                'arkit' in tag.text.lower()
            )
            if arkit_refs:
                links['arkit'] = links.get('arkit', set())
                links['arkit'].add('ARKit')
                
        except Exception as e:
            logger.error(f"Error analyzing documentation structure: {str(e)}")