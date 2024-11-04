from pathlib import Path
import json
import networkx as nx
from typing import Dict, List, Set, Tuple
import matplotlib.pyplot as plt
from rich.console import Console
import logging
import numpy as np

logger = logging.getLogger(__name__)
console = Console()

class TopicAnalyzer:
    """Analyzes relationships between documentation topics"""
    
    def __init__(self, extracted_dir: Path = Path('data/extracted')):
        self.extracted_dir = extracted_dir
        self.graph = nx.DiGraph()
        
    def analyze_relationships(self) -> nx.DiGraph:
        """Build a graph of topic relationships"""
        # Load all extracted files
        files = list(self.extracted_dir.glob("extracted_*.json"))
        
        if not files:
            logger.warning(f"No extracted files found in {self.extracted_dir}")
            return self.graph
        
        # Track topics and their relationships
        topics_by_page: Dict[str, List[str]] = {}  # page -> topics
        topic_categories: Dict[str, str] = {}  # topic -> category
        
        # First pass: collect all topics and their categories
        for file in files:
            with open(file) as f:
                data = json.load(f)
                title = data['title']
                category = data.get('category', 'Other')
                
                # Get topics from this page
                page_topics = [t['title'] for t in data.get('topics', [])]
                topics_by_page[title] = page_topics
                
                # Associate topics with categories
                for topic in page_topics:
                    topic_categories[topic] = category
        
        # Build relationships based on co-occurrence and hierarchy
        for page_title, topics in topics_by_page.items():
            if not topics:
                continue
                
            # Create relationships between consecutive topics (hierarchy)
            for i in range(len(topics) - 1):
                self.graph.add_edge(topics[i], topics[i + 1], weight=1)
            
            # Create relationships between topics that appear on the same page
            for i, topic1 in enumerate(topics):
                for topic2 in topics[i + 1:]:
                    if self.graph.has_edge(topic1, topic2):
                        # Increment weight if relationship already exists
                        self.graph[topic1][topic2]['weight'] += 1
                    else:
                        self.graph.add_edge(topic1, topic2, weight=1)
        
        # Add category information to nodes
        for topic, category in topic_categories.items():
            if topic in self.graph:
                self.graph.nodes[topic]['category'] = category
        
        return self.graph
    
    def visualize_relationships(self, output_file: Path = Path('data/topic_graph.png')):
        """Create a visualization of topic relationships"""
        if not self.graph:
            self.analyze_relationships()
            
        if len(self.graph) == 0:
            logger.warning("No relationships found to visualize")
            return
            
        # Create the visualization
        plt.figure(figsize=(20, 15))
        
        # Use spring layout with adjusted parameters
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # Get categories for coloring
        categories = {
            data.get('category', 'Other') 
            for _, data in self.graph.nodes(data=True)
        }
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        color_map = dict(zip(categories, colors))
        
        # Draw nodes with colors based on category
        for category in categories:
            nodes = [
                node for node, data in self.graph.nodes(data=True)
                if data.get('category', 'Other') == category
            ]
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=nodes,
                node_color=[color_map[category]],
                node_size=2000,
                alpha=0.7,
                label=category
            )
        
        # Draw edges with varying thickness based on weight
        edges = self.graph.edges(data=True)
        weights = [data['weight'] for _, _, data in edges]
        nx.draw_networkx_edges(
            self.graph, pos,
            width=[w/max(weights) * 3 for w in weights],
            edge_color='gray',
            alpha=0.5,
            arrows=True,
            arrowsize=20
        )
        
        # Add labels with wrapped text
        labels = {
            node: '\n'.join(self._wrap_text(node, 20))
            for node in self.graph.nodes()
        }
        nx.draw_networkx_labels(
            self.graph, pos,
            labels,
            font_size=8,
            font_weight='bold'
        )
        
        plt.title("VisionOS Documentation Topic Relationships", pad=20, size=16)
        plt.legend(title="Categories", title_fontsize=12)
        plt.axis('off')
        
        # Save the visualization
        output_file.parent.mkdir(exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        console.print(f"[green]Topic relationship graph saved to {output_file}")
        
        # Close the figure to free memory
        plt.close()
    
    def get_central_topics(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """Get the most central topics based on PageRank"""
        if not self.graph:
            self.analyze_relationships()
            
        if len(self.graph) == 0:
            return []
            
        try:
            # Calculate both PageRank and degree centrality
            pagerank = nx.pagerank(self.graph, alpha=0.85)
            degree = nx.degree_centrality(self.graph)
            
            # Combine the scores
            combined_scores = {
                node: (pagerank.get(node, 0) + degree.get(node, 0)) / 2
                for node in self.graph.nodes()
            }
            
            return sorted(
                combined_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_n]
            
        except Exception as e:
            logger.error(f"Error calculating centrality: {str(e)}")
            return []
    
    def get_topic_clusters(self) -> Dict[str, List[str]]:
        """Identify clusters of related topics"""
        if not self.graph:
            self.analyze_relationships()
            
        if len(self.graph) == 0:
            return {}
            
        try:
            # Convert to undirected graph for community detection
            undirected = self.graph.to_undirected()
            
            # Use connected components if the graph is too sparse
            if nx.number_connected_components(undirected) > 1:
                communities = list(nx.connected_components(undirected))
            else:
                try:
                    communities = nx.community.louvain_communities(undirected)
                except Exception:
                    # Fallback to simpler clustering
                    communities = [set(self.graph.nodes())]
            
            # Create named clusters based on dominant category
            clusters = {}
            for i, community in enumerate(communities, 1):
                # Get the most common category in this cluster
                categories = [
                    self.graph.nodes[node].get('category', 'Other')
                    for node in community
                ]
                dominant_category = max(set(categories), key=categories.count)
                clusters[f"Cluster {i} ({dominant_category})"] = list(community)
                
            return clusters
            
        except Exception as e:
            logger.error(f"Error detecting communities: {str(e)}")
            return {"Main Cluster": list(self.graph.nodes())}
    
    @staticmethod
    def _wrap_text(text: str, width: int) -> List[str]:
        """Wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
    
    def visualize_hierarchical(self, output_file: Path = Path('data/topic_hierarchy.png')):
        """Create a hierarchical visualization of topic relationships"""
        if not self.graph:
            self.analyze_relationships()
            
        if len(self.graph) == 0:
            logger.warning("No relationships found to visualize")
            return
            
        plt.figure(figsize=(20, 15))
        
        # Use spring layout with adjusted parameters for better hierarchy
        pos = nx.spring_layout(
            self.graph,
            k=2.0,  # Increase node spacing
            iterations=50,  # More iterations for better layout
            seed=42  # For consistent layout
        )
        
        # Get categories for coloring
        categories = {
            data.get('category', 'Other') 
            for _, data in self.graph.nodes(data=True)
        }
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        color_map = dict(zip(categories, colors))
        
        # Draw nodes by category with larger sizes
        for category in categories:
            nodes = [
                node for node, data in self.graph.nodes(data=True)
                if data.get('category', 'Other') == category
            ]
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=nodes,
                node_color=[color_map[category]],
                node_size=4000,  # Larger nodes
                alpha=0.7,
                label=category
            )
        
        # Draw edges with varying width based on weight
        edges = self.graph.edges(data=True)
        edge_weights = [data.get('weight', 1) for _, _, data in edges]
        max_weight = max(edge_weights) if edge_weights else 1
        
        nx.draw_networkx_edges(
            self.graph, pos,
            width=[w/max_weight * 2 for w in edge_weights],
            edge_color='gray',
            alpha=0.5,
            arrows=True,
            arrowsize=20
        )
        
        # Add labels with wrapped text
        labels = {
            node: '\n'.join(self._wrap_text(node, 20))
            for node in self.graph.nodes()
        }
        nx.draw_networkx_labels(
            self.graph, pos,
            labels,
            font_size=8,
            font_weight='bold'
        )
        
        plt.title("VisionOS Documentation Topic Hierarchy", pad=20, size=16)
        plt.legend(title="Categories", title_fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.axis('off')
        
        # Save the visualization with extra margin for legend
        plt.tight_layout()
        output_file.parent.mkdir(exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        console.print(f"[green]Topic hierarchy saved to {output_file}")
        
        plt.close()