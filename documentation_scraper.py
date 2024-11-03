import asyncio
import json
from datetime import datetime
from typing import List, Optional
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from pydantic import BaseModel
import logging
import os
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Data Models
class CodeExample(BaseModel):
    code: str
    description: Optional[str]

class Parameter(BaseModel):
    name: str
    type: str
    description: Optional[str]

class DocumentationEntry(BaseModel):
    title: str
    description: str
    url: str
    framework: str
    parameters: Optional[List[Parameter]] = None
    examples: Optional[List[CodeExample]] = None
    metadata: dict
    scraped_at: datetime

class VisionOSScraper:
    BASE_URL = "https://developer.apple.com/documentation/visionos"
    
    def __init__(self):
        self.visited_urls = set()
        self.documentation = []
        self.is_running = True
        self.browser = None
        self.context = None
        self.playwright = None

    async def init_browser(self):
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context(
                user_agent="Documentation Bot - Research Purpose"
            )
        except Exception as e:
            logger.error(f"Error initializing browser: {str(e)}")
            await self.cleanup()
            raise

    async def cleanup(self):
        """Cleanup resources in the correct order"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def stop(self):
        """Signal the scraper to stop"""
        self.is_running = False
        logger.info("Stopping scraper...")

    def parse_content(self, html: str, url: str) -> Optional[DocumentationEntry]:
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Find main content
            main_content = soup.find('main')
            if not main_content:
                logger.debug(f"No main content found for {url}")
                return None

            # Extract title 
            title_elem = main_content.find('h1')
            if not title_elem:
                logger.debug(f"No title found for {url}")
                return None
            title = title_elem.get_text(strip=True)
            logger.debug(f"Found title: {title}")

            # Extract description
            description = ""
            # Look for the first paragraph after the title
            desc_elem = title_elem.find_next('p')
            if desc_elem:
                description = desc_elem.get_text(strip=True)
            logger.debug(f"Found description: {description}")

            # Extract code examples
            examples = []
            code_blocks = main_content.find_all('div', class_='code-listing')
            for block in code_blocks:
                code = block.get_text(strip=True)
                desc = ""
                # Look for description paragraph before code block
                prev_elem = block.find_previous('p')
                if prev_elem:
                    desc = prev_elem.get_text(strip=True)
                examples.append(CodeExample(code=code, description=desc))
            logger.debug(f"Found {len(examples)} code examples")

            # Extract parameters
            parameters = []
            param_sections = main_content.find_all(['h3', 'h4'], string=lambda x: x and 'Parameters' in x)
            for section in param_sections:
                param_list = section.find_next('ul')
                if param_list:
                    for param in param_list.find_all('li'):
                        param_text = param.get_text(strip=True)
                        # Parse parameter text into name, type, description
                        parts = param_text.split('-', 1)
                        if len(parts) == 2:
                            name = parts[0].strip()
                            desc = parts[1].strip()
                            parameters.append(Parameter(
                                name=name,
                                type="",  # We'll need to enhance this
                                description=desc
                            ))
            logger.debug(f"Found {len(parameters)} parameters")

            entry = DocumentationEntry(
                title=title,
                description=description,
                url=url,
                framework="VisionOS",
                parameters=parameters if parameters else None,
                examples=examples if examples else None,
                metadata={
                    "platform": "visionOS",
                    "scrape_timestamp": datetime.utcnow().isoformat(),
                    "section": self._determine_section(url),
                    "has_code_examples": bool(examples),
                    "has_parameters": bool(parameters)
                },
                scraped_at=datetime.utcnow()
            )
            
            logger.debug(f"Successfully created entry for {url}")
            return entry

        except Exception as e:
            logger.error(f"Error parsing content for {url}: {str(e)}")
            logger.exception(e)  # This will log the full stack trace
            return None

    def _determine_section(self, url: str) -> str:
        """Determine the documentation section from the URL"""
        parts = url.split('/')
        if len(parts) > 4:
            return parts[4].replace('-', ' ').title()
        return "General"

    def _classify_content(self, content: str) -> List[str]:
        """Classify content into relevant topics"""
        topics = []
        topic_keywords = {
            'UI': ['window', 'view', 'button', 'interface', 'SwiftUI'],
            '3D': ['RealityKit', 'model', '3D', 'scene', 'mesh'],
            'Interaction': ['gesture', 'input', 'touch', 'hand', 'eye'],
            'Graphics': ['material', 'texture', 'shader', 'rendering'],
            'System': ['privacy', 'permission', 'setting', 'configuration'],
            'Media': ['audio', 'video', 'image', 'sound', 'spatial']
        }
        
        content_lower = content.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword.lower() in content_lower for keyword in keywords):
                topics.append(topic)
        
        return topics

    async def scrape_page(self, url: str):
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)
            content = await page.content()
            
            # Save raw HTML for debugging
            debug_dir = Path('debug')
            debug_dir.mkdir(exist_ok=True)
            page_name = url.split('/')[-1] or 'index'
            with open(debug_dir / f"{page_name}.html", 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Parse the content
            entry = self.parse_content(content, url)
            if entry:
                self.documentation.append(entry.dict())
                logger.info(f"Successfully scraped: {url}")

            # Find additional links
            links = await page.query_selector_all('a[href^="/documentation/visionos"]')
            new_urls = []
            for link in links:
                href = await link.get_attribute('href')
                if href:
                    full_url = f"https://developer.apple.com{href}"
                    if full_url not in self.visited_urls:
                        new_urls.append(full_url)

            await page.close()
            return new_urls

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return []

    async def run(self):
        try:
            await self.init_browser()
            urls_to_scrape = [self.BASE_URL]
            last_save_time = datetime.utcnow()
            save_interval = 60  # Save every 60 seconds
            
            while urls_to_scrape and self.is_running:
                try:
                    # Process 5 pages concurrently
                    batch = urls_to_scrape[:5]
                    urls_to_scrape = urls_to_scrape[5:]
                    
                    tasks = [self.scrape_page(url) for url in batch]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Add new URLs to the queue
                    for result in results:
                        if isinstance(result, list) and result:  # Only add if result is a valid list
                            urls_to_scrape.extend(result)
                    
                    # Save periodically
                    now = datetime.utcnow()
                    if (now - last_save_time).seconds >= save_interval:
                        self.save_documentation()
                        last_save_time = now
                    
                    # Small delay to be respectful to the server
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error processing batch: {str(e)}")
                    continue
            
            # Final save
            self.save_documentation()
                
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
        finally:
            await self.cleanup()

    def save_documentation(self):
        # Create a 'data' directory if it doesn't exist
        output_dir = Path('data')
        output_dir.mkdir(exist_ok=True)
        
        # Improved deduplication that considers the base URL without fragments
        seen_base_urls = {}
        unique_docs = []
        for doc in self.documentation:
            # Remove URL fragments (everything after #) for comparison
            base_url = doc['url'].split('#')[0]
            
            if base_url not in seen_base_urls:
                seen_base_urls[base_url] = doc
                unique_docs.append(doc)
            else:
                # If we have a more complete version (with examples/parameters), use that
                existing = seen_base_urls[base_url]
                if (not existing.get('examples') and doc.get('examples')) or \
                   (not existing.get('parameters') and doc.get('parameters')):
                    seen_base_urls[base_url] = doc
                    unique_docs[unique_docs.index(existing)] = doc
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = output_dir / f'visionos_documentation_{timestamp}.json'
        
        # Save the documentation
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(unique_docs, f, indent=2, default=str)
        
        # Save manifest
        manifest = {
            'timestamp': timestamp,
            'total_pages': len(seen_base_urls),
            'total_entries': len(unique_docs),
            'base_url': self.BASE_URL,
            'visited_urls': list(self.visited_urls)
        }
        
        manifest_file = output_dir / f'manifest_{timestamp}.json'
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Documentation saved to {filename}")
        logger.info(f"Total unique pages: {len(seen_base_urls)}")
        logger.info(f"Total unique entries: {len(unique_docs)}")