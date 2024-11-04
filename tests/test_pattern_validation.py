from analyzers.llm_interface import LLMDocumentationInterface
from analyzers.project_analyzer import ProjectAnalyzer
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
import pytest

# Configure rich logging with more detail
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True, show_time=False)]
)
logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO)

def test_validate_cylinder_implementation(capsys, caplog):
    """Test our cylinder rotation implementation against scraped patterns"""
    console.print(Panel.fit("Starting Cylinder Implementation Validation", style="bold green"))
    
    # Initialize our improved interfaces
    llm_interface = LLMDocumentationInterface()
    project_analyzer = ProjectAnalyzer()
    
    # Read our implementation
    with open('SampleView.swift', 'r') as f:
        implementation = f.read()
    
    # Show the code being validated
    console.print("\n[bold cyan]Validating Implementation:")
    console.print(Syntax(implementation, "swift", theme="monokai", line_numbers=True))
    
    # Analyze API usage
    api_patterns = project_analyzer.analyze_api_patterns(implementation)
    
    # Create results table
    table = Table(title="API Pattern Analysis")
    table.add_column("Category", style="cyan")
    table.add_column("Details", style="green")
    
    # Container Types
    if api_patterns['container_types']:
        for api, container in api_patterns['container_types'].items():
            table.add_row("Container Type", f"{api}: {container}")
            logger.info(f"Found {api} using {container}")
    
    # Method Usage
    if api_patterns['method_usage']:
        for api, methods in api_patterns['method_usage'].items():
            table.add_row("Method Usage", f"{api}: {', '.join(methods)}")
            logger.info(f"Found {api} using {methods}")
    
    console.print(table)
    
    # Validate EventSubscription usage
    subscription_valid = llm_interface.verify_api_usage(
        'EventSubscription',
        {'container_type': api_patterns['container_types'].get('EventSubscription')}
    )
    
    # Validate quaternion operations
    quaternion_valid = llm_interface.verify_api_usage(
        'simd_quatf',
        {'methods': api_patterns['method_usage'].get('quaternion', set())}
    )
    
    # Print validation summary
    summary_table = Table(title="Validation Summary")
    summary_table.add_column("API", style="cyan")
    summary_table.add_column("Status", style="green")
    summary_table.add_column("Details", style="yellow")
    
    summary_table.add_row(
        "EventSubscription",
        "✓" if subscription_valid else "✗",
        "Array usage matches documentation"
    )
    summary_table.add_row(
        "Quaternion Operations",
        "✓" if quaternion_valid else "✗",
        "Multiplication operation matches documentation"
    )
    
    console.print(summary_table)
    
    # Assertions with detailed messages
    assert subscription_valid, "EventSubscription usage doesn't match documentation patterns"
    assert quaternion_valid, "Quaternion operations don't match documentation patterns" 