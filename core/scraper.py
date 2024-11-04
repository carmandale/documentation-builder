from pathlib import Path
from typing import List, Optional
from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
from models.base import DocumentationPage
from extractors.doc_extractor import DocumentationExtractor
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
        """Scrape and extract content from a single URL"""
        try:
            logger.info(f"Scraping: {url}")
            
            # Navigate to the page
            response = await page.goto(url, wait_until='networkidle', timeout=30000)
            if not response:
                logger.error(f"No response from {url}")
                return None
                
            # Get the content
            content = await page.content()
            
            # Save raw HTML
            raw_file = self.debug_dir / f"raw_{url.split('/')[-1]}.html"
            raw_file.write_text(content, encoding='utf-8')
            
            # Take screenshot
            screenshot_file = self.debug_dir / f"screenshot_{url.split('/')[-1]}.png"
            await page.screenshot(path=str(screenshot_file))
            
            # Extract content
            soup = BeautifulSoup(content, 'html.parser')
            doc_page = self.doc_extractor.extract_page(soup, url)
            
            if doc_page:
                # Save extracted data
                output_file = self.extracted_dir / f"extracted_{url.split('/')[-1]}.json"
                output_file.write_text(
                    doc_page.model_dump_json(indent=2),
                    encoding='utf-8'
                )
                
            return doc_page
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None