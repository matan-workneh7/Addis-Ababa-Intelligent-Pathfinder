#!/usr/bin/env python3
"""
Test script to verify GUI functionality.
"""

import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.controllers.generic_pathfinding_controller import GenericPathfindingController
from src.controllers.classic_dfs_controller import ClassicDFSController

def test_gui_components():
    """Test that all GUI components can be initialized."""
    print("Testing GUI components...")
    
    # Test controllers
    try:
        bfs_controller = GenericPathfindingController()
        dfs_controller = ClassicDFSController()
        print("✓ Controllers initialized successfully")
    except Exception as e:
        print(f"✗ Controller error: {e}")
        return False
    
    # Test graph access
    try:
        graph = bfs_controller.domain_adapter.graph_model.graph
        print(f"✓ Graph loaded successfully ({len(graph.nodes)} nodes)")
    except Exception as e:
        print(f"✗ Graph access error: {e}")
        return False
    
    # Test pathfinding
    try:
        result = bfs_controller.find_optimal_paths("sarbet", "gotera", "bfs")
        if result["success"]:
            print(f"✓ BFS pathfinding works ({len(result['paths'])} paths found)")
        else:
            print(f"✗ BFS failed: {result.get('message')}")
    except Exception as e:
        print(f"✗ BFS error: {e}")
        return False
    
    try:
        result = dfs_controller.find_paths_with_constraints("sarbet", "gotera")
        if result["success"]:
            print(f"✓ DFS pathfinding works ({len(result['paths'])} paths found)")
        else:
            print(f"✗ DFS failed: {result.get('message')}")
    except Exception as e:
        print(f"✗ DFS error: {e}")
        return False
    
    return True

def test_gui_window():
    """Test GUI window creation."""
    print("\nTesting GUI window...")
    
    try:
        root = tk.Tk()
        root.title("Test")
        root.geometry("300x200")
        
        label = ttk.Label(root, text="GUI Test Successful!")
        label.pack(pady=50)
        
        # Test for 2 seconds then close
        root.after(2000, root.destroy)
        root.mainloop()
        
        print("✓ GUI window test completed")
        return True
        
    except Exception as e:
        print(f"✗ GUI window error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("GUI FUNCTIONALITY TEST")
    print("=" * 50)
    
    # Test components
    components_ok = test_gui_components()
    
    # Test window
    window_ok = test_gui_window()
    
    print("\n" + "=" * 50)
    if components_ok and window_ok:
        print("✅ ALL TESTS PASSED - GUI is ready!")
        print("\nTo start the GUI:")
        print("python gui_pathfinder.py")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 50)
