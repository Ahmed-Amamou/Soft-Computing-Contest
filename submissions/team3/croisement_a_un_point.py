import random

def fix_routes(truck_routes, demands, capacity, all_cities, depot):
    """
    Corrige les itinéraires des camions en enlevant les villes en double et en ajoutant les villes manquantes.

    Args:
        truck_routes (list): Liste des itinéraires des camions.
        demands (dict): Dictionnaire des demandes pour chaque ville.
        capacity (int): La capacité maximale d'un camion.
        all_cities (set): L'ensemble de toutes les villes (y compris le dépôt).
        depot (int): L'ID du dépôt.

    Returns:
        list: Itinéraires corrigés des camions.
    """
    # Créer un ensemble des villes déjà visitées
    visited_cities = set()
    print(type(all_cities))
    missing_cities = all_cities.copy()  # Assurez-vous que all_cities est un set

    for route in truck_routes:
        # Enlever les villes en double (en ignorant le dépôt)
        for city in route[1:-1]:  # Ignorer le dépôt au début et à la fin
            if city in visited_cities:
                route.remove(city)
            else:
                visited_cities.add(city)

        # Ajouter les villes manquantes
        for city in route[1:-1]:  # Ignorer le dépôt
            if city in missing_cities:
                missing_cities.remove(city)

    # Ajouter les villes manquantes à chaque camion, tout en respectant la capacité
    remaining_capacity = [capacity - sum(demands.get(city, 0) for city in route[1:-1]) for route in truck_routes]
    for route, cap in zip(truck_routes, remaining_capacity):
        # Ajouter les villes manquantes tant qu'il reste de la capacité
        for city in missing_cities.copy():
            if demands.get(city, 0) <= cap:
                route.insert(-1, city)  # Ajouter avant le dépôt
                missing_cities.remove(city)
                cap -= demands.get(city, 0)  # Mettre à jour la capacité restante

    return truck_routes


def crossover(parent1, parent2, demands, capacity, all_cities, depot):
    """
    Effectue un croisement à 1 point entre deux parents pour créer deux enfants,
    avec des corrections sur les routes pour enlever les villes en double et ajouter les villes manquantes.

    Args:
        parent1 (tuple): Première solution (truck_routes, truck_capacities).
        parent2 (tuple): Deuxième solution (truck_routes, truck_capacities).
        demands (dict): Dictionnaire des demandes pour chaque ville.
        capacity (int): La capacité maximale d'un camion.
        all_cities (set): L'ensemble de toutes les villes (y compris le dépôt).
        depot (int): L'ID du dépôt.

    Returns:
        tuple: Deux enfants (child1, child2), où chaque enfant est une solution (truck_routes, truck_capacities).
    """
    # Sélectionner un point de croisement aléatoire pour les routes des camions
    crossover_point = random.randint(1, len(parent1[0]) - 1)  # Point aléatoire entre les camions
    child1_routes = parent1[0][:crossover_point] + parent2[0][crossover_point:]
    child2_routes = parent2[0][:crossover_point] + parent1[0][crossover_point:]

    # Les capacités restent inchangées pour l'instant
    child1_capacities = parent1[1]
    child2_capacities = parent2[1]

    # Corriger les itinéraires des enfants en supprimant les doublons et en ajoutant les villes manquantes
    child1_routes = fix_routes(child1_routes, demands, capacity, all_cities, depot)
    child2_routes = fix_routes(child2_routes, demands, capacity, all_cities, depot)

    return (child1_routes, child1_capacities), (child2_routes, child2_capacities)


def generate_offspring(population, demands, capacity, all_cities, depot):
    """
    Génère une nouvelle population en effectuant un croisement sur chaque paire d'individus.

    Args:
        population (list): La population actuelle de solutions (liste de tuples (truck_routes, truck_capacities)).
        demands (dict): Dictionnaire des demandes pour chaque ville.
        capacity (int): La capacité maximale d'un camion.
        all_cities (set): L'ensemble de toutes les villes (y compris le dépôt).
        depot (int): L'ID du dépôt.

    Returns:
        list: Nouvelle population après croisement (liste de tuples (truck_routes, truck_capacities)).
    """
    new_population = []

    # S'assurer que la population est paire pour faire des croisements
    if len(population) % 2 != 0:
        population.append(population[-1])  # Ajouter un individu supplémentaire si nécessaire

    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i + 1]

        # Effectuer le croisement entre parent1 et parent2
        child1, child2 = crossover(parent1, parent2, demands, capacity, all_cities, depot)

        # Ajouter les enfants à la nouvelle population
        new_population.append(child1)
        new_population.append(child2)

    return new_population
