from bs4 import BeautifulSoup
from models.base import ConceptRelationship, CodePattern
from typing import List
import logging
import re

logger = logging.getLogger(__name__)

class RelationshipExtractor:
    """Extracts relationships between concepts in documentation"""
    
    def extract_relationships(self, content: str, code_patterns: dict) -> List[ConceptRelationship]:
        """Extract relationships from Swift code content"""
        relationships = []
        
        # Parse Swift imports
        import_relationships = self._extract_import_relationships(content)
        relationships.extend(import_relationships)
        
        # Extract code pattern dependencies
        code_relationships = self._extract_code_relationships(code_patterns)
        relationships.extend(code_relationships)
        
        # Extract VisionOS-specific patterns
        visionos_relationships = self._analyze_visionos_patterns(content)
        relationships.extend(visionos_relationships)
        
        return relationships
    
    def _extract_import_relationships(self, content: str) -> List[ConceptRelationship]:
        """Extract framework relationships from Swift imports"""
        relationships = []
        
        # Find import statements
        import_lines = [line.strip() for line in content.split('\n') if line.strip().startswith('import ')]
        
        for line in import_lines:
            framework = line.replace('import ', '').strip()
            if framework:
                relationships.append(
                    ConceptRelationship(
                        source=framework,
                        target='framework_usage',
                        relationship_type="import_dependency",
                        strength=1.0
                    )
                )
        
        return relationships
    
    def _extract_code_relationships(self, code_patterns: dict) -> List[ConceptRelationship]:
        relationships = []
        
        # Add framework dependencies
        for pattern_id, pattern in code_patterns.items():
            # Check pattern type and structure
            if isinstance(pattern, (list, tuple)):
                for p in pattern:
                    self._process_single_pattern(p, pattern_id, relationships)
            else:
                self._process_single_pattern(pattern, pattern_id, relationships)
        
        return relationships
    
    def _process_single_pattern(self, pattern, pattern_id: str, relationships: List[ConceptRelationship]):
        """Process a single pattern for relationships"""
        # Extract code content
        code_content = None
        if isinstance(pattern, dict):
            code_content = pattern.get('content', '')  # Try 'content' first
            if not code_content:
                code_content = pattern.get('code', '')  # Fall back to 'code'
        elif hasattr(pattern, 'content'):
            code_content = pattern.content
        elif hasattr(pattern, 'code'):
            code_content = pattern.code
        
        # Only process if we have code content
        if code_content:
            # Process frameworks
            frameworks = []
            if isinstance(pattern, dict):
                frameworks = pattern.get('frameworks', [])
            elif hasattr(pattern, 'frameworks'):
                frameworks = pattern.frameworks
            
            # Add framework relationships
            for framework in frameworks:
                relationships.append(
                    ConceptRelationship(
                        source=framework,
                        target=pattern_id,
                        relationship_type="framework_dependency",
                        strength=1.0
                    )
                )
            
            # Analyze the code content
            if 'RealityKit' in frameworks:
                self._analyze_realitykit_dependencies({'code': code_content, 'pattern_type': pattern_id}, relationships)
    
    def _analyze_realitykit_dependencies(self, pattern, relationships: List[ConceptRelationship]):
        """Analyze RealityKit specific dependencies"""
        # Get code content safely
        code_content = None
        if isinstance(pattern, dict):
            code_content = pattern.get('content', '') or pattern.get('code', '')
        elif hasattr(pattern, 'content'):
            code_content = pattern.content
        elif hasattr(pattern, 'code'):
            code_content = pattern.code
            
        if code_content and 'ModelEntity' in code_content:
            relationships.append(
                ConceptRelationship(
                    source='3d_content',
                    target=pattern.get('pattern_type', 'unknown') if isinstance(pattern, dict) else pattern.pattern_type,
                    relationship_type="concept_dependency",
                    strength=0.9
                )
            )
    
    def _analyze_audio_dependencies(self, pattern, relationships: List[ConceptRelationship]):
        """Analyze audio-specific dependencies and relationships"""
        code_content = None
        if isinstance(pattern, dict):
            code_content = pattern.get('content', '') or pattern.get('code', '')
        elif hasattr(pattern, 'content'):
            code_content = pattern.content
        elif hasattr(pattern, 'code'):
            code_content = pattern.code
            
        if not code_content:
            return
            
        # Check for audio frameworks
        if any(framework in pattern.code for framework in ['AVFoundation', 'AVFAudio']):
            relationships.append(
                ConceptRelationship(
                    source='spatial_audio',
                    target=pattern.pattern_type,
                    relationship_type="framework_dependency",
                    strength=1.0
                )
            )
        
        # Check for RealityKit audio features
        if 'AudioComponent' in pattern.code or 'SpatialAudio' in pattern.code:
            relationships.append(
                ConceptRelationship(
                    source='realitykit_audio',
                    target=pattern.pattern_type,
                    relationship_type="feature_dependency",
                    strength=0.9
                )
            )
        
        # Check for audio-visual synchronization
        if 'VideoPlayer' in pattern.code and any(audio_term in pattern.code 
            for audio_term in ['audio', 'sound', 'volume']):
            relationships.append(
                ConceptRelationship(
                    source='media_sync',
                    target=pattern.pattern_type,
                    relationship_type="feature_dependency",
                    strength=0.8
                )
            )
    
    def _analyze_game_mechanics(self, pattern, relationships: List[ConceptRelationship]):
        """Analyze game-specific mechanics and physics relationships"""
        # Get code content safely
        code_content = None
        if isinstance(pattern, dict):
            code_content = pattern.get('content', '') or pattern.get('code', '')
        elif hasattr(pattern, 'content'):
            code_content = pattern.content
        elif hasattr(pattern, 'code'):
            code_content = pattern.code
            
        if not code_content:
            return
            
        # Physics system usage
        if any(term in code_content for term in ['PhysicsBodyComponent', 'PhysicsMotion', 'collision']):
            relationships.append(
                ConceptRelationship(
                    source='physics_system',
                    target=pattern.get('pattern_type', 'unknown') if isinstance(pattern, dict) else getattr(pattern, 'pattern_type', 'unknown'),
                    relationship_type="feature_dependency",
                    strength=1.0
                )
            )
        
        # Game input handling
        if any(term in code_content for term in ['InputTarget', 'handleTap', 'handleDrag']):
            relationships.append(
                ConceptRelationship(
                    source='game_input',
                    target=pattern.get('pattern_type', 'unknown') if isinstance(pattern, dict) else getattr(pattern, 'pattern_type', 'unknown'),
                    relationship_type="interaction_pattern",
                    strength=0.9
                )
            )
        
        # Game state management
        if 'GameState' in code_content or 'score' in code_content.lower():
            relationships.append(
                ConceptRelationship(
                    source='game_state',
                    target=pattern.get('pattern_type', 'unknown') if isinstance(pattern, dict) else getattr(pattern, 'pattern_type', 'unknown'),
                    relationship_type="state_management",
                    strength=0.8
                )
            )
        
        # Collision detection
        if 'CollisionComponent' in code_content or 'collision(with:)' in code_content:
            relationships.append(
                ConceptRelationship(
                    source='collision_system',
                    target=pattern.get('pattern_type', 'unknown') if isinstance(pattern, dict) else getattr(pattern, 'pattern_type', 'unknown'),
                    relationship_type="physics_interaction",
                    strength=0.9
                )
            )
    
    def _analyze_swift_structure(self, content: str) -> List[ConceptRelationship]:
        """Analyze Swift code structure for relationships"""
        relationships = []
        
        # Find class/struct definitions
        type_definitions = re.finditer(r'(class|struct|enum)\s+(\w+)', content)
        for match in type_definitions:
            type_kind, type_name = match.groups()
            relationships.append(
                ConceptRelationship(
                    source=type_name,
                    target=type_kind,
                    relationship_type="type_definition",
                    strength=0.9
                )
            )
        
        # Find protocol conformance
        protocol_matches = re.finditer(r':\s*(.*?)\s*{', content)
        for match in protocol_matches:
            protocols = [p.strip() for p in match.group(1).split(',')]
            for protocol in protocols:
                if protocol != 'Codable':  # Skip common protocols
                    relationships.append(
                        ConceptRelationship(
                            source=protocol,
                            target='protocol_conformance',
                            relationship_type="protocol_dependency",
                            strength=0.8
                        )
                    )
        
        return relationships
    
    def _analyze_visionos_patterns(self, content: str) -> List[ConceptRelationship]:
        """Analyze VisionOS-specific patterns and relationships"""
        relationships = []
        
        # View Types
        if 'WindowGroup' in content:
            relationships.append(
                ConceptRelationship(
                    source='2d_views',
                    target='window_management',
                    relationship_type="view_hierarchy",
                    strength=0.9
                )
            )
        
        if 'ImmersiveSpace' in content:
            relationships.append(
                ConceptRelationship(
                    source='immersive_views',
                    target='spatial_experience',
                    relationship_type="view_hierarchy",
                    strength=1.0
                )
            )
        
        # 3D Content
        if 'RealityView' in content:
            relationships.append(
                ConceptRelationship(
                    source='3d_content',
                    target='realitykit_integration',
                    relationship_type="content_type",
                    strength=0.9
                )
            )
        
        # Input Handling
        if 'HandTrackingProvider' in content:
            relationships.append(
                ConceptRelationship(
                    source='hand_tracking',
                    target='input_system',
                    relationship_type="input_method",
                    strength=0.8
                )
            )
        
        # Spatial Audio
        if 'SpatialAudioEngine' in content:
            relationships.append(
                ConceptRelationship(
                    source='spatial_audio',
                    target='audio_system',
                    relationship_type="audio_feature",
                    strength=0.9
                )
            )
        
        return relationships