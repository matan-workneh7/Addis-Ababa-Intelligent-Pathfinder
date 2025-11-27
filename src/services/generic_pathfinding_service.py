"""
Pure generic pathfinding service.
Completely domain-agnostic and reusable for any graph type and algorithm.
"""

from typing import List, Optional, Iterator, Dict, Any

from core.graph_interface import (
    GraphInterface, PathfindingAlgorithmInterface, ConstraintInterface,
    MessageHandlerInterface, PathCalculatorInterface
)


class GenericPathfindingService:
    """Pure generic pathfinding service for any graph type and algorithm."""
    
    def __init__(self, graph: GraphInterface, algorithm: PathfindingAlgorithmInterface,
                 path_calculator: PathCalculatorInterface, message_handler: MessageHandlerInterface = None):
        """
        Initialize with generic components.
        
        Args:
            graph: Graph implementation
            algorithm: Pathfinding algorithm (BFS, DFS, A*, etc.)
            path_calculator: Calculator for path costs and statistics
            message_handler: Optional message handler
        """
        self.graph = graph
        self.algorithm = algorithm
        self.path_calculator = path_calculator
        self.message_handler = message_handler
    
    def find_paths(self, start: int, goal: int, 
                   constraints: Optional[List[ConstraintInterface]] = None,
                   max_paths: Optional[int] = None) -> Dict[str, Any]:
        """
        Find paths using the configured algorithm.
        
        Args:
            start: Start node
            goal: Goal node
            constraints: List of constraints to validate against
            max_paths: Maximum number of paths to find
            
        Returns:
            Dictionary with path results and metadata
        """
        # Validate basic requirements
        if not self.graph.node_exists(start):
            error_msg = f"Start node {start} not found"
            if self.message_handler:
                self.message_handler.handle_error(error_msg)
            return {"success": False, "message": error_msg, "paths": []}
        
        if not self.graph.node_exists(goal):
            error_msg = f"Goal node {goal} not found"
            if self.message_handler:
                self.message_handler.handle_error(error_msg)
            return {"success": False, "message": error_msg, "paths": []}
        
        # Find paths using algorithm
        paths = self.algorithm.find_path(start, goal, self.graph, constraints, max_paths)
        
        if not paths:
            no_path_msg = "No paths found between the specified nodes"
            if self.message_handler:
                self.message_handler.handle_info(no_path_msg)
            return {"success": False, "message": no_path_msg, "paths": []}
        
        # Get visited nodes for visualization (if algorithm supports it)
        visited_nodes = set()
        if hasattr(self.algorithm, 'get_visited_nodes'):
            visited_nodes = self.algorithm.get_visited_nodes()
        
        # Calculate statistics
        stats = self.path_calculator.get_path_statistics(paths, self.graph)
        
        if self.message_handler:
            self.message_handler.handle_success(f"Found {len(paths)} paths using {type(self.algorithm).__name__}")
        
        return {
            "success": True,
            "paths": paths,
            "primary_path": paths[0],
            "all_paths": paths,
            "visited_nodes": visited_nodes,
            "statistics": stats,
            "algorithm": type(self.algorithm).__name__
        }
    
    def find_paths_streaming(self, start: int, goal: int,
                           constraints: Optional[List[ConstraintInterface]] = None,
                           max_paths: Optional[int] = None) -> Iterator[Dict[str, Any]]:
        """
        Find paths using streaming generator.
        
        Yields:
            Path results one at a time
        """
        if not self.graph.node_exists(start) or not self.graph.node_exists(goal):
            return
        
        path_count = 0
        for path in self.algorithm.find_paths_streaming(start, goal, self.graph, constraints, max_paths):
            if max_paths and path_count >= max_paths:
                break
            
            path_cost = self.path_calculator.calculate_path_cost(path, self.graph)
            
            yield {
                "path": path,
                "cost": path_cost,
                "steps": len(path) - 1,
                "algorithm": type(self.algorithm).__name__
            }
            path_count += 1
    
    def get_path_summary(self, path_results: Dict[str, Any]) -> str:
        """
        Get a summary of path results.
        
        Args:
            path_results: Results from find_paths
            
        Returns:
            Formatted summary string
        """
        if not path_results["success"]:
            return "No path found"
        
        stats = path_results["statistics"]
        primary_path = path_results["primary_path"]
        algorithm = path_results["algorithm"]
        
        summary = f"✓ Path found using {algorithm}!\\n"
        summary += f"  Steps: {len(primary_path)-1}\\n"
        summary += f"  Cost: {stats['avg_cost']:.2f}\\n"
        summary += f"  Total paths: {stats['count']}"
        
        if stats["count"] > 1:
            summary += f"\\n  Min cost: {stats['min_cost']:.2f}"
            summary += f"\\n  Max cost: {stats['max_cost']:.2f}"
        
        return summary
    
    def validate_path(self, path: List[int], 
                      constraints: Optional[List[ConstraintInterface]] = None) -> tuple[bool, str]:
        """
        Validate a path against constraints.
        
        Args:
            path: Path to validate
            constraints: List of constraints
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not constraints:
            return True, ""
        
        for constraint in constraints:
            is_valid, error_msg = constraint.validate(path, self.graph)
            if not is_valid:
                return False, error_msg
        
        return True, ""
