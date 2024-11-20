import asyncio
from pathlib import Path
from core.scraper import DocumentationScraper
from core.url_sources import DocumentationURLCollector, URLSources, ProjectResource
from analyzers.project_analyzer import ProjectAnalyzer
from analyzers.pattern_refiner import PatternRefiner
from core.knowledge_base import VisionOSKnowledgeBase
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
from core.llm_interface import VisionOSCodeGenerator
from analyzers.component_analyzer import ComponentAnalyzer
import argparse

console = Console()

url_sources = URLSources()
doc_analyzer = DocumentationAnalyzer(Path('data/knowledge'))
pattern_evolution = PatternEvolution(Path('data/knowledge'))
project_analyzer = ProjectAnalyzer()
relationship_tracker = RelationshipTracker(Path('data/knowledge'))
component_analyzer = ComponentAnalyzer()

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
                    
                    # Check if project is already downloaded
                    project_name = re.sub(r'[^\w\-_]', '_', project.title)
                    project_dir = url_collector.projects_dir / project_name
                    if project_dir.exists():
                        project.mark_downloaded(project_dir)
                        console.print(f"[green]Project already downloaded: {project_dir}")
                        return project
                    
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
    
    # Track per-base-url discoveries
    per_base_discoveries = {}
    
    for base_url in BASE_URLS:
        logger.info(f"🚀 Starting processing of base URL: {base_url}")
        try:
            links = await url_collector.get_documentation_links(base_url)
            
            # Store discovered links
            for category, urls in links.items():
                discovered_urls[category].update(urls)
                logger.debug(f"Found {len(urls)} {category} links in {base_url}")
                
                # Store per-base-url statistics
                if base_url not in per_base_discoveries:
                    per_base_discoveries[base_url] = defaultdict(set)
                per_base_discoveries[base_url][category].update(urls)
                
                # Detailed logging for documentation URLs
                if category == 'documentation':
                    logger.info(f"\nDocumentation URLs from {base_url}:")
                    for url in sorted(urls):
                        logger.info(f"  - {url}")
        
        except Exception as e:
            logger.error(f"Error processing base URL {base_url}: {str(e)}")
        
        finally:
            logger.info(f"🏁 Finished processing of base URL: {base_url}")
    
    # Log detailed summary per base URL
    logger.info("\nDiscovery Summary by Base URL:")
    for base_url, categories in per_base_discoveries.items():
        logger.info(f"\n{base_url}:")
        for category, urls in categories.items():
            logger.info(f"  {category}: {len(urls)} URLs")
    
    # Overall summary
    logger.info("\nTotal URL Discovery Summary:")
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

async def main(clear_cache: bool = False):
    """Main scraper function.
    
    Args:
        clear_cache: If True, clear the cache before running
    """
    logger.debug("Starting documentation scraper")
    url_collector = DocumentationURLCollector()
    
    logger.debug("Inspecting cache...")
    console.print("[bold cyan]Inspecting cache...")
    url_collector.inspect_cache()
    
    if clear_cache:
        logger.debug("Clearing cache...")
        url_collector.clear_cache()
        console.print("[yellow]Cache cleared. Starting fresh discovery...")
        all_samples = []
    else:
        all_samples = url_collector._load_from_cache()
    
    # Discover new URLs
    discovered_urls = await discover_urls()
    
    if not clear_cache:
        # Filter out already processed URLs
        new_urls = {category: urls - url_collector.processed_urls for category, urls in discovered_urls.items()}
        if not any(new_urls.values()):
            logger.info("No new URLs to process")
            if all_samples:  # If we have cached samples, continue with analysis
                discovered_urls = {}
            else:
                return
        else:
            logger.info("Found new URLs to process:")
            for category, urls in new_urls.items():
                if urls:
                    logger.info(f"{category}: {len(urls)} new URLs")
            discovered_urls = new_urls
    
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
    
    # Update processed URLs cache
    if not clear_cache:
        for urls in discovered_urls.values():
            url_collector.processed_urls.update(urls)
        url_collector.url_cache.write_text(json.dumps({
            'processed_urls': list(url_collector.processed_urls),
            'last_updated': datetime.now(UTC).isoformat()
        }))
    
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

    # After pattern analysis, before showing results
    console.print("\n[bold cyan]Refining Pattern Analysis...")
    pattern_refiner = PatternRefiner()
    component_patterns = component_analyzer.analyze_samples()
    refined_patterns = pattern_refiner.analyze_existing_patterns(pattern_data, component_patterns)
    
    # Update pattern data with refined patterns
    for pattern_type, refined_data in refined_patterns.items():
        if pattern_type in pattern_data:
            pattern_data[pattern_type].update({
                "detection_terms": refined_data["detection_terms"],
                "common_imports": refined_data["common_imports"],
                "confidence": refined_data["confidence"]
            })
    
    # Add refined pattern summary to output
    refined_table = Table(title="Refined Pattern Analysis")
    refined_table.add_column("Pattern Type", style="cyan")
    refined_table.add_column("Detection Terms", style="green")
    refined_table.add_column("Common Imports", style="yellow")
    refined_table.add_column("Confidence", style="blue")
    
    for pattern_type, data in refined_patterns.items():
        refined_table.add_row(
            pattern_type,
            ", ".join(sorted(data["detection_terms"])),
            ", ".join(sorted(data["common_imports"])),
            f"{data['confidence']:.2f}"
        )
    
    console.print(refined_table)
    
    # Initialize knowledge base with refined patterns
    knowledge_base = VisionOSKnowledgeBase()
    knowledge_base.build_from_analysis(pattern_data)
    
    # Initialize code generator
    code_generator = VisionOSCodeGenerator()
    
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

async def analyze_real_samples():
    """Analyze patterns in downloaded samples"""
    console.print("\n[bold cyan]Starting Pattern Analysis of Downloaded Samples[/]")
    
    # Get real sample paths
    sample_paths = []
    for ext in ['*.swift']:
        sample_paths.extend(list(Path('data/projects').rglob(ext)))
    
    console.print(f"\nFound [green]{len(sample_paths)}[/] Swift files to analyze")
    
    # Initialize pattern refiner
    pattern_refiner = PatternRefiner()
    
    # Initialize pattern statistics
    pattern_stats = defaultdict(lambda: {
        'count': 0,
        'files': set(),
        'examples': [],
        'co_occurrences': defaultdict(int),
        'projects': set(),  # Track which projects use each pattern
        'contexts': defaultdict(int)  # Track common usage contexts
    })
    
    # Track project-level statistics
    project_stats = defaultdict(lambda: {
        'pattern_count': 0,
        'unique_patterns': set(),
        'relationship_count': 0,
        'file_count': 0
    })
    
    # Progress bar for analysis
    with Progress() as progress:
        analyze_task = progress.add_task("[cyan]Analyzing files...", total=len(sample_paths))
        
        # Analyze each file
        for file_path in sample_paths:
            progress.update(analyze_task, advance=1)
            try:
                content = file_path.read_text()
                project_name = file_path.parts[file_path.parts.index('projects') + 1]
                
                # Update project stats
                project_stats[project_name]['file_count'] += 1
                
                # Detect patterns in the file
                detected_patterns = pattern_refiner.detect_patterns(content)
                
                # Update project pattern count
                project_stats[project_name]['pattern_count'] += len(detected_patterns)
                
                # Analyze relationships
                relationships = pattern_refiner.analyze_relationships(detected_patterns)
                project_stats[project_name]['relationship_count'] += len(relationships)
                
                # Update statistics for each detected pattern
                for pattern in detected_patterns:
                    pattern_stats[pattern.type]['count'] += 1
                    pattern_stats[pattern.type]['files'].add(str(file_path))
                    pattern_stats[pattern.type]['projects'].add(project_name)
                    project_stats[project_name]['unique_patterns'].add(pattern.type)
                    
                    # Store a short example if we don't have many
                    if len(pattern_stats[pattern.type]['examples']) < 3:
                        # Get context (5 lines before and after)
                        lines = content.splitlines()
                        pattern_line = content[:pattern.start].count('\n')
                        start_line = max(0, pattern_line - 5)
                        end_line = min(len(lines), pattern_line + 6)
                        example = '\n'.join(lines[start_line:end_line])
                        if example not in pattern_stats[pattern.type]['examples']:
                            pattern_stats[pattern.type]['examples'].append(example)
                    
                    # Track co-occurrences with other patterns
                    for other_pattern in detected_patterns:
                        if other_pattern.type != pattern.type:
                            pattern_stats[pattern.type]['co_occurrences'][other_pattern.type] += 1
                    
                    # Analyze context
                    context_lines = content.splitlines()[max(0, pattern.line_number - 3):pattern.line_number]
                    context = ' '.join(context_lines)
                    if 'init' in context or 'setup' in context:
                        pattern_stats[pattern.type]['contexts']['initialization'] += 1
                    if 'update' in context:
                        pattern_stats[pattern.type]['contexts']['update'] += 1
                    if 'gesture' in context or 'interaction' in context:
                        pattern_stats[pattern.type]['contexts']['interaction'] += 1
                    if 'animation' in context:
                        pattern_stats[pattern.type]['contexts']['animation'] += 1
            
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {str(e)}")
    
    # Generate comprehensive report
    output_path = Path('data/analysis/pattern_analysis.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert sets to lists for JSON serialization
    serializable_stats = {
        'patterns': {},
        'projects': {},
        'summary': {
            'total_files': len(sample_paths),
            'total_projects': len(project_stats),
            'total_patterns_found': sum(stat['count'] for stat in pattern_stats.values()),
            'most_common_patterns': [],
            'most_common_relationships': [],
            'pattern_distribution': {}
        }
    }
    
    # Process pattern stats
    for pattern_type, data in pattern_stats.items():
        serializable_stats['patterns'][pattern_type.value] = {
            'count': data['count'],
            'files': list(data['files']),
            'examples': data['examples'],
            'co_occurrences': dict(data['co_occurrences']),
            'projects': list(data['projects']),
            'contexts': dict(data['contexts'])
        }
        
        # Update pattern distribution
        serializable_stats['summary']['pattern_distribution'][pattern_type.value] = {
            'count': data['count'],
            'project_coverage': len(data['projects']) / len(project_stats) * 100
        }
    
    # Process project stats
    for project_name, data in project_stats.items():
        serializable_stats['projects'][project_name] = {
            'pattern_count': data['pattern_count'],
            'unique_patterns': len(data['unique_patterns']),
            'relationship_count': data['relationship_count'],
            'file_count': data['file_count'],
            'pattern_density': data['pattern_count'] / data['file_count'] if data['file_count'] > 0 else 0
        }
    
    # Sort and get most common patterns
    sorted_patterns = sorted(
        [(k.value, v['count'], len(v['projects'])) for k, v in pattern_stats.items()],
        key=lambda x: (x[1], x[2]),
        reverse=True
    )
    serializable_stats['summary']['most_common_patterns'] = [
        {'pattern': p[0], 'count': p[1], 'project_coverage': p[2]}
        for p in sorted_patterns[:10]
    ]
    
    # Save detailed analysis
    with open(output_path, 'w') as f:
        json.dump(serializable_stats, f, indent=2)
    
    # Print summary report
    console.print("\n[bold cyan]Pattern Analysis Summary[/]")
    console.print(f"Total files analyzed: [green]{len(sample_paths)}[/]")
    console.print(f"Total projects analyzed: [green]{len(project_stats)}[/]")
    console.print(f"Total patterns found: [green]{sum(stat['count'] for stat in pattern_stats.values())}[/]")
    
    console.print("\n[bold]Top 10 Most Common Patterns:[/]")
    for pattern in sorted_patterns[:10]:
        console.print(f"- {pattern[0]}: {pattern[1]} occurrences in {pattern[2]} projects")
    
    console.print(f"\nDetailed analysis saved to: [green]{output_path}[/]")
    
    return pattern_stats, project_stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the VisionOS documentation scraper')
    parser.add_argument('--clear-cache', action='store_true', help='Clear the cache before running')
    parser.add_argument('--no-prompt', action='store_true', help='Run without prompting')
    args = parser.parse_args()
    
    asyncio.run(main(clear_cache=args.clear_cache))