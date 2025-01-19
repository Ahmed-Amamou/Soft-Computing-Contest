import copy
import sys
import os

from population_initiale import generate_multiple_solutions
from selection_par_tournoi import tournament_selection
from best_solution import get_best_solution
from mutation import mutate_population

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from submissions.team3.croisement_a_un_point import generate_offspring
from submissions.team3.main import algorithme_genetique
from template_code.read_instances import read_instance

from template_code.verify_solution import verify_solution
import math

import time  # Import nécessaire pour la mesure du temps

if __name__ == "__main__":
    # Example: Reading an instance
    instance_path = "../../data/A/A-n32-k5.vrp"
    instance_data = read_instance(instance_path)
    nodes = instance_data["nodes"]
    # print("Le nombre de villes est: ", instance_data["dimension"])
    # print("Les villes à visiter sont les suivants:")
    # for node_id, (x, y) in nodes.items():
    #     print("Node ID: ", node_id, ", Coordinates: (", x, ",", y, ")")
    individus = 20  # nb d'individus dans la population
    n = 10000  # Nombre d'itérations

    # Génération de la population initiale
    populationInitiale = generate_multiple_solutions(individus, instance_data)

    # Trouver la meilleure solution initiale
    Sbest1, fitness = get_best_solution(populationInitiale, instance_data)
    Sbest = copy.deepcopy(Sbest1)
   # print("Sbest initial:", Sbest, "\n fitness:", fitness)
    new_fitness = 0

    # Mesure du temps d'exécution
    start_time = time.time()  # Démarre le chronomètre
   # print(populationInitiale)
    # Boucle pour n itérations
    for iteration in range(n):
       # print(f"\n--- Iteration {iteration + 1} ---")

        # Sélection par tournoi
        populationSelectionneeParTournoi = tournament_selection(populationInitiale, instance_data)

        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationSelectionneeParTournoi, instance_data)
        SbestList = list(new_Sbest)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness
    #    print("Sbest après tournoi:", Sbest, "\n fitness:", fitness)

        # Croisement à un point
        populationCroiseeAUnPoint = generate_offspring(populationInitiale, instance_data["demands"], instance_data["capacity"], list(instance_data["nodes"].keys()), 0)
        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
      #  print("population apres croisement", populationCroiseeAUnPoint)
        new_Sbest, new_fitness = get_best_solution(populationCroiseeAUnPoint, instance_data)
        SbestList = list(new_Sbest)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness
        #print("Sbest après croisement:", Sbest, "\n fitness:", fitness)

        # Mutation de la population
        populationAvecMutation = mutate_population(populationCroiseeAUnPoint)
        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationAvecMutation, instance_data)
        SbestList = list(new_Sbest)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness

      #  print("S après mutation:", SbestList, "\n fitness:", new_fitness)
      #  print(verify_solution(instance_data, SbestList[0]))
       # print("Sbest après mutation:", Sbest, "\n fitness:", fitness)
       # print("saleeem", verify_solution(instance_data, Sbest[0]))
        # Mettre à jour la population pour la prochaine itération
        populationInitiale = populationAvecMutation

    end_time = time.time()  # Arrête le chronomètre

    print("\n--- Résultats finaux ---")
    print("Sbest est:", Sbest[0], "\n fitness:", fitness)
    print(f"Temps total d'exécution de la boucle : {end_time - start_time:.5f} secondes")
    # Validation finale
    b, f, m = verify_solution(instance_data, Sbest[0])
    print("La Solution est: ", b,"\nLe cout total est :", f)
    s=algorithme_genetique(instance_data)
