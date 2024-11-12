from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from core.xcode_manager import XcodeProjectManager
from core.knowledge_base import VisionOSKnowledgeBase
import json
import re

class LLMSession:
    def __init__(self, project_name: str, xcode_manager: XcodeProjectManager):
        self.project_name = project_name
        self.xcode_manager = xcode_manager
        self.knowledge_base = VisionOSKnowledgeBase()
        self.project_dir = Path("projects") / project_name
        self.conversation_file = self.project_dir / "conversations" / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.context = {}  # Store project context and history
        
    async def process_command(self, command: str):
        """Process user command through LLM"""
        try:
            # Log conversation
            self._log_conversation("user", command)
            
            # Process command and generate response
            response = await self._generate_response(command)
            
            # Validate any generated code
            if "CREATE_FILE:" in response or "EDIT_FILE:" in response:
                validation_result = self._validate_code(response)
                if not validation_result['valid']:
                    self._log_conversation("system", f"Validation failed: {validation_result['reasons']}")
                    return f"Code generation failed validation: {validation_result['reasons']}"
            
            # Log response
            self._log_conversation("assistant", response)
            
            # Handle file operations
            if "CREATE_FILE:" in response:
                self._handle_file_creation(response)
            elif "EDIT_FILE:" in response:
                self._handle_file_edit(response)
                
            return response
            
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self._log_conversation("error", error_msg)
            raise
            
    def _validate_code(self, response: str) -> Dict[str, Any]:
        """Validate generated code against our knowledge base"""
        # Extract code content
        code = response.split("\n", 1)[1] if "\n" in response else response
        
        result = {
            'valid': True,
            'reasons': [],
            'patterns_found': [],
            'missing_patterns': []
        }
        
        # Check basic structure
        if not self._check_basic_structure(code):
            result['valid'] = False
            result['reasons'].append("Missing basic SwiftUI view structure")
            
        # Check imports
        if not self._check_required_imports(code):
            result['valid'] = False
            result['reasons'].append("Missing required imports")
            
        # Check for visionOS patterns
        patterns = self._check_patterns(code)
        result['patterns_found'] = patterns['found']
        result['missing_patterns'] = patterns['missing']
        
        if patterns['missing']:
            result['valid'] = False
            result['reasons'].append(f"Missing required patterns: {', '.join(patterns['missing'])}")
            
        return result
        
    def _check_basic_structure(self, code: str) -> bool:
        """Check basic SwiftUI view structure"""
        required_patterns = [
            r'struct\s+\w+\s*:\s*View\s*{',
            r'var\s+body\s*:\s*some\s+View\s*{'
        ]
        return all(re.search(pattern, code) for pattern in required_patterns)
        
    def _check_required_imports(self, code: str) -> bool:
        """Check for required imports"""
        required_imports = {'SwiftUI'}
        found_imports = set(re.findall(r'import\s+(\w+)', code))
        return required_imports.issubset(found_imports)
        
    def _check_patterns(self, code: str) -> Dict[str, list]:
        """Check for visionOS patterns"""
        # Get patterns from knowledge base
        known_patterns = self.knowledge_base.query_pattern('ui_components')
        
        result = {
            'found': [],
            'missing': []
        }
        
        # Check each pattern
        for pattern in known_patterns.get('required_patterns', []):
            if re.search(pattern['regex'], code):
                result['found'].append(pattern['name'])
            else:
                result['missing'].append(pattern['name'])
                
        return result
        
    async def _generate_response(self, command: str) -> str:
        """Generate response using knowledge base and patterns"""
        # 1. Build context from our knowledge base
        context = self._build_knowledge_context()
        
        # 2. Define framework usage rules based on our analyzed patterns
        framework_rules = {
            "ARKit": {
                "required_imports": ["ARKit", "RealityKit"],
                "valid_patterns": self.knowledge_base.get_validated_patterns("arkit"),
                "invalid_patterns": self.knowledge_base.get_invalid_patterns("arkit"),
                "usage_context": "visionOS"  # vs "iOS"
            },
            "SwiftUI": {
                "required_patterns": self.knowledge_base.get_validated_patterns("ui_components"),
                "spatial_patterns": self.knowledge_base.get_validated_patterns("spatial_ui")
            },
            # Other frameworks...
        }
        
        # 3. Validate against knowledge base first
        if "Create" in command or "Edit" in command:
            validated_patterns = self._validate_against_knowledge(command)
            if not validated_patterns['valid']:
                return f"Cannot generate code: {validated_patterns['reason']}"
        
        # 4. Generate with strict knowledge base context
        response = await self._generate_with_knowledge(command, context, framework_rules)
        
        # 5. Validate output
        if "CREATE_FILE:" in response or "EDIT_FILE:" in response:
            validation = self._validate_code_against_knowledge(response)
            if not validation['valid']:
                return f"Generated code failed validation: {validation['reasons']}"
        
        return response

    def _build_knowledge_context(self) -> Dict[str, Any]:
        """Build context strictly from our knowledge base"""
        return {
            "patterns": {
                "validated": self.knowledge_base.get_all_validated_patterns(),
                "examples": self.knowledge_base.get_validated_examples(),
                "relationships": self.knowledge_base.get_pattern_relationships()
            },
            "frameworks": {
                "usage": self.knowledge_base.get_framework_usage_patterns(),
                "relationships": self.knowledge_base.get_framework_relationships()
            },
            "rules": {
                "must_use_knowledge_base": True,
                "validate_framework_usage": True,
                "check_platform_specifics": True
            }
        }

    def _validate_against_knowledge(self, command: str) -> Dict[str, Any]:
        """Validate command against our knowledge base"""
        result = {
            'valid': True,
            'reason': None,
            'patterns': []
        }

        # Check if we have validated patterns for this type of request
        patterns = self.knowledge_base.find_relevant_patterns(command)
        if not patterns:
            result['valid'] = False
            result['reason'] = "No validated patterns found for this request"
            return result

        # Validate framework usage if mentioned
        frameworks = self._extract_frameworks(command)
        for framework in frameworks:
            framework_validation = self.knowledge_base.validate_framework_usage(
                framework, 
                platform="visionOS"
            )
            if not framework_validation['valid']:
                result['valid'] = False
                result['reason'] = f"Invalid {framework} usage: {framework_validation['reason']}"
                return result

        return result