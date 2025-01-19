import random

def uniform_selection(population):
    """
    Effectue une sélection uniforme sur la population donnée en générant des nombres aléatoires.

    Args:
        population (list): Liste des individus de la population.

    Returns:
        list: Population sélectionnée après application de la sélection uniforme.
    """
    # Taille de la population
    N = len(population)

    # Générer les nombres aléatoires entre 0 et 1
    random_numbers = [random.random() for _ in range(N)]

    # Calcul des intervalles pour chaque individu
    intervals = [(i / N, (i + 1) / N) for i in range(N)]

    # Population sélectionnée
    selected_population = []

    for r in random_numbers:
        for i, (lower, upper) in enumerate(intervals):
            if lower <= r < upper:
                selected_population.append(population[i])
                break

    return selected_population