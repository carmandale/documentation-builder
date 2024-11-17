"""VisionOS-specific pattern definitions for the documentation analyzer"""

from typing import Dict, Set
import re

def get_visionos_patterns(content: str) -> Dict[str, Set[str]]:
    """Get VisionOS-specific patterns from content
    
    Args:
        content: Content to analyze
        
    Returns:
        Dictionary of pattern categories and their matches
    """
    return {
        # Volumetric Window Features
        'volumetric': set(re.findall(r'(?:VolumetricWindow|volumetricSystemBackground|volumetricWindowStyle)\b', content)),
        'window_groups': set(re.findall(r'(?:WindowGroup|ImmersiveSpace|WindowStyle|WindowAnchor)\b', content)),
        
        # Spatial UI
        'spatial_ui': set(re.findall(r'(?:SpatialHoverEffect|spatialHoverRadius|SpatialTapGesture|SpatialPinchGesture)\b', content)),
        'ornaments': set(re.findall(r'(?:windowOrnament|ornamentAlignment|ornamentPosition|OrnamentAttachment)\b', content)),
        
        # Immersive Spaces
        'immersive': set(re.findall(r'(?:ImmersiveSpace|ImmersionStyle|FullImmersion|MixedImmersion|ProgressiveImmersion)\b', content)),
        'immersive_gestures': set(re.findall(r'(?:SpatialGesture|HandGesture|EyeGesture|HeadGesture|BodyGesture)\b', content)),
        
        # Shared Spaces
        'shared': set(re.findall(r'(?:SharedSpace|GroupSession|SharedStorage|CollaborationSession)\b', content)),
        'presence': set(re.findall(r'(?:Presence|PersonAnchor|SharedAnchor|AnchorOwnership)\b', content)),
        
        # Dynamic Scenes
        'scene_understanding': set(re.findall(r'(?:SceneUnderstanding|PlaneDetection|MeshAnchor|SceneReconstruction)\b', content)),
        'scene_anchors': set(re.findall(r'(?:WorldAnchor|TrackedAnchor|ProjectedAnchor|AttachmentAnchor)\b', content)),
        
        # Mixed Reality Features
        'passthrough': set(re.findall(r'(?:Passthrough|HandTracking|EyeTracking|RoomPlan|SpatialMapping)\b', content)),
        'reality_effects': set(re.findall(r'(?:RealityEffect|VisualEffect|MaterialEffect|LightingEffect|EnvironmentEffect)\b', content))
    }

def get_realitykit_patterns(content: str) -> Dict[str, Set[str]]:
    """Get RealityKit-specific patterns from content
    
    Args:
        content: Content to analyze
        
    Returns:
        Dictionary of pattern categories and their matches
    """
    return {
        # Scene Systems
        'scene_system': set(re.findall(r'class\s+\w+:\s*SceneSystem', content)),
        'scene_update': set(re.findall(r'func\s+update\(context:\s*SceneUpdateContext\)', content)),
        'scene_setup': set(re.findall(r'func\s+setup\(scene:\s*RealityKit\.Scene\)', content)),
        
        # Entity Systems
        'entity_system': set(re.findall(r'class\s+\w+:\s*System', content)),
        'entity_query': set(re.findall(r'scene\.components\.query\(', content)),
        'entity_subscription': set(re.findall(r'scene\.subscribe\(', content)),
        
        # Component Systems
        'component_system': set(re.findall(r'class\s+\w+:\s*ComponentSystem', content)),
        'component_update': set(re.findall(r'func\s+update\(component:\s*\w+Component\)', content)),
        'component_registration': set(re.findall(r'scene\.registerSystem\(', content)),
        
        # Event Systems
        'event_system': set(re.findall(r'class\s+\w+:\s*EventSystem', content)),
        'event_handling': set(re.findall(r'func\s+handle\w+Event\(', content)),
        'event_subscription': set(re.findall(r'EventSubscription\{', content))
    }

def get_reality_composer_patterns(content: str) -> Dict[str, Set[str]]:
    """Get Reality Composer Pro specific patterns from content
    
    Args:
        content: Content to analyze
        
    Returns:
        Dictionary of pattern categories and their matches
    """
    return {
        # Behaviors and Timelines
        'behaviors': set(re.findall(r'(?:Behavior|BehaviorComponent|BehaviorValue|InputTarget|BehaviorSystem|BehaviorDefinition|BehaviorEvents)\b', content)),
        'timelines': set(re.findall(r'(?:Timeline|AnimationTimeline|TimelineAnimation|PlaybackController|TimelineAsset|TimelineDefinition|TimelineEvents)\b', content)),
        
        # Materials and Shaders
        'shader_graph': set(re.findall(r'(?:ShaderGraphMaterial|CustomMaterial|MaterialParameters|ShaderFunction|MaterialPropertyBlock|ShaderDefinition|ShaderEvents)\b', content)),
        'material_properties': set(re.findall(r'\.material\s*=|\.materials\s*=|\.customMaterial\s*=|\.shaderGraph\s*=|\.materialDefinition\s*=', content)),
        
        # Assets and Resources
        'assets': set(re.findall(r'\.usda\b|\.usdz\b|\.rcproject\b|\.reality\b|\.materialx\b|\.shadergraph\b|\.behavior\b|\.timeline\b', content)),
        'custom_systems': set(re.findall(r'(?:SystemComponent|SystemRegistry|ComponentSystem|UpdateSystem|SystemTraits|SystemDefinition|SystemEvents)\b', content))
    }
