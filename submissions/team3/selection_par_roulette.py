import random
import math


def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def roulette_selection(population, instance_data):
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

    fitness_values = []
    total_fitness = 0
    for individual in population:
        fitness = eval_solution(individual)
        fitness_values.append(fitness)
        total_fitness += fitness

    selected_population = []
    for _ in range(len(population)):
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, fitness in enumerate(fitness_values):
            current += fitness
            if current > pick:
                selected_population.append(population[i])
                break

    return selected_population
