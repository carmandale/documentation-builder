import unittest
from pathlib import Path
from analyzers.component_analyzer_adapter import ComponentAnalyzerAdapter
from core.enhanced_knowledge_base import EnhancedVisionOSKnowledgeBase

class TestComponentAnalyzerAdapter(unittest.TestCase):
    def setUp(self):
        self.knowledge_base = EnhancedVisionOSKnowledgeBase()
        self.adapter = ComponentAnalyzerAdapter(self.knowledge_base)
        
    def tearDown(self):
        pass
    
    def test_analyze_file(self):
        test_content = """
        import SwiftUI
        import RealityKit
        
        struct ImmersiveView: View {
            var body: some View {
                RealityView { content in
                    // Add 3D content
                }
                .gesture(TapGesture().targetedToAnyEntity().onEnded { _ in
                    // Handle tap
                })
            }
        }
        """
        
        # Create a temporary test file
        test_file = Path("test_component.swift")
        with open(test_file, "w") as f:
            f.write(test_content)
            
        try:
            components = self.adapter.analyze_file(test_file)
            self.assertTrue(len(components) > 0)
            
            # Check View component
            view_component = next((c for c in components if c.name == "ImmersiveView"), None)
            self.assertIsNotNone(view_component)
            self.assertEqual(view_component.name, "ImmersiveView")
            self.assertEqual(view_component.type, "SwiftUI")
            
            # Check RealityView component
            reality_view = next((c for c in components if c.name == "RealityView"), None)
            self.assertIsNotNone(reality_view)
            self.assertEqual(reality_view.type, "RealityKit")
            
            # Check imports
            self.assertIn("SwiftUI", view_component.required_imports)
            self.assertIn("RealityKit", view_component.required_imports)
            
            # Check related components
            self.assertIn("RealityView", view_component.related_components)
        finally:
            # Clean up
            test_file.unlink()
    
    def test_component_type_detection(self):
        # Test SwiftUI component
        swiftui_type = self.adapter._determine_component_type(
            "import SwiftUI\nstruct TestView: View {}", "TestView"
        )
        self.assertEqual(swiftui_type, "SwiftUI")
        
        # Test RealityKit component
        realitykit_type = self.adapter._determine_component_type(
            "import RealityKit\nlet entity = ModelEntity()", "ModelEntity"
        )
        self.assertEqual(realitykit_type, "RealityKit")
    
    def test_permission_extraction(self):
        test_content = """
        struct TestView: View {
            @Environment(\\.openImmersiveSpace) var openImmersiveSpace
            @Environment(\\.handTracking) var handTracking
            
            var body: some View {
                RealityView { content in
                    content.handTrackingSystem?.isEnabled = true
                }
                .handTracking(.continuous)
                .privacyInfo("Hand tracking used for interaction")
            }
        }
        """
        patterns = []  # No patterns needed for this test
        permissions = self.adapter._extract_permissions(test_content, patterns)
        self.assertIn("handTracking", permissions)
        self.assertIn("immersiveSpace", permissions)
    
    def test_constraint_extraction(self):
        test_content = """
        if #available(visionOS 1.0, *) {
            VisionProView()
        }
        """
        constraints = self.adapter._extract_constraints(test_content, "TestComponent")
        
        self.assertTrue(len(constraints) > 0)
        version_constraint = next((c for c in constraints if c['type'] == 'version'), None)
        self.assertIsNotNone(version_constraint)
        self.assertEqual(version_constraint['min_version'], "1.0")

if __name__ == '__main__':
    unittest.main()
