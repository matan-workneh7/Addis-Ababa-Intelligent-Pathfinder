"""
Pure generic BFS algorithm implementation.
Completely domain-agnostic and reusable for any graph type.
"""

from collections import deque
from typing import List, Set, Optional, Iterator
from abc import ABC

from core.graph_interface import (
    GraphInterface, ConstraintInterface, PathfindingAlgorithmInterface
)


class BFSAlgorithm(PathfindingAlgorithmInterface):
    """Pure generic BFS algorithm implementation."""
    
    def __init__(self, message_handler=None):
        """Initialize BFS with optional message handler."""
        self.message_handler = message_handler
        self._last_visited_nodes = set()
    
    def get_visited_nodes(self) -> set:
        """Get the set of visited nodes from the last search."""
        return self._last_visited_nodes
    
    def find_path(self, start: int, goal: int, graph: GraphInterface,
                  constraints: Optional[List[ConstraintInterface]] = None,
                  max_paths: Optional[int] = None) -> List[List[int]]:
        """
        Find shortest path using BFS.
        
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
        
        # Build parent tree for path reconstruction
        distance, parents, visited = self._build_parent_tree(start, goal, graph)
        
        if goal not in distance:
            if self.message_handler:
                self.message_handler.handle_info("No path found between nodes")
            return []
        
        # Find all optimal paths
        all_paths = []
        self._backtrack_paths(goal, [goal], all_paths, start, max_paths or 1, parents)
        
        # Validate paths against constraints
        valid_paths = []
        for path in all_paths:
            if self._validate_path(path, graph, constraints):
                valid_paths.append(path)
        
        # Store visited nodes for visualization access
        self._last_visited_nodes = visited
        
        if len(valid_paths) > 1 and self.message_handler:
            self.message_handler.handle_success(f"Found {len(valid_paths)} optimal paths")
        
        return valid_paths
    
    def find_paths_streaming(self, start: int, goal: int, graph: GraphInterface,
                           constraints: Optional[List[ConstraintInterface]] = None,
                           max_paths: Optional[int] = None) -> Iterator[List[int]]:
        """
        Find paths using streaming generator.
        
        Yields:
            Paths one at a time
        """
        if not graph.node_exists(start) or not graph.node_exists(goal):
            return
        
        if start == goal:
            yield [start]
            return
        
        # Build parent tree
        distance, parents = self._build_parent_tree(start, goal, graph)
        
        if goal not in distance:
            return
        
        # Stream backtrack with validation
        path_count = 0
        for path in self._stream_backtrack(goal, [goal], start, parents):
            if max_paths and path_count >= max_paths:
                break
            if self._validate_path(path, graph, constraints):
                yield path
                path_count += 1
    
    def _build_parent_tree(self, start: int, goal: int, graph: GraphInterface) -> tuple[dict, dict, set]:
        """Build parent tree for path reconstruction."""
        queue = deque([start])
        visited = {start}
        distance = {start: 0}
        parents = {start: []}
        
        while queue:
            current = queue.popleft()
            
            if current == goal:
                break
            
            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    distance[neighbor] = distance[current] + 1
                    parents[neighbor] = [current]
                    queue.append(neighbor)
                elif distance[neighbor] == distance[current] + 1:
                    parents[neighbor].append(current)
        
        return distance, parents, visited
    
    def _backtrack_paths(self, node: int, current_path: List[int], all_paths: List[List[int]], 
                        start_node: int, max_paths: int, parents: dict) -> None:
        """Recursive backtrack to find all paths."""
        if len(all_paths) >= max_paths:
            return
        
        if node == start_node:
            all_paths.append(current_path[::-1])  # Reverse to get start->goal
            return
        
        if node in parents:
            for parent in parents[node]:
                if len(all_paths) >= max_paths:
                    break
                self._backtrack_paths(parent, current_path + [parent], all_paths, start_node, max_paths, parents)
    
    def _stream_backtrack(self, node: int, current_path: List[int], 
                         start_node: int, parents: dict) -> Iterator[List[int]]:
        """Streaming backtrack using generator."""
        if node == start_node:
            yield current_path[::-1]
            return
        
        if node in parents:
            for parent in parents[node]:
                yield from self._stream_backtrack(parent, current_path + [parent], start_node, parents)
    
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
