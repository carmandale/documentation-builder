import json
from pathlib import Path
from typing import Dict, Any, Set, List
from datetime import datetime, UTC
from collections import defaultdict

class PatternEvolution:
    """Tracks how patterns evolve based on discovered content"""
    
    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.evolution_file = knowledge_dir / 'pattern_evolution.json'
        self.pattern_history = self._load_history()
        
    def _load_history(self) -> Dict:
        """Load patterns from history file"""
        if self.evolution_file.exists():
            return json.loads(self.evolution_file.read_text())
        return {
            'patterns': {},
            'categories': {},
            'relationships': {},
            'versions': []
        }
    
    def _save_history(self):
        """Save patterns to history file"""
        # Convert sets to lists for JSON serialization
        serializable = {}
        for key, value in self.pattern_history.items():
            if isinstance(value, dict):
                serializable[key] = {
                    k: list(v) if isinstance(v, set) else v 
                    for k, v in value.items()
                }
            else:
                serializable[key] = list(value) if isinstance(value, set) else value
        
        self.evolution_file.write_text(json.dumps(serializable, indent=2))
    
    def record_pattern_discovery(self, pattern: Dict):
        """Record a newly discovered pattern"""
        timestamp = datetime.now(UTC).isoformat()
        
        if pattern['type'] not in self.pattern_history['patterns']:
            self.pattern_history['patterns'][pattern['type']] = {
                'first_seen': timestamp,
                'occurrences': 0,
                'variations': set(),
                'contexts': set(),
                'related_patterns': set()
            }
        
        entry = self.pattern_history['patterns'][pattern['type']]
        entry['occurrences'] += 1
        entry['variations'].add(pattern['implementation'])
        entry['contexts'].add(pattern['context'])
        
        if 'related_patterns' in pattern:
            entry['related_patterns'].update(pattern['related_patterns'])
        
        self._save_history()
    
    def _identify_new_patterns(self) -> List[Dict]:
        """Identify potential new patterns"""
        new_patterns = []
        
        # Look for patterns that appear frequently but aren't categorized
        for pattern_type, data in self.pattern_history['patterns'].items():
            if pattern_type not in self.pattern_history['categories']:
                if data['occurrences'] >= 3:  # Threshold for new pattern
                    new_patterns.append({
                        'type': pattern_type,
                        'occurrences': data['occurrences'],
                        'contexts': list(data['contexts']),
                        'confidence': min(data['occurrences'] / 10.0, 1.0)
                    })
        
        return new_patterns
    
    def _suggest_refinements(self) -> List[Dict]:
        """Suggest refinements to existing patterns"""
        refinements = []
        
        for pattern_type, data in self.pattern_history['patterns'].items():
            if len(data['variations']) > 1:
                refinements.append({
                    'type': pattern_type,
                    'variations': len(data['variations']),
                    'suggestion': 'Consider splitting pattern based on variations'
                })
        
        return refinements
    
    def _analyze_relationships(self) -> List[Dict]:
        """Analyze relationships between patterns"""
        relationships = []
        
        for pattern_type, data in self.pattern_history['patterns'].items():
            if data['related_patterns']:
                relationships.append({
                    'source': pattern_type,
                    'related': list(data['related_patterns']),
                    'strength': len(data['related_patterns']) / 10.0
                })
        
        return relationships
    
    def _suggest_categories(self) -> List[Dict]:
        """Suggest new categories based on pattern clustering"""
        categories = []
        
        # Group patterns by context similarity
        context_groups = defaultdict(list)
        for pattern_type, data in self.pattern_history['patterns'].items():
            for context in data['contexts']:
                context_key = context[:50]  # Use first 50 chars as key
                context_groups[context_key].append(pattern_type)
        
        # Suggest categories for groups with multiple patterns
        for context, patterns in context_groups.items():
            if len(patterns) > 1:
                categories.append({
                    'context': context,
                    'patterns': patterns,
                    'confidence': len(patterns) / 5.0
                })
        
        return categories
    
    def suggest_pattern_updates(self) -> Dict[str, Any]:
        """Suggest updates to pattern definitions based on history"""
        suggestions = {
            'new_patterns': self._identify_new_patterns(),
            'pattern_refinements': self._suggest_refinements(),
            'relationship_updates': self._analyze_relationships(),
            'category_changes': self._suggest_categories()
        }
        return suggestions