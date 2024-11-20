from typing import Dict, List, Optional, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import re

@dataclass
class ProjectStructure:
    """Represents the structure and organization of a sample project"""
    main_files: List[str]
    view_files: List[str]
    model_files: List[str]
    helper_files: List[str]
    resources: List[str]
    dependencies: Set[str]

@dataclass
class CodePattern:
    """A reusable code pattern found in the sample"""
    name: str
    file_path: str
    line_number: int
    code_snippet: str
    dependencies: List[str]
    usage_context: str

@dataclass
class BestPractice:
    """A best practice demonstrated in the sample"""
    category: str
    description: str
    example_file: str
    example_code: str
    rationale: str

class ProjectAnalyzer:
    """Analyzes Apple sample projects to extract patterns and best practices"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.structure = self._analyze_structure()
        self.patterns: List[CodePattern] = []
        self.best_practices: List[BestPractice] = []
        
    def _analyze_structure(self) -> ProjectStructure:
        """Analyze project structure and organization"""
        main_files = []
        view_files = []
        model_files = []
        helper_files = []
        resources = []
        dependencies = set()
        
        # Recursively analyze project structure
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.project_path)
                path_str = str(rel_path)
                
                if path_str.endswith('.swift'):
                    # Analyze file content to categorize
                    content = file_path.read_text()
                    
                    if 'import' in content:
                        # Extract dependencies
                        for line in content.split('\n'):
                            if line.strip().startswith('import'):
                                dep = line.split()[1].strip()
                                dependencies.add(dep)
                    
                    if 'App.swift' in path_str:
                        main_files.append(path_str)
                    elif 'View' in path_str:
                        view_files.append(path_str)
                    elif 'Model' in path_str or 'Data' in path_str:
                        model_files.append(path_str)
                    else:
                        helper_files.append(path_str)
                else:
                    resources.append(path_str)
        
        return ProjectStructure(
            main_files=main_files,
            view_files=view_files,
            model_files=model_files,
            helper_files=helper_files,
            resources=resources,
            dependencies=dependencies
        )
    
    def analyze_patterns(self):
        """Extract reusable code patterns"""
        for file_path in self.project_path.rglob('*.swift'):
            content = file_path.read_text()
            rel_path = file_path.relative_to(self.project_path)
            
            # Look for common VisionOS patterns
            patterns = [
                (r'@Observable\s+class\s+(\w+)', 'Observable Class Pattern'),
                (r'RealityView\s*{[^}]+}', 'RealityView Pattern'),
                (r'ImmersiveSpace\s*{[^}]+}', 'ImmersiveSpace Pattern'),
                (r'@Model\s+class\s+(\w+)', 'Model Class Pattern'),
                (r'Entity\s*{[^}]+}', 'Entity Pattern'),
                (r'WindowGroup\s*{[^}]+}', 'WindowGroup Pattern'),
            ]
            
            for line_num, line in enumerate(content.split('\n'), 1):
                for pattern, name in patterns:
                    if re.search(pattern, line):
                        self.patterns.append(CodePattern(
                            name=name,
                            file_path=str(rel_path),
                            line_number=line_num,
                            code_snippet=line.strip(),
                            dependencies=self._get_dependencies(content),
                            usage_context=self._get_context(content, line_num)
                        ))
    
    def analyze_best_practices(self):
        """Extract best practices from code organization and patterns"""
        # Analyze file organization
        if self.structure.model_files:
            self.best_practices.append(BestPractice(
                category="Project Structure",
                description="Separate model logic into dedicated files",
                example_file=self.structure.model_files[0],
                example_code="Model files: " + ", ".join(self.structure.model_files),
                rationale="Improves code organization and maintainability"
            ))
        
        # Analyze view hierarchy
        view_hierarchy = self._analyze_view_hierarchy()
        if view_hierarchy:
            self.best_practices.append(BestPractice(
                category="View Architecture",
                description="Organize views hierarchically with clear parent-child relationships",
                example_file=view_hierarchy[0] if view_hierarchy else "",
                example_code="View hierarchy: " + " -> ".join(view_hierarchy),
                rationale="Creates maintainable and reusable view components"
            ))
    
    def _get_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from file content"""
        deps = []
        for line in content.split('\n'):
            if line.strip().startswith('import'):
                deps.append(line.split()[1].strip())
        return deps
    
    def _get_context(self, content: str, target_line: int, context_lines: int = 3) -> str:
        """Get surrounding context for a line of code"""
        lines = content.split('\n')
        start = max(0, target_line - context_lines - 1)
        end = min(len(lines), target_line + context_lines)
        return '\n'.join(lines[start:end])
    
    def _analyze_view_hierarchy(self) -> List[str]:
        """Analyze view hierarchy in the project"""
        hierarchy = []
        for view_file in self.structure.view_files:
            content = (self.project_path / view_file).read_text()
            # Look for parent view
            if 'WindowGroup' in content or 'ImmersiveSpace' in content:
                hierarchy.insert(0, view_file)
            else:
                hierarchy.append(view_file)
        return hierarchy
    
    def generate_development_plan(self) -> Dict:
        """Generate a development plan based on project analysis"""
        return {
            'project_structure': {
                'main_files': self.structure.main_files,
                'view_files': self.structure.view_files,
                'model_files': self.structure.model_files,
                'helper_files': self.structure.helper_files,
                'resources': self.structure.resources
            },
            'dependencies': list(self.structure.dependencies),
            'patterns': [
                {
                    'name': pattern.name,
                    'file': pattern.file_path,
                    'usage': pattern.usage_context
                }
                for pattern in self.patterns
            ],
            'best_practices': [
                {
                    'category': bp.category,
                    'description': bp.description,
                    'rationale': bp.rationale
                }
                for bp in self.best_practices
            ],
            'implementation_steps': self._generate_implementation_steps()
        }
    
    def _generate_implementation_steps(self) -> List[Dict]:
        """Generate implementation steps based on project analysis"""
        steps = []
        
        # Project setup
        steps.append({
            'phase': 'Setup',
            'steps': [
                'Create new VisionOS project',
                f'Add required dependencies: {", ".join(self.structure.dependencies)}',
                'Set up project structure following sample organization'
            ]
        })
        
        # Core implementation
        if self.structure.model_files:
            steps.append({
                'phase': 'Data Model',
                'steps': [
                    'Create data models',
                    'Implement Observable patterns',
                    'Set up data persistence if needed'
                ]
            })
        
        # View implementation
        view_hierarchy = self._analyze_view_hierarchy()
        if view_hierarchy:
            steps.append({
                'phase': 'View Implementation',
                'steps': [
                    'Create main app view structure',
                    'Implement child views',
                    'Add navigation and state management'
                ]
            })
        
        return steps
