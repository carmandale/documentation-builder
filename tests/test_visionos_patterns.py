import unittest
from patterns.visionos_patterns import (
    get_pattern,
    get_patterns_by_category,
    get_related_patterns,
    VisionOSPattern
)

class TestVisionOSPatterns(unittest.TestCase):
    def test_get_pattern(self):
        # Test getting existing pattern
        pattern = get_pattern("basic_immersive_space")
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.name, "Basic Immersive Space")
        self.assertEqual(pattern.category, "immersive_space")
        
        # Test getting non-existent pattern
        pattern = get_pattern("non_existent_pattern")
        self.assertIsNone(pattern)
    
    def test_get_patterns_by_category(self):
        # Test getting immersive space patterns
        patterns = get_patterns_by_category("immersive_space")
        self.assertEqual(len(patterns), 2)  # basic and shared space
        self.assertTrue(all(p.category == "immersive_space" for p in patterns))
        
        # Test getting volumetric patterns
        patterns = get_patterns_by_category("volumetric")
        self.assertEqual(len(patterns), 1)  # basic volumetric
        self.assertTrue(all(p.category == "volumetric" for p in patterns))
        
        # Test getting non-existent category
        patterns = get_patterns_by_category("non_existent")
        self.assertEqual(len(patterns), 0)
    
    def test_get_related_patterns(self):
        # Test getting related patterns
        patterns = get_related_patterns("basic_immersive_space")
        pattern_names = [p.name for p in patterns if p is not None]
        self.assertTrue(
            any("Hand Tracking" in name for name in pattern_names),
            f"Expected to find Hand Tracking pattern in {pattern_names}"
        )
        
        # Test getting related patterns for non-existent pattern
        patterns = get_related_patterns("non_existent_pattern")
        self.assertEqual(len(patterns), 0)
    
    def test_pattern_validation(self):
        # Test basic immersive space pattern
        pattern = get_pattern("basic_immersive_space")
        self.assertIn("SwiftUI", pattern.required_imports)
        self.assertIn("RealityKit", pattern.required_imports)
        self.assertIn("immersiveSpace", pattern.required_permissions)
        self.assertTrue(len(pattern.best_practices) > 0)
        self.assertTrue(len(pattern.common_pitfalls) > 0)
        
        # Test hand tracking pattern
        pattern = get_pattern("basic_hand_tracking")
        self.assertIn("ARKit", pattern.required_imports)
        self.assertIn("handTracking", pattern.required_permissions)
        self.assertTrue(any("privacy" in bp.lower() for bp in pattern.best_practices))

if __name__ == '__main__':
    unittest.main()
