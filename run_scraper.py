import asyncio
from core.scraper import DocumentationScraper
from core.url_sources import DocumentationURLCollector
from analyzers.project_analyzer import ProjectAnalyzer
from extractors.relationship_extractor import RelationshipExtractor
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

console = Console()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraper.log')
    ]
)
logger = logging.getLogger(__name__)

# Primary documentation URLs
base_urls = [
    "https://developer.apple.com/documentation/visionos/",
    "https://developer.apple.com/design/human-interface-guidelines/immersive-experiences",
    "https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos"
]

async def discover_urls():
    """Discover all relevant URLs from base documentation"""
    url_collector = DocumentationURLCollector()
    discovered_urls = {}
    
    # Process base URLs first
    for base_url in base_urls:
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

async def main():
    # First discover all URLs
    console.print("[bold cyan]Discovering Documentation URLs...")
    discovered_urls = await discover_urls()
    
    # Print URL summary
    console.print("\n[bold cyan]Found URLs by Category:")
    for category, urls in discovered_urls.items():
        if urls:
            console.print(f"[yellow]{category}: [green]{len(urls)} URLs")
    
    # Initialize collectors and extractors
    url_collector = DocumentationURLCollector()
    project_analyzer = ProjectAnalyzer()
    relationship_extractor = RelationshipExtractor()
    
    # Testing mode flag - change to False for full analysis
    TESTING_MODE = True
    
    # Core sample apps that demonstrate patterns
    core_urls = [
        # Basic Concepts
        "https://developer.apple.com/documentation/visionos/world",  # Hello World example
        
        # Immersive Experiences
        "https://developer.apple.com/documentation/visionos/building-an-immersive-media-viewing-experience",  # Media viewing
        "https://developer.apple.com/documentation/visionos/swift-splash",  # Full immersive space
        
        # Mixed Reality and 3D
        "https://developer.apple.com/documentation/visionos/bot-anist",  # 3D content and gestures
        "https://developer.apple.com/documentation/visionos/diorama",  # Mixed reality
        
        # UI Patterns
        "https://developer.apple.com/documentation/visionos/happy-beam",  # Windows and ornaments
        
        # Audio
        "https://developer.apple.com/documentation/visionos/playing-spatial-audio-in-visionos",  # Spatial audio patterns
        
        # Games and Interactive Content
        "https://developer.apple.com/documentation/realitykit/creating-a-spaceship-game"  # Game mechanics and physics
    ]
    
    # Test subset for initial validation
    test_urls = [
        "https://developer.apple.com/documentation/visionos/world",  # Basic structure
        "https://developer.apple.com/documentation/visionos/bot-anist",  # 3D and gestures
        "https://developer.apple.com/documentation/visionos/playing-spatial-audio-in-visionos"  # Audio
    ]
    
    # Select URLs based on testing mode
    urls_to_process = test_urls if TESTING_MODE else core_urls
    
    # Log testing mode
    if TESTING_MODE:
        console.print("[bold yellow]Running in TEST MODE with subset of URLs")
        console.print(f"Testing with {len(urls_to_process)} of {len(core_urls)} total URLs")
    else:
        console.print("[bold green]Running FULL ANALYSIS")
        console.print(f"Processing all {len(urls_to_process)} URLs")
    
    try:
        # Track all relationships and errors
        all_relationships = []
        downloaded_projects = []
        failed_downloads = []
        failed_analyses = []
        
        # Process each URL with error tracking
        for url in urls_to_process:
            try:
                console.print(f"\n[cyan]Processing: {url}")
                project = await url_collector.process_documentation_page(url)
                
                if project:
                    console.print(f"[green]Found project: {project.title}")
                    try:
                        await url_collector.download_project(project)
                        if project.local_path:
                            console.print(f"[green]Downloaded to: {project.local_path}")
                            downloaded_projects.append(project)
                    except Exception as e:
                        logger.error(f"Failed to download {url}: {str(e)}")
                        failed_downloads.append((url, str(e)))
            except Exception as e:
                logger.error(f"Failed to process {url}: {str(e)}")
                failed_analyses.append((url, str(e)))
        
        # Create results table
        results_table = Table(title="Pattern Analysis Results")
        results_table.add_column("Project", style="cyan")
        results_table.add_column("Pattern Type", style="green")
        results_table.add_column("Count", justify="right", style="yellow")
        results_table.add_column("Files", style="blue")
        
        # Analyze downloaded projects
        console.print("\n[bold cyan]Analyzing Projects:")
        for project in downloaded_projects:
            console.print(f"\n[yellow]Analyzing {project.title}:")
            analysis = project_analyzer.analyze_project(project.local_path)
            
            # Find all Swift files in the project
            swift_files = []
            for root, dirs, files in os.walk(project.local_path):
                for file in files:
                    if file.endswith('.swift'):
                        file_path = Path(root) / file
                        try:
                            content = file_path.read_text()
                            swift_files.append((file, content))
                            logger.info(f"Successfully read {file}")
                        except Exception as e:
                            logger.error(f"Error reading file {file}: {str(e)}")
                            continue  # Skip this file but continue processing others
            
            # Extract relationships from each Swift file
            for filename, content in swift_files:
                try:
                    # Extract relationships directly from content
                    relationships = relationship_extractor.extract_relationships(
                        content=content,  # Pass content directly
                        code_patterns=analysis.get('patterns', {})
                    )
                    if relationships:
                        logger.info(f"Found {len(relationships)} relationships in {filename}")
                        all_relationships.extend(relationships)
                    else:
                        logger.info(f"No relationships found in {filename}")
                except Exception as e:
                    logger.error(f"Error extracting relationships from {filename}: {str(e)}")
                    continue  # Skip this file but continue processing others
            
            # Add results to table
            for category, patterns in analysis['patterns'].items():
                if patterns:
                    files = ", ".join(set(p['file'] for p in patterns))
                    results_table.add_row(
                        project.title,
                        category,
                        str(len(patterns)),
                        files
                    )
            
            # Show pattern details
            for category, patterns in analysis['patterns'].items():
                if patterns:
                    console.print(f"\n[green]{category} patterns:")
                    for pattern in patterns:
                        console.print(Panel(
                            Syntax(pattern['content'], "swift", theme="monokai"),
                            title=f"{pattern['type']} in {pattern['file']}"
                        ))
        
        # Print relationship analysis
        relationship_table = Table(title="Concept Relationships")
        relationship_table.add_column("Source", style="cyan")
        relationship_table.add_column("Target", style="green")
        relationship_table.add_column("Type", style="yellow")
        relationship_table.add_column("Strength", justify="right")
        
        for rel in all_relationships:
            relationship_table.add_row(
                rel.source,
                rel.target,
                rel.relationship_type,
                f"{rel.strength:.2f}"
            )
        
        console.print(relationship_table)
        console.print(results_table)
        
        # Save relationships
        relationships_file = Path('data/extracted/relationships/relationships.json')
        relationships_file.parent.mkdir(parents=True, exist_ok=True)
        with open(relationships_file, 'w') as f:
            json.dump([
                {
                    'source': r.source,
                    'target': r.target,
                    'type': r.relationship_type,
                    'strength': r.strength
                }
                for r in all_relationships
            ], f, indent=2)
        
        # Print analysis summary
        console.print("\n[bold cyan]Analysis Summary:")
        console.print(f"[green]Successfully processed: {len(downloaded_projects)} projects")
        if failed_downloads:
            console.print("[red]Failed downloads:")
            for url, error in failed_downloads:
                console.print(f"  {url}: {error}")
        if failed_analyses:
            console.print("[red]Failed analyses:")
            for url, error in failed_analyses:
                console.print(f"  {url}: {error}")
            
        # Save analysis results
        results = {
            'discovered_urls': {k: list(v) for k, v in discovered_urls.items()},
            'processed_projects': len(downloaded_projects),
            'failed_downloads': failed_downloads,
            'failed_analyses': failed_analyses,
            'relationships': [
                {
                    'source': r.source,
                    'target': r.target,
                    'type': r.relationship_type,
                    'strength': r.strength
                }
                for r in all_relationships
            ]
        }
        
        results_file = Path('data/analysis_results.json')
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print("\n[bold green]Test Analysis Complete!")
            
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())