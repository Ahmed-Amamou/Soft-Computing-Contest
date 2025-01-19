import random


def crossover(parent1, parent2, demands, capacity, all_cities, depot):
    """
    Performs the Order Crossover (OX) on two parents to generate two children.

    Args:
        parent1 (tuple): First parent solution (truck_routes, truck_capacities).
        parent2 (tuple): Second parent solution (truck_routes, truck_capacities).
        demands (dict): Demands for each city.
        capacity (int): Maximum truck capacity.
        all_cities (set): Set of all cities (including the depot).
        depot (int): The ID of the depot.

    Returns:
        tuple: Two children solutions (truck_routes, truck_capacities).
    """
    truck_routes1, _ = parent1
    truck_routes2, _ = parent2


    # Flatten the routes (excluding depots) for OX crossover
    parent1_sequence = [city for route in truck_routes1 for city in route if city != depot]
    parent2_sequence = [city for route in truck_routes2 for city in route if city != depot]

    # Perform OX crossover
    size = len(parent1_sequence)
    start, end = sorted(random.sample(range(size), 2))

    child1_sequence = [None] * size
    child2_sequence = [None] * size

    # Copy the segment from parent1 to child1 and parent2 to child2
    child1_sequence[start:end] = parent1_sequence[start:end]
    child2_sequence[start:end] = parent2_sequence[start:end]

    # Fill the remaining positions in order from the other parent
    fill_positions(child1_sequence, parent2_sequence, demands, capacity, depot)  # Corrected
    fill_positions(child2_sequence, parent1_sequence, demands, capacity, depot)

    # Convert the sequences back to truck routes
    child1_routes = split_into_routes(child1_sequence, demands, capacity, depot)
    child2_routes = split_into_routes(child2_sequence, demands, capacity, depot)

    # Return the children as new solutions
    return (child1_routes, None), (child2_routes, None)


def fill_positions(child_sequence, parent_sequence, demands, capacity, depot):
    """
    Fills the None positions in the child sequence with the cities from the parent sequence
    while maintaining their order and avoiding duplicates, and ensuring truck capacity is not exceeded.

    Args:
        child_sequence (list): The child sequence with some positions filled.
        parent_sequence (list): The parent sequence to take cities from.
        demands (dict): Demands for each city.
        capacity (int): Maximum truck capacity.
        depot (int): The ID of the depot.
    """
    size = len(child_sequence)
    current_index = 0  # Start at the beginning of the child sequence
    current_load = 0  # Initialize the current load for the truck
    print("child sequence kbal l filling",child_sequence)
    # Initialize a new route with the depot
   # current_route = [depot]
    current_route = []
    for city in parent_sequence:
        if city not in child_sequence:  # Check if the city is already in the child sequence
            # Check if adding the city exceeds the truck's capacity
            city_demand = demands.get(city, 0)  # Get demand for the city

            # If adding the city would exceed capacity, finalize the current route and start a new one
            if current_load + city_demand > capacity:
               # current_route.append(depot)  # Close the current route with the depot
                child_sequence.extend(current_route)  # Add the completed route to the child sequence

                # Start a new route with the depot
              #  current_route = [depot]
                current_route = []
                current_load = 0  # Reset the load for the new route

            # Add the city to the current route
            current_route.append(city)
            current_load += city_demand  # Update the load of the current route

            # Find the next available position to fill in the child sequence
            while child_sequence[current_index] is not None:
                current_index = (current_index + 1) % size

            child_sequence[current_index] = city  # Fill the position in the child sequence

    # After filling positions, close the last route with the depot and add it to the child sequence
  #  current_route.append(depot)
    child_sequence.extend(current_route)


def split_into_routes(sequence, demands, capacity, depot):
    """
    Splits a sequence of cities into feasible routes based on truck capacity,
    ensuring that the truck capacity does not exceed the maximum allowed capacity.

    Args:
        sequence (list): The sequence of cities to split.
        demands (dict): Demands for each city.
        capacity (int): Maximum truck capacity.
        depot (int): The ID of the depot.

    Returns:
        list: List of routes (each route is a list of cities, starting and ending with the depot).
    """
    routes = []  # Initialize the list to store the routes
    current_route = []  # Start the first route with the depot
    current_load = 0  # Initialize the current load to 0

    for city in sequence:
        city_demand = demands.get(city, 0)  # Get the demand for the city (default to 0 if not found)

        # If adding this city would exceed the truck's capacity, finalize the current route
        if current_load + city_demand > capacity:
            #current_route.append(depot)  # Close the current route with the depot
            routes.append(current_route)  # Add the route to the routes list
            current_route = []  # Start a new route with the depot
            current_load = 0  # Reset the load for the new route

        # Add the city to the current route
        current_route.append(city)
        current_load += city_demand  # Update the current load with the city's demand

    # After the loop, ensure the last route is added
   # current_route.append(depot)  # Close the last route with the depot
    routes.append(current_route)  # Add the last route to the routes list
    resultat = []
    for sous_liste in routes:
        nettoyee = []
        for element in sous_liste:
            if element is not None:
                nettoyee.append(element)
        resultat.append(nettoyee)
    while len(resultat)<5:
        resultat.append([])
    routes=resultat
    return routes


def generate_offspring(population, demands, capacity, all_cities, depot):
    """
    Generates a new population by performing crossover on pairs of individuals.

    Args:
        population (list): The current population of solutions (list of tuples).
        demands (dict): Demands for each city.
        capacity (int): Maximum truck capacity.
        all_cities (set): Set of all cities (including the depot).
        depot (int): The ID of the depot.

    Returns:
        list: New population after crossover (list of tuples).
    """
    new_population = []

    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i + 1]

        # Perform crossover between parent1 and parent2
        child1, child2 = crossover(parent1, parent2, demands, capacity, all_cities, depot)

        # Add the children to the new population
        new_population.append(child1)
        new_population.append(child2)

    return new_population