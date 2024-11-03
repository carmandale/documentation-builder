import json
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from collections import defaultdict
import logging
from datetime import datetime

console = Console()
logger = logging.getLogger(__name__)

class DocumentationAnalyzer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.latest_doc = None
        self.latest_manifest = None
        self.documentation = []
        self.analysis_results = {}
        
    def load_latest_documentation(self):
        """Load the most recent documentation files"""
        doc_files = list(self.data_dir.glob('visionos_documentation_*.json'))
        manifest_files = list(self.data_dir.glob('manifest_*.json'))
        
        if not doc_files:
            raise FileNotFoundError("No documentation files found")
            
        self.latest_doc = max(doc_files, key=lambda x: x.stat().st_mtime)
        self.latest_manifest = max(manifest_files, key=lambda x: x.stat().st_mtime)
        
        with open(self.latest_doc) as f:
            self.documentation = json.load(f)
            
        console.print(f"[green]Loaded documentation from {self.latest_doc.name}[/green]")
        
    def analyze_coverage(self) -> Dict[str, Any]:
        """Analyze documentation coverage and completeness"""
        topics = defaultdict(int)
        missing_fields = defaultdict(int)
        total_entries = len(self.documentation)
        
        for entry in self.documentation:
            # Track topics/categories
            if 'metadata' in entry and 'category' in entry['metadata']:
                topics[entry['metadata']['category']] += 1
                
            # Track missing important fields
            for field in ['description', 'examples', 'parameters']:
                if not entry.get(field):
                    missing_fields[field] += 1
        
        return {
            'total_entries': total_entries,
            'topics': dict(topics),
            'missing_fields': dict(missing_fields),
            'coverage_score': self._calculate_coverage_score(missing_fields, total_entries)
        }
    
    def analyze_code_examples(self) -> Dict[str, Any]:
        """Analyze the quality and presence of code examples"""
        examples_stats = {
            'total_examples': 0,
            'entries_with_examples': 0,
            'example_types': defaultdict(int)
        }
        
        for entry in self.documentation:
            if entry.get('examples'):
                examples_stats['entries_with_examples'] += 1
                examples_stats['total_examples'] += len(entry['examples'])
                
                # Categorize examples
                for example in entry['examples']:
                    if 'SwiftUI' in example.get('code', ''):
                        examples_stats['example_types']['SwiftUI'] += 1
                    if 'RealityKit' in example.get('code', ''):
                        examples_stats['example_types']['RealityKit'] += 1
        
        return examples_stats
    
    def analyze_relationships(self) -> Dict[str, List[str]]:
        """Analyze relationships between different documentation entries"""
        relationships = defaultdict(list)
        
        for entry in self.documentation:
            title = entry['title']
            # Look for related entries based on common keywords or references
            related = [
                other['title'] for other in self.documentation
                if other['title'] != title and
                (any(keyword in other['description'] 
                    for keyword in entry['title'].lower().split())
                 or any(keyword in other['title'].lower().split() 
                    for keyword in entry['title'].lower().split()))
            ]
            if related:
                relationships[title] = related
                
        return dict(relationships)
    
    def generate_llm_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for LLM consumption of the documentation"""
        recommendations = {
            'structured_topics': [],
            'key_concepts': set(),
            'suggested_prompts': [],
            'improvement_areas': []
        }
        
        # Analyze and group related concepts
        for entry in self.documentation:
            # Extract key concepts from titles and descriptions
            keywords = self._extract_key_concepts(entry['title'], entry['description'])
            recommendations['key_concepts'].update(keywords)
            
            # Group related topics
            topic = self._categorize_entry(entry)
            if topic:
                recommendations['structured_topics'].append({
                    'topic': topic,
                    'title': entry['title'],
                    'key_points': self._extract_key_points(entry)
                })
        
        # Generate suggested prompts
        recommendations['suggested_prompts'] = self._generate_prompt_templates()
        
        return recommendations
    
    def _calculate_coverage_score(self, missing_fields: Dict[str, int], total_entries: int) -> float:
        """Calculate a coverage score based on completeness of documentation"""
        if total_entries == 0:
            return 0.0
            
        fields_weight = {
            'description': 0.4,
            'examples': 0.4,
            'parameters': 0.2
        }
        
        score = 1.0
        for field, count in missing_fields.items():
            score -= (count / total_entries) * fields_weight.get(field, 0.1)
            
        return max(0.0, min(1.0, score))
    
    def _extract_key_concepts(self, title: str, description: str) -> set:
        """Extract key technical concepts from text"""
        # This could be enhanced with NLP techniques
        combined_text = f"{title} {description}".lower()
        key_terms = {
            'SwiftUI', 'RealityKit', 'ARKit', '3D', 'spatial', 'immersive',
            'window', 'volume', 'gesture', 'animation', 'scene', 'material'
        }
        return {term for term in key_terms if term.lower() in combined_text}
    
    def _categorize_entry(self, entry: Dict[str, Any]) -> str:
        """Categorize documentation entry into high-level topics"""
        title = entry['title'].lower()
        if 'window' in title or 'view' in title:
            return 'UI Components'
        elif '3d' in title or 'reality' in title:
            return '3D Content'
        elif 'gesture' in title or 'interaction' in title:
            return 'User Interaction'
        elif 'animation' in title:
            return 'Animation'
        return 'General'
    
    def _extract_key_points(self, entry: Dict[str, Any]) -> List[str]:
        """Extract key points from an entry for LLM consumption"""
        points = []
        if entry.get('description'):
            points.append(entry['description'])
        if entry.get('parameters'):
            points.append(f"Requires parameters: {', '.join(p['name'] for p in entry['parameters'])}")
        if entry.get('examples'):
            points.append(f"Includes {len(entry['examples'])} code examples")
        return points
    
    def _generate_prompt_templates(self) -> List[str]:
        """Generate template prompts for common VisionOS development tasks"""
        return [
            "How do I create a {component_type} in VisionOS using SwiftUI?",
            "What are the best practices for implementing {feature_type} in a VisionOS app?",
            "Show me an example of {interaction_type} in VisionOS",
            "How do I integrate {framework} with my VisionOS app?",
            "What are the key considerations when designing {ui_element} for VisionOS?"
        ]
    
    def display_analysis(self):
        """Display the analysis results in a formatted way"""
        console.print("\n[bold blue]Documentation Analysis Report[/bold blue]")
        
        # Coverage Analysis
        coverage = self.analyze_coverage()
        console.print(Panel(
            f"[bold]Coverage Analysis[/bold]\n\n"
            f"Total Entries: {coverage['total_entries']}\n"
            f"Coverage Score: {coverage['coverage_score']:.2%}\n"
            f"Missing Fields:\n" +
            "\n".join(f"  - {k}: {v}" for k, v in coverage['missing_fields'].items())
        ))
        
        # Code Examples Analysis
        examples = self.analyze_code_examples()
        console.print(Panel(
            f"[bold]Code Examples Analysis[/bold]\n\n"
            f"Entries with Examples: {examples['entries_with_examples']}\n"
            f"Total Examples: {examples['total_examples']}\n"
            f"Example Types:\n" +
            "\n".join(f"  - {k}: {v}" for k, v in examples['example_types'].items())
        ))
        
        # Relationships
        relationships = self.analyze_relationships()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Topic")
        table.add_column("Related To")
        
        for topic, related in list(relationships.items())[:10]:  # Show top 10
            table.add_row(topic, "\n".join(related[:3]))  # Show top 3 related
        
        console.print("\n[bold]Related Topics[/bold]")
        console.print(table)
        
        # LLM Recommendations
        recommendations = self.generate_llm_recommendations()
        console.print(Panel(
            f"[bold]LLM Usage Recommendations[/bold]\n\n"
            f"Key Concepts:\n" +
            "\n".join(f"  - {concept}" for concept in sorted(recommendations['key_concepts'])) +
            "\n\nSuggested Prompt Templates:\n" +
            "\n".join(f"  - {prompt}" for prompt in recommendations['suggested_prompts'])
        ))
        
        # Add raw sample display at the end
        self.display_raw_sample()
    
    def display_raw_sample(self):
        """Display a sample of the raw documentation data"""
        console.print("\n[bold blue]Raw Documentation Sample[/bold blue]")
        
        if not self.documentation:
            console.print("[red]No documentation loaded[/red]")
            return
            
        sample = self.documentation[0]
        console.print(Panel(
            f"[bold]Sample Entry[/bold]\n\n"
            f"Title: {sample.get('title', 'N/A')}\n"
            f"URL: {sample.get('url', 'N/A')}\n"
            f"Description: {sample.get('description', 'N/A')[:200]}...\n"
            f"Framework: {sample.get('framework', 'N/A')}\n"
            f"Metadata: {json.dumps(sample.get('metadata', {}), indent=2)}"
        ))

if __name__ == "__main__":
    analyzer = DocumentationAnalyzer()
    analyzer.load_latest_documentation()
    analyzer.display_analysis() 