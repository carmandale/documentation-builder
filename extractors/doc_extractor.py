from bs4 import BeautifulSoup, Tag
from models.base import DocumentationPage, Topic
from extractors.code_extractor import CodeBlockExtractor
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class DocumentationExtractor:
    """Main documentation page extractor"""
    
    def extract_page(self, soup: BeautifulSoup, url: str) -> Optional[DocumentationPage]:
        """Extract all relevant information from a documentation page"""
        try:
            # Find main content
            main_content = soup.find('main')
            if not main_content:
                logger.error("No main content found")
                return None
                
            # Extract title
            title = main_content.find('h1')
            if not title:
                logger.error("No title found")
                return None
                
            # Extract introduction
            intro = main_content.find(['p', 'div'], class_='introduction')
            introduction = intro.get_text(strip=True) if intro else None
            
            # Extract code blocks using specialized extractor
            code_blocks = CodeBlockExtractor.extract_code_blocks(soup)
            
            # Extract topics
            topics = self._extract_topics(main_content)
            
            # Extract related links
            related_links = self._extract_related_links(soup)
            
            return DocumentationPage(
                title=title.get_text(strip=True),
                url=url,
                introduction=introduction,
                code_blocks=code_blocks,
                topics=topics,
                related_links=related_links
            )
            
        except Exception as e:
            logger.error(f"Error extracting page: {str(e)}")
            return None
    
    def _extract_topics(self, main_content: Tag) -> List[Topic]:
        """Extract topics from the page"""
        topics = []
        for heading in main_content.find_all(['h2', 'h3']):
            level = int(heading.name[1])  # Get numeric level from h2, h3
            topics.append(Topic(
                title=heading.get_text(strip=True),
                level=level,
                content=self._get_topic_content(heading)
            ))
        return topics
    
    def _get_topic_content(self, heading: Tag) -> Optional[str]:
        """Get the content following a topic heading"""
        content = []
        for sibling in heading.next_siblings:
            if sibling.name in ['h2', 'h3']:
                break
            if sibling.string and sibling.string.strip():
                content.append(sibling.string.strip())
        return " ".join(content) if content else None
    
    def _extract_related_links(self, soup: BeautifulSoup) -> List[dict]:
        """Extract related links from the page"""
        related_links = []
        related_section = soup.find(['div', 'section'], class_='related')
        if related_section:
            for link in related_section.find_all('a'):
                related_links.append({
                    'title': link.get_text(strip=True),
                    'url': link.get('href', '')
                })
        return related_links