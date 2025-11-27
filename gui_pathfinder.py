#!/usr/bin/env python3
"""
GUI Path Finder using Tkinter.
Map display on left, output on right, with algorithm selection and location inputs.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from pathlib import Path
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
import osmnx as ox

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.controllers.generic_pathfinding_controller import GenericPathfindingController
from src.controllers.classic_dfs_controller import ClassicDFSController
from src.controllers.astar_controller import AStarController


class PathFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Path Finder - Addis Ababa")
        self.root.geometry("1400x800")
        
        # Initialize controllers
        self.bfs_controller = GenericPathfindingController()
        self.dfs_controller = ClassicDFSController()
        from core.addis_ababa_adapter import AddisAbabaAdapter
        adapter = AddisAbabaAdapter()
        self.astar_controller = AStarController(adapter)
        
        # Available locations
        self.locations = [
            "Bole International Airport", "Meskel Square", "Piassa",
            "Kazanchis", "Arat Kilo", "Mexico Square", "Sarbet",
            "Bole Medhanealem", "Gotera", "Megenagna"
        ]
        
        # Current algorithm
        self.current_algorithm = tk.StringVar(value="BFS")
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI layout."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Top panel - Controls
        self.setup_control_panel(main_frame)
        
        # Middle panel - Map and Output
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel - Map
        self.setup_map_panel(content_frame)
        
        # Right panel - Output
        self.setup_output_panel(content_frame)
        
    def setup_control_panel(self, parent):
        """Setup the control panel with inputs and algorithm selection."""
        control_frame = ttk.LabelFrame(parent, text="Path Finding Controls", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start Location
        ttk.Label(control_frame, text="Start Location:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(control_frame, textvariable=self.start_var, values=self.locations, width=30)
        self.start_combo.grid(row=0, column=1, padx=(0, 20))
        
        # End Location
        ttk.Label(control_frame, text="Destination:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.end_var = tk.StringVar()
        self.end_combo = ttk.Combobox(control_frame, textvariable=self.end_var, values=self.locations, width=30)
        self.end_combo.grid(row=0, column=3, padx=(0, 20))
        
        # Algorithm Selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        algorithm_frame = ttk.Frame(control_frame)
        algorithm_frame.grid(row=0, column=5, padx=(0, 20))
        
        ttk.Radiobutton(algorithm_frame, text="BFS", variable=self.current_algorithm, 
                       value="BFS").grid(row=0, column=0, padx=(0, 10))
        ttk.Radiobutton(algorithm_frame, text="DFS", variable=self.current_algorithm, 
                       value="DFS").grid(row=0, column=1, padx=(0, 10))
        ttk.Radiobutton(algorithm_frame, text="A*", variable=self.current_algorithm, 
                       value="A*").grid(row=0, column=2)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=6, padx=(10, 0))
        
        self.find_button = ttk.Button(button_frame, text="Find Path", command=self.find_path)
        self.find_button.grid(row=0, column=0, padx=(0, 5))
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_all)
        self.clear_button.grid(row=0, column=1, padx=(0, 5))
        
        self.reset_button = ttk.Button(button_frame, text="Reset View", command=self.reset_view)
        self.reset_button.grid(row=0, column=2, padx=(0, 5))
        
        self.test_button = ttk.Button(button_frame, text="Test Constraints", command=self.test_constraints)
        self.test_button.grid(row=0, column=3)
        
    def setup_map_panel(self, parent):
        """Setup the map display panel with zoom controls."""
        map_frame = ttk.LabelFrame(parent, text="Map Visualization", padding="10")
        map_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Create matplotlib figure for map
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=map_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar for zoom/pan controls
        toolbar_frame = ttk.Frame(map_frame)
        toolbar_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
        # Enable zoom with mouse wheel
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        
        # Store original view limits for reset
        self.original_xlim = None
        self.original_ylim = None
        
        # Load initial map
        self.load_initial_map()
        
    def setup_output_panel(self, parent):
        """Setup the output display panel."""
        output_frame = ttk.LabelFrame(parent, text="Results Output", padding="10")
        output_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Create scrolled text widget for output
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=40)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for formatting
        self.output_text.tag_configure("success", foreground="green", font=("Arial", 10, "bold"))
        self.output_text.tag_configure("error", foreground="red", font=("Arial", 10, "bold"))
        self.output_text.tag_configure("info", foreground="blue", font=("Arial", 10, "bold"))
        self.output_text.tag_configure("header", font=("Arial", 12, "bold"))
        
    def load_initial_map(self):
        """Load the initial Addis Ababa map."""
        try:
            # Get the graph from BFS controller's domain adapter
            graph = self.bfs_controller.domain_adapter.graph_model.graph
            
            # Plot the base map
            self.ax.clear()
            ox.plot_graph(graph, ax=self.ax, show=False, close=False)
            self.ax.set_title("Addis Ababa Road Network", fontsize=14, fontweight='bold')
            
            # Store original limits for reset functionality
            self.original_xlim = self.ax.get_xlim()
            self.original_ylim = self.ax.get_ylim()
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error loading map: {e}")
            # Create empty plot
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Map loading failed\nPath finding still works", 
                        ha='center', va='center', transform=self.ax.transAxes, fontsize=12)
            self.ax.set_title("Addis Ababa Road Network", fontsize=14, fontweight='bold')
            self.original_xlim = self.ax.get_xlim()
            self.original_ylim = self.ax.get_ylim()
            self.canvas.draw()
    
    def on_scroll(self, event):
        """Handle mouse wheel zoom."""
        if event.inaxes != self.ax:
            return
            
        # Get current x and y limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Get mouse position in data coordinates
        xdata = event.xdata
        ydata = event.ydata
        
        # Determine zoom direction
        if event.button == 'up':
            # Zoom in
            scale_factor = 0.9
        else:
            # Zoom out
            scale_factor = 1.1
            
        # Calculate new limits
        new_width = (xlim[1] - xlim[0]) * scale_factor
        new_height = (ylim[1] - ylim[0]) * scale_factor
        
        # Center on mouse position
        relx = (xdata - xlim[0]) / (xlim[1] - xlim[0])
        rely = (ydata - ylim[0]) / (ylim[1] - ylim[0])
        
        new_xlim = [
            xdata - new_width * relx,
            xdata + new_width * (1 - relx)
        ]
        new_ylim = [
            ydata - new_height * rely,
            ydata + new_height * (1 - rely)
        ]
        
        # Apply new limits
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw_idle()
    
    def on_mouse_press(self, event):
        """Handle mouse click for pan mode."""
        if event.inaxes != self.ax:
            return
            
        # Middle mouse button to reset view
        if event.button == 2:  # Middle button
            self.reset_view()
    
    def reset_view(self):
        """Reset the map view to original limits."""
        if self.original_xlim and self.original_ylim:
            self.ax.set_xlim(self.original_xlim)
            self.ax.set_ylim(self.original_ylim)
            self.canvas.draw_idle()
            
    def find_path(self):
        """Find path using selected algorithm."""
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()
        algorithm = self.current_algorithm.get()
        
        if not start or not end:
            messagebox.showwarning("Input Error", "Please enter both start and destination locations.")
            return
            
        # Clear previous output
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Finding path from {start} to {end} using {algorithm}...\n\n", "info")
        
        # Disable button during processing
        self.find_button.config(state="disabled")
        
        # Run pathfinding in separate thread to avoid GUI freezing
        threading.Thread(target=self._run_pathfinding, args=(start, end, algorithm), daemon=True).start()
        
    def _run_pathfinding(self, start, end, algorithm):
        """Run pathfinding in separate thread."""
        try:
            if algorithm == "DFS":
                # Use Classic DFS controller
                result = self.dfs_controller.find_paths_with_constraints(start, end)
                self._display_dfs_result(result, start, end)
            elif algorithm == "A*":
                # Use A* controller
                result = self.astar_controller.find_optimal_paths(start, end, algorithm.lower())
                self._display_astar_result(result, start, end)
            else:
                # Use BFS controller for BFS
                result = self.bfs_controller.find_optimal_paths(start, end, algorithm.lower())
                self._display_bfs_result(result, start, end, algorithm)
                
        except Exception as e:
            self.root.after(0, lambda: self._display_error(str(e)))
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.find_button.config(state="normal"))
            
    def _display_bfs_result(self, result, start, end, algorithm):
        """Display BFS/A* result."""
        self.root.after(0, lambda: self.output_text.insert(tk.END, f"=== {algorithm} RESULTS ===\n\n", "header"))
        
        if result["success"]:
            paths = result["paths"]
            if paths:
                # Display path information
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Found {len(paths)} optimal paths\n", "success"))
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Primary path: {len(paths[0])-1} steps\n", "info"))
                
                if len(paths) > 1:
                    self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ {len(paths)-1} alternative paths\n", "info"))
                
                # Display route
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"\nRoute: {result.get('start_node', 'Unknown')} to {result.get('goal_node', 'Unknown')}\n"))
                
                # Visualize paths
                self.root.after(0, self._visualize_paths, result)
                
            else:
                self.root.after(0, lambda: self.output_text.insert(tk.END, "No paths found\n", "error"))
        else:
            self.root.after(0, lambda: self.output_text.insert(tk.END, f"✗ {result.get('message', 'Unknown error')}\n", "error"))
            
    def _display_dfs_result(self, result, start, end):
        """Display Classic DFS result."""
        self.root.after(0, lambda: self.output_text.insert(tk.END, "=== CLASSIC DFS RESULTS ===\n\n", "header"))
        
        if result["success"]:
            paths = result["paths"]
            if paths:
                # Display DFS-specific information
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Found {len(paths)} paths\n", "success"))
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Nodes explored: {len(result.get('visited_nodes', [])):,}\n", "info"))
                
                # Find shortest path
                shortest_idx = min(range(len(paths)), key=lambda i: len(paths[i]))
                shortest_length = len(paths[shortest_idx]) - 1
                
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Shortest path: {shortest_length} steps (Path {shortest_idx + 1})\n", "info"))
                
                # Display all path details
                self.root.after(0, lambda: self.output_text.insert(tk.END, "\nPATH DETAILS:\n", "header"))
                for i, path in enumerate(paths):
                    path_length = len(path) - 1
                    if i == shortest_idx:
                        self.root.after(0, lambda i=i, path_length=path_length: 
                                       self.output_text.insert(tk.END, f"PRIMARY: {path_length} steps\n", "success"))
                    else:
                        self.root.after(0, lambda i=i, path_length=path_length: 
                                       self.output_text.insert(tk.END, f"ALT {i}: {path_length} steps\n"))
                
                # Visualize paths
                self.root.after(0, self._visualize_paths, result)
                
            else:
                self.root.after(0, lambda: self.output_text.insert(tk.END, "No paths found\n", "error"))
        else:
            self.root.after(0, lambda: self.output_text.insert(tk.END, f"✗ {result.get('message', 'Unknown error')}\n", "error"))
            
    def _display_astar_result(self, result, start, end):
        """Display A* result."""
        self.root.after(0, lambda: self.output_text.insert(tk.END, "=== A* RESULTS ===\n\n", "header"))
        
        if result["success"]:
            paths = result["paths"]
            if paths:
                # Display A*-specific information
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Found {len(paths)} optimal paths\n", "success"))
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Nodes explored: {len(result.get('visited_nodes', [])):,}\n", "info"))
                
                # Display heuristic weight if available
                heuristic_weight = result.get('heuristic_weight', 1.0)
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Heuristic weight: {heuristic_weight}\n", "info"))
                
                # Find shortest path
                shortest_idx = min(range(len(paths)), key=lambda i: len(paths[i]))
                shortest_length = len(paths[shortest_idx]) - 1
                
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"✓ Shortest path: {shortest_length} steps (Path {shortest_idx + 1})\n", "info"))
                
                # Display all path details
                self.root.after(0, lambda: self.output_text.insert(tk.END, "\nPATH DETAILS:\n", "header"))
                for i, path in enumerate(paths):
                    path_length = len(path) - 1
                    if i == shortest_idx:
                        self.root.after(0, lambda i=i, path_length=path_length: 
                                       self.output_text.insert(tk.END, f"PRIMARY: {path_length} steps\n", "success"))
                    else:
                        self.root.after(0, lambda i=i, path_length=path_length: 
                                       self.output_text.insert(tk.END, f"ALT {i}: {path_length} steps\n"))
                
                # Visualize paths
                self.root.after(0, self._visualize_paths, result)
                
            else:
                self.root.after(0, lambda: self.output_text.insert(tk.END, "No paths found\n", "error"))
        else:
            self.root.after(0, lambda: self.output_text.insert(tk.END, f"✗ {result.get('message', 'Unknown error')}\n", "error"))
            
    def _visualize_paths(self, result):
        """Visualize paths on the map using original terminal visualization style."""
        try:
            # Store current zoom level
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            
            # Clear previous plot
            self.ax.clear()
            
            # Get graph and visualization settings
            graph = self.bfs_controller.domain_adapter.graph_model.graph
            from config.settings import VISUALIZATION_COLORS, EXPLORED_LINE_WIDTH, EXPLORED_ALPHA, PRIMARY_LINE_WIDTH, ALTERNATIVE_LINE_WIDTH
            
            # Plot base graph (lightgray edges)
            ox.plot_graph(graph, ax=self.ax, show=False, close=False, node_size=0, 
                         edge_linewidth=0.3, edge_color=VISUALIZATION_COLORS["base_edges"])
            
            # Plot explored nodes (blue) - if available in result
            visited_nodes = result.get("visited_nodes", set())
            if visited_nodes:
                self._plot_explored_area_gui(visited_nodes, graph, EXPLORED_LINE_WIDTH, EXPLORED_ALPHA)
            
            # Plot paths
            paths = result["paths"]
            if paths:
                # Plot alternative paths first (so primary is on top)
                colors = VISUALIZATION_COLORS["alternatives"]
                for i, path in enumerate(paths[1:], 1):  # Skip primary (index 0)
                    if i - 1 < len(colors) and len(path) > 1:
                        self._draw_path_gui(path, graph, colors[i - 1], ALTERNATIVE_LINE_WIDTH)
                
                # Plot primary path (red) on top
                primary_path = paths[0]
                if len(primary_path) > 1:
                    self._draw_path_gui(primary_path, graph, VISUALIZATION_COLORS["primary"], PRIMARY_LINE_WIDTH)
                    
                    # Add start and end markers
                    start_node, end_node = primary_path[0], primary_path[-1]
                    if graph.has_node(start_node) and graph.has_node(end_node):
                        start_y, start_x = graph.nodes[start_node]['y'], graph.nodes[start_node]['x']
                        end_y, end_x = graph.nodes[end_node]['y'], graph.nodes[end_node]['x']
                        
                        self.ax.plot(start_x, start_y, 'go', markersize=10, label='Start')
                        self.ax.plot(end_x, end_y, 'ro', markersize=10, label='End')
            
            # Add title
            algorithm = "BFS" if "BFS" in str(result) else "DFS"
            self.ax.set_title(f"Path Finding - {algorithm} Algorithm", fontsize=14, fontweight='bold')
            
            # Add legend with proper colors
            self._add_legend_gui(paths, VISUALIZATION_COLORS, visited_nodes)
            
            # Restore zoom level
            self.ax.set_xlim(current_xlim)
            self.ax.set_ylim(current_ylim)
            
            # Refresh canvas
            self.canvas.draw()
            
        except Exception as e:
            print(f"Visualization error: {e}")
            # Show error on plot
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Visualization Error\n{str(e)}\n\nPath finding results\nare shown in the\noutput panel", 
                        ha='center', va='center', transform=self.ax.transAxes, fontsize=12)
            algorithm = "BFS" if "BFS" in str(result) else "DFS"
            self.ax.set_title(f"Path Finding - {algorithm} Algorithm", fontsize=14, fontweight='bold')
            self.canvas.draw()
    
    def _plot_explored_area_gui(self, visited_nodes, graph, line_width, alpha):
        """Plot explored area in blue - matches original terminal visualization."""
        visited_nodes_list = list(visited_nodes)
        if visited_nodes_list:
            # Create subgraph of visited nodes
            visited_subgraph = graph.subgraph(visited_nodes_list)
            
            # Plot edges in explored area
            for u, v in visited_subgraph.edges():
                if graph.has_node(u) and graph.has_node(v):
                    u_data = graph.nodes[u]
                    v_data = graph.nodes[v]
                    x_coords = [u_data['x'], v_data['x']]
                    y_coords = [u_data['y'], v_data['y']]
                    self.ax.plot(x_coords, y_coords, 'b-', 
                               linewidth=line_width, 
                               alpha=alpha)
    
    def _draw_path_gui(self, path, graph, color, linewidth):
        """Draw a single path on the map - matches original visualization."""
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            if graph.has_node(u) and graph.has_node(v):
                u_data = graph.nodes[u]
                v_data = graph.nodes[v]
                x_coords = [u_data['x'], v_data['x']]
                y_coords = [u_data['y'], v_data['y']]
                self.ax.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=0.9)
    
    def _add_legend_gui(self, paths, colors, visited_nodes):
        """Add legend matching original terminal visualization."""
        legend_handles = []
        legend_labels = []
        
        # Add explored nodes if present
        if visited_nodes:
            from matplotlib.lines import Line2D
            explored_line = Line2D([0], [0], color='blue', linewidth=0.8, alpha=0.25, label='Explored Area')
            legend_handles.append(explored_line)
            legend_labels.append('Explored Area')
        
        # Add paths
        if paths and len(paths) > 0:
            # Primary path (red)
            from matplotlib.lines import Line2D
            primary_line = Line2D([0], [0], color=colors["primary"], linewidth=4, label='Primary Path')
            legend_handles.append(primary_line)
            legend_labels.append('Primary Path')
            
            # Alternative paths
            for i, path in enumerate(paths[1:], 1):
                if i - 1 < len(colors["alternatives"]):
                    alt_color = colors["alternatives"][i - 1]
                    alt_line = Line2D([0], [0], color=alt_color, linewidth=3, label=f'Alternative {i}')
                    legend_handles.append(alt_line)
                    legend_labels.append(f'Alternative {i}')
        
        # Add start/end markers if paths exist
        if paths and len(paths) > 0:
            from matplotlib.lines import Line2D
            start_marker = Line2D([0], [0], marker='o', color='w', markerfacecolor='g', 
                                markersize=8, label='Start')
            end_marker = Line2D([0], [0], marker='o', color='w', markerfacecolor='r', 
                              markersize=8, label='End')
            legend_handles.append(start_marker)
            legend_labels.append('Start')
            legend_handles.append(end_marker)
            legend_labels.append('End')
        
        if legend_handles:
            self.ax.legend(handles=legend_handles, labels=legend_labels, loc='upper right')
            
    def _display_error(self, error_msg):
        """Display error message."""
        self.output_text.insert(tk.END, f"✗ Error: {error_msg}\n", "error")
        
    def test_constraints(self):
        """Test constraint handling."""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "=== TESTING CONSTRAINTS ===\n\n", "header")
        
        # Test cases
        test_cases = [
            ("Unknown Location", "nonexistentplace", "sarbet"),
            ("Same Location", "sarbet", "sarbet"),
            ("Valid Path", "meskel square", "sarbet"),
            ("Case Insensitive", "PIASSA", "Arat Kilo")
        ]
        
        for test_name, start, end in test_cases:
            self.output_text.insert(tk.END, f"Testing: {test_name}\n", "info")
            self.output_text.insert(tk.END, f"Input: '{start}' → '{end}'\n")
            
            try:
                result = self.bfs_controller.find_optimal_paths(start, end, "bfs")
                if result["success"]:
                    paths = result["paths"]
                    if paths:
                        self.output_text.insert(tk.END, f"✓ Success: {len(paths)} path(s) found\n", "success")
                    else:
                        self.output_text.insert(tk.END, "✓ Success: Same location (0 steps)\n", "success")
                else:
                    self.output_text.insert(tk.END, f"✓ Handled: {result.get('message', 'Unknown constraint')}\n", "info")
            except Exception as e:
                self.output_text.insert(tk.END, f"✗ Error: {e}\n", "error")
            
            self.output_text.insert(tk.END, "\n")
            
        self.output_text.insert(tk.END, "Constraint testing complete!\n", "success")
        
    def clear_all(self):
        """Clear all outputs and reset map."""
        # Clear output
        self.output_text.delete(1.0, tk.END)
        
        # Clear inputs
        self.start_var.set("")
        self.end_var.set("")
        
        # Reset map
        self.load_initial_map()


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = PathFinderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
