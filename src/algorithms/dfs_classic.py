"""
Classic DFS algorithm implementation based on stack-based traversal.
Based on the user's provided DFS example, integrated with generic architecture.
Works reliably for weighted graphs with constraint support.
"""

from typing import List, Set, Optional, Iterator, Dict, Any

from core.graph_interface import (
    GraphInterface, ConstraintInterface, PathfindingAlgorithmInterface
)


class ClassicDFSAlgorithm(PathfindingAlgorithmInterface):
    """Classic DFS algorithm using stack-based traversal (user's implementation)."""
    
    def __init__(self, message_handler=None, max_paths: int = 5):
        """
        Initialize Classic DFS with optional parameters.
        
        Args:
            message_handler: Optional message handler
            max_paths: Maximum number of paths to find
        """
        self.message_handler = message_handler
        self.max_paths = max_paths
        self._last_visited_nodes = set()
        self._all_found_paths = []
    
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
        Find paths using classic DFS (stack-based).
        Based on the user's provided implementation.
        
        Args:
            start: Start node
            goal: Goal node
            graph: Graph implementation
            constraints: List of constraints to validate against
            max_paths: Maximum number of paths to find
            
        Returns:
            List of paths found by classic DFS
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
        
        # Find paths using classic DFS
        all_paths = []
        
        # Classic DFS implementation based on user's example
        path = self._dfs_search(graph, start, goal)
        
        if path and self._validate_path(path, graph, constraints):
            all_paths.append(path)
            self._all_found_paths.append(path)
            
            # Track visited nodes for visualization
            self._last_visited_nodes.update(path)
            
            # Find alternative paths by exploring different routes
            if max_paths and max_paths > 1:
                alternative_paths = self._find_alternative_paths(
                    graph, start, goal, path, constraints, max_paths - 1
                )
                all_paths.extend(alternative_paths)
                self._all_found_paths.extend(alternative_paths)
        
        if all_paths and self.message_handler:
            self.message_handler.handle_success(f"Found {len(all_paths)} paths using Classic DFS")
        
        return all_paths
    
    def find_paths_streaming(self, start: int, goal: int, graph: GraphInterface,
                           constraints: Optional[List[ConstraintInterface]] = None,
                           max_paths: Optional[int] = None) -> Iterator[List[int]]:
        """
        Find paths using streaming classic DFS.
        
        Yields:
            Paths one at a time as they're discovered
        """
        if not graph.node_exists(start) or not graph.node_exists(goal):
            return
        
        if start == goal:
            yield [start]
            return
        
        # Reset tracking
        self._last_visited_nodes = set()
        
        # Find primary path
        primary_path = self._dfs_search(graph, start, goal)
        if primary_path and self._validate_path(primary_path, graph, constraints):
            yield primary_path
            self._last_visited_nodes.update(primary_path)
        
        # Find alternative paths
        if max_paths and max_paths > 1:
            alternatives = self._find_alternative_paths(
                graph, start, goal, primary_path, constraints, max_paths - 1
            )
            for alt_path in alternatives:
                yield alt_path
    
    def _dfs_search(self, graph: GraphInterface, start: int, goal: int) -> Optional[List[int]]:
        """
        Classic DFS search based on user's implementation.
        Uses stack for traversal and tracks visited nodes and path reconstruction.
        
        Args:
            graph: Graph implementation
            start: Start node
            goal: Goal node
            
        Returns:
            Path from start to goal, or None if not found
        """
        # Initialize stack with start node
        stack = [start]
        visited = set()
        came_from = {}
        visited.add(start)
        came_from[start] = None
        
        # Track ALL explored nodes for visualization
        self._last_visited_nodes.add(start)
        
        while stack:
            current = stack.pop()
            
            # Track current node as explored (even if not in final path)
            self._last_visited_nodes.add(current)
            
            if current == goal:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            # Get neighbors (similar to graph[current] in user's example)
            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append(neighbor)
                    
                    # Track neighbor as explored when added to stack
                    self._last_visited_nodes.add(neighbor)
        
        return None
    
    def _find_alternative_paths(self, graph: GraphInterface, start: int, goal: int, 
                               primary_path: List[int], constraints: Optional[List[ConstraintInterface]],
                               max_alternatives: int) -> List[List[int]]:
        """
        Find alternative paths by avoiding some nodes of the primary path.
        For urban graphs, we avoid fewer nodes to allow reasonable alternatives.
        
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
        
        # For urban graphs, avoid fewer nodes to allow alternatives
        # Only avoid every 10th node to create some diversity
        avoided_nodes = set()
        if len(primary_path) > 20:
            # Avoid every 10th node to create some diversity but keep routes reasonable
            avoided_nodes = set(primary_path[5::10])  # Start from 5th node, take every 10th
        else:
            # For shorter paths, avoid fewer intermediate nodes
            avoided_nodes = set(primary_path[1:-1:max(1, len(primary_path)//4)])
        
        for attempt in range(max_alternatives):
            # Modified DFS that avoids certain nodes
            alt_path = self._dfs_with_avoidance(graph, start, goal, avoided_nodes, attempt)
            
            if alt_path and self._validate_path(alt_path, graph, constraints):
                # Check if it's different enough from existing paths
                is_different = True
                for existing_path in [primary_path] + alternatives:
                    if self._paths_too_similar(alt_path, existing_path, threshold=0.5):  # Lower threshold for urban
                        is_different = False
                        break
                
                if is_different:
                    alternatives.append(alt_path)
                    self._last_visited_nodes.update(alt_path)
        
        return alternatives
    
    def _dfs_with_avoidance(self, graph: GraphInterface, start: int, goal: int,
                            avoided_nodes: Set[int], attempt: int) -> Optional[List[int]]:
        """
        DFS search that avoids certain nodes to find alternative routes.
        
        Args:
            graph: Graph implementation
            start: Start node
            goal: Goal node
            avoided_nodes: Nodes to avoid
            attempt: Attempt number for different strategies
            
        Returns:
            Alternative path, or None if not found
        """
        stack = [start]
        visited = set()
        came_from = {}
        visited.add(start)
        came_from[start] = None
        
        # Different strategies for different attempts
        neighbor_order_strategy = attempt % 3
        
        while stack:
            current = stack.pop()
            
            if current == goal:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            # Get neighbors with different ordering strategies
            neighbors = list(graph.get_neighbors(current))
            
            # Apply neighbor ordering strategy
            if neighbor_order_strategy == 0:
                # Normal order
                pass
            elif neighbor_order_strategy == 1:
                # Reverse order
                neighbors.reverse()
            elif neighbor_order_strategy == 2:
                # Sort by node ID
                neighbors.sort()
            
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in avoided_nodes:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append(neighbor)
        
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
            is_valid, _ = constraint.validate(path, graph)
            if not is_valid:
                return False
        
        return True
