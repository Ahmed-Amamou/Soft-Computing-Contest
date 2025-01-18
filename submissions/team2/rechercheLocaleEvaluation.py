import os
import random
import statistics
import time
from functions import  parse_vrp_file
from rechercheLocaleImpl import local_search
# Extraction des routes et coût optimal
def parse_solution_file(solution_path):
    """
    Parse le fichier .sol pour obtenir les routes et le coût optimal.
    """
    optimal_cost = None
    optimal_routes = []

    with open(solution_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Route #"):
                route = list(map(int, line.split()[2:]))
                optimal_routes.append(route)
            elif line.startswith("Cost"):
                optimal_cost = int(line.split()[1])

    return optimal_routes, optimal_cost

# Chargement de la solution optimale à partir du fichier
def load_optimal_solution(solution_path):
    """
    Charge et renvoie la solution optimale depuis le fichier.
    """
    optimal_routes, optimal_cost = parse_solution_file(solution_path)
    return optimal_cost

def calculate_proximity(optimal_cost, generated_cost):
    proximity = (abs(optimal_cost - generated_cost) / optimal_cost) * 100
    return proximity

# Évaluation de l'algorithme de recherche locale
def evaluate_local_search(data_path, solution_path, max_iterations=100, num_simulations=5):
    results = {}
    print(f"Evaluating files in directory: {data_path}")
    # Parcours de toutes les instances dans le répertoire
    for root, dirs, files in os.walk(data_path):  
        print(f"Checking directory: {root}")
        print(f"Files found: {files}")
        
        for filename in files:
            if filename.endswith('.vrp'):
                instance_path = os.path.join(root, filename)
                solution_file = instance_path.replace('.vrp', '.sol')
                print(f"Processing instance file: {filename}")

                try:
                    # Lecture des données de l'instance
                    node_coords, demands, capacity, depot_coords = parse_vrp_file(instance_path)
                    print(f"Instance data loaded for {filename}")
                    
                    # Chargement de la solution optimale
                    optimal_routes, optimal_cost = parse_solution_file(solution_file)
                    print(f"Optimal cost loaded: {optimal_cost}")
                    
                except Exception as e:
                    print(f"Error reading instance {filename}: {e}")
                    continue

                # Initialisation des résultats de l'instance
                instance_results = {
                    'local_search': {
                        'costs': [],
                        'exec_times': [],
                        'proximities': [],
                        'valid_solutions': 0,
                    }
                }

                for _ in range(num_simulations):  # Nombre de simulations par instance
                    try:
                        print(f"Running local_search for {filename}")
                        
                        # Mesure du temps d'exécution
                        start_time = time.time()

                        # Exécution de la recherche locale
                        best_solution, best_cost = local_search(node_coords, demands, capacity, max_iterations, depot_coords)
                        
                        exec_time = time.time() - start_time  

                        print(f"Best Solution: {best_solution}, Best Cost: {best_cost}")

                        # Calcul de la proximité de la solution par rapport à la solution optimale
                        proximity = calculate_proximity(optimal_cost, best_cost)
                        print(f"Proximity to optimal solution: {proximity:.2f}%")

                        # Enregistrement des résultats
                        instance_results['local_search']['costs'].append(best_cost)
                        instance_results['local_search']['exec_times'].append(exec_time)
                        instance_results['local_search']['proximities'].append(proximity)

                        # Validation de la solution
                        if best_cost <= optimal_cost * 1.1:  # Tolérance de 10% par rapport à la solution optimale
                            instance_results['local_search']['valid_solutions'] += 1

                    except Exception as e:
                        print(f"Error during local_search for {filename}: {e}")
                        continue
                
                # Calcul des métriques pour l'instance
                if instance_results['local_search']['costs']:
                    instance_results['local_search']['average_cost'] = statistics.mean(instance_results['local_search']['costs'])
                    instance_results['local_search']['min_cost'] = min(instance_results['local_search']['costs'])
                    instance_results['local_search']['max_cost'] = max(instance_results['local_search']['costs'])
                    instance_results['local_search']['average_exec_time'] = statistics.mean(instance_results['local_search']['exec_times'])
                    instance_results['local_search']['average_proximity'] = statistics.mean(instance_results['local_search']['proximities'])
                    instance_results['local_search']['valid_percentage'] = (instance_results['local_search']['valid_solutions'] / num_simulations) * 100
                else:
                    print(f"No costs recorded for {filename}")

                results[filename] = instance_results

    print("Final evaluation results:", results)
    return results

# Affichage des résultats de l'évaluation
def display_local_results(results):
    for instance, instance_results in results.items():
        print(f"\nInstance: {instance}")
        for algorithm, metrics in instance_results.items():
            print(f"  Algorithm: {algorithm}")
            print(f"    Average Cost: {metrics['average_cost']:.2f}")
            print(f"    Min Cost: {metrics['min_cost']:.2f}")
            print(f"    Max Cost: {metrics['max_cost']:.2f}")
            print(f"    Average Execution Time: {metrics['average_exec_time']:.4f} seconds")
            print(f"    Average Proximity: {metrics['average_proximity']:.2f}%")
            print(f"    Valid Solutions: {metrics['valid_percentage']:.2f}%")

# Exemple d'utilisation
if __name__ == "__main__":
    # Chemin vers les données et les solutions optimales
    data_path = "C:/Soft-Computing-Contest/data/A/"
    solution_path = "C:/Soft-Computing-Contest/data/A/A-n32-k5.sol"
    
    # Paramètres d'évaluation
    max_iterations = 100
    num_simulations = 5
    
    # Évaluation de l'algorithme de recherche locale
    results = evaluate_local_search(data_path, solution_path, max_iterations, num_simulations)
    
    # Affichage des résultats
    display_local_results(results)