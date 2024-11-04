from bs4 import BeautifulSoup
from models.base import DocumentationPage, Topic, CodeBlock
from extractors.code_extractor import CodeBlockExtractor
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class DocumentationExtractor:
    """Extracts structured documentation from HTML"""
    
    def extract(self, soup: BeautifulSoup) -> DocumentationPage:
        """Extract documentation page content"""
        title = self._extract_title(soup)
        topics = self._extract_topics(soup)
        code_blocks = CodeBlockExtractor.extract_code_blocks(soup)
        
        return DocumentationPage(
            title=title,
            url="",  # URL will be set by scraper
            topics=topics,
            code_blocks=code_blocks,
            code_patterns={},  # New functionality will be populated later
            relationships=[],
            validation_tests=[]
        )
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_elem = soup.find(['h1', 'title'])
        return title_elem.get_text(strip=True) if title_elem else "Untitled"
    
    def _extract_topics(self, soup: BeautifulSoup) -> List[Topic]:
        """Extract topics from the page"""
        topics = []
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        
        for header in headers:
            level = int(header.name[1])  # Get numeric level from h1, h2, etc.
            content = self._extract_section_content(header)
            
            topic = Topic(
                title=header.get_text(strip=True),
                level=level,
                content=content,
                path=self._get_topic_path(header)
            )
            topics.append(topic)
        
        return topics
    
    def _extract_section_content(self, header_elem) -> Optional[str]:
        """Extract content belonging to a section"""
        content = []
        elem = header_elem.find_next_sibling()
        
        while elem and not elem.name in ['h1', 'h2', 'h3', 'h4']:
            if elem.name == 'p':
                content.append(elem.get_text(strip=True))
            elem = elem.find_next_sibling()
        
        return "\n".join(content) if content else None
    
    def _get_topic_path(self, elem) -> List[str]:
        """Get hierarchical path to topic"""
        path = []
        current = elem
        
        while current:
            if current.name in ['h1', 'h2', 'h3', 'h4']:
                path.insert(0, current.get_text(strip=True))
            current = current.find_previous(['h1', 'h2', 'h3', 'h4'])
        
        return path