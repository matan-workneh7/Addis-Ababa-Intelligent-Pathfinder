"""
Pure generic A* algorithm implementation.
Completely domain-agnostic and reusable for any graph type.
"""

import heapq
from typing import List, Set, Optional, Iterator, Callable, Dict, Any

from core.graph_interface import (
    GraphInterface, ConstraintInterface, PathfindingAlgorithmInterface
)


class AStarAlgorithm(PathfindingAlgorithmInterface):
    """Pure generic A* algorithm implementation."""
    
    def __init__(self, heuristic: Callable[[int, int, GraphInterface], float], 
                 message_handler=None):
        """
        Initialize A* with heuristic function.
        
        Args:
            heuristic: Function to estimate distance from node to goal
            message_handler: Optional message handler
        """
        self.heuristic = heuristic
        self.message_handler = message_handler
    
    def find_path(self, start: int, goal: int, graph: GraphInterface,
                  constraints: Optional[List[ConstraintInterface]] = None,
                  max_paths: Optional[int] = None) -> List[List[int]]:
        """
        Find optimal path using A* algorithm.
        
        Args:
            start: Start node
            goal: Goal node
            graph: Graph implementation
            constraints: List of constraints to validate against
            max_paths: Maximum number of paths to find
            
        Returns:
            List of optimal paths
        """
        if not graph.node_exists(start) or not graph.node_exists(goal):
            if self.message_handler:
                self.message_handler.handle_error(f"Start or goal node not found")
            return []
        
        if start == goal:
            if self.message_handler:
                self.message_handler.handle_info("Start and goal are the same")
            return [[start]]
        
        # A* search
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal, graph)}
        closed_set = set()
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                path = self._reconstruct_path(came_from, current)
                
                # Validate path
                if self._validate_path(path, graph, constraints):
                    if self.message_handler:
                        self.message_handler.handle_success(f"Found optimal path with cost {g_score[goal]}")
                    return [path]
                else:
                    return []
            
            closed_set.add(current)
            
            for neighbor in graph.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score[current] + self._get_edge_cost(current, neighbor, graph)
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal, graph)
                    
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        if self.message_handler:
            self.message_handler.handle_info("No path found using A*")
        return []
    
    def find_paths_streaming(self, start: int, goal: int, graph: GraphInterface,
                           constraints: Optional[List[ConstraintInterface]] = None,
                           max_paths: Optional[int] = None) -> Iterator[List[int]]:
        """
        Find paths using streaming A*.
        
        For A*, this yields paths as they're found during the search.
        """
        path = self.find_path(start, goal, graph, constraints, 1)
        if path:
            yield path[0]
    
    def _reconstruct_path(self, came_from: Dict[int, Optional[int]], current: int) -> List[int]:
        """Reconstruct path from came_from dictionary."""
        path = [current]
        while current is not None:
            current = came_from[current]
            if current is not None:
                path.append(current)
        return list(reversed(path))
    
    def _get_edge_cost(self, u: int, v: int, graph: GraphInterface) -> float:
        """Get cost of edge between two nodes."""
        edge_data = graph.get_edge_data(u, v)
        if edge_data and 'length' in edge_data:
            return edge_data['length']
        return 1.0  # Default cost
    
    def _validate_path(self, path: List[int], graph: GraphInterface, 
                      constraints: Optional[List[ConstraintInterface]]) -> bool:
        """Validate path against all constraints."""
        if not constraints:
            return True
        
        for constraint in constraints:
            is_valid, _ = constraint.validate(path, graph)
            if not is_valid:
                return False
        
        return True