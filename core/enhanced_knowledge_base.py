from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
import logging
from utils.logging import logger

@dataclass
class ComponentMetadata:
    name: str
    type: str  # RealityKit, SwiftUI, etc.
    required_imports: List[str] = field(default_factory=list)
    initialization_pattern: str = ""
    required_permissions: List[str] = field(default_factory=list)
    common_properties: List[Dict[str, Any]] = field(default_factory=list)
    example_implementations: List[Dict[str, Any]] = field(default_factory=list)
    related_components: List[str] = field(default_factory=list)
    constraints: List[Dict[str, Any]] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    documentation_url: str = ""
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class PatternMetadata:
    name: str
    category: str  # initialization, interaction, lifecycle
    description: str
    code_template: str
    required_components: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    example_usage: List[Dict[str, Any]] = field(default_factory=list)
    related_patterns: List[str] = field(default_factory=list)
    documentation_url: str = ""
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ComponentRelationship:
    """Defines a relationship between two components."""
    source: str
    target: str
    relationship_type: str  # parent-child, peer, dependency
    required: bool = False
    state_sharing: Optional[str] = None  # How components share state
    communication_pattern: Optional[str] = None  # How components communicate
    constraints: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)

@dataclass
class ComponentHierarchy:
    """Represents the hierarchy and relationships of components."""
    root_components: Set[str] = field(default_factory=set)
    relationships: Dict[str, List[ComponentRelationship]] = field(default_factory=dict)
    common_combinations: List[List[str]] = field(default_factory=list)
    integration_patterns: Dict[str, List[str]] = field(default_factory=dict)
    
    def add_relationship(self, relationship: ComponentRelationship):
        """Add a relationship between components."""
        if relationship.source not in self.relationships:
            self.relationships[relationship.source] = []
        self.relationships[relationship.source].append(relationship)
    
    def get_children(self, component: str) -> List[ComponentRelationship]:
        """Get all child relationships for a component."""
        return [r for r in self.relationships.get(component, [])
                if r.relationship_type == "parent-child"]
    
    def get_dependencies(self, component: str) -> List[ComponentRelationship]:
        """Get all dependencies for a component."""
        return [r for r in self.relationships.get(component, [])
                if r.relationship_type == "dependency"]
    
    def get_peers(self, component: str) -> List[ComponentRelationship]:
        """Get all peer relationships for a component."""
        return [r for r in self.relationships.get(component, [])
                if r.relationship_type == "peer"]

class EnhancedVisionOSKnowledgeBase:
    """Enhanced knowledge base for VisionOS development patterns and components."""
    
    def __init__(self, data_dir: Path = Path('data/knowledge')):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Core data storage paths
        self.components_path = data_dir / 'components'
        self.patterns_path = data_dir / 'patterns'
        self.relationships_path = data_dir / 'relationships'
        self.validation_path = data_dir / 'validation'
        
        # Create subdirectories
        self.components_path.mkdir(exist_ok=True)
        self.patterns_path.mkdir(exist_ok=True)
        self.relationships_path.mkdir(exist_ok=True)
        self.validation_path.mkdir(exist_ok=True)
        
        # Initialize storage
        self._init_storage()
        
        self.hierarchy = ComponentHierarchy()
        self._load_relationships()
        
    def _init_storage(self):
        """Initialize the storage structure"""
        # Components by type
        self.components: Dict[str, ComponentMetadata] = {}
        
        # Patterns by category
        self.patterns: Dict[str, Dict[str, PatternMetadata]] = {
            "initialization": {},
            "interactions": {},
            "lifecycle": {}
        }
        
        # Relationships
        self.relationships = {
            "component_hierarchy": {},  # Parent-child relationships
            "service_dependencies": {}, # Required system services
            "interaction_flows": {},    # How components interact
        }
        
        # Validation rules
        self.validation_rules = {
            "required_setup": [],      # Must-have initialization
            "compatibility": [],       # Version/device compatibility
            "performance": [],         # Performance guidelines
            "security": []            # Security requirements
        }
        
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing data from storage"""
        try:
            # Load components
            for component_file in self.components_path.glob('*.json'):
                with open(component_file, 'r') as f:
                    data = json.load(f)
                    self.components[data['name']] = ComponentMetadata(**data)
            
            # Load patterns
            for category in self.patterns:
                category_dir = self.patterns_path / category
                if category_dir.exists():
                    for pattern_file in category_dir.glob('*.json'):
                        with open(pattern_file, 'r') as f:
                            data = json.load(f)
                            self.patterns[category][data['name']] = PatternMetadata(**data)
            
            # Load relationships
            if (self.relationships_path / 'relationships.json').exists():
                with open(self.relationships_path / 'relationships.json', 'r') as f:
                    self.relationships = json.load(f)
            
            # Load validation rules
            if (self.validation_path / 'validation_rules.json').exists():
                with open(self.validation_path / 'validation_rules.json', 'r') as f:
                    self.validation_rules = json.load(f)
                    
        except Exception as e:
            logger.error(f"Error loading existing data: {e}")
    
    def add_component(self, component: ComponentMetadata):
        """Add or update a component in the knowledge base"""
        try:
            self.components[component.name] = component
            
            # Save to file
            component_file = self.components_path / f"{component.name}.json"
            with open(component_file, 'w') as f:
                json.dump(asdict(component), f, indent=2)
                
            logger.info(f"Added/updated component: {component.name}")
        except Exception as e:
            logger.error(f"Error adding component {component.name}: {e}")
    
    def add_pattern(self, pattern: PatternMetadata):
        """Add or update a pattern in the knowledge base"""
        try:
            category = pattern.category
            if category not in self.patterns:
                self.patterns[category] = {}
            
            self.patterns[category][pattern.name] = pattern
            
            # Ensure category directory exists
            category_dir = self.patterns_path / category
            category_dir.mkdir(exist_ok=True)
            
            # Save to file
            pattern_file = category_dir / f"{pattern.name}.json"
            with open(pattern_file, 'w') as f:
                json.dump(asdict(pattern), f, indent=2)
                
            logger.info(f"Added/updated pattern: {pattern.name} in category {category}")
        except Exception as e:
            logger.error(f"Error adding pattern {pattern.name}: {e}")
    
    def add_component_relationship(self, relationship: ComponentRelationship):
        """Add a relationship between components."""
        self.hierarchy.add_relationship(relationship)
        self._save_relationships()
    
    def add_common_combination(self, components: List[str]):
        """Add a commonly used combination of components."""
        self.hierarchy.common_combinations.append(components)
        self._save_relationships()
    
    def add_integration_pattern(self, pattern_name: str, components: List[str]):
        """Add an integration pattern for components."""
        self.hierarchy.integration_patterns[pattern_name] = components
        self._save_relationships()
    
    def get_component_hierarchy(self, component: str) -> Dict[str, Any]:
        """Get the complete hierarchy for a component."""
        result = {
            "children": [asdict(r) for r in self.hierarchy.get_children(component)],
            "dependencies": [asdict(r) for r in self.hierarchy.get_dependencies(component)],
            "peers": [asdict(r) for r in self.hierarchy.get_peers(component)],
            "common_combinations": [
                combo for combo in self.hierarchy.common_combinations
                if component in combo
            ],
            "integration_patterns": {
                name: pattern
                for name, pattern in self.hierarchy.integration_patterns.items()
                if component in pattern
            }
        }
        return result
    
    def _save_relationships(self):
        """Save relationship data to disk."""
        relationships_file = self.relationships_path / 'component_relationships.json'
        data = {
            "root_components": list(self.hierarchy.root_components),
            "relationships": {
                source: [asdict(r) for r in rels]
                for source, rels in self.hierarchy.relationships.items()
            },
            "common_combinations": self.hierarchy.common_combinations,
            "integration_patterns": self.hierarchy.integration_patterns
        }
        relationships_file.write_text(json.dumps(data, indent=2))
    
    def _load_relationships(self):
        """Load relationship data from disk."""
        relationships_file = self.relationships_path / 'component_relationships.json'
        if relationships_file.exists():
            data = json.loads(relationships_file.read_text())
            self.hierarchy.root_components = set(data["root_components"])
            self.hierarchy.relationships = {
                source: [
                    ComponentRelationship(**rel_data)
                    for rel_data in rels
                ]
                for source, rels in data["relationships"].items()
            }
            self.hierarchy.common_combinations = data["common_combinations"]
            self.hierarchy.integration_patterns = data["integration_patterns"]
    
    def add_relationship(self, relationship_type: str, source: str, target: str, metadata: Dict[str, Any] = None):
        """Add a relationship between components"""
        try:
            if relationship_type not in self.relationships:
                self.relationships[relationship_type] = {}
            
            if source not in self.relationships[relationship_type]:
                self.relationships[relationship_type][source] = {}
            
            self.relationships[relationship_type][source][target] = metadata or {}
            
            # Save relationships
            with open(self.relationships_path / 'relationships.json', 'w') as f:
                json.dump(self.relationships, f, indent=2)
                
            logger.info(f"Added relationship: {source} -> {target} ({relationship_type})")
        except Exception as e:
            logger.error(f"Error adding relationship: {e}")
    
    def add_validation_rule(self, category: str, rule: Dict[str, Any]):
        """Add a validation rule"""
        try:
            if category not in self.validation_rules:
                self.validation_rules[category] = []
            
            self.validation_rules[category].append(rule)
            
            # Save validation rules
            with open(self.validation_path / 'validation_rules.json', 'w') as f:
                json.dump(self.validation_rules, f, indent=2)
                
            logger.info(f"Added validation rule to category: {category}")
        except Exception as e:
            logger.error(f"Error adding validation rule: {e}")
    
    def get_component(self, name: str) -> Optional[ComponentMetadata]:
        """Get component by name"""
        return self.components.get(name)
    
    def get_pattern(self, category: str, name: str) -> Optional[PatternMetadata]:
        """Get pattern by category and name"""
        return self.patterns.get(category, {}).get(name)
    
    def get_related_components(self, component_name: str) -> List[str]:
        """Get components related to the given component"""
        related = set()
        
        # Check component hierarchy
        hierarchy = self.relationships["component_hierarchy"]
        if component_name in hierarchy:
            related.update(hierarchy[component_name].keys())
        
        # Check service dependencies
        dependencies = self.relationships["service_dependencies"]
        if component_name in dependencies:
            related.update(dependencies[component_name].keys())
        
        # Check interaction flows
        flows = self.relationships["interaction_flows"]
        if component_name in flows:
            related.update(flows[component_name].keys())
        
        return list(related)
    
    def get_required_patterns(self, component_name: str) -> List[PatternMetadata]:
        """Get patterns required for a component"""
        component = self.get_component(component_name)
        if not component:
            return []
        
        required_patterns = []
        for category in self.patterns:
            for pattern in self.patterns[category].values():
                if component_name in pattern.required_components:
                    required_patterns.append(pattern)
        
        return required_patterns
    
    def validate_component_usage(self, component_name: str, context: Dict[str, Any]) -> List[str]:
        """Validate component usage in a given context"""
        issues = []
        component = self.get_component(component_name)
        
        if not component:
            return ["Component not found"]
        
        # Check required permissions
        for permission in component.required_permissions:
            if permission not in context.get('permissions', []):
                issues.append(f"Missing required permission: {permission}")
        
        # Check required imports
        for imp in component.required_imports:
            if imp not in context.get('imports', []):
                issues.append(f"Missing required import: {imp}")
        
        # Check constraints
        for constraint in component.constraints:
            constraint_type = constraint['type']
            if constraint_type == 'version':
                if context.get('os_version', '') < constraint['min_version']:
                    issues.append(f"Requires minimum OS version: {constraint['min_version']}")
            elif constraint_type == 'device':
                if context.get('device_type') not in constraint['supported_devices']:
                    issues.append(f"Not supported on device type: {context.get('device_type')}")
        
        return issues
