import pytest
from pathlib import Path
from analyzers.component_analyzer import ComponentAnalyzer
import logging

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def component_analyzer():
    return ComponentAnalyzer()

@pytest.fixture
def sample_swift_files(tmp_path):
    # Create test directory structure
    test_files = {
        "ui_test.swift": """
        import SwiftUI
        
        struct ContentView: View {
            @State private var count = 0
            
            var body: some View {
                NavigationStack {
                    Button("Count: \\(count)") {
                        count += 1
                    }
                }
            }
        }
        """,
        
        "reality_test.swift": """
        import RealityKit
        
        class CustomEntity: Entity {
            required init() {
                super.init()
                let model = ModelComponent(mesh: .generateBox(size: 0.1))
                self.components[ModelComponent.self] = model
            }
        }
        """,
        
        "state_test.swift": """
        import SwiftUI
        import RealityKit
        
        @Observable class AppState {
            var selectedEntity: Entity?
            var isAnimating: Bool = false
        }
        """
    }
    
    # Create the files
    for filename, content in test_files.items():
        test_file = tmp_path / filename
        test_file.write_text(content)
    
    return tmp_path

def test_analyze_samples(component_analyzer, sample_swift_files):
    """Test basic sample analysis"""
    results = component_analyzer.analyze_samples(sample_swift_files)
    
    # Check structure
    assert results
    assert 'components' in results
    assert 'imports' in results
    assert 'relationships' in results
    
    # Check UI patterns
    components = results['components']
    assert 'ui_navigation' in components
    assert 'NavigationStack' in components['ui_navigation']
    
    # Check state patterns
    assert 'state_property_wrappers' in components
    assert '@State' in components['state_property_wrappers']
    
    # Check imports
    imports = results['imports']
    assert 'SwiftUI' in set().union(*imports.values())
    assert 'RealityKit' in set().union(*imports.values())

def test_relationship_tracking(component_analyzer, sample_swift_files):
    """Test relationship detection"""
    results = component_analyzer.analyze_samples(sample_swift_files)
    relationships = results['relationships']
    
    # Check framework relationships
    assert any('SwiftUI' in imp and 'RealityKit' in imp 
              for imp in results['imports'].values())
    
    # Check state management
    assert any('@State' in comp 
              for comp in results['components'].values())

def test_error_handling(component_analyzer):
    """Test error handling with invalid input"""
    results = component_analyzer.analyze_samples(Path('nonexistent_dir'))
    
    # Check empty structure
    assert all(not values for values in results['components'].values())
    assert all(not values for values in results['imports'].values())
    assert all(not values for values in results['relationships'].values())