from typing import List, Dict, Set, Optional, Tuple
from pathlib import Path
import json
import logging
import aiohttp
import asyncio
from dataclasses import dataclass
from enum import Enum
import zipfile
import io
from bs4 import BeautifulSoup
from datetime import datetime, UTC
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class SourceType(Enum):
    OFFICIAL_DOC = "official_documentation"
    SAMPLE_CODE = "sample_code"
    TUTORIAL = "tutorial"
    WWDC = "wwdc"
    COMMUNITY = "community"

class ResourceType(Enum):
    DOC_PAGE = "documentation_page"
    SAMPLE_CODE = "sample_code"
    XCODE_PROJECT = "xcode_project"
    TUTORIAL = "tutorial"

@dataclass
class DocumentationSource:
    url: str
    source_type: SourceType
    description: str
    verified: bool = False

@dataclass
class DocumentationResource:
    url: str
    resource_type: ResourceType
    download_url: Optional[str] = None  # For Xcode projects
    local_path: Optional[Path] = None

@dataclass
class ProjectResource:
    """Represents a downloadable project resource"""
    doc_url: str  # Documentation page URL
    download_url: str  # Direct download URL
    title: str  # Project title
    description: str  # Project description
    requirements: Dict[str, str]  # e.g., {'visionOS': '2.0+', 'Xcode': '16.0+'}
    local_path: Optional[Path] = None

class DocumentationURLCollector:
    """Collects and manages documentation URLs and associated resources"""
    
    # Core Apple documentation
    APPLE_DOCS = {
        'documentation': 'https://developer.apple.com/documentation/visionos',
        'wwdc': 'https://developer.apple.com/videos/wwdc2024/?q=visionos'
    }
    
    # Known working sample code repositories
    SAMPLE_CODE_SOURCES = [
        DocumentationSource(
            url="https://github.com/apple/sample-code-visionos",
            source_type=SourceType.SAMPLE_CODE,
            description="Official Apple VisionOS samples"
        ),
        # Add more sample code repositories here
    ]
    
    # Community tutorials and resources
    COMMUNITY_SOURCES = [
        DocumentationSource(
            url="https://www.hackingwithswift.com/visionos",
            source_type=SourceType.TUTORIAL,
            description="Hacking with Swift VisionOS tutorials"
        ),
        # Add more community sources here
    ]
    
    def __init__(self, base_dir: Path = Path('data')):
        self.base_dir = base_dir
        self.docs_dir = base_dir / 'docs'
        self.projects_dir = base_dir / 'projects'
        self.cache_file = base_dir / 'url_cache.json'
        self.projects: List[ProjectResource] = []
        
        # Create directories
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    async def process_documentation_page(self, url: str) -> Optional[ProjectResource]:
        """Extract project information and download URL from a documentation page"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            
            try:
                page = await context.new_page()
                await page.goto(url, wait_until='networkidle')
                
                # Wait for the download button to be visible
                download_button = await page.query_selector('a.button-cta.sample-download')
                if not download_button:
                    logger.error("No download button found")
                    # Save page content for debugging
                    content = await page.content()
                    debug_file = self.docs_dir / f"debug_{url.split('/')[-1]}.html"
                    debug_file.write_text(content)
                    logger.info(f"Saved debug HTML to {debug_file}")
                    return None
                
                # Get button properties
                download_url = await download_button.get_attribute('href')
                
                # Get page title
                title_elem = await page.query_selector('h1')
                title = await title_elem.text_content() if title_elem else "Untitled"
                
                # Get description
                desc_elem = await page.query_selector('h1 + p')
                description = await desc_elem.text_content() if desc_elem else ""
                
                logger.info(f"Found download URL: {download_url}")
                
                return ProjectResource(
                    doc_url=url,
                    download_url=download_url,
                    title=title,
                    description=description,
                    requirements={
                        'visionOS': '2.0+',
                        'Xcode': '15.0+'
                    }
                )
                
            except Exception as e:
                logger.error(f"Error processing documentation page {url}: {str(e)}")
                return None
            finally:
                await browser.close()
    
    async def download_project(self, resource: ProjectResource):
        """Download and extract project files"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(resource.download_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # Create project directory
                        project_dir = self.projects_dir / resource.title.lower().replace(' ', '-')
                        project_dir.mkdir(exist_ok=True)
                        
                        # Save project metadata
                        metadata = {
                            'title': resource.title,
                            'description': resource.description,
                            'doc_url': resource.doc_url,
                            'requirements': resource.requirements,
                            'downloaded_at': datetime.now(UTC).isoformat()
                        }
                        
                        with open(project_dir / 'metadata.json', 'w') as f:
                            json.dump(metadata, f, indent=2)
                        
                        # Extract project files
                        with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
                            zip_ref.extractall(project_dir)
                        
                        resource.local_path = project_dir
                        logger.info(f"Downloaded project to {project_dir}")
                        
            except Exception as e:
                logger.error(f"Error downloading project {resource.download_url}: {str(e)}")
    
    def add_documentation_urls(self, urls: List[str]):
        """Add official documentation URLs"""
        for url in urls:
            resource = DocumentationResource(
                url=url,
                resource_type=ResourceType.DOC_PAGE
            )
            
            # Check for associated sample code
            if "sample-code" in url or any(sample in url.lower() for sample in 
                ['creating-', 'building-', 'implementing-', 'displaying-']):
                # Sample code URLs typically have a download link
                download_url = f"{url}/download"  # We'll need to verify this pattern
                
                project_resource = DocumentationResource(
                    url=url,
                    resource_type=ResourceType.XCODE_PROJECT,
                    download_url=download_url
                )
                
                self.resources.append(project_resource)
            
            self.resources.append(resource)
    
    async def verify_urls(self, urls: List[str]) -> List[str]:
        """Verify URLs are accessible"""
        valid_urls = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                try:
                    async with session.head(url) as response:
                        if response.status == 200:
                            valid_urls.append(url)
                            logger.info(f"Verified URL: {url}")
                        else:
                            logger.warning(f"Invalid URL (status {response.status}): {url}")
                except Exception as e:
                    logger.error(f"Error verifying URL {url}: {str(e)}")
        return valid_urls
    
    def add_source(self, source: DocumentationSource):
        """Add a new documentation source"""
        if source.source_type == SourceType.OFFICIAL_DOC:
            self.urls['official'].add(source.url)
        elif source.source_type == SourceType.SAMPLE_CODE:
            self.urls['sample_code'].add(source.url)
        elif source.source_type == SourceType.TUTORIAL:
            self.urls['tutorials'].add(source.url)
        elif source.source_type == SourceType.WWDC:
            self.urls['wwdc'].add(source.url)
        elif source.source_type == SourceType.COMMUNITY:
            self.urls['community'].add(source.url)
        
        self.save_cache()
        logger.info(f"Added new source: {source.url} ({source.source_type.value})")
    
    def get_all_urls(self) -> List[str]:
        """Get all documentation URLs"""
        all_urls = []
        for urls in self.urls.values():
            all_urls.extend(urls)
        return list(set(all_urls))  # Remove duplicates