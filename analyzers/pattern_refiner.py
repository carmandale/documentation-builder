from pathlib import Path
from typing import Dict, Any, List, Set, Optional
import json
import logging
from utils.logging import logger
import re
from models.base import CodePattern, ValidationTest

class PatternRefiner:
    """Refines patterns based on actual Apple documentation and code"""
    
    def __init__(self, knowledge_dir: Path = Path('data/knowledge')):
        self.knowledge_dir = knowledge_dir
        self.patterns_path = knowledge_dir / 'patterns.json'
        self.refined_patterns_path = knowledge_dir / 'refined_patterns.json'
        
    def analyze_existing_patterns(
        self, 
        pattern_data: Dict[str, Any],
        component_patterns: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze and refine patterns"""
        try:
            refined_patterns = {}
            logger.info("Starting pattern refinement analysis...")
            
            for pattern_type, data in pattern_data.items():
                # Extract code from file
                code = ""
                if data.get('files'):
                    try:
                        with open(data['files'][0], 'r') as f:
                            code = f.read()
                    except Exception as e:
                        logger.error(f"Error reading file: {e}")
                        
                # Create pattern with proper string values
                pattern = CodePattern(
                    pattern_type=pattern_type,
                    code=code,
                    source_file=str(data.get('files', [''])[0]),  # Convert Path to string
                    frameworks=list(data.get('common_imports', [])),
                    usage_count=data.get('count', 0)
                )
                
                # Get component analysis data if available
                component_data = component_patterns.get(pattern_type, {}) if component_patterns else {}
                
                # Combine pattern detection with component analysis
                confidence = self._calculate_combined_confidence(
                    data,
                    component_data
                )
                
                logger.info(f"\nRefining pattern: {pattern_type}")
                
                # Collect all files using this pattern
                pattern_files = data.get('files', [])
                logger.debug(f"Found {len(pattern_files)} files for {pattern_type}")
                
                # Extract actual usage patterns
                usage_patterns = self._extract_usage_patterns(pattern_files, pattern_type)
                
                # Validate patterns
                confidence = self.validate_pattern(pattern_type, str(usage_patterns))
                logger.info(f"Pattern confidence: {confidence:.2f}")
                
                # Log detailed findings
                logger.debug(f"Detection terms: {usage_patterns['terms']}")
                logger.debug(f"Common imports: {usage_patterns['imports']}")
                logger.debug(f"Related components: {usage_patterns['components']}")
                
                # Record refined pattern
                refined_patterns[pattern_type] = {
                    "detection_terms": usage_patterns["terms"],
                    "common_imports": usage_patterns["imports"],
                    "related_components": usage_patterns["components"],
                    "frequency": data['count'],
                    "confidence": confidence,
                    "source_files": len(pattern_files),
                    "validation_status": "valid" if confidence >= 0.45 else "needs_review"
                }
                
                logger.info(f"Refined {pattern_type}: {len(usage_patterns['terms'])} terms found")
                
            # Save refined patterns
            self._save_refined_patterns(refined_patterns)
            
            # Log summary
            logger.info("\nPattern Refinement Summary:")
            for pattern_type, data in refined_patterns.items():
                logger.info(f"{pattern_type}:")
                logger.info(f"  - Terms: {len(data['detection_terms'])}")
                logger.info(f"  - Confidence: {data['confidence']:.2f}")
                logger.info(f"  - Status: {data['validation_status']}")
            
            return refined_patterns
            
        except Exception as e:
            logger.error(f"Error refining patterns: {e}")
            return {}
    
    def _extract_usage_patterns(self, files: List[Path], pattern_type: str) -> Dict[str, Set[str]]:
        """Extract actual usage patterns from files"""
        terms = set()
        imports = set()
        components = set()
        
        for file in files:
            try:
                content = file.read_text()
                
                # Extract imports
                imports.update(re.findall(r'import\s+(\w+)', content))
                
                # Extract gesture patterns
                if pattern_type == 'gestures':
                    # Basic gestures
                    terms.update(re.findall(r'\.gesture\(\s*(\w+Gesture)', content))
                    # Spatial gestures
                    terms.update(re.findall(r'(SpatialTapGesture|targetedToAnyEntity)', content))
                    # Gesture handlers
                    terms.update(re.findall(r'\.(onEnded|onChanged)\s*{', content))
                    # Custom gesture components
                    components.update(re.findall(r'class\s+\w+Gesture', content))
                
                # Extract pattern-specific terms
                terms.update(self._extract_pattern_terms(content, pattern_type))
                
            except Exception as e:
                logger.error(f"Error extracting patterns from {file}: {e}")
                
        return {
            "terms": terms,
            "imports": imports,
            "components": components
        }
    
    def _extract_pattern_terms(self, content: str, pattern_type: str) -> Set[str]:
        """Extract terms specific to a pattern type"""
        terms = set()
        
        if pattern_type == "animation":
            # Animation patterns
            terms.update(re.findall(r'(?:withAnimation|animation|transition|\.animate)', content))
            terms.update(re.findall(r'Animation[A-Z]\w+', content))  # AnimationPhase, etc.
            
        elif pattern_type == "3d_content":
            # 3D content patterns
            terms.update(re.findall(r'(?:Entity|Model3D|RealityView|Scene3D)', content))
            terms.update(re.findall(r'\.load\(["\'].*\.usd[z]?["\']', content))
            terms.update(re.findall(r'Material|Shader|Texture', content))
            
        elif pattern_type == "arkit":
            # ARKit patterns
            terms.update(re.findall(r'(?:ARKit|ARSession|ARConfiguration)', content))
            terms.update(re.findall(r'(?:anchor|AnchorEntity|WorldTracking)', content))
            terms.update(re.findall(r'SceneReconstruction|PlaneDetection', content))
            
        elif pattern_type == "spatial_audio":
            # Spatial audio patterns
            terms.update(re.findall(r'(?:SpatialAudio|AudioEngine|Sound3D)', content))
            terms.update(re.findall(r'\.playAudio|\.spatial\.audio', content))
            terms.update(re.findall(r'AudioComponent|SoundEffect', content))
            
        elif pattern_type == "immersive_spaces":
            # Immersive space patterns
            terms.update(re.findall(r'(?:ImmersiveSpace|WindowGroup)', content))
            terms.update(re.findall(r'\.immersive|\.fullspace', content))
            terms.update(re.findall(r'ImmersionStyle|SpaceStyle', content))
        
        elif pattern_type == "ui_components":
            # Look for SwiftUI view definitions
            terms.update(re.findall(r'(?:struct|class)\s+(\w+)(?::\s*View)', content))
            # Look for SwiftUI view types
            terms.update(re.findall(r'(?:Text|NavigationStack|RealityView|View)\b', content))
            # Look for custom views
            terms.update(re.findall(r'struct\s+(\w+View)\b', content))
        
        elif pattern_type == "scene_understanding":
            # Scene understanding patterns
            terms.update(re.findall(r'(?:SceneUnderstanding|SceneReconstruction)', content))
            terms.update(re.findall(r'(?:PlaneAnchor|MeshAnchor|PointCloud)', content))
            terms.update(re.findall(r'\.sceneReconstruction|\.planeDetection', content))
        
        elif pattern_type == "gestures":
            # Basic gesture types
            terms.update(re.findall(r'(?:TapGesture|DragGesture|LongPressGesture|RotateGesture|MagnifyGesture|SpatialTapGesture)\b', content))
            
            # Gesture modifiers and handlers
            terms.update(re.findall(r'\.gesture\(\s*\w+', content))
            terms.update(re.findall(r'\.(onEnded|onChanged|onMoved)\s*{', content))
            
            # Spatial targeting
            terms.update(re.findall(r'targetedToAnyEntity|targetedToEntity', content))
            
            # Custom gesture components
            terms.update(re.findall(r'class\s+(\w+Gesture)\b', content))
            
            # SwiftUI gesture state
            terms.update(re.findall(r'@GestureState\b', content))
            
            # Gesture state handling
            terms.update(re.findall(r'GestureState<[^>]+>', content))
            
            # Simultaneous and exclusive gestures
            terms.update(re.findall(r'\.simultaneously\(with:|\.exclusively\(before:', content))
        
        return terms
    
    def _calculate_confidence(self, usage_patterns: Dict[str, Set[str]]) -> float:
        """Calculate confidence score for pattern detection"""
        # Simple confidence calculation
        term_count = len(usage_patterns["terms"])
        import_count = len(usage_patterns["imports"])
        component_count = len(usage_patterns["components"])
        
        if term_count == 0:
            return 0.0
            
        # Adjust weights and thresholds
        term_score = min(1.0, term_count / 3)  # Max score at 3 terms (was 5)
        import_score = min(1.0, import_count / 2)  # Max score at 2 imports (was 3)
        component_score = min(1.0, component_count / 1)  # Max score at 1 component (was 2)
        
        # Combined weighted score with slightly higher weights
        return min(1.0, (term_score * 0.6 + import_score * 0.3 + component_score * 0.2))  # Total > 1.0 to ensure > 0.5
    
    def _save_refined_patterns(self, patterns: Dict[str, Any]):
        """Save refined patterns to file"""
        try:
            # Convert sets to lists for JSON serialization
            json_patterns = {}
            for pattern_type, data in patterns.items():
                json_patterns[pattern_type] = {
                    "detection_terms": list(data["detection_terms"]),
                    "common_imports": list(data["common_imports"]),
                    "related_components": list(data.get("related_components", [])),
                    "frequency": data["frequency"],
                    "confidence": data["confidence"],
                    "source_files": data["source_files"]
                }
            
            self.refined_patterns_path.write_text(
                json.dumps(json_patterns, indent=2)
            )
            logger.info(f"Saved refined patterns to {self.refined_patterns_path}")
        except Exception as e:
            logger.error(f"Error saving refined patterns: {e}") 
    
    def validate_pattern(self, pattern_type: str, content: str) -> float:
        """Validate a pattern match with confidence score"""
        validation_rules = {
            "animation": {
                "required": ["Animation", "animate"],
                "optional": ["transition", "withAnimation"],
                "imports": ["SwiftUI"]
            },
            "3d_content": {
                "required": ["Entity", "Model3D"],
                "optional": ["RealityView", "Scene3D"],
                "imports": ["RealityKit"]
            },
            "arkit": {
                "required": ["ARKit", "ARSession"],
                "optional": ["anchor", "WorldTracking"],
                "imports": ["ARKit"]
            },
            "scene_understanding": {
                "required": ["SceneUnderstanding", "Anchor"],
                "optional": ["PlaneDetection", "MeshAnchor"],
                "imports": ["ARKit", "RealityKit"]
            },
            "state_management": {
                "required": ["@State", "@Observable"],
                "optional": ["@Environment", "@Binding"],
                "imports": ["SwiftUI", "Observation"]
            },
            "lifecycle": {
                "required": ["onAppear", "task"],
                "optional": ["onDisappear", "onChange"],
                "imports": ["SwiftUI"]
            },
            "update_loops": {
                "required": ["RealityView", "update"],
                "optional": ["SystemsUpdater", "components"],
                "imports": ["RealityKit"]
            },
            "gestures": {
                "required": [
                    "gesture",
                    "TapGesture",
                    "DragGesture"
                ],
                "optional": [
                    "onEnded",
                    "onChanged",
                    "LongPressGesture",
                    "RotateGesture",
                    "MagnifyGesture",
                    "SpatialTapGesture",
                    "targetedToAnyEntity"
                ],
                "imports": ["SwiftUI"]
            }
        }
        
        if pattern_type not in validation_rules:
            return 0.5  # Default confidence
            
        rules = validation_rules[pattern_type]
        score = 0.0
        
        # Check required terms
        required_found = sum(1 for term in rules["required"] if term in content)
        if required_found > 0:
            score += 0.6 * (required_found / len(rules["required"]))
            
        # Check optional terms
        optional_found = sum(1 for term in rules["optional"] if term in content)
        if optional_found > 0:
            score += 0.3 * (optional_found / len(rules["optional"]))
            
        # Check imports
        imports_found = sum(1 for imp in rules["imports"] if f"import {imp}" in content)
        if imports_found > 0:
            score += 0.1 * (imports_found / len(rules["imports"]))
            
        return min(1.0, score)
    
    def _calculate_combined_confidence(
        self,
        pattern_data: Dict[str, Any],
        component_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score combining pattern and component analysis
        
        Args:
            pattern_data: Pattern detection data
            component_data: Component analysis data
            
        Returns:
            float: Confidence score between 0-1
        """
        base_confidence = 0.5  # Start with neutral confidence
        
        # Boost confidence based on:
        # 1. Number of examples
        if pattern_data.get('count', 0) > 5:
            base_confidence += 0.1
            
        # 2. Framework imports match expectations
        expected_imports = {
            'ui_components': {'SwiftUI'},
            '3d_content': {'RealityKit'},
            'animation': {'SwiftUI'},
            'arkit': {'ARKit'},
            'gestures': {'SwiftUI'},
            'spatial_audio': {'AVFoundation'}
        }
        
        pattern_type = pattern_data.get('pattern_type', '')
        if pattern_type in expected_imports:
            imports = set(pattern_data.get('common_imports', []))
            if expected_imports[pattern_type].issubset(imports):
                base_confidence += 0.1
                
        # 3. Component analysis validation
        if component_data:
            if component_data.get('validated', False):
                base_confidence += 0.2
                
        # Cap confidence between 0-1
        return min(1.0, max(0.0, base_confidence))