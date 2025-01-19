import random


def crossover(parent1, parent2, demands, capacity, all_cities, depot):
    """
    Performs the Order Crossover (OX) on two parents to generate two children.
    """
    truck_routes1, _ = parent1
    truck_routes2, _ = parent2

    # Flatten the routes (excluding depots)
    parent1_sequence = [city for route in truck_routes1 for city in route if city != depot]
    parent2_sequence = [city for route in truck_routes2 for city in route if city != depot]

    # Perform OX crossover
    size = len(parent1_sequence)
    start, end = sorted(random.sample(range(size), 2))

    # Initialize child sequences
    child1_sequence = [None] * size
    child2_sequence = [None] * size

    # Copy segments from parents to children
    child1_sequence[start:end] = parent1_sequence[start:end]
    child2_sequence[start:end] = parent2_sequence[start:end]

    # Fill remaining positions
    fill_remaining(child1_sequence, parent2_sequence)
    fill_remaining(child2_sequence, parent1_sequence)

    # Convert back to routes
    child1_routes = split_into_routes(child1_sequence, demands, capacity, depot)
    child2_routes = split_into_routes(child2_sequence, demands, capacity, depot)

    return (child1_routes, None), (child2_routes, None)


def fill_remaining(child_sequence, parent_sequence):
    """
    Fills the None positions in the child sequence with cities from the parent sequence,
    maintaining order and avoiding duplicates.
    """
    used_cities = set(city for city in child_sequence if city is not None)

    for city in parent_sequence:
        if city not in used_cities:
            # Find the next empty position
            for i in range(len(child_sequence)):
                if child_sequence[i] is None:
                    child_sequence[i] = city
                    used_cities.add(city)
                    break


def split_into_routes(sequence, demands, capacity, depot):
    """
    Splits a sequence of cities into feasible routes based on truck capacity.
    """
    routes = []
    current_route = []
    current_load = 0

    for city in sequence:
        city_demand = demands.get(city, 0)

        # If adding this city exceeds the truck's capacity, start a new route
        if current_load + city_demand > capacity:
            if current_route:
                routes.append(current_route)
            current_route = []
            current_load = 0

        # Add the city to the current route
        current_route.append(city)
        current_load += city_demand

    # Add the last route if not empty
    if current_route:
        routes.append(current_route)

    # Ensure all routes are valid
    resultat = []
    for sous_liste in routes:
        nettoyee = []
        for element in sous_liste:
            if element is not None:
                nettoyee.append(element)
        resultat.append(nettoyee)
    while len(resultat) < 5:
        resultat.append([])
    routes = resultat
    return routes


def generate_offspring(population, demands, capacity, all_cities, depot):
    """
    Generates a new population by performing crossover on pairs of individuals.
    """
    new_population = []

    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i + 1]
        child1, child2 = crossover(parent1, parent2, demands, capacity, all_cities, depot)
        new_population.extend([child1, child2])

    return new_population


