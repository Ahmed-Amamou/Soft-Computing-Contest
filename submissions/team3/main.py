import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from template_code.read_instances import read_instance
from template_code.verify_solution import verify_solution

import math
import random


def distance(node1, node2):
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def generate_multiple_solutions(n, instance_data):

    solutions = []

    for _ in range(n):
        truck_routes, truck_capacities = generate_random_solution(
            instance_data["nodes"],
            instance_data["dimension"],
            instance_data["trucks"],
            1,  # ID du dépôt
            instance_data["capacity"],
            instance_data["demands"]
        )
        solutions.append((truck_routes, truck_capacities))

    return solutions

# depot : id
def generate_random_solution(nodes, num_nodes, num_trucks, depot, capacity, demands):
    # Initialisation des variables
    truck_routes = [[] for _ in range(num_trucks)]  # Liste des itinéraires des camions
    remaining_nodes = list(nodes.keys())  # Liste des nodes disponibles (tous sauf le dépôt)
    remaining_nodes.remove(depot)  # Retirer le dépôt des nodes à visiter
    truck_capacities = [0] * num_trucks  # Capacité utilisée par chaque camion

    # Mélanger les nodes restantes pour une attribution aléatoire
    random.shuffle(remaining_nodes)

    # Attribution des nodes aux camions
    truck_index = 0

    for node in remaining_nodes:
        # Ignorer le dépôt
        if node == depot:
            continue


        node_demand = demands.get(node, 0)  # Récupérer la demande, par défaut 0 si le nœud n'existe pas dans demands


        # Vérifier si ajouter ce node au camion courant respecte la capacité
        if truck_capacities[truck_index] + node_demand <= capacity:
            truck_routes[truck_index].append(node)
            truck_capacities[truck_index] += node_demand
        else:
            # Passer au camion suivant
            truck_index += 1
            if truck_index >= num_trucks:
                raise ValueError("Nombre de camions insuffisant pour transporter toutes les demandes.")
            # Ajouter le node au prochain camion
            truck_routes[truck_index].append(node)
            truck_capacities[truck_index] += node_demand

    # Ajouter le dépôt au début et retour au dépôt à la fin pour chaque camion
    for i in range(num_trucks):
        if truck_routes[i]:
            truck_routes[i] = [depot] + truck_routes[i] + [depot]

    return truck_routes, truck_capacities


if __name__ == "__main__":
    # Example: Reading an instance
    instance_path = "../../data/A/A-n32-k5.vrp"
    instance_data = read_instance(instance_path)
    print("Le nombre de villes est: ", instance_data["dimension"])
    print("Les villes à visiter sont les suivants:")
    for node_id, (x, y) in instance_data["nodes"].items():
        print("Node ID: ", node_id, ", Coordinates: (", x, ",", y, ")")
    individus = 5  # nb d'individus dans la population
    populationInitiale = generate_multiple_solutions(individus, instance_data)
    for p in populationInitiale:
        print("s:   ",p,"\n")