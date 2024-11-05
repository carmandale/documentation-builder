from pathlib import Path
import logging
from typing import Dict, Set, Optional, List
from bs4 import BeautifulSoup
import aiohttp
import re
from dataclasses import dataclass
import json
from collections import defaultdict
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

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
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                content = await page.content()
                
                # Save debug content
                filename = url.split('/')[-1] or 'visionos'
                debug_file = self.debug_dir / f"{filename}.html"
                debug_file.write_text(content)
                logger.info(f"Saved HTML to {debug_file}")
                
                # Parse content
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    
                    # Categorize URLs
                    if '/documentation/' in href:
                        logger.info(f"Found documentation link: {href}")
                        links['documentation'].add(self._make_absolute_url(href))
                    elif '/videos/' in href or '/wwdc/' in href:
                        logger.info(f"Found videos link: {href}")
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
                
                # Parse content
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find sections
                sections = soup.find_all(['h1', 'h2', 'h3'])
                
                # Find topics
                topics = soup.find_all(class_='topic')
                
                # Find sample code
                samples = soup.find_all(class_='sample-code')
                
                structure = {
                    'sections': len(sections),
                    'topics': len(topics),
                    'samples': len(samples)
                }
                
                await browser.close()
                
                logger.info(f"Found {structure['sections']} sections, {structure['topics']} topics, and {structure['samples']} samples")
                
                return structure
                
        except Exception as e:
            logger.error(f"Error analyzing structure of {url}: {str(e)}")
            return {}

    async def process_documentation_page(self, url: str) -> Optional[ProjectResource]:
        """Process a documentation page to find downloadable projects"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Convert relative URLs to absolute
                if not url.startswith('http'):
                    url = f"{self.BASE_URL}{url}"
                    
                await page.goto(url)
                
                # Look for download link
                download_links = await page.query_selector_all('a[href*=".zip"]')
                for link in download_links:
                    href = await link.get_attribute('href')
                    absolute_href = self._make_absolute_url(href)
                    logger.info(f"Found download URL: {absolute_href}")
                    
                    # Get project title
                    title_elem = await page.query_selector('h1')
                    title = await title_elem.text_content() if title_elem else url.split('/')[-1]
                    
                    await browser.close()
                    return ProjectResource(
                        title=title,
                        url=url,
                        download_url=absolute_href
                    )
                
                await browser.close()
                
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
        
        return None

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