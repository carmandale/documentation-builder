from bs4 import Tag
from typing import List, Optional
from datetime import datetime, UTC
from models.base import CodeExample, DocumentationEntry
from utils.logging import logger

class BaseExtractor:
    def extract(self, content: Tag) -> Optional[DocumentationEntry]:
        """Extract core documentation content"""
        try:
            # Convert string content to BeautifulSoup if needed
            if isinstance(content, str):
                content = BeautifulSoup(content, 'html.parser')
            
            title = self._extract_title(content)
            if not title:
                return None

            return DocumentationEntry(
                title=title,
                description=self._extract_description(content),
                url=self._extract_url(content),
                examples=self._extract_code_examples(content),
                related_topics=self._extract_related_topics(content),
                prerequisites=self._extract_prerequisites(content),
                scraped_at=datetime.now(UTC)
            )
        except Exception as e:
            logger.error(f"Extraction error: {str(e)}")
            return None

    def _extract_title(self, content: Tag) -> Optional[str]:
        """Extract title from Apple's actual documentation structure"""
        # Try documentation hero title first
        title_elem = content.find('div', class_='documentation-title')
        if title_elem and (h1 := title_elem.find('h1')):
            return h1.get_text(strip=True)
        
        # Fallback to any h1
        h1 = content.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return None

    def _extract_description(self, content: Tag) -> str:
        """Extract description from Apple's actual documentation structure"""
        # Try abstract section first
        abstract = content.find('div', class_='abstract')
        if abstract and (p := abstract.find('p')):
            return p.get_text(strip=True)
        
        return ""

    def _extract_code_examples(self, content: Tag) -> List[CodeExample]:
        """Extract code examples from Apple's actual documentation structure"""
        examples = []
        code_blocks = content.find_all('div', class_='code-listing')
        
        for block in code_blocks:
            # Get code content from pre > code tag
            code_elem = block.find('code')
            if not code_elem:
                continue
                
            code = code_elem.get_text(strip=True)
            
            # Get description from preceding paragraph
            description = ""
            prev_elem = block.find_previous('p')
            if prev_elem:
                description = prev_elem.get_text(strip=True)

            # Determine frameworks used
            frameworks = []
            if 'SwiftUI' in code:
                frameworks.append('SwiftUI')
            if 'RealityKit' in code or 'ModelEntity' in code:
                frameworks.append('RealityKit')

            example = CodeExample(
                code=code,
                description=description,
                type=self._determine_code_type(code),
                frameworks=frameworks
            )
            examples.append(example)
        
        return examples

    def _extract_related_topics(self, content: Tag) -> List[str]:
        """Extract related topics from Apple's actual documentation structure"""
        topics = []
        
        # Look for "See Also" or similar sections
        related_section = content.find(['h2', 'h3'], 
            string=lambda x: x and any(s in x.lower() for s in ['see also', 'related', 'see more']))
        
        if related_section:
            # Find all links in the section
            links = related_section.find_next(['ul', 'div']).find_all('a')
            topics = [link.get_text(strip=True) for link in links]
        
        return topics

    def _extract_prerequisites(self, content: Tag) -> List[str]:
        """Extract prerequisites from Apple's actual documentation structure"""
        prereqs = []
        
        # Look for prerequisites section
        prereq_section = content.find(['h2', 'h3'], 
            string=lambda x: x and any(s in x.lower() for s in ['prerequisites', 'requirements']))
        
        if prereq_section:
            # Find list items in the section
            prereq_list = prereq_section.find_next('ul')
            if prereq_list:
                prereqs = [li.get_text(strip=True) for li in prereq_list.find_all('li')]
        
        return prereqs

    def _extract_url(self, content: Tag) -> str:
        """Extract URL from content or return default"""
        # Try to find canonical URL
        canonical = content.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            return canonical['href']
        
        # Return a default URL structure
        return "https://developer.apple.com/documentation/visionos"

    def _determine_code_type(self, code: str) -> str:
        """Determine the type of code example"""
        code_lower = code.lower()
        
        if 'struct' in code_lower and 'view' in code_lower:
            return 'ui_component'
        elif 'realitykit' in code_lower or 'entity' in code_lower:
            return '3d'
        elif 'animate' in code_lower or 'transition' in code_lower:
            return 'animation'
        
        return 'other' 