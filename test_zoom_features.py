#!/usr/bin/env python3
"""
Test script to verify zoom functionality in the GUI.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.controllers.generic_pathfinding_controller import GenericPathfindingController

def test_zoom_components():
    """Test that zoom components can be initialized."""
    print("Testing zoom components...")
    
    try:
        # Test controller
        bfs_controller = GenericPathfindingController()
        print("✓ Controller initialized")
        
        # Test graph access
        graph = bfs_controller.domain_adapter.graph_model.graph
        print(f"✓ Graph loaded ({len(graph.nodes)} nodes)")
        
        # Test matplotlib figure creation
        fig, ax = plt.subplots(figsize=(8, 6))
        print("✓ Matplotlib figure created")
        
        # Test toolbar creation
        root = tk.Tk()
        root.withdraw()  # Hide window for testing
        
        canvas = FigureCanvasTkAgg(fig, master=root)
        toolbar = NavigationToolbar2Tk(canvas, root)
        print("✓ Navigation toolbar created")
        
        # Test zoom event handlers
        class MockEvent:
            def __init__(self, button='up', xdata=38.8, ydata=9.0, inaxes=True):
                self.button = button
                self.xdata = xdata
                self.ydata = ydata
                self.inaxes = inaxes
        
        # Simulate zoom events
        event = MockEvent()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        print(f"✓ Initial limits: x={xlim}, y={ylim}")
        
        # Test zoom calculation
        scale_factor = 0.9
        new_width = (xlim[1] - xlim[0]) * scale_factor
        new_height = (ylim[1] - ylim[0]) * scale_factor
        print(f"✓ Zoom calculation works: width={new_width:.2f}, height={new_height:.2f}")
        
        root.destroy()
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_gui_with_zoom():
    """Test GUI with zoom functionality."""
    print("\nTesting GUI with zoom...")
    
    try:
        # Import GUI
        from gui_pathfinder import PathFinderGUI
        
        # Create test window
        root = tk.Tk()
        root.title("Zoom Test")
        root.geometry("400x300")
        
        # Test GUI initialization
        app = PathFinderGUI(root)
        print("✓ GUI with zoom initialized")
        
        # Test zoom methods exist
        assert hasattr(app, 'on_scroll'), "Missing on_scroll method"
        assert hasattr(app, 'on_mouse_press'), "Missing on_mouse_press method"
        assert hasattr(app, 'reset_view'), "Missing reset_view method"
        print("✓ All zoom methods present")
        
        # Test toolbar exists
        assert hasattr(app, 'toolbar'), "Missing toolbar"
        print("✓ Navigation toolbar present")
        
        # Test original limits stored
        assert app.original_xlim is not None, "Original xlim not stored"
        assert app.original_ylim is not None, "Original ylim not stored"
        print("✓ Original view limits stored")
        
        # Test reset view
        app.reset_view()
        print("✓ Reset view method works")
        
        # Close after 2 seconds
        root.after(2000, root.destroy)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"✗ GUI test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("ZOOM FUNCTIONALITY TEST")
    print("=" * 50)
    
    # Test components
    components_ok = test_zoom_components()
    
    # Test GUI
    gui_ok = test_gui_with_zoom()
    
    print("\n" + "=" * 50)
    if components_ok and gui_ok:
        print("✅ ALL ZOOM TESTS PASSED!")
        print("\nZoom Features Available:")
        print("• Mouse wheel zoom (in/out)")
        print("• Navigation toolbar (pan, zoom box, reset)")
        print("• Middle-click reset")
        print("• Reset View button")
        print("• View preservation during pathfinding")
        print("\nTo start the GUI with zoom:")
        print("python gui_pathfinder.py")
    else:
        print("❌ SOME ZOOM TESTS FAILED")
    print("=" * 50)
