#!/usr/bin/env python3
"""
Test A* alternative path finding specifically.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_astar_alternatives_debug():
    """Debug why A* alternatives aren't being found."""
    print("Debugging A* alternative paths...")
    
    try:
        from controllers.astar_controller import AStarController
        from core.addis_ababa_adapter import AddisAbabaAdapter
        
        adapter = AddisAbabaAdapter()
        controller = AStarController(adapter)
        
        # Test with different locations
        test_cases = [
            ('sarbet', 'gotera'),
            ('bole airport', 'meskel square'),
            ('piassa', 'kazanchis')
        ]
        
        for start, end in test_cases:
            print(f"\n--- Testing: {start} → {end} ---")
            
            # Test basic A*
            result = controller.find_optimal_paths(start, end, 'astar')
            print(f"Basic A*: {len(result['paths'])} paths")
            
            # Test with constraints
            result2 = controller.find_paths_with_constraints(start, end, max_paths=5)
            print(f"With constraints: {len(result2['paths'])} paths")
            
            # Check algorithm internals
            algorithm = controller.astar_algorithm
            all_paths = algorithm.get_all_found_paths()
            visited_nodes = algorithm.get_visited_nodes()
            
            print(f"Algorithm internals:")
            print(f"  All found paths: {len(all_paths)}")
            print(f"  Visited nodes: {len(visited_nodes)}")
            
            if all_paths:
                for i, path in enumerate(all_paths):
                    print(f"    Internal path {i+1}: {len(path)} nodes")
            
            # Test similarity check
            if len(all_paths) > 1:
                path1 = all_paths[0]
                path2 = all_paths[1]
                set1, set2 = set(path1), set(path2)
                intersection = len(set1 & set2)
                union = len(set1 | set2)
                similarity = intersection / union if union > 0 else 0
                print(f"  Similarity between path 1 and 2: {similarity:.2f}")
                print(f"  Threshold: 0.4 (lowered from 0.7)")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_alternative_heuristics():
    """Test different heuristic weights manually."""
    print("\nTesting alternative heuristics...")
    
    try:
        from controllers.astar_controller import AStarController
        from core.addis_ababa_adapter import AddisAbabaAdapter
        
        adapter = AddisAbabaAdapter()
        controller = AStarController(adapter)
        
        # Test different heuristic weights
        weights = [0.5, 1.0, 1.5, 2.0]
        
        for weight in weights:
            print(f"\n--- Testing heuristic weight: {weight} ---")
            
            result = controller.find_paths_with_constraints(
                'sarbet', 'gotera', 
                max_paths=3,
                heuristic_weight=weight
            )
            
            print(f"Paths found: {len(result['paths'])}")
            if result['paths']:
                for i, path in enumerate(result['paths']):
                    cost = result['path_costs'][i]
                    print(f"  Path {i+1}: {len(path)} nodes, {cost:.0f}m")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("A* ALTERNATIVE PATHS - DEBUG TEST")
    print("=" * 70)
    
    # Debug alternatives
    debug_ok = test_astar_alternatives_debug()
    
    # Test heuristics
    heuristics_ok = test_alternative_heuristics()
    
    print("\n" + "=" * 70)
    if debug_ok and heuristics_ok:
        print("✅ A* ALTERNATIVES DEBUG COMPLETED")
        print("Check the output above to understand why alternatives aren't found")
    else:
        print("❌ A* ALTERNATIVES DEBUG FAILED")
    print("=" * 70)
