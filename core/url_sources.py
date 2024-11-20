from pathlib import Path
from typing import Dict, Set, Optional, List, Any
from bs4 import BeautifulSoup
import aiohttp
import re
from dataclasses import dataclass
import json
from collections import defaultdict
from playwright.async_api import async_playwright, Page
import time
import asyncio
from utils.logging import logger
from core.config import TEST_SAMPLE_COUNT, BASE_URLS, MAX_CRAWL_DEPTH
import zipfile
import io
from datetime import datetime, UTC
from models.base import ProjectResource
from core.serialization import JSONSerializer

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

    # Documentation content selectors
    DOCUMENTATION_SELECTORS = {
        'title': ['.topictitle h1', '.documentation-hero h1'],
        'type': ['.eyebrow', '.topictitle .eyebrow'],
        'description': ['.abstract.content', '.doc-content .description'],
        'availability': ['.availability span.platform', '.summary-section.availability .platform'],
        'code_blocks': ['.declarations-container pre.source', '.declaration-list pre.source'],
        'navigation_path': ['.nav-menu-items.hierarchy .nav-menu-item a', '.breadcrumbs-list li a'],
        'parameters': ['.parameters dl', '.parameters-section dl'],
        'relationships': ['.contenttable-section .link-block'],
        'examples': ['.example-container', '.sample-code'],
        'metadata': {
            'crawl_timestamp': datetime.now(UTC).isoformat(),
            'format_version': '1.1',
            'source': 'Apple Developer Documentation',
            'extraction_status': 'complete'
        }
    }

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

        self.logged_samples = set()

        # Add new cache paths without modifying existing ones
        self.documentation_content_dir = self.cache_dir / 'documentation'
        self.documentation_content_dir.mkdir(exist_ok=True)
        
        # Add new cache file for documentation content
        self.documentation_content_cache = self.cache_dir / 'documentation_content.json'
        if not self.documentation_content_cache.exists():
            self.documentation_content_cache.write_text(json.dumps({
                'cached_at': datetime.now(UTC).isoformat(),
                'pages': {}
            }))

    def is_relevant_url(self, url: str) -> bool:
        """Check if URL is relevant for visionOS development"""
        url_lower = url.lower()
        
        # Direct visionOS content
        if "/documentation/visionos" in url_lower or "/visionos" in url_lower:
            logger.debug(f"Found visionOS URL: {url}")
            return True
            
        # Include design guidelines
        if "/design/human-interface-guidelines" in url_lower:
            logger.debug(f"Found design guidelines URL: {url}")
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
        """Get documentation links and cache pages"""
        links = defaultdict(set)
        processed_urls = set()
        
        try:
            logger.info(f"\nStarting documentation link discovery from: {base_url}")
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                logger.debug("Browser launched successfully")
                
                # Step 1: Initial page setup
                collector_page = await browser.new_page()
                try:
                    logger.debug(f"Navigating to base URL: {base_url}")
                    await collector_page.goto(base_url)
                    await collector_page.wait_for_load_state('networkidle')
                    
                    # Collect initial URLs
                    all_links = await collector_page.query_selector_all('a[href]')
                    urls_to_process = set()
                    
                    for link in all_links:
                        href = await link.get_attribute('href')
                        if href:
                            abs_url = self._make_absolute_url(href)
                            if self.is_relevant_url(abs_url):
                                urls_to_process.add(abs_url)
                                if 'introductory-visionos-samples' in abs_url:
                                    logger.debug(f"Found intro samples page: {abs_url}")
                
                    logger.info(f"Found {len(urls_to_process)} relevant URLs to process")
                    
                finally:
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
                        
                        # Special handling for intro samples page
                        if 'introductory-visionos-samples' in url:
                            logger.info(f"Processing intro samples page: {url}")
                            
                            # Debug: Save the page content
                            content = await page.content()
                            debug_path = self.debug_dir / "intro_samples_page.html"
                            debug_path.write_text(content)
                            logger.debug(f"Saved intro page content to {debug_path}")
                            
                            # Find all sample page links
                            sample_page_links = await page.query_selector_all('div.section-content a.link')
                            logger.debug(f"Found {len(sample_page_links)} sample page links")
                            
                            # Visit each sample page
                            for link in sample_page_links:
                                href = await link.get_attribute('href')
                                if href:
                                    sample_page_url = self._make_absolute_url(href)
                                    logger.debug(f"Visiting sample page: {sample_page_url}")
                                    
                                    # Create new page for each sample
                                    sample_page = await browser.new_page()
                                    try:
                                        await sample_page.goto(sample_page_url)
                                        await sample_page.wait_for_load_state('networkidle')
                                        
                                        # Use the same selector that works for other samples
                                        download_buttons = await sample_page.query_selector_all('a.button-cta.sample-download')
                                        for button in download_buttons:
                                            download_href = await button.get_attribute('href')
                                            if download_href and 'docs-assets.developer.apple.com' in download_href and download_href.endswith('.zip'):
                                                logger.info(f"Found sample download from intro page: {download_href}")
                                                links['samples'].add(self._make_absolute_url(download_href))
                                    finally:
                                        await sample_page.close()
                        
                        # Also get links with {} icons
                        nav_items = await page.query_selector_all('article.article-content a')
                        for item in nav_items:
                            text = await item.text_content()
                            if text and '{' in text:
                                href = await item.get_attribute('href')
                                if href:
                                    sample_url = self._make_absolute_url(href)
                                    if sample_url not in processed_urls:
                                        # Create a new page for each sample
                                        sample_page = await browser.new_page()
                                        try:
                                            await sample_page.goto(sample_url)
                                            await sample_page.wait_for_load_state('networkidle')
                                            
                                            # Now look for the actual download button on the sample page
                                            download_buttons = await sample_page.query_selector_all('a.button-cta.sample-download')
                                            for button in download_buttons:
                                                download_href = await button.get_attribute('href')
                                                if download_href and 'docs-assets.developer.apple.com' in download_href and download_href.endswith('.zip'):
                                                    logger.info(f"Found sample download from intro page: {download_href}")
                                                    links['samples'].add(self._make_absolute_url(download_href))
                                        finally:
                                            await sample_page.close()
                        
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
                
                # Add caching for discovered URLs:
                for category, urls in links.items():
                    if category in ['documentation', 'frameworks', 'tools']:
                        for url in urls:
                            await self.cache_documentation_page(url, category)
                        
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
        try:
            relationships = {}
            if self.doc_cache.exists():
                relationships = json.loads(self.doc_cache.read_text())
            
            relationship_data = {
                'sample_url': project.download_url,
                'documentation_url': project.documentation_url,
                'documentation_title': project.documentation_title,
                'cached_at': datetime.now(UTC).isoformat(),
                'doc_type': self._categorize_doc_url(project.documentation_url)
            }
            
            relationships[project.title] = relationship_data
            
            self.doc_cache.write_text(json.dumps(relationships, indent=2))
            logger.debug(f"Cached documentation relationship for {project.title}")
            
        except Exception as e:
            logger.error(f"Error caching relationship for {project.title}: {e}")

    def _categorize_doc_url(self, url: str) -> str:
        """Categorize documentation URL by type"""
        if not url:
            return 'unknown'
        
        if '/documentation/visionos/' in url:
            return 'visionos'
        elif '/documentation/realitykit/' in url:
            return 'realitykit'
        elif '/documentation/swiftui/' in url:
            return 'swiftui'
        elif '/documentation/arkit/' in url:
            return 'arkit'
        elif '/design/' in url:
            return 'design'
        return 'other'

    async def download_project(self, project: ProjectResource) -> bool:
        """Download and extract a project"""
        if not project.download_url:
            return False
            
        # Check if already downloaded
        project_name = re.sub(r'[^\w\-_]', '_', project.title)
        project_dir = self.projects_dir / project_name
        if project_dir.exists():
            project.mark_downloaded(project_dir)
            logger.debug(f"Project already downloaded: {project_dir}")
            return True
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(project.download_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # Create project directory
                        project_dir = self.projects_dir / project_name
                        project_dir.mkdir(exist_ok=True)
                        
                        # Extract zip content
                        with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
                            zip_ref.extractall(project_dir)
                            
                        project.mark_downloaded(project_dir)
                        self._cache_doc_relationship(project)
                        return True
                        
        except Exception as e:
            logger.error(f"Error downloading project: {str(e)}")
            
        return False

    def _normalize_url(self, url: str) -> str:
        """Normalize a URL by removing fragments and query parameters"""
        # Remove fragment
        url = url.split('#')[0]
        # Remove query parameters
        url = url.split('?')[0]
        # Ensure absolute URL
        if url.startswith('/'):
            url = self.BASE_URL + url
        return url

    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URLs to absolute URLs"""
        if url.startswith('/'):
            return self.BASE_URL + url
        elif url.startswith('http'):
            return url
        else:
            return self.BASE_URL + '/' + url

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
            cache_time = datetime.fromisoformat(cache_data.get('cached_at', '1970-01-01T00:00:00+00:00'))
            age = datetime.now(UTC) - cache_time
            
            # Add size check
            if len(cache_data.get('samples', [])) == 0:
                logger.warning("Cache exists but contains no samples")
                return False
                
            return age.days < 1
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Cache validation error: {str(e)}")
            return False

    def _load_from_cache(self) -> List[ProjectResource]:
        """Load samples from cache"""
        try:
            cache_data = json.loads(self.samples_cache.read_text())
            return [ProjectResource.model_validate(p) for p in cache_data.get('samples', [])]
        except Exception as e:
            logger.error(f"Error loading cache: {str(e)}")
            return []

    def _update_cache(self, new_samples: List[ProjectResource]):
        """Update samples cache by merging with existing samples"""
        try:
            existing_samples = self._load_from_cache()
            
            # Create a dict of existing samples by URL for easy lookup
            existing_by_url = {s.url: s for s in existing_samples}
            
            # Update/add new samples
            for sample in new_samples:
                existing_by_url[sample.url] = sample
                
            # Create updated cache data
            cache_data = {
                'cached_at': datetime.now(UTC).isoformat(),
                'samples': [s.model_dump() for s in existing_by_url.values()]
            }
            
            # Use serializer to save cache
            JSONSerializer.save_json(cache_data, self.samples_cache)
            
            logger.info(f"Successfully cached {len(new_samples)} samples (Total: {len(existing_by_url)})")
            logger.debug(f"Cache updated at: {cache_data['cached_at']}")
            
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
        if self.samples_cache.exists():
            try:
                cache_data = json.loads(self.samples_cache.read_text())
                samples = cache_data.get('samples', [])
                
                logger.info("\nSamples Cache:")
                logger.info(f"Total samples: {len(samples)}")
                downloaded = sum(1 for s in samples if s.get('downloaded', False))
                logger.info(f"Downloaded: {downloaded}")
                logger.info(f"Not downloaded: {len(samples) - downloaded}")
                
                logger.info("\nSample Details:")
                for i, sample in enumerate(samples, 1):
                    status = "Downloaded" if sample.get('downloaded') else "Not Downloaded"
                    logger.info(f"{i:2d}. {sample.get('title')}: {status}")
                    
            except json.JSONDecodeError:
                logger.error("Samples cache is corrupted")

        if self.doc_cache.exists():
            try:
                doc_data = json.loads(self.doc_cache.read_text())
                
                logger.info("\nDocumentation Links Summary:")
                logger.debug(f"Found {len(doc_data)} documentation links")
                
                url_types = defaultdict(int)
                for _, data in doc_data.items():
                    url = data.get('documentation_url', '')
                    if url:
                        if '/documentation/visionos/' in url:
                            url_types['visionos'] += 1
                        elif '/documentation/realitykit/' in url:
                            url_types['realitykit'] += 1
                        elif '/documentation/swiftui/' in url:
                            url_types['swiftui'] += 1
                        elif '/documentation/arkit/' in url:
                            url_types['arkit'] += 1
                        else:
                            url_types['other'] += 1
                
                for doc_type, count in url_types.items():
                    logger.info(f"- {doc_type}: {count} URLs")
                    
            except Exception as e:
                logger.error(f"Error analyzing documentation cache: {str(e)}")

        # Add documentation content inspection
        try:
            cache_data = self._load_doc_content_cache()
            pages = cache_data.get('pages', {})
            
            logger.info("\nDocumentation Pages Cache:")
            logger.info(f"Total cached pages: {len(pages)}")
            
            # Count by category
            categories = defaultdict(int)
            for data in pages.values():
                categories[data.get('category', 'unknown')] += 1
                
            for category, count in categories.items():
                logger.info(f"- {category}: {count} pages")
                
            # Show sample-documentation relationships
            relationships = self._get_sample_doc_relationships()
            logger.info(f"\nSample-Documentation Relationships: {len(relationships)}")
            for sample, docs in relationships.items():
                logger.info(f"- {sample}: {len(docs)} documentation pages")
                
        except Exception as e:
            logger.error(f"Error inspecting documentation cache: {str(e)}")

    def _get_sample_doc_relationships(self) -> Dict[str, List[str]]:
        """Get relationships between samples and documentation"""
        relationships = defaultdict(list)
        
        try:
            if self.doc_cache.exists():
                doc_data = json.loads(self.doc_cache.read_text())
                for sample, data in doc_data.items():
                    if doc_url := data.get('documentation_url'):
                        relationships[sample].append(doc_url)
        except Exception as e:
            logger.error(f"Error getting sample-doc relationships: {str(e)}")
            
        return relationships

    async def cache_documentation_page(self, url: str, category: str = 'documentation', visited_urls: Set[str] = None, current_depth: int = 0, max_depth: int = None) -> bool:
        """Cache a documentation page with full dynamic content and recursively process child pages
        
        Args:
            url: The documentation page URL to cache
            category: The category of documentation
            visited_urls: Set of already visited URLs to prevent loops
            current_depth: Current recursion depth
            max_depth: Maximum depth to traverse (default MAX_CRAWL_DEPTH)
        """
        if max_depth is None:
            max_depth = MAX_CRAWL_DEPTH
            
        if visited_urls is None:
            visited_urls = set()
            self.depth_stats = defaultdict(set)  # Track URLs at each depth
            
        if url in visited_urls:
            logger.debug(f"Skipping already visited URL: {url}")
            return True
            
        if current_depth > max_depth:
            logger.debug(f"Reached max depth ({max_depth}) at URL: {url}")
            return True
            
        visited_urls.add(url)
        self.depth_stats[current_depth].add(url)
        
        try:
            logger.info(f"\nCaching documentation page ({category}) [Depth {current_depth}/{max_depth}]: {url}")
            safe_name = re.sub(r'[^\w\-_]', '_', url.split('/')[-1])
            file_path = self.documentation_content_dir / f"{safe_name}.json"
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                try:
                    # Navigate and wait for dynamic content
                    logger.debug(f"Navigating to: {url}")
                    await page.goto(url)
                    await page.wait_for_load_state('networkidle')
                    
                    # Save raw HTML for debugging
                    debug_path = self.debug_dir / f"doc_page_{safe_name}.html"
                    debug_path.write_text(await page.content())
                    logger.debug(f"Saved raw HTML to {debug_path}")
                    
                    # Extract current page content
                    content = await self._extract_page_content(page, url, category)
                    
                    # Save the content
                    file_path.write_text(json.dumps(content, indent=2))
                    
                    # Update cache index
                    cache_data = self._load_doc_content_cache()
                    cache_data['pages'][url] = {
                        'local_path': str(file_path),
                        'category': category,
                        'cached_at': datetime.now(UTC).isoformat(),
                        'title': content.get('title', ''),
                        'type': content.get('type', ''),
                        'description': content.get('description', ''),
                        'child_pages': content.get('child_pages', [])
                    }
                    self._save_doc_content_cache(cache_data)
                    
                    # Visit each child page
                    for child_url in content.get('child_pages', []):
                        if child_url not in visited_urls:
                            logger.debug(f"Visiting child page: {child_url}")
                            child_page = await browser.new_page()
                            try:
                                await self.cache_documentation_page(
                                    child_url, 
                                    category, 
                                    visited_urls,
                                    current_depth + 1,
                                    max_depth
                                )
                            finally:
                                await child_page.close()
                    
                    logger.info(f"Successfully cached documentation page: {content.get('title', url)}")
                    logger.debug(f"Content extracted: {json.dumps(content, indent=2)}")
                    return True
                    
                finally:
                    await page.close()
                    await browser.close()
                    
        except Exception as e:
            logger.error(f"Error caching documentation page {url}: {str(e)}")
            logger.debug("Error details:", exc_info=True)
            return False

        # After processing all child pages, log depth statistics if we're at the root
        if current_depth == 0:
            logger.info("\n=== Documentation Crawl Statistics ===")
            total_pages = sum(len(urls) for urls in self.depth_stats.values())
            logger.info(f"Total pages processed: {total_pages}")
            for depth, urls in sorted(self.depth_stats.items()):
                logger.info(f"Depth {depth}: {len(urls)} pages")
                for url in urls:
                    logger.debug(f"  - {url}")
            logger.info("===================================\n")

    async def _extract_page_content(self, page: Page, url: str, category: str) -> Dict[str, Any]:
        """Extract all relevant content from a documentation page."""
        try:
            content = {}
            
            # Extract title
            title_element = await page.query_selector('h1')
            if title_element:
                content['title'] = await title_element.text_content()
                
            # Extract description
            desc_element = await page.query_selector('.description')
            if desc_element:
                content['description'] = await desc_element.text_content()
                
            # Extract declaration
            decl_element = await page.query_selector('.declaration, .swift')
            if decl_element:
                swift_text = await decl_element.text_content()
                formatted_html = await decl_element.inner_html()
                content['declaration'] = {
                    'swift': swift_text.strip() if swift_text else '',
                    'formatted': formatted_html.strip() if formatted_html else ''
                }
                
            # Extract parameters
            params_section = await page.query_selector('.parameters')
            if params_section:
                parameters = []
                param_items = await params_section.query_selector_all('dt, dd')
                
                current_param = None
                for item in param_items:
                    tag_name = await (await item.get_property('tagName')).json_value()
                    text_content = await item.text_content()
                    
                    if tag_name.lower() == 'dt':
                        if current_param:
                            parameters.append(current_param)
                        current_param = {'name': text_content.strip()}
                    elif tag_name.lower() == 'dd' and current_param:
                        current_param['description'] = text_content.strip()
                
                if current_param:
                    parameters.append(current_param)
                    
                content['parameters'] = parameters
            
            return content
            
        except Exception as e:
            logger.error(f"Error extracting page content: {str(e)}")
            logger.debug("Error details:", exc_info=True)
            return {}

    def _load_doc_content_cache(self) -> dict:
        """Load documentation content cache"""
        try:
            if self.documentation_content_cache.exists():
                return json.loads(self.documentation_content_cache.read_text())
        except Exception as e:
            logger.error(f"Error loading documentation cache: {str(e)}")
        
        return {'cached_at': datetime.now(UTC).isoformat(), 'pages': {}}

    def _save_doc_content_cache(self, cache_data: dict):
        """Save documentation content cache"""
        try:
            self.documentation_content_cache.write_text(json.dumps(cache_data, indent=2))
        except Exception as e:
            logger.error(f"Error saving documentation cache: {str(e)}")

    async def search_documentation(self, query: str) -> List[Dict]:
        """Search through cached documentation"""
        results = []
        try:
            cache_data = self._load_doc_content_cache()
            
            for url, page_info in cache_data['pages'].items():
                try:
                    file_path = Path(page_info['local_path'])
                    if not file_path.exists():
                        continue
                        
                    content = json.loads(file_path.read_text())
                    
                    # Search in main documentation
                    doc_text = content.get('documentation', '').lower()
                    if query.lower() in doc_text:
                        results.append({
                            'url': url,
                            'title': content.get('title', ''),
                            'type': 'documentation',
                            'match': 'Documentation content match'
                        })
                    
                    # Search in API details
                    for api in content.get('api_details', []):
                        api_text = f"{api.get('name', '')} {api.get('description', '')}".lower()
                        if query.lower() in api_text:
                            results.append({
                                'url': url,
                                'title': content.get('title', ''),
                                'type': 'api',
                                'api_name': api.get('name', ''),
                                'api_description': api.get('description', ''),
                                'api_example': api.get('example', '')
                            })
                            
                except Exception as e:
                    logger.error(f"Error searching file {file_path}: {str(e)}")
                    
            return results
            
        except Exception as e:
            logger.error(f"Error searching documentation: {str(e)}")
            return []

class URLSources:
    """Simple URL management class"""
    def __init__(self):
        self.urls = defaultdict(set)
        
    def add_url(self, url: str, category: str):
        # Normalize URL before adding
        normalized_url = url.strip().rstrip('/')
        if normalized_url not in self.urls[category]:
            self.urls[category].add(normalized_url)
            logger.debug(f"Added {category} URL: {normalized_url}")
        
    def get_urls(self, category: str = None) -> Set[str]:
        if category:
            return self.urls.get(category, set())
        return set().union(*self.urls.values())