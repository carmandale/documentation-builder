from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, List
import json

class RelationshipTracker:
    """Tracks relationships between patterns and concepts"""
    
    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.relationships_file = knowledge_dir / 'relationships.json'
        self.relationships = self._load_relationships()
    
    def _load_relationships(self) -> Dict:
        """Load existing relationships from file"""
        if self.relationships_file.exists():
            return json.loads(self.relationships_file.read_text())
        return {}
    
    def _save_relationships(self):
        """Save relationships to file"""
        # Convert sets to lists for JSON serialization
        serializable = {}
        for key, rel in self.relationships.items():
            rel_copy = rel.copy()
            if 'evidence' in rel_copy:
                rel_copy['evidence'] = list(rel_copy['evidence'])
            serializable[key] = rel_copy
        
        self.relationships_file.write_text(json.dumps(serializable, indent=2))
    
    def _calculate_strength(self, evidence: List[Dict]) -> float:
        """Calculate relationship strength based on evidence"""
        if not evidence:
            return 0.5
        
        # More evidence increases strength
        base_strength = min(len(evidence) * 0.1, 0.5)
        
        # Recent evidence weighs more
        recent_strength = 0.0
        now = datetime.now(UTC)
        for e in evidence[-5:]:  # Look at last 5 pieces of evidence
            if 'timestamp' in e:
                age = (now - datetime.fromisoformat(e['timestamp'])).days
                recent_strength += max(0.1 - (age * 0.01), 0)
        
        return min(base_strength + recent_strength, 1.0)
    
    def record_relationship(self, source: str, target: str, relationship_type: str, 
                          evidence: Dict):
        """Record a relationship between patterns/concepts"""
        key = f"{source}:{target}"
        
        if key not in self.relationships:
            self.relationships[key] = {
                'type': relationship_type,
                'strength': 0.5,
                'evidence': [],
                'first_seen': datetime.now(UTC).isoformat()
            }
            
        rel = self.relationships[key]
        evidence['timestamp'] = datetime.now(UTC).isoformat()
        rel['evidence'].append(evidence)
        rel['strength'] = self._calculate_strength(rel['evidence'])
        
        self._save_relationships()
    
    def get_related_items(self, item: str, min_strength: float = 0.5) -> List[Dict]:
        """Get items related to the given item"""
        related = []
        
        for key, rel in self.relationships.items():
            source, target = key.split(':')
            if source == item and rel['strength'] >= min_strength:
                related.append({
                    'item': target,
                    'type': rel['type'],
                    'strength': rel['strength']
                })
                
        return related
    
    def get_relationship_stats(self) -> Dict:
        """Get statistics about tracked relationships"""
        stats = {
            'total_relationships': len(self.relationships),
            'relationship_types': {},
            'strongest_relationships': [],
            'most_connected_items': {}
        }
        
        # Count relationship types
        for rel in self.relationships.values():
            rel_type = rel['type']
            stats['relationship_types'][rel_type] = stats['relationship_types'].get(rel_type, 0) + 1
        
        # Find strongest relationships
        sorted_rels = sorted(
            self.relationships.items(), 
            key=lambda x: x[1]['strength'], 
            reverse=True
        )[:10]
        stats['strongest_relationships'] = [
            {'relationship': k, **v} for k, v in sorted_rels
        ]
        
        # Count connections per item
        for key in self.relationships:
            source, _ = key.split(':')
            stats['most_connected_items'][source] = stats['most_connected_items'].get(source, 0) + 1
        
        return stats