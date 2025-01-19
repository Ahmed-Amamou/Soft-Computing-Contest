import math
import random

from calculer_distance import distance


def tournament_selection(population, instance_data, victory_probability=0.8):

    nodes = instance_data["nodes"]
    demands = instance_data["demands"]
    capacity = instance_data["capacity"]

    def eval_solution(solution):
        truck_routes, _ = solution
        total_distance = 0
        for route in truck_routes:
            for i in range(len(route) - 1):
                total_distance += distance(nodes[route[i]], nodes[route[i + 1]])
        return total_distance

    # Mélanger la population pour créer des paires aléatoires
    random.shuffle(population)
    new_population = []

    for i in range(0, len(population) - 1, 2):
        # Former une paire
        individual1 = population[i]
        individual2 = population[i + 1]

        # Calculer la distance totale pour chaque individu
        fitness1 = eval_solution(individual1)
        fitness2 = eval_solution(individual2)

        # Identifier le gagnant et le perdant
        if fitness1 < fitness2:
            winner, loser = individual1, individual2
        else:
            winner, loser = individual2, individual1

        # Probabilité stochastique pour choisir le gagnant
        if random.random() < victory_probability:
            new_population.append(winner)
        else:
            new_population.append(loser)

    # Si la population initiale contient un nombre impair d'individus, ajouter le dernier individuellement
    if len(population) % 2 == 1:
        new_population.append(population[-1])

    return new_population
