class VisionOSPromptTemplate:
    def generate_component_prompt(self, component: str, knowledge_base: VisionOSKnowledgeBase) -> str:
        """Generate an LLM prompt with context from knowledge base"""
        knowledge = knowledge_base.query_pattern(component)
        relationships = knowledge_base.get_component_relationship(component)
        
        return f"""
        Generate visionOS code using these validated patterns:
        
        Common Usage Patterns:
        {knowledge['common_patterns']}
        
        Related Components:
        {relationships['commonly_used_with']}
        
        Example Implementation:
        {knowledge['examples'][0]}  # First example
        
        Requirements:
        - Follow the pattern shown in the example
        - Use related components as shown in relationships
        - Maintain the same structure as sample code
        """ 