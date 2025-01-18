from functions import calculate_distance, calculate_total_cost, create_initial_solution, neighborhood_solution, parse_vrp_file , print_solution
import os
# Recherche Locale
def local_search(node_coords, demands, capacity, max_iterations, depot_coords):
    nodes = list(node_coords.keys())  
    nodes.append(-1)  # Ajout du dépôt
    node_coords[-1] = depot_coords
    node_index_map = {node: idx for idx, node in enumerate(nodes)}
    # Création de la matrice des distances
    distance_matrix = [[calculate_distance(node_coords[nodes[i]], node_coords[nodes[j]]) 
                        if nodes[i] != -1 and nodes[j] != -1 else
                        calculate_distance(depot_coords, node_coords[nodes[j]]) if nodes[i] == -1 else
                        calculate_distance(node_coords[nodes[i]], depot_coords)
                        for j in range(len(nodes))] for i in range(len(nodes))]
    
    # Générer une solution initiale
    initial_solution = create_initial_solution(demands, capacity, distance_matrix,node_index_map)
    best_solution = initial_solution
    best_cost = calculate_total_cost(best_solution, distance_matrix,node_index_map)
    
    # Recherche locale
    for iteration in range(max_iterations):
        # Générer des voisins
        neighbors = neighborhood_solution(best_solution, demands, capacity)
        
        # Trouver le meilleur voisin
        best_candidate = None
        best_candidate_cost = float('inf')
        
        for candidate in neighbors:
            cost = calculate_total_cost(candidate, distance_matrix,node_index_map)
            if cost < best_candidate_cost:
                best_candidate = candidate
                best_candidate_cost = cost
        
        # Mettre à jour la meilleure solution si un meilleur voisin est trouvé
        if best_candidate_cost < best_cost:
            best_solution = best_candidate
            best_cost = best_candidate_cost
            
            print(f"Iteration {iteration}")
            print_solution(best_solution, best_cost)
        else:
            # Si aucun meilleur voisin n'est trouvé, arrêter la recherche
            print(f"Iteration {iteration}: No improvement found. Stopping early.")
            break
    
    return best_solution, best_cost
# Chargement des données
filename = "C:/Soft-Computing-Contest/data/A/A-n32-k5.vrp"
node_coords, demands, capacity, depot_coords = parse_vrp_file(filename)
# Paramètres
max_iterations = 100

# Résolution avec recherche locale
best_solution, best_cost = local_search(node_coords, demands, capacity, max_iterations, depot_coords)

# Affichage des résultats
print_solution(best_solution, best_cost)

