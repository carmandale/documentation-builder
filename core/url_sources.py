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
import zipfile
import io

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
    
    ESSENTIAL_FRAMEWORKS = {
        'SwiftUI',
        'RealityKit', 
        'ARKit',
        'AVFoundation',
        'CoreML',
        'Metal',
        'WebKit',
        'VisionKit',
        'Foundation'
    }
    
    REALITY_COMPOSER_TERMS = {
        'reality-composer-pro',
        'reality composer pro',
        'realitycomposerpro'
    }

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
        if url.startswith('http'):
            return url
        elif url.startswith('//'):
            return f"https:{url}"
        elif url.startswith('/'):
            return f"{self.BASE_URL}{url}"
        else:
            return f"{self.BASE_URL}/{url}"

    def is_relevant_url(self, url: str) -> bool:
        """Check if URL is relevant for visionOS development"""
        url_lower = url.lower()
        
        # Direct visionOS content
        if "/documentation/visionos" in url_lower:
            logger.debug(f"Found visionOS URL: {url}")
            return True
            
        # Reality Composer Pro content
        if any(term in url_lower for term in self.REALITY_COMPOSER_TERMS):
            logger.debug(f"Found Reality Composer Pro URL: {url}")
            return True
            
        # Essential frameworks - only when related to visionOS
        for framework in self.ESSENTIAL_FRAMEWORKS:
            framework_path = f"/documentation/{framework.lower()}"
            if framework_path in url_lower:
                # Check for visionOS relevance
                is_relevant = any(term in url_lower for term in [
                    "visionos", "spatial", "3d", "reality", "immersive"
                ])
                if is_relevant:
                    logger.debug(f"Found relevant framework URL ({framework}): {url}")
                return is_relevant
                
        return False

    async def get_documentation_links(self, base_url: str) -> Dict[str, Set[str]]:
        """Get categorized documentation links"""
        links = defaultdict(set)
        processed_urls = set()
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Process initial page
                await self._process_page_for_samples(page, base_url, links, processed_urls)
                
                # Get all links from the page
                all_links = await page.query_selector_all('a[href]')
                for link in all_links:
                    href = await link.get_attribute('href')
                    if href:
                        abs_url = self._make_absolute_url(href)
                        if self.is_relevant_url(abs_url):
                            await self._process_page_for_samples(page, abs_url, links, processed_urls)
                
                await browser.close()
                
                # Log summary
                logger.debug("\nURL Discovery Summary:")
                for category, urls in links.items():
                    logger.debug(f"{category}: {len(urls)} URLs found")
                
                return dict(links)
                
        except Exception as e:
            logger.error(f"Error getting documentation links: {str(e)}")
            return dict(links)

    async def _process_page_for_samples(self, page, url: str, links: Dict[str, Set[str]], processed_urls: Set[str]):
        """Process a single page for sample downloads"""
        if url in processed_urls:
            return
            
        try:
            logger.debug("Processing URL: %s", url)
            
            # Add navigation timeout and retry logic
            for attempt in range(3):
                try:
                    response = await page.goto(url, wait_until='networkidle', timeout=30000)
                    if response.ok:
                        break
                except Exception as e:
                    logger.warning("Navigation attempt %d failed: %s", attempt + 1, str(e))
                    if attempt == 2:
                        raise
                
            processed_urls.add(url)
            
            # Create new context for each page
            content = await page.content()
            
            # Save debug content
            debug_path = self.debug_dir / f"raw_{url.split('/')[-1]}.html"
            debug_path.write_text(content)
            logger.debug("Saved debug content to %s", debug_path)
            
            # Find direct download buttons
            download_buttons = await page.query_selector_all('a.sample-download')
            logger.debug("Found %d sample-download links", len(download_buttons))
            
            for button in download_buttons:
                href = await button.get_attribute('href')
                if href and href.endswith('.zip'):
                    abs_url = self._make_absolute_url(href)
                    links['samples'].add(abs_url)
                    logger.debug("Found sample download: %s", abs_url)
            
            # Get all links before categorizing
            all_links = await page.query_selector_all('a[href]')
            for link in all_links:
                href = await link.get_attribute('href')
                if href:
                    abs_url = self._make_absolute_url(href)
                    if self.is_relevant_url(abs_url):
                        if 'documentation' in abs_url:
                            links['documentation'].add(abs_url)
                        else:
                            links['other'].add(abs_url)
                            
        except Exception as e:
            logger.error("Error processing page %s: %s", url, str(e))
            logger.debug("Full error details:", exc_info=True)

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
        """Process a documentation page to extract project information"""
        if not url.endswith('.zip'):
            return None
            
        try:
            # Extract title from zip filename
            title = Path(url).stem
            
            # Create ProjectResource
            resource = ProjectResource(
                title=title,
                url=url,
                download_url=url
            )
            
            # Download the zip file using aiohttp instead of playwright
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # Save zip content
                        cache_dir = Path('data/cache/samples')
                        cache_dir.mkdir(parents=True, exist_ok=True)
                        
                        local_path = cache_dir / f"{title}.zip"
                        local_path.write_bytes(content)
                        
                        # Verify zip content
                        try:
                            with zipfile.ZipFile(local_path) as zf:
                                has_source = any(
                                    name.endswith(('.swift', '.h', '.m', '.cpp', '.c', '.mm'))
                                    for name in zf.namelist()
                                )
                                if has_source:
                                    resource.mark_downloaded(local_path)
                                    logger.info(f"Successfully downloaded {title}")
                                    return resource
                                else:
                                    logger.warning(f"No source code files found in {url}")
                                    local_path.unlink()  # Remove invalid zip
                                    return None
                        except zipfile.BadZipFile:
                            logger.error(f"Invalid zip file: {url}")
                            local_path.unlink()  # Remove invalid zip
                            return None
                    else:
                        logger.error(f"Failed to download {url}: {response.status}")
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
        if self._validate_samples_cache():
            return self._load_from_cache()
            
        # Cache miss - discover new samples
        samples = []
        base_url = "https://developer.apple.com/documentation/visionos/"
        
        # Get sample URLs
        sample_urls = await self.get_sample_urls_from_page(base_url)
        
        # Process each sample URL
        for url in sample_urls:
            if self._validate_sample_url(url):
                project = await self.process_documentation_page(url)
                if project:
                    samples.append(project)
                    
        # Update cache
        self._update_cache(samples)
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

    async def get_sample_urls_from_page(self, url: str) -> Set[str]:
        """Get sample URLs from a documentation page"""
        logger.debug("Searching for samples on: %s", url)
        samples = set()
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                start = time.time()
                logger.debug("[Timing] Browser launch: %.2fs", time.time() - start)
                
                page = await browser.new_page()
                await page.goto(url)
                logger.debug("[Timing] Initial page load: %.2fs", time.time() - start)
                
                # Find pages with {} icons in navigation
                nav_items = await page.query_selector_all('article.article-content a')
                for item in nav_items:
                    text = await item.text_content()
                    href = await item.get_attribute('href')
                    if text and '{' in text and href:
                        logger.debug("Found sample page from nav: %s", href)
                        samples.add(self._make_absolute_url(href))
                
                # Check intro samples section
                intro_section = await page.query_selector('text="Introductory visionOS samples"')
                if intro_section:
                    parent = await intro_section.query_selector('xpath=ancestor::section')
                    if parent:
                        links = await parent_section.query_selector_all('a[href]')
                        for link in links:
                            href = await link.get_attribute('href')
                            if href:
                                logger.debug("Found sample from intro section: %s", href)
                                samples.add(self._make_absolute_url(href))
                
                # Look for direct download buttons
                for selector in self.SAMPLE_SELECTORS:
                    buttons = await page.query_selector_all(selector)
                    logger.debug("Found %d elements with selector: %s", len(buttons), selector)
                    for button in buttons:
                        href = await button.get_attribute('href')
                        if href and href.endswith('.zip'):
                            samples.add(self._make_absolute_url(href))
                
                await browser.close()
                return samples
                
        except Exception as e:
            logger.error("Error getting sample URLs: %s", str(e))
            
        return samples

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

    def _validate_sample_url(self, url: str) -> bool:
        """Validate if a URL is likely a sample project"""
        return any([
            url.endswith('.zip') and 'docs-assets.developer.apple.com' in url,
            'sample.code' in url.lower() and url.endswith('.zip'),
            'example.code' in url.lower() and url.endswith('.zip')
        ])

    # Add more sample link selectors
    SAMPLE_SELECTORS = [
        'a.sample-download',
        'a[href*="sample"][href$=".zip"]',
        'a[href*="download"][href$=".zip"]',
        '.sample-card a[href$=".zip"]',
        '.documentation-card a[href$=".zip"]'
    ]

    async def _find_sample_links(self, page):
        """Find sample download links using multiple selectors"""
        sample_links = set()
        for selector in self.SAMPLE_SELECTORS:
            try:
                elements = await page.query_selector_all(selector)
                logger.debug("Found %d elements with selector: %s", len(elements), selector)
                for element in elements:
                    href = await element.get_attribute('href')
                    if href and href.endswith('.zip'):
                        sample_links.add(self._make_absolute_url(href))
            except Exception as e:
                logger.warning("Error with selector %s: %s", selector, str(e))
        return sample_links

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