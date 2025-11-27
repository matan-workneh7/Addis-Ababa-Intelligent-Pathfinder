"""
Pure generic path calculator implementation.
Completely domain-agnostic and reusable for any graph type.
"""

from typing import List, Dict, Any

from core.graph_interface import GraphInterface, PathCalculatorInterface


class GenericPathCalculator(PathCalculatorInterface):
    """Generic path calculator implementation."""
    
    def calculate_path_cost(self, path: List[int], graph: GraphInterface) -> float:
        """
        Calculate total cost of a path.
        
        Args:
            path: List of node IDs
            graph: Graph implementation
            
        Returns:
            Total cost of the path
        """
        total_cost = 0.0
        
        for i in range(len(path) - 1):
            try:
                edge_data = graph.get_edge_data(path[i], path[i+1])
                if edge_data and 'length' in edge_data:
                    total_cost += edge_data['length']
                else:
                    # Fallback: use unit cost
                    total_cost += 1.0
            except:
                continue
                
        return total_cost
    
    def paths_are_similar(self, path1: List[int], path2: List[int], threshold: float = 0.8) -> bool:
        """
        Check if two paths are essentially the same based on node overlap.
        
        Args:
            path1: First path
            path2: Second path
            threshold: Similarity threshold (0.0 to 1.0)
            
        Returns:
            True if paths are similar, False otherwise
        """
        if not path2:
            return False
            
        # Calculate similarity based on common nodes
        common_nodes = set(path1) & set(path2)
        similarity = len(common_nodes) / max(len(set(path1)), len(set(path2)))
        return similarity > threshold
    
    def get_path_statistics(self, paths: List[List[int]], graph: GraphInterface) -> Dict[str, Any]:
        """
        Get statistics for a collection of paths.
        
        Args:
            paths: List of paths
            graph: Graph implementation
            
        Returns:
            Dictionary with path statistics
        """
        if not paths:
            return {"count": 0, "avg_cost": 0, "avg_steps": 0}
        
        costs = [self.calculate_path_cost(path, graph) for path in paths]
        steps = [len(path) - 1 for path in paths]  # steps = nodes - 1
        
        return {
            "count": len(paths),
            "avg_cost": sum(costs) / len(costs),
            "avg_steps": sum(steps) / len(steps),
            "min_cost": min(costs),
            "max_cost": max(costs),
            "min_steps": min(steps),
            "max_steps": max(steps)
        }
