import typer
from pathlib import Path
from typing import List, Optional
import asyncio
import json
from core.scraper import DocumentationScraper
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.panel import Panel
from analyzers.topic_analyzer import TopicAnalyzer

# Set up rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("rich")
console = Console()

app = typer.Typer(help="VisionOS Documentation Scraper CLI")

@app.command()
def scrape(
    urls: List[str] = typer.Argument(
        None,
        help="URLs to scrape. If not provided, will use default VisionOS documentation URLs"
    ),
    output_dir: Path = typer.Option(
        Path("data"),
        "--output-dir", "-o",
        help="Directory to store output files"
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug logging"
    )
):
    """Scrape VisionOS documentation pages"""
    if debug:
        logger.setLevel(logging.DEBUG)
    
    # Default URLs if none provided
    if not urls:
        urls = [
            "https://developer.apple.com/documentation/visionos/adding-3d-content-to-your-app",
            "https://developer.apple.com/documentation/visionos/creating-your-first-visionos-app",
            "https://developer.apple.com/documentation/visionos/creating-fully-immersive-experiences",
            "https://developer.apple.com/documentation/visionos/creating-immersive-spaces-in-visionos-with-swiftui",
            "https://developer.apple.com/documentation/visionos/bot-anist",
            "https://developer.apple.com/documentation/visionos/swift-splash"
        ]
    
    with console.status("[bold green]Scraping documentation...") as status:
        try:
            # Initialize scraper
            scraper = DocumentationScraper(output_dir=output_dir)
            
            # Run the scraper
            pages = asyncio.run(scraper.scrape_urls(urls))
            
            # Report results
            console.print(f"\n[bold green]Successfully scraped {len(pages)} pages!")
            
            # Create a table for results
            table = Table(title="Scraped Pages Summary")
            table.add_column("Title", style="cyan")
            table.add_column("Code Blocks", justify="right", style="green")
            table.add_column("Topics", justify="right", style="blue")
            
            for page in pages:
                table.add_row(
                    page.title,
                    str(len(page.code_blocks)),
                    str(len(page.topics))
                )
            
            console.print(table)
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise typer.Exit(code=1)

@app.command()
def analyze(
    input_dir: Path = typer.Option(
        Path("data/extracted"),
        "--input-dir", "-i",
        help="Directory containing extracted documentation files"
    )
):
    """Analyze extracted documentation"""
    try:
        files = list(input_dir.glob("extracted_*.json"))
        if not files:
            logger.error(f"No extracted files found in {input_dir}")
            raise typer.Exit(code=1)
            
        console.print(f"\n[bold]Found {len(files)} documentation files")
        
        # Analysis data
        total_code_blocks = 0
        topics = set()
        frameworks = set()
        code_types = {}
        
        for file in files:
            with open(file) as f:
                data = json.load(f)
                # Code blocks analysis
                code_blocks = data.get("code_blocks", [])
                total_code_blocks += len(code_blocks)
                
                # Collect frameworks and code types
                for block in code_blocks:
                    frameworks.update(block.get("frameworks", []))
                    code_type = block.get("type", "unknown")
                    code_types[code_type] = code_types.get(code_type, 0) + 1
                
                # Topic analysis
                topics.update(t["title"] for t in data.get("topics", []))
        
        # Display results in tables and panels
        # Code Statistics
        code_table = Table(title="Code Analysis")
        code_table.add_column("Metric", style="cyan")
        code_table.add_column("Value", justify="right", style="green")
        
        code_table.add_row("Total Code Blocks", str(total_code_blocks))
        code_table.add_row("Unique Frameworks", str(len(frameworks)))
        
        console.print(Panel(code_table, title="Code Statistics"))
        
        # Code Types Distribution
        if code_types:
            types_table = Table(title="Code Types Distribution")
            types_table.add_column("Type", style="cyan")
            types_table.add_column("Count", justify="right", style="green")
            
            for code_type, count in sorted(code_types.items(), key=lambda x: x[1], reverse=True):
                types_table.add_row(code_type, str(count))
            
            console.print(Panel(types_table, title="Code Types"))
        
        # Topics Overview
        topics_panel = Panel(
            "\n".join(f"• {topic}" for topic in sorted(topics)[:10]),
            title=f"Top Topics (showing 10 of {len(topics)})"
        )
        console.print(topics_panel)
        
        # Frameworks Used
        if frameworks:
            frameworks_panel = Panel(
                "\n".join(f"• {fw}" for fw in sorted(frameworks)),
                title="Frameworks Referenced"
            )
            console.print(frameworks_panel)
            
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def clean(
    output_dir: Path = typer.Option(
        Path("data"),
        "--output-dir", "-o",
        help="Directory to clean"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force cleanup without confirmation"
    )
):
    """Clean output directories"""
    if not force:
        confirm = typer.confirm(f"This will delete all files in {output_dir}. Continue?")
        if not confirm:
            raise typer.Exit()
    
    try:
        if output_dir.exists():
            for item in output_dir.glob("**/*"):
                if item.is_file():
                    item.unlink()
            for item in output_dir.glob("*"):
                if item.is_dir():
                    item.rmdir()
            output_dir.rmdir()
            console.print("[green]Cleanup complete!")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def analyze_topics(
    input_dir: Path = typer.Option(
        Path("data/extracted"),
        "--input-dir", "-i",
        help="Directory containing extracted documentation files"
    ),
    output_file: Path = typer.Option(
        Path("data/topic_graph.png"),
        "--output", "-o",
        help="Output file for topic graph visualization"
    )
):
    """Analyze relationships between documentation topics"""
    try:
        analyzer = TopicAnalyzer(input_dir)
        
        # Get central topics
        central_topics = analyzer.get_central_topics()
        
        console.print("\n[bold cyan]Most Central Topics:")
        for topic, score in central_topics:
            console.print(f"• {topic} (score: {score:.3f})")
        
        # Get topic clusters
        clusters = analyzer.get_topic_clusters()
        
        console.print("\n[bold cyan]Topic Clusters:")
        for cluster_name, topics in clusters.items():
            console.print(f"\n[bold]{cluster_name}:")
            for topic in topics:
                console.print(f"• {topic}")
        
        # Create visualization
        analyzer.visualize_relationships(output_file)
        
    except Exception as e:
        logger.error(f"Error during topic analysis: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def visualize(
    input_dir: Path = typer.Option(
        Path("data/extracted"),
        "--input-dir", "-i",
        help="Directory containing extracted documentation files"
    ),
    output_dir: Path = typer.Option(
        Path("data/visualizations"),
        "--output-dir", "-o",
        help="Directory for visualization outputs"
    )
):
    """Generate visualizations of the documentation structure"""
    try:
        analyzer = TopicAnalyzer(input_dir)
        
        # Create output directory
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Generate network visualization
        analyzer.visualize_relationships(output_dir / "topic_network.png")
        
        # Generate hierarchical visualization
        analyzer.visualize_hierarchical(output_dir / "topic_hierarchy.png")
        
        # Generate statistics
        stats = {
            "central_topics": analyzer.get_central_topics(),
            "clusters": analyzer.get_topic_clusters(),
            "node_count": len(analyzer.graph.nodes()),
            "edge_count": len(analyzer.graph.edges())
        }
        
        # Save statistics
        with open(output_dir / "topic_stats.json", "w") as f:
            json.dump(stats, f, indent=2, default=str)
        
        console.print("[green]Visualizations and statistics generated successfully!")
        
    except Exception as e:
        logger.error(f"Error generating visualizations: {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 