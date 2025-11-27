"""
Same location constraint implementation.
Pure generic constraint that can work with any graph.
"""

from typing import List, Dict, Any

from core.graph_interface import GraphInterface, ConstraintInterface


class SameLocationConstraint(ConstraintInterface):
    """Constraint to handle same start and goal locations."""
    
    def validate(self, path: List[int], graph: GraphInterface) -> tuple[bool, str]:
        """
        Validate that start and goal are not the same.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(path) == 1:
            return False, "Start and goal are the same location"
        return True, ""
