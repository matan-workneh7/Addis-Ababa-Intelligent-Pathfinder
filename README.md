# Addis Ababa Intelligent Path Finder

## Project Overview

The Addis Ababa Path Finder is a comprehensive navigation system designed to solve urban routing challenges in Ethiopia's capital city. This system provides optimal path finding algorithms with constraint handling, real-time visualization, and scalable architecture.

**Key Benefits:**
- Reduces travel time through optimal routing
- Supports logistics and delivery services
- Provides foundation for transportation analysis
- Enables emergency services route optimization

**Target Users:**
- Logistics companies and delivery services
- Emergency response teams
- Urban planning departments
- Transportation researchers
- Navigation service providers

## Architecture Summary

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GUI Layer     │    │  Controllers    │    │   Services      │
│                 │    │                 │    │                 │
│ • Tkinter GUI   │◄──►│ • Generic        │◄──►│ • Pathfinding   │
│ • Visualization │    │ • Classic DFS    │    │ • Visualization │
│ • User Input    │    │ • A* Controller  │    │ • Constraint    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Algorithms   │    │   Core Layer     │    │   Data Layer    │
│                 │    │                 │    │                 │
│ • BFS Algorithm │◄──►│ • Interfaces     │◄──►│ • NetworkX      │
│ • Classic DFS   │    │ • Adapters       │    │ • OSMnx Cache   │
│ • A* Algorithm  │    │ • Models         │    │ • Location DB   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Core Features

### Functional Requirements
- **Multi-Algorithm Support**: BFS, Classic DFS, A* with heuristic search
- **Optimal Path Finding**: Guaranteed shortest paths with A* algorithm
- **Alternative Path Discovery**: Multiple route options with diversity checking
- **Advanced Constraint Handling**: Distance limits, node limits, time constraints, location validation
- **Real-time Visualization**: Interactive map with explored area display
- **GUI Application**: User-friendly interface with algorithm selection
- **Smart Location Suggestions**: AI-powered location recommendations for invalid inputs

### Non-Functional Requirements
- **Performance**: O(V+E) memory complexity, handles city-scale networks
- **Scalability**: Supports graphs with 10,000+ nodes
- **Reliability**: Robust error handling and recovery
- **Usability**: Intuitive interface with zoom/pan capabilities
- **Maintainability**: Clean architecture with separation of concerns

## Tech Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **NetworkX**: Graph algorithms and data structures
- **OSMnx**: OpenStreetMap data retrieval and processing
- **Matplotlib**: Visualization and plotting
- **Tkinter**: GUI framework (built-in Python)
- **Folium**: Interactive web maps with Leaflet
- **Contextily**: Map tiles for basemap visualization

### Core Libraries
- **heapq**: Priority queue implementation for A* algorithm
- **threading**: Non-blocking GUI operations
- **difflib**: Fuzzy string matching for location suggestions
- **tempfile**: Temporary file handling for web maps
- **webbrowser**: Cross-platform browser integration
- **time**: Timestamps and cache-busting
- **math**: Mathematical operations for heuristics
- **pathlib**: Modern path handling

### External Dependencies
- **OpenStreetMap API**: Real-time map data
- **Addis Ababa Road Network**: Geographic information system
- **FastAPI**: Web framework (for future API extensions)
- **Uvicorn**: ASGI server (for future API extensions)
- **Pydantic**: Data validation (for future API extensions)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git for version control
- 8GB+ RAM recommended for large city maps
- Web browser for interactive maps

### Development Setup

```bash
# Clone the repository
git clone <repository_url>
cd BFS-Searching-Algorithm\(2nd trial\)

# Install dependencies
pip install -r requirements.txt

# Verify installation
python gui_pathfinder.py
```

### Requirements.txt

```txt
# Core Dependencies
osmnx>=1.6.0              # OpenStreetMap data processing
networkx>=3.0             # Graph algorithms and data structures
matplotlib>=3.7.0         # Plotting and visualization
contextily                # Map tiles for basemap
folium                    # Interactive web maps

# GUI and System Libraries
# tkinter - Built into Python (no pip install needed)
# threading - Built into Python
# heapq - Built into Python
# difflib - Built into Python
# tempfile - Built into Python
# webbrowser - Built into Python
# time - Built into Python
# math - Built into Python
# pathlib - Built into Python

# Additional Libraries
pathlib2>=2.3.0           # Path handling (Python 2 compatibility)
Pillow>=9.0.0             # Image processing

# Future API Extensions (currently unused)
fastapi==0.115.2          # Web framework
uvicorn==0.31.0            # ASGI server
pydantic==2.9.2            # Data validation
```

### Running the Application

```bash
# Set up virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Launch application
python gui_pathfinder.py
```

## Environment Variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| OSM_CACHE_DIR | String | Directory for map cache | ./cache/osmnx |
| MAX_MEMORY_USAGE | Integer | Memory limit in MB | 8192 |
| LOG_LEVEL | Enum | Logging verbosity | INFO | DEBUG | ERROR |
| GUI_THEME | String | Interface theme | light | dark |
| DEFAULT_ALGORITHM | Enum | Default pathfinding algorithm | bfs | dfs | astar |

## Usage Instructions

### GUI Application

```bash
# Launch the interactive GUI
python gui_pathfinder.py
```

**Steps:**
1. Select start location from dropdown
2. Select destination location
3. Choose algorithm (BFS, DFS, A*)
4. Click "Find Path" button
5. View results with interactive visualization
6. Use zoom/pan to explore details

### Programmatic Usage

```python
from src.controllers.generic_pathfinding_controller import GenericPathfindingController
from src.controllers.classic_dfs_controller import ClassicDFSController
from src.controllers.astar_controller import AStarController

# Initialize controllers
bfs_controller = GenericPathfindingController()
dfs_controller = ClassicDFSController()
astar_controller = AStarController()

# Find optimal paths
results = bfs_controller.find_optimal_paths("Bole Airport", "Meskel Square")

# Check results
if results["success"]:
    print(f"Found {len(results['paths'])} optimal paths")
    for i, path in enumerate(results['paths']):
        print(f"Path {i+1}: {len(path)} nodes")
```

### Advanced Configuration

```python
# Custom constraints
results = controller.find_paths_with_constraints(
    start="Sarbet",
    goal="Gotera",
    max_paths=5,
    max_distance=10000,  # 10km limit
    max_nodes=1000,      # Processing limit
    max_time=60.0        # 1-minute time constraint
)
```

## Constraint System

### Available Constraints

#### 1. TimeConstraint
- **Purpose**: Limits estimated travel time along paths
- **Logic**: `time = distance / average_speed`
- **Default Speed**: 8.3 m/s (30 km/h urban speed)
- **Application**: Applied to all algorithms with 1-minute (60s) limit
- **Error Display**: Shows time in minutes for user-friendly format

```python
# Time constraint implementation
class TimeConstraint:
    def __init__(self, max_time_seconds: float, path_calculator, average_speed_m_per_s: float = 8.3):
        self.max_time_seconds = max_time_seconds
        self.path_calculator = path_calculator
        self.average_speed_m_per_s = average_speed_m_per_s
    
    def validate(self, path: List[int], graph: GraphInterface) -> tuple[bool, str]:
        distance_m = self.path_calculator.calculate_path_cost(path, graph)
        estimated_time_s = distance_m / self.average_speed_m_per_s
        
        if estimated_time_s > self.max_time_seconds:
            est_min = estimated_time_s / 60.0
            max_min = self.max_time_seconds / 60.0
            return False, f"Estimated travel time ({est_min:.1f} min) exceeds maximum ({max_min:.1f} min)"
        
        return True, ""
```

#### 2. DistanceConstraint
- **Purpose**: Limits maximum path distance in meters
- **Application**: Default 10,000m (10km) limit
- **Validation**: Checks cumulative path length

#### 3. NodeLimitConstraint
- **Purpose**: Limits maximum number of nodes in path
- **Application**: Default 25 nodes limit
- **Validation**: Prevents excessively long paths

#### 4. LocationValidationConstraint
- **Purpose**: Validates start/end locations exist in graph
- **Features**: Smart suggestions for invalid locations
- **Logic**: Fuzzy matching with 2-3 character prefixes

#### 5. SameLocationConstraint
- **Purpose**: Handles case where initial and goal states are the same
- **Logic**: Returns zero-distance path without running algorithms
- **Display**: "Path found: 0 steps (same location)" with single point visualization
- **Implementation**: Validates location, shows green marker with annotation

#### 6. UnknownLocationConstraint  
- **Purpose**: Handles invalid/unknown start or goal locations
- **Features**: AI-powered location suggestions based on user input
- **Logic**: Fuzzy matching with 2-3 character prefixes, word matching
- **Display**: "Did you mean [suggestions]?" with 1-4 location options
- **Priority**: Exact match → Prefix match → Word match → Fuzzy match

#### 7. MultipleOptimalPathsConstraint
- **Purpose**: Handles discovery of 2+ equal-cost optimal paths
- **Logic**: Validates path diversity with 40% similarity threshold
- **Features**: Weighted heuristics [0.5, 1.5, 2.0, 0.8] for alternatives
- **Validation**: Each alternative must satisfy all constraints
- **Display**: Shows primary path + alternative paths with different colors

### Constraint Application Logic

```python
# All algorithms receive the same constraint set
constraints = [
    TimeConstraint(60.0, path_calculator, 8.3),        # 1-minute time limit
    DistanceConstraint(10000, path_calculator),        # 10km distance limit  
    NodeLimitConstraint(25),                            # 25 node limit
    SameLocationConstraint(),                          # Handle same start/end
    UnknownLocationConstraint(),                       # Handle invalid locations
    MultipleOptimalPathsConstraint(),                  # Handle multiple paths
]

# Applied during pathfinding with special case handling
if start == end:
    result = handle_same_location(start, algorithm)    # SameLocationConstraint
elif not validate_locations(start, end):
    result = show_location_suggestions(start, end)    # UnknownLocationConstraint
else:
    # Normal pathfinding with all constraints
    if algorithm == "BFS":
        result = bfs_controller.find_optimal_paths(start, end, "bfs", max_time=60.0)
    elif algorithm == "A*":
        result = astar_controller.find_optimal_paths(start, end, "astar", max_time=60.0)
    elif algorithm == "DFS":
        result = dfs_controller.find_paths_with_constraints(start, end, max_time=60.0)
    
    # Handle multiple optimal paths
    if len(result["paths"]) > 1:
        result = apply_multiple_paths_constraint(result)  # MultipleOptimalPathsConstraint
```

## Heuristic Path Logic

### A* Algorithm Heuristics

#### Primary Heuristic: Euclidean Distance
- **Formula**: `√((lat₂-lat₁)² + (lon₂-lon₁)²)`
- **Purpose**: Estimates straight-line distance to goal
- **Optimality**: Guarantees admissible (never overestimates) heuristic

```python
def _heuristic(self, graph: GraphInterface, node1: int, node2: int) -> float:
    node1_data = graph.get_node_data(node1)
    node2_data = graph.get_node_data(node2)
    
    lat1, lon1 = node1_data['y'], node1_data['x']
    lat2, lon2 = node2_data['y'], node2_data['x']
    
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
```

#### Alternative Path Discovery
- **Strategy**: Weighted heuristics with different multipliers
- **Weights**: `[0.5, 1.5, 2.0, 0.8]`
- **Purpose**: Creates diverse path exploration strategies

| Weight | Effect | Use Case |
|--------|--------|----------|
| 0.5 | Explores more nodes, less greedy | Maximum diversity |
| 1.0 | Standard A* heuristic | Balanced approach |
| 1.5 | More greedy, faster | Quick alternatives |
| 2.0 | Very greedy, direct paths | Minimal exploration |

#### Path Diversity Validation
- **Similarity Threshold**: 40% for alternatives (vs 80% for primary)
- **Validation**: Each alternative must satisfy all constraints
- **Uniqueness**: Paths must be sufficiently different from existing ones

```python
def _paths_too_similar(self, path1: List[int], path2: List[int], threshold: float = 0.4) -> bool:
    # Calculate Jaccard similarity between paths
    set1, set2 = set(path1), set(path2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    if union == 0:
        return False
    
    similarity = intersection / union
    return similarity > threshold
```

### Algorithm Comparison

| Algorithm | Heuristic Used | Optimality | Exploration Pattern |
|-----------|----------------|------------|-------------------|
| **BFS** | None (unweighted) | Optimal for unweighted graphs | Layer-by-layer expansion |
| **DFS** | None (unweighted) | Not optimal | Deep dive, backtracking |
| **A*** | Euclidean distance | Optimal for weighted graphs | Goal-directed search |

## Project Structure

```
BFS-Searching-Algorithm(2nd trial)/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── gui_pathfinder.py           # Main GUI application
├── src/                        # Source code
│   ├── __init__.py            # Package initialization
│   ├── algorithms/             # Pathfinding algorithms
│   │   ├── bfs.py             # Breadth-First Search
│   │   ├── dfs_classic.py     # Classic Depth-First Search
│   │   └── astar_improved.py  # A* with heuristic search
│   ├── controllers/           # Workflow orchestration
│   │   ├── generic_pathfinding_controller.py
│   │   ├── classic_dfs_controller.py
│   │   └── astar_controller.py
│   ├── core/                  # Core interfaces and adapters
│   │   ├── graph_interface.py
│   │   ├── addis_ababa_adapter.py
│   │   ├── graph_model.py
│   │   ├── location_model.py
│   │   └── networkx_graph_adapter.py
│   ├── services/              # Business logic services
│   │   ├── generic_pathfinding_service.py
│   │   └── visualization_service.py
│   └── shared/                # Shared utilities
│       ├── constraints/       # Path constraints
│       ├── calculators/      # Path calculations
│       └── utils/            # Common utilities
├── docs/                      # Essential documentation
│   ├── README.md
│   ├── ARCHITECTURE.md
│   └── ASTAR_IMPLEMENTATION_COMPLETE.md
├── cache/                     # Map data cache
└── config/                    # Configuration files
```

## Database Schema

The system uses a graph-based data structure rather than traditional relational databases:

### Graph Model
- **Nodes**: Geographic coordinates and location metadata
- **Edges**: Road connections with distance weights
- **Properties**: Road types, speed limits, traffic conditions

### Location Database
```python
LOCATIONS = {
    "Bole International Airport": (8.9806, 38.7997),
    "Meskel Square": (9.0105, 38.7866),
    "Piassa": (9.0345, 38.7429),
    # ... 50+ predefined locations
}
```

## System Requirements

### Hardware Requirements
- **CPU**: 4+ cores for optimal performance
- **Memory**: 8GB+ RAM for large city maps
- **Storage**: 2GB+ for map cache
- **Network**: Stable internet for OSM data updates

### Automated Testing
```yaml
# Example CI workflow
name: Path Finder Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/
      - name: Test GUI
        run: timeout 10 python gui_pathfinder.py
```

### Performance Considerations
- **Memory Usage**: O(V + E) complexity for large graphs
- **Processing Speed**: <2 seconds for city-scale routes
- **Caching**: Local map cache for faster subsequent runs
- **Scalability**: Supports graphs with 10,000+ nodes

## Security & Data Protection

### Privacy Features
- **Location Privacy**: User locations processed in memory only
- **Data Storage**: Local cache management
- **API Usage**: Respectful external service usage
- **No Personal Data**: No collection of personal information

### Data Sources
- **OpenStreetMap**: Open data with proper attribution
- **Local Cache**: Stored map data for offline use
- **Public APIs**: No authentication required

## Logging & Performance Monitoring

### Log Configuration
```python
import logging

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Performance Metrics
- **Algorithm Execution Time**: Track path calculation speed
- **Memory Usage**: Monitor memory consumption
- **Cache Performance**: Cache hit rates and efficiency
- **GUI Response**: Interface responsiveness
- **Error Tracking**: Exception logging and reporting

### Key Performance Indicators
- **Path Calculation Speed**: <2 seconds for city-scale routes
- **Memory Efficiency**: <1GB for typical operations
- **Success Rate**: High path finding success rate
- **User Experience**: Smooth interface interactions

## Contributing Guidelines

### Development Standards
1. **Code Style**: Follow PEP 8 Python standards
2. **Testing**: Minimum 80% code coverage required
3. **Documentation**: Update README for new features
4. **Branching**: feature/branch-name for new features
5. **Commits**: Conventional commit messages

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request with description
6. Code review and merge

### Code Review Checklist
- [ ] Tests pass for new functionality
- [ ] Documentation is updated
- [ ] Code follows project standards
- [ ] No security vulnerabilities
- [ ] Performance impact assessed

## Versioning & Changelog

### Version Strategy
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Major**: Breaking changes or new algorithms
- **Minor**: New features or improvements
- **Patch**: Bug fixes and security updates

### Changelog Format
```
## [2.0.0] - 2024-01-15
### Added
- A* algorithm with heuristic search
- Interactive GUI with zoom/pan
- Improved architecture

### Changed
- Improved memory efficiency by 40%
- Updated visualization system

### Fixed
- Memory leaks in large graph processing
- GUI freezing during path calculation
```

## Support & Resources

### Getting Help
- **Documentation**: Check this README and `/docs` folder
- **Issues**: Report bugs via GitHub issues
- **Community**: Join discussions in GitHub forums

### External Resources
- **OpenStreetMap**: https://www.openstreetmap.org/
- **NetworkX Documentation**: https://networkx.org/
- **OSMnx Documentation**: https://osmnx.readthedocs.io/

---

## Quick Start Guide

```bash
# 1. Clone and setup
git clone <repository_url>
cd BFS-Searching-Algorithm\(2nd trial\)
pip install -r requirements.txt

# 2. Launch GUI
python gui_pathfinder.py

# 3. Find your first route
- Select "Bole International Airport" as start
- Select "Meskel Square" as destination
- Choose "A*" algorithm for optimal path
- Click "Find Path" and view results!

# 4. Explore features
- Try different algorithms (BFS, DFS, A*)
- Test with various location pairs
- Use zoom and pan in visualization
- Compare path lengths and exploration patterns
```

**This comprehensive path finding system provides efficient routing algorithms with visualization capabilities for urban navigation applications!** 
