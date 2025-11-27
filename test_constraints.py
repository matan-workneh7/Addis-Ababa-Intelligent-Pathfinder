#!/usr/bin/env python3
"""
Test script to demonstrate constraint checking behavior.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.controllers.generic_pathfinding_controller import GenericPathfindingController

def test_constraint_scenarios():
    """Test different constraint scenarios."""
    print("=" * 60)
    print("CONSTRAINT BEHAVIOR TESTING")
    print("=" * 60)
    
    controller = GenericPathfindingController()
    
    test_cases = [
        {
            "name": "Unknown Start Location",
            "start": "nonexistentplace",
            "goal": "sarbet",
            "expected": "Should fail with unknown location error"
        },
        {
            "name": "Unknown Goal Location", 
            "start": "sarbet",
            "goal": "unknownplace",
            "expected": "Should fail with unknown location error"
        },
        {
            "name": "Same Start and Goal",
            "start": "sarbet",
            "goal": "sarbet", 
            "expected": "Should return 0-step path"
        },
        {
            "name": "Valid Different Locations",
            "start": "meskel square",
            "goal": "sarbet",
            "expected": "Should find optimal paths"
        },
        {
            "name": "Case Insensitive Test",
            "start": "PIASSA",
            "goal": "Arat Kilo",
            "expected": "Should work with mixed case"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Input: '{test_case['start']}' → '{test_case['goal']}'")
        print(f"   Expected: {test_case['expected']}")
        print(f"   Result: ", end="")
        
        try:
            result = controller.find_optimal_paths(
                test_case['start'], 
                test_case['goal'], 
                algorithm="bfs"
            )
            
            if result["success"]:
                paths = result["paths"]
                if paths:
                    print(f"✓ Found {len(paths)} path(s)")
                    print(f"     Primary: {len(paths[0])-1} steps")
                    if len(paths) > 1:
                        print(f"     Alternatives: {len(paths)-1} more")
                else:
                    print("✗ No paths found")
            else:
                print(f"✗ {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("CONSTRAINT TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_constraint_scenarios()
