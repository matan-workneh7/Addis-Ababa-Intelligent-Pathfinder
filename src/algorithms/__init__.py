"""
Path finding algorithms.

This module contains various path finding algorithms, each implementing
the PathfindingAlgorithmInterface for consistency.
"""

from .bfs import BFSAlgorithm
from .dfs_classic import ClassicDFSAlgorithm
from .astar_improved import AStarAlgorithm as AStarImprovedAlgorithm

__all__ = [
    "BFSAlgorithm", 
    "ClassicDFSAlgorithm",
    "AStarImprovedAlgorithm"
]