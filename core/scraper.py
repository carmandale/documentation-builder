from pathlib import Path
from typing import List, Optional
from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
from models.base import DocumentationPage, Topic
from extractors import CodeBlockExtractor, DocumentationExtractor
from extractors.relationship_extractor import RelationshipExtractor
from extractors.validation_extractor import ValidationExtractor
import logging
import asyncio
import json

logger = logging.getLogger(__name__)

class DocumentationScraper:
    """Main documentation scraper class"""
    
    def __init__(self, output_dir: Path = Path('data')):
        self.output_dir = output_dir
        self.debug_dir = output_dir / 'debug'
        self.extracted_dir = output_dir / 'extracted'
        self.doc_extractor = DocumentationExtractor()
        self.validation_extractor = ValidationExtractor()
        
        # Create necessary directories
        self.output_dir.mkdir(exist_ok=True)
        self.debug_dir.mkdir(exist_ok=True)
        self.extracted_dir.mkdir(exist_ok=True)
    
    async def scrape_urls(self, urls: List[str]) -> List[DocumentationPage]:
        """Scrape multiple URLs and extract their content"""
        pages = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            
            try:
                page = await context.new_page()
                
                for url in urls:
                    doc_page = await self.scrape_url(page, url)
                    if doc_page:
                        pages.append(doc_page)
                    await asyncio.sleep(2)  # Be nice to the server
                    
            finally:
                await browser.close()
                
        return pages
    
    async def scrape_url(self, page: Page, url: str) -> Optional[DocumentationPage]:
        """Scrape a single documentation page with the new structure"""
        try:
            logger.info(f"Scraping URL: {url}")
            # Navigate to the URL
            await page.goto(url, wait_until='networkidle')
            content = await page.content()
            
            if not content:
                logger.warning(f"No content found for {url}")
                return None
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # Save debug content
            debug_file = self.debug_dir / f"raw_{url.split('/')[-1]}.html"
            debug_file.write_text(content, encoding='utf-8')
            logger.debug(f"Saved debug content to {debug_file}")
            
            # Extract code blocks and convert to patterns
            code_blocks = CodeBlockExtractor.extract_code_blocks(soup)
            logger.info(f"Found {len(code_blocks)} code blocks")
            
            code_patterns = CodeBlockExtractor().extract_patterns(code_blocks)
            logger.info(f"Generated {len(code_patterns)} patterns")
            
            # Extract relationships
            relationships = RelationshipExtractor().extract_relationships(soup, code_patterns)
            logger.info(f"Found {len(relationships)} relationships")
            
            # Generate validation tests
            validation_tests = self.validation_extractor.generate_tests(code_patterns)
            logger.info(f"Generated {len(validation_tests)} validation tests")
            
            # Create page
            doc_page = DocumentationPage(
                title=self._extract_title(soup),
                url=url,
                code_blocks=code_blocks,
                code_patterns=code_patterns,
                relationships=relationships,
                validation_tests=validation_tests,
                topics=self._extract_topics(soup)
            )
            
            # Save extracted data
            output_file = self.extracted_dir / f"extracted_{url.split('/')[-1]}.json"
            output_file.write_text(
                doc_page.model_dump_json(indent=2),
                encoding='utf-8'
            )
            logger.info(f"Saved extracted data to {output_file}")
            
            return doc_page
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}", exc_info=True)
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from the page"""
        return self.doc_extractor._extract_title(soup)
    
    def _extract_topics(self, soup: BeautifulSoup) -> List[Topic]:
        """Extract topics from the page"""
        return self.doc_extractor._extract_topics(soup)