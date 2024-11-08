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
from datetime import datetime, UTC

@dataclass
class ProjectResource:
    """Represents a downloadable project resource"""
    title: str
    url: str
    download_url: Optional[str] = None
    local_path: Optional[Path] = None
    downloaded: bool = False
    documentation_url: Optional[str] = None
    documentation_title: Optional[str] = None

    def mark_downloaded(self, path: Path):
        self.local_path = path
        self.downloaded = True

class DocumentationURLCollector:
    """Handles documentation URL discovery and sample collection"""
    BASE_URL = "https://developer.apple.com"
    
    # Framework and tool detection
    ESSENTIAL_FRAMEWORKS = {
        'SwiftUI', 'RealityKit', 'ARKit', 'AVFoundation',
        'CoreML', 'Metal', 'WebKit', 'VisionKit', 'Foundation'
    }
    
    REALITY_COMPOSER_TERMS = {
        'reality-composer-pro',
        'reality composer pro',
        'realitycomposerpro'
    }
    
    # Sample detection patterns
    SAMPLE_SELECTORS = [
        'a.sample-download',  # Primary download button
        'a[href*="sample"][href$=".zip"]',
        'a[href*="download"][href$=".zip"]',
        '.sample-card a[href$=".zip"]'
    ]

    def __init__(self, base_dir: Path = Path('data')):
        # Directory setup
        self.base_dir = base_dir
        self.projects_dir = base_dir / 'projects'
        self.debug_dir = base_dir / 'debug'
        self.cache_dir = base_dir / 'cache'
        
        # Cache files
        self.url_cache = self.cache_dir / 'url_cache.json'
        self.samples_cache = self.cache_dir / 'discovered_samples.json'
        self.doc_cache = self.cache_dir / 'documentation_cache.json'
        self.analysis_cache = self.cache_dir / 'analysis_cache.json'
        
        # Create directories
        for directory in [self.projects_dir, self.debug_dir, self.cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize cache files
        for cache_file in [self.url_cache, self.samples_cache, self.doc_cache, self.analysis_cache]:
            if not cache_file.exists():
                cache_file.write_text('{}')

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
                is_relevant = any(term in url_lower for term in [
                    "visionos", "spatial", "3d", "reality", "immersive"
                ])
                if is_relevant:
                    logger.debug(f"Found relevant framework URL ({framework}): {url}")
                return is_relevant
                
        return False

    async def get_documentation_links(self, base_url: str) -> Dict[str, Set[str]]:
        """Get categorized documentation links with improved page handling"""
        links = defaultdict(set)
        processed_urls = set()
        
        try:
            logger.info(f"\nStarting documentation link discovery from: {base_url}")
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                logger.debug("Browser launched successfully")
                
                # Step 1: Collect URLs from base page
                logger.debug(f"Creating initial page for URL collection: {base_url}")
                collector_page = await browser.new_page()
                try:
                    logger.debug(f"Navigating to base URL: {base_url}")
                    await collector_page.goto(base_url)
                    await collector_page.wait_for_load_state('networkidle')
                    
                    logger.debug("Collecting links from base page")
                    all_links = await collector_page.query_selector_all('a[href]')
                    urls_to_process = set()
                    
                    for link in all_links:
                        href = await link.get_attribute('href')
                        if href:
                            abs_url = self._make_absolute_url(href)
                            if self.is_relevant_url(abs_url):
                                urls_to_process.add(abs_url)
                                logger.debug(f"Found relevant URL: {abs_url}")
                    
                    logger.info(f"Found {len(urls_to_process)} relevant URLs to process")
                    
                except Exception as e:
                    logger.error(f"Error collecting URLs from base page: {str(e)}")
                    logger.debug("Error details:", exc_info=True)
                finally:
                    logger.debug("Closing collector page")
                    await collector_page.close()
                
                # Step 2: Process each URL with its own page
                for url in urls_to_process:
                    if url in processed_urls:
                        logger.debug(f"Skipping already processed URL: {url}")
                        continue
                        
                    logger.debug(f"\nProcessing URL: {url}")
                    page = await browser.new_page()
                    try:
                        logger.debug(f"Navigating to: {url}")
                        await page.goto(url)
                        await page.wait_for_load_state('networkidle')
                        
                        # Look for sample download buttons
                        download_buttons = await page.query_selector_all('a.button-cta.sample-download')
                        for button in download_buttons:
                            href = await button.get_attribute('href')
                            if href and 'docs-assets.developer.apple.com' in href and href.endswith('.zip'):
                                logger.info(f"Found sample download: {href}")
                                links['samples'].add(self._make_absolute_url(href))
                        
                        # Track frameworks and tools
                        if "/documentation/visionos" in url.lower():
                            links['documentation'].add(url)
                            logger.debug(f"Added to documentation: {url}")
                        
                        for framework in self.ESSENTIAL_FRAMEWORKS:
                            if f"/documentation/{framework.lower()}" in url.lower():
                                links['frameworks'].add(url)
                                logger.debug(f"Added to frameworks: {url}")
                                break
                        
                        if any(term in url.lower() for term in self.REALITY_COMPOSER_TERMS):
                            links['tools'].add(url)
                            logger.debug(f"Added to tools: {url}")
                        
                        processed_urls.add(url)
                        
                    except Exception as e:
                        logger.error(f"Error processing URL {url}: {str(e)}")
                        logger.debug("Error details:", exc_info=True)
                    finally:
                        logger.debug(f"Closing page for URL: {url}")
                        await page.close()
                
                logger.debug("Closing browser")
                await browser.close()
                
                # Log summary
                logger.info("\nURL Discovery Summary:")
                for category, urls in links.items():
                    logger.info(f"{category}: {len(urls)} URLs found")
                    for url in urls:
                        logger.debug(f"  {category}: {url}")
                
                return dict(links)
                
        except Exception as e:
            logger.error(f"Fatal error in get_documentation_links: {str(e)}")
            logger.debug("Error details:", exc_info=True)
            return dict(links)

    async def _process_page_for_samples(self, page, url: str, links: Dict[str, Set[str]], processed_urls: Set[str]):
        """Process a single page for sample downloads"""
        if url in processed_urls:
            return
            
        try:
            logger.debug("Processing URL: %s", url)
            await page.goto(url)
            processed_urls.add(url)

            # Special handling for introductory samples page
            if 'introductory-visionos-samples' in url:
                logger.info(f"Processing samples page: {url}")
                sample_links = await page.query_selector_all('article a')
                for link in sample_links:
                    href = await link.get_attribute('href')
                    if href:
                        sample_url = self._make_absolute_url(href)
                        if sample_url not in processed_urls:
                            await self._process_page_for_samples(page, sample_url, links, processed_urls)
            
            # Find sample pages from navigation (with {} icons)
            nav_items = await page.query_selector_all('article.article-content a')
            for item in nav_items:
                text = await item.text_content()
                if text and '{' in text:
                    href = await item.get_attribute('href')
                    if href:
                        links['documentation'].add(self._make_absolute_url(href))
            
            # Find direct download links
            for selector in self.SAMPLE_SELECTORS:
                buttons = await page.query_selector_all(selector)
                for button in buttons:
                    href = await button.get_attribute('href')
                    if href and href.endswith('.zip'):
                        links['samples'].add(self._make_absolute_url(href))
            
            # Save debug content
            content = await page.content()
            debug_path = self.debug_dir / f"raw_{url.split('/')[-1]}.html"
            debug_path.write_text(content)
            
            # Process documentation structure
            soup = BeautifulSoup(content, 'html.parser')
            self._analyze_documentation_structure(soup, links)
            
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")

    def _analyze_documentation_structure(self, soup: BeautifulSoup, links: Dict[str, Set[str]]):
        """Analyze documentation page structure"""
        try:
            # Find framework references
            for framework in self.ESSENTIAL_FRAMEWORKS:
                framework_refs = soup.find_all(
                    lambda tag: tag.name in ['p', 'div', 'span', 'a'] and 
                    framework.lower() in tag.text.lower()
                )
                if framework_refs:
                    links['frameworks'].add(framework)
            
            # Find Reality Composer Pro references
            rc_refs = soup.find_all(
                lambda tag: tag.name in ['p', 'div', 'span', 'a'] and
                any(term in tag.text.lower() for term in self.REALITY_COMPOSER_TERMS)
            )
            if rc_refs:
                links['tools'].add('Reality Composer Pro')
                
        except Exception as e:
            logger.error(f"Error analyzing documentation structure: {str(e)}")

    async def discover_all_samples(self) -> List[ProjectResource]:
        """Load or discover all samples"""
        if self._validate_samples_cache():
            return self._load_from_cache()
            
        logger.debug("Cache miss - discovering samples...")
        samples = []
        
        for base_url in BASE_URLS:
            links = await self.get_documentation_links(base_url)
            for url in links.get('samples', set()):
                if self._validate_sample_url(url):
                    project = await self.process_documentation_page(url)
                    if project:
                        samples.append(project)
        
        self._update_cache(samples)
        return samples

    async def process_documentation_page(self, url: str) -> Optional[ProjectResource]:
        """Process a documentation page to create a ProjectResource"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                
                # Get the documentation page title
                title_elem = await page.query_selector('h1')
                title = await title_elem.text_content() if title_elem else url.split('/')[-1]
                
                # Get the download URL if present
                download_button = await page.query_selector('a.sample-download')
                download_url = await download_button.get_attribute('href') if download_button else None
                
                if download_url:
                    # Create ProjectResource with documentation reference
                    project = ProjectResource(
                        title=title,
                        url=url,
                        download_url=self._make_absolute_url(download_url),
                        documentation_url=url,  # Store the documentation URL
                        documentation_title=title  # Store the documentation title
                    )
                    
                    # Cache the relationship
                    self._cache_doc_relationship(project)
                    
                    return project
                    
        except Exception as e:
            logger.error(f"Error processing documentation page {url}: {str(e)}")
            
        return None

    def _cache_doc_relationship(self, project: ProjectResource):
        """Cache the relationship between sample and documentation"""
        relationships = {}
        if self.doc_cache.exists():
            relationships = json.loads(self.doc_cache.read_text())
        
        relationships[project.title] = {
            'sample_url': project.download_url,
            'documentation_url': project.documentation_url,
            'documentation_title': project.documentation_title,
            'cached_at': datetime.now(UTC).isoformat()
        }
        
        self.doc_cache.write_text(json.dumps(relationships, indent=2))

    async def download_project(self, project: ProjectResource) -> bool:
        """Download and extract a project"""
        if not project.download_url:
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(project.download_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # Create project directory
                        project_name = re.sub(r'[^\w\-_]', '_', project.title)
                        project_dir = self.projects_dir / project_name
                        project_dir.mkdir(exist_ok=True)
                        
                        # Extract zip content
                        with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
                            zip_ref.extractall(project_dir)
                            
                        project.mark_downloaded(project_dir)
                        return True
                        
        except Exception as e:
            logger.error(f"Error downloading project: {str(e)}")
            
        return False

    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URLs to absolute URLs"""
        if url.startswith('http'):
            return url
        elif url.startswith('//'):
            return f"https:{url}"
        elif url.startswith('/'):
            return f"{self.BASE_URL}{url}"
        return f"{self.BASE_URL}/{url}"

    def _validate_sample_url(self, url: str) -> bool:
        """Validate if a URL is likely a sample project"""
        return any([
            url.endswith('.zip') and 'docs-assets.developer.apple.com' in url,
            'sample.code' in url.lower() and url.endswith('.zip'),
            'example.code' in url.lower() and url.endswith('.zip')
        ])

    # Cache management methods
    def _validate_samples_cache(self) -> bool:
        """Check if samples cache is valid"""
        try:
            if not self.samples_cache.exists():
                return False
                
            cache_data = json.loads(self.samples_cache.read_text())
            cache_time = cache_data.get('cached_at', 0)
            return time.time() - cache_time < 24 * 60 * 60
            
        except Exception:
            return False

    def _load_from_cache(self) -> List[ProjectResource]:
        """Load samples from cache"""
        try:
            cache_data = json.loads(self.samples_cache.read_text())
            return [ProjectResource(**p) for p in cache_data.get('samples', [])]
        except Exception as e:
            logger.error(f"Error loading cache: {str(e)}")
            return []

    def _update_cache(self, samples: List[ProjectResource]):
        """Update samples cache"""
        try:
            cache_data = {
                'cached_at': time.time(),
                'samples': [vars(s) for s in samples]
            }
            self.samples_cache.write_text(json.dumps(cache_data, indent=2))
        except Exception as e:
            logger.error(f"Error updating cache: {str(e)}")

    def clear_cache(self):
        """Clear all cache files"""
        logger.info("Clearing cache files...")
        for cache_file in [self.url_cache, self.samples_cache, self.doc_cache, self.analysis_cache]:
            if cache_file.exists():
                logger.info(f"Removing {cache_file}")
                cache_file.unlink()
        logger.info("Cache cleared")

    def inspect_cache(self):
        """Inspect and report on cache contents"""
        logger.info("\nCache Inspection:")
        if not self.samples_cache.exists():
            logger.info("No samples cache found")
            return
            
        try:
            cache_data = json.loads(self.samples_cache.read_text())
            logger.info("\nSamples Cache:")
            logger.info(f"Total samples: {len(cache_data)}")
            
            downloaded = sum(1 for s in cache_data if s.get('downloaded', False))
            logger.info(f"Downloaded: {downloaded}")
            logger.info(f"Not downloaded: {len(cache_data) - downloaded}")
            
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