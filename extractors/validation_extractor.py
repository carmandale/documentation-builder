from models.base import ValidationTest, CodePattern
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ValidationExtractor:
    """Generates validation tests from code patterns"""
    
    def generate_tests(self, code_patterns: Dict[str, CodePattern]) -> List[ValidationTest]:
        """Generate validation tests for code patterns"""
        tests = []
        
        for pattern_id, pattern in code_patterns.items():
            # Generate test based on pattern type
            if pattern.pattern_type == "3d_content":
                tests.extend(self._generate_3d_tests(pattern_id, pattern))
            elif pattern.pattern_type == "animation":
                tests.extend(self._generate_animation_tests(pattern_id, pattern))
            elif pattern.pattern_type == "ui_component":
                tests.extend(self._generate_ui_tests(pattern_id, pattern))
        
        return tests
    
    def _generate_3d_tests(self, pattern_id: str, pattern: CodePattern) -> List[ValidationTest]:
        """Generate tests for 3D content patterns"""
        tests = []
        
        # Basic existence test
        tests.append(ValidationTest(
            pattern_id=pattern_id,
            test_code=f"// Test {pattern_id} exists\nlet entity = content.entities.first\nXCTAssertNotNil(entity)",
            expected_behavior="Entity should exist in content",
            frameworks=pattern.frameworks
        ))
        
        # Transform test if relevant
        if "transform" in pattern.code.lower():
            tests.append(ValidationTest(
                pattern_id=pattern_id,
                test_code=f"// Test {pattern_id} transform\nlet transform = entity.transform\n// Verify transform values",
                expected_behavior="Entity should have expected transform values",
                frameworks=pattern.frameworks
            ))
        
        return tests
    
    def _generate_animation_tests(self, pattern_id: str, pattern: CodePattern) -> List[ValidationTest]:
        """Generate tests for animation patterns"""
        tests = []
        
        # Animation setup test
        tests.append(ValidationTest(
            pattern_id=pattern_id,
            test_code=f"// Test {pattern_id} animation setup\n// Verify animation configuration",
            expected_behavior="Animation should be properly configured",
            frameworks=pattern.frameworks
        ))
        
        return tests
    
    def _generate_ui_tests(self, pattern_id: str, pattern: CodePattern) -> List[ValidationTest]:
        """Generate tests for UI component patterns"""
        tests = []
        
        # Basic UI test
        tests.append(ValidationTest(
            pattern_id=pattern_id,
            test_code=f"// Test {pattern_id} UI setup\n// Verify UI component structure",
            expected_behavior="UI component should be properly structured",
            frameworks=pattern.frameworks
        ))
        
        return tests 