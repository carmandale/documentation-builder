from pathlib import Path
from typing import List, Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    """Analyzes downloaded Xcode projects for patterns and examples"""
    
    def __init__(self, projects_dir: Path = Path('data/projects')):
        self.projects_dir = projects_dir
    
    def analyze_project(self, project_path: Path) -> Dict[str, any]:
        """Analyze a downloaded project"""
        try:
            # Find Swift files
            swift_files = list(project_path.rglob('*.swift'))
            logger.info(f"Found {len(swift_files)} Swift files")
            
            patterns = {
                '3d_content': [],
                'animation': [],
                'transforms': [],
                'ui_components': []
            }
            
            # Track pattern frequency and validation
            pattern_usage = {}
            pattern_validation = {}
            
            for file in swift_files:
                content = file.read_text()
                logger.info(f"\nAnalyzing {file.name}:")
                
                # Look for specific patterns
                if 'RealityKit' in content:
                    self._analyze_patterns(content, file.name, patterns, pattern_usage, pattern_validation)
            
            return {
                'patterns': patterns,
                'usage': pattern_usage,
                'validation': pattern_validation
            }
            
        except Exception as e:
            logger.error(f"Error analyzing project: {str(e)}")
            return {}
    
    def _extract_code_block(self, content: str, pattern: str, context_lines: int = 5) -> str:
        """Extract code block around a pattern with context"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if pattern in line:
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                return '\n'.join(lines[start:end])
        return ""
    
    def analyze_api_patterns(self, content: str) -> Dict[str, any]:
        """Analyze how APIs are used in the code"""
        api_patterns = {
            'container_types': {},  # Track what container types are used
            'method_usage': {},     # Track how methods are called
            'common_patterns': []   # Track recurring patterns
        }
        
        # Example: Track EventSubscription usage
        if 'EventSubscription' in content:
            container_match = re.search(
                r'(var|let)\s+\w+\s*:\s*(\[|\{).*EventSubscription', 
                content
            )
            if container_match:
                container_type = 'Array' if container_match.group(2) == '[' else 'Set'
                api_patterns['container_types']['EventSubscription'] = container_type
                
        # Track quaternion operations
        if 'simd_quatf' in content:
            for line in content.split('\n'):
                if 'simd_quatf' in line:
                    if '*' in line:
                        api_patterns['method_usage'].setdefault('quaternion', set()).add('multiplication')
                    if 'concatenated' in line:
                        api_patterns['method_usage'].setdefault('quaternion', set()).add('concatenation')
        
        return api_patterns
    
    def _analyze_animation_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze animation state machine patterns"""
        animation_matches = [
            line.strip()
            for line in content.split('\n')
            if 'AnimationState' in line and not line.strip().startswith('//')
        ]
        if animation_matches:
            pattern_key = 'animation_state_machine'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['animation'].append({
                'file': filename,
                'type': 'state_machine',
                'content': '\n'.join(animation_matches),
                'context': self._extract_code_block(content, animation_matches[0], 15)
            })
    
    def _analyze_patterns(self, content: str, filename: str, patterns: Dict, usage: Dict, validation: Dict):
        """Analyze code for specific patterns"""
        try:
            # Look for animation patterns
            if 'RealityKit' in content:
                self._analyze_animation_pattern(content, filename, patterns, usage)
                
                # Look for transform patterns
                if 'transform' in content:
                    self._analyze_transform_pattern(content, filename, patterns, usage)
                    
                # Look for event subscription patterns
                if 'subscribe' in content:
                    self._analyze_subscription_pattern(content, filename, patterns, usage)
                    
        except Exception as e:
            logger.error(f"Error analyzing patterns in {filename}: {str(e)}")
    
    def _analyze_transform_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze transform and rotation patterns"""
        transform_matches = [
            line.strip()
            for line in content.split('\n')
            if 'transform' in line and ('rotation' in line or 'simd_quatf' in line)
            and not line.strip().startswith('//')
        ]
        if transform_matches:
            pattern_key = 'transform_rotation'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['transforms'].append({
                'file': filename,
                'type': 'rotation',
                'content': '\n'.join(transform_matches),
                'context': self._extract_code_block(content, transform_matches[0], 15)
            })
    
    def _analyze_subscription_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze event subscription patterns"""
        subscription_matches = [
            line.strip()
            for line in content.split('\n')
            if 'subscribe' in line and not line.strip().startswith('//')
        ]
        if subscription_matches:
            pattern_key = 'event_subscription'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['ui_components'].append({
                'file': filename,
                'type': 'subscription',
                'content': '\n'.join(subscription_matches),
                'context': self._extract_code_block(content, subscription_matches[0], 15)
            })