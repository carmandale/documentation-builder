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
            # Framework patterns
            (PatternType.SWIFTUI, r'import\s+SwiftUI'),
            (PatternType.REALITYKIT, r'import\s+RealityKit'),
            
            # UI patterns
            (PatternType.VIEW, r'struct\s+\w+:\s*View'),
            (PatternType.REALITY_VIEW, r'RealityView\s*{[^}]*}'),
            (PatternType.TEXT, r'Text\s*\([^)]*\)'),
            
            # Entity patterns
            (PatternType.MODEL_ENTITY, r'ModelEntity\s*\([^)]*\)'),
            (PatternType.ENTITY, r'class\s+\w+:\s*Entity'),
            
            # State patterns
            (PatternType.STATE, r'@State\s+(?:private\s+)?var'),
            (PatternType.OBSERVED_OBJECT, r'@ObservedObject\s+var'),
            (PatternType.STATE_OBJECT, r'@StateObject\s+var'),
            
            # Event System patterns
            (PatternType.EVENT_SUBSCRIPTION, r'EventSubscription|subscribe\s*\(\s*to:\s*\w+\.?\w*\.self'),
            (PatternType.EVENT_HANDLING, r'SceneEvents\.Update|handle\w+Event'),
            (PatternType.EVENT_SYSTEM, r'class\s+\w+:\s*EventSystem'),
            
            # Transform patterns
            (PatternType.TRANSFORM_ACTION, r'\.(move|rotate|scale)\(to:'),
            (PatternType.TRANSFORM_ANIMATE, r'\.transform\.animate'),
            (PatternType.TRANSFORM_SEQUENCE, r'\.transformSequence'),
            (PatternType.TRANSFORM, r'transform\s*=\s*Transform\(|\.transform\s*=|transform\.rotation'),
            
            # Spatial patterns
            (PatternType.POSITION, r'\.position\s*=|\(position:'),
            (PatternType.SCALE, r'\.scale\s*=|\(scale:'),
            (PatternType.ROTATION, r'\.rotation\s*=|\(rotation:|simd_quatf\(angle:'),
            
            # Gesture patterns
            (PatternType.DRAG_GESTURE, r'DragGesture\s*\(\s*\)'),
            (PatternType.TAP_GESTURE, r'TapGesture\s*\(\s*\)'),
            (PatternType.GESTURE, r'\.gesture\s*\([^)]*\)'),
            
            # Animation patterns
            (PatternType.WITH_ANIMATION, r'withAnimation\s*\([^)]*\)'),
            (PatternType.ANIMATION, r'\.animation\s*\([^)]*\)'),
            (PatternType.TRANSITION, r'\.transition\s*\([^)]*\)'),
            
            # Lifecycle patterns
            (PatternType.ON_APPEAR, r'\.onAppear\s*{'),
            (PatternType.ON_DISAPPEAR, r'\.onDisappear\s*{'),
            (PatternType.TASK, r'\.task\s*{'),
            (PatternType.ON_CHANGE, r'\.onChange\s*\([^)]*\)\s*{'),
            
            # Interaction patterns
            (PatternType.ON_TAP_GESTURE, r'\.onTapGesture\s*{'),
            (PatternType.ON_LONG_PRESS_GESTURE, r'\.onLongPressGesture\s*{'),
            (PatternType.SIMULTANEOUS_GESTURE, r'\.simultaneousGesture\s*\([^)]*\)'),
            (PatternType.HIGH_PRIORITY_GESTURE, r'\.highPriorityGesture\s*\([^)]*\)'),
            
            # Reality Composer Pro patterns
            (PatternType.USDZ_LOADING, r'try\s+await\s+Entity\.load\("[^"]+\.usdz"\)'),
            (PatternType.REALITY_FILE, r'\.reality\s*file\s*reference'),
            (PatternType.MATERIAL_VARIANTS, r'materialVariants\s*='),
            (PatternType.ANIMATION_CONTROLLER, r'(AnimationController|availableAnimations)'),
            (PatternType.REALITY_COMPOSER_IMPORT, r'import\s+RealityComposer'),
            (PatternType.REALITY_COMPOSER_ASSET, r'\.realityComposerContent'),
            
            # Component System patterns
            (PatternType.COMPONENT_DEFINITION, r'protocol\s+(\w+)Component\s*:\s*Component'),
            (PatternType.COMPONENT_ACCESS, r'(\w+)\.components\[(\w+)Component\.self\]'),
            (PatternType.COMPONENT_ADD, r'addComponent\((\w+)\)'),
            (PatternType.COMPONENT_SYSTEM, r'class\s+(\w+)System\s*:\s*System'),
            (PatternType.COMPONENT_QUERY, r'components\.query\('),
            (PatternType.COMPONENT_UPDATE, r'func\s+update\(context:\s*SceneUpdateContext\)'),
            
            # RealityKit System patterns
            (PatternType.SCENE_SYSTEM, r'class\s+\w+:\s*SceneSystem'),
            (PatternType.SCENE_UPDATE, r'func\s+update\(context:\s*SceneUpdateContext\)'),
            (PatternType.SCENE_SETUP, r'func\s+setup\(scene:\s*RealityKit\.Scene\)'),
            (PatternType.ENTITY_SYSTEM, r'class\s+\w+:\s*System'),
            (PatternType.ENTITY_QUERY, r'scene\.components\.query\('),
            (PatternType.ENTITY_SUBSCRIPTION, r'scene\.subscribe\('),
            (PatternType.COMPONENT_REGISTRATION, r'scene\.registerSystem\('),
            
            # Entity Action patterns
            (PatternType.PHYSICS_ACTION, r'\.(applyForce|applyTorque|setVelocity)\('),
            (PatternType.PHYSICS_CONSTRAINT, r'PhysicsConstraint\('),
            (PatternType.HIERARCHY_ACTION, r'\.(addChild|removeFromParent|moveToParent)\('),
            (PatternType.HIERARCHY_QUERY, r'\.(findEntity|findEntities)\('),
            (PatternType.ANIMATION_ACTION, r'\.(playAnimation|resumeAnimation|pauseAnimation)\('),
            (PatternType.ANIMATION_CONTROL, r'AnimationController\('),
            (PatternType.INTERACTION_ACTION, r'\.(enableInteraction|disableInteraction)\('),
            (PatternType.GESTURE_ACTION, r'\.(addGestureRecognizer|removeGestureRecognizer)\('),
            
            # View Attachment patterns
            (PatternType.VIEW_ATTACH, r'\.attachments\s*{[^}]*}'),
            (PatternType.VIEW_ENTITY, r'ViewAttachmentEntity\('),
            (PatternType.VIEW_GEOMETRY, r'\.attachmentGeometry\s*='),
            (PatternType.ATTACH_TRANSFORM, r'\.transform\s*=\s*Transform3D\('),
            (PatternType.ATTACH_ORIENTATION, r'\.orientation\s*='),
            (PatternType.ATTACH_POSITION, r'\.position\s*='),
            (PatternType.REALITY_VIEW_CONTENT, r'\.content\s*='),
            (PatternType.REALITY_VIEW_UPDATE, r'\.update\s*{')
        ]
        
        # Detect patterns for each type
        for pattern_type, pattern_regex in pattern_mappings:
            matches = re.finditer(pattern_regex, code)
            for match in matches:
                start, end = match.span()
                patterns.append(Pattern(
                    name=pattern_type.value,
                    type=pattern_type,
                    confidence=0.85,
                    line_number=code[:start].count('\n') + 1,
                    start=start,
                    end=end
                ))
                # Only log at debug level for first occurrence of each pattern type
                if not any(p.type == pattern_type for p in patterns[:-1]):
                    logger.debug(f"Found first {pattern_type.value} pattern")
        
        return patterns

    def analyze_relationships(self, patterns: List[Pattern]) -> List[PatternRelationship]:
        """Analyze relationships between detected patterns"""
        relationships: List[PatternRelationship] = []
        
        # Group patterns by category
        framework_patterns = [p for p in patterns if p.type in (PatternType.SWIFTUI, PatternType.REALITYKIT)]
        ui_patterns = [p for p in patterns if p.type in (PatternType.VIEW, PatternType.REALITY_VIEW, PatternType.TEXT)]
        entity_patterns = [p for p in patterns if p.type in (PatternType.MODEL_ENTITY, PatternType.ENTITY)]
        state_patterns = [p for p in patterns if p.type in (PatternType.STATE, PatternType.OBSERVED_OBJECT, PatternType.STATE_OBJECT)]
        gesture_patterns = [p for p in patterns if p.type in (PatternType.DRAG_GESTURE, PatternType.TAP_GESTURE, PatternType.GESTURE)]
        animation_patterns = [p for p in patterns if p.type in (PatternType.WITH_ANIMATION, PatternType.ANIMATION, PatternType.TRANSITION)]
        lifecycle_patterns = [p for p in patterns if p.type in (PatternType.ON_APPEAR, PatternType.ON_DISAPPEAR, PatternType.TASK, PatternType.ON_CHANGE)]
        spatial_patterns = [p for p in patterns if p.type in (PatternType.POSITION, PatternType.SCALE, PatternType.ROTATION, PatternType.TRANSFORM)]
        interaction_patterns = [p for p in patterns if p.type in (PatternType.ON_TAP_GESTURE, PatternType.ON_LONG_PRESS_GESTURE, PatternType.SIMULTANEOUS_GESTURE, PatternType.HIGH_PRIORITY_GESTURE)]
        reality_composer_patterns = [p for p in patterns if p.type in (PatternType.USDZ_LOADING, PatternType.REALITY_FILE, PatternType.MATERIAL_VARIANTS, PatternType.ANIMATION_CONTROLLER, PatternType.REALITY_COMPOSER_IMPORT, PatternType.REALITY_COMPOSER_ASSET)]
        component_patterns = [p for p in patterns if p.type in (PatternType.COMPONENT_DEFINITION, PatternType.COMPONENT_ACCESS, PatternType.COMPONENT_ADD, PatternType.COMPONENT_SYSTEM, PatternType.COMPONENT_QUERY, PatternType.COMPONENT_UPDATE)]
        system_patterns = [p for p in patterns if p.type in (PatternType.SCENE_SYSTEM, PatternType.SCENE_UPDATE, PatternType.SCENE_SETUP, PatternType.ENTITY_SYSTEM, PatternType.ENTITY_QUERY, PatternType.ENTITY_SUBSCRIPTION, PatternType.COMPONENT_REGISTRATION, PatternType.EVENT_SYSTEM, PatternType.EVENT_HANDLING, PatternType.EVENT_SUBSCRIPTION)]
        action_patterns = [p for p in patterns if p.type in (PatternType.TRANSFORM_ACTION, PatternType.TRANSFORM_ANIMATE, PatternType.TRANSFORM_SEQUENCE, PatternType.PHYSICS_ACTION, PatternType.PHYSICS_CONSTRAINT, PatternType.HIERARCHY_ACTION, PatternType.HIERARCHY_QUERY, PatternType.ANIMATION_ACTION, PatternType.ANIMATION_CONTROL, PatternType.INTERACTION_ACTION, PatternType.GESTURE_ACTION)]
        attachment_patterns = [p for p in patterns if p.type in (PatternType.VIEW_ATTACH, PatternType.VIEW_ENTITY, PatternType.VIEW_GEOMETRY, PatternType.ATTACH_TRANSFORM, PatternType.ATTACH_ORIENTATION, PatternType.ATTACH_POSITION, PatternType.REALITY_VIEW_CONTENT, PatternType.REALITY_VIEW_UPDATE)]

        # Analyze framework relationships
        if framework_patterns:
            swiftui = next((p for p in framework_patterns if p.type == PatternType.SWIFTUI), None)
            realitykit = next((p for p in framework_patterns if p.type == PatternType.REALITYKIT), None)
            if swiftui and realitykit:
                relationships.append(PatternRelationship(
                    source=swiftui,
                    target=realitykit,
                    relationship_type="framework_integration",
                    confidence=0.9
                ))

        # Analyze UI and Entity relationships
        for ui_pattern in ui_patterns:
            # UI to Entity relationships
            for entity_pattern in entity_patterns:
                relationships.append(PatternRelationship(
                    source=ui_pattern,
                    target=entity_pattern,
                    relationship_type="view_entity_binding",
                    confidence=0.85
                ))
            
            # UI to State relationships
            for state_pattern in state_patterns:
                relationships.append(PatternRelationship(
                    source=ui_pattern,
                    target=state_pattern,
                    relationship_type="view_state_binding",
                    confidence=0.85
                ))

        # Analyze Gesture and Interaction relationships
        for gesture_pattern in gesture_patterns:
            # Gesture to State relationships
            for state_pattern in state_patterns:
                relationships.append(PatternRelationship(
                    source=gesture_pattern,
                    target=state_pattern,
                    relationship_type="gesture_state_binding",
                    confidence=0.8
                ))
            
            # Gesture to Animation relationships
            for animation_pattern in animation_patterns:
                relationships.append(PatternRelationship(
                    source=gesture_pattern,
                    target=animation_pattern,
                    relationship_type="gesture_animation_binding",
                    confidence=0.8
                ))

        # Analyze System and Component relationships
        for system_pattern in system_patterns:
            # System to Component relationships
            for component_pattern in component_patterns:
                relationships.append(PatternRelationship(
                    source=system_pattern,
                    target=component_pattern,
                    relationship_type="system_component_binding",
                    confidence=0.9
                ))
            
            # System to Entity relationships
            for entity_pattern in entity_patterns:
                relationships.append(PatternRelationship(
                    source=system_pattern,
                    target=entity_pattern,
                    relationship_type="system_entity_binding",
                    confidence=0.9
                ))

        # Analyze Action and Entity relationships
        for action_pattern in action_patterns:
            # Action to Entity relationships
            for entity_pattern in entity_patterns:
                relationships.append(PatternRelationship(
                    source=action_pattern,
                    target=entity_pattern,
                    relationship_type="action_entity_binding",
                    confidence=0.85
                ))
            
            # Action to Animation relationships
            for animation_pattern in animation_patterns:
                relationships.append(PatternRelationship(
                    source=action_pattern,
                    target=animation_pattern,
                    relationship_type="action_animation_binding",
                    confidence=0.8
                ))

        # Analyze View Attachment relationships
        for attachment_pattern in attachment_patterns:
            # Attachment to Entity relationships
            for entity_pattern in entity_patterns:
                relationships.append(PatternRelationship(
                    source=attachment_pattern,
                    target=entity_pattern,
                    relationship_type="attachment_entity_binding",
                    confidence=0.9
                ))
            
            # Attachment to Spatial relationships
            for spatial_pattern in spatial_patterns:
                relationships.append(PatternRelationship(
                    source=attachment_pattern,
                    target=spatial_pattern,
                    relationship_type="attachment_spatial_binding",
                    confidence=0.85
                ))

        # Log relationship detection results
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