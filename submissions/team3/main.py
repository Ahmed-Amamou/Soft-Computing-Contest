import copy
import sys
import os

from population_initiale import generate_multiple_solutions
from selection_par_tournoi import tournament_selection
from best_solution import get_best_solution
from mutation import mutate_population


# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from template_code.read_instances import read_instance

from template_code.verify_solution import verify_solution
import math







if __name__ == "__main__":
    # Example: Reading an instance
    instance_path = "../../data/A/A-n32-k5.vrp"
    instance_data = read_instance(instance_path)
    nodes = instance_data["nodes"]
    print("Le nombre de villes est: ", instance_data["dimension"])
    print("Les villes à visiter sont les suivants:")
    for node_id, (x, y) in nodes.items():
        print("Node ID: ", node_id, ", Coordinates: (", x, ",", y, ")")
    individus = 12  # nb d'individus dans la population
    # Nombre d'itérations
    n = 700 # Exemple : 100 itérations

    # Génération de la population initiale
    populationInitiale = generate_multiple_solutions(individus, instance_data)

    # Trouver la meilleure solution initiale
    Sbest1, fitness = get_best_solution(populationInitiale, instance_data)
    Sbest = copy.deepcopy(Sbest1)
    print("Sbest initial:", Sbest, "\n fitness:", fitness)
    new_fitness = 0
    # Boucle pour n itérations
    for iteration in range(n):
        print(f"\n--- Iteration {iteration + 1} ---")

        # Sélection par tournoi
        populationSelectionneeParTournoi = tournament_selection(populationInitiale, instance_data)

        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationSelectionneeParTournoi, instance_data)
        SbestList = list(new_Sbest)
        print("Sbestbest           ",Sbest)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness
        print("Sbest après tournoi:", Sbest, "\n fitness:", fitness)

        # Croisement à un point

        #populationCroiseeAUnPoint = generate_offspring(populationSelectionneeParTournoi, instance_data["demands"],instance_data["capacity"],nodes.keys,1)
        populationCroiseeAUnPoint=populationSelectionneeParTournoi
        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationCroiseeAUnPoint, instance_data)
        SbestList = list(new_Sbest)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness = new_fitness
        print("Sbest après croisement:", Sbest, "\n fitness:", fitness)

        # Mutation de la population
        populationAvecMutation = mutate_population(populationCroiseeAUnPoint)
        # Mettre à jour Sbest uniquement si une meilleure solution est trouvée
        new_Sbest, new_fitness = get_best_solution(populationAvecMutation, instance_data)
        SbestList=list(new_Sbest)
        if new_fitness < fitness:  # Si la nouvelle solution est meilleure
            Sbest = copy.deepcopy(new_Sbest)
            fitness=new_fitness

        print("S après mutation:", SbestList, "\n fitness:", new_fitness)
        print(verify_solution(instance_data, SbestList[0]))
        print("Sbest après mutation:", Sbest, "\n fitness:", fitness)
        print("saleeem",verify_solution(instance_data, Sbest[0]))
        # Mettre à jour la population pour la prochaine itération
        populationInitiale = populationAvecMutation

    print("Sbest est",Sbest, "\n fitness:", fitness)

b,f,m=verify_solution(instance_data, Sbest[0])
print(f)
print(verify_solution(instance_data,Sbest[0]))

