"""
Node limit constraint implementation.
Pure generic constraint that can work with any graph.
"""

from typing import List, Dict, Any

from core.graph_interface import GraphInterface, ConstraintInterface


class NodeLimitConstraint(ConstraintInterface):
    """Constraint to limit the number of nodes processed."""
    
    def __init__(self, max_nodes: int):
        """Initialize with maximum allowed nodes."""
        self.max_nodes = max_nodes
        self.nodes_processed = 0
    
    def validate(self, path: List[int], graph: GraphInterface) -> tuple[bool, str]:
        """
        Validate that the path doesn't exceed node limit.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(path) > self.max_nodes:
            return False, f"Path exceeds maximum node limit ({self.max_nodes})"
        return True, ""
    
    def increment_processed(self) -> None:
        """Increment the count of processed nodes."""
        self.nodes_processed += 1
    
    def is_limit_exceeded(self) -> bool:
        """Check if the processing limit has been exceeded."""
        return self.nodes_processed > self.max_nodes
    
    def reset(self) -> None:
        """Reset the processed node counter."""
        self.nodes_processed = 0
