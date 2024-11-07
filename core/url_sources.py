from pathlib import Path
from typing import Dict, Set, Optional, List, Any
from bs4 import BeautifulSoup
import aiohttp
import re
from dataclasses import dataclass
import json
from collections import defaultdict
from playwright.async_api import async_playwright
import time
import asyncio
from utils.logging import logger
from core.config import TEST_SAMPLE_COUNT

@dataclass
class ProjectResource:
    """Represents a downloadable project resource"""
    title: str
    url: str
    download_url: Optional[str] = None
    local_path: Optional[Path] = None

class DocumentationURLCollector:
    BASE_URL = "https://developer.apple.com"
    
    def __init__(self, base_dir: Path = Path('data')):
        self.base_dir = base_dir
        self.projects_dir = base_dir / 'projects'
        self.debug_dir = base_dir / 'debug'
        self.cache_dir = base_dir / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.url_cache = self.cache_dir / 'url_cache.json'
        self.samples_cache = self.cache_dir / 'discovered_samples.json'
        
        # Ensure all directories exist
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize cache files if they don't exist
        if not self.url_cache.exists():
            self.url_cache.write_text('[]')
        if not self.samples_cache.exists():
            self.samples_cache.write_text('[]')

    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URLs to absolute URLs"""
        if url.startswith('/'):
            return f"{self.BASE_URL}{url}"
        return url

    async def get_documentation_links(self, url: str) -> Dict[str, Set[str]]:
        """Get all documentation links from a page"""
        links = defaultdict(set)
        start_time = time.time()
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                logger.debug(f"[Timing] Browser launch: {time.time() - start_time:.2f}s")
                
                page_start = time.time()
                await page.goto(url)
                logger.debug(f"[Timing] Initial page load: {time.time() - page_start:.2f}s")
                
                wait_start = time.time()
                await page.wait_for_load_state('networkidle')
                logger.debug(f"[Timing] Wait for network idle: {time.time() - wait_start:.2f}s")
                
                # Get content at different stages
                initial_content = await page.content()
                initial_size = len(initial_content)
                logger.debug(f"[Content] Initial size: {initial_size}")
                
                # Wait a bit and check content again
                await asyncio.sleep(1)
                after_wait_content = await page.content()
                after_size = len(after_wait_content)
                logger.debug(f"[Content] After wait size: {after_size}")
                
                if initial_size != after_size:
                    logger.debug(f"[Content] Size changed by: {after_size - initial_size}")
                    # Save both versions for comparison
                    debug_file = self.debug_dir / f"{url.split('/')[-1]}_initial.html"
                    debug_file.write_text(initial_content)
                    debug_file = self.debug_dir / f"{url.split('/')[-1]}_after.html"
                    debug_file.write_text(after_wait_content)
                
                # Save raw content for debugging
                debug_file = self.debug_dir / f"{url.split('/')[-1]}_initial.html"
                debug_file.write_text(initial_content)
                logger.debug(f"Saved initial content to {debug_file}")
                
                # Parse content
                soup = BeautifulSoup(initial_content, 'html.parser')
                
                # Log all links before categorization
                all_links = soup.find_all('a', href=True)
                logger.debug(f"Found {len(all_links)} total links before categorization")
                
                # Find all links
                for link in all_links:
                    href = link['href']
                    logger.debug(f"Processing link: {href}")
                    
                    # Categorize URLs
                    if '/documentation/' in href:
                        logger.debug(f"Found documentation link: {href}")
                        links['documentation'].add(self._make_absolute_url(href))
                    elif '/videos/' in href or '/wwdc/' in href:
                        logger.debug(f"Found videos link: {href}")
                        links['videos'].add(self._make_absolute_url(href))
                    else:
                        links['other'].add(self._make_absolute_url(href))
                
                await browser.close()
                
                # Log summary
                for category, urls in links.items():
                    logger.info(f"Found {len(urls)} {category} links")
                
                return links
                
        except Exception as e:
            logger.error(f"Error getting links from {url}: {str(e)}")
            return links

    async def analyze_documentation_structure(self, url: str) -> Dict:
        """Analyze the structure of a documentation page"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                content = await page.content()
                
                # Save debug content
                debug_file = self.debug_dir / f"{url.split('/')[-1]}_structure.html"
                debug_file.write_text(content)
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find sections and topics
                sections = soup.find_all(['h1', 'h2', 'h3'])
                topics = soup.find_all(class_='topic')
                
                # Look for samples more aggressively
                samples = set()
                
                # 1. Look for direct sample links
                sample_links = soup.find_all('a', href=lambda x: x and (
                    'sample' in x.lower() or 
                    x.endswith('.zip') or 
                    '/documentation/visionos/' in x
                ))
                for link in sample_links:
                    href = link.get('href', '')
                    if href:
                        logger.debug(f"Found potential sample link: {href}")
                        samples.add(href)
                
                # 2. Look for sample cards/sections
                sample_sections = soup.find_all(['div', 'section'], class_=lambda x: x and 'sample' in x.lower())
                for section in sample_sections:
                    links = section.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        if href:
                            logger.debug(f"Found sample in section: {href}")
                            samples.add(href)
                
                # 3. Look for download buttons
                download_buttons = soup.find_all(class_='sample-download')
                for button in download_buttons:
                    parent_link = button.find_parent('a', href=True)
                    if parent_link and parent_link.get('href'):
                        logger.debug(f"Found sample download button: {parent_link['href']}")
                        samples.add(parent_link['href'])
                
                structure = {
                    'sections': len(sections),
                    'topics': len(topics),
                    'samples': len(samples)
                }
                
                logger.info(f"Found {structure['sections']} sections, {structure['topics']} topics, and {structure['samples']} samples")
                
                await browser.close()
                return structure
                
        except Exception as e:
            logger.error(f"Error analyzing documentation structure: {str(e)}")
            logger.debug("Full error details:", exc_info=True)
            return {'sections': 0, 'topics': 0, 'samples': 0}

    async def process_documentation_page(self, url: str) -> Optional[ProjectResource]:
        """Process a documentation page for samples"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                # First try to find download buttons
                download_buttons = await page.query_selector_all('a.download-button, a[href*="download"]')
                
                # Then look for specific sample links
                if not download_buttons:
                    download_buttons = await page.query_selector_all([
                        'a[href*=".zip"]',
                        'a[href*="sample-code"]',
                        'a[href*="/sample/"]'
                    ].join(','))
                
                if download_buttons:
                    # Get the title
                    title_elem = await page.query_selector('h1')
                    title = await title_elem.text_content() if title_elem else url.split('/')[-1]
                    
                    # Get the download URL
                    for button in download_buttons:
                        href = await button.get_attribute('href')
                        if href:
                            # Validate it's a zip file URL
                            if href.endswith('.zip') or '/sample-code/' in href or '/sample/' in href:
                                logger.info(f"Found valid download URL: {href}")
                                return ProjectResource(
                                    title=title,
                                    url=url,
                                    download_url=self._make_absolute_url(href)
                                )
                
                await browser.close()
                return None
                
        except Exception as e:
            logger.error(f"Error processing page {url}: {str(e)}")
            return None

    async def process_and_download(self, url: str) -> Optional[ProjectResource]:
        """Process page and optionally download"""
        project = await self.process_documentation_page(url)
        if project:
            await self.download_project(project)
        return project

    async def download_project(self, project: ProjectResource) -> bool:
        """Download a project to local storage"""
        if not project.download_url:
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(project.download_url) as response:
                    if response.status == 200:
                        # Verify content type
                        content_type = response.headers.get('content-type', '')
                        if not ('zip' in content_type.lower() or 'octet-stream' in content_type.lower()):
                            logger.warning(f"Unexpected content type: {content_type} for {project.download_url}")
                            return False
                        
                        # Create project directory with sanitized name
                        project_name = re.sub(r'[^\w\-]', '-', project.title.lower())
                        project_dir = self.projects_dir / project_name
                        project_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Save zip file
                        zip_path = project_dir / 'project.zip'
                        content = await response.read()
                        
                        # Verify it's actually a zip file
                        if not content.startswith(b'PK'):
                            logger.error(f"Downloaded content is not a zip file for {project.title}")
                            return False
                            
                        zip_path.write_bytes(content)
                        
                        try:
                            # Extract zip file
                            import zipfile
                            with zipfile.ZipFile(zip_path) as zf:
                                zf.extractall(project_dir)
                                
                            # Update project path
                            project.local_path = project_dir
                            logger.info(f"Downloaded project to {project_dir}")
                            
                            # Clean up zip file
                            zip_path.unlink()
                            
                            return True
                        except zipfile.BadZipFile:
                            logger.error(f"Invalid zip file for {project.title}")
                            if zip_path.exists():
                                zip_path.unlink()
                            return False
                            
                    logger.error(f"Got status {response.status} for {project.download_url}")
                        
        except Exception as e:
            logger.error(f"Error downloading project {project.title}: {str(e)}")
            
        return False

    async def discover_all_samples(self) -> List[ProjectResource]:
        """Discover and cache all sample projects"""
        # Validate cache before using
        if self._validate_samples_cache() and self.samples_cache.exists():
            try:
                cached = json.loads(self.samples_cache.read_text())
                logger.info(f"Found {len(cached)} samples in cache")
                if cached:  # Only use cache if it has data
                    return [ProjectResource(**p) for p in cached]
            except json.JSONDecodeError:
                logger.warning("Invalid cache file, rediscovering samples")
        
        # Discover new samples
        samples = []
        links = await self.get_documentation_links(self.BASE_URL)
        doc_links = links.get('documentation', set())
        
        logger.info(f"Processing {len(doc_links)} documentation links")
        for url in doc_links:
            # Process each URL for samples
            structure = await self.analyze_documentation_structure(url)
            if structure['samples'] > 0:
                logger.debug(f"Found {structure['samples']} potential samples in {url}")
                
                # Use Playwright for dynamic content
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page()
                    await page.goto(url)
                    await page.wait_for_load_state('networkidle')
                    
                    # Get sample links using Playwright selectors
                    sample_links = await page.query_selector_all('a.sample-download')
                    if not sample_links:
                        sample_links = await page.query_selector_all('a[href*=".zip"]')
                    
                    for link in sample_links:
                        href = await link.get_attribute('href')
                        if href:
                            # Get title using Playwright
                            parent = await link.evaluate('el => el.closest("div, section")')
                            title_elem = await parent.query_selector('h1, h2, h3')
                            title = await title_elem.text_content() if title_elem else url.split('/')[-1]
                            
                            project = ProjectResource(
                                title=title,
                                url=url,
                                download_url=self._make_absolute_url(href)
                            )
                            samples.append(project)
                            logger.info(f"Found sample: {title}")
                    
                    await browser.close()
        
        # Cache results with validation and debug logging
        if samples:
            try:
                cache_data = [
                    {
                        'title': p.title,
                        'url': p.url,
                        'download_url': p.download_url,
                        'local_path': str(p.local_path) if p.local_path else None
                    } 
                    for p in samples
                ]
                logger.debug(f"Caching {len(samples)} samples")
                logger.debug(f"Cache data: {json.dumps(cache_data, indent=2)}")
                self.samples_cache.write_text(json.dumps(cache_data, indent=2))
                logger.info(f"Successfully cached {len(samples)} samples")
            except Exception as e:
                logger.error(f"Error caching samples: {str(e)}", exc_info=True)
        else:
            logger.warning("No samples found to cache")
        
        return samples

    async def download_samples(self, samples: List[ProjectResource], 
                             mode: str = 'test') -> List[ProjectResource]:
        """Download samples based on mode"""
        if mode == 'skip':
            return []
            
        to_download = samples
        if mode == 'test':
            # Use first TEST_SAMPLE_COUNT samples
            to_download = samples[:TEST_SAMPLE_COUNT]
            
        return [s for s in to_download if await self.download_project(s)]

    async def _get_page_content(self, url: str) -> str:
        """Get page content using playwright"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            logger.error(f"Error getting page content: {str(e)}")
            return ""

    def _validate_cache(self, cache_file: Path, schema: Dict) -> bool:
        """Validate cache file against schema"""
        try:
            if not cache_file.exists():
                logger.warning(f"Cache file does not exist: {cache_file}")
                return False
                
            data = json.loads(cache_file.read_text())
            
            # Validate structure
            if not isinstance(data, list):
                logger.error(f"Cache must be a list: {cache_file}")
                return False
                
            # Validate each entry
            for entry in data:
                if not isinstance(entry, dict):
                    logger.error(f"Cache entry must be a dict: {entry}")
                    return False
                    
                # Check required fields
                for field, field_type in schema.items():
                    if field not in entry:
                        logger.error(f"Missing required field {field} in {entry}")
                        return False
                    if not isinstance(entry[field], field_type):
                        logger.error(f"Field {field} has wrong type in {entry}")
                        return False
            
            logger.debug(f"Cache validation successful for {cache_file}")
            return True
            
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in cache file: {cache_file}")
            return False
        except Exception as e:
            logger.error(f"Error validating cache: {str(e)}")
            return False

    def _validate_samples_cache(self):
        """Validate the samples cache"""
        try:
            if not self.samples_cache.exists():
                return False
                
            # Check cache age
            cache_age = time.time() - self.samples_cache.stat().st_mtime
            if cache_age > 86400:  # 24 hours
                logger.info("Cache is older than 24 hours")
                return False
                
            # Validate cache content
            cache_data = json.loads(self.samples_cache.read_text())
            if not isinstance(cache_data, list):
                logger.warning("Invalid cache format")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Cache validation error: {str(e)}")
            return False

    def _validate_url_cache(self) -> bool:
        """Validate URL cache"""
        schema = {
            'url': str,
            'category': str,
            'last_checked': str
        }
        return self._validate_cache(self.url_cache, schema)

class URLSources:
    """Simple URL management class"""
    def __init__(self):
        self.urls = defaultdict(set)
        
    def add_url(self, url: str, category: str):
        self.urls[category].add(url)
        
    def get_urls(self, category: str = None) -> Set[str]:
        if category:
            return self.urls.get(category, set())
        return set().union(*self.urls.values())