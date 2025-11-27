"""
Distance constraint implementation.
Pure generic constraint that can work with any graph and path calculator.
"""

from typing import List, Dict, Any

from core.graph_interface import GraphInterface, ConstraintInterface, PathCalculatorInterface


class DistanceConstraint(ConstraintInterface):
    """Constraint to limit path distance."""
    
    def __init__(self, max_distance: float, path_calculator: PathCalculatorInterface):
        """
        Initialize with maximum allowed distance.
        
        Args:
            max_distance: Maximum allowed path distance
            path_calculator: Calculator to compute path distance
        """
        self.max_distance = max_distance
        self.path_calculator = path_calculator
    
    def validate(self, path: List[int], graph: GraphInterface) -> tuple[bool, str]:
        """
        Validate that the path doesn't exceed distance limit.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        distance = self.path_calculator.calculate_path_cost(path, graph)
        if distance > self.max_distance:
            return False, f"Path distance ({distance:.0f}) exceeds maximum ({self.max_distance:.0f})"
        return True, ""
