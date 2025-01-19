import copy
import sys
import os

from population_initiale import generate_multiple_solutions
from selection_par_tournoi import tournament_selection
from best_solution import get_best_solution
from mutation import mutate_population

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from submissions.team3.croisement_a_un_point import generate_offspring


from template_code.verify_solution import verify_solution

import time

def algorithme_genetique(instance_data):


    nodes = instance_data["nodes"]

    individus = 12  # nb d'individus dans la population
    n = 10000  # Nombre d'itérations

    # Génération de la population initiale
    populationInitiale = generate_multiple_solutions(individus, instance_data)

    # Trouver la meilleure solution initiale
    Sbest1, fitness = get_best_solution(populationInitiale, instance_data)
    Sbest = copy.deepcopy(Sbest1)


    # Mesure du temps d'exécution
    start_time = time.time()  # Démarre le chronomètre

    for iteration in range(n):

        # Sélection par tournoi
        populationSelectionneeParTournoi = tournament_selection(populationInitiale, instance_data)

        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationSelectionneeParTournoi, instance_data)

        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness

        # Croisement à un point
        populationCroiseeAUnPoint = generate_offspring(populationInitiale, instance_data["demands"], instance_data["capacity"], int(instance_data["trucks"]), 0)
        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationCroiseeAUnPoint, instance_data)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness

        # Mutation de la population
        populationAvecMutation = mutate_population(populationCroiseeAUnPoint)
        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationAvecMutation, instance_data)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness
        # Mettre à jour la population pour la prochaine itération
        populationInitiale = populationAvecMutation

    end_time = time.time()  # Arrête le chronomètre

    print("\n--- Résultats finaux ---")
    print("Sbest est:", Sbest[0], "\n fitness:", fitness)
    print(f"Temps total d'exécution de la boucle : {end_time - start_time:.5f} secondes")

    # Validation finale
    b, f, m = verify_solution(instance_data, Sbest[0])
    print("La Solution est: ", b,"\nLe cout total est :", f, m)
    return (Sbest[0])
