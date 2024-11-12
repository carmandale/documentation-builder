from pathlib import Path
from typing import Dict, Optional, List
import json
import shutil
from datetime import datetime
from utils.logging import logger
from rich.prompt import Confirm

class XcodeProjectManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self._analyze_project_structure()
        
    def _analyze_project_structure(self):
        """Find key project directories and files"""
        try:
            # Find .xcodeproj
            self.xcodeproj = next(self.project_root.glob("*.xcodeproj"))
            
            # Find main app directory (same name as xcodeproj)
            app_name = self.xcodeproj.stem
            self.app_dir = self.project_root / app_name
            
            if not self.app_dir.exists():
                raise FileNotFoundError(f"App directory not found: {self.app_dir}")
                
            # Check for Views directory
            self.views_dir = self.app_dir / "Views"
            self.has_views_dir = self.views_dir.exists()
            
            logger.info(f"Project structure analyzed:")
            logger.info(f"  Project: {self.xcodeproj}")
            logger.info(f"  App Directory: {self.app_dir}")
            logger.info(f"  Views Directory: {'Exists' if self.has_views_dir else 'Not present'}")
            
        except Exception as e:
            logger.error(f"Error analyzing project structure: {str(e)}")
            raise
            
    def setup_views_directory(self) -> bool:
        """Create Views directory and move existing views if user wants it"""
        if not self.has_views_dir:
            if Confirm.ask("Would you like to create a Views directory for better organization?"):
                # Create Views directory
                self.views_dir = self.app_dir / "Views"
                self.views_dir.mkdir(exist_ok=True)
                self.has_views_dir = True
                logger.info(f"Created Views directory: {self.views_dir}")
                
                # Find and move existing view files
                view_files = list(self.app_dir.glob("*View.swift"))
                if view_files:
                    if Confirm.ask(f"Found {len(view_files)} view files. Move them to Views directory?"):
                        for file in view_files:
                            # Create backup
                            backup_path = file.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                            shutil.copy2(file, backup_path)
                            logger.info(f"Backed up {file.name} to {backup_path}")
                            
                            # Move file
                            new_path = self.views_dir / file.name
                            shutil.move(file, new_path)
                            logger.info(f"Moved {file.name} to Views directory")
                
                return True
        return False
        
    def create_swiftui_view(self, name: str, content: str) -> Path:
        """Create a new SwiftUI view file"""
        # Ensure proper naming
        if not name.endswith("View.swift"):
            name = f"{name}View.swift"
            
        # Determine target directory
        target_dir = self.views_dir if self.has_views_dir else self.app_dir
        file_path = target_dir / name
        
        # Backup any existing file
        if file_path.exists():
            backup_path = file_path.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.copy2(file_path, backup_path)
            logger.info(f"Backed up existing file to {backup_path}")
            
        # Write new content
        file_path.write_text(content)
        logger.info(f"Created SwiftUI view at {file_path}")
        
        return file_path
        
    def edit_swiftui_view(self, name: str, content: str):
        """Edit an existing SwiftUI view"""
        # Ensure proper naming
        if not name.endswith("View.swift"):
            name = f"{name}View.swift"
            
        file_path = self.views_dir / name
        if not file_path.exists():
            raise FileNotFoundError(f"View file {name} not found")
            
        # Create backup
        backup_path = file_path.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(file_path, backup_path)
        logger.info(f"Backed up file to {backup_path}")
        
        # Update file
        file_path.write_text(content)
        logger.info(f"Updated SwiftUI view at {file_path}")
        
    def get_view_content(self, name: str) -> Optional[str]:
        """Get content of an existing view"""
        if not name.endswith("View.swift"):
            name = f"{name}View.swift"
            
        file_path = self.views_dir / name
        if not file_path.exists():
            return None
            
        return file_path.read_text()
        
    def list_views(self) -> List[str]:
        """List all SwiftUI views in the project"""
        return [f.stem for f in self.views_dir.glob("*View.swift")]