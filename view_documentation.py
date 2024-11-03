import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def find_latest_documentation() -> Optional[tuple[Path, Path]]:
    data_dir = Path('data')
    if not data_dir.exists():
        console.print("[red]No data directory found![/red]")
        return None
    
    doc_files = list(data_dir.glob('visionos_documentation_*.json'))
    manifest_files = list(data_dir.glob('manifest_*.json'))
    
    if not doc_files:
        console.print("[red]No documentation files found![/red]")
        return None
        
    latest_doc = max(doc_files, key=lambda x: x.stat().st_mtime)
    latest_manifest = max(manifest_files, key=lambda x: x.stat().st_mtime)
    return latest_doc, latest_manifest

def view_documentation():
    files = find_latest_documentation()
    if not files:
        return
        
    doc_file, manifest_file = files
    
    # Load the data
    with open(doc_file) as f:
        data = json.load(f)
    with open(manifest_file) as f:
        manifest = json.load(f)
    
    # Show summary
    console.print(Panel.fit(
        f"Documentation Summary\n"
        f"Total entries: {len(data)}\n"
        f"Total pages scraped: {manifest['total_pages']}\n"
        f"Timestamp: {manifest['timestamp']}"
    ))
    
    # Create table of entries
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Title", style="dim")
    table.add_column("Description", style="dim", max_width=60)
    table.add_column("Framework", style="dim")
    
    for entry in data[:10]:  # Show first 10 entries
        table.add_row(
            entry['title'],
            entry['description'][:100] + "..." if len(entry['description']) > 100 else entry['description'],
            entry['framework']
        )
    
    console.print("\nFirst 10 Documentation Entries:")
    console.print(table)
    
    # Show sample full entry
    console.print("\nDetailed view of first entry:")
    console.print(json.dumps(data[0], indent=2))
    
    # Show options
    console.print("\n[green]Options:[/green]")
    console.print("1. View all entries")
    console.print("2. Search entries")
    console.print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        for entry in data:
            console.print("\n---")
            console.print(f"[bold]{entry['title']}[/bold]")
            console.print(entry['description'])
            console.print(f"URL: {entry['url']}")
    elif choice == "2":
        search_term = input("Enter search term: ").lower()
        results = [
            entry for entry in data 
            if search_term in entry['title'].lower() 
            or search_term in entry['description'].lower()
        ]
        console.print(f"\nFound {len(results)} matching entries:")
        for entry in results:
            console.print("\n---")
            console.print(f"[bold]{entry['title']}[/bold]")
            console.print(entry['description'])

if __name__ == "__main__":
    view_documentation() 