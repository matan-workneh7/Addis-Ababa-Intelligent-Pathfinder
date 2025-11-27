"""
Path Finder - Clean Architecture Package.

This package provides a clean, well-structured implementation of path finding
algorithms following SOLID principles and clean architecture patterns.
"""

# Core Interfaces
from .core.graph_interface import (
    GraphInterface, ConstraintInterface, PathCalculatorInterface,
    MessageHandlerInterface, PathfindingAlgorithmInterface
)

# Core Models
from .core.graph_model import GraphModel
from .core.location_model import LocationModel

# Algorithms
from .algorithms.bfs import BFSAlgorithm
from .algorithms.dfs import DFSAlgorithm
from .algorithms.astar import AStarAlgorithm
from .algorithms.dfs_classic import ClassicDFSAlgorithm

# Shared Components
from .shared.constraints.node_limit_constraint import NodeLimitConstraint
from .shared.constraints.distance_constraint import DistanceConstraint
from .shared.constraints.same_location_constraint import SameLocationConstraint
from .shared.calculators.generic_path_calculator import GenericPathCalculator
from .shared.utils.constraint_validator import ConstraintValidator

# Services
from .services.generic_pathfinding_service import GenericPathfindingService
from .services.visualization_service import VisualizationService

# Controllers
from .controllers.generic_pathfinding_controller import GenericPathfindingController
from .controllers.classic_dfs_controller import ClassicDFSController

# Core Adapters
from .core.networkx_graph_adapter import NetworkXGraphAdapter
from .core.addis_ababa_adapter import AddisAbabaAdapter

__version__ = "3.0.0"
__author__ = "Path Finder Team"

__all__ = [
    # Core Interfaces
    "GraphInterface", "ConstraintInterface", "PathCalculatorInterface",
    "MessageHandlerInterface", "PathfindingAlgorithmInterface",
    
    # Core Models
    "GraphModel", "LocationModel",
    
    # Algorithms
    "BFSAlgorithm", "DFSAlgorithm", "AStarAlgorithm", "ClassicDFSAlgorithm",
    
    # Shared Components
    "NodeLimitConstraint", "DistanceConstraint", "SameLocationConstraint",
    "GenericPathCalculator", "ConstraintValidator",
    
    # Services
    "GenericPathfindingService", "VisualizationService",
    
    # Controllers
    "GenericPathfindingController", "ClassicDFSController",
    
    # Core Adapters
    "NetworkXGraphAdapter", "AddisAbabaAdapter",
]
