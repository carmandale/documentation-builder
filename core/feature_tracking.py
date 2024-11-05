from typing import Dict, List
from pathlib import Path
import json
from datetime import datetime

class FeatureTracker:
    """Tracks feature status and changes"""
    
    def __init__(self):
        self.features = {
            'url_discovery': {
                'status': 'working',
                'last_verified': None,
                'dependencies': ['DocumentationURLCollector', 'URLSources'],
                'test_files': ['test_functionality.py']
            },
            'pattern_analysis': {
                'status': 'working',
                'last_verified': None,
                'dependencies': ['DocumentationAnalyzer', 'PatternEvolution'],
                'test_files': ['test_functionality.py']
            },
            'project_download': {
                'status': 'working',
                'last_verified': None,
                'dependencies': ['DocumentationURLCollector'],
                'test_files': ['test_functionality.py']
            }
        }
    
    def verify_feature(self, feature_name: str):
        """Mark a feature as verified"""
        if feature_name in self.features:
            self.features[feature_name]['last_verified'] = datetime.now().isoformat()
            self.features[feature_name]['status'] = 'working'
    
    def get_feature_status(self, feature_name: str) -> Dict:
        """Get current status of a feature"""
        return self.features.get(feature_name, {})
    
    def get_working_features(self) -> List[str]:
        """Get list of currently working features"""
        return [name for name, data in self.features.items() 
                if data['status'] == 'working'] 