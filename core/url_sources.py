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
from core.config import TEST_SAMPLE_COUNT, BASE_URLS

@dataclass
class ProjectResource:
    """Represents a downloadable project resource"""
    title: str
    url: str
    download_url: Optional[str] = None
    local_path: Optional[Path] = None
    downloaded: bool = False

    def mark_downloaded(self, path: Path):
        self.local_path = path
        self.downloaded = True

class DocumentationURLCollector:
    BASE_URL = "https://developer.apple.com"
    
    def __init__(self, base_dir: Path = Path('data')):
        self.base_dir = base_dir
        self.projects_dir = base_dir / 'projects'
        self.debug_dir = base_dir / 'debug'
        self.cache_dir = base_dir / 'cache'
        self.url_cache = self.cache_dir / 'url_cache.json'
        self.samples_cache = self.cache_dir / 'discovered_samples.json'
        self.doc_cache = self.cache_dir / 'documentation_cache.json'
        self.analysis_cache = self.cache_dir / 'analysis_cache.json'
        
        # Ensure all directories exist
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize cache files if they don't exist
        for cache_file in [self.url_cache, self.samples_cache, self.doc_cache, self.analysis_cache]:
            if not cache_file.exists():
                cache_file.write_text('{}')

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
        """Process a documentation page for samples with improved download URL detection"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                logger.info(f"Processing page: {url}")
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                # Get the title
                title_elem = await page.query_selector('h1')
                title = await title_elem.text_content() if title_elem else url.split('/')[-1]
                
                # Look for download URLs in multiple ways
                download_url = None
                
                # 1. Direct download button
                download_button = await page.query_selector('a.sample-download')
                if download_button:
                    download_url = await download_button.get_attribute('href')
                    logger.debug(f"Found download button with URL: {download_url}")
                
                # 2. Check for zip links
                if not download_url:
                    zip_link = await page.query_selector('a[href$=".zip"]')
                    if zip_link:
                        download_url = await zip_link.get_attribute('href')
                        logger.debug(f"Found zip link with URL: {download_url}")
                
                # 3. Check docs-assets links
                if not download_url:
                    assets_link = await page.query_selector('a[href*="docs-assets.developer.apple.com"]')
                    if assets_link:
                        href = await assets_link.get_attribute('href')
                        if href and href.endswith('.zip'):
                            download_url = href
                            logger.debug(f"Found docs-assets link with URL: {download_url}")
                
                if download_url:
                    download_url = self._make_absolute_url(download_url)
                    logger.info(f"Found download URL for {title}: {download_url}")
                    return ProjectResource(
                        title=title,
                        url=url,
                        download_url=download_url,
                        downloaded=False  # Explicitly set initial state
                    )
                else:
                    logger.debug(f"No download URL found for {url}")
                
                await browser.close()
                return None
                
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            return None

    async def process_and_download(self, url: str) -> Optional[ProjectResource]:
        """Process page and optionally download"""
        project = await self.process_documentation_page(url)
        if project:
            await self.download_project(project)
        return project

    async def download_project(self, project: ProjectResource) -> bool:
        """Download a project if not already downloaded"""
        if project.downloaded and project.local_path and project.local_path.exists():
            logger.info(f"Project already downloaded: {project.title}")
            return True

        if not project.download_url:
            logger.error(f"No download URL for project: {project.title}")
            return False

        try:
            async with aiohttp.ClientSession() as session:
                logger.info(f"Downloading {project.title} from {project.download_url}")
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
                                
                            # Update project path and status
                            project.mark_downloaded(project_dir)
                            logger.info(f"Downloaded project to {project_dir}")
                            
                            # Clean up zip file
                            zip_path.unlink()
                            
                            # Update cache
                            self._update_cache(project)
                            
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
        """Load or discover all samples"""
        if self.samples_cache.exists():
            # Load from cache
            cache_data = json.loads(self.samples_cache.read_text())
            samples = []
            for item in cache_data:
                sample = ProjectResource(**item)
                # Verify if project still exists
                if sample.local_path:
                    path = Path(sample.local_path)
                    if path.exists():
                        sample.downloaded = True
                    else:
                        sample.local_path = None
                        sample.downloaded = False
                samples.append(sample)
            return samples
        return []

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

    def _validate_cache(self, cache_file: Path, max_age: int = 86400) -> bool:
        """Validate cache file with age check"""
        try:
            if not cache_file.exists():
                return False
                
            # Check cache age
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age > max_age:  # Default 24 hours
                logger.info(f"Cache {cache_file.name} is older than {max_age/3600:.1f} hours")
                return False
                
            # Validate content
            json.loads(cache_file.read_text())
            return True
            
        except Exception as e:
            logger.error(f"Cache validation error for {cache_file}: {str(e)}")
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

    async def get_sample_urls_from_page(self, url: str) -> List[str]:
        """Extract sample URLs from a documentation page with improved detection"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                # Look for sample links with various patterns
                sample_urls = set()  # Use set for automatic deduplication
                
                # 1. Direct download links
                download_links = await page.query_selector_all('a[href*="docs-assets.developer.apple.com"]')
                for link in download_links:
                    href = await link.get_attribute('href')
                    if href and href.endswith('.zip'):
                        sample_urls.add(self._make_absolute_url(href))
                
                # 2. Sample project pages
                sample_pages = await page.query_selector_all([
                    'a[href*="/documentation/visionos/"][href*="-sample"]',
                    'a[href*="/documentation/visionos/"][href*="example"]',
                    'a.sample-download',  # Sample download buttons
                    'div.sample-card a',  # Sample cards
                ].join(','))
                
                for link in sample_pages:
                    href = await link.get_attribute('href')
                    if href:
                        sample_urls.add(self._make_absolute_url(href))
                
                # Save debug content
                debug_file = self.debug_dir / f"{url.split('/')[-1]}_samples.html"
                debug_file.write_text(await page.content())
                
                await browser.close()
                
                # Log what we found
                if sample_urls:
                    logger.info(f"Found {len(sample_urls)} unique sample URLs on {url}")
                    for sample_url in sample_urls:
                        logger.debug(f"Sample URL: {sample_url}")
                
                return list(sample_urls)
                
        except Exception as e:
            logger.error(f"Error getting sample URLs from {url}: {str(e)}")
            return []

    async def extract_documentation_content(self, url: str) -> Dict:
        """Extract and cache documentation content"""
        # Check cache first
        cache_key = re.sub(r'[^\w\-]', '-', url.split('/')[-1])
        cache_file = self.doc_cache.parent / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                cached = json.loads(cache_file.read_text())
                logger.info(f"Using cached documentation for {url}")
                return cached
            except json.JSONDecodeError:
                logger.warning(f"Invalid cache for {url}")

        # Cache miss - extract content
        content = await self._extract_doc_content(url)
        if content:
            try:
                cache_file.write_text(json.dumps(content, indent=2))
                logger.info(f"Cached documentation for {url}")
            except Exception as e:
                logger.error(f"Error caching documentation: {str(e)}")
        
        return content

    def _get_code_context(self, element, context_lines=3):
        """Get surrounding context for a code block"""
        context = []
        prev = element.find_previous_siblings(limit=context_lines)
        next = element.find_next_siblings(limit=context_lines)
        
        for p in reversed(prev):
            if p.get_text(strip=True):
                context.append(p.get_text(strip=True))
        
        for n in next:
            if n.get_text(strip=True):
                context.append(n.get_text(strip=True))
                
        return context

    async def _discover_new_samples(self) -> List[ProjectResource]:
        """Internal method to discover new samples"""
        samples = []
        
        # First get all documentation URLs
        discovered_urls = {}
        for base_url in BASE_URLS:
            # Get categorized links
            links = await self.get_documentation_links(base_url)
            
            # Merge discovered URLs
            for category, urls in links.items():
                if category not in discovered_urls:
                    discovered_urls[category] = set()
                discovered_urls[category].update(urls)
                
            # Check for samples in documentation structure
            structure = await self.analyze_documentation_structure(base_url)
            if structure['samples'] > 0:
                # Get sample URLs from this page
                page_samples = await self.get_sample_urls_from_page(base_url)
                for sample_url in page_samples:
                    # Process each sample URL
                    project = await self.process_documentation_page(sample_url)
                    if project:
                        samples.append(project)
        
        # Process all documentation URLs for samples
        doc_urls = discovered_urls.get('documentation', set())
        for url in doc_urls:
            # Skip if URL is already processed
            if any(s.url == url for s in samples):
                continue
            
            # Check if this is a sample page
            project = await self.process_documentation_page(url)
            if project:
                samples.append(project)
                logger.info(f"Found sample: {project.title}")
        
        logger.info(f"Discovered {len(samples)} total samples")
        return samples

    def _update_cache(self, project: ProjectResource):
        """Update the cache with latest project status"""
        try:
            samples = []
            if self.samples_cache.exists():
                cache_data = json.loads(self.samples_cache.read_text())
                samples = [ProjectResource(**item) for item in cache_data]

            # Update or add project
            updated = False
            for i, sample in enumerate(samples):
                if sample.url == project.url:
                    samples[i] = project
                    updated = True
                    break
            if not updated:
                samples.append(project)

            # Save updated cache using model_dump
            cache_data = [s.model_dump() for s in samples]
            self.samples_cache.write_text(json.dumps(cache_data, indent=2))
            
        except Exception as e:
            logger.error(f"Error updating cache: {str(e)}")
            # Backup corrupted cache
            if self.samples_cache.exists():
                backup = self.samples_cache.with_suffix('.json.bak')
                self.samples_cache.rename(backup)
                logger.info(f"Backed up corrupted cache to {backup}")
            # Start fresh
            self.samples_cache.write_text('[]')

    def clear_cache(self):
        """Clear all cache files"""
        logger.info("Clearing cache files...")
        cache_files = [
            self.url_cache,
            self.samples_cache,
            self.doc_cache,
            self.analysis_cache
        ]
        
        for cache_file in cache_files:
            if cache_file.exists():
                logger.info(f"Removing {cache_file}")
                cache_file.unlink()
                
        logger.info("Cache cleared")

    def inspect_cache(self):
        """Inspect and report on cache contents"""
        logger.info("\nCache Inspection:")
        
        if self.samples_cache.exists():
            try:
                cache_data = json.loads(self.samples_cache.read_text())
                logger.info(f"\nSamples Cache:")
                logger.info(f"Total samples: {len(cache_data)}")
                
                downloaded = sum(1 for s in cache_data if s.get('downloaded', False))
                logger.info(f"Downloaded: {downloaded}")
                logger.info(f"Not downloaded: {len(cache_data) - downloaded}")
                
                # Show sample details
                logger.info("\nSample Details:")
                for sample in cache_data:
                    status = "Downloaded" if sample.get('downloaded') else "Not Downloaded"
                    logger.info(f"- {sample['title']}: {status}")
                    if sample.get('local_path'):
                        path = Path(sample['local_path'])
                        if not path.exists():
                            logger.warning(f"  Warning: Path does not exist: {path}")
            except json.JSONDecodeError:
                logger.error("Samples cache is corrupted")
        else:
            logger.info("No samples cache found")

    async def _extract_doc_content(self, url: str) -> Dict:
        """Extract content from documentation page"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Get title
                title_elem = soup.find(['h1', 'title'])
                title = title_elem.get_text(strip=True) if title_elem else url.split('/')[-1]
                
                # Get introduction
                intro_elem = soup.find('div', class_='introduction')
                intro = intro_elem.get_text(strip=True) if intro_elem else None
                
                # Look for sample downloads
                sample_links = soup.find_all('a', href=lambda x: x and (
                    'sample' in x.lower() or 
                    x.endswith('.zip') or 
                    '/documentation/visionos/' in x
                ))
                
                samples = []
                for link in sample_links:
                    href = link.get('href', '')
                    if href:
                        samples.append({
                            'url': self._make_absolute_url(href),
                            'title': link.get_text(strip=True) or href.split('/')[-1]
                        })
                
                return {
                    'title': title,
                    'url': url,
                    'introduction': intro,
                    'samples': samples
                }
                
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return None

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