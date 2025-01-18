from functions import calculate_distance, calculate_total_cost, create_initial_solution, neighborhood_solution, print_solution
# from rechTabouEvaluation import parse_solution_file

# Recherche Tabou
def tabu_search(node_coords, demands, capacity, max_iterations, tabu_tenure, depot_coords):
    nodes = list(node_coords.keys())  
    nodes.append(-1)  
    node_coords[-1] = depot_coords
    
    node_index_map = {node: idx for idx, node in enumerate(nodes)}
    
    # Création de la matrice des distances
    distance_matrix = [[calculate_distance(node_coords[nodes[i]], node_coords[nodes[j]]) 
                        if nodes[i] != -1 and nodes[j] != -1 else
                        calculate_distance(depot_coords, node_coords[nodes[j]]) if nodes[i] == -1 else
                        calculate_distance(node_coords[nodes[i]], depot_coords)
                        for j in range(len(nodes))] for i in range(len(nodes))]
    
    # Générer une solution initiale
    initial_solution = create_initial_solution(demands, capacity , distance_matrix, node_index_map)
    best_solution = initial_solution
    best_cost = calculate_total_cost(best_solution, distance_matrix, node_index_map)
    
    # Liste Tabou et suivi des itérations
    tabu_list = []
    tabu_iterations = {}

    for iteration in range(max_iterations):
        neighborhood = []

        neighbors = neighborhood_solution(best_solution, demands, capacity)
        neighborhood.extend(neighbors)

        best_candidate = None
        best_candidate_cost = float('inf')

        for candidate in neighborhood:
            cost = calculate_total_cost(candidate, distance_matrix, node_index_map)
            if (candidate not in tabu_list or iteration - tabu_iterations.get(tuple(map(tuple, candidate)), 0) > tabu_tenure) and cost < best_candidate_cost:
                best_candidate = candidate
                best_candidate_cost = cost

        # Vérification pour éviter l'erreur 'NoneType'
        if best_candidate is not None and best_candidate_cost < best_cost:
            best_solution = best_candidate
            best_cost = best_candidate_cost

  
            tabu_list.append(best_candidate)
            tabu_iterations[tuple(map(tuple, best_candidate))] = iteration

 
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)

    return best_solution, best_cost

# filename = '../../data/A/A-n32-k5.vrp'  
# node_coords, demands, capacity, depot_coords = parse_solution_file(filename)

# # Paramètres
# max_iterations = 100
# tabu_tenure = 10

# Résolution avec recherche Tabou
# best_solution, best_cost = tabu_search(node_coords, demands, capacity, max_iterations, tabu_tenure, depot_coords)

# # Affichage des résultats
# print_solution(best_solution, best_cost)