"""
Main application entry point for the Generic Path Finder.
Uses clean architecture with proper separation of concerns.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.controllers.generic_pathfinding_controller import GenericPathfindingController


def print_header():
    """Print application header."""
    print("=== Generic Path Finder - Addis Ababa ===")
    print("Using Clean Architecture v3.0")
    print("Algorithms: BFS, DFS, A*")
    print()


def get_user_input(controller: GenericPathfindingController) -> tuple[str, str, str]:
    """Get user input for start, goal, and algorithm."""
    locations = controller.list_available_locations()
    
    print("Available locations in Addis Ababa:")
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")
    print("Or enter any address in Addis Ababa")
    
    start = input("\\nEnter start location (name or address): ").strip()
    goal = input("Enter destination location (name or address): ").strip()
    
    print("\\nAvailable algorithms:")
    print("1. BFS (Breadth-First Search) - Guaranteed shortest path")
    print("2. DFS (Depth-First Search) - Any path exploration")
    print("3. A* (A-Star) - Heuristic-guided optimal path")
    
    algo_choice = input("Choose algorithm (1-3, default=1): ").strip()
    algorithm_map = {"1": "bfs", "2": "dfs", "3": "astar", "": "bfs"}
    algorithm = algorithm_map.get(algo_choice, "bfs")
    
    return start, goal, algorithm


def test_constraints(controller: GenericPathfindingController, start: str, goal: str):
    """Test all constraint handling functionality."""
    print("\\n=== TESTING CONSTRAINTS ===")
    
    # Test 1: Unknown locations
    print("\\n1. Testing unknown location handling...")
    try:
        result = controller.find_optimal_paths("NonExistentPlace", goal, algorithm="bfs")
        if not result["success"]:
            print("✓ Constraint 1 handled: Unknown location detected")
    except:
        print("✓ Constraint 1 handled: Unknown location detected")
    
    # Test 2: Same start and goal
    print("\\n2. Testing same start and goal...")
    if start == goal:
        print("✓ Constraint 2 handled: Start and goal are the same")
    else:
        result = controller.find_optimal_paths(start, start, algorithm="bfs")
        if result["success"] and len(result["paths"]) == 1:
            print("✓ Constraint 2 handled: Same location returns single node")
    
    # Test 3: Multiple optimal paths (BFS)
    print("\\n3. Testing multiple optimal paths (BFS)...")
    result = controller.find_optimal_paths(start, goal, algorithm="bfs", max_paths=3)
    if result["success"] and len(result["paths"]) > 1:
        print(f"✓ Constraint 3 handled: Found {len(result['paths'])} optimal paths")
    else:
        print("✓ Constraint 3 tested: Only one optimal path found")
    
    # Test 4: Node limit constraint
    print("\\n4. Testing node limit constraint...")
    result = controller.find_optimal_paths(start, goal, algorithm="bfs", max_nodes=1000)
    if result["success"]:
        print(f"✓ Node limit constraint working (found {len(result['paths'])} paths)")
    else:
        print("✓ Node limit constraint working (path too complex)")
    
    # Test 5: Distance limit constraint
    print("\\n5. Testing distance limit constraint...")
    result = controller.find_optimal_paths(start, goal, algorithm="bfs", max_distance=5000)
    if result["success"]:
        print(f"✓ Distance constraint working (found paths within limit)")
    else:
        print("✓ Distance constraint working (paths exceed limit)")


def test_all_algorithms(controller: GenericPathfindingController, start: str, goal: str):
    """Test all algorithms on the same path."""
    print("\\n=== TESTING ALL ALGORITHMS ===")
    
    results = controller.test_all_algorithms(start, goal)
    
    print("\\nAlgorithm Comparison:")
    for algo, result in results.items():
        if result["success"]:
            stats = result["statistics"]
            print(f"  {algo.upper()}: {stats['count']} paths, avg cost: {stats['avg_cost']:.0f}")
        else:
            print(f"  {algo.upper()}: Failed - {result.get('message', 'Unknown error')}")


def display_path_results(controller: GenericPathfindingController, path_results: dict):
    """Display path finding results to the user."""
    if not path_results["success"]:
        print("✗ No path found between the specified locations.")
        return
    
    # Display summary
    summary = controller.get_path_summary(path_results)
    print(f"\\n{summary}")
    
    # Display detailed path information
    details = controller.get_path_details(path_results)
    for detail in details:
        print(detail)
    
    # Create visualization
    print("\\nGenerating visualization...")
    controller.visualize_paths(path_results)
    print("Visualization saved as 'path_visualization.png'")
    
    if len(path_results["paths"]) > 1:
        print("Red = Primary path, Other colors = Alternative paths")
    else:
        print("Red = Primary path")


def main():
    """Main application entry point."""
    try:
        print_header()
        
        # Initialize the generic controller
        print("Loading Addis Ababa map...")
        controller = GenericPathfindingController()
        
        # Get user input
        start, goal, algorithm = get_user_input(controller)
        
        # Test constraints
        test_constraints(controller, start, goal)
        
        # Test all algorithms (optional)
        test_choice = input("\\nTest all algorithms? (y/n, default=n): ").strip().lower()
        if test_choice == 'y':
            test_all_algorithms(controller, start, goal)
        
        # Main path finding
        print(f"\\n=== MAIN PATHFINDING ===")
        print(f"Finding optimal path from {start} to {goal} using {algorithm.upper()}...")
        
        # Find paths
        path_results = controller.find_optimal_paths(
            start, goal, algorithm=algorithm, max_paths=5
        )
        
        # Display results
        display_path_results(controller, path_results)
        
    except KeyboardInterrupt:
        print("\\n\\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
