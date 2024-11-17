from typing import List, Dict, Set, Optional
from models.base import Pattern, PatternType, PatternRelationship, ValidationResult
import re
from utils.logging import logger

class PatternRefiner:
    """Analyzes and refines code patterns from Swift code"""
    
    def __init__(self):
        # Pattern detection rules
        self.framework_patterns = {
            'SwiftUI': r'import\s+SwiftUI',
            'RealityKit': r'import\s+RealityKit'
        }
        
        self.ui_patterns = {
            'View': r'struct\s+\w+:\s*View',
            'RealityView': r'RealityView\s*{[^}]*}',
            'Text': r'Text\s*\([^)]*\)'
        }
        
        self.entity_patterns = {
            'ModelEntity': r'ModelEntity\s*\([^)]*\)',
            'Entity': r'class\s+\w+:\s*Entity'
        }
        
        self.state_patterns = {
            '@State': r'@State\s+(?:private\s+)?var',
            '@ObservedObject': r'@ObservedObject\s+var',
            '@StateObject': r'@StateObject\s+var'
        }
        
        self.gesture_patterns = {
            'DragGesture': r'DragGesture\s*\(\s*\)',
            'TapGesture': r'TapGesture\s*\(\s*\)',
            'gesture': r'\.gesture\s*\([^)]*\)'
        }
        
        # Fix animation patterns
        self.animation_patterns = {
            'withAnimation': r'withAnimation\s*\([^)]*\)',
            'animation': r'\.animation\s*\([^)]*\)',
            'transition': r'\.transition\s*\([^)]*\)'
        }
        
        # Add lifecycle patterns
        self.lifecycle_patterns = {
            'onAppear': r'\.onAppear\s*{',
            'onDisappear': r'\.onDisappear\s*{',
            'task': r'\.task\s*{',
            'onChange': r'\.onChange\s*\([^)]*\)\s*{'
        }
        
        # Add spatial patterns
        self.spatial_patterns = {
            'position': r'\.position\s*\([^)]*\)',
            'scale': r'\.scale\s*\([^)]*\)',
            'rotation': r'\.rotation\s*\([^)]*\)',
            'transform': r'\.transform\s*\([^)]*\)'
        }
        
        # Add interaction patterns
        self.interaction_patterns = {
            'onTapGesture': r'\.onTapGesture\s*{',
            'onLongPressGesture': r'\.onLongPressGesture\s*{',
            'simultaneousGesture': r'\.simultaneousGesture\s*\([^)]*\)',
            'highPriorityGesture': r'\.highPriorityGesture\s*\([^)]*\)'
        }
        
        # Fix Reality Composer Pro patterns
        self.reality_composer_patterns = {
            'usdz_loading': r'try\s+await\s+Entity\.load\("[\w\-\.]+\.usdz"\)',
            'reality_file': r'\.reality\s*file\s*reference',
            'material_variants': r'materialVariants\s*=',
            'animation_controller': r'(AnimationController|availableAnimations)',
            'reality_composer_import': r'import\s+RealityComposer',
            'reality_composer_asset': r'\.realityComposerContent'
        }
        
        # Add Component System patterns
        self.component_patterns = {
            'component_definition': r'protocol\s+(\w+)Component\s*:\s*Component',
            'component_access': r'(\w+)\.components\[(\w+)Component\.self\]',
            'component_add': r'addComponent\((\w+)\)',
            'component_system': r'class\s+(\w+)System\s*:\s*System',
            'component_query': r'components\.query\(',
            'component_update': r'func\s+update\(context:\s*SceneUpdateContext\)'
        }
        
        # Add RealityKit System patterns
        self.realitykit_system_patterns = {
            # Scene Systems
            'scene_system': r'class\s+\w+:\s*SceneSystem',
            'scene_update': r'func\s+update\(context:\s*SceneUpdateContext\)',
            'scene_setup': r'func\s+setup\(scene:\s*RealityKit\.Scene\)',
            
            # Entity Systems
            'entity_system': r'class\s+\w+:\s*System',
            'entity_query': r'scene\.components\.query\(',
            'entity_subscription': r'scene\.subscribe\(',
            
            # Component Systems
            'component_system': r'class\s+\w+:\s*ComponentSystem',
            'component_update': r'func\s+update\(component:\s*\w+Component\)',
            'component_registration': r'scene\.registerSystem\(',
            
            # Event Systems
            'event_system': r'class\s+\w+:\s*EventSystem',
            'event_handling': r'func\s+handle\w+Event\(',
            'event_subscription': r'EventSubscription\{'
        }
        
        # Add Entity Action patterns
        self.entity_action_patterns = {
            # Transforms
            'transform_action': r'\.(move|rotate|scale)\(to:',
            'transform_animate': r'\.transform\.animate\(',
            'transform_sequence': r'\.transformSequence\(',
            
            # Physics
            'physics_action': r'\.(applyForce|applyTorque|setVelocity)\(',
            'physics_constraint': r'PhysicsConstraint\(',
            
            # Hierarchy
            'hierarchy_action': r'\.(addChild|removeFromParent|moveToParent)\(',
            'hierarchy_query': r'\.(findEntity|findEntities)\(',
            
            # Animation
            'animation_action': r'\.(playAnimation|resumeAnimation|pauseAnimation)\(',
            'animation_control': r'AnimationController\(',
            
            # Interaction
            'interaction_action': r'\.(enableInteraction|disableInteraction)\(',
            'gesture_action': r'\.(addGestureRecognizer|removeGestureRecognizer)\('
        }
        
        # Add View Attachment patterns
        self.view_attachment_patterns = {
            # Basic Attachments
            'view_attach': r'\.attachments\s*{[^}]*}',
            'view_entity': r'ViewAttachmentEntity\(',
            'view_geometry': r'\.attachmentGeometry\s*=',
            
            # Attachment Properties
            'attach_transform': r'\.transform\s*=\s*Transform\(',
            'attach_orientation': r'\.orientation\s*=',
            'attach_position': r'\.position\s*=',
            
            # SwiftUI Integration
            'reality_view': r'RealityView\s*{[^}]*}',
            'reality_view_content': r'\.content\s*{[^}]*}',
            'reality_view_update': r'\.update\s*{[^}]*}'
        }

    def detect_patterns(self, code: str) -> List[Pattern]:
        """Detect patterns in Swift code"""
        patterns: List[Pattern] = []
        
        # Dictionary mapping pattern types to their pattern dictionaries
        pattern_mappings = [
            (PatternType.FRAMEWORK, self.framework_patterns),
            (PatternType.UI, self.ui_patterns),
            (PatternType.ENTITY, self.entity_patterns),
            (PatternType.STATE, self.state_patterns),
            (PatternType.GESTURE, self.gesture_patterns),
            (PatternType.ANIMATION, self.animation_patterns),
            (PatternType.LIFECYCLE, self.lifecycle_patterns),
            (PatternType.SPATIAL, self.spatial_patterns),
            (PatternType.INTERACTION, self.interaction_patterns),
            (PatternType.REALITY_COMPOSER, self.reality_composer_patterns),
            (PatternType.COMPONENT, self.component_patterns),
            (PatternType.REALITYKIT_SYSTEM, self.realitykit_system_patterns),
            (PatternType.ENTITY_ACTION, self.entity_action_patterns),
            (PatternType.VIEW_ATTACHMENT, self.view_attachment_patterns)
        ]
        
        # Detect patterns for each type
        for pattern_type, pattern_dict in pattern_mappings:
            for name, pattern in pattern_dict.items():
                matches = re.finditer(pattern, code)
                for match in matches:
                    patterns.append(Pattern(
                        name=name,
                        type=pattern_type,
                        confidence=0.85,
                        line_number=code[:match.start()].count('\n') + 1
                    ))
                    # Only log at debug level for first occurrence of each pattern type
                    if not any(p.type == pattern_type for p in patterns[:-1]):
                        logger.debug(f"Found first {pattern_type.value} pattern: {name}")
        
        return patterns

    def analyze_relationships(self, patterns: List[Pattern]) -> List[PatternRelationship]:
        """Analyze relationships between detected patterns"""
        relationships: List[PatternRelationship] = []
        
        # Find framework relationships - Fix the framework relationship detection
        frameworks = [p for p in patterns if p.type == PatternType.FRAMEWORK]
        for i, f1 in enumerate(frameworks):
            for f2 in frameworks[i+1:]:
                # Only create relationship if both frameworks are present
                if f1.name == "SwiftUI" and f2.name == "RealityKit" or \
                   f1.name == "RealityKit" and f2.name == "SwiftUI":
                    relationships.append(PatternRelationship(
                        source=f1,
                        target=f2,
                        relationship_type="framework_integration",
                        confidence=0.9
                    ))
        
        # Find view hierarchy relationships
        views = [p for p in patterns if p.type == PatternType.UI]
        content_views = [v for v in views if v.name != "View"]  # Get actual view types
        view_protocol = next((v for v in views if v.name == "View"), None)
        
        if view_protocol:
            for view in content_views:
                relationships.append(PatternRelationship(
                    source=view,
                    target=view_protocol,
                    relationship_type="view_hierarchy",
                    confidence=0.85
                ))
        
        # Find state-gesture relationships
        states = [p for p in patterns if p.type == PatternType.STATE]
        gestures = [p for p in patterns if p.type == PatternType.GESTURE]
        
        for state in states:
            for gesture in gestures:
                # Create relationship if state is used in gesture handler
                relationships.append(PatternRelationship(
                    source=state,
                    target=gesture,
                    relationship_type="state_gesture_binding",
                    confidence=0.8
                ))
        
        # Log relationship detection results - only log summary at debug level
        if relationships:
            logger.debug(f"Found {len(relationships)} relationships between patterns")
        
        return relationships

    def validate_patterns(self, patterns: List[Pattern]) -> ValidationResult:
        """Validate detected patterns"""
        # Check framework requirements
        has_swiftui = any(p.name == "SwiftUI" and p.type == PatternType.FRAMEWORK for p in patterns)
        has_realitykit = any(p.name == "RealityKit" and p.type == PatternType.FRAMEWORK for p in patterns)
        
        # Check required patterns
        has_view = any(p.name == "View" and p.type == PatternType.UI for p in patterns)
        
        # Check relationships
        relationships = self.analyze_relationships(patterns)
        relationships_valid = len(relationships) > 0
        
        missing = []
        if not has_swiftui:
            missing.append("SwiftUI framework")
        if not has_view:
            missing.append("View protocol")
            
        return ValidationResult(
            framework_requirements_met=has_swiftui,
            has_required_patterns=has_view,
            relationships_valid=relationships_valid,
            missing_patterns=missing
        )