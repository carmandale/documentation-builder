from pathlib import Path
import typer
import shutil
import json
from datetime import datetime
from typing import Optional, List, Dict
from core.xcode_manager import XcodeProjectManager
from core.llm_session import LLMSession
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
import os
from utils.logging import logger

app = typer.Typer()
console = Console()

def setup_project_structure(name: str) -> Path:
    """Create project directory structure"""
    try:
        # Get absolute path for projects directory
        base_dir = Path.cwd() / "projects"
        project_dir = base_dir / name
        
        logger.debug(f"Setting up project structure:")
        logger.debug(f"  Base directory: {base_dir}")
        logger.debug(f"  Project directory: {project_dir}")
        
        # Create main project directory
        project_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created project directory: {project_dir}")
        
        # Create necessary subdirectories
        subdirs = ["backups", "conversations"]
        for subdir in subdirs:
            (project_dir / subdir).mkdir(exist_ok=True)
            logger.debug(f"Created subdirectory: {subdir}")
            
        return project_dir
        
    except Exception as e:
        logger.error(f"Failed to setup project structure: {str(e)}")
        raise

def _save_json(file_path: Path, data: dict):
    """Save data as JSON"""
    try:
        logger.debug(f"Saving JSON data to: {file_path}")
        with file_path.open('w') as f:
            json.dump(data, f, indent=2)
        logger.debug("JSON data saved successfully")
    except Exception as e:
        logger.error(f"Failed to save JSON data: {str(e)}")
        raise

def _sanitize_path(path_str: str) -> Path:
    """Handle paths with spaces and special characters"""
    try:
        logger.debug(f"Sanitizing path: {path_str}")
        
        # Strip any surrounding quotes (both single and double)
        path_str = path_str.strip("'\"")
        logger.debug(f"Stripped quotes: {path_str}")
        
        # First expand any user references (~/...)
        expanded = os.path.expanduser(path_str)
        logger.debug(f"Expanded path: {expanded}")
        
        # Convert to absolute path
        abs_path = Path(expanded).resolve()
        logger.debug(f"Absolute path: {abs_path}")
        
        return abs_path
        
    except Exception as e:
        logger.error(f"Failed to sanitize path: {str(e)}")
        raise

def _sanitize_project_name(name: str) -> str:
    """Convert spaces to underscores in project name"""
    try:
        logger.debug(f"Sanitizing project name: {name}")
        sanitized = name.replace(' ', '_')
        logger.debug(f"Sanitized name: {sanitized}")
        return sanitized
    except Exception as e:
        logger.error(f"Failed to sanitize project name: {str(e)}")
        raise

def _validate_xcode_project(path: Path) -> bool:
    """Validate that path contains an Xcode project"""
    try:
        logger.debug(f"Validating Xcode project at: {path}")
        
        # Check if path exists
        if not path.exists():
            logger.error(f"Path does not exist: {path}")
            return False
            
        # Look for .xcodeproj directory
        xcodeproj = list(path.glob("*.xcodeproj"))
        if not xcodeproj:
            logger.error(f"No .xcodeproj found in: {path}")
            return False
            
        logger.info(f"Found valid Xcode project: {xcodeproj[0]}")
        return True
        
    except Exception as e:
        logger.error(f"Error validating Xcode project: {str(e)}")
        return False

@app.command(name="new")
def create_project(
    project_name: str = typer.Option(None, "--name", "-n", prompt=True),
    project_path: str = typer.Option(None, "--path", "-p", prompt="Path to Xcode project")
):
    """Create a new visionOS project"""
    try:
        logger.info(f"\nStarting project creation:")
        
        # Sanitize project name
        project_name = _sanitize_project_name(project_name)
        console.print(f"Project Name: [green]{project_name}")
        
        # Handle paths with spaces and special characters
        xcode_project_path = _sanitize_path(project_path)
        
        # Show where we'll create our project metadata
        our_project_dir = Path.cwd() / "projects" / project_name
        console.print(f"\nProject Structure:")
        console.print(f"  Xcode Project: [green]{xcode_project_path}")
        console.print(f"  Project Data: [green]{our_project_dir.absolute()}")
        
        # Confirm with user
        if not Confirm.ask("\nProceed with project creation?"):
            console.print("[yellow]Project creation cancelled")
            return
        
        # Validate Xcode project first
        if not _validate_xcode_project(xcode_project_path):
            console.print(f"[red]No valid Xcode project found at: {xcode_project_path}")
            return
            
        # Setup project structure
        project_dir = setup_project_structure(project_name)
        console.print(f"\n[green]Created project structure:")
        console.print(f"  Config: {project_dir}/config.json")
        console.print(f"  Conversations: {project_dir}/conversations/")
        console.print(f"  Backups: {project_dir}/backups/")
        
        # Create project configuration
        project_config = {
            "name": project_name,
            "xcode_path": str(xcode_project_path),
            "created_at": datetime.now().isoformat()
        }
        
        # Save project configuration
        config_file = project_dir / "config.json"
        _save_json(config_file, project_config)
        console.print(f"[green]Saved project configuration")
        
        # Initialize Xcode project manager and set up Views directory
        console.print("\n[cyan]Setting up Xcode project structure...")
        xcode_manager = XcodeProjectManager(xcode_project_path)
        if xcode_manager.setup_views_directory():
            console.print("[green]Views directory created and configured")
        
        # Start interactive mode
        _start_interactive_mode(project_name, xcode_manager)
        
        logger.info("Project setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        console.print(f"[red]Error creating project: {str(e)}")
        if console.is_terminal:
            console.print_exception()
            
def _start_interactive_mode(project_name: str, xcode_manager: XcodeProjectManager):
    """Start interactive command mode"""
    console.print("\n[cyan]Starting interactive mode. Type 'help' for commands, 'quit' to exit.")
    
    while True:
        try:
            command = Prompt.ask("\nEnter command").strip()
            
            if command == "quit":
                break
            elif command == "help":
                _show_help()
            elif command.startswith("create "):
                view_name = command.split(" ", 1)[1]
                _create_view(view_name, xcode_manager)
            elif command.startswith("list"):
                _list_views(xcode_manager)
            else:
                console.print("[yellow]Unknown command. Type 'help' for available commands.")
                
        except Exception as e:
            logger.error(f"Command error: {str(e)}")
            console.print(f"[red]Error: {str(e)}")

def _show_help():
    """Show available commands"""
    console.print(Panel.fit("""
        Available Commands:
        create <name> - Create a new SwiftUI view
        list         - List existing views
        help        - Show this help
        quit        - Exit interactive mode
    """, title="Commands"))

def _create_view(name: str, xcode_manager: XcodeProjectManager):
    """Create a new SwiftUI view"""
    try:
        # Basic SwiftUI view template
        content = f"""import SwiftUI
import RealityKit

struct {name}View: View {{
    var body: some View {{
        VStack {{
            Text("Hello from {name}View!")
                .font(.title)
        }}
    }}
}}

#Preview {{
    {name}View()
}}
"""
        # Create the view file
        file_path = xcode_manager.create_swiftui_view(name, content)
        console.print(f"[green]Created view at: {file_path}")
        
    except Exception as e:
        logger.error(f"Error creating view: {str(e)}")
        console.print(f"[red]Error creating view: {str(e)}")

def _list_views(xcode_manager: XcodeProjectManager):
    """List all SwiftUI views"""
    try:
        views = xcode_manager.list_views()
        if views:
            console.print("\n[cyan]Available Views:")
            for view in views:
                console.print(f"  - {view}")
        else:
            console.print("[yellow]No views found")
            
    except Exception as e:
        logger.error(f"Error listing views: {str(e)}")
        console.print(f"[red]Error listing views: {str(e)}")

@app.command(name="list-projects")
def list_projects():
    """List all existing projects"""
    try:
        projects_dir = Path.cwd() / "projects"
        if not projects_dir.exists():
            console.print("[yellow]No projects directory found")
            return
            
        projects = [d for d in projects_dir.iterdir() if d.is_dir()]
        
        if not projects:
            console.print("[yellow]No projects found")
            return
            
        console.print("\n[cyan]Available Projects:")
        for project_dir in projects:
            config_file = project_dir / "config.json"
            if config_file.exists():
                config = json.loads(config_file.read_text())
                console.print(f"\n[green]{project_dir.name}:")
                console.print(f"  Xcode Project: {config['xcode_path']}")
                console.print(f"  Created: {config['created_at']}")
            else:
                console.print(f"[yellow]{project_dir.name} (No config found)")
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        console.print(f"[red]Error listing projects: {str(e)}")

@app.command()
def continue_project(
    project_name: str = typer.Option(None, "--name", "-n", prompt="Project name")
):
    """Continue working on an existing project"""
    try:
        project_dir = Path.cwd() / "projects" / project_name
        
        # Verify project exists
        if not project_dir.exists():
            console.print(f"[red]Project {project_name} not found")
            return
            
        # Load project configuration
        config_file = project_dir / "config.json"
        if not config_file.exists():
            console.print(f"[red]No configuration found for project {project_name}")
            return
            
        config = json.loads(config_file.read_text())
        xcode_project_path = Path(config['xcode_path'])
        
        # Verify Xcode project still exists
        if not _validate_xcode_project(xcode_project_path):
            console.print(f"[red]Xcode project no longer exists at: {xcode_project_path}")
            return
            
        # Initialize Xcode project manager
        console.print(f"\n[cyan]Loading project {project_name}...")
        xcode_manager = XcodeProjectManager(xcode_project_path)
        
        # Start interactive mode
        _start_interactive_mode(project_name, xcode_manager)
        
    except Exception as e:
        logger.error(f"Error continuing project: {str(e)}")
        console.print(f"[red]Error continuing project: {str(e)}")
        if console.is_terminal:
            console.print_exception()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """VisionOS Project Manager"""
    if ctx.invoked_subcommand is None:
        # No command given, show menu of options
        projects = _get_available_projects()
        
        console.print("\n[cyan]VisionOS Project Manager")
        
        if projects:
            console.print("\nAvailable Projects:")
            for i, project in enumerate(projects, 1):
                try:
                    config = _load_project_config(project.name)
                    console.print(f"\n{i}. [green]{project.name}")
                    console.print(f"   Xcode Project: {config['xcode_path']}")
                    console.print(f"   Created: {config['created_at']}")
                except Exception as e:
                    logger.error(f"Error loading project {project.name}: {e}")
                    console.print(f"\n{i}. [yellow]{project.name} (Config error)")
            
            console.print("\nOptions:")
            if len(projects) == 1:
                console.print("1. Continue existing project")
            else:
                console.print(f"1-{len(projects)}. Select project to continue")
        else:
            console.print("\n[yellow]No existing projects found")
            
        console.print("n. Create new project")
        console.print("q. Quit")
        
        choice = Prompt.ask("\nWhat would you like to do?", default="q")
        
        if choice.lower() == 'q':
            return
        elif choice.lower() == 'n':
            create_project()
        elif choice.isdigit() and 1 <= int(choice) <= len(projects):
            project = projects[int(choice) - 1]
            continue_project(project.name)
        else:
            console.print("[red]Invalid choice")

def _get_available_projects() -> List[Path]:
    """Get list of available projects"""
    projects_dir = Path.cwd() / "projects"
    if not projects_dir.exists():
        return []
    return [d for d in projects_dir.iterdir() if d.is_dir() and (d / "config.json").exists()]

def _load_project_config(project_name: str) -> Dict:
    """Load project configuration"""
    config_file = Path.cwd() / "projects" / project_name / "config.json"
    if not config_file.exists():
        raise FileNotFoundError(f"No configuration found for project {project_name}")
    return json.loads(config_file.read_text())

if __name__ == "__main__":
    app()