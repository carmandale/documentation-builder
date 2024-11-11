from pathlib import Path
from typing import Dict, Set, List, Any, Optional
import re
from collections import defaultdict
from utils.logging import logger

class ComponentAnalyzer:
    """Analyzes UI components from real VisionOS samples"""
    
    def __init__(self, samples_dir: Path = Path('data/projects')):
        self.samples_dir = samples_dir
        self.components: Dict[str, Set[str]] = defaultdict(set)
        self.imports: Dict[str, Set[str]] = defaultdict(set)
        self.relationships: Dict[str, Set[str]] = defaultdict(set)
    
    def analyze_samples(self, samples_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Analyze all Swift files in samples directory
        
        Args:
            samples_dir: Optional directory to analyze. Uses self.samples_dir if None.
            
        Returns:
            Dict containing analysis results with components, imports and relationships
        """
        if samples_dir is None:
            samples_dir = self.samples_dir
        
        try:
            swift_files = list(samples_dir.glob('**/*.swift'))
            logger.info(f"Found {len(swift_files)} Swift files to analyze")
            
            for file_path in swift_files:
                try:
                    content = file_path.read_text()
                    self._analyze_file(content, file_path)
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")
            
            return self._generate_report()
            
        except Exception as e:
            logger.error(f"Error in component analysis: {e}")
            return {}
    
    def _analyze_file(self, content: str, file_path: Path):
        """Analyze a single Swift file"""
        # Extract imports
        imports = set(re.findall(r'import\s+(\w+)', content))
        
        # Define UI patterns
        ui_patterns = {
            'navigation': set(re.findall(r'(?:NavigationStack|NavigationSplitView|NavigationLink)\b', content)),
            'windows': set(re.findall(r'(?:WindowGroup|VolumetricWindow|ImmersiveSpace)\b', content)),
            'controls': set(re.findall(r'(?:Button|Toggle|Slider|Picker)\b', content)),
            'layout': set(re.findall(r'(?:HStack|VStack|Grid|LazyVGrid)\b', content)),
            'ornaments': set(re.findall(r'(?:\.ornament|\.toolbar|\.windowStyle)\b', content)),
            'media': set(re.findall(r'(?:VideoPlayer|AVPlayer|SpatialPlayer)\b', content))
        }
        
        # Extract state management patterns
        state_patterns = {
            'property_wrappers': set(re.findall(r'@(?:State|StateObject|ObservedObject|EnvironmentObject|Binding|Environment|Published|Observable)\b', content)),
            'environment': set(re.findall(r'\.environment\(\s*\\\.[\w.]+\s*\)', content)),
            'bindings': set(re.findall(r'@Binding\s+var\s+\w+', content)),
            'observation': set(re.findall(r'@(?:Observable|Observation)\s+class', content))
        }
        
        # Extract lifecycle patterns
        lifecycle_patterns = {
            'view_lifecycle': set(re.findall(r'\.(?:onAppear|onDisappear|task|onChange)\s*[({]', content)),
            'async_patterns': set(re.findall(r'@MainActor|async\s+func|await\s+', content)),
            'tasks': set(re.findall(r'Task\s*[{]|\.task\s*[{]', content)),
            'phase_handling': set(re.findall(r'\.phase\b|PhaseAnimator|ContentTransition', content))
        }
        
        # Extract update patterns
        update_patterns = {
            'reality_view': set(re.findall(r'RealityView\s*[{]\s*[^}]*(?:content|update|attachments)\s+in\b', content)),
            'system_updates': set(re.findall(r'func\s+update\s*\([^)]*\)\s*(?:async\s+)?[{]', content)),
            'animation_updates': set(re.findall(r'\.animation\s*\([^)]*\)|withAnimation\s*[{]', content))
        }
        
        # Enhanced Reality Composer Pro patterns
        reality_composer_patterns = {
            'behaviors': set(re.findall(r'(?:Behavior|BehaviorComponent|BehaviorValue|InputTarget|BehaviorSystem|BehaviorDefinition|BehaviorEvents)\b', content)),
            'timelines': set(re.findall(r'(?:Timeline|AnimationTimeline|TimelineAnimation|PlaybackController|TimelineAsset|TimelineDefinition|TimelineEvents)\b', content)),
            'shader_graph': set(re.findall(r'(?:ShaderGraphMaterial|CustomMaterial|MaterialParameters|ShaderFunction|MaterialPropertyBlock|ShaderDefinition|ShaderEvents)\b', content)),
            'custom_systems': set(re.findall(r'(?:SystemComponent|SystemRegistry|ComponentSystem|UpdateSystem|SystemTraits|SystemDefinition|SystemEvents)\b', content)),
            'assets': set(re.findall(r'\.usda\b|\.usdz\b|\.rcproject\b|\.reality\b|\.materialx\b|\.shadergraph\b|\.behavior\b|\.timeline\b', content)),
            'material_properties': set(re.findall(r'\.material\s*=|\.materials\s*=|\.customMaterial\s*=|\.shaderGraph\s*=|\.materialDefinition\s*=', content)),
            
            # Enhanced Physics Patterns
            'physics': set(re.findall(r'(?:PhysicsBody|PhysicsMotion|PhysicsMaterial|PhysicsSimulation|DynamicBody|StaticBody|KinematicBody|PhysicsDefinition|PhysicsEvents)\b', content)),
            'collisions': set(re.findall(r'(?:CollisionComponent|TriggerComponent|ContactEventHandler|CollisionFilter|CollisionShape|CollisionMask|CollisionDefinition|CollisionEvents)\b', content)),
            'forces': set(re.findall(r'(?:PhysicsForce|GravityModifier|ForceField|ImpulseForce|TorqueForce|ConstantForce|ForceDefinition|ForceEvents)\b', content)),
            
            # Enhanced Component Patterns
            'components': set(re.findall(r'(?:ModelComponent|TransformComponent|SceneComponent|InputTargetComponent|PhysicsBodyComponent|CollisionComponent|ComponentDefinition|ComponentEvents)\b', content)),
            'input_handling': set(re.findall(r'(?:InputTargetHandler|GestureRecognizer|TargetComponent|InputDevice|InputSystem|InputDefinition|InputEvents)\b', content)),
            'scene_graph': set(re.findall(r'(?:SceneGraph|ParentEntity|ChildEntity|EntityContainer|SceneSystem|EntityQuery|SceneDefinition|SceneEvents)\b', content)),
            
            # Enhanced Simulation Patterns
            'simulation': set(re.findall(r'(?:SimulationSystem|SimulationState|SimulationComponent|PhysicsSimulation|ParticleSimulation|SimulationDefinition|SimulationEvents)\b', content)),
            'particles': set(re.findall(r'(?:ParticleSystem|ParticleEmitter|ParticleModifier|EmissionShape|ParticleProperties|ParticleDefinition|ParticleEvents)\b', content)),
            'constraints': set(re.findall(r'(?:PhysicsConstraint|JointConstraint|FixedConstraint|HingeConstraint|SpringConstraint|ConstraintDefinition|ConstraintEvents)\b', content)),
            
            # New Event System Patterns
            'events': set(re.findall(r'(?:EventHandler|EventSystem|EventComponent|EventDefinition|EventTrigger|EventResponse|EventQueue|EventDispatcher)\b', content)),
            'triggers': set(re.findall(r'(?:TriggerSystem|TriggerComponent|TriggerDefinition|TriggerHandler|TriggerResponse|TriggerQueue|TriggerDispatcher)\b', content)),
            'actions': set(re.findall(r'(?:ActionSystem|ActionComponent|ActionDefinition|ActionHandler|ActionResponse|ActionQueue|ActionDispatcher)\b', content)),
            
            # Enhanced Property Modification Patterns
            'property_changes': set(re.findall(r'(?:setPropertyValue|setMaterialProperty|setShaderParameter|setTextureProperty|setAnimationProperty|setPhysicsProperty)\s*\(', content)),
            'dynamic_properties': set(re.findall(r'\.(?:materialParameters|shaderParameters|animationParameters|behaviorParameters|physicsParameters|sceneParameters)\s*[=.]', content)),
            'property_bindings': set(re.findall(r'\.bind\s*\(\s*["\']\w+["\']\s*,\s*to:', content)),
            
            # Enhanced Trigger Patterns
            'triggers': set(re.findall(r'(?:addTrigger|removeTrigger|enableTrigger|disableTrigger|TriggerCondition)\b', content)),
            'trigger_conditions': set(re.findall(r'\.(?:when|onTrigger|triggerWhen|triggerOnCondition)\s*[({]', content)),
            'trigger_actions': set(re.findall(r'\.(?:then|perform|execute|triggerAction)\s*[({]', content)),
            
            # Enhanced Scene Modification Patterns
            'scene_changes': set(re.findall(r'(?:modifyEntity|updateScene|updateMaterials|updateBehaviors|updatePhysics|updateComponents)\b', content)),
            'runtime_updates': set(re.findall(r'\.(?:updatePropertyValue|updateMaterial|updateBehavior|updateAnimation|updatePhysics|updateComponent)\s*[({]', content)),
            'state_changes': set(re.findall(r'\.(?:setState|setMode|setConfiguration|setParameters|setProperties|setAttributes)\s*[({]', content)),
            
            # New Scene Component Patterns
            'scene_components': set(re.findall(r'(?:SceneComponent|SceneModifier|SceneModification|SceneUpdate|SceneConfiguration)\b', content)),
            'component_updates': set(re.findall(r'(?:updateComponent|modifyComponent|configureComponent|setupComponent)\s*[({]', content)),
            'component_properties': set(re.findall(r'\.(?:componentProperties|componentParameters|componentConfiguration|componentAttributes)\s*[=.]', content)),
            
            # New Material Update Patterns
            'material_updates': set(re.findall(r'(?:updateMaterial|modifyMaterial|configureMaterial|setupMaterial)\s*[({]', content)),
            'material_properties': set(re.findall(r'\.(?:materialProperties|materialParameters|materialConfiguration|materialAttributes)\s*[=.]', content)),
            'shader_updates': set(re.findall(r'(?:updateShader|modifyShader|configureShader|setupShader)\s*[({]', content))
        }
        
        # Extract Reality Composer Pro relationships
        rcp_relationships = {
            'behavior_timeline': set(re.findall(r'(?:Behavior|BehaviorComponent).+?Timeline', content)),
            'shader_material': set(re.findall(r'(?:ShaderGraphMaterial|CustomMaterial).+?Entity', content)),
            'asset_references': set(re.findall(r'try\s+await\s+Entity\s*\(\s*named:\s*["\']\w+["\']', content)),
            'physics_collision': set(re.findall(r'(?:PhysicsBody|PhysicsMotion).+?(?:Collision|Contact)', content)),
            'component_physics': set(re.findall(r'(?:ModelComponent|TransformComponent).+?Physics', content)),
            'input_behavior': set(re.findall(r'(?:InputTarget|GestureRecognizer).+?Behavior', content)),
            'simulation_constraint': set(re.findall(r'(?:Simulation|Physics).+?Constraint', content)),
            'particle_material': set(re.findall(r'(?:ParticleSystem|ParticleEmitter).+?Material', content)),
            
            # New Event Relationships
            'event_trigger': set(re.findall(r'(?:Event|Trigger).+?(?:Handler|Response)', content)),
            'action_event': set(re.findall(r'(?:Action|Response).+?(?:Event|Trigger)', content)),
            'component_event': set(re.findall(r'(?:Component|System).+?(?:Event|Trigger)', content)),
            
            # New Property/Trigger Relationships
            'property_trigger': set(re.findall(r'(?:Property|Parameter).+?(?:Trigger|Condition)', content)),
            'trigger_action': set(re.findall(r'(?:Trigger|Condition).+?(?:Action|Response)', content)),
            'property_animation': set(re.findall(r'(?:Property|Parameter).+?(?:Animation|Timeline)', content)),
            
            # New Scene Update Relationships
            'property_update': set(re.findall(r'(?:Property|Parameter).+?(?:Update|Change)', content)),
            'scene_update': set(re.findall(r'(?:Scene|Entity).+?(?:Update|Modify)', content)),
            'material_update': set(re.findall(r'(?:Material|Shader).+?(?:Update|Change)', content)),
            
            # New Property/Scene Relationships
            'property_scene': set(re.findall(r'(?:Property|Parameter).+?(?:Scene|Entity)', content)),
            'material_scene': set(re.findall(r'(?:Material|Shader).+?(?:Scene|Entity)', content)),
            'component_scene': set(re.findall(r'(?:Component|System).+?(?:Scene|Entity)', content)),
            
            # New Update Relationships
            'component_update': set(re.findall(r'(?:Component|System).+?(?:Update|Change)', content))
        }
        
        # Enhanced Scene Modification Patterns
        scene_modification_patterns = {
            # Direct Property Changes
            'property_changes': set(re.findall(r'(?:\.transform\s*=|\.position\s*=|\.scale\s*=|\.rotation\s*=|\.orientation\s*=|\.eulerAngles\s*=|\.quaternion\s*=|\.localPosition\s*=|\.worldPosition\s*=)', content)),
            'material_changes': set(re.findall(r'(?:\.material\s*=|\.materials\s*=|\.baseColor\s*=|\.roughness\s*=|\.metallic\s*=|\.opacity\s*=|\.normal\s*=|\.emissive\s*=|\.materialParameters\s*=|\.shaderParameters\s*=)', content)),
            'animation_changes': set(re.findall(r'(?:\.speed\s*=|\.duration\s*=|\.repeatCount\s*=|\.autoreverses\s*=|\.isPlaying\s*=|\.currentTime\s*=|\.animationParameters\s*=|\.playbackRate\s*=)', content)),
            'physics_changes': set(re.findall(r'(?:\.mass\s*=|\.friction\s*=|\.restitution\s*=|\.velocity\s*=|\.angularVelocity\s*=|\.isAffectedByGravity\s*=|\.physicsParameters\s*=|\.collisionFilter\s*=)', content)),
            
            # Runtime Updates
            'reality_updates': set(re.findall(r'RealityView\s*[{]\s*[^}]*(?:content|attachments)\s+in[^}]+?update:', content)),
            'system_updates': set(re.findall(r'func\s+update\s*\([^)]*\)\s*(?:async\s+)?[{]', content)),
            'component_updates': set(re.findall(r'(?:updateComponent|modifyComponent|configureComponent|setupComponent|updateProperties|updateParameters)\s*[({]', content)),
            'timeline_updates': set(re.findall(r'(?:updateTimeline|modifyTimeline|configureTimeline|updateAnimation|setTime|updatePlayback)\s*[({]', content)),
            'behavior_updates': set(re.findall(r'(?:updateBehavior|modifyBehavior|configureBehavior|triggerBehavior|setBehaviorState|updateBehaviorState)\s*[({]', content)),
            
            # Scene Graph Changes
            'hierarchy_changes': set(re.findall(r'(?:addChild|removeFromParent|moveToParent|replaceChild|insertChild|reparent|reorderChild)\s*[({]', content)),
            'entity_changes': set(re.findall(r'(?:addEntity|removeEntity|replaceEntity|createEntity|destroyEntity|spawnEntity|cloneEntity)\s*[({]', content)),
            'scene_traversal': set(re.findall(r'(?:findEntity|findChild|findParent|findAncestor|findDescendant|findByName|findByType|findByComponent)\s*[({]', content)),
            
            # State-Driven Changes
            'state_bindings': set(re.findall(r'@Binding\s+var\s+\w+\s*:', content)),
            'observable_changes': set(re.findall(r'@Observable\s+(?:class|struct)\s+\w+', content)),
            'environment_changes': set(re.findall(r'@Environment\s*\(\s*\\\.[\w.]+\s*\)', content)),
            
            # Component State Changes
            'component_state': set(re.findall(r'(?:\.isEnabled\s*=|\.isActive\s*=|\.state\s*=|\.mode\s*=|\.configuration\s*=|\.parameters\s*=|\.settings\s*=)', content)),
            'component_properties': set(re.findall(r'(?:\.properties\s*=|\.parameters\s*=|\.attributes\s*=|\.settings\s*=|\.configuration\s*=)', content)),
            'component_events': set(re.findall(r'(?:\.onEvent\s*[{]|\.handleEvent\s*[{]|\.triggerEvent\s*[{]|\.eventHandler\s*=)', content)),
            
            # RCP-Specific Updates
            'rcp_material_updates': set(re.findall(r'(?:updateMaterial|modifyMaterial|configureMaterial|setMaterialParameters|updateShaderParameters)\s*[({]', content)),
            'rcp_behavior_updates': set(re.findall(r'(?:updateBehavior|modifyBehavior|configureBehavior|setBehaviorParameters|updateBehaviorState)\s*[({]', content)),
            'rcp_animation_updates': set(re.findall(r'(?:updateAnimation|modifyAnimation|configureAnimation|setAnimationParameters|updateAnimationState)\s*[({]', content)),
            'rcp_physics_updates': set(re.findall(r'(?:updatePhysics|modifyPhysics|configurePhysics|setPhysicsParameters|updatePhysicsState)\s*[({]', content)),
            'rcp_component_updates': set(re.findall(r'(?:updateComponent|modifyComponent|configureComponent|setComponentParameters|updateComponentState)\s*[({]', content))
        }
        
        # Enhanced State Management Patterns
        state_management_patterns = {
            # State Property Patterns
            'state_properties': set(re.findall(r'@(?:State|StateObject|ObservedObject|Published|Observable|Binding)\s+(?:private\s+)?var\s+\w+', content)),
            'state_access': set(re.findall(r'(?:\$\w+|\w+\.wrappedValue|\w+\.projectedValue)', content)),
            'state_updates': set(re.findall(r'(?:self\.)?(\w+)\s*=\s*(?!self)', content)),
            
            # Environment Patterns
            'environment_values': set(re.findall(r'@Environment\(\\\.\w+\)\s+(?:private\s+)?var\s+\w+', content)),
            'environment_objects': set(re.findall(r'@EnvironmentObject\s+(?:private\s+)?var\s+\w+', content)),
            'environment_updates': set(re.findall(r'\.environment\(\s*\\\.[\w.]+\s*,\s*[\w.]+\)', content)),
            
            # Observation Patterns
            'observable_types': set(re.findall(r'@Observable\s+(?:final\s+)?(?:class|actor)\s+\w+', content)),
            'observation_registration': set(re.findall(r'\.observe\s*\(|\.register\s*\(|\.unregister\s*\(', content)),
            'observation_triggers': set(re.findall(r'(?:objectWillChange|willSet|didSet|objectDidChange)\.send\s*\(', content)),
            
            # State Flow Patterns
            'state_flow': set(re.findall(r'\.onChange\s*\(\s*of:\s*[\w\$\.]+\s*\)\s*{[^}]+}', content)),
            'state_dependencies': set(re.findall(r'\.animation\s*\([^)]*,\s*value:\s*[\w\$\.]+\)', content)),
            'state_propagation': set(re.findall(r'\.propagateState\s*\(|\.updateState\s*\(|\.refreshState\s*\(', content)),
            
            # RCP State Integration
            'rcp_state_bindings': set(re.findall(r'@Binding\s+var\s+\w+\s*:\s*(?:Entity|Material|Component)', content)),
            'rcp_state_updates': set(re.findall(r'\.update\s*\(\s*state:\s*[\w\$\.]+\s*\)', content)),
            'rcp_state_sync': set(re.findall(r'\.syncState\s*\(|\.bindState\s*\(|\.linkState\s*\(', content)),
            
            # State Persistence
            'state_persistence': set(re.findall(r'@SceneStorage|@AppStorage|@UserDefault', content)),
            'persistence_access': set(re.findall(r'UserDefaults\.|SceneStorage\.|AppStorage\.', content)),
            'persistence_updates': set(re.findall(r'(?:save|load|update|refresh)State\s*\(', content))
        }
        
        # Enhanced Binding Patterns (separated from state management)
        binding_patterns = {
            # SwiftUI Bindings
            'swiftui_bindings': set(re.findall(r'@Binding\s+(?:private\s+)?var\s+\w+', content)),
            'binding_creation': set(re.findall(r'Binding\s*\(\s*get:\s*{[^}]+},\s*set:\s*{[^}]+}\)', content)),
            'binding_updates': set(re.findall(r'(?:\$\w+|\w+\.binding)\s*=\s*', content)),
            
            # RCP Bindings
            'rcp_bindings': set(re.findall(r'@Binding\s+var\s+\w+\s*:\s*(?:Entity|Material|Component|Transform)', content)),
            'rcp_binding_updates': set(re.findall(r'\.bind\s*\(\s*["\']\w+["\']\s*,\s*to:', content)),
            'rcp_binding_sync': set(re.findall(r'\.syncBinding\s*\(|\.bindComponent\s*\(|\.linkBinding\s*\(', content)),
            
            # Binding Relationships
            'binding_chains': set(re.findall(r'\.bind\s*\([^)]*\)\.bind\s*\(', content)),
            'binding_transforms': set(re.findall(r'\.bind\s*\([^)]*\)\s*{[^}]*transform:', content)),
            'binding_conditions': set(re.findall(r'\.bind\s*\([^)]*\)\s*{[^}]*condition:', content))
        }
        
        # Enhanced State Flow Patterns
        state_flow_patterns = {
            # SwiftUI State Flow
            'state_handlers': set(re.findall(r'\.onChange\s*\(\s*of:\s*[\w\$\.]+\s*\)\s*{[^}]+}', content)),
            'state_watchers': set(re.findall(r'\.onReceive\s*\([^)]+\)\s*{[^}]+}', content)),
            'state_effects': set(re.findall(r'\.task\s*\([^)]*\)\s*{[^}]*\$[\w\.]+[^}]+}', content)),
            
            # RCP State Integration
            'rcp_state_handlers': set(re.findall(r'\.onUpdate\s*\([^)]*\)\s*{[^}]*(?:entity|material|component)[^}]+}', content)),
            'rcp_state_updates': set(re.findall(r'(?:entity|material|component)\.(?:update|modify|configure)\s*\([^)]*state:', content)),
            'rcp_state_sync': set(re.findall(r'\.sync(?:State|Properties|Configuration)\s*\([^)]*\)', content)),
            
            # Component State Flow
            'component_state_updates': set(re.findall(r'components\.(?:set|update|modify)\s*\([^)]*\)', content)),
            'component_state_sync': set(re.findall(r'\.syncComponent\s*\([^)]*\)', content)),
            'component_state_flow': set(re.findall(r'\.componentDidUpdate\s*{[^}]+}', content)),
            
            # Material State Flow
            'material_state_updates': set(re.findall(r'material\.(?:set|update|modify)(?:Parameter|Property)\s*\([^)]*\)', content)),
            'material_state_sync': set(re.findall(r'\.syncMaterial\s*\([^)]*\)', content)),
            'material_state_flow': set(re.findall(r'\.materialDidUpdate\s*{[^}]+}', content)),
            
            # Entity State Flow
            'entity_state_updates': set(re.findall(r'entity\.(?:set|update|modify)(?:Component|Property|State)\s*\([^)]*\)', content)),
            'entity_state_sync': set(re.findall(r'\.syncEntity\s*\([^)]*\)', content)),
            'entity_state_flow': set(re.findall(r'\.entityDidUpdate\s*{[^}]+}', content)),
            
            # State Binding Flow
            'binding_flow': set(re.findall(r'Binding\s*\(\s*get:\s*{[^}]+\$[\w\.]+[^}]+},\s*set:', content)),
            'binding_updates': set(re.findall(r'(?:\$\w+|\w+\.binding)\s*=\s*(?!self)', content)),
            'binding_transforms': set(re.findall(r'\.map\s*{[^}]*\$[\w\.]+[^}]+}', content)),
            
            # State Propagation Flow
            'state_propagation': set(re.findall(r'(?:self\.)?(\w+)\s*=\s*(?!self)', content)),
            'state_mutations': set(re.findall(r'(?:mutating\s+)?func\s+\w+\s*\([^)]*\)\s*{[^}]*(?:self\.)?[\w\.]+\s*=', content)),
            'state_transactions': set(re.findall(r'withTransaction|withAnimation|withMutation', content)),
            
            # State Observation Flow
            'observation_registration': set(re.findall(r'\.observe\s*\(|\.register\s*\(|\.unregister\s*\(', content)),
            'observation_triggers': set(re.findall(r'(?:objectWillChange|willSet|didSet|objectDidChange)\.send\s*\(', content)),
            'observation_flow': set(re.findall(r'\.observationRegistrar\s*\{[^}]+}', content)),
            
            # State Environment Flow
            'environment_values': set(re.findall(r'@Environment\(\\\.\w+\)\s+(?:private\s+)?var\s+\w+', content)),
            'environment_updates': set(re.findall(r'\.environment\(\s*\\\.[\w.]+\s*,\s*[\w.]+\)', content)),
            'environment_flow': set(re.findall(r'\.environmentObject\s*\([^)]+\)', content))
        }
        
        # Add new component pattern section
        component_patterns = {
            # Component Definition Patterns
            'component_definitions': set(re.findall(r'(?:struct|class)\s+\w+(?:Component|State)\s*:\s*(?:Component|Codable)', content)),
            
            # Component Properties
            'component_properties': set(re.findall(r'(?:public|private)\s+var\s+\w+\s*:\s*(?:Entity|Bool|SIMD3|Transform)', content)),
            
            # Component Methods
            'component_methods': set(re.findall(r'(?:mutating\s+)?func\s+on(?:Changed|Ended)\s*\(\s*value:\s*EntityTargetValue<[^>]+>', content)),
            
            # Component State Management
            'component_state': set(re.findall(r'@MainActor\s+(?:final\s+)?(?:class|struct)\s+\w+State\s*:\s*Sendable', content))
        }
        
        # Store findings
        if 'RealityKit' in imports:
            for category, patterns in component_patterns.items():
                self.components[f'component_{category}'].update(patterns)
        
        # Store findings with better categorization
        if 'SwiftUI' in imports:
            # Store UI patterns
            for category, patterns in ui_patterns.items():
                self.components[f'ui_{category}'].update(patterns)
                
            # Store state patterns
            for category, patterns in state_patterns.items():
                self.components[f'state_{category}'].update(patterns)
                
            # Store lifecycle patterns
            for category, patterns in lifecycle_patterns.items():
                self.components[f'lifecycle_{category}'].update(patterns)
                
            # Store update patterns
            for category, patterns in update_patterns.items():
                self.components[f'update_{category}'].update(patterns)
                
            # Store imports
            self.imports[str(file_path)] = imports
            
            # Track relationships
            if state_patterns['property_wrappers'] and update_patterns['system_updates']:
                self.relationships['state_update_integration'].add(str(file_path))
        
        # Store Reality Composer Pro patterns
        if any(imp in imports for imp in ['RealityKit', 'RealityFoundation']):
            for category, patterns in reality_composer_patterns.items():
                self.components[f'rcp_{category}'].update(patterns)
                
            # Track relationships
            for rel_type, patterns in rcp_relationships.items():
                if patterns:
                    self.relationships[f'rcp_{rel_type}'].add(str(file_path))
            
            # Enhanced Scene Modification Patterns
            for category, patterns in scene_modification_patterns.items():
                self.components[f'scene_{category}'].update(patterns)
                
                # Track relationships between modifications
                self._track_scene_relationships(content, str(file_path))
        
        # Store state management patterns
        if 'SwiftUI' in imports:
            for category, patterns in state_management_patterns.items():
                self.components[f'state_{category}'].update(patterns)
                
                # Track state relationships
                self._track_state_relationships(content, str(file_path))
            
            # Track RCP state integration
            if 'RealityKit' in imports:
                self._track_rcp_state_relationships(content, str(file_path))
        
        # Store binding patterns
        for category, patterns in binding_patterns.items():
            self.components[f'binding_{category}'].update(patterns)
            
            # Track binding relationships
            self._track_binding_relationships(content, str(file_path))
        
        # Store state flow patterns
        for category, patterns in state_flow_patterns.items():
            self.components[f'state_flow_{category}'].update(patterns)
            
            # Track state flow relationships
            self._track_state_flow_relationships(content, str(file_path))
        
        # Add RealityKitContent patterns section
        realitykit_content_patterns = {
            # System Components
            'system_components': set(re.findall(r'(?:struct|class)\s+\w+System\s*:\s*System', content)),
            
            # Gesture Components
            'gesture_components': set(re.findall(r'(?:struct|class)\s+\w+GestureComponent\s*:\s*(?:Component|GestureComponent)', content)),
            
            # Input Components
            'input_components': set(re.findall(r'(?:struct|class)\s+\w+InputComponent\s*:\s*(?:Component|InputComponent)', content)),
            
            # Component Event Handlers
            'event_handlers': set(re.findall(r'func\s+on(?:Changed|Ended)\s*\(\s*value:\s*EntityTargetValue<[^>]+>', content))
        }
        
        # Store findings
        if Path(file_path).parent.name == 'RealityKitContent':
            for category, patterns in realitykit_content_patterns.items():
                self.components[f'rcp_{category}'].update(patterns)
        
        # Track relationships between components and state
        self._track_component_relationships(content, str(file_path))

    def _generate_report(self) -> Dict[str, Any]:
        """Generate analysis report"""
        return {
            'components': self.components,
            'imports': self.imports,
            'relationships': self.relationships
        }

    def _track_scene_relationships(self, content: str, file_path: str):
        """Track relationships between scene modifications"""
        # SwiftUI-RCP Flow
        if any(term in content for term in self.components['state_flow_rcp_state_handlers']):
            if any(term in content for term in self.components['state_flow_state_handlers']):
                self.relationships['swiftui_rcp_flow'].add(file_path)
                
        # Component State Flow
        if any(term in content for term in self.components['state_flow_component_state_updates']):
            if any(term in content for term in self.components['state_flow_state_propagation']):
                self.relationships['component_state_flow'].add(file_path)
                
        # Material State Flow
        if any(term in content for term in self.components['state_flow_material_state_updates']):
            if any(term in content for term in self.components['state_flow_state_propagation']):
                self.relationships['material_state_flow'].add(file_path)
                
        # Entity State Flow
        if any(term in content for term in self.components['state_flow_entity_state_updates']):
            if any(term in content for term in self.components['state_flow_state_propagation']):
                self.relationships['entity_state_flow'].add(file_path)

    def _track_state_relationships(self, content: str, file_path: str):
        """Track relationships between state patterns"""
        # State-View relationships
        if any(term in content for term in self.components['state_state_properties']):
            if 'View' in content:
                self.relationships['state_view_integration'].add(file_path)
                
        # State-Environment relationships
        if any(term in content for term in self.components['state_environment_values']):
            if any(term in content for term in self.components['state_state_properties']):
                self.relationships['state_environment_integration'].add(file_path)
                
        # State-Observation relationships
        if any(term in content for term in self.components['state_observable_types']):
            if any(term in content for term in self.components['state_observation_triggers']):
                self.relationships['state_observation_integration'].add(file_path)

    def _track_binding_relationships(self, content: str, file_path: str):
        """Track relationships between bindings"""
        # SwiftUI-RCP Binding relationships
        if any(term in content for term in self.components['binding_swiftui_bindings']):
            if any(term in content for term in self.components['binding_rcp_bindings']):
                self.relationships['swiftui_rcp_binding_integration'].add(file_path)
                
        # Binding-State relationships
        if any(term in content for term in self.components['binding_binding_creation']):
            if any(term in content for term in self.components['state_state_properties']):
                self.relationships['binding_state_integration'].add(file_path)
                
        # Binding-Transform relationships
        if any(term in content for term in self.components['binding_binding_transforms']):
            if any(term in content for term in self.components['binding_binding_chains']):
                self.relationships['binding_transform_integration'].add(file_path)

    def _track_state_flow_relationships(self, content: str, file_path: str):
        """Track relationships in state flow patterns"""
        # State-View Flow
        if any(term in content for term in self.components['state_flow_view_integration']):
            if any(term in content for term in self.components['state_flow_state_handlers']):
                self.relationships['state_view_flow'].add(file_path)
                
        # State-Model Flow
        if any(term in content for term in self.components['state_flow_model_integration']):
            if any(term in content for term in self.components['state_flow_state_mutations']):
                self.relationships['state_model_flow'].add(file_path)
                
        # State-Environment Flow
        if any(term in content for term in self.components['state_flow_environment_integration']):
            if any(term in content for term in self.components['state_flow_state_updates']):
                self.relationships['state_environment_flow'].add(file_path)
                
        # State-RCP Flow
        if any(term in content for term in self.components['state_flow_rcp_state_bindings']):
            if any(term in content for term in self.components['state_flow_state_transactions']):
                self.relationships['state_rcp_flow'].add(file_path)
                
        # State-Storage Flow
        if any(term in content for term in self.components['state_flow_state_storage']):
            if any(term in content for term in self.components['state_flow_storage_updates']):
                self.relationships['state_storage_flow'].add(file_path)

    def _track_component_relationships(self, content: str, file_path: str):
        """Track relationships between components"""
        try:
            # Track SwiftUI-RealityKit relationships
            if 'SwiftUI' in content and 'RealityKit' in content:
                if any(term in content for term in ['RealityView', 'Entity', 'Model3D']):
                    self.relationships['swiftui_realitykit_integration'].add(file_path)
                    
            # Track Component-State relationships
            if any(term in content for term in ['@State', '@Binding', '@Observable']):
                if any(term in content for term in ['components.set', 'components.update']):
                    self.relationships['component_state_integration'].add(file_path)
                    
            # Track Material-Animation relationships
            if any(term in content for term in ['.material', '.materials']):
                if any(term in content for term in ['withAnimation', '.animation']):
                    self.relationships['material_animation_integration'].add(file_path)
                    
        except Exception as e:
            logger.error(f"Error tracking component relationships in {file_path}: {e}")

    def _track_rcp_state_relationships(self, content: str, file_path: str):
        """Track RealityKit component state relationships"""
        try:
            # Track RCP-Scene relationships
            if any(term in content for term in ['Entity', 'Scene', 'AnchorEntity']):
                if any(term in content for term in ['components.set', 'addChild']):
                    self.relationships['rcp_scene_integration'].add(file_path)
                    
            # Track RCP-Material relationships
            if any(term in content for term in ['Material', 'ShaderGraphMaterial']):
                if any(term in content for term in ['setParameter', 'parameters']):
                    self.relationships['rcp_material_integration'].add(file_path)
                    
            # Track RCP-Animation relationships
            if any(term in content for term in ['AnimationResource', 'PlaybackController']):
                if any(term in content for term in ['play', 'resume', 'pause']):
                    self.relationships['rcp_animation_integration'].add(file_path)
                    
        except Exception as e:
            logger.error(f"Error tracking RCP state relationships in {file_path}: {e}")