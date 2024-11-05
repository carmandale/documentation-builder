from typing import List, Dict, Set, Optional, Tuple, Any
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
import re
from urllib.parse import urljoin
from collections import defaultdict

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

class URLRepository:
    """Manages and persists discovered URLs"""
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.urls_file = base_dir / 'urls' / 'discovered_urls.json'
        self.urls_file.parent.mkdir(parents=True, exist_ok=True)
        self.urls = self._load_urls()

    def _load_urls(self) -> Dict[str, Set[str]]:
        """Load existing URLs from disk"""
        if self.urls_file.exists():
            data = json.loads(self.urls_file.read_text())
            # Convert lists back to sets
            return {k: set(v) for k, v in data.items()}
        return {
            'documentation': set(),
            'samples': set(),
            'tutorials': set(),
            'videos': set(),
            'community': set(),
            'other': set()
        }

    def add_url(self, url: str, category: str, metadata: Optional[Dict] = None):
        """Add a new URL with optional metadata"""
        if category not in self.urls:
            self.urls[category] = set()
        
        self.urls[category].add(url)
        self._save_urls()
        
        # Save additional metadata if provided
        if metadata:
            self._save_metadata(url, metadata)

    def _save_urls(self):
        """Save URLs to disk"""
        # Convert sets to lists for JSON serialization
        serializable = {k: list(v) for k, v in self.urls.items()}
        self.urls_file.write_text(json.dumps(serializable, indent=2))

    def _save_metadata(self, url: str, metadata: Dict):
        """Save metadata for a URL"""
        metadata_file = self.base_dir / 'urls' / 'metadata.json'
        existing = {}
        if metadata_file.exists():
            existing = json.loads(metadata_file.read_text())
        
        existing[url] = metadata
        metadata_file.write_text(json.dumps(existing, indent=2))

    def get_urls(self, category: Optional[str] = None) -> Set[str]:
        """Get all URLs or URLs for a specific category"""
        if category:
            return self.urls.get(category, set())
        
        # Return all URLs if no category specified
        all_urls = set()
        for urls in self.urls.values():
            all_urls.update(urls)
        return all_urls

    def merge_sources(self, hardcoded_sources: Dict[str, List[str]]):
        """Merge hardcoded sources with discovered URLs"""
        for category, urls in hardcoded_sources.items():
            for url in urls:
                self.add_url(url, category, {'source': 'hardcoded'})

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
        self.knowledge_dir = base_dir / 'knowledge'
        self.cache_file = base_dir / 'url_cache.json'
        
        # Knowledge bases
        self.pattern_knowledge = KnowledgeBase(self.knowledge_dir / 'patterns.json')
        self.concept_knowledge = KnowledgeBase(self.knowledge_dir / 'concepts.json')
        self.framework_knowledge = KnowledgeBase(self.knowledge_dir / 'frameworks.json')
        
        # Create directories
        for directory in [self.docs_dir, self.projects_dir, self.knowledge_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.url_repository = URLRepository(base_dir)
        
        # Merge hardcoded sources
        self.url_repository.merge_sources({
            'documentation': [self.APPLE_DOCS['documentation']],
            'videos': [self.APPLE_DOCS['wwdc']],
            'samples': [source.url for source in self.SAMPLE_CODE_SOURCES],
            'community': [source.url for source in self.COMMUNITY_SOURCES]
        })
        
        self.analyzer = DocumentationAnalyzer(self.knowledge_dir)
    
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
    
    async def get_documentation_links(self, url: str) -> Dict[str, Set[str]]:
        """Get all documentation links from a page"""
        links = defaultdict(set)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            try:
                await page.goto(url)
                await page.wait_for_selector('#app', timeout=10000)
                await page.wait_for_timeout(1000)
                
                content = await page.content()
                
                # Save debug HTML
                debug_dir = Path('debug')
                debug_dir.mkdir(exist_ok=True)
                filename = url.rstrip('/').split('/')[-1] or 'index'
                debug_file = debug_dir / f"{filename}.html"
                debug_file.write_text(content)
                logger.info(f"Saved HTML to {debug_file}")
                
                soup = BeautifulSoup(content, 'html.parser')
                all_links = soup.find_all('a', href=True)
                
                for link in all_links:
                    href = link.get('href')
                    if not href:
                        continue
                        
                    # Get the link text and any description
                    title = link.get_text(strip=True)
                    description = ""
                    desc_elem = link.find_next('p')
                    if desc_elem:
                        description = desc_elem.get_text(strip=True)
                    
                    # Make sure we have an absolute URL
                    full_url = urljoin(url, href)
                    
                    # Skip navigation/utility links
                    if any(skip in full_url.lower() for skip in ['#ac-gn', 'search', 'account']):
                        continue
                    
                    # Determine category and store link
                    category = 'other'  # Default category
                    
                    if '/documentation/visionos/' in full_url:
                        category = 'documentation'
                    elif '/sample-code/' in full_url or '/tutorials/' in full_url:
                        category = 'samples'
                    elif '/videos/' in full_url or '/wwdc/' in full_url:
                        category = 'videos'
                    elif '/documentation/' in full_url:  # Other documentation
                        category = 'documentation'
                    
                    # Store the link in appropriate category
                    links[category].add(full_url)
                    
                    # Log based on category
                    if category != 'other':
                        logger.info(f"Found {category} link: {full_url}")
                    
                    # Store metadata
                    metadata = {
                        'discovered_at': datetime.now(UTC).isoformat(),
                        'source_url': url,
                        'title': title,
                        'description': description
                    }
                    self.url_repository.add_url(full_url, category, metadata)
                
            except Exception as e:
                logger.error(f"Error processing page {url}: {str(e)}")
                raise  # Re-raise to see the full error in development
            finally:
                await browser.close()
            
            # Log summary of found links
            for category, urls in links.items():
                logger.info(f"Found {len(urls)} {category} links")
            
            return links
    
    async def analyze_documentation_structure(self, url: str) -> Dict[str, Any]:
        """Analyze the structure of a documentation page"""
        structure = {}
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            try:
                await page.goto(url)
                # Wait for navigation to be available
                await page.wait_for_selector('nav[role="navigation"]', timeout=10000)
                
                # Get the rendered content
                content = await page.content()
                
                # Save debug HTML
                debug_dir = Path('debug')
                debug_dir.mkdir(exist_ok=True)
                filename = url.rstrip('/').split('/')[-1] or 'index'
                debug_file = debug_dir / f"{filename}.html"
                debug_file.write_text(content)
                
                # Analyze structure from rendered content
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract sections
                sections = []
                for section in soup.select('h2'):
                    section_id = section.get('id', '')
                    section_title = section.get_text(strip=True)
                    section_content = []
                    
                    # Get content until next h2
                    current = section.find_next_sibling()
                    while current and current.name != 'h2':
                        if current.name == 'a':
                            href = current.get('href')
                            if href:
                                section_content.append({
                                    'type': 'link',
                                    'url': urljoin(url, href),
                                    'title': current.get_text(strip=True)
                                })
                        elif current.name == 'p':
                            section_content.append({
                                'type': 'text',
                                'content': current.get_text(strip=True)
                            })
                        current = current.find_next_sibling()
                    
                    sections.append({
                        'id': section_id,
                        'title': section_title,
                        'content': section_content
                    })
                
                structure['sections'] = sections
                
                # Extract topics from the navigation
                topics = []
                nav = soup.select_one('nav[role="navigation"]')
                if nav:
                    for link in nav.select('a'):
                        href = link.get('href')
                        if href and '/documentation/' in href:
                            topics.append({
                                'url': urljoin(url, href),
                                'title': link.get_text(strip=True)
                            })
                
                structure['topics'] = topics
                
                # Extract any sample code references
                samples = []
                for link in soup.select('a[href*="sample-code"], a[href*="tutorials"]'):
                    href = link.get('href')
                    if href:
                        samples.append({
                            'url': urljoin(url, href),
                            'title': link.get_text(strip=True)
                        })
                
                structure['samples'] = samples
                
                logger.info(f"Found {len(sections)} sections, {len(topics)} topics, and {len(samples)} samples")
                
            except Exception as e:
                logger.error(f"Error analyzing page structure for {url}: {str(e)}")
            finally:
                await browser.close()
        
        return structure
    
    def _extract_keywords(self, text: str) -> set:
        """Extract relevant keywords from text"""
        # Could be enhanced with NLP for better keyword extraction
        keywords = set()
        
        # Common VisionOS concept patterns
        patterns = [
            r'\b\w+Kit\b',  # Match frameworks like RealityKit
            r'\b\w+View\b',  # Match view types
            r'\b\w+Space\b', # Match space types
            r'\b\w+Volume\b', # Match volume types
            r'\b\w+Gesture\b', # Match gesture types
            r'\b3D\s+\w+\b',  # Match 3D concepts
            r'\bAR\s+\w+\b',  # Match AR concepts
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            keywords.update(match.group(0) for match in matches)
        
        return keywords
    
    def _save_doc_structure(self, structure: dict):
        """Save documentation structure to cache"""
        cache_path = self.base_dir / 'doc_structure.json'
        with open(cache_path, 'w') as f:
            # Convert sets to lists for JSON serialization
            serializable_structure = {}
            for section, links in structure.items():
                serializable_links = []
                for link in links:
                    link_copy = link.copy()
                    link_copy['keywords'] = list(link['keywords'])
                    serializable_links.append(link_copy)
                serializable_structure[section] = serializable_links
            
            json.dump(serializable_structure, f, indent=2)
    
    async def learn_from_url(self, url: str, content: str):
        """Learn patterns and concepts from a documentation page"""
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract concepts and their relationships
        concepts = self._extract_concepts(soup)
        self.concept_knowledge.add_concepts(concepts)
        
        # Learn code patterns
        code_blocks = soup.select('pre code')
        for block in code_blocks:
            pattern = self._analyze_code_pattern(block.get_text())
            if pattern:
                self.pattern_knowledge.add_pattern(pattern)
        
        # Extract framework usage
        frameworks = self._extract_framework_usage(soup)
        self.framework_knowledge.add_frameworks(frameworks)
        
        # Update relationships between concepts
        self._update_concept_relationships(concepts)

    def _extract_concepts(self, soup) -> List[Dict]:
        """Extract VisionOS concepts and their descriptions"""
        concepts = []
        
        # Look for concept definitions in headers and strong tags
        for element in soup.select('h1, h2, h3, strong'):
            text = element.get_text(strip=True)
            if self._is_visionos_concept(text):
                description = ""
                next_p = element.find_next('p')
                if next_p:
                    description = next_p.get_text(strip=True)
                
                concepts.append({
                    'name': text,
                    'description': description,
                    'category': self._categorize_concept(text),
                    'related_concepts': self._find_related_concepts(element)
                })
        
        return concepts

    def _analyze_code_pattern(self, code: str) -> Optional[Dict]:
        """Analyze code block for common patterns"""
        pattern = {
            'code': code,
            'frameworks': self._extract_imports(code),
            'pattern_type': self._identify_pattern_type(code),
            'concepts_used': self._extract_used_concepts(code)
        }
        
        if pattern['pattern_type']:
            return pattern
        return None

    def _update_concept_relationships(self, concepts: List[Dict]):
        """Update relationships between concepts based on proximity and usage"""
        for concept in concepts:
            # Find concepts that are frequently used together
            related = self.concept_knowledge.find_related_concepts(concept['name'])
            
            # Update relationship strengths
            for related_concept in related:
                self.concept_knowledge.update_relationship(
                    concept['name'],
                    related_concept,
                    relationship_type='co-occurrence'
                )

    def get_all_urls(self) -> Dict[str, Set[str]]:
        """Get all known URLs (both discovered and hardcoded)"""
        return {
            category: self.url_repository.get_urls(category)
            for category in ['documentation', 'samples', 'tutorials', 'videos', 'community', 'other']
        }

    async def process_all_urls(self):
        """Process and analyze all known URLs"""
        all_urls = self.url_repository.get_urls()
        
        # First pass: collect all documentation
        for url in all_urls:
            try:
                content = await self._fetch_page_content(url)
                if content:
                    self.url_repository.add_content(url, content)
            except Exception as e:
                logger.error(f"Error fetching {url}: {str(e)}")
        
        # Second pass: analyze patterns
        await self.analyzer.analyze_documentation_set(all_urls)
        
        # Update our categories and patterns based on discoveries
        self._update_categories_from_analysis()
        self._update_patterns_from_analysis()
    
    def _update_categories_from_analysis(self):
        """Update categories based on discovered patterns"""
        insights = self.analyzer.get_insights()
        
        # Update category definitions
        for category, confidence in insights['suggested_categories'].items():
            if confidence > 0.8:  # High confidence threshold
                self.add_category(category)
        
        # Update URL categorization
        self._recategorize_urls(insights['topic_clusters'])
    
    def _update_patterns_from_analysis(self):
        """Update code patterns based on discoveries"""
        insights = self.analyzer.get_insights()
        
        # Update pattern definitions
        for pattern, occurrences in insights['common_patterns'].items():
            if occurrences > 5:  # Threshold for pattern significance
                self.pattern_knowledge.add_pattern(pattern)
        
        # Update framework relationships
        for framework, relationships in insights['framework_usage'].items():
            self.framework_knowledge.update_relationships(framework, relationships)

class KnowledgeBase:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        """Load existing knowledge base"""
        if self.file_path.exists():
            return json.loads(self.file_path.read_text())
        return {'items': [], 'relationships': []}
    
    def save(self):
        """Save knowledge base to disk"""
        self.file_path.write_text(json.dumps(self.data, indent=2))
    
    def add_concepts(self, concepts: List[Dict]):
        """Add new concepts to knowledge base"""
        for concept in concepts:
            if not self._concept_exists(concept['name']):
                self.data['items'].append(concept)
                self.save()
    
    def update_relationship(self, source: str, target: str, relationship_type: str):
        """Update relationship between concepts"""
        for rel in self.data['relationships']:
            if rel['source'] == source and rel['target'] == target:
                rel['strength'] += 0.1
                rel['occurrences'] += 1
                self.save()
                return
                
        # New relationship
        self.data['relationships'].append({
            'source': source,
            'target': target,
            'type': relationship_type,
            'strength': 0.5,
            'occurrences': 1
        })
        self.save()

class DocumentationAnalyzer:
    """Analyzes documentation content to discover patterns and categories"""
    
    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.category_patterns = self._load_patterns('category_patterns.json')
        self.discovered_patterns = defaultdict(int)
        self.topic_clusters = defaultdict(set)
        self.framework_relationships = defaultdict(set)
        
    async def analyze_documentation_set(self, urls: Set[str]):
        """Analyze a set of documentation pages to discover patterns"""
        for url in urls:
            content = await self._fetch_content(url)
            self._analyze_page_structure(content)
            self._extract_code_patterns(content)
            self._analyze_topic_relationships(content)
            
        self._update_knowledge_base()
    
    def _analyze_page_structure(self, content: str):
        """Analyze page structure to discover common patterns"""
        soup = BeautifulSoup(content, 'html.parser')
        
        # Analyze headers to understand documentation structure
        headers = soup.find_all(['h1', 'h2', 'h3'])
        for header in headers:
            text = header.get_text(strip=True)
            
            # Track common section patterns
            if header.name == 'h2':
                self.discovered_patterns['section_titles'][text] += 1
            
            # Analyze topic clustering
            if any(keyword in text.lower() for keyword in ['view', 'space', 'scene', 'gesture']):
                category = self._categorize_topic(text)
                self.topic_clusters[category].add(text)
    
    def _extract_code_patterns(self, content: str):
        """Extract and analyze code patterns"""
        soup = BeautifulSoup(content, 'html.parser')
        code_blocks = soup.find_all('code')
        
        for block in code_blocks:
            code = block.get_text()
            
            # Analyze imports to understand framework relationships
            imports = re.findall(r'import\s+(\w+)', code)
            for imp in imports:
                if imp in ['SwiftUI', 'RealityKit', 'ARKit']:
                    self.framework_relationships[imp].update(imports)
            
            # Look for common code patterns
            self._analyze_code_pattern(code)
    
    def _analyze_code_pattern(self, code: str):
        """Analyze code for common patterns"""
        patterns = {
            'view_modifier': r'func\s+\w+\s*\(\s*\)\s*->\s*some\s+View',
            'gesture_handler': r'\.gesture\(',
            'reality_view': r'RealityView\s*\{',
            'spatial_anchor': r'\.spatialAnchor',
            'immersive_space': r'ImmersiveSpace',
        }
        
        for pattern_name, regex in patterns.items():
            if re.search(regex, code):
                self.discovered_patterns['code_patterns'][pattern_name] += 1
    
    def _analyze_topic_relationships(self, content: str):
        """Analyze relationships between topics"""
        soup = BeautifulSoup(content, 'html.parser')
        
        # Look for related topics sections
        related = soup.find_all(['h2', 'h3'], string=re.compile(r'related|see also', re.I))
        for section in related:
            main_topic = section.find_previous(['h1', 'h2']).get_text(strip=True)
            links = section.find_next('ul').find_all('a')
            
            for link in links:
                related_topic = link.get_text(strip=True)
                self.topic_clusters['related_topics'].add((main_topic, related_topic))
    
    def _update_knowledge_base(self):
        """Update knowledge base with discovered patterns"""
        # Update category patterns
        self._save_patterns('discovered_categories.json', self.topic_clusters)
        
        # Update code patterns
        self._save_patterns('discovered_patterns.json', self.discovered_patterns)
        
        # Update framework relationships
        self._save_patterns('framework_relationships.json', self.framework_relationships)
        
        # Generate insights
        self._generate_pattern_insights()
    
    def _generate_pattern_insights(self):
        """Generate insights from discovered patterns"""
        insights = {
            'common_patterns': self._identify_common_patterns(),
            'framework_usage': self._analyze_framework_usage(),
            'topic_clusters': self._analyze_topic_clusters(),
            'suggested_categories': self._suggest_categories()
        }
        
        self._save_patterns('pattern_insights.json', insights)