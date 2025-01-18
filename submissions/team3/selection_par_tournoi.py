import random
import math

# Fonction pour calculer la distance entre deux points
def distance(point_a, point_b):
    return math.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)

# Fonction pour calculer la distance totale d'une solution (route)
def calculate_total_distance(truck_routes, nodes):
    total_distance = 0
    for route in truck_routes:
        for i in range(len(route) - 1):
            node_a = route[i]
            node_b = route[i + 1]
            # Assurez-vous que node_a et node_b sont des IDs de nœuds individuels, pas des listes
            x1, y1 = nodes[node_a]  # coordonnées pour node_a
            x2, y2 = nodes[node_b]  # coordonnées pour node_b
            total_distance += distance((x1, y1), (x2, y2))  # Calculez la distance entre les nœuds
    return total_distance

# Fonction pour vérifier si une solution respecte les contraintes de capacité
def check_feasibility(route, demands, truck_capacity):
    current_load = 0
    for customer in route:
        if customer == 0:
            continue  # Ignorer le dépôt
        current_load += demands[customer]
        if current_load > truck_capacity:
            return False
    return True

# Fonction pour évaluer la fitness d'une solution
def evaluate_fitness(truck_routes, truck_capacities, demands, nodes):
    total_distance = 0
    total_penalty = 0

    # Calcule la distance totale pour tous les camions
    for i, route in enumerate(truck_routes):
        truck_capacity = truck_capacities[i]  # Capacité du camion i
        # Vérifier si la solution est faisable pour ce camion
        if not check_feasibility(route, demands, truck_capacity):
            total_penalty += 1  # Ajouter une pénalité si la capacité est dépassée
        else:
            total_distance += calculate_total_distance([route], nodes)  # Calculer la distance pour ce camion

    # Pénaliser davantage les solutions non faisables en augmentant la valeur de la fitness
    if total_penalty > 0:
        total_distance += 1000 * total_penalty  # Pénalité pour les solutions non faisables

    return total_distance

# Fonction de sélection par tournoi
# Fonction de sélection par tournoi stochastique
def stochastic_tournament_selection(population, demands, nodes, probability_of_strong=0.7):
    """
    Effectue une sélection par tournoi stochastique pour générer une nouvelle population.

    :param population: Liste de solutions possibles (chromosomes), chaque solution est un tuple (truck_routes, truck_capacities).
    :param demands: Liste des demandes pour chaque nœud.
    :param truck_capacities: Liste des capacités de camions.
    :param nodes: Dictionnaire des coordonnées des nœuds.
    :param probability_of_strong: Probabilité qu'un meilleur individu soit sélectionné (entre 0.7 et 1.0).
    :return: Nouvelle population après la sélection.
    """
    new_population = []
    random.shuffle(population)  # Mélanger la population pour des paires aléatoires

    # Former les paires successives
    for i in range(0, len(population), 2):
        if i + 1 >= len(population):
            # Si la population est impaire, ignorer le dernier individu non apparié
            break

        # Obtenir les deux individus de la paire
        individual1 = population[i]
        individual2 = population[i + 1]

        # Calculer la fitness des deux individus
        fitness1 = evaluate_fitness(individual1[0], individual1[1], demands, nodes)
        fitness2 = evaluate_fitness(individual2[0], individual2[1], demands, nodes)

        # Déterminer le gagnant en fonction de la probabilité de victoire
        if fitness1 < fitness2:
            strong, weak = individual1, individual2
        else:
            strong, weak = individual2, individual1

        # Probabilité de sélectionner le plus fort
        if random.random() < probability_of_strong:
            new_population.append(strong)
        else:
            new_population.append(weak)

    return new_population