from pathlib import Path
from typing import Dict, Set, Optional, List
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
        
        # Ensure directories exist
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.debug_dir.mkdir(parents=True, exist_ok=True)

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
                
                # Look for samples using multiple selectors that might indicate a sample
                samples = []
                sample_indicators = [
                    soup.find_all(class_='sample-code'),  # Original check
                    soup.find_all('a', href=lambda x: x and 'sample' in x.lower()),  # Links containing 'sample'
                    soup.find_all(class_='sample-card'),  # Sample cards
                    soup.find_all(class_='sample-download'),  # Download buttons
                    soup.find_all(string=lambda x: x and 'sample' in x.lower()),  # Text containing 'sample'
                    soup.find_all('a', href=lambda x: x and x.endswith('.zip'))  # ZIP download links
                ]
                
                # Debug logging
                for i, indicator in enumerate(sample_indicators):
                    logger.debug(f"Sample indicator {i}: Found {len(indicator)} matches")
                    if indicator:
                        logger.debug(f"First match example: {indicator[0]}")
                
                # Combine all unique samples
                all_samples = set()
                for indicator_list in sample_indicators:
                    for item in indicator_list:
                        if hasattr(item, 'get') and item.get('href'):
                            all_samples.add(item['href'])
                        elif hasattr(item, 'parent') and hasattr(item.parent, 'get') and item.parent.get('href'):
                            all_samples.add(item.parent['href'])
                
                structure = {
                    'sections': len(sections),
                    'topics': len(topics),
                    'samples': len(all_samples)
                }
                
                logger.info(f"Found {structure['sections']} sections, {structure['topics']} topics, and {structure['samples']} samples")
                
                await browser.close()
                return structure
                
        except Exception as e:
            logger.error(f"Error analyzing documentation structure: {str(e)}")
            logger.debug("Full error details:", exc_info=True)
            return {'sections': 0, 'topics': 0, 'samples': 0}

    async def process_documentation_page(self, url: str) -> Optional[ProjectResource]:
        """Discover and analyze project without downloading"""
        start_time = time.time()
        logger.debug(f"Starting to process documentation page: {url}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Ensure absolute URL before first load
                if not url.startswith('http'):
                    url = f"{self.BASE_URL}{url}"
                
                # Single page load with timing
                load_start = time.time()
                logger.debug(f"Loading URL: {url}")
                await page.goto(url)
                logger.debug(f"Initial page load took: {time.time() - load_start:.2f}s")
                
                # Wait for network idle with timeout
                wait_start = time.time()
                try:
                    await page.wait_for_load_state('networkidle', timeout=5000)
                    logger.debug(f"Network idle wait took: {time.time() - wait_start:.2f}s")
                except Exception as e:
                    logger.debug(f"Network idle timeout: {str(e)}")
                
                # Get and validate content
                content = await page.content()
                content_hash = hash(content)
                logger.debug(f"Initial content length: {len(content)}, hash: {content_hash}")
                
                # Save initial state
                debug_file = self.debug_dir / f"{url.split('/')[-1]}_initial.html"
                debug_file.write_text(content)
                
                # Wait and check for dynamic content
                await asyncio.sleep(2)
                after_content = await page.content()
                after_hash = hash(after_content)
                
                if content_hash != after_hash:
                    logger.debug(f"Content changed after wait!")
                    logger.debug(f"Initial size: {len(content)}, After size: {len(after_content)}")
                    debug_file = self.debug_dir / f"{url.split('/')[-1]}_after_wait.html"
                    debug_file.write_text(after_content)
                
                # Look for download links with explicit wait
                logger.debug("Searching for download links")
                download_links = await page.query_selector_all('a[href*=".zip"]')
                logger.debug(f"Found {len(download_links)} download links")
                
                for link in download_links:
                    href = await link.get_attribute('href')
                    logger.debug(f"Download link found: {href}")
                    absolute_href = self._make_absolute_url(href)
                    
                    # Get project title with validation
                    title_elem = await page.query_selector('h1')
                    if title_elem:
                        title = await title_elem.text_content()
                        logger.debug(f"Found title: {title}")
                    else:
                        title = url.split('/')[-1]
                        logger.debug(f"Using fallback title: {title}")
                    
                    total_time = time.time() - start_time
                    logger.debug(f"Total processing time: {total_time:.2f}s")
                    
                    await browser.close()
                    return ProjectResource(
                        title=title,
                        url=url,
                        download_url=absolute_href
                    )
                
                logger.debug(f"No download links found after {time.time() - start_time:.2f}s")
                await browser.close()
                
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            logger.debug("Full error details:", exc_info=True)
        
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
                        # Create project directory with sanitized name
                        project_name = re.sub(r'[^\w\-]', '-', project.title.lower())
                        project_dir = self.projects_dir / project_name
                        project_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Save zip file
                        zip_path = project_dir / 'project.zip'
                        zip_path.write_bytes(await response.read())
                        
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
                        
                    logger.error(f"Got status {response.status} for {project.download_url}")
                        
        except Exception as e:
            logger.error(f"Error downloading project {project.title}: {str(e)}")
            
        return False

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