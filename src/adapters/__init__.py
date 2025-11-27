"""
Adapters for connecting generic components to specific implementations.
"""

from .networkx_graph_adapter import NetworkXGraphAdapter
from .addis_ababa_adapter import AddisAbabaAdapter

__all__ = ["NetworkXGraphAdapter", "AddisAbabaAdapter"]
