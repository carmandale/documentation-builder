from typing import Dict, Any
from core.knowledge_base import VisionOSKnowledgeBase
from core.prompt_templates import VisionOSPromptTemplate

class VisionOSCodeGenerator:
    def __init__(self):
        self.knowledge_base = VisionOSKnowledgeBase()
        self.prompt_template = VisionOSPromptTemplate()
        
    def generate_code(self, requirements: Dict[str, Any]) -> str:
        """Generate code based on requirements using knowledge base"""
        # 1. Identify required components
        components = self._identify_components(requirements)
        
        # 2. Get relevant knowledge
        knowledge = {
            comp: self.knowledge_base.query_pattern(comp)
            for comp in components
        }
        
        # 3. Generate prompt with context
        prompt = self._build_prompt(requirements, knowledge)
        
        # 4. Send to LLM with context
        return self._generate_with_context(prompt, knowledge) 