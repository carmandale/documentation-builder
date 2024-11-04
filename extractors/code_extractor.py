from bs4 import BeautifulSoup, Tag
from models.base import CodeBlock
from typing import List, Optional, Set
import logging
import re

logger = logging.getLogger(__name__)

class CodeBlockExtractor:
    """Extracts code blocks from documentation pages"""
    
    # Common VisionOS frameworks
    KNOWN_FRAMEWORKS = {
        'RealityKit', 'SwiftUI', 'ARKit', 'Metal', 
        'RealityFoundation', 'WindowKit', 'ImmersiveSpace'
    }
    
    @staticmethod
    def extract_code_blocks(soup: BeautifulSoup) -> List[CodeBlock]:
        """Extract all code blocks from the page"""
        code_blocks = []
        
        # Find all code listings
        listings = soup.find_all('div', class_='code-listing')
        
        for listing in listings:
            try:
                code_block = CodeBlockExtractor._process_code_block(listing)
                if code_block:
                    code_blocks.append(code_block)
            except Exception as e:
                logger.error(f"Error processing code block: {str(e)}")
                
        return code_blocks
    
    @staticmethod
    def _process_code_block(block: Tag) -> Optional[CodeBlock]:
        """Process a single code block"""
        # Get the code content
        code_content = block.find('code')
        if not code_content:
            return None
            
        # Get the full code text
        code_text = code_content.get_text(strip=True)
        
        # Look for description in previous siblings
        desc = block.find_previous(['p', 'div'], class_='description')
        description = desc.get_text(strip=True) if desc else None
        
        # Get language (defaulting to swift)
        language = block.get('data-syntax', 'swift')
        
        # Detect frameworks used
        frameworks = CodeBlockExtractor._detect_frameworks(code_text)
        
        # Determine code type
        code_type = CodeBlockExtractor._determine_code_type(code_text, frameworks)
        
        return CodeBlock(
            code=code_text,
            description=description,
            language=language,
            preview=code_text[:200],
            frameworks=list(frameworks),
            type=code_type
        )
    
    @staticmethod
    def _detect_frameworks(code: str) -> Set[str]:
        """Detect frameworks used in the code"""
        frameworks = set()
        
        # Look for import statements
        import_pattern = r'import\s+(\w+)'
        imports = re.findall(import_pattern, code)
        frameworks.update(fw for fw in imports if fw in CodeBlockExtractor.KNOWN_FRAMEWORKS)
        
        # Look for framework usage in code
        for framework in CodeBlockExtractor.KNOWN_FRAMEWORKS:
            if framework in code:
                frameworks.add(framework)
        
        # Special cases
        if 'RealityView' in code or 'ModelEntity' in code:
            frameworks.add('RealityKit')
        if 'View' in code or 'WindowGroup' in code:
            frameworks.add('SwiftUI')
        
        return frameworks
    
    @staticmethod
    def _determine_code_type(code: str, frameworks: Set[str]) -> str:
        """Determine the type of code example"""
        code_lower = code.lower()
        
        # UI Components
        if 'struct' in code_lower and 'view' in code_lower:
            return 'ui_component'
            
        # 3D Content
        if 'realitykit' in code_lower or 'entity' in code_lower or 'Model3D' in code_lower:
            return '3d_content'
            
        # Animation
        if 'animate' in code_lower or 'transition' in code_lower:
            return 'animation'
            
        # App Structure
        if '@main' in code or 'WindowGroup' in code:
            return 'app_structure'
            
        # Event Handling
        if 'gesture' in code_lower or 'event' in code_lower or 'action' in code_lower:
            return 'event_handling'
            
        # Immersive Space
        if 'ImmersiveSpace' in code or 'openImmersiveSpace' in code:
            return 'immersive_space'
        
        return 'other'