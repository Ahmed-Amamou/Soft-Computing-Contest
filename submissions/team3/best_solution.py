import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from template_code.verify_solution import verify_solution


def get_best_solution(population, instance_data):


    nodes = instance_data["nodes"]
    demands = instance_data["demands"]


    b,total_distance,m=verify_solution(instance_data,population[0][0])
    best_solution = population[0]
    best_fitness = total_distance

    # Parcourir la population pour trouver la solution avec la distance minimale
    for individual in population[1:]:
        b, total_distance, m = verify_solution(instance_data, individual[0])
        fitness = total_distance
        if fitness < best_fitness:
            best_solution = individual
            best_fitness = fitness

    return [best_solution, best_fitness]
