import asyncio
from pathlib import Path
from core.scraper import DocumentationScraper
from core.url_sources import DocumentationURLCollector, URLSources, ProjectResource
from analyzers.project_analyzer import ProjectAnalyzer
from extractors.relationship_extractor import RelationshipExtractor
from core.config import (
    TESTING_MODE, 
    BASE_URLS, 
    SKIP_DOWNLOADS,
    TEST_SAMPLE_COUNT,
    TEST_PATTERN_VALIDATION,
    TEST_SAMPLE_STRATEGY,
    ARKIT_SAMPLES
)
from utils.logging import logger

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
import json
from bs4 import BeautifulSoup
import glob
import os
import re
from collections import defaultdict
from collections import Counter
from typing import Dict, Set, Optional, List
from playwright.async_api import async_playwright
from analyzers.pattern_evolution import PatternEvolution
from analyzers.relationship_tracker import RelationshipTracker
from typing import Optional
import aiohttp
from core.documentation_analyzer import DocumentationAnalyzer
import hashlib
from datetime import datetime, UTC
from rich.progress import Progress
import random

console = Console()

url_sources = URLSources()
doc_analyzer = DocumentationAnalyzer(Path('data/knowledge'))
pattern_evolution = PatternEvolution(Path('data/knowledge'))
project_analyzer = ProjectAnalyzer()
relationship_tracker = RelationshipTracker(Path('data/knowledge'))

async def process_url(url: str, url_collector: DocumentationURLCollector, skip_downloads: bool = SKIP_DOWNLOADS):
    """Process a single URL with improved error handling"""
    retries = 3
    while retries > 0:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                console.print(f"\n[cyan]Processing URL: {url}")
                
                # Handle ZIP URLs differently from documentation URLs
                if url.endswith('.zip'):
                    project = ProjectResource(
                        title=url.split('/')[-1].replace('.zip', ''),
                        url=url,
                        download_url=url
                    )
                    
                    if not skip_downloads:
                        console.print(f"[yellow]Attempting download to {url_collector.projects_dir}...")
                        success = await url_collector.download_project(project)
                        if success:
                            console.print(f"[green]Downloaded to: {project.local_path}")
                            url_collector._update_cache([project])
                            console.print(f"[green]Project cached: {project.title}")
                        else:
                            console.print(f"[red]Download failed")
                            retries -= 1
                            if retries > 0:
                                await asyncio.sleep(2)  # Add delay between retries
                            continue
                    return project
                
        except aiohttp.ClientError as e:
            retries -= 1
            if retries == 0:
                logger.error(f"Network error processing {url}: {str(e)}")
                return None
            await asyncio.sleep(2)  # Wait before retry
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            return None
    return None

async def discover_urls():
    """Discover all relevant URLs from base documentation"""
    logger.debug("Starting URL discovery process")
    url_collector = DocumentationURLCollector()
    discovered_urls = defaultdict(set)
    
    for base_url in BASE_URLS:
        logger.debug(f"Processing base URL: {base_url}")
        links = await url_collector.get_documentation_links(base_url)
        
        # Actually process and store the links we find
        for category, urls in links.items():
            discovered_urls[category].update(urls)
            logger.debug(f"Found {len(urls)} {category} links in {base_url}")
            for url in urls:
                logger.debug(f"  {category}: {url}")
    
    # Log summary before returning
    logger.info("URL Discovery Summary:")
    for category, urls in discovered_urls.items():
        logger.info(f"{category}: {len(urls)} URLs found")
    
    return dict(discovered_urls)

def pattern_matches(code: str, pattern_type: str) -> bool:
    """Check if code matches a specific pattern type"""
    patterns = {
        'ui_components': [
            r'WindowGroup',
            r'NavigationStack',
            r'TabView',
            r'View\s*{',
            r'@main\s+struct.*App\s*:'
        ],
        'animation': [
            r'withAnimation',
            r'animation',
            r'transition',
            r'\.animate',
            r'Animation'
        ],
        'gestures': [
            r'gesture',
            r'onTapGesture',
            r'DragGesture',
            r'LongPressGesture',
            r'RotationGesture'
        ],
        '3d_content': [
            r'RealityView',
            r'Entity',
            r'Model3D',
            r'attachments',
            r'\.load\(".*\.usd[z]?"'
        ],
        'spatial_audio': [
            r'SpatialAudioEmitter',
            r'AudioEngine',
            r'playSound',
            r'spatial\.audio',
            r'\.audio\('
        ],
        'immersive_spaces': [
            r'ImmersiveSpace',
            r'immersiveSpace',
            r'fullspace',
            r'ornament',
            r'WindowGroup\s*{\s*ImmersiveSpace'
        ]
    }
    
    # Get patterns for the specified type
    type_patterns = patterns.get(pattern_type, [])
    
    # Check if any pattern matches
    return any(re.search(pattern, code, re.IGNORECASE) for pattern in type_patterns)

async def analyze_patterns_from_docs(discovered_urls: Dict[str, Set[str]], url_collector: DocumentationURLCollector) -> Dict[str, Dict]:
    """Analyze patterns from documentation pages"""
    pattern_data = defaultdict(lambda: {'count': 0, 'examples': [], 'keywords': set()})
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            for url in discovered_urls.get('documentation', set()):
                try:
                    await page.goto(url)
                    await page.wait_for_load_state('networkidle')
                    content = await page.content()
                    
                    soup = BeautifulSoup(content, 'html.parser')
                    code_blocks = soup.find_all('code')
                    
                    for block in code_blocks:
                        code = block.get_text()
                        
                        # Analyze code to identify patterns
                        for pattern_type in ['ui_components', 'animation', 'gestures', '3d_content', 'spatial_audio', 'immersive_spaces']:
                            if pattern_matches(code, pattern_type):
                                pattern_data[pattern_type]['count'] += 1
                                pattern_data[pattern_type]['examples'].append({
                                    'code': code,
                                    'source_url': url
                                })
                                
                except Exception as e:
                    logger.error(f"Error analyzing patterns in {url}: {str(e)}")
                    continue
                    
            await browser.close()
            
    except Exception as e:
        logger.error(f"Error in pattern analysis: {str(e)}")
    
    return pattern_data

def extract_pattern_keywords(soup: BeautifulSoup, pattern_type: str) -> Set[str]:
    """Extract keywords related to a pattern type"""
    keywords = set()
    
    # Pattern-specific sections to look for
    section_indicators = {
        'ui_components': ['view', 'window', 'interface'],
        'animation': ['animation', 'transition', 'movement'],
        'gestures': ['gesture', 'interaction', 'input'],
        '3d_content': ['3d', 'model', 'entity'],
        'spatial_audio': ['audio', 'sound', 'spatial'],
        'immersive_spaces': ['space', 'immersive', 'environment']
    }
    
    # Find relevant sections
    for indicator in section_indicators.get(pattern_type, []):
        sections = soup.find_all(['h1', 'h2', 'h3', 'h4'], 
                               string=re.compile(indicator, re.I))
        for section in sections:
            # Get keywords from section content
            content = get_section_content(section)
            keywords.update(extract_technical_terms(content))
    
    return keywords

def get_section_content(section_header) -> str:
    """Get content of a section until next header"""
    content = []
    current = section_header.find_next_sibling()
    while current and not current.name in ['h1', 'h2', 'h3', 'h4']:
        content.append(current.get_text())
        current = current.find_next_sibling()
    return ' '.join(content)

def extract_technical_terms(text: str) -> Set[str]:
    """Extract technical terms from text"""
    terms = set()
    
    # Common VisionOS technical term patterns
    patterns = [
        r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',  # CamelCase terms
        r'\b\w+Kit\b',  # Frameworks
        r'\b\w+View\b',  # View types
        r'\b\w+Controller\b',  # Controller types
        r'\b\w+Protocol\b',  # Protocol types
        r'\b3D\s+\w+\b',  # 3D-related terms
        r'\bAR\s+\w+\b',  # AR-related terms
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        terms.update(match.group(0) for match in matches)
    
    return terms

async def fetch_content(url: str) -> Optional[str]:
    """Fetch content from a URL with improved caching"""
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = Path('data/cache/content') / f"{cache_key}.html"
    
    # Check cache age
    if cache_file.exists():
        age = datetime.now(UTC) - datetime.fromtimestamp(cache_file.stat().st_mtime, UTC)
        if age.days < 1:  # Cache is fresh
            return cache_file.read_text(encoding='utf-8')
    
    # Fetch new content
    content = await _fetch_url_content(url)
    if content:
        cache_file.parent.mkdir(exist_ok=True)
        cache_file.write_text(content, encoding='utf-8')
    return content

async def _fetch_url_content(url: str) -> Optional[str]:
    """Internal function to fetch URL content"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                logger.warning(f"Got status {response.status} for {url}")
                return None
    except Exception as e:
        logger.error(f"Error fetching URL {url}: {str(e)}")
        return None

def select_test_samples(samples: List[str], strategy: str = TEST_SAMPLE_STRATEGY) -> List[str]:
    """Select samples based on strategy"""
    if strategy == "arkit_first":
        # Prioritize ARKit samples first
        arkit_samples = [
            sample for sample in samples 
            if any(arkit_name in sample.lower() for arkit_name in ARKIT_SAMPLES)
        ]
        other_samples = [
            sample for sample in samples 
            if not any(arkit_name in sample.lower() for arkit_name in ARKIT_SAMPLES)
        ]
        
        # Take ARKit samples first, then fill with others up to TEST_SAMPLE_COUNT
        selected = arkit_samples[:TEST_SAMPLE_COUNT]
        if len(selected) < TEST_SAMPLE_COUNT:
            selected.extend(other_samples[:TEST_SAMPLE_COUNT - len(selected)])
            
        return selected[:TEST_SAMPLE_COUNT]
        
    elif strategy == "first":
        return samples[:TEST_SAMPLE_COUNT]
    elif strategy == "random":
        return random.sample(samples, min(TEST_SAMPLE_COUNT, len(samples)))
    else:  # diverse
        return samples[:TEST_SAMPLE_COUNT]

async def main():
    logger.debug("Starting documentation scraper")
    url_collector = DocumentationURLCollector()
    
    # First inspect cache
    logger.debug("Inspecting cache...")
    console.print("[bold cyan]Inspecting cache...")
    url_collector.inspect_cache()
    
    # Ask if cache should be cleared
    if console.input("\nWould you like to clear the cache and start fresh? (y/n): ").lower() == 'y':
        logger.debug("Clearing cache...")
        url_collector.clear_cache()
        console.print("[yellow]Cache cleared. Starting fresh discovery...")
        all_samples = []
    else:
        # Check cache
        logger.debug("Checking sample cache...")
        console.print("\n[bold cyan]Checking sample cache...")
        all_samples = await url_collector.discover_all_samples()
    
    # Show detailed sample information
    if all_samples:
        console.print("\n[bold cyan]Found Samples in Cache:")
        sample_table = Table(
            title="Cached Samples",
            show_lines=True,
            width=120,
            pad_edge=False
        )
        sample_table.add_column("Title", style="green", width=30, overflow="fold")
        sample_table.add_column("URL", style="blue", width=50, overflow="ellipsis")
        sample_table.add_column("Local Path", style="yellow", width=20, overflow="ellipsis")
        sample_table.add_column("Status", style="magenta", width=15, justify="center")
        
        # Download missing samples with progress
        if not SKIP_DOWNLOADS:
            missing_samples = [s for s in all_samples if not s.downloaded]
            if missing_samples:
                console.print(f"\n[yellow]Found {len(missing_samples)} samples to download...")
                with Progress() as progress:
                    task = progress.add_task("[cyan]Downloading samples...", total=len(missing_samples))
                    
                    for sample in missing_samples:
                        try:
                            success = await url_collector.download_project(sample)
                            if success:
                                console.print(f"[green]Downloaded: {sample.title}")
                            else:
                                console.print(f"[red]Failed to download: {sample.title}")
                            progress.update(task, advance=1)
                        except Exception as e:
                            console.print(f"[red]Error downloading {sample.title}: {str(e)}")
                            progress.update(task, advance=1)
        
        # Update table with current status
        for sample in all_samples:
            status = "✓ Downloaded" if sample.local_path else "Not Downloaded"
            # Truncate and format URL for display
            url_display = sample.url[:47] + "..." if len(sample.url) > 50 else sample.url
            sample_table.add_row(
                sample.title,
                url_display,
                str(sample.local_path) if sample.local_path else "-",
                status
            )
        console.print(sample_table)
    else:
        logger.debug("Cache miss - discovering samples...")
        console.print("[yellow]Cache miss - discovering samples...")
        discovered_urls = await discover_urls()
        
        # Log discovered URLs
        for category, urls in discovered_urls.items():
            logger.debug(f"Found {len(urls)} {category} URLs")
            for url in urls:
                logger.debug(f"{category}: {url}")
        
        # Process discovered URLs
        console.print("\n[bold cyan]Found URLs by Category:")
        for category, urls in discovered_urls.items():
            console.print(f"[yellow]{category}: [green]{len(urls)} URLs")
        
        # Process URLs based on mode
        if TESTING_MODE:
            console.print("\n[yellow]Running in TEST MODE with first 3 samples")
            sample_urls = list(discovered_urls.get('samples', set()))
            
            # Use the sample selection strategy
            test_urls = select_test_samples(sample_urls, TEST_SAMPLE_STRATEGY)
            
            console.print("\nProcessing these sample URLs:")
            for url in test_urls:
                console.print(f"[green]- {url}")
        else:
            test_urls = discovered_urls.get('samples', set())
        
        # Process URLs concurrently
        processed_projects = await process_urls_concurrent(test_urls, url_collector)
        processed_projects = [p for p in processed_projects if p is not None]
        
        console.print(f"\nSuccessfully processed: {len(processed_projects)} projects")
        all_samples = processed_projects
    
    # Analyze results
    console.print("\n[bold cyan]Analysis Summary:")
    pattern_data = defaultdict(lambda: {'count': 0, 'examples': [], 'files': []})
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing projects...", total=len(all_samples))
        
        for project in all_samples:
            if project.local_path:
                progress.update(task, advance=1, description=f"Analyzing {project.title}")
                console.print(f"\nAnalyzing {project.title}:")
                analysis = project_analyzer.analyze_project(project.local_path)
                
                # Track patterns with context
                for pattern_type, pattern_info in analysis.get('patterns', {}).items():
                    if pattern_info['count'] > 0:
                        pattern_data[pattern_type]['count'] += pattern_info['count']
                        pattern_data[pattern_type]['files'].extend(pattern_info['files'])
                        pattern_data[pattern_type]['examples'].extend(pattern_info['examples'])
                        console.print(f"[green]Found {pattern_info['count']} {pattern_type} patterns")
    
    # Show pattern analysis results
    results_table = Table(
        title="Pattern Analysis Results",
        show_lines=True,
        width=120,
        pad_edge=False
    )
    results_table.add_column("Project", style="cyan", width=30, overflow="fold")
    results_table.add_column("Pattern Type", style="green", width=20)
    results_table.add_column("Count", justify="right", style="yellow", width=10)
    results_table.add_column("Files", style="blue", width=40, overflow="fold")
    results_table.add_column("Status", style="magenta", width=10, justify="center")
    
    # Group by project for better readability
    for project in all_samples:
        if project.local_path:
            for pattern_type, data in pattern_data.items():
                project_files = [f for f in data['files'] if str(project.local_path) in str(f)]
                if project_files:
                    validation_status = "✓" if data.get('validated', False) else "-"
                    results_table.add_row(
                        project.title,
                        pattern_type,
                        str(len(project_files)),
                        "\n".join(str(f) for f in project_files[:3]),
                        validation_status
                    )
    
    console.print(results_table)
    
    # Show summary
    summary_table = Table(
        title="Pattern Analysis Summary",
        show_lines=True,
        width=80,
        pad_edge=False
    )
    summary_table.add_column("Pattern Type", style="cyan", width=30)
    summary_table.add_column("Total Count", style="yellow", width=20, justify="right")
    summary_table.add_column("Total Files", style="green", width=20, justify="right")
    
    for pattern_type, data in pattern_data.items():
        summary_table.add_row(
            pattern_type,
            str(data['count']),
            str(len(set(data['files'])))  # Use set to count unique files
        )
    
    console.print("\nSummary:")
    console.print(summary_table)
    console.print("\n[bold green]Analysis Complete!")

    # After analysis, prepare knowledge base
    knowledge_base = VisionOSKnowledgeBase()
    knowledge_base.build_from_analysis(pattern_data)
    
    # Initialize code generator
    code_generator = VisionOSCodeGenerator()
    
    # Now ready for LLM use
    return code_generator

async def process_urls_concurrent(urls: Set[str], url_collector: DocumentationURLCollector):
    processed = set()
    tasks = []
    
    async def process_with_limit(url: str):
        if url in processed:
            return None
        processed.add(url)
        return await process_url(url, url_collector)
    
    for url in urls:
        tasks.append(process_with_limit(url))
    
    return await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())