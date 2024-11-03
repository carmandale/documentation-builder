import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
import typer
from typing import Optional, List, Dict

console = Console()
app = typer.Typer()

def load_latest_documentation(data_dir: str = "data") -> List[Dict]:
    """Load the most recent documentation file"""
    data_dir = Path(data_dir)
    doc_files = list(data_dir.glob('visionos_documentation_*.json'))
    if not doc_files:
        raise FileNotFoundError("No documentation files found")
    
    latest_doc = max(doc_files, key=lambda x: x.stat().st_mtime)
    console.print(f"[green]Loading documentation from {latest_doc.name}[/green]")
    
    with open(latest_doc) as f:
        return json.load(f)

@app.command()
def view(
    entry_number: Optional[int] = typer.Argument(None, help="View specific entry number"),
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search in titles and descriptions"),
    show_examples: bool = typer.Option(False, "--examples", "-e", help="Show code examples"),
    show_parameters: bool = typer.Option(False, "--params", "-p", help="Show parameters")
):
    """View documentation content"""
    try:
        docs = load_latest_documentation()
        
        if search:
            docs = [
                entry for entry in docs
                if search.lower() in entry['title'].lower() 
                or search.lower() in entry.get('description', '').lower()
            ]
            console.print(f"\nFound {len(docs)} entries matching '{search}'")
        
        if entry_number is not None:
            if 0 <= entry_number < len(docs):
                display_entry(docs[entry_number], show_examples, show_parameters)
            else:
                console.print(f"[red]Entry number {entry_number} not found[/red]")
            return
        
        # Display summary table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim")
        table.add_column("Title")
        table.add_column("Description", max_width=60)
        table.add_column("Examples", justify="right")
        table.add_column("Parameters", justify="right")
        
        for i, entry in enumerate(docs):
            examples_count = len(entry.get('examples', [])) if entry.get('examples') else 0
            params_count = len(entry.get('parameters', [])) if entry.get('parameters') else 0
            
            table.add_row(
                str(i),
                entry['title'],
                (entry.get('description', '')[:57] + '...') if entry.get('description') else 'No description',
                str(examples_count),
                str(params_count)
            )
        
        console.print(table)
        console.print("\nUse --help for more options")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

def display_entry(entry: dict, show_examples: bool = False, show_parameters: bool = False):
    """Display detailed view of a single entry"""
    console.print(Panel(
        f"[bold blue]{entry['title']}[/bold blue]\n\n"
        f"[bold]URL:[/bold] {entry['url']}\n\n"
        f"[bold]Description:[/bold]\n{entry.get('description', 'No description')}\n"
    ))
    
    if show_parameters and entry.get('parameters'):
        console.print("\n[bold]Parameters:[/bold]")
        param_table = Table(show_header=True)
        param_table.add_column("Name")
        param_table.add_column("Type")
        param_table.add_column("Description")
        
        for param in entry['parameters']:
            param_table.add_row(
                param.get('name', 'N/A'),
                param.get('type', 'N/A'),
                param.get('description', '')
            )
        console.print(param_table)
    
    if show_examples and entry.get('examples'):
        console.print("\n[bold]Code Examples:[/bold]")
        for i, example in enumerate(entry['examples'], 1):
            if example.get('description'):
                console.print(f"\nExample {i} Description: {example['description']}")
            console.print(Syntax(example.get('code', ''), "swift", theme="monokai"))
    
    if entry.get('metadata'):
        console.print("\n[bold]Metadata:[/bold]")
        console.print(json.dumps(entry['metadata'], indent=2))

@app.command()
def stats():
    """Show documentation statistics"""
    docs = load_latest_documentation()
    
    total_entries = len(docs)
    entries_with_params = sum(1 for d in docs if d.get('parameters'))
    entries_with_examples = sum(1 for d in docs if d.get('examples'))
    total_examples = sum(len(d.get('examples', [])) if d.get('examples') else 0 for d in docs)
    
    console.print(Panel(
        f"[bold]Documentation Statistics[/bold]\n\n"
        f"Total Entries: {total_entries}\n"
        f"Entries with Parameters: {entries_with_params}\n"
        f"Entries with Examples: {entries_with_examples}\n"
        f"Total Code Examples: {total_examples}\n"
    ))

if __name__ == "__main__":
    app()