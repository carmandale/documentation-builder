from typing import List, Optional, Set, Dict
from pydantic import BaseModel, Field
from models.base import Pattern, PatternType, PatternContext, ValidationResult

class VisionOSPatternType(PatternType):
    """VisionOS-specific pattern types"""
    IMMERSIVE_SPACE = "immersive_space"
    HAND_TRACKING = "hand_tracking"
    VOLUMETRIC = "volumetric"
    SHARED_SPACE = "shared_space"
    REALITY_VIEW = "reality_view"
    ENTITY_ANCHOR = "entity_anchor"

class VisionOSPattern(Pattern):
    """VisionOS-specific pattern implementation optimized for LLM consumption"""
    type: VisionOSPatternType
    required_imports: Set[str] = Field(default_factory=set)
    required_permissions: Set[str] = Field(default_factory=set)
    implementation_steps: List[str] = Field(...) 
    prerequisites: List[str] = Field(...) 
    best_practices: List[str] = Field(...) 
    common_pitfalls: List[str] = Field(...) 
    related_patterns: Set[str] = Field(default_factory=set)
    code_template: str = Field(...) 
    validation_rules: List[str] = Field(...) 
    usage_examples: List[str] = Field(...) 
    component_interactions: Dict[str, str] = Field(...) 
    
    class Config:
        use_enum_values = True
    
    @property
    def is_complete(self) -> bool:
        """Verify that the pattern follows all documentation rules."""
        return all([
            len(self.implementation_steps) > 0,
            len(self.prerequisites) > 0,
            len(self.best_practices) > 0,
            len(self.common_pitfalls) > 0,
            len(self.code_template.strip()) > 0,
            len(self.validation_rules) > 0,
            len(self.usage_examples) > 0,
            len(self.component_interactions) > 0,
            # Verify implementation steps are numbered
            all(step.startswith(f"{i+1}. ") for i, step in enumerate(self.implementation_steps)),
            # Verify code template has necessary sections
            "MARK: -" in self.code_template,
            "import" in self.code_template.lower() or len(self.required_imports) > 0,
        ])
    
    def validate(self) -> ValidationResult:
        """Validate that the pattern meets all requirements."""
        issues = []
        if not self.implementation_steps:
            issues.append("Missing implementation steps")
        if not self.prerequisites:
            issues.append("Missing prerequisites")
        if not self.best_practices:
            issues.append("Missing best practices")
        if not self.common_pitfalls:
            issues.append("Missing common pitfalls")
        if not self.code_template.strip():
            issues.append("Missing code template")
        if not self.validation_rules:
            issues.append("Missing validation rules")
        if not self.usage_examples:
            issues.append("Missing usage examples")
        if not self.component_interactions:
            issues.append("Missing component interactions")
            
        # Check implementation steps are properly numbered
        for i, step in enumerate(self.implementation_steps):
            if not step.startswith(f"{i+1}. "):
                issues.append(f"Implementation step {i+1} is not properly numbered")
                
        # Check code template includes necessary sections
        if "MARK: -" not in self.code_template:
            issues.append("Code template missing MARK comments")
        if "import" not in self.code_template.lower() and not self.required_imports:
            issues.append("No imports specified in code template or required_imports")
            
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues
        )

# Pattern Definitions
IMMERSIVE_SPACE_PATTERNS = {
    "basic_immersive_space": VisionOSPattern(
        name="Basic Immersive Space",
        type=VisionOSPatternType.IMMERSIVE_SPACE,
        description="Basic immersive space setup with step-by-step implementation guide",
        implementation_steps=[
            "1. Create a new SwiftUI View conforming to View protocol",
            "2. Add ImmersiveSpace scene type modifier",
            "3. Setup RealityView for 3D content",
            "4. Configure space persistence and tracking",
            "5. Handle space activation/deactivation lifecycle"
        ],
        prerequisites=[
            "Basic SwiftUI knowledge",
            "Understanding of 3D coordinate spaces",
            "RealityKit fundamentals"
        ],
        code_template="""
// MARK: - Immersive Space Implementation
struct ImmersiveSpaceView: View {
    // MARK: - Properties
    @State private var isSpaceActive = false
    
    // MARK: - Body
    var body: some View {
        RealityView { content in
            // Add your 3D content here
            // Example: content.add(anchorEntity)
        }
        .gesture(/* Add interaction gestures */)
    }
    
    // MARK: - Space Lifecycle
    private func activateSpace() {
        // Handle space activation
    }
}
""",
        validation_rules=[
            "Must include proper space lifecycle handling",
            "Should handle memory management for 3D content",
            "Must request appropriate system permissions"
        ],
        usage_examples=[
            "Interactive 3D visualization",
            "Shared multiplayer space",
            "Volumetric content display"
        ],
        component_interactions={
            "HandTracking": "Optional: Add hand tracking for interaction",
            "SharedSpace": "Optional: Enable multiplayer capabilities",
            "EntityAnchoring": "Required: For placing 3D content"
        },
        best_practices=["Use proper coordinate space"],
        required_imports={"SwiftUI", "RealityKit"},
        required_permissions={"immersiveSpace"},
        common_pitfalls=["Not handling space transitions", "Memory leaks"]
    ),
    "shared_space": VisionOSPattern(
        name="Shared Space Experience",
        type=VisionOSPatternType.SHARED_SPACE,
        description="Implementation of a shared immersive space for multiple users",
        implementation_steps=[
            "1. Create a new SwiftUI View conforming to View protocol",
            "2. Add SharedSpace scene type modifier",
            "3. Setup RealityView for 3D content",
            "4. Configure space persistence and tracking",
            "5. Handle space activation/deactivation lifecycle",
            "6. Implement multiplayer capabilities using MultipeerConnectivity"
        ],
        prerequisites=[
            "Basic SwiftUI knowledge",
            "Understanding of 3D coordinate spaces",
            "RealityKit fundamentals",
            "MultipeerConnectivity basics"
        ],
        code_template='''
class SharedSpaceSession: ObservableObject {
    @Published var isHosting = false
    @Published var connectedPeers: [MCPeerID] = []
    
    private let session: MCSession
    
    init() {
        // Initialize shared session
    }
}

struct SharedSpaceView: View {
    @StateObject private var session = SharedSpaceSession()
    
    var body: some View {
        RealityView { content in
            // Setup shared space content
        }
        .task {
            // Start hosting or join session
        }
    }
}
''',
        validation_rules=[
            "Must include proper space lifecycle handling",
            "Should handle memory management for 3D content",
            "Must request appropriate system permissions",
            "Must implement multiplayer capabilities correctly"
        ],
        usage_examples=[
            "Interactive 3D visualization",
            "Shared multiplayer space",
            "Volumetric content display"
        ],
        component_interactions={
            "HandTracking": "Optional: Add hand tracking for interaction",
            "EntityAnchoring": "Required: For placing 3D content",
            "MultipeerConnectivity": "Required: For multiplayer capabilities"
        },
        best_practices=[
            "Implement proper session management",
            "Handle peer disconnections gracefully",
            "Sync state efficiently between peers"
        ],
        common_pitfalls=[
            "Not handling network latency",
            "Assuming all peers have same capabilities",
            "Not implementing proper error recovery"
        ],
        related_patterns={"basic_immersive_space", "state_sync"},
        required_imports={"SwiftUI", "RealityKit", "MultipeerConnectivity"},
        required_permissions={"immersiveSpace", "nearbyInteraction"}
    )
}

HAND_TRACKING_PATTERNS = {
    "basic_hand_tracking": VisionOSPattern(
        name="Basic Hand Tracking",
        type=VisionOSPatternType.HAND_TRACKING,
        description="Basic hand tracking implementation with step-by-step guide",
        implementation_steps=[
            "1. Create a new SwiftUI View conforming to View protocol",
            "2. Add HandTracking scene type modifier",
            "3. Setup RealityView for 3D content",
            "4. Configure hand tracking settings",
            "5. Handle hand tracking events"
        ],
        prerequisites=[
            "Basic SwiftUI knowledge",
            "Understanding of 3D coordinate spaces",
            "RealityKit fundamentals"
        ],
        code_template='''
struct HandTrackingView: View {
    @State private var handPosition: SIMD3<Float>?
    
    var body: some View {
        RealityView { content in
            let handTrackingSystem = content.handTrackingSystem
            handTrackingSystem?.isEnabled = true
        }
        .handTracking(.continuous) { hand in
            handPosition = hand.position
        }
        .privacyInfo("Hand tracking is used for interaction")
    }
}
''',
        validation_rules=[
            "Must include proper hand tracking settings",
            "Should handle hand tracking events correctly",
            "Must request appropriate system permissions"
        ],
        usage_examples=[
            "Interactive 3D visualization",
            "Hand-based interaction",
            "Volumetric content display"
        ],
        component_interactions={
            "EntityAnchoring": "Required: For placing 3D content",
            "RealityView": "Required: For 3D content display"
        },
        best_practices=[
            "Always provide privacy information",
            "Handle tracking state changes",
            "Implement fallback interactions"
        ],
        common_pitfalls=[
            "Not handling tracking loss",
            "Ignoring privacy considerations",
            "Over-relying on precise tracking"
        ],
        related_patterns={"basic_immersive_space", "gesture_recognition", "interaction_feedback"},
        required_imports={"SwiftUI", "RealityKit", "ARKit"},
        required_permissions={"handTracking"}
    ),
    "basic_hand_tracking": VisionOSPattern(
        name="Basic Hand Tracking",
        type=VisionOSPatternType.HAND_TRACKING,
        description="Basic implementation of hand tracking with gesture recognition",
        implementation_steps=[
            "1. Create a new SwiftUI View conforming to View protocol",
            "2. Add HandTracking scene type modifier",
            "3. Setup RealityView for 3D content",
            "4. Configure hand tracking settings",
            "5. Handle hand tracking events",
            "6. Implement gesture recognition"
        ],
        prerequisites=[
            "Basic SwiftUI knowledge",
            "Understanding of 3D coordinate spaces",
            "RealityKit fundamentals",
            "Gesture recognition basics"
        ],
        code_template='''
struct HandTrackingView: View {
    @State private var handPosition: SIMD3<Float>?
    
    var body: some View {
        RealityView { content in
            let handTrackingSystem = content.handTrackingSystem
            handTrackingSystem?.isEnabled = true
        }
        .handTracking(.continuous) { hand in
            handPosition = hand.position
        }
        .gesture(/* Add gesture recognition */)
        .privacyInfo("Hand tracking is used for interaction")
    }
}
''',
        validation_rules=[
            "Must include proper hand tracking settings",
            "Should handle hand tracking events correctly",
            "Must implement gesture recognition correctly",
            "Must request appropriate system permissions"
        ],
        usage_examples=[
            "Interactive 3D visualization",
            "Hand-based interaction",
            "Volumetric content display"
        ],
        component_interactions={
            "EntityAnchoring": "Required: For placing 3D content",
            "RealityView": "Required: For 3D content display",
            "GestureRecognition": "Required: For gesture-based interaction"
        },
        best_practices=[
            "Always provide privacy information",
            "Handle tracking state changes",
            "Implement fallback interactions"
        ],
        common_pitfalls=[
            "Not handling tracking loss",
            "Ignoring privacy considerations",
            "Over-relying on precise tracking"
        ],
        related_patterns={"basic_immersive_space", "gesture_recognition", "interaction_feedback"},
        required_imports={"SwiftUI", "RealityKit", "ARKit"},
        required_permissions={"handTracking"}
    )
}

VOLUMETRIC_PATTERNS = {
    "basic_volumetric": VisionOSPattern(
        name="Basic Volumetric",
        type=VisionOSPatternType.VOLUMETRIC,
        description="Basic volumetric content setup with step-by-step guide",
        implementation_steps=[
            "1. Create a new SwiftUI View conforming to View protocol",
            "2. Add Volumetric scene type modifier",
            "3. Setup RealityView for 3D content",
            "4. Configure volumetric settings",
            "5. Handle volumetric events"
        ],
        prerequisites=[
            "Basic SwiftUI knowledge",
            "Understanding of 3D coordinate spaces",
            "RealityKit fundamentals"
        ],
        code_template='''
struct VolumetricView: View {
    var body: some View {
        RealityView { content in
            var material = VolumetricMaterial()
            material.scattering = .init(0.2)
            material.absorption = .init(0.1)
            
            let mesh = MeshResource.generateBox(size: 0.2)
            let entity = ModelEntity(mesh: mesh, materials: [material])
            content.add(entity)
        }
        .volumetric(true)
    }
}
''',
        validation_rules=[
            "Must include proper volumetric settings",
            "Should handle volumetric events correctly",
            "Must request appropriate system permissions"
        ],
        usage_examples=[
            "Interactive 3D visualization",
            "Volumetric content display",
            "Mixed reality experiences"
        ],
        component_interactions={
            "EntityAnchoring": "Required: For placing 3D content",
            "RealityView": "Required: For 3D content display"
        },
        best_practices=[
            "Optimize material properties for performance",
            "Use appropriate mesh sizes",
            "Consider viewing angles"
        ],
        common_pitfalls=[
            "Overusing volumetric effects",
            "Not considering performance impact",
            "Incorrect material properties"
        ],
        related_patterns={"material_effects", "lighting"},
        required_imports={"SwiftUI", "RealityKit"},
        required_permissions=set()
    ),
    "basic_volumetric_content": VisionOSPattern(
        name="Basic Volumetric Content",
        type=VisionOSPatternType.VOLUMETRIC,
        description="Implementation of basic volumetric content with material properties",
        implementation_steps=[
            "1. Create a new SwiftUI View conforming to View protocol",
            "2. Add Volumetric scene type modifier",
            "3. Setup RealityView for 3D content",
            "4. Configure volumetric settings",
            "5. Handle volumetric events",
            "6. Implement material properties"
        ],
        prerequisites=[
            "Basic SwiftUI knowledge",
            "Understanding of 3D coordinate spaces",
            "RealityKit fundamentals",
            "Material properties basics"
        ],
        code_template='''
struct VolumetricView: View {
    var body: some View {
        RealityView { content in
            var material = VolumetricMaterial()
            material.scattering = .init(0.2)
            material.absorption = .init(0.1)
            
            let mesh = MeshResource.generateBox(size: 0.2)
            let entity = ModelEntity(mesh: mesh, materials: [material])
            content.add(entity)
        }
        .volumetric(true)
    }
}
''',
        validation_rules=[
            "Must include proper volumetric settings",
            "Should handle volumetric events correctly",
            "Must implement material properties correctly",
            "Must request appropriate system permissions"
        ],
        usage_examples=[
            "Interactive 3D visualization",
            "Volumetric content display",
            "Mixed reality experiences"
        ],
        component_interactions={
            "EntityAnchoring": "Required: For placing 3D content",
            "RealityView": "Required: For 3D content display",
            "MaterialProperties": "Required: For volumetric content display"
        },
        best_practices=[
            "Optimize material properties for performance",
            "Use appropriate mesh sizes",
            "Consider viewing angles"
        ],
        common_pitfalls=[
            "Overusing volumetric effects",
            "Not considering performance impact",
            "Incorrect material properties"
        ],
        related_patterns={"material_effects", "lighting"},
        required_imports={"SwiftUI", "RealityKit"},
        required_permissions=set()
    )
}

def get_pattern(pattern_name: str) -> Optional[VisionOSPattern]:
    """Get a specific pattern by name."""
    all_patterns = {
        **IMMERSIVE_SPACE_PATTERNS,
        **HAND_TRACKING_PATTERNS,
        **VOLUMETRIC_PATTERNS
    }
    return all_patterns.get(pattern_name)

def get_patterns_by_type(pattern_type: VisionOSPatternType) -> List[VisionOSPattern]:
    """Get all patterns of a specific type."""
    all_patterns = {
        **IMMERSIVE_SPACE_PATTERNS,
        **HAND_TRACKING_PATTERNS,
        **VOLUMETRIC_PATTERNS
    }
    return [p for p in all_patterns.values() if p.type == pattern_type]

def get_related_patterns(pattern_name: str) -> List[VisionOSPattern]:
    """Get all patterns related to a specific pattern."""
    pattern = get_pattern(pattern_name)
    if not pattern:
        return []
    
    related = []
    for name in pattern.related_patterns:
        if related_pattern := get_pattern(name):
            related.append(related_pattern)
    
    # Also find patterns that reference this one
    all_patterns = {
        **IMMERSIVE_SPACE_PATTERNS,
        **HAND_TRACKING_PATTERNS,
        **VOLUMETRIC_PATTERNS
    }
    
    for other in all_patterns.values():
        if pattern_name in other.related_patterns:
            related.append(other)
    
    return related

def validate_pattern(pattern: VisionOSPattern) -> ValidationResult:
    """Validate a pattern's relationships and requirements."""
    result = ValidationResult(
        framework_requirements_met=True,
        has_required_patterns=True,
        relationships_valid=True
    )
    
    # Validate related patterns exist
    for related_name in pattern.related_patterns:
        if not get_pattern(related_name):
            result.missing_patterns.append(related_name)
            result.has_required_patterns = False
    
    # Validate framework requirements
    if not pattern.required_imports:
        result.validation_messages.append("No framework requirements specified")
    
    # Validate relationships are bidirectional
    for related_name in pattern.related_patterns:
        related = get_pattern(related_name)
        if related and pattern.name not in related.related_patterns:
            result.invalid_relationships.append(
                f"Non-bidirectional relationship: {pattern.name} -> {related_name}"
            )
            result.relationships_valid = False
    
    return result
