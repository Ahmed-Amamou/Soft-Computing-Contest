import math
import random

# Calcul de la distance entre deux nœuds
def calculate_distance(node1, node2):
    return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)

# Calcul du coût total d'une solution (routes)
def calculate_total_cost(routes, distance_matrix, node_index_map):
    cost = 0
    depot_index = node_index_map[-1]  
    for route in routes:
        cost += distance_matrix[depot_index][node_index_map[route[0]]]  
        for i in range(len(route) - 1):  
            cost += distance_matrix[node_index_map[route[i]]][node_index_map[route[i + 1]]]
        cost += distance_matrix[node_index_map[route[-1]]][depot_index]  
    return cost

# Création de la solution initiale
def create_initial_solution(demands, capacity, distance_matrix, node_index_map):
    routes = [] 
    unserved_customers = list(demands.keys()) 
    depot_index = node_index_map[-1]  
    current_route = []  
    current_load = 0  
    while unserved_customers:
        current_route = []
        current_load = 0
        current_node = depot_index 
        while unserved_customers:
            nearest_customer = None
            min_distance = float('inf')
            for customer in unserved_customers:
                customer_index = node_index_map[customer]
                if current_load + demands[customer] <= capacity:
                    dist = distance_matrix[current_node][customer_index]
                    if dist < min_distance:
                        min_distance = dist
                        nearest_customer = customer
            if nearest_customer is not None:
                current_route.append(nearest_customer)
                current_load += demands[nearest_customer]
                unserved_customers.remove(nearest_customer)
                current_node = node_index_map[nearest_customer]
            else:
                break  
        if current_route:
            routes.append(current_route)
    return routes

# Fonction de génération des voisins d'une solution
def neighborhood_solution(routes, demands, capacity):

    solutions = set()  

    while len(solutions) < 30:  
        new_routes = [route.copy() for route in routes] 
        route1, route2 = random.sample(new_routes, 2)  

        if route1 and route2:  
            node1 = random.choice(route1)  
            node2 = random.choice(route2)  

            load_route1 = sum(demands[node] for node in route1)
            load_route2 = sum(demands[node] for node in route2)

            if load_route2 + demands[node1] <= capacity:
                route1.remove(node1)
                route2.append(node1)
                solutions.add(tuple(map(tuple, new_routes)))  
                continue  

            if load_route1 + demands[node2] <= capacity:
                route2.remove(node2)
                route1.append(node2)
                solutions.add(tuple(map(tuple, new_routes)))  
                continue  

            load_route1_after = load_route1 - demands[node1] + demands[node2]
            load_route2_after = load_route2 - demands[node2] + demands[node1]

            if load_route1_after <= capacity and load_route2_after <= capacity:
                route1.remove(node1)
                route2.remove(node2)
                route1.append(node2)
                route2.append(node1)
                solutions.add(tuple(map(tuple, new_routes)))  
                continue  

      
        continue

    return [list(map(list, solution)) for solution in solutions]


def parse_vrp_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    node_coords = {}
    demands = {}
    capacity = 0
    depot = None  
    section = None

    for line in lines:
        line = line.strip()
        if line.startswith('CAPACITY'):
            capacity = int(line.split(':')[1].strip())
        elif line.startswith('NODE_COORD_SECTION'):
            section = 'NODE_COORD'
        elif line.startswith('DEMAND_SECTION'):
            section = 'DEMAND'
        elif line.startswith('DEPOT_SECTION'):
            section = 'DEPOT'
        elif line == 'EOF':
            break
        elif section == 'NODE_COORD':
            parts = line.split()
            node_coords[int(parts[0])] = (int(parts[1]), int(parts[2]))
        elif section == 'DEMAND':
            parts = line.split()
            demands[int(parts[0])] = int(parts[1])
        elif section == 'DEPOT':
            if line.isdigit():
                depot = int(line)

    if depot is None or depot not in node_coords:
        raise ValueError("Les coordonnées du dépôt sont introuvables dans le fichier.")

    depot_coords = node_coords[depot]
    return node_coords, demands, capacity, depot_coords

# Fonction d'affichage de la solution 
def print_solution(routes, cost):
    for i, route in enumerate(routes, start=1):
        print(f"Route #{i}: {' '.join(map(str, route))}")
    print(f"Cost {cost}")