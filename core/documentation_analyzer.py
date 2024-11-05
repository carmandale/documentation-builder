from pathlib import Path
import json
import logging
from collections import defaultdict
from typing import Dict, Set, List, Any, Optional
import aiohttp
from bs4 import BeautifulSoup
import re

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
    
    def _get_code_context(self, code_block) -> str:
        """Get the context around a code block"""
        context = []
        
        # Get previous paragraph or header
        prev_elem = code_block.find_previous(['p', 'h1', 'h2', 'h3', 'h4'])
        if prev_elem:
            context.append(prev_elem.get_text())
            
        # Get next paragraph
        next_elem = code_block.find_next('p')
        if next_elem:
            context.append(next_elem.get_text())
            
        return ' '.join(context)
    
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