"""
NetworkX graph adapter.
Adapts NetworkX graphs to the generic GraphInterface.
"""

from typing import List, Dict, Any, Optional

from .graph_interface import GraphInterface


class NetworkXGraphAdapter(GraphInterface):
    """Adapter for NetworkX graphs to implement GraphInterface."""
    
    def __init__(self, networkx_graph):
        """Initialize with a NetworkX graph."""
        self.graph = networkx_graph
    
    def get_neighbors(self, node: int) -> List[int]:
        """Get neighbors of a node."""
        return list(self.graph.neighbors(node))
    
    def node_exists(self, node: int) -> bool:
        """Check if a node exists."""
        return node in self.graph.nodes
    
    def edge_exists(self, u: int, v: int) -> bool:
        """Check if an edge exists."""
        return self.graph.has_edge(u, v)
    
    def get_node_data(self, node: int) -> Dict[str, Any]:
        """Get data for a node."""
        return dict(self.graph.nodes[node])
    
    def get_edge_data(self, u: int, v: int) -> Optional[Dict[str, Any]]:
        """Get edge data."""
        try:
            edge_data = self.graph.get_edge_data(u, v)
            return dict(edge_data) if edge_data else None
        except:
            return None
    
    def get_subgraph(self, nodes: List[int]) -> 'NetworkXGraphAdapter':
        """Get subgraph with specified nodes."""
        subgraph = self.graph.subgraph(nodes)
        return NetworkXGraphAdapter(subgraph)
