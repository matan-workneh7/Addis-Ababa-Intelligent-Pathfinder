"""
A* algorithm implementation with constraint support and visualization tracking.
Based on the provided JavaScript implementation, adapted for Python architecture.
"""

import heapq
import math
from typing import List, Set, Optional, Iterator, Dict, Any

from core.graph_interface import (
    GraphInterface, ConstraintInterface, PathfindingAlgorithmInterface
)


class AStarAlgorithm(PathfindingAlgorithmInterface):
    """A* algorithm implementation with heuristic search and constraint support."""
    
    def __init__(self, message_handler=None, max_paths: int = 5):
        """
        Initialize A* with optional parameters.
        
        Args:
            message_handler: Optional message handler
            max_paths: Maximum number of paths to find
        """
        self.message_handler = message_handler
        self.max_paths = max_paths
        self._last_visited_nodes = set()
        self._all_found_paths = []
        self._open_list = []
        self._closed_list = set()
        
    def get_visited_nodes(self) -> set:
        """Get the set of visited nodes from the last search."""
        return self._last_visited_nodes
    
    def get_all_found_paths(self) -> List[List[int]]:
        """Get all paths found during the search."""
        return self._all_found_paths
    
    def find_path(self, start: int, goal: int, graph: GraphInterface,
                  constraints: Optional[List[ConstraintInterface]] = None,
                  max_paths: Optional[int] = None) -> List[List[int]]:
        """
        Find paths using A* algorithm.
        
        Args:
            start: Start node
            goal: Goal node
            graph: Graph implementation
            constraints: List of constraints to validate against
            max_paths: Maximum number of paths to find
            
        Returns:
            List of optimal paths found by A*
        """
        if not graph.node_exists(start) or not graph.node_exists(goal):
            if self.message_handler:
                self.message_handler.handle_error(f"Start or goal node not found")
            return []
        
        if start == goal:
            if self.message_handler:
                self.message_handler.handle_info("Start and goal are the same")
            return [[start]]
        
        # Reset tracking
        self._last_visited_nodes = set()
        self._all_found_paths = []
        self._open_list = []
        self._closed_list = set()
        
        # Find paths using A*
        all_paths = []
        
        # Primary A* search
        primary_path = self._astar_search(graph, start, goal, constraints)
        
        if primary_path and self._validate_path(primary_path, graph, constraints):
            all_paths.append(primary_path)
            self._all_found_paths.append(primary_path)
            
            # Track visited nodes
            self._last_visited_nodes.update(primary_path)
            
            # Find alternative paths by exploring different heuristics
            max_alternatives = (max_paths or self.max_paths) - 1
            if max_alternatives > 0:
                alternative_paths = self._find_alternative_paths(
                    graph, start, goal, primary_path, constraints, max_alternatives
                )
                all_paths.extend(alternative_paths)
                self._all_found_paths.extend(alternative_paths)
        
        if all_paths and self.message_handler:
            self.message_handler.handle_success(f"Found {len(all_paths)} paths using A*")
        
        return all_paths
    
    def find_paths_streaming(self, start: int, goal: int, graph: GraphInterface,
                           constraints: Optional[List[ConstraintInterface]] = None,
                           max_paths: Optional[int] = None) -> Iterator[List[int]]:
        """
        Find paths using streaming A*.
        
        Yields:
            Path results one at a time
        """
        paths = self.find_path(start, goal, graph, constraints, max_paths)
        for path in paths:
            yield path
    
    def _astar_search(self, graph: GraphInterface, start: int, goal: int,
                      constraints: Optional[List[ConstraintInterface]]) -> Optional[List[int]]:
        """
        Perform A* search using Manhattan distance heuristic.
        
        Args:
            graph: Graph implementation
            start: Start node
            goal: Goal node
            constraints: List of constraints
            
        Returns:
            Optimal path if found, None otherwise
        """
        # Priority queue: (f_score, g_score, node_id, path)
        open_list = [(0, 0, start, [start])]
        closed_set = set()
        g_scores = {start: 0}
        f_scores = {start: self._heuristic(graph, start, goal)}
        
        while open_list:
            # Get node with lowest f_score
            current_f, current_g, current, path = heapq.heappop(open_list)
            
            # Track visited nodes for visualization
            self._last_visited_nodes.add(current)
            
            # Check if we found the goal
            if current == goal:
                return path
            
            # Skip if already processed
            if current in closed_set:
                continue
            
            closed_set.add(current)
            
            # Explore neighbors
            for neighbor in graph.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                # Calculate tentative g_score
                edge_data = graph.get_edge_data(current, neighbor)
                edge_weight = edge_data.get('length', 1.0) if edge_data else 1.0
                tentative_g = current_g + edge_weight
                
                # Check if this path to neighbor is better
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    f_scores[neighbor] = tentative_g + self._heuristic(graph, neighbor, goal)
                    new_path = path + [neighbor]
                    
                    heapq.heappush(open_list, (f_scores[neighbor], tentative_g, neighbor, new_path))
                    
                    # Track neighbor as explored
                    self._last_visited_nodes.add(neighbor)
        
        return None
    
    def _heuristic(self, graph: GraphInterface, node1: int, node2: int) -> float:
        """
        Calculate heuristic distance between two nodes.
        Uses Euclidean distance for geographic coordinates.
        
        Args:
            graph: Graph implementation
            node1: First node
            node2: Second node
            
        Returns:
            Heuristic distance
        """
        try:
            # Get node coordinates
            node1_data = graph.get_node_data(node1)
            node2_data = graph.get_node_data(node2)
            
            # Calculate Euclidean distance
            lat1, lon1 = node1_data['y'], node1_data['x']
            lat2, lon2 = node2_data['y'], node2_data['x']
            
            return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
        except:
            # Fallback to unit distance
            return 1.0
    
    def _find_alternative_paths(self, graph: GraphInterface, start: int, goal: int,
                               primary_path: List[int], constraints: Optional[List[ConstraintInterface]],
                               max_alternatives: int) -> List[List[int]]:
        """
        Find alternative paths using different heuristic strategies.
        
        Args:
            graph: Graph implementation
            start: Start node
            goal: Goal node
            primary_path: Primary path found
            constraints: List of constraints
            max_alternatives: Maximum number of alternatives to find
            
        Returns:
            List of alternative paths
        """
        alternatives = []
        
        # For A*, use different heuristic weights for alternatives
        heuristic_weights = [0.5, 1.5, 2.0, 0.8]  # Different heuristic multipliers
        
        for i in range(min(max_alternatives, len(heuristic_weights))):
            weight = heuristic_weights[i]
            alt_path = self._astar_with_weighted_heuristic(
                graph, start, goal, constraints, weight
            )
            
            if alt_path and self._validate_path(alt_path, graph, constraints):
                # Check if it's different enough from existing paths
                is_different = True
                for existing_path in [primary_path] + alternatives:
                    if self._paths_too_similar(alt_path, existing_path, threshold=0.4):  # Lower threshold
                        is_different = False
                        break
                
                if is_different:
                    alternatives.append(alt_path)
                    self._last_visited_nodes.update(alt_path)
        
        return alternatives
    
    def _astar_with_weighted_heuristic(self, graph: GraphInterface, start: int, goal: int,
                                     constraints: Optional[List[ConstraintInterface]], 
                                     heuristic_weight: float) -> Optional[List[int]]:
        """
        A* search with weighted heuristic for finding alternatives.
        
        Args:
            graph: Graph implementation
            start: Start node
            goal: Goal node
            constraints: List of constraints
            heuristic_weight: Weight multiplier for heuristic
            
        Returns:
            Alternative path if found, None otherwise
        """
        # Priority queue: (f_score, g_score, node_id, path)
        open_list = [(0, 0, start, [start])]
        closed_set = set()
        g_scores = {start: 0}
        f_scores = {start: heuristic_weight * self._heuristic(graph, start, goal)}
        
        while open_list:
            # Get node with lowest f_score
            current_f, current_g, current, path = heapq.heappop(open_list)
            
            # Track visited nodes
            self._last_visited_nodes.add(current)
            
            # Check if we found the goal
            if current == goal:
                return path
            
            # Skip if already processed
            if current in closed_set:
                continue
            
            closed_set.add(current)
            
            # Explore neighbors
            for neighbor in graph.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                # Calculate tentative g_score
                edge_data = graph.get_edge_data(current, neighbor)
                edge_weight = edge_data.get('length', 1.0) if edge_data else 1.0
                tentative_g = current_g + edge_weight
                
                # Check if this path to neighbor is better
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    f_scores[neighbor] = tentative_g + heuristic_weight * self._heuristic(graph, neighbor, goal)
                    new_path = path + [neighbor]
                    
                    heapq.heappush(open_list, (f_scores[neighbor], tentative_g, neighbor, new_path))
                    
                    # Track neighbor as explored
                    self._last_visited_nodes.add(neighbor)
        
        return None
    
    def _paths_too_similar(self, path1: List[int], path2: List[int], threshold: float = 0.8) -> bool:
        """
        Check if two paths are too similar.
        
        Args:
            path1: First path
            path2: Second path
            threshold: Similarity threshold
            
        Returns:
            True if paths are too similar
        """
        set1, set2 = set(path1), set(path2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        similarity = intersection / union if union > 0 else 0
        return similarity > threshold
    
    def _validate_path(self, path: List[int], graph: GraphInterface,
                      constraints: Optional[List[ConstraintInterface]]) -> bool:
        """
        Validate path against all constraints.
        
        Args:
            path: Path to validate
            graph: Graph implementation
            constraints: List of constraints
            
        Returns:
            True if path is valid, False otherwise
        """
        if not constraints:
            return True
        
        for constraint in constraints:
            if not constraint.validate(path, graph):
                return False
        
        return True
