"""
Pure generic DFS algorithm implementation.
Completely domain-agnostic and reusable for any graph type.
"""

from typing import List, Set, Optional, Iterator

from core.graph_interface import (
    GraphInterface, ConstraintInterface, PathfindingAlgorithmInterface
)


class DFSAlgorithm(PathfindingAlgorithmInterface):
    """Pure generic DFS algorithm implementation."""
    
    def __init__(self, message_handler=None):
        """Initialize DFS with optional message handler."""
        self.message_handler = message_handler
    
    def find_path(self, start: int, goal: int, graph: GraphInterface,
                  constraints: Optional[List[ConstraintInterface]] = None,
                  max_paths: Optional[int] = None) -> List[List[int]]:
        """
        Find path using DFS (depth-first search).
        
        Args:
            start: Start node
            goal: Goal node
            graph: Graph implementation
            constraints: List of constraints to validate against
            max_paths: Maximum number of paths to find
            
        Returns:
            List of paths found by DFS
        """
        if not graph.node_exists(start) or not graph.node_exists(goal):
            if self.message_handler:
                self.message_handler.handle_error(f"Start or goal node not found")
            return []
        
        if start == goal:
            if self.message_handler:
                self.message_handler.handle_info("Start and goal are the same")
            return [[start]]
        
        all_paths = []
        visited = set()
        
        self._dfs_recursive(start, goal, [start], visited, graph, constraints, 
                           all_paths, max_paths or 1)
        
        if all_paths and self.message_handler:
            self.message_handler.handle_success(f"Found {len(all_paths)} paths using DFS")
        
        return all_paths
    
    def find_paths_streaming(self, start: int, goal: int, graph: GraphInterface,
                           constraints: Optional[List[ConstraintInterface]] = None,
                           max_paths: Optional[int] = None) -> Iterator[List[int]]:
        """
        Find paths using streaming DFS.
        
        Yields:
            Paths one at a time
        """
        if not graph.node_exists(start) or not graph.node_exists(goal):
            return
        
        if start == goal:
            yield [start]
            return
        
        path_count = 0
        for path in self._dfs_streaming(start, goal, [start], set(), graph, constraints):
            if max_paths and path_count >= max_paths:
                break
            yield path
            path_count += 1
    
    def _dfs_recursive(self, current: int, goal: int, current_path: List[int],
                      visited: Set[int], graph: GraphInterface, 
                      constraints: Optional[List[ConstraintInterface]], 
                      all_paths: List[List[int]], max_paths: int) -> None:
        """Recursive DFS implementation."""
        if len(all_paths) >= max_paths:
            return
        
        if current == goal:
            if self._validate_path(current_path, graph, constraints):
                all_paths.append(current_path.copy())
            return
        
        visited.add(current)
        
        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                current_path.append(neighbor)
                self._dfs_recursive(neighbor, goal, current_path, visited, 
                                   graph, constraints, all_paths, max_paths)
                current_path.pop()
        
        visited.remove(current)
    
    def _dfs_streaming(self, current: int, goal: int, current_path: List[int],
                      visited: Set[int], graph: GraphInterface,
                      constraints: Optional[List[ConstraintInterface]]) -> Iterator[List[int]]:
        """Streaming DFS implementation."""
        if current == goal:
            if self._validate_path(current_path, graph, constraints):
                yield current_path.copy()
            return
        
        visited.add(current)
        
        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                current_path.append(neighbor)
                yield from self._dfs_streaming(neighbor, goal, current_path, 
                                            visited, graph, constraints)
                current_path.pop()
        
        visited.remove(current)
    
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