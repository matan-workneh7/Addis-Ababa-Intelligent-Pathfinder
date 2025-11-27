"""
Abstract interfaces for generic graph operations.
Pure generic interfaces that can work with any graph implementation.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set
from collections.abc import Iterator


class GraphInterface(ABC):
    """Abstract interface for graph operations."""
    
    @abstractmethod
    def get_neighbors(self, node: int) -> List[int]:
        """Get neighbors of a node."""
        pass
    
    @abstractmethod
    def node_exists(self, node: int) -> bool:
        """Check if a node exists."""
        pass
    
    @abstractmethod
    def edge_exists(self, u: int, v: int) -> bool:
        """Check if an edge exists."""
        pass
    
    @abstractmethod
    def get_node_data(self, node: int) -> Dict[str, Any]:
        """Get data for a node."""
        pass
    
    @abstractmethod
    def get_edge_data(self, u: int, v: int) -> Optional[Dict[str, Any]]:
        """Get edge data."""
        pass
    
    @abstractmethod
    def get_subgraph(self, nodes: List[int]) -> 'GraphInterface':
        """Get subgraph with specified nodes."""
        pass


class ConstraintInterface(ABC):
    """Abstract interface for path constraints."""
    
    @abstractmethod
    def validate(self, path: List[int], graph: GraphInterface) -> tuple[bool, str]:
        """
        Validate a path against this constraint.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass


class PathCalculatorInterface(ABC):
    """Abstract interface for path calculations."""
    
    @abstractmethod
    def calculate_path_cost(self, path: List[int], graph: GraphInterface) -> float:
        """Calculate the cost of a path."""
        pass
    
    @abstractmethod
    def paths_are_similar(self, path1: List[int], path2: List[int], threshold: float = 0.8) -> bool:
        """Check if two paths are essentially the same."""
        pass
    
    @abstractmethod
    def get_path_statistics(self, paths: List[List[int]], graph: GraphInterface) -> Dict[str, Any]:
        """Get statistics for a collection of paths."""
        pass


class MessageHandlerInterface(ABC):
    """Abstract interface for handling messages and output."""
    
    @abstractmethod
    def handle_error(self, message: str) -> None:
        """Handle error messages."""
        pass
    
    @abstractmethod
    def handle_info(self, message: str) -> None:
        """Handle informational messages."""
        pass
    
    @abstractmethod
    def handle_success(self, message: str) -> None:
        """Handle success messages."""
        pass


class PathfindingAlgorithmInterface(ABC):
    """Abstract interface for pathfinding algorithms."""
    
    @abstractmethod
    def find_path(self, start: int, goal: int, graph: GraphInterface, 
                  constraints: Optional[List[ConstraintInterface]] = None,
                  max_paths: Optional[int] = None) -> List[List[int]]:
        """Find paths using this algorithm."""
        pass
    
    @abstractmethod
    def find_paths_streaming(self, start: int, goal: int, graph: GraphInterface,
                           constraints: Optional[List[ConstraintInterface]] = None,
                           max_paths: Optional[int] = None) -> Iterator[List[int]]:
        """Find paths using streaming generator."""
        pass
