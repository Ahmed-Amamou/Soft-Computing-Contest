import math
import random

from calculer_distance import distance


def stochastic_remainder_selection(population, instance_data):
    nodes = instance_data["nodes"]

    def eval_solution(solution):
        truck_routes, _ = solution
        total_distance = 0
        for route in truck_routes:
            for i in range(len(route) - 1):
                total_distance += distance(nodes[route[i]], nodes[route[i + 1]])
        return total_distance

    # Calculer le fitness pour chaque individu et normaliser les probabilités
    fitness_values = [eval_solution(ind) for ind in population]
    max_fitness = max(fitness_values) + 1  # Ajouter 1 pour éviter des probabilités nulles
    probabilities = [(max_fitness - f) for f in fitness_values]
    total_prob = sum(probabilities)
    probabilities = [p / total_prob for p in probabilities]

    # Phase 1 : Ajouter la partie entière des individus à la nouvelle population
    new_population = []
    remainders = []
    for i, individual in enumerate(population):
        E_i = len(population) * probabilities[i]
        copies = math.floor(E_i)
        new_population.extend([individual] * copies)
        remainders.append(E_i - copies)

    # Phase 2 : Utiliser les restes pour compléter la population
    while len(new_population) < len(population):
        for i, individual in enumerate(population):
            if len(new_population) >= len(population):
                break
            if random.random() < remainders[i]:
                new_population.append(individual)

    return new_population
