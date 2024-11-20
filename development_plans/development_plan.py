from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass
from patterns.visionos_patterns import VisionOSPattern

class AppType(str, Enum):
    """Types of VisionOS applications, based on Apple's sample projects"""
    IMMERSIVE = "immersive"  # Full immersive experiences like Botanist
    VOLUMETRIC = "volumetric"  # Apps focusing on 3D content
    MIXED_REALITY = "mixed_reality"  # Apps blending real and virtual
    WINDOW = "window"  # Traditional window-based apps
    SHARED_SPACE = "shared_space"  # Multi-user experiences

class FeatureRequirement(str, Enum):
    """Feature requirements based on Apple's samples"""
    HAND_TRACKING = "hand_tracking"
    SPATIAL_AUDIO = "spatial_audio"
    SCENE_UNDERSTANDING = "scene_understanding"
    MULTIPLAYER = "multiplayer"
    PERSISTENCE = "persistence"
    PHYSICS = "physics"
    VOLUMETRIC_CAPTURE = "volumetric_capture"
    SPATIAL_ANCHORS = "spatial_anchors"

@dataclass
class ImmersiveFeature:
    """Immersive feature configuration based on Botanist patterns"""
    name: str
    setup_code: str
    required_imports: List[str]
    configuration: Dict[str, str]
    best_practices: List[str]

class DevelopmentStage(BaseModel):
    """A stage in the development plan, enhanced with Botanist patterns"""
    name: str
    description: str
    patterns: List[VisionOSPattern]
    prerequisites: List[str]
    implementation_steps: List[str]
    validation_steps: List[str]
    common_issues: List[str]
    testing_requirements: List[str]
    botanist_reference: Optional[str] = None  # Reference to Botanist implementation
    performance_considerations: Optional[List[str]] = None

class DevelopmentPlan(BaseModel):
    """A complete development plan for a VisionOS application"""
    app_type: AppType
    features: List[FeatureRequirement]
    description: str
    architecture_overview: str
    required_capabilities: List[str]
    development_stages: List[DevelopmentStage]
    integration_points: Dict[str, List[str]]
    performance_considerations: List[str]
    testing_strategy: List[str]
    deployment_steps: List[str]
    immersive_features: Optional[List[ImmersiveFeature]] = None
    botanist_patterns: Optional[List[Dict]] = None

    def get_implementation_sequence(self) -> List[str]:
        """Get the complete sequence of implementation steps."""
        steps = []
        for stage in self.development_stages:
            steps.extend([f"{stage.name}: {step}" for step in stage.implementation_steps])
        return steps

    def get_required_patterns(self) -> List[VisionOSPattern]:
        """Get all patterns required for this development plan."""
        patterns = []
        for stage in self.development_stages:
            patterns.extend(stage.patterns)
        return list(set(patterns))

    def validate_requirements(self) -> List[str]:
        """Validate that all requirements are met."""
        issues = []
        
        # Check for required patterns
        patterns = self.get_required_patterns()
        if not patterns:
            issues.append("No patterns specified in development plan")
            
        # Check for implementation steps
        if not any(stage.implementation_steps for stage in self.development_stages):
            issues.append("No implementation steps specified")
            
        # Check for testing strategy
        if not self.testing_strategy:
            issues.append("No testing strategy specified")
            
        # Check for deployment steps
        if not self.deployment_steps:
            issues.append("No deployment steps specified")
            
        # Validate immersive features if present
        if self.app_type == AppType.IMMERSIVE and not self.immersive_features:
            issues.append("Immersive app type requires immersive_features")
            
        return issues

# Example development plan templates based on Botanist
IMMERSIVE_APP_TEMPLATE = DevelopmentPlan(
    app_type=AppType.IMMERSIVE,
    features=[
        FeatureRequirement.HAND_TRACKING,
        FeatureRequirement.SPATIAL_AUDIO,
        FeatureRequirement.SCENE_UNDERSTANDING
    ],
    description="Immersive VisionOS application with natural interactions",
    architecture_overview="""
    1. Main App Structure (from Botanist)
       - App entry point with WindowGroup
       - ImmersiveSpace for 3D content
       - RealityView for rendering
       - Entity system for 3D objects
       
    2. Component Organization
       - Separate view models for state
       - Modular view components
       - Shared utilities
       - Asset management
    """,
    required_capabilities=[
        "3D content rendering",
        "Hand tracking",
        "Spatial awareness",
        "Audio playback"
    ],
    development_stages=[
        DevelopmentStage(
            name="Project Setup",
            description="Initialize VisionOS project with required configurations",
            patterns=[],  # Add relevant patterns
            prerequisites=["Xcode 15+", "VisionOS SDK"],
            implementation_steps=[
                "1. Create new VisionOS project",
                "2. Configure basic app settings",
                "3. Set up project structure",
                "4. Add required frameworks"
            ],
            validation_steps=[
                "Verify project builds",
                "Check framework integration"
            ],
            common_issues=[
                "Missing SDK components",
                "Framework conflicts"
            ],
            testing_requirements=[
                "Basic build verification",
                "Framework availability checks"
            ],
            botanist_reference="Project structure follows Botanist sample",
            performance_considerations=[
                "Minimize framework overhead",
                "Optimize asset loading"
            ]
        ),
        # Add more stages...
    ],
    integration_points={
        "HandTracking": ["ImmersiveSpace", "RealityView"],
        "3DContent": ["RealityView", "EntitySystem"],
        "Audio": ["SpatialAudioEngine"]
    },
    performance_considerations=[
        "Optimize 3D asset loading",
        "Manage memory for large scenes",
        "Handle tracking efficiently",
        "Buffer audio properly"
    ],
    testing_strategy=[
        "Unit tests for core logic",
        "Integration tests for 3D rendering",
        "Performance testing",
        "User interaction testing"
    ],
    deployment_steps=[
        "1. Build for release",
        "2. Test on physical device",
        "3. Verify privacy permissions",
        "4. Submit to App Store"
    ],
    immersive_features=[
        ImmersiveFeature(
            name="3D Scene Setup",
            setup_code="""
            ImmersiveSpace {
                RealityView { content in
                    // Scene setup from Botanist
                }
            }
            """,
            required_imports=["RealityKit", "SwiftUI"],
            configuration={
                "lighting": "IBL with custom HDR",
                "physics": "Basic collision detection",
                "audio": "Spatial audio zones"
            },
            best_practices=[
                "Use async loading for models",
                "Implement proper scene cleanup",
                "Handle state transitions"
            ]
        )
    ],
    botanist_patterns=[
        {
            "pattern": "ImmersiveSpace Setup",
            "reference": "Botanist ImmersiveView.swift",
            "key_points": [
                "Scene organization",
                "Entity management",
                "State handling"
            ]
        }
    ]
)

# Add more templates for other app types...
