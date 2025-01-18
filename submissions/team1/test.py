def load_vrp_instance(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    
    nodes = []  # Liste pour stocker les coordonnées des nœuds
    is_node_section = False  # Indicateur pour vérifier si on est dans la section des coordonnées

    for line in data:
        line = line.strip()

        # Détecter la section des coordonnées
        if line == "NODE_COORD_SECTION":
            is_node_section = True
            continue
        if line == "EOF":
            break

        if is_node_section:
            # Traiter uniquement les lignes dans la section des coordonnées
            parts = line.split()
            if len(parts) >= 3:  # Vérifier que la ligne contient au moins 3 parties
                try:
                    node_id = int(parts[0])  # Numéro du nœud
                    x_coord = float(parts[1])  # Coordonnée X
                    y_coord = float(parts[2])  # Coordonnée Y
                    nodes.append((node_id, x_coord, y_coord))
                except ValueError:
                    print(f"Ignoring malformed line: {line}")
    
    return nodes

# Exemple d'utilisation
file_path = 'C:/Users/asus/Downloads/Vrp-Set-F/F/F-n72-k4.vrp'
nodes = load_vrp_instance(file_path)
print("Coordonnées des nœuds :", nodes)


import math

def calculate_distance_matrix(nodes):
    num_nodes = len(nodes)
    distance_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                x1, y1 = nodes[i][1], nodes[i][2]
                x2, y2 = nodes[j][1], nodes[j][2]
                distance_matrix[i][j] = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    return distance_matrix

# Example usage
distance_matrix = calculate_distance_matrix(nodes)
print("Distance Matrix:")
for row in distance_matrix:
    print(row)

import matplotlib.pyplot as plt

def plot_nodes(nodes):
    x_coords = [node[1] for node in nodes]
    y_coords = [node[2] for node in nodes]
    plt.scatter(x_coords, y_coords)
    for node in nodes:
        plt.annotate(str(node[0]), (node[1], node[2]))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Node Locations")
    plt.show()

# Example usage
plot_nodes(nodes)

def nearest_neighbor(nodes, distance_matrix, capacity, demands):
    num_nodes = len(nodes)
    visited = [False] * num_nodes
    routes = []
    depot = 0
    visited[depot] = True

    while not all(visited):
        current_route = []
        current_capacity = 0
        current_node = depot

        while True:
            current_route.append(current_node)
            visited[current_node] = True
            next_node = None
            min_distance = float('inf')

            for i in range(num_nodes):
                if not visited[i] and current_capacity + demands[i] <= capacity:
                    if distance_matrix[current_node][i] < min_distance:
                        min_distance = distance_matrix[current_node][i]
                        next_node = i

            if next_node is None:  # No valid next node
                break

            current_node = next_node
            current_capacity += demands[next_node]

        current_route.append(depot)  # Return to the depot
        routes.append(current_route)

    return routes

# Example usage:
capacity = 100  # Example vehicle capacity
demands = [0] * len(nodes)  # Example demands for each node
distance_matrix = calculate_distance_matrix(nodes)
routes = nearest_neighbor(nodes, distance_matrix, capacity, demands)
print("Routes:", routes)
import matplotlib.pyplot as plt

def plot_routes(nodes, routes):
    # Plot all nodes
    x_coords = [node[1] for node in nodes]
    y_coords = [node[2] for node in nodes]
    
    # Plot nodes and label them
    plt.scatter(x_coords, y_coords, c='blue', label="Nodes")
    for node in nodes:
        plt.annotate(str(node[0]), (node[1], node[2]), textcoords="offset points", xytext=(5,5))
    
    # Plot routes
    colors = ['red', 'green', 'purple', 'orange', 'cyan']  # Add more colors if needed
    for idx, route in enumerate(routes):
        route_x = [nodes[node][1] for node in route]
        route_y = [nodes[node][2] for node in route]
        color = colors[idx % len(colors)]
        plt.plot(route_x, route_y, color=color, label=f"Route {idx + 1}")
    
    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")
    plt.title("Vehicle Routing Problem (VRP) Routes")
    plt.legend()
    plt.show()

# Example usage
plot_routes(nodes, routes)
