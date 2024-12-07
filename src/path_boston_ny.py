# Importing necessary libraries
import heapq
import folium


# Graph structure
class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, from_node, to_node, weight):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, weight))


# Dijkstra's algorithm implementation
def dijkstra(graph, start_node, end_node):
    pq = []
    heapq.heappush(pq, (0, start_node))  # (cumulative weight, current node)
    shortest_paths = {start_node: (None, 0)}  # node: (previous node, cumulative weight)

    while pq:
        current_weight, current_node = heapq.heappop(pq)

        # If we've reached the destination
        if current_node == end_node:
            break

        for neighbor, weight in graph.edges.get(current_node, []):
            new_weight = current_weight + weight
            if (
                neighbor not in shortest_paths
                or new_weight < shortest_paths[neighbor][1]
            ):
                shortest_paths[neighbor] = (current_node, new_weight)
                heapq.heappush(pq, (new_weight, neighbor))

    # Reconstruct the shortest path
    path, total_weight = [], shortest_paths.get(end_node, (None, float("inf")))[1]
    node = end_node
    while node:
        path.append(node)
        next_node = shortest_paths[node][0]
        node = next_node
    path.reverse()

    return path, total_weight


# Function to calculate weight of an edge
def calculate_weight(
    distance,
    speed_limit,
    traffic_multiplier=1,
    weather_multiplier=1,
    traffic_lights=False,
):
    base_time = distance / speed_limit  # Base time (hours)
    weight = base_time * traffic_multiplier * weather_multiplier
    if traffic_lights:
        weight *= 1.1  # Add 10% penalty for traffic lights
    return weight


# Create the graph
def create_static_graph():
    graph = Graph()

    # Add edges (Example: Boston -> Hartford -> New York), modify with static data
    # Format: (distance in miles, speed limit in mph, traffic multiplier, weather multiplier, traffic lights)
    routes = [
        ("Boston", "Providence", 50.9, 65, 1.2, 1, False),
        ("Boston", "Worcester", 47.4, 65, 1.2, 1, False),
        ("Springfield", "Hartford", 26.9, 65, 1.2, 1, False),
        ("Worcester", "Springfield", 52.6, 65, 1.2, 1, False),
        ("Worcester", "Hartford", 62.5, 65, 1.2, 1, False),
        ("Worcester", "Providence", 39.5, 65, 1.2, 1, False),
        ("Providence", "Hartford", 86.4, 55, 1.2, 1, False),
        ("Providence", "New Haven", 103.0, 55, 1.2, 1, False),
        ("Hartford", "New Haven", 39.0, 55, 1.2, 1, False),
        ("New Haven", "New York", 81.6, 55, 1.2, 1, False),
    ]

    for from_city, to_city, distance, speed_limit, traffic, weather, lights in routes:
        weight = calculate_weight(distance, speed_limit, traffic, weather, lights)
        graph.add_edge(from_city, to_city, weight)
        graph.add_edge(to_city, from_city, weight)  # Assuming roads are bidirectional

    return graph


if __name__ == "__main__":
    # Main function to demonstrate the optimizer
    graph = create_static_graph()
    start_city = "Boston"
    destination_city = "New York"

    # Calculating shortest route
    path, total_time = dijkstra(graph, start_city, destination_city)

    # Displaying the results
    results = {
        "Optimized Path": " -> ".join(path),
        "Total Travel Time (hours)": f"{total_time:.2f}",
    }
    print(results)

    # Main function to demonstrate the optimizer
    graph = create_static_graph()
    start_city = "Boston"
    destination_city = "New York"

    # Calculating shortest route
    path, total_time = dijkstra(graph, start_city, destination_city)

    # --- Visualization using folium ---
    # Sample coordinates (replace with actual coordinates for cities)
    city_coordinates = {
        "Boston": (42.3601, -71.0589),
        "Providence": (41.8240, -71.4128),
        "Worcester": (42.2626, -71.8023),
        "Springfield": (42.1015, -72.5898),
        "Hartford": (41.7637, -72.6851),
        "New Haven": (41.3083, -72.9279),
        "New York": (40.7128, -74.0060),
    }

    # Create the map centered around the starting city
    map_osm = folium.Map(location=city_coordinates[start_city], zoom_start=7)

    # Add markers for each city on the path
    for city in path:
        if city in city_coordinates:
            folium.Marker(location=city_coordinates[city], popup=city).add_to(map_osm)

    # Draw the route on the map
    for i in range(len(path) - 1):
        if path[i] in city_coordinates and path[i + 1] in city_coordinates:
            folium.PolyLine(
                locations=[city_coordinates[path[i]], city_coordinates[path[i + 1]]],
                color="blue",
                weight=2.5,
                opacity=1,
            ).add_to(map_osm)

    # Save the map as html.
    map_osm.save("src/Boston_NY.html")
