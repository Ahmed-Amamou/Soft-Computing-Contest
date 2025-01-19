import random


def mutate_solution(truck_routes):
    """
    Effectue une mutation en échangeant deux villes (nœuds) au sein du même camion dans une solution.

    Args:
        truck_routes (list): Liste des itinéraires des camions.

    Returns:
        list: Nouvelle solution après mutation (liste des itinéraires des camions avec deux villes échangées).
    """
    # Choisir un camion aléatoire
    truck_index = random.randint(0, len(truck_routes) - 1)

    # Si le camion a plus d'une ville (excluant le dépôt)
    if len(truck_routes[truck_index][1:-1]) > 2:
        # Sélectionner deux villes au hasard dans le camion

        route = truck_routes[truck_index][1:-1]  # Exclure le dépôt
        city1, city2 = random.sample(route, 2)  # Choisir deux villes différentes

        # Échanger les deux villes
        city1_index = truck_routes[truck_index].index(city1)
        city2_index = truck_routes[truck_index].index(city2)

        # Effectuer l'échange
        truck_routes[truck_index][city1_index], truck_routes[truck_index][city2_index] = truck_routes[truck_index][
            city2_index], truck_routes[truck_index][city1_index]

    return truck_routes


def mutate_population(population):
    """
    Applique une mutation à chaque solution de la population.

    Args:
        population (list): La population actuelle de solutions (liste de tuples (truck_routes, truck_capacities)).

    Returns:
        list: Nouvelle population après mutation (liste de tuples (truck_routes, truck_capacities)).
    """
    new_population = []

    for truck_routes, truck_capacities in population:
        # Appliquer la mutation sur les itinéraires des camions
        mutated_routes = mutate_solution(truck_routes.copy())  # Créer une copie pour ne pas modifier l'original
        new_population.append((mutated_routes, truck_capacities))

    return new_population
