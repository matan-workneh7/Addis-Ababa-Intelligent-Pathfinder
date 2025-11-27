# 🏗️ **Clean Architecture Documentation**

## 📁 **Project Structure**

```
path-finder/
├── src/                          # Source code
│   ├── core/                     # Core interfaces and models
│   │   ├── graph_interface.py    # Fundamental interfaces
│   │   ├── graph_model.py       # Graph domain model
│   │   ├── location_model.py    # Location domain model
│   │   ├── networkx_graph_adapter.py  # Graph implementation
│   │   └── addis_ababa_adapter.py     # Domain-specific adapter
│   ├── algorithms/               # Algorithm implementations
│   │   ├── bfs.py              # Breadth-First Search
│   │   ├── dfs.py              # Depth-First Search
│   │   ├── astar.py            # A* Algorithm
│   │   └── dfs_classic.py      # User's Classic DFS
│   ├── shared/                   # Reusable components
│   │   ├── constraints/        # Path validation constraints
│   │   ├── calculators/        # Path cost calculators
│   │   └── utils/              # Utility functions
│   ├── services/                 # Business logic services
│   │   ├── generic_pathfinding_service.py
│   │   ├── pathfinding_service.py
│   │   └── visualization_service.py
│   ├── controllers/              # Application controllers
│   │   ├── generic_pathfinding_controller.py
│   │   ├── classic_dfs_controller.py
│   │   └── pathfinding_controller.py
│   └── __init__.py              # Main package exports
├── config/                       # Configuration files
├── assets/                       # Generated images and assets
├── docs/                         # Documentation
├── tests/                        # Test files
├── main_generic.py              # Generic path finder app
├── main_classic_dfs.py          # Classic DFS app
└── requirements.txt              # Dependencies
```

## 🎯 **Architecture Principles**

### **✅ 1. Single Responsibility Principle**
- **Core/**: Interfaces and domain models only
- **Algorithms/**: Pure algorithm implementations
- **Shared/**: Reusable components
- **Services/**: Business logic coordination
- **Controllers/**: User interaction handling

### **✅ 2. Dependency Injection**
- Controllers depend on services
- Services depend on algorithms and adapters
- Algorithms depend on interfaces (not implementations)
- No circular dependencies

### **✅ 3. Clean Layer Separation**
```
Controllers → Services → Algorithms → Core Interfaces
     ↓            ↓           ↓              ↓
   User UI    Business   Algorithm    Domain Models
   Layer      Logic      Layer         Layer
```

### **✅ 4. Configuration Separation**
- All configuration in `config/` directory
- Environment-specific settings
- No hardcoded values in source code

## 📦 **Module Responsibilities**

### **🔧 Core Module**
- **Purpose**: Define contracts and domain models
- **Contains**: Interfaces, models, adapters
- **Dependencies**: None (pure domain)
- **Export**: GraphInterface, PathfindingAlgorithmInterface, etc.

### **⚡ Algorithms Module**
- **Purpose**: Implement path finding algorithms
- **Contains**: BFS, DFS, A*, Classic DFS
- **Dependencies**: Core interfaces only
- **Export**: Algorithm implementations

### **🔄 Shared Module**
- **Purpose**: Reusable components across the system
- **Contains**: Constraints, calculators, utilities
- **Dependencies**: Core interfaces
- **Export**: Constraints, calculators, utils

### **🎮 Services Module**
- **Purpose**: Business logic coordination
- **Contains**: Pathfinding services, visualization
- **Dependencies**: Algorithms, shared components
- **Export**: Service classes

### **🎯 Controllers Module**
- **Purpose**: Handle user interactions
- **Contains**: Application controllers
- **Dependencies**: Services only
- **Export**: Controller classes

## 🚀 **Import Patterns**

### **✅ Correct Dependencies**
```python
# Controller imports services
from src.services.generic_pathfinding_service import GenericPathfindingService

# Service imports algorithms
from src.algorithms.bfs import BFSAlgorithm

# Algorithm imports interfaces
from src.core.graph_interface import GraphInterface

# Shared components import interfaces
from src.core.graph_interface import ConstraintInterface
```

### **❌ Incorrect Dependencies**
```python
# Never import controllers from services
# Never import services from algorithms
# Never import algorithms from core
# No circular imports allowed
```

## 📋 **Naming Conventions**

### **✅ File Names**
- **snake_case**: `generic_pathfinding_controller.py`
- **Descriptive**: `classic_dfs_controller.py` (not `controller.py`)
- **Single purpose**: One responsibility per file

### **✅ Class Names**
- **PascalCase**: `GenericPathfindingController`
- **Descriptive**: `ClassicDFSController` (not `Controller`)
- **Interface suffix**: `GraphInterface`, `ConstraintInterface`

### **✅ Function Names**
- **snake_case**: `find_optimal_paths()`
- **Verb-first**: `calculate_path_cost()`, `validate_constraints()`
- **Small and focused**: Single responsibility per function

## 🔗 **Export Strategy**

### **✅ Named Exports (Multiple Items)**
```python
# __init__.py files
from .bfs import BFSAlgorithm
from .dfs import DFSAlgorithm

__all__ = ["BFSAlgorithm", "DFSAlgorithm"]
```

### **✅ Default Export (Single Main Item)**
```python
# For modules with one primary export
from .main_service import MainService as default
```

## 🎨 **Documentation Strategy**

### **✅ Document Only Important Logic**
- **Why**: Explain why complex decisions were made
- **What**: Don't document obvious code
- **Where**: Module-level docstrings and complex functions

### **✅ Example Documentation**
```python
def find_optimal_paths(self, start: str, goal: str) -> List[Path]:
    """
    Find optimal paths using the configured algorithm.
    
    Why: This method coordinates multiple algorithms to find
    the best paths while respecting domain constraints.
    
    Args:
        start: Starting location identifier
        goal: Destination location identifier
        
    Returns:
        List of optimal paths sorted by cost
    """
```

## 🚫 **Anti-Patterns to Avoid**

### **❌ God Files**
- Don't put everything in one file
- Split large files into focused modules
- One responsibility per file

### **❌ Deep Nesting**
- Avoid `src/controllers/services/algorithms/core/`
- Keep folder structure flat (max 3-4 levels)
- Group by purpose, not hierarchy

### **❌ Mixed Concerns**
- Never mix frontend and backend logic
- Keep UI separate from business logic
- Maintain clean layer boundaries

### **❌ Circular Dependencies**
- Controllers → Services → Algorithms → Core
- Never reverse this flow
- Use dependency injection to break cycles

## ✅ **Benefits of This Architecture**

### **🎯 Maintainability**
- **Clear separation**: Easy to find and modify code
- **Single responsibility**: Changes are isolated
- **Testable**: Each layer can be tested independently

### **🔄 Reusability**
- **Shared components**: Can be used across different parts
- **Interface-based**: Easy to swap implementations
- **Modular**: Components can be reused in other projects

### **📈 Scalability**
- **Layered**: Easy to add new features
- **Extensible**: New algorithms can be added easily
- **Configurable**: Behavior can be changed without code changes

### **🧪 Testability**
- **Mockable**: Dependencies can be mocked
- **Isolated**: Each layer can be tested separately
- **Clear contracts**: Interfaces define expected behavior

## 🎉 **Migration Summary**

### **✅ What Was Cleaned Up**
- **Moved files**: Organized by purpose/domain
- **Deleted MD files**: Moved to docs/ folder
- **Moved images**: Organized in assets/ folder
- **Updated imports**: Reflect new structure
- **Added index files**: Clean exports for each module
- **Fixed circular dependencies**: Clear layer separation

### **✅ New Structure Benefits**
- **Clean imports**: Easy to understand dependencies
- **Focused modules**: Each has single responsibility
- **Professional organization**: Industry-standard structure
- **Maintainable**: Easy to navigate and modify

**This clean architecture follows SOLID principles and industry best practices!** 🎯
