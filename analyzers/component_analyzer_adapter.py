from pathlib import Path
from typing import List, Dict, Optional, Any
import re
from collections import defaultdict
from utils.logging import logger
from .component_analyzer import ComponentAnalyzer
from core.enhanced_knowledge_base import EnhancedVisionOSKnowledgeBase
from patterns.visionos_patterns import (
    VisionOSPattern,
    VisionOSPatternType,
    get_pattern,
    get_patterns_by_type,
    validate_pattern
)
from dataclasses import dataclass

@dataclass
class ComponentMetadata:
    """Metadata about a VisionOS component."""
    name: str
    type: str
    required_imports: List[str]
    required_permissions: List[str]
    features: List[str]
    related_components: List[str]
    best_practices: List[str]
    patterns: List[VisionOSPattern]

@dataclass
class ComponentRelationship:
    """Relationship between two components."""
    source: str
    target: str
    relationship_type: str
    required: bool
    state_sharing: Optional[str]
    communication_pattern: Optional[str]

class ComponentAnalyzerAdapter:
    """Analyzes VisionOS components and extracts metadata."""
    
    def __init__(self, knowledge_base: EnhancedVisionOSKnowledgeBase):
        self.knowledge_base = knowledge_base
        self.component_analyzer = ComponentAnalyzer()
        
    def analyze_file(self, file_path: Path) -> List[ComponentMetadata]:
        """Analyze a Swift file for VisionOS components."""
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return []
            
        content = file_path.read_text()
        components = []
        
        # Core VisionOS patterns
        patterns = {
            'struct_view': r"struct\s+(\w+)\s*:\s*View\s*{",
            'class_view': r"class\s+(\w+)\s*:\s*View\s*{",
            'window_group': r"WindowGroup\s*(\(.*?\))?\s*{",
            'immersive_space': r"ImmersiveSpace\s*(\(.*?\))?\s*{",
            'reality_view': r"RealityView\s*{\s*content\s+in",
            'entity_component': r"Entity\s*{\s*(\w+)\s+in",
            'spatial_anchor': r"AnchorEntity\(.*?\)",
            'attachment': r"@Attachable\s+var\s+(\w+)",
        }
        
        # Find all component definitions
        for pattern_type, pattern in patterns.items():
            for match in re.finditer(pattern, content):
                name = match.group(1) if '(' in pattern else match.group(0)
                component_type = self._determine_component_type(content, pattern_type)
                component = self._create_component_metadata(name, content, component_type)
                components.append(component)
                
        return components
        
    def _determine_component_type(self, content: str, pattern_type: str) -> str:
        """Determine the type of a component based on its pattern type."""
        type_mapping = {
            'struct_view': 'SwiftUI',
            'class_view': 'SwiftUI',
            'window_group': 'WindowGroup',
            'immersive_space': 'ImmersiveSpace',
            'reality_view': 'RealityKit',
            'entity_component': 'Entity',
            'spatial_anchor': 'Anchor',
            'attachment': 'Attachment'
        }
        return type_mapping.get(pattern_type, 'Unknown')
        
    def _create_component_metadata(self, name: str, content: str, component_type: str) -> ComponentMetadata:
        """Create metadata for a component."""
        patterns = self._find_matching_patterns(content)
        
        return ComponentMetadata(
            name=name,
            type=component_type,
            required_imports=self._extract_imports(content),
            required_permissions=self._extract_permissions(content, patterns),
            features=self._extract_features(content, patterns),
            related_components=[r.source for r in self._find_related_components(content, patterns)],
            best_practices=self._extract_best_practices(content, patterns),
            patterns=patterns
        )
        
    def _find_matching_patterns(self, content: str) -> List[VisionOSPattern]:
        """Find VisionOS patterns that match the content."""
        matching_patterns = []
        
        # Check each pattern type
        for pattern_type in VisionOSPatternType:
            patterns = get_patterns_by_type(pattern_type)
            for pattern in patterns:
                if self._matches_pattern_structure(content, pattern):
                    matching_patterns.append(pattern)
        
        return matching_patterns
        
    def _matches_pattern_structure(self, content: str, pattern: VisionOSPattern) -> bool:
        """Check if content matches a pattern's structure."""
        # Check imports
        for required_import in pattern.required_imports:
            if not re.search(rf"import\s+{required_import}", content):
                return False
                
        # Check permissions
        for permission in pattern.required_permissions:
            permission_pattern = rf"@Environment\(\\\.{permission}\)|{permission}System"
            if not re.search(permission_pattern, content):
                return False
                
        return True
        
    def _extract_imports(self, content: str) -> List[str]:
        """Extract framework imports."""
        imports = re.findall(r"import\s+(\w+)", content)
        return list(set(imports))
        
    def _extract_permissions(self, content: str, patterns: List[VisionOSPattern]) -> List[str]:
        """Extract required permissions."""
        permissions = set()
        
        # Get permissions from patterns
        for pattern in patterns:
            permissions.update(pattern.required_permissions)
            
        # Look for additional permissions in code
        permission_patterns = {
            "handTracking": r"@Environment\(\\\.handTracking\)|handTrackingSystem",
            "immersiveSpace": r"@Environment\(\\\.openImmersiveSpace\)|immersiveSpaceSystem",
            "nearbyInteraction": r"@Environment\(\\\.nearbyInteraction\)|nearbyInteractionSystem"
        }
        
        for permission, pattern in permission_patterns.items():
            if re.search(pattern, content):
                permissions.add(permission)
                
        return list(permissions)
        
    def _extract_features(self, content: str, patterns: List[VisionOSPattern]) -> List[str]:
        """Extract component features."""
        features = set()
        
        # Features from patterns
        for pattern in patterns:
            if pattern.type == VisionOSPatternType.HAND_TRACKING:
                features.add("hand_tracking")
            elif pattern.type == VisionOSPatternType.IMMERSIVE_SPACE:
                features.add("immersive_space")
            elif pattern.type == VisionOSPatternType.VOLUMETRIC:
                features.add("volumetric_content")
                
        # Additional feature detection
        feature_patterns = {
            "gesture_recognition": r"\.gesture\(|\.onTapGesture|\.onLongPressGesture",
            "3d_content": r"ModelEntity|Entity|AnchorEntity",
            "animation": r"\.animation\(|withAnimation|AnimationPhase",
            "haptic_feedback": r"\.sensoryFeedback|\.impact\(|\.selection"
        }
        
        for feature, pattern in feature_patterns.items():
            if re.search(pattern, content):
                features.add(feature)
                
        return list(features)
        
    def _find_related_components(self, content: str, patterns: List[VisionOSPattern]) -> List[ComponentRelationship]:
        """Find relationships between components."""
        relationships = []
        component_names = set()
        
        # Find all component references
        view_pattern = r"(?:struct|class)\s+(\w+)\s*:\s*View\s*{"
        reality_view_pattern = r"RealityView\s*{\s*content\s+in"
        entity_pattern = r"ModelEntity|Entity|AnchorEntity"
        
        # Collect component names
        for match in re.finditer(view_pattern, content):
            component_names.add(match.group(1))
            
        if re.search(reality_view_pattern, content):
            component_names.add("RealityView")
            
        if re.search(entity_pattern, content):
            component_names.add("Entity")
            
        # Analyze relationships
        for name in component_names:
            # Check for parent-child relationships
            child_pattern = rf"{name}\s*{{\s*([^}}]+)}}"
            for match in re.finditer(child_pattern, content):
                child_content = match.group(1)
                for other in component_names:
                    if other != name and other in child_content:
                        relationships.append(
                            ComponentRelationship(
                                source=name,
                                target=other,
                                relationship_type="parent-child",
                                required=True,
                                state_sharing=self._detect_state_sharing(content),
                                communication_pattern=self._detect_communication(child_content)
                            )
                        )
            
            # Check for dependencies
            for other in component_names:
                if other != name:
                    if re.search(rf"@ObservedObject\s+var\s+\w+\s*:\s*{other}", content):
                        relationships.append(
                            ComponentRelationship(
                                source=name,
                                target=other,
                                relationship_type="dependency",
                                required=True,
                                state_sharing="ObservedObject",
                                communication_pattern="Publisher-Subscriber"
                            )
                        )
                    elif re.search(rf"@StateObject\s+var\s+\w+\s*:\s*{other}", content):
                        relationships.append(
                            ComponentRelationship(
                                source=name,
                                target=other,
                                relationship_type="dependency",
                                required=True,
                                state_sharing="StateObject",
                                communication_pattern="Owner-Owned"
                            )
                        )
        
        return relationships
        
    def _detect_state_sharing(self, content: str) -> Dict[str, Any]:
        """Detect how components share and manage state in VisionOS."""
        state_patterns = {
            # VisionOS-specific State
            'sceneStorage': {
                'pattern': r'@SceneStorage\("(.*?)"\)\s+(?:private\s+)?var\s+(\w+)',
                'type': 'scene_persistent',
                'scope': 'immersive_scene',
                'persistence': 'scene_level'
            },
            'spaceState': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)(?=.*ImmersiveSpace)',
                'type': 'space_state',
                'scope': 'immersive_space',
                'persistence': 'space_lifetime'
            },
            'entityState': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)(?=.*Entity)',
                'type': 'entity_state',
                'scope': 'entity',
                'persistence': 'entity_lifetime'
            },
            'anchorState': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)(?=.*AnchorEntity)',
                'type': 'anchor_state',
                'scope': 'spatial_anchor',
                'persistence': 'anchor_lifetime'
            },
            
            # RealityKit Integration
            'realityState': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)(?=.*RealityView)',
                'type': 'reality_state',
                'scope': 'reality_view',
                'persistence': 'view_lifetime'
            },
            'volumetricState': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)(?=.*Volume)',
                'type': 'volumetric_state',
                'scope': 'volumetric_content',
                'persistence': 'content_lifetime'
            },
            
            # Multi-user State
            'sharedState': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)(?=.*shared)',
                'type': 'shared_state',
                'scope': 'multi_user',
                'persistence': 'session'
            },
            
            # Tracking State
            'trackingState': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)(?=.*tracking)',
                'type': 'tracking_state',
                'scope': 'spatial_tracking',
                'persistence': 'tracking_session'
            },
            
            # Standard SwiftUI State (but in VisionOS context)
            'state': {
                'pattern': r'@State\s+(?:private\s+)?var\s+(\w+)',
                'type': 'view_state',
                'scope': 'view',
                'persistence': 'temporary'
            },
            'stateObject': {
                'pattern': r'@StateObject\s+(?:private\s+)?var\s+(\w+)',
                'type': 'object_state',
                'scope': 'object_lifetime',
                'persistence': 'persistent'
            },
            'observedObject': {
                'pattern': r'@ObservedObject\s+(?:private\s+)?var\s+(\w+)',
                'type': 'shared_object',
                'scope': 'shared',
                'persistence': 'external'
            }
        }
        
        state_usage = {}
        
        # Detect state patterns
        for state_type, info in state_patterns.items():
            matches = list(re.finditer(info['pattern'], content))
            if matches:
                state_usage[state_type] = {
                    'variables': [m.group(1) for m in matches],
                    'type': info['type'],
                    'scope': info['scope'],
                    'persistence': info['persistence']
                }
        
        # Detect RealityKit state management
        if re.search(r'RealityKit\s*\{', content):
            state_usage['realitykit_integration'] = {
                'has_reality_view': bool(re.search(r'RealityView\s*{', content)),
                'has_entity_management': bool(re.search(r'Entity\s*{', content)),
                'has_anchor_management': bool(re.search(r'AnchorEntity', content)),
                'has_spatial_tracking': bool(re.search(r'ARSession|WorldTracking', content))
            }
        
        # Detect multi-user state patterns
        if re.search(r'GroupSession|SharedSpace', content):
            state_usage['multi_user_features'] = {
                'has_group_session': bool(re.search(r'GroupSession', content)),
                'has_shared_space': bool(re.search(r'SharedSpace', content)),
                'has_synchronization': bool(re.search(r'synchronize|sync', content, re.I))
            }
        
        return state_usage
        
    def _extract_state_patterns(self, content: str) -> List[Dict[str, Any]]:
        """Extract state management patterns from the content."""
        patterns = []
        state_usage = self._detect_state_sharing(content)
        
        # Analyze state patterns
        for state_type, info in state_usage.items():
            if state_type == 'state':
                patterns.append({
                    'type': 'LocalState',
                    'description': 'Simple view-local state management',
                    'variables': info['variables'],
                    'best_practices': [
                        'Use for simple view-specific state',
                        'Keep state close to where it\'s used',
                        'Consider using StateObject for complex state'
                    ]
                })
            elif state_type in ['stateObject', 'observedObject']:
                patterns.append({
                    'type': 'SharedState',
                    'description': 'Complex shared state management',
                    'variables': info['variables'],
                    'best_practices': [
                        'Use StateObject for state ownership',
                        'Use ObservedObject for state sharing',
                        'Implement proper state update methods'
                    ]
                })
            elif state_type == 'environmentObject':
                patterns.append({
                    'type': 'GlobalState',
                    'description': 'App-wide state management',
                    'variables': info['variables'],
                    'best_practices': [
                        'Use sparingly for truly global state',
                        'Consider using StateObject for more localized sharing',
                        'Document the environment object lifecycle'
                    ]
                })
                
        return patterns
        
    def _detect_communication(self, content: str) -> Optional[str]:
        """Detect communication patterns between components."""
        if ".sink" in content or ".publisher" in content:
            return "Publisher-Subscriber"
        elif "@escaping" in content:
            return "Callback"
        elif "delegate" in content.lower():
            return "Delegate"
        elif "NotificationCenter" in content:
            return "Notification"
        return None

    def _extract_best_practices(self, content: str, patterns: List[VisionOSPattern]) -> List[str]:
        """Extract best practices from patterns."""
        best_practices = set()
        
        for pattern in patterns:
            best_practices.update(pattern.best_practices)
            
        return list(best_practices)
    
    def _extract_initialization_pattern(self, content: str, component_name: str) -> Optional[str]:
        """Extract initialization pattern for a component"""
        try:
            # Look for struct or class definition
            class_pattern = rf'(?:struct|class)\s+{component_name}\s*:.*{{(.*?)}}'
            class_match = re.search(class_pattern, content, re.DOTALL)
            
            if class_match:
                class_content = class_match.group(1)
                # Look for init method
                init_pattern = r'init\s*\([^)]*\)\s*{[^}]*}'
                init_match = re.search(init_pattern, class_content)
                if init_match:
                    return init_match.group(0)
                
            # Look for property initialization
            prop_pattern = rf'{component_name}\s*\([^)]*\)'
            prop_match = re.search(prop_pattern, content)
            if prop_match:
                return prop_match.group(0)
                
        except Exception as e:
            logger.error(f"Error extracting initialization pattern for {component_name}: {e}")
            
        return None
    
    def _extract_common_properties(self, content: str, component_name: str) -> List[Dict[str, Any]]:
        """Extract common properties for a component"""
        properties = []
        try:
            # Look for property definitions
            prop_pattern = r'(?:var|let)\s+(\w+)\s*:\s*([^{=\n]+)(?:\s*=\s*([^{\n]+))?'
            matches = re.finditer(prop_pattern, content)
            
            for match in matches:
                prop_name = match.group(1)
                prop_type = match.group(2).strip()
                default_value = match.group(3).strip() if match.group(3) else None
                
                properties.append({
                    'name': prop_name,
                    'type': prop_type,
                    'default_value': default_value
                })
                
        except Exception as e:
            logger.error(f"Error extracting properties for {component_name}: {e}")
            
        return properties
    
    def _extract_constraints(self, content: str, component_name: str) -> List[Dict[str, Any]]:
        """Extract usage constraints for a component"""
        constraints = []
        
        # Check for OS version requirements
        os_pattern = r'if\s+#available\(visionOS\s+(\d+\.\d+),.*\)'
        os_match = re.search(os_pattern, content)
        if os_match:
            constraints.append({
                'type': 'version',
                'min_version': os_match.group(1)
            })
        
        # Check for device requirements
        if re.search(r'Vision\s*Pro', content):
            constraints.append({
                'type': 'device',
                'supported_devices': ['Apple Vision Pro']
            })
        
        return constraints
    
    def _find_documentation_url(self, component_name: str) -> str:
        """Find documentation URL for a component"""
        # This would ideally come from a mapping file or documentation index
        base_url = "https://developer.apple.com/documentation/visionos/"
        return f"{base_url}{component_name.lower()}"
