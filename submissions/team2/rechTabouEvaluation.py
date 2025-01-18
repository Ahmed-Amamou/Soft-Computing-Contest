import os
import random
import sys
import statistics
import time

# Ajout explicite du chemin du dossier 'template_code'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../template_code')))
from read_instances import read_instance
from verify_solution import verify_solution

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
    """
    Calcule le pourcentage de proximité de la solution générée par rapport à la solution optimale.
    
    Args:
        optimal_cost (int): Le coût optimal extrait du fichier .sol.
        generated_cost (int): Le coût généré par l'algorithme (tabu search).
    
    Returns:
        float: Le pourcentage de proximité de la solution générée par rapport à la solution optimale.
    """
    proximity = (abs(optimal_cost - generated_cost) / optimal_cost) * 100
    return proximity


def evaluate_algorithm(data_path, tabu_search_fn, solution_path, iterations=100, tabu_tenures=[5, 10, 20]):
    results = {}
    print(f"Evaluating files in directory: {data_path}")

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
                    instance_data = read_instance(instance_path)
                    nodes, demands, capacity = instance_data["nodes"], instance_data["demands"], instance_data["capacity"]
                    depot_coords = nodes[1]  # Supposons que le dépôt est le nœud 1
                    print(f"Instance data loaded for {filename}")
                    
                    # Chargement de la solution optimale
                    optimal_routes, optimal_cost = parse_solution_file(solution_file)
                    print(f"Optimal cost loaded: {optimal_cost}")
                    
                except Exception as e:
                    print(f"Error reading instance {filename}: {e}")
                    continue

                instance_results = {'tabu_tenures': {}}
                for tenure in tabu_tenures:
                    costs = []
                    valid_solutions = 0
                    exec_times = []
                    proximities = []
                    total_simulations = 5

                    for _ in range(total_simulations):
                        
                            print(f"Running tabu_search with tenure={tenure} for {filename}")
                            
                            start_time = time.time()

                            best_solution, best_cost = tabu_search_fn(
                                nodes, demands, capacity, iterations, tenure, depot_coords
                            )
                            
                            exec_time = time.time() - start_time
                            print(f"Best Solution: {best_solution}, Best Cost: {best_cost}")

                            proximity = calculate_proximity(optimal_cost, best_cost)
                            proximities.append(proximity)
                            print(f"Proximity to optimal solution: {proximity:.2f}%")

                            # Vérification de la validité de la solution
                            is_valid, total_cost, message = verify_solution(
                                {'nodes': nodes, 'demands': demands, 'capacity': capacity},
                                best_solution
                            )
                            print(f"Solution validity: {is_valid}")
                            print(f"Verification message: {message}")
                            print(f"Total cost after verification: {total_cost}")

                            if is_valid:
                                costs.append(total_cost)
                                valid_solutions += 1
                            else:
                                print(f"Invalid solution at iteration {_ + 1}, message: {message}")

                            exec_times.append(exec_time)
                    if costs:
                        initial_cost = costs[0]
                        instance_results['tabu_tenures'][tenure] = {
                            'average_cost': statistics.mean(costs),
                            'min_cost': min(costs),
                            'max_cost': max(costs),
                            'valid_percentage': (valid_solutions / total_simulations) * 100,
                            'feasibility_rate': (valid_solutions / total_simulations) * 100,
                            'average_execution_time': statistics.mean(exec_times),
                            'average_proximity': statistics.mean(proximities),
                            'diversity': statistics.variance(costs) if len(costs) > 1 else 0,
                            'convergence_rate': (initial_cost - min(costs)) / initial_cost * 100
                        }
                    else:
                        print(f"No valid solutions recorded for {filename} with tenure={tenure}. Valid Solutions: {valid_solutions}/{total_simulations}")

                results[filename] = instance_results

    print("Final evaluation results:", results)
    return results


def evaluate_algorithm_for_single_instance(instance_path, tabu_search_fn, solution_path, iterations=100, tabu_tenures=[5, 10, 20]):
    """
    Évalue l'algorithme de recherche tabou sur une seule instance et ses paramètres.
    """
    results = {}
    filename = os.path.basename(instance_path)
    print(f"Processing instance file: {filename}")

    try:
        # Lecture des données de l'instance
        instance_data = read_instance(instance_path)
        nodes, demands, capacity = instance_data["nodes"], instance_data["demands"], instance_data["capacity"]
        print(f"Instance data loaded for {filename}")
        
        # Chargement de la solution optimale
        optimal_routes, optimal_cost = parse_solution_file(solution_path)
        print(f"Optimal cost loaded: {optimal_cost}")
        
    except Exception as e:
        print(f"Error reading instance {instance_path}: {e}")
        return {}

    # Initialisation des résultats de l'instance
    instance_results = {
        'tabu_tenures': {},
    }

    for tenure in tabu_tenures:
        costs = []
        valid_solutions = 0
        exec_times = []  # Liste pour stocker les temps d'exécution
        proximities = []  # Liste pour stocker la proximité
        total_simulations = 5  # Total de simulations pour chaque tenure

        for _ in range(total_simulations):  # Nombre de simulations par paramètre
            try:
                print(f"Running tabu_search with tenure={tenure} for {filename}")
                
                # Mesure du temps d'exécution
                start_time = time.time()

                best_solution, best_cost = tabu_search_fn(
                    nodes, demands, capacity, iterations, tenure
                )
                
                exec_time = time.time() - start_time  

                print(f"Best Solution: {best_solution}, Best Cost: {best_cost}")

                # Calcul de la proximité de la solution par rapport à la solution optimale
                proximity = calculate_proximity(optimal_cost, best_cost)
                proximities.append(proximity)
                print(f"Proximity to optimal solution: {proximity:.2f}%")

                # Validation de la solution
                is_valid, _, _ = verify_solution(
                    {'nodes': nodes, 'demands': demands, 'capacity': capacity},
                    best_solution
                )
                print(f"Solution validity: {is_valid}")
                costs.append(best_cost)
                exec_times.append(exec_time)

                if is_valid:
                    valid_solutions += 1
            except Exception as e:
                print(f"Error during tabu_search or validation for {filename}, tenure={tenure}: {e}")
                continue
        
        if costs:
            # Calcul de l'indicateur de diversité et convergence
            initial_cost = costs[0]  # Vous pouvez définir le coût initial comme le premier coût obtenu
            instance_results['tabu_tenures'][tenure] = {
                'average_cost': statistics.mean(costs),
                'min_cost': min(costs),
                'max_cost': max(costs),
                'valid_percentage': (valid_solutions / total_simulations) * 100,
                'feasibility_rate': (valid_solutions / total_simulations) * 100,
                'average_execution_time': statistics.mean(exec_times),
                'average_proximity': statistics.mean(proximities),
                'diversity': statistics.variance(costs) if len(costs) > 1 else 0,
                'convergence_rate': (initial_cost - min(costs)) / initial_cost * 100  # Taux de convergence
            }
        else:
            print(f"No costs recorded for {filename} with tenure={tenure}")

    results[instance_path] = instance_results

    print("Final evaluation results:", results)
    return results

# Afficher des résultats de l'évaluation
def display_results(results):
    """
    Affiche les résultats de l'évaluation.
    
    Args:
        results (dict): Résultats de l'évaluation.
    """
    for instance, instance_results in results.items():
        print(f"\nInstance: {instance}")
        for tenure, metrics in instance_results['tabu_tenures'].items():
            print(f"  Tabu Tenure: {tenure}")
            print(f"    Average Cost: {metrics['average_cost']:.2f}")
            print(f"    Min Cost: {metrics['min_cost']:.2f}")
            print(f"    Max Cost: {metrics['max_cost']:.2f}")
            print(f"    Valid Solutions: {metrics['valid_percentage']:.2f}%")
            print(f"    Average Execution Time: {metrics['average_execution_time']:.4f} seconds")
            print(f"    Average Proximity: {metrics['average_proximity']:.2f}%")
            print(f"    Diversity: {metrics['diversity']:.2f}")
            print(f"    Convergence Rate: {metrics['convergence_rate']:.2f}%")
