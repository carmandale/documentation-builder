from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import re

class AppPhase(str, Enum):
    """VisionOS app lifecycle phases"""
    LAUNCH = "launch"
    ACTIVATION = "activation"
    SCENE_SETUP = "scene_setup"
    CONTENT_LOADING = "content_loading"
    INTERACTION = "interaction"
    BACKGROUND = "background"
    DEACTIVATION = "deactivation"

class StateManagementType(str, Enum):
    """Types of state management in VisionOS"""
    OBSERVABLE = "observable"
    STATE_OBJECT = "state_object"
    ENVIRONMENT_OBJECT = "environment_object"
    BINDING = "binding"
    APP_STORAGE = "app_storage"
    SCENE_STORAGE = "scene_storage"

class AssetLoadingStrategy(str, Enum):
    """Asset loading strategies in VisionOS"""
    PRELOAD = "preload"
    LAZY = "lazy"
    STREAMING = "streaming"
    ON_DEMAND = "on_demand"
    BACKGROUND = "background"

class InteractionType(str, Enum):
    """Types of interactions in VisionOS"""
    DIRECT = "direct"  # Direct manipulation
    INDIRECT = "indirect"  # System controls
    GAZE = "gaze"  # Eye tracking
    GESTURE = "gesture"  # Hand gestures
    SPATIAL = "spatial"  # Spatial interactions

@dataclass
class StatePattern:
    """State management pattern"""
    type: StateManagementType
    file_path: str
    code_context: str
    dependencies: List[str]
    scope: str
    usage_example: str
    best_practices: List[str]

@dataclass
class AssetLoadingPattern:
    """Asset loading pattern"""
    strategy: AssetLoadingStrategy
    file_path: str
    code_context: str
    asset_types: List[str]
    performance_notes: List[str]
    error_handling: str

@dataclass
class InteractionPattern:
    """Interaction pattern"""
    type: InteractionType
    file_path: str
    code_context: str
    feedback_mechanism: str
    accessibility: List[str]
    best_practices: List[str]

@dataclass
class AppPhasePattern:
    """App lifecycle phase pattern"""
    phase: AppPhase
    file_path: str
    code_context: str
    critical_operations: List[str]
    state_changes: List[str]
    performance_considerations: List[str]

class VisionOSPatternAnalyzer:
    """Analyzes VisionOS patterns in sample projects"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.state_patterns: List[StatePattern] = []
        self.asset_patterns: List[AssetLoadingPattern] = []
        self.interaction_patterns: List[InteractionPattern] = []
        self.phase_patterns: List[AppPhasePattern] = []
    
    def analyze_state_management(self):
        """Analyze state management patterns"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = str(file_path.relative_to(self.project_path))
            
            # Analyze Observable patterns
            if '@Observable' in content:
                self._analyze_observable_pattern(content, rel_path)
            
            # Analyze StateObject patterns
            if '@StateObject' in content:
                self._analyze_state_object_pattern(content, rel_path)
            
            # Analyze Environment patterns
            if '@Environment' in content or '@EnvironmentObject' in content:
                self._analyze_environment_pattern(content, rel_path)
            
            # Analyze Scene Storage
            if 'SceneStorage' in content:
                self._analyze_scene_storage_pattern(content, rel_path)
    
    def analyze_asset_loading(self):
        """Analyze asset loading patterns"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = str(file_path.relative_to(self.project_path))
            
            # Analyze model loading
            if 'ModelEntity' in content or 'loadModel' in content:
                self._analyze_model_loading(content, rel_path)
            
            # Analyze texture loading
            if 'MaterialParameters' in content or 'TextureResource' in content:
                self._analyze_texture_loading(content, rel_path)
            
            # Analyze audio loading
            if 'AudioFileResource' in content:
                self._analyze_audio_loading(content, rel_path)
    
    def analyze_interactions(self):
        """Analyze interaction patterns"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = str(file_path.relative_to(self.project_path))
            
            # Analyze gesture interactions
            if 'gesture' in content.lower():
                self._analyze_gesture_interaction(content, rel_path)
            
            # Analyze direct manipulation
            if 'onTapGesture' in content or 'dragGesture' in content:
                self._analyze_direct_interaction(content, rel_path)
            
            # Analyze spatial interactions
            if 'SpatialTapGesture' in content or 'WorldTracking' in content:
                self._analyze_spatial_interaction(content, rel_path)
    
    def analyze_app_phases(self):
        """Analyze app lifecycle phases"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = str(file_path.relative_to(self.project_path))
            
            # Analyze app launch
            if 'WindowGroup' in content or 'App.swift' in str(file_path):
                self._analyze_launch_phase(content, rel_path)
            
            # Analyze scene setup
            if 'ImmersiveSpace' in content or 'RealityView' in content:
                self._analyze_scene_setup_phase(content, rel_path)
            
            # Analyze content loading
            if 'Task' in content or 'async' in content:
                self._analyze_content_loading_phase(content, rel_path)
    
    def _analyze_observable_pattern(self, content: str, file_path: str):
        """Analyze Observable pattern usage"""
        matches = re.finditer(r'@Observable\s+class\s+(\w+)', content)
        for match in matches:
            class_name = match.group(1)
            context = self._get_context(content, match.start())
            
            self.state_patterns.append(StatePattern(
                type=StateManagementType.OBSERVABLE,
                file_path=file_path,
                code_context=context,
                dependencies=['Observation'],
                scope='Class-level state',
                usage_example=f"Observable class {class_name}",
                best_practices=[
                    "Use for complex state management",
                    "Prefer over StateObject for shared state",
                    "Keep state updates on main thread"
                ]
            ))
    
    def _analyze_model_loading(self, content: str, file_path: str):
        """Analyze model loading patterns"""
        if 'ModelEntity.load' in content:
            context = self._get_context(content, content.index('ModelEntity.load'))
            
            self.asset_patterns.append(AssetLoadingPattern(
                strategy=AssetLoadingStrategy.LAZY,
                file_path=file_path,
                code_context=context,
                asset_types=['3D Models', 'USDZ'],
                performance_notes=[
                    "Load models asynchronously",
                    "Consider memory impact",
                    "Cache frequently used models"
                ],
                error_handling="Use do-catch with specific error handling"
            ))
    
    def _analyze_gesture_interaction(self, content: str, file_path: str):
        """Analyze gesture interaction patterns"""
        if 'SpatialTapGesture' in content:
            context = self._get_context(content, content.index('SpatialTapGesture'))
            
            self.interaction_patterns.append(InteractionPattern(
                type=InteractionType.GESTURE,
                file_path=file_path,
                code_context=context,
                feedback_mechanism="Haptic and visual feedback",
                accessibility=["Voice commands", "Alternative controls"],
                best_practices=[
                    "Provide clear visual indicators",
                    "Handle gesture conflicts",
                    "Consider hand visibility"
                ]
            ))
    
    def _analyze_launch_phase(self, content: str, file_path: str):
        """Analyze app launch phase"""
        if 'WindowGroup' in content:
            context = self._get_context(content, content.index('WindowGroup'))
            
            self.phase_patterns.append(AppPhasePattern(
                phase=AppPhase.LAUNCH,
                file_path=file_path,
                code_context=context,
                critical_operations=[
                    "Initialize core state",
                    "Set up window configuration",
                    "Prepare initial views"
                ],
                state_changes=[
                    "App state initialization",
                    "Environment setup",
                    "Initial data loading"
                ],
                performance_considerations=[
                    "Minimize launch time",
                    "Defer non-critical operations",
                    "Optimize initial state setup"
                ]
            ))
    
    def _get_context(self, content: str, start_index: int, context_lines: int = 5) -> str:
        """Get code context around an index"""
        lines = content.split('\n')
        line_num = content[:start_index].count('\n')
        start = max(0, line_num - context_lines)
        end = min(len(lines), line_num + context_lines + 1)
        return '\n'.join(lines[start:end])
    
    def generate_pattern_guide(self) -> Dict:
        """Generate a comprehensive pattern guide"""
        return {
            'state_management': {
                'patterns': [
                    {
                        'type': pattern.type.value,
                        'usage': pattern.usage_example,
                        'best_practices': pattern.best_practices
                    }
                    for pattern in self.state_patterns
                ],
                'recommendations': [
                    "Use Observable for complex shared state",
                    "Prefer StateObject for view-specific state",
                    "Use Environment for dependency injection",
                    "Consider SceneStorage for persistence"
                ]
            },
            'asset_loading': {
                'patterns': [
                    {
                        'strategy': pattern.strategy.value,
                        'performance_notes': pattern.performance_notes
                    }
                    for pattern in self.asset_patterns
                ],
                'best_practices': [
                    "Load assets asynchronously",
                    "Implement proper error handling",
                    "Use appropriate caching strategies",
                    "Consider memory management"
                ]
            },
            'interactions': {
                'patterns': [
                    {
                        'type': pattern.type.value,
                        'best_practices': pattern.best_practices
                    }
                    for pattern in self.interaction_patterns
                ],
                'guidelines': [
                    "Provide clear visual feedback",
                    "Ensure accessibility",
                    "Handle multiple interaction types",
                    "Consider spatial awareness"
                ]
            },
            'app_phases': {
                'phases': [
                    {
                        'phase': pattern.phase.value,
                        'critical_operations': pattern.critical_operations,
                        'performance_considerations': pattern.performance_considerations
                    }
                    for pattern in self.phase_patterns
                ],
                'optimization_tips': [
                    "Optimize app launch sequence",
                    "Implement proper state transitions",
                    "Handle background/foreground transitions",
                    "Manage resource cleanup"
                ]
            }
        }
