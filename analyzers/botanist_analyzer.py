from pathlib import Path
from typing import List, Dict
from .sample_project_analyzer import ProjectAnalyzer, BestPractice

class BotanistAnalyzer(ProjectAnalyzer):
    """Specialized analyzer for the Botanist sample project"""
    
    def __init__(self, project_path: Path):
        super().__init__(project_path)
        self.immersive_patterns = []
        self.volume_patterns = []
        self.interaction_patterns = []
        
    def analyze_immersive_patterns(self):
        """Analyze immersive space implementation patterns"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = file_path.relative_to(self.project_path)
            
            if 'ImmersiveSpace' in content:
                # Analyze immersive space setup
                self.immersive_patterns.extend([
                    {
                        'file': str(rel_path),
                        'pattern': 'ImmersiveSpace Setup',
                        'code': self._extract_context(content, 'ImmersiveSpace'),
                        'purpose': 'Define immersive experience container'
                    }
                ])
            
            if 'RealityView' in content:
                # Analyze reality view implementation
                self.immersive_patterns.extend([
                    {
                        'file': str(rel_path),
                        'pattern': 'RealityView Implementation',
                        'code': self._extract_context(content, 'RealityView'),
                        'purpose': 'Render 3D content in space'
                    }
                ])
    
    def analyze_volume_patterns(self):
        """Analyze volumetric content patterns"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = file_path.relative_to(self.project_path)
            
            if 'Entity' in content:
                # Analyze entity setup
                self.volume_patterns.extend([
                    {
                        'file': str(rel_path),
                        'pattern': 'Entity Setup',
                        'code': self._extract_context(content, 'Entity'),
                        'purpose': 'Define 3D object properties'
                    }
                ])
            
            if 'ModelEntity' in content:
                # Analyze model loading
                self.volume_patterns.extend([
                    {
                        'file': str(rel_path),
                        'pattern': 'Model Loading',
                        'code': self._extract_context(content, 'ModelEntity'),
                        'purpose': 'Load and configure 3D models'
                    }
                ])
    
    def analyze_interaction_patterns(self):
        """Analyze user interaction patterns"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = file_path.relative_to(self.project_path)
            
            if 'onTapGesture' in content or 'gesture' in content.lower():
                # Analyze gesture handling
                self.interaction_patterns.extend([
                    {
                        'file': str(rel_path),
                        'pattern': 'Gesture Handling',
                        'code': self._extract_context(content, 'gesture'),
                        'purpose': 'Handle user interactions'
                    }
                ])
            
            if 'StateObject' in content or '@State' in content:
                # Analyze state management
                self.interaction_patterns.extend([
                    {
                        'file': str(rel_path),
                        'pattern': 'State Management',
                        'code': self._extract_context(content, '@State'),
                        'purpose': 'Manage interactive state'
                    }
                ])
    
    def _extract_context(self, content: str, keyword: str, context_lines: int = 5) -> str:
        """Extract code context around a keyword"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                return '\n'.join(lines[start:end])
        return ""
    
    def generate_botanist_specific_plan(self) -> Dict:
        """Generate Botanist-specific development plan"""
        # Analyze all patterns
        self.analyze_immersive_patterns()
        self.analyze_volume_patterns()
        self.analyze_interaction_patterns()
        
        return {
            'project_overview': {
                'description': 'Interactive VisionOS application demonstrating immersive spaces, volumetric content, and natural interactions',
                'key_features': [
                    'Immersive 3D environment',
                    'Interactive plant models',
                    'Natural gesture interactions',
                    'State management',
                    'Spatial audio'
                ]
            },
            'implementation_phases': [
                {
                    'phase': 'Project Setup',
                    'steps': [
                        'Create VisionOS project',
                        'Configure project settings',
                        'Import required frameworks',
                        'Set up asset catalogs'
                    ]
                },
                {
                    'phase': 'Core Structure',
                    'steps': [
                        'Define app entry point',
                        'Create main view hierarchy',
                        'Set up navigation structure',
                        'Configure window groups'
                    ],
                    'patterns': self.patterns[:5]  # First 5 core patterns
                },
                {
                    'phase': 'Immersive Space',
                    'steps': [
                        'Create ImmersiveSpace view',
                        'Configure RealityView',
                        'Set up 3D scene',
                        'Add lighting and effects'
                    ],
                    'patterns': self.immersive_patterns
                },
                {
                    'phase': 'Volumetric Content',
                    'steps': [
                        'Create 3D model entities',
                        'Set up model loading',
                        'Configure transformations',
                        'Add animations'
                    ],
                    'patterns': self.volume_patterns
                },
                {
                    'phase': 'Interactions',
                    'steps': [
                        'Implement gesture recognition',
                        'Add state management',
                        'Create feedback systems',
                        'Polish user experience'
                    ],
                    'patterns': self.interaction_patterns
                }
            ],
            'best_practices': [
                {
                    'category': 'Performance',
                    'practices': [
                        'Optimize 3D model loading',
                        'Use efficient gesture handling',
                        'Manage memory for assets',
                        'Handle state updates efficiently'
                    ]
                },
                {
                    'category': 'User Experience',
                    'practices': [
                        'Provide clear interaction cues',
                        'Ensure comfortable viewing distances',
                        'Add spatial audio feedback',
                        'Maintain stable frame rate'
                    ]
                },
                {
                    'category': 'Code Organization',
                    'practices': [
                        'Separate concerns by feature',
                        'Use SwiftUI best practices',
                        'Maintain clear view hierarchy',
                        'Document complex interactions'
                    ]
                }
            ]
        }
