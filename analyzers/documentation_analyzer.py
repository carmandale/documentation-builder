from bs4 import BeautifulSoup
from typing import List, Dict
import re

class DocumentationAnalyzer:
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