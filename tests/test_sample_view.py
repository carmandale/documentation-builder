from analyzers.llm_interface import LLMDocumentationInterface
from analyzers.project_analyzer import ProjectAnalyzer
import pytest
from typing import Dict

def test_cylinder_rotation_implementation():
    """Test our cylinder rotation implementation against scraped patterns"""
    
    # Initialize interface
    llm_interface = LLMDocumentationInterface()
    
    # Look for relevant patterns
    rotation_pattern = llm_interface.find_transform_pattern('rotation')
    animation_pattern = llm_interface.find_animation_pattern('ModelEntity')
    
    # Test requirements
    requirements = {
        'type': '3d_content',
        'frameworks': ['RealityKit', 'SwiftUI'],
        'concepts': ['rotation', 'animation']
    }
    
    # Read current implementation
    with open('SampleView.swift', 'r') as f:
        implementation = f.read()
    
    # Validate implementation
    validation_results = llm_interface.validate_implementation(
        implementation,
        requirements
    )
    
    print("Validation Results:", validation_results)
    
    return validation_results 

def validate_api_usage(implementation: str) -> Dict[str, bool]:
    """Validate API usage against documentation patterns"""
    llm_interface = LLMDocumentationInterface()
    project_analyzer = ProjectAnalyzer()
    
    # Analyze implementation
    api_patterns = project_analyzer.analyze_api_patterns(implementation)
    
    validations = {}
    
    # Validate EventSubscription usage
    if 'EventSubscription' in implementation:
        container_type = api_patterns['container_types'].get('EventSubscription')
        validations['event_subscription'] = llm_interface.verify_api_usage(
            'EventSubscription',
            {'container_type': container_type}
        )
    
    # Validate quaternion operations
    if 'simd_quatf' in implementation:
        quaternion_methods = api_patterns['method_usage'].get('quaternion', set())
        validations['quaternion_ops'] = llm_interface.verify_api_usage(
            'simd_quatf',
            {'methods': quaternion_methods}
        )
    
    return validations 