import asyncio
from core.scraper import DocumentationScraper
from core.url_sources import DocumentationURLCollector, URLSources
from analyzers.project_analyzer import ProjectAnalyzer
from extractors.relationship_extractor import RelationshipExtractor
from core.config import (
    TESTING_MODE, 
    BASE_URLS, 
    SKIP_DOWNLOADS,
    TEST_SAMPLE_COUNT,
    TEST_PATTERN_VALIDATION
)
from utils.logging import logger  # Add this import
import logging
from pathlib import Path
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

console = Console()

url_sources = URLSources()
doc_analyzer = DocumentationAnalyzer(Path('data/knowledge'))
pattern_evolution = PatternEvolution(Path('data/knowledge'))
project_analyzer = ProjectAnalyzer()
relationship_tracker = RelationshipTracker(Path('data/knowledge'))

async def process_url(url: str, url_collector: DocumentationURLCollector, skip_downloads: bool = True):
    """Process a single URL"""
    try:
        project = await url_collector.process_documentation_page(url)
        if project:
            console.print(f"Found project: {project.title}")
            if not skip_downloads:  # Only download if flag is False
                await url_collector.download_project(project)
                if project.local_path:
                    console.print(f"Downloaded to: {project.local_path}")
            return project
    except Exception as e:
        logger.error(f"Error processing URL {url}: {str(e)}")
    return None

async def discover_urls():
    """Discover all relevant URLs from base documentation"""
    url_collector = DocumentationURLCollector()
    discovered_urls = {}
    
    # Process base URLs first
    for base_url in BASE_URLS:  # Use imported BASE_URLS
        console.print(f"\n[cyan]Analyzing: {base_url}")
        
        # Get categorized links
        links = await url_collector.get_documentation_links(base_url)
        
        # Analyze documentation structure
        structure = await url_collector.analyze_documentation_structure(base_url)
        
        # Merge discovered URLs
        for category, urls in links.items():
            if category not in discovered_urls:
                discovered_urls[category] = set()
            discovered_urls[category].update(urls)
            
        console.print(f"[green]Found {sum(len(urls) for urls in links.values())} links")
    
    return discovered_urls

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
                        for pattern_type, data in pattern_data.items():
                            if pattern_matches(code, pattern_type):
                                try:
                                    # Wrap code in HTML for BeautifulSoup
                                    html = f"<div><code>{code}</code></div>"
                                    soup = BeautifulSoup(html, 'html.parser')
                                    code_elem = soup.find('code')
                                    
                                    if code_elem:
                                        context = doc_analyzer._get_code_context(code_elem)
                                        data['examples'].append({
                                            'code': code,
                                            'source_url': url,
                                            'context': context
                                        })
                                    else:
                                        logger.warning(f"Could not create code element for context extraction")
                                        
                                except Exception as e:
                                    logger.error(f"Error extracting context: {str(e)}")
                                    continue
                    
                    # Extract keywords and concepts
                    for pattern_type, data in pattern_data.items():
                        keywords = extract_pattern_keywords(soup, pattern_type)
                        data['keywords'].update(keywords)
                    
                except Exception as e:
                    logger.error(f"Error analyzing patterns in {url}: {str(e)}")
                    continue
                    
            await browser.close()
            
    except Exception as e:
        logger.error(f"Error in pattern analysis: {str(e)}")
    
    return pattern_data

def pattern_matches(code: str, pattern_type: str) -> bool:
    """Check if code matches a specific pattern type"""
    try:
        patterns = {
            '3d_content': ['RealityKit', 'Entity', 'ModelEntity'],
            'animation': ['animate', 'withAnimation', 'transition'],
            'ui_components': ['View', 'Button', 'Text'],
            'gestures': ['gesture', 'onTap', 'onDrag'],
            'spatial_audio': ['AudioEngine', 'spatialAudio'],
            'immersive_spaces': ['ImmersiveSpace', 'immersiveSpace']
        }
        
        if pattern_type not in patterns:
            logger.warning(f"Unknown pattern type: {pattern_type}")
            return False
            
        return any(pattern.lower() in code.lower() for pattern in patterns[pattern_type])
        
    except Exception as e:
        logger.error(f"Error matching pattern: {str(e)}")
        return False

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
    """Fetch content from a URL"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                logger.warning(f"Got status {response.status} for {url}")
                return None
    except Exception as e:
        logger.error(f"Error fetching content from {url}: {str(e)}")
        return None

async def main():
    url_collector = DocumentationURLCollector()
    
    # First check cache
    console.print("[bold cyan]Checking sample cache...")
    all_samples = await url_collector.discover_all_samples()
    
    if not all_samples:
        console.print("[yellow]Cache miss - discovering samples...")
        # Discover URLs
        discovered_urls = await discover_urls()
        
        # Process discovered URLs
        console.print("\n[bold cyan]Found URLs by Category:")
        for category, urls in discovered_urls.items():
            console.print(f"[yellow]{category}: [green]{len(urls)} URLs")
        
        # Process URLs based on mode
        if TESTING_MODE:
            console.print("\n[yellow]Running in TEST MODE with first 3 samples")
            # Filter for actual sample URLs
            sample_urls = [
                url for url in discovered_urls.get('documentation', set())
                if any(x in url.lower() for x in ['/sample/', 'sample-code', '.zip'])
            ]
            test_urls = sample_urls[:TEST_SAMPLE_COUNT]
            console.print(f"Selected {len(test_urls)} sample URLs for testing")
        else:
            test_urls = discovered_urls.get('documentation', set())
            
        # Process URLs without downloading if SKIP_DOWNLOADS is True
        processed_projects = []
        for url in test_urls:
            project = await process_url(url, url_collector, skip_downloads=SKIP_DOWNLOADS)
            if project:
                processed_projects.append(project)
                
        console.print(f"\nSuccessfully processed: {len(processed_projects)} projects")
        
        # Cache the results
        all_samples = processed_projects
    
    # Analyze results
    console.print("\nAnalysis Summary:")
    pattern_data = defaultdict(lambda: {'count': 0, 'examples': [], 'files': []})
    
    for project in all_samples:
        if project.local_path:
            console.print(f"\nAnalyzing {project.title}:")
            analysis = project_analyzer.analyze_project(project.local_path)
            
            # Track patterns with context
            for pattern_type, pattern_info in analysis['patterns'].items():
                if pattern_info['count'] > 0:  # Only process if patterns were found
                    pattern_data[pattern_type]['count'] += pattern_info['count']
                    pattern_data[pattern_type]['files'].extend(pattern_info['files'])
                    pattern_data[pattern_type]['examples'].extend(pattern_info['examples'])
    
    # Show pattern analysis results
    table = Table(title="Pattern Analysis Results")
    table.add_column("Project", style="cyan")
    table.add_column("Pattern Type", style="green")
    table.add_column("Count", justify="right", style="yellow")
    table.add_column("Files", style="blue")
    table.add_column("Status", style="magenta")  # New column
    
    # Track overall statistics
    total_patterns = defaultdict(int)
    total_files = defaultdict(set)
    
    for project in all_samples:
        if project.local_path:
            analysis = project_analyzer.analyze_project(project.local_path)
            
            for pattern_type, pattern_info in analysis.get('patterns', {}).items():
                if pattern_info['count'] > 0:
                    validation_status = "✓" if pattern_info.get('validated', False) else "⚠️"
                    table.add_row(
                        project.title,
                        pattern_type,
                        str(pattern_info['count']),
                        "\n".join(pattern_info['files'][:3]),  # Show first 3 files
                        validation_status
                    )
                    
                    # Update totals
                    total_patterns[pattern_type] += pattern_info['count']
                    total_files[pattern_type].update(pattern_info['files'])
    
    console.print(table)
    
    # Show summary
    summary = Table(title="Pattern Analysis Summary")
    summary.add_column("Pattern Type", style="cyan")
    summary.add_column("Total Count", style="yellow")
    summary.add_column("Total Files", style="green")
    
    for pattern_type in total_patterns:
        summary.add_row(
            pattern_type,
            str(total_patterns[pattern_type]),
            str(len(total_files[pattern_type]))
        )
    
    console.print("\nSummary:")
    console.print(summary)
    console.print("\nAnalysis Complete!")

if __name__ == "__main__":
    asyncio.run(main())