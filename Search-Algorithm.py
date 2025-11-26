from collections import deque
import heapq
import osmnx as ox
import networkx as nx

class OSMCityMap:
    def __init__(self, city_name="Addis Ababa, Ethiopia"):
        print("Loading OSM data for Addis Ababa...")
        self.graph = ox.graph_from_place(city_name, network_type='drive')
        self.heuristics = {}
        self.locations = {}
    
    def get_nearest_node(self, place_name):
        try:
            location = ox.geocode(place_name)
            return ox.nearest_nodes(self.graph, location[1], location[0])
        except:
            return None
    
    def get_neighbors(self, node_id):
        return list(self.graph.neighbors(node_id))
    
    def get_edge_distance(self, node1, node2):
        try:
            return self.graph[node1][node2][0]['length']
        except:
            return float('inf')
    
    def get_heuristic(self, location):
        return self.heuristics.get(location, float('inf'))
    
    def location_exists(self, location):
        return location in self.locations
    
    def calculate_path_distance(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.get_edge_distance(path[i], path[i+1])
        return total_distance

class SearchAlgorithm:
    def __init__(self, city_map):
        self.city_map = city_map
        self.all_paths = []
    
    def bfs(self, start, goal):
        start_node = self.city_map.locations[start]
        goal_node = self.city_map.locations[goal]
        
        if start_node == goal_node:
            return [start], 0
        
        queue = deque([(start_node, [start_node], 0)])
        visited = set()
        best_distance = float('inf')
        optimal_paths = []
        
        while queue:
            current, path, distance = queue.popleft()
            
            if current in visited and distance > best_distance:
                continue
                
            visited.add(current)
            
            if current == goal_node:
                if distance < best_distance:
                    best_distance = distance
                    optimal_paths = [[start] + path[1:]]
                elif distance == best_distance:
                    optimal_paths.append([start] + path[1:])
                continue
            
            if distance >= best_distance:
                continue
            
            for neighbor in self.city_map.get_neighbors(current):
                if neighbor not in path:
                    edge_distance = self.city_map.get_edge_distance(current, neighbor)
                    new_distance = distance + edge_distance
                    queue.append((neighbor, path + [neighbor], new_distance))
        
        self.all_paths = optimal_paths
        return optimal_paths[0] if optimal_paths else None, best_distance
    
    def dfs(self, start, goal):
        start_node = self.city_map.locations[start]
        goal_node = self.city_map.locations[goal]
        
        if start_node == goal_node:
            return [start], 0
        
        stack = [(start_node, [start_node], 0)]
        visited = set()
        best_distance = float('inf')
        optimal_paths = []
        
        while stack:
            current, path, distance = stack.pop()
            
            if current in visited and distance > best_distance:
                continue
                
            visited.add(current)
            
            if current == goal_node:
                if distance < best_distance:
                    best_distance = distance
                    optimal_paths = [[start] + path[1:]]
                elif distance == best_distance:
                    optimal_paths.append([start] + path[1:])
                continue
            
            if distance >= best_distance:
                continue
            
            for neighbor in self.city_map.get_neighbors(current):
                if neighbor not in path:
                    edge_distance = self.city_map.get_edge_distance(current, neighbor)
                    new_distance = distance + edge_distance
                    stack.append((neighbor, path + [neighbor], new_distance))
        
        self.all_paths = optimal_paths
        return optimal_paths[0] if optimal_paths else None, best_distance
    
    def greedy_search(self, start, goal):
        start_node = self.city_map.locations[start]
        goal_node = self.city_map.locations[goal]
        
        if start_node == goal_node:
            return [start], 0
        
        priority_queue = [(0, start_node, [start_node], 0)]
        visited = set()
        best_distance = float('inf')
        optimal_paths = []
        
        while priority_queue:
            heuristic_value, current, path, distance = heapq.heappop(priority_queue)
            
            if current in visited and distance > best_distance:
                continue
                
            visited.add(current)
            
            if current == goal_node:
                if distance < best_distance:
                    best_distance = distance
                    optimal_paths = [[start] + path[1:]]
                elif distance == best_distance:
                    optimal_paths.append([start] + path[1:])
                continue
            
            if distance >= best_distance:
                continue
            
            for neighbor in self.city_map.get_neighbors(current):
                if neighbor not in path:
                    edge_distance = self.city_map.get_edge_distance(current, neighbor)
                    new_distance = distance + edge_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor, path + [neighbor], new_distance))
        
        self.all_paths = optimal_paths
        return optimal_paths[0] if optimal_paths else None, best_distance

def create_addis_ababa_map():
    city_map = OSMCityMap()
    
    key_places = [
        "Bole International Airport, Addis Ababa",
        "Meskel Square, Addis Ababa", 
        "Piassa, Addis Ababa",
        "Mekanisa, Addis Ababa",
        "Kazanchis, Addis Ababa",
        "Arada, Addis Ababa",
        "Lideta, Addis Ababa",
        "Gulele, Addis Ababa",
        "Nefas Silk Lafto, Addis Ababa",
        "Bole Bulbula, Addis Ababa"
    ]
    
    print("Mapping locations to OSM nodes...")
    for place in key_places:
        node_id = city_map.get_nearest_node(place)
        if node_id:
            city_map.locations[place] = node_id
            print(f"✓ {place} -> Node {node_id}")
        else:
            print(f"✗ Failed to find: {place}")
    
    return city_map

def display_path(path, distance, algorithm_name):
    if path is None:
        print(f"{algorithm_name}: No path found!")
        return
    
    print(f"\n{algorithm_name} - Optimal Path:")
    print(f"Distance: {distance:.2f} km")
    print("Route: " + " -> ".join(path))
    print(f"Number of stops: {len(path) - 1}")

def get_user_location(city_map, prompt):
    print(f"\n{prompt}")
    print("Available locations:")
    locations = list(city_map.locations.keys())
    for i, place in enumerate(locations, 1):
        print(f"{i}. {place}")
    
    while True:
        try:
            choice = input("Enter number (1-" + str(len(locations)) + "): ").strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(locations):
                    return locations[index]
            print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

def get_locations_from_user(city_map):
    print("\n=== SELECT LOCATIONS ===")
    locations = list(city_map.locations.keys())
    
    print("Available locations:")
    for i, place in enumerate(locations, 1):
        print(f"{i}. {place}")
    
    print("\nSelect your start and destination:")
    start_choice = input("Enter START location number: ").strip()
    goal_choice = input("Enter DESTINATION location number: ").strip()
    
    try:
        start_index = int(start_choice) - 1
        goal_index = int(goal_choice) - 1
        
        if 0 <= start_index < len(locations) and 0 <= goal_index < len(locations):
            return locations[start_index], locations[goal_index]
        else:
            print("Invalid selection. Please try again.")
            return get_locations_from_user(city_map)
    except ValueError:
        print("Please enter valid numbers.")
        return get_locations_from_user(city_map)

def handle_constraints(search_algorithm, start, goal):
    print("\n=== CONSTRAINT HANDLING ===")
    
    if start == goal:
        print("Constraint: Initial and goal states are the same!")
        print(f"You are already at your destination: {start}")
        return True
    
    return True


def main():
    print("=== CITY PATH FINDER - ADDIS ABABA ===")
    print("Available Search Algorithms: BFS, DFS, Greedy Search")
    
    city_map = create_addis_ababa_map()
    search_algorithm = SearchAlgorithm(city_map)
    
    while True:
        try:
            start, goal = get_locations_from_user(city_map)
            
            if not handle_constraints(search_algorithm, start, goal):
                continue
            
            print(f"\nSearching for path from {start} to {goal}...")
            
            bfs_path, bfs_distance = search_algorithm.bfs(start, goal)
            dfs_path, dfs_distance = search_algorithm.dfs(start, goal)
            greedy_path, greedy_distance = search_algorithm.greedy_search(start, goal)
            
            display_path(bfs_path, bfs_distance, "BFS")
            display_path(dfs_path, dfs_distance, "DFS")
            display_path(greedy_path, greedy_distance, "Greedy Search")
            
            if len(search_algorithm.all_paths) > 1:
                print(f"\nNote: Found {len(search_algorithm.all_paths)} optimal paths with the same distance!")
                print("All paths are equally optimal.")
            
            another = input("\nFind another path? (y/n): ").strip()
            if another.lower() != 'y':
                break
            
        except KeyboardInterrupt:
            print("\nExiting program...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()