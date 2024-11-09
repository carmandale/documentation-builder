import pytest
from pathlib import Path
from analyzers.pattern_refiner import PatternRefiner
from extractors.code_extractor import CodeBlockExtractor
from utils.logging import logger
import logging

# Test data with real project structure
SAMPLE_PATTERN_DATA = {
    "ui_components": {
        "count": 2,
        "files": [
            "tests/data/sample1.swift",
            "tests/data/sample2.swift"
        ],
        "examples": [],
        "validated": False
    }
}

@pytest.fixture
def setup_test_files(tmp_path):
    # Create test data directory
    test_data = tmp_path / "tests" / "data"
    test_data.mkdir(parents=True)
    
    # Sample 1 - Simple UI Component
    sample1 = test_data / "sample1.swift"
    sample1.write_text("""
    import SwiftUI
    
    struct ContentView: View {
        var body: some View {
            Text("Hello")
        }
    }
    """)
    
    # Sample 2 - More Complex UI
    sample2 = test_data / "sample2.swift"
    sample2.write_text("""
    import SwiftUI
    import RealityKit
    
    struct MainView: View {
        var body: some View {
            NavigationStack {
                RealityView { content in
                    // 3D content setup
                }
            }
        }
    }
    """)
    
    return tmp_path

def test_pattern_refinement(setup_test_files, caplog):
    """Test pattern refinement with logging"""
    caplog.set_level(logging.DEBUG)
    
    # Arrange
    pattern_data = SAMPLE_PATTERN_DATA.copy()
    pattern_data["ui_components"]["files"] = [
        str(setup_test_files / "tests" / "data" / "sample1.swift"),
        str(setup_test_files / "tests" / "data" / "sample2.swift")
    ]
    
    refiner = PatternRefiner(knowledge_dir=setup_test_files)
    
    # Act
    refined_patterns = refiner.analyze_existing_patterns(pattern_data)
    
    # Assert
    assert refined_patterns["ui_components"]["detection_terms"] == {
        "ContentView", "MainView", "NavigationStack", "RealityView", "Text", "View"
    }
    assert refined_patterns["ui_components"]["common_imports"] == {"SwiftUI", "RealityKit"}
    assert abs(refined_patterns["ui_components"]["confidence"] - 0.5) < 0.0001
    
    # Check logs
    assert "Refining pattern: ui_components" in caplog.text
    assert "Found 2 files for ui_components" in caplog.text
    assert "Refined ui_components: 6 terms found" in caplog.text

def test_pattern_validation(setup_test_files, caplog):
    """Test pattern validation with different pattern types"""
    caplog.set_level(logging.DEBUG)
    
    # Test data for multiple patterns
    pattern_data = {
        "ui_components": {
            "count": 1,
            "files": [str(setup_test_files / "tests" / "data" / "sample1.swift")],
            "examples": [],
            "validated": False
        },
        "animation": {
            "count": 1,
            "files": [str(setup_test_files / "tests" / "data" / "animation.swift")],
            "examples": [],
            "validated": False
        }
    }
    
    # Create animation test file
    animation_file = setup_test_files / "tests" / "data" / "animation.swift"
    animation_file.write_text("""
    import SwiftUI
    
    struct AnimatedView: View {
        @State private var scale = 1.0
        
        var body: some View {
            Circle()
                .scaleEffect(scale)
                .animation(.spring(), value: scale)
                .onTapGesture {
                    withAnimation {
                        scale *= 1.5
                    }
                }
        }
    }
    """)
    
    refiner = PatternRefiner(knowledge_dir=setup_test_files)
    refined_patterns = refiner.analyze_existing_patterns(pattern_data)
    
    # Check UI Components
    assert refined_patterns["ui_components"]["validation_status"] == "valid"
    assert abs(refined_patterns["ui_components"]["confidence"] - 0.5) < 0.0001
    
    # Check Animation
    assert "animation" in refined_patterns
    assert "withAnimation" in refined_patterns["animation"]["detection_terms"]
    assert abs(refined_patterns["animation"]["confidence"] - 0.45) < 0.0001
    
    # Check logs
    assert "Pattern Refinement Summary:" in caplog.text
    assert "Refining pattern: ui_components" in caplog.text
    assert "Refining pattern: animation" in caplog.text

def test_scene_understanding_pattern(setup_test_files, caplog):
    """Test scene understanding pattern with real sample data"""
    # Use real sample code from Apple's samples
    scene_file = setup_test_files / "tests" / "data" / "scene_understanding.swift"
    scene_file.write_text("""
    import ARKit
    import RealityKit
    
    class SceneAnalyzer: ObservableObject {
        let session = ARSession()
        
        func setupSceneUnderstanding() {
            let config = ARWorldTrackingConfiguration()
            config.sceneReconstruction = .mesh
            config.planeDetection = [.horizontal, .vertical]
            
            session.run(config)
        }
        
        func handleAnchor(_ anchor: ARAnchor) {
            switch anchor {
            case let planeAnchor as ARPlaneAnchor:
                // Handle plane detection
                break
            case let meshAnchor as ARMeshAnchor:
                // Handle mesh anchor
                break
            default:
                break
            }
        }
    }
    """)
    
    pattern_data = {
        "scene_understanding": {
            "count": 1,
            "files": [str(scene_file)],
            "examples": [],
            "validated": False
        }
    }
    
    refiner = PatternRefiner(knowledge_dir=setup_test_files)
    refined_patterns = refiner.analyze_existing_patterns(pattern_data)
    
    # Assert pattern detection
    assert "scene_understanding" in refined_patterns
    assert "SceneUnderstanding" in refined_patterns["scene_understanding"]["detection_terms"]
    assert "planeDetection" in refined_patterns["scene_understanding"]["detection_terms"]
    assert {"ARKit", "RealityKit"} == refined_patterns["scene_understanding"]["common_imports"]
    assert refined_patterns["scene_understanding"]["confidence"] >= 0.45