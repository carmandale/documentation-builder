from pathlib import Path
from typing import Dict, List, Optional
from models.base import CodePattern, ValidationTest
import json
import logging
import re

logger = logging.getLogger(__name__)

class LLMDocumentationInterface:
    """Interface for LLMs to query and use the documentation"""
    
    def __init__(self, extracted_dir: Path = Path("data/extracted")):
        self.extracted_dir = extracted_dir
        self.patterns = {}
        self.relationships = {}
        self.validation_results = {}
        self._load_extracted_data()
    
    def _load_extracted_data(self):
        """Load all extracted documentation into memory"""
        for file in self.extracted_dir.glob("*.json"):
            try:
                with open(file) as f:
                    data = json.load(f)
                    self._index_patterns(data.get('code_patterns', {}))
                    self._index_relationships(data.get('relationships', []))
            except Exception as e:
                logger.error(f"Error loading {file}: {str(e)}")
    
    def _index_patterns(self, patterns: Dict):
        """Index code patterns for quick lookup"""
        for pattern_id, pattern in patterns.items():
            # Create searchable index of pattern features
            key_features = {
                'type': pattern.get('pattern_type'),
                'frameworks': set(pattern.get('frameworks', [])),
                'concepts': set(pattern.get('related_concepts', []))
            }
            self.patterns[pattern_id] = {
                'data': pattern,
                'features': key_features
            }
    
    def find_pattern(self, requirements: Dict[str, any]) -> List[CodePattern]:
        """Find code patterns matching specific requirements"""
        matching_patterns = []
        
        for pattern_id, pattern_data in self.patterns.items():
            features = pattern_data['features']
            
            # Check each requirement
            matches = True
            for req_key, req_value in requirements.items():
                if req_key == 'type' and req_value != features['type']:
                    matches = False
                    break
                elif req_key == 'frameworks' and not set(req_value).issubset(features['frameworks']):
                    matches = False
                    break
                elif req_key == 'concepts' and not set(req_value).issubset(features['concepts']):
                    matches = False
                    break
            
            if matches:
                matching_patterns.append(pattern_data['data'])
        
        return matching_patterns
    
    def find_animation_pattern(self, entity_type: str = None) -> Optional[CodePattern]:
        """Find animation patterns for specific entity types"""
        requirements = {
            'type': 'animation',
            'frameworks': ['RealityKit']
        }
        if entity_type:
            requirements['concepts'] = [entity_type]
        
        patterns = self.find_pattern(requirements)
        return patterns[0] if patterns else None
    
    def find_transform_pattern(self, transform_type: str) -> Optional[CodePattern]:
        """Find transform patterns by type (rotation, position, scale)"""
        requirements = {
            'type': '3d_content',
            'concepts': [transform_type]
        }
        
        patterns = self.find_pattern(requirements)
        return patterns[0] if patterns else None
    
    def validate_implementation(self, code: str, requirements: Dict[str, any]) -> Dict[str, any]:
        """Validate code implementation against requirements"""
        patterns = self.find_pattern(requirements)
        if not patterns:
            return {'valid': False, 'reason': 'No matching patterns found'}
            
        validation_results = []
        for pattern in patterns:
            tests = pattern.get('validation_tests', [])
            for test in tests:
                # Compare implementation against pattern tests
                test_result = self._run_validation_test(code, test)
                validation_results.append(test_result)
        
        return {
            'valid': all(result['passed'] for result in validation_results),
            'results': validation_results
        }
    
    def _run_validation_test(self, code: str, test: ValidationTest) -> Dict[str, any]:
        """Run a single validation test"""
        # Basic pattern matching for now
        required_elements = test.prerequisites
        missing_elements = [elem for elem in required_elements if elem not in code]
        
        return {
            'passed': len(missing_elements) == 0,
            'missing': missing_elements,
            'test_id': test.pattern_id
        }
    
    def explain_pattern(self, pattern: CodePattern) -> Dict[str, any]:
        """Explain a code pattern in detail"""
        return {
            'type': pattern.pattern_type,
            'frameworks': pattern.frameworks,
            'code': pattern.code,
            'prerequisites': pattern.prerequisites,
            'related_concepts': pattern.related_concepts,
            'validation_examples': pattern.validation_examples
        }
    
    def suggest_improvements(self, code: str, pattern: CodePattern) -> Dict[str, any]:
        """Compare code against a pattern and suggest improvements"""
        differences = []
        missing_concepts = []
        
        # Check for required frameworks
        for framework in pattern.frameworks:
            if framework not in code:
                differences.append(f"Missing framework: {framework}")
        
        # Check for prerequisites
        for prereq in pattern.prerequisites:
            if prereq not in code:
                missing_concepts.append(prereq)
        
        return {
            'differences': differences,
            'missing_concepts': missing_concepts,
            'pattern_code': pattern.code
        }
    
    def verify_api_usage(self, api_name: str, usage_context: Dict[str, any]) -> bool:
        """Verify API usage against documented patterns"""
        # Check container types
        if 'container_type' in usage_context:
            actual_usage = self._find_api_usage(api_name)
            if actual_usage:
                if usage_context['container_type'] != actual_usage['container_type']:
                    logger.warning(
                        f"Using {usage_context['container_type']} for {api_name} "
                        f"but documentation uses {actual_usage['container_type']}"
                    )
                    return False
        return True
    
    def _find_api_usage(self, api_name: str) -> Optional[Dict[str, any]]:
        """Find how an API is used in documentation"""
        for pattern in self.patterns.values():
            if api_name in pattern['data']['code']:
                return self._analyze_api_usage(pattern['data']['code'], api_name)
        return None
    
    def _analyze_api_usage(self, code: str, api_name: str) -> Dict[str, any]:
        """Analyze how an API is used in code"""
        usage = {
            'container_type': None,
            'method_calls': set(),
            'common_patterns': []
        }
        
        # Detect container types
        container_match = re.search(
            rf'(var|let)\s+\w+\s*:\s*(\[|\{{).*{api_name}',
            code
        )
        if container_match:
            usage['container_type'] = 'Array' if container_match.group(2) == '[' else 'Set'
        
        # Find method calls
        method_pattern = rf'{api_name}\.\w+'
        usage['method_calls'].update(re.findall(method_pattern, code))
        
        return usage