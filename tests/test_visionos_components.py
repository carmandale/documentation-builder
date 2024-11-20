import unittest
import os
from pathlib import Path
from analyzers.component_analyzer_adapter import ComponentAnalyzerAdapter

class TestVisionOSComponents(unittest.TestCase):
    def setUp(self):
        self.adapter = ComponentAnalyzerAdapter()
        self.fixtures_dir = Path(__file__).parent / "fixtures"
    
    def test_immersive_space_analysis(self):
        file_path = self.fixtures_dir / "ImmersiveSpaceView.swift"
        components = self.adapter.analyze_file(str(file_path))
        
        # Verify immersive space component
        space_view = next((c for c in components if c.name == "ImmersiveSpaceView"), None)
        self.assertIsNotNone(space_view)
        self.assertEqual(space_view.type, "SwiftUI")
        
        # Check required imports
        self.assertIn("RealityKit", space_view.required_imports)
        self.assertIn("RealityKitContent", space_view.required_imports)
        
        # Check permissions and features
        self.assertIn("immersiveSpace", space_view.required_permissions)
        self.assertTrue(any("gesture" in f for f in space_view.features))
    
    def test_volumetric_analysis(self):
        file_path = self.fixtures_dir / "VolumetricView.swift"
        components = self.adapter.analyze_file(str(file_path))
        
        # Verify volumetric component
        vol_view = next((c for c in components if c.name == "VolumetricView"), None)
        self.assertIsNotNone(vol_view)
        
        # Check features
        self.assertTrue(any("volumetric" in f for f in vol_view.features))
        self.assertTrue(any("haptic" in f for f in vol_view.features))
    
    def test_hand_tracking_analysis(self):
        file_path = self.fixtures_dir / "HandTrackingView.swift"
        components = self.adapter.analyze_file(str(file_path))
        
        # Verify hand tracking component
        hand_view = next((c for c in components if c.name == "HandTrackingView"), None)
        self.assertIsNotNone(hand_view)
        
        # Check permissions and features
        self.assertIn("handTracking", hand_view.required_permissions)
        self.assertTrue(any("privacy" in f for f in hand_view.features))
        
if __name__ == '__main__':
    unittest.main()
