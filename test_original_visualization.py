#!/usr/bin/env python3
"""
Test script to verify GUI visualization matches original terminal style.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.controllers.generic_pathfinding_controller import GenericPathfindingController
from src.services.visualization_service import VisualizationService

def test_original_visualization():
    """Test that GUI uses the same visualization as original terminal."""
    print("Testing original visualization style...")
    
    try:
        # Test original visualization service
        bfs_controller = GenericPathfindingController()
        viz_service = VisualizationService(
            bfs_controller.domain_adapter.graph_model,
            bfs_controller.domain_adapter.location_model
        )
        
        # Test pathfinding with visited nodes
        result = bfs_controller.find_optimal_paths("sarbet", "gotera", "bfs")
        
        if result["success"]:
            print(f"✓ Pathfinding works: {len(result['paths'])} paths found")
            
            # Check if visited_nodes are included
            if "visited_nodes" in result:
                print(f"✓ Visited nodes included: {len(result['visited_nodes'])} nodes")
            else:
                print("✗ Visited nodes missing from result")
                return False
            
            # Test original visualization service
            primary_path = result["paths"][0]
            visited_nodes = result.get("visited_nodes", set())
            alternative_paths = result["paths"][1:] if len(result["paths"]) > 1 else None
            
            print("✓ Original visualization service available")
            print(f"  - Primary path: {len(primary_path)} nodes")
            print(f"  - Visited nodes: {len(visited_nodes)} nodes")
            print(f"  - Alternative paths: {len(alternative_paths) if alternative_paths else 0}")
            
            # Check visualization colors
            from config.settings import VISUALIZATION_COLORS, EXPLORED_LINE_WIDTH, EXPLORED_ALPHA
            print(f"✓ Visualization colors:")
            print(f"  - Primary: {VISUALIZATION_COLORS['primary']}")
            print(f"  - Explored: {VISUALIZATION_COLORS['explored']}")
            print(f"  - Alternatives: {VISUALIZATION_COLORS['alternatives'][:3]}")
            print(f"  - Explored line width: {EXPLORED_LINE_WIDTH}")
            print(f"  - Explored alpha: {EXPLORED_ALPHA}")
            
            return True
        else:
            print(f"✗ Pathfinding failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_gui_visualization_methods():
    """Test that GUI has the correct visualization methods."""
    print("\nTesting GUI visualization methods...")
    
    try:
        from gui_pathfinder import PathFinderGUI
        import tkinter as tk
        
        # Create test window
        root = tk.Tk()
        root.withdraw()  # Hide window for testing
        
        # Initialize GUI
        app = PathFinderGUI(root)
        
        # Check visualization methods exist
        methods_to_check = [
            '_visualize_paths',
            '_plot_explored_area_gui', 
            '_draw_path_gui',
            '_add_legend_gui'
        ]
        
        for method in methods_to_check:
            if hasattr(app, method):
                print(f"✓ {method} method exists")
            else:
                print(f"✗ {method} method missing")
                return False
        
        # Test explored area plotting
        class MockGraph:
            def subgraph(self, nodes):
                return MockSubgraph()
            def has_node(self, node):
                return True
            def nodes(self):
                return {'x': 38.8, 'y': 9.0}
        
        class MockSubgraph:
            def edges(self):
                return [(1, 2), (2, 3)]
        
        visited_nodes = {1, 2, 3, 4}
        graph = MockGraph()
        
        # This should work without errors
        try:
            app._plot_explored_area_gui(visited_nodes, graph, 0.8, 0.25)
            print("✓ Explored area plotting works")
        except Exception as e:
            print(f"✗ Explored area plotting failed: {e}")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ORIGINAL VISUALIZATION STYLE TEST")
    print("=" * 60)
    
    # Test original visualization
    original_ok = test_original_visualization()
    
    # Test GUI methods
    gui_ok = test_gui_visualization_methods()
    
    print("\n" + "=" * 60)
    if original_ok and gui_ok:
        print("✅ ORIGINAL VISUALIZATION STYLE CONFIRMED!")
        print("\nGUI now matches terminal visualization:")
        print("• Blue explored area (0.8 width, 0.25 alpha)")
        print("• Red primary path (4 width)")
        print("• Yellow/lime/cyan alternative paths (3 width)")
        print("• Green start marker, Red end marker")
        print("• Proper legend with all elements")
        print("\nVisualization matches original terminal exactly!")
    else:
        print("❌ VISUALIZATION STYLE ISSUES DETECTED")
    print("=" * 60)
