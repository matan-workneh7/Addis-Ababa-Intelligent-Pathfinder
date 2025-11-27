"""
Main application entry point for Classic DFS Path Finder.
Uses the user's classic DFS algorithm with clean architecture.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.controllers.classic_dfs_controller import ClassicDFSController


def print_header():
    """Print application header."""
    print("=== Classic DFS Path Finder - Addis Ababa ===")
    print("Using Clean Architecture with Stack-Based DFS Algorithm")
    print("Features: Addis Ababa constraints and path validation")
    print()


def show_dfs_algorithm_info():
    """Show information about the classic DFS algorithm."""
    print("\\n=== CLASSIC DFS ALGORITHM ===")
    print("Based on your provided implementation:")
    print("• Uses stack for traversal (not recursion)")
    print("• Explores as far down a branch as possible")
    print("• Tracks visited nodes and path reconstruction")
    print("• Backtracks when dead end is reached")
    print("\\nAlgorithm Steps:")
    print("1. Initialize stack with start node")
    print("2. Pop current node from stack")
    print("3. If goal found, reconstruct path")
    print("4. Push unvisited neighbors to stack")
    print("5. Repeat until stack empty or goal found")
    print("\\nAddis Ababa Constraints:")
    print("• Maximum depth (prevent endless loops)")
    print("• Maximum cost (reasonable travel distance)")
    print("• Path diversity (different routes)")
    print()


def get_user_input(controller: ClassicDFSController) -> tuple[str, str, dict]:
    """Get user input for start, goal, and DFS options."""
    locations = controller.list_available_locations()
    
    print("Available locations in Addis Ababa:")
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")
    print("Or enter any address in Addis Ababa")
    
    start = input("\\nEnter start location (name or address): ").strip()
    goal = input("Enter destination location (name or address): ").strip()
    
    print("\\nClassic DFS Options:")
    print("1. Find Paths with Constraints")
    print("2. Test Different Constraint Combinations")
    print("3. Compare with Other DFS Algorithms")
    
    choice = input("Choose option (1-3, default=1): ").strip()
    
    dfs_options = {
        "mode": {"1": "constraints", "2": "testing", "3": "comparison", "": "constraints"}.get(choice, "constraints"),
        "max_depth": None,
        "max_cost": None,
        "diversity_threshold": 0.7
    }
    
    if dfs_options["mode"] == "constraints":
        depth_input = input("Maximum depth (optional, default=25): ").strip()
        if depth_input:
            try:
                dfs_options["max_depth"] = int(depth_input)
            except ValueError:
                print("Invalid depth, using default 25")
        
        cost_input = input("Maximum cost in meters (optional, default=10000): ").strip()
        if cost_input:
            try:
                dfs_options["max_cost"] = float(cost_input)
            except ValueError:
                print("Invalid cost, using default 10000")
        
        diversity_input = input("Diversity threshold (0.0-1.0, default=0.7): ").strip()
        if diversity_input:
            try:
                dfs_options["diversity_threshold"] = float(diversity_input)
            except ValueError:
                print("Invalid diversity, using default 0.7")
    
    return start, goal, dfs_options


def run_with_constraints(controller: ClassicDFSController, start: str, goal: str, options: dict):
    """Run Classic DFS with Addis Ababa constraints."""
    print("\\n=== CLASSIC DFS WITH CONSTRAINTS ===")
    print(f"Searching from {start} to {goal} using your classic DFS algorithm...")
    
    result = controller.run_classic_dfs_with_constraints(
        start_location=start,
        goal_location=goal,
        max_depth=options["max_depth"],
        max_cost=options["max_cost"],
        diversity_threshold=options["diversity_threshold"]
    )
    
    if result["success"]:
        print(f"\\n✓ Classic DFS completed successfully!")
        print(f"  Paths found: {len(result['paths'])}")
        print(f"  Constraints applied: {len(result.get('constraints_applied', []))}")
        print(f"  Nodes explored: {len(result.get('visited_nodes', set()))}")
    else:
        print(f"✗ Classic DFS failed: {result.get('message', 'Unknown error')}")


def run_constraint_testing(controller: ClassicDFSController, start: str, goal: str):
    """Run Classic DFS constraint testing."""
    print("\\n=== CONSTRAINT TESTING ===")
    print("Testing Classic DFS with different constraint combinations...")
    
    results = controller.test_classic_dfs_constraints(start, goal)
    
    print(f"\\n=== CONSTRAINT TESTING SUMMARY ===")
    for test_name, result in results.items():
        if result["success"]:
            print(f"✓ {test_name}: {len(result['paths'])} paths")
        else:
            print(f"✗ {test_name}: Failed")


def run_algorithm_comparison(controller: ClassicDFSController, start: str, goal: str):
    """Run comparison of Classic DFS with other DFS algorithms."""
    print("\\n=== ALGORITHM COMPARISON ===")
    print("Comparing Classic DFS with other DFS implementations...")
    
    # Test Classic DFS
    print(f"\\nTesting Classic DFS:")
    classic_result = controller.run_classic_dfs_with_constraints(start, goal, max_depth=25, max_cost=10000)
    
    # Test Simple DFS
    print(f"\\nTesting Simple DFS:")
    try:
        from src.controllers.simple_dfs_controller import SimpleDFSController
        simple_controller = SimpleDFSController()
        simple_result = simple_controller.find_paths(start, goal, max_paths=3)
        
        if simple_result["success"]:
            print(f"✓ Simple DFS: {len(simple_result['paths'])} paths")
        else:
            print(f"✗ Simple DFS: Failed")
    except Exception as e:
        print(f"✗ Simple DFS: Error - {e}")
        simple_result = None
    
    # Test Optimized DFS
    print(f"\\nTesting Optimized DFS:")
    try:
        from src.controllers.optimized_dfs_controller import OptimizedDFSController
        optimized_controller = OptimizedDFSController()
        optimized_result = optimized_controller.find_all_alternatives(start, goal, max_paths=3, time_limit=10.0)
        
        if optimized_result["success"]:
            print(f"✓ Optimized DFS: {len(optimized_result['paths'])} paths")
        else:
            print(f"✗ Optimized DFS: Failed")
    except Exception as e:
        print(f"✗ Optimized DFS: Error - {e}")
        optimized_result = None
    
    # Comparison summary
    print(f"\\n=== COMPARISON SUMMARY ===")
    print(f"Classic DFS: {len(classic_result['paths']) if classic_result['success'] else 0} paths")
    print(f"Simple DFS: {len(simple_result['paths']) if simple_result and simple_result['success'] else 0} paths")
    print(f"Optimized DFS: {len(optimized_result['paths']) if optimized_result and optimized_result['success'] else 0} paths")
    
    # Find best performer
    results = {
        "Classic DFS": len(classic_result['paths']) if classic_result['success'] else 0,
        "Simple DFS": len(simple_result['paths']) if simple_result and simple_result['success'] else 0,
        "Optimized DFS": len(optimized_result['paths']) if optimized_result and optimized_result['success'] else 0
    }
    
    best_algorithm = max(results.keys(), key=lambda k: results[k])
    print(f"Best performer: {best_algorithm} ({results[best_algorithm]} paths)")


def main():
    """Main application entry point."""
    try:
        print_header()
        show_dfs_algorithm_info()
        
        # Initialize the Classic DFS controller
        print("Loading Addis Ababa map...")
        controller = ClassicDFSController()
        
        # Get user input
        start, goal, options = get_user_input(controller)
        
        # Run based on mode
        if options["mode"] == "constraints":
            run_with_constraints(controller, start, goal, options)
        elif options["mode"] == "testing":
            run_constraint_testing(controller, start, goal)
        elif options["mode"] == "comparison":
            run_algorithm_comparison(controller, start, goal)
        
        print("\\n=== CLASSIC DFS EXPLORATION COMPLETE ===")
        print("Key Features:")
        print("✓ User's classic DFS algorithm (stack-based)")
        print("✓ Addis Ababa-specific constraints")
        print("✓ Path validation and diversity")
        print("✓ Constraint testing and comparison")
        print("✓ Visualization with exploration area")
        print("\\nCheck the generated visualization file!")
        
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
