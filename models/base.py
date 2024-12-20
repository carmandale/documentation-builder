from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class Topic(BaseModel):
    """Represents a section/topic in the documentation"""
    title: str
    level: int  # h1, h2, h3 etc.
    content: Optional[str] = None
    path: List[str] = Field(default_factory=list)  # Breadcrumb path to this topic

class CodeBlock(BaseModel):
    """Represents a code example from documentation"""
    code: str
    description: Optional[str] = None
    language: str = "swift"  # Default to Swift for visionOS
    preview: str = Field(..., description="First 200 chars of code for quick reference")
    frameworks: List[str] = Field(default_factory=list)
    type: str = Field(
        default="other",
        description="Type of code example: ui_component, 3d_content, animation, app_structure, event_handling, immersive_space, other"
    )

class CodePattern(BaseModel):
    """Represents a reusable code pattern"""
    pattern_type: str = Field(..., description="Type of pattern (e.g., animation, transform)")
    code: str
    source_file: str  # Track where we found it
    frameworks: List[str]
    prerequisites: List[str] = Field(default_factory=list)
    related_concepts: List[str] = Field(default_factory=list)
    validation_examples: List[str] = Field(default_factory=list)
    usage_count: int = 0  # Track how often we see this pattern
    variations: List[str] = Field(default_factory=list)  # Track variations of the pattern

class ConceptRelationship(BaseModel):
    """Represents a relationship between two concepts"""
    source: str
    target: str
    relationship_type: str
    strength: float = 1.0

class ValidationTest(BaseModel):
    """Represents a validation test for a code pattern"""
    pattern_id: str
    test_code: str
    expected_behavior: str
    frameworks: List[str]

class DocumentationPage(BaseModel):
    """Represents a single documentation page"""
    title: str
    url: str
    introduction: Optional[str] = None
    code_blocks: List[CodeBlock]  # Keep the original working attribute
    code_patterns: Dict[str, CodePattern] = Field(default_factory=dict)  # Add new functionality
    topics: List[Topic]
    relationships: List[ConceptRelationship] = Field(default_factory=list)
    validation_tests: List[ValidationTest] = Field(default_factory=list)
    category: Optional[str] = None
    frameworks_used: List[str] = Field(default_factory=list)
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    model_config = ConfigDict(
        ser_json={
            datetime: lambda dt: dt.isoformat()
        }
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        # Aggregate frameworks from both code_blocks and code_patterns
        frameworks = set()
        
        # From code_blocks
        for block in data.get('code_blocks', []):
            frameworks.update(block.frameworks)
            
        # From code_patterns
        for pattern in data.get('code_patterns', {}).values():
            frameworks.update(pattern.frameworks)
            
        self.frameworks_used = list(frameworks)
        self._determine_category()
    
    def _determine_category(self):
        """Determine the main category of the documentation"""
        title_lower = self.title.lower()
        if '3d' in title_lower or 'reality' in title_lower:
            self.category = '3D_Content'
        elif 'immersive' in title_lower:
            self.category = 'Immersive_Experience'
        elif 'window' in title_lower or 'view' in title_lower:
            self.category = 'UI_Components'
        elif 'first' in title_lower or 'getting started' in title_lower:
            self.category = 'Getting_Started'
        else:
            self.category = 'Other'
    
class CodeExample(BaseModel):
    """Code example from documentation"""
    code: str
    language: str = "swift"
    context: Optional[str] = None
    source_file: Optional[str] = None
    line_number: Optional[int] = None

class DocumentationEntry(BaseModel):
    """Documentation entry with code examples"""
    title: str
    content: str
    code_examples: List[CodeExample] = []
    metadata: Dict[str, Any] = {}

class ProjectResource(BaseModel):
    """Project resource from documentation"""
    title: str
    url: str
    download_url: str
    documentation_url: Optional[str] = None
    documentation_title: Optional[str] = None
    local_path: Optional[Path] = None
    downloaded: bool = False

    def mark_downloaded(self, path: Path):
        """Mark project as downloaded and set local path"""
        self.downloaded = True
        self.local_path = path
    
    @classmethod
    def model_validate(cls, data: dict):
        """Pydantic v2 compatible validation method"""
        if isinstance(data.get('local_path'), str):
            data['local_path'] = Path(data['local_path'])
        return cls(**data)
    
    def model_dump(self, *args, **kwargs):
        """Pydantic v2 compatible dump method"""
        d = super().model_dump(*args, **kwargs)
        if d.get('local_path'):
            d['local_path'] = str(d['local_path'])
        return d
    
    def dict(self, *args, **kwargs):
        """Legacy dict method for compatibility"""
        return self.model_dump(*args, **kwargs)
    
class PatternType(str, Enum):
    """Pattern types for code analysis"""
    # Framework patterns
    SWIFTUI = "swiftui"
    REALITYKIT = "realitykit"
    
    # UI patterns
    VIEW = "view"
    REALITY_VIEW = "reality_view"
    TEXT = "text"
    
    # Entity patterns
    MODEL_ENTITY = "model_entity"
    ENTITY = "entity"
    
    # State patterns
    STATE = "state"
    OBSERVED_OBJECT = "observed_object"
    STATE_OBJECT = "state_object"
    
    # Gesture patterns
    DRAG_GESTURE = "drag_gesture"
    TAP_GESTURE = "tap_gesture"
    GESTURE = "gesture"
    
    # Animation patterns
    WITH_ANIMATION = "with_animation"
    ANIMATION = "animation"
    TRANSITION = "transition"
    
    # Lifecycle patterns
    ON_APPEAR = "on_appear"
    ON_DISAPPEAR = "on_disappear"
    TASK = "task"
    ON_CHANGE = "on_change"
    
    # Spatial patterns
    POSITION = "position"
    SCALE = "scale"
    ROTATION = "rotation"
    TRANSFORM = "transform"
    
    # Interaction patterns
    ON_TAP_GESTURE = "on_tap_gesture"
    ON_LONG_PRESS_GESTURE = "on_long_press_gesture"
    SIMULTANEOUS_GESTURE = "simultaneous_gesture"
    HIGH_PRIORITY_GESTURE = "high_priority_gesture"
    
    # Reality Composer Pro patterns
    USDZ_LOADING = "usdz_loading"
    REALITY_FILE = "reality_file"
    MATERIAL_VARIANTS = "material_variants"
    ANIMATION_CONTROLLER = "animation_controller"
    REALITY_COMPOSER_IMPORT = "reality_composer_import"
    REALITY_COMPOSER_ASSET = "reality_composer_asset"
    
    # Component System patterns
    COMPONENT_DEFINITION = "component_definition"
    COMPONENT_ACCESS = "component_access"
    COMPONENT_ADD = "component_add"
    COMPONENT_SYSTEM = "component_system"
    COMPONENT_QUERY = "component_query"
    COMPONENT_UPDATE = "component_update"
    
    # RealityKit System patterns
    SCENE_SYSTEM = "scene_system"
    SCENE_UPDATE = "scene_update"
    SCENE_SETUP = "scene_setup"
    ENTITY_SYSTEM = "entity_system"
    ENTITY_QUERY = "entity_query"
    ENTITY_SUBSCRIPTION = "entity_subscription"
    COMPONENT_REGISTRATION = "component_registration"
    EVENT_SYSTEM = "event_system"
    EVENT_HANDLING = "event_handling"
    EVENT_SUBSCRIPTION = "event_subscription"
    
    # Entity Action patterns
    TRANSFORM_ACTION = "transform_action"
    TRANSFORM_ANIMATE = "transform_animate"
    TRANSFORM_SEQUENCE = "transform_sequence"
    PHYSICS_ACTION = "physics_action"
    PHYSICS_CONSTRAINT = "physics_constraint"
    HIERARCHY_ACTION = "hierarchy_action"
    HIERARCHY_QUERY = "hierarchy_query"
    ANIMATION_ACTION = "animation_action"
    ANIMATION_CONTROL = "animation_control"
    INTERACTION_ACTION = "interaction_action"
    GESTURE_ACTION = "gesture_action"
    
    # View Attachment patterns
    VIEW_ATTACH = "view_attach"
    VIEW_ENTITY = "view_entity"
    VIEW_GEOMETRY = "view_geometry"
    ATTACH_TRANSFORM = "attach_transform"
    ATTACH_ORIENTATION = "attach_orientation"
    ATTACH_POSITION = "attach_position"
    REALITY_VIEW_CONTENT = "reality_view_content"
    REALITY_VIEW_UPDATE = "reality_view_update"

class Pattern(BaseModel):
    """Represents a detected code pattern"""
    name: str
    type: PatternType
    confidence: float
    source_code: Optional[str] = None
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    start: int = 0  # Start position in the code
    end: int = 0    # End position in the code

class PatternRelationship(BaseModel):
    """Represents a relationship between patterns"""
    source: Pattern
    target: Pattern
    relationship_type: str
    confidence: float

class ValidationResult(BaseModel):
    """Results of pattern validation"""
    framework_requirements_met: bool
    has_required_patterns: bool
    relationships_valid: bool
    missing_patterns: List[str] = []
    invalid_relationships: List[str] = []
    validation_messages: List[str] = []
    
class PatternContext(BaseModel):
    """Represents the context in which a pattern appears"""
    pattern: Pattern
    context_type: str
    related_patterns: List[Pattern]
    scope: Dict[str, int]  # start/end line numbers
    is_valid: bool
    validation_messages: List[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0)
    
    def __str__(self) -> str:
        return f"{self.context_type} context for {self.pattern.name} ({len(self.related_patterns)} related patterns)"
    
    def add_validation_message(self, message: str):
        """Add a validation message"""
        self.validation_messages.append(message)
        
    def get_patterns_by_type(self, pattern_type: PatternType) -> List[Pattern]:
        """Get all related patterns of a specific type"""
        return [p for p in self.related_patterns if p.type == pattern_type]
    
    def has_pattern(self, pattern_name: str) -> bool:
        """Check if a specific pattern exists in this context"""
        return any(p.name == pattern_name for p in self.related_patterns)
    
    def get_scope_lines(self) -> range:
        """Get the line range for this context"""
        return range(self.scope['start'], self.scope['end'] + 1)
    
class SemanticAnalysis(BaseModel):
    """Results of semantic analysis"""
    pattern_roles: Dict[str, Set[str]]  # Pattern name -> set of roles
    relationships: List[Tuple[Pattern, str, Pattern]]  # (source, relationship_type, target)
    semantic_groups: Dict[str, Set[str]]  # Group type -> set of pattern names
    confidence_scores: Dict[str, float]  # Pattern name -> confidence score
    context_hierarchy: Dict[str, List[str]]  # Parent pattern -> list of child patterns