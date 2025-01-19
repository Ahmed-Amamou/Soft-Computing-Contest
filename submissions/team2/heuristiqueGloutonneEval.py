import os
import random
import sys
import statistics
import time

# Add the path to the 'template_code' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from template_code.read_instances import read_instance
from template_code.verify_solution import verify_solution

def parse_solution_file(solution_path):
    """
    Parses a .sol file to extract optimal routes and cost.

    Args:
        solution_path (str): Path to the .sol file.

    Returns:
        list: Optimal routes.
        int: Optimal cost.
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

def calculate_proximity(optimal_cost, generated_cost):
    """
    Calculates the proximity of the generated cost to the optimal cost.

    Args:
        optimal_cost (int): Optimal cost.
        generated_cost (float): Generated cost.

    Returns:
        float: Proximity percentage.
    """
    return (abs(optimal_cost - generated_cost) / optimal_cost) * 100

def evaluate_algorithm(data_path, your_method, solution_path, iterations=100, params=[5, 10, 20]):
    results = {}
    print(f"Evaluating files in directory: {data_path}")

    for root, dirs, files in os.walk(data_path):
        for filename in files:
            if filename.endswith('.vrp'):
                instance_path = os.path.join(root, filename)
                solution_file = instance_path.replace('.vrp', '.sol')
                print(f"Processing instance file: {filename}")

                try:
                    instance_data = read_instance(instance_path)
                    nodes, demands, capacity, trucks = (
                        instance_data["nodes"],
                        instance_data["demands"],
                        instance_data["capacity"],
                        instance_data["trucks"],  # Extract the number of trucks
                    )

                    optimal_routes, optimal_cost = parse_solution_file(solution_file)
                    print(f"Optimal cost loaded: {optimal_cost}")
                except Exception as e:
                    print(f"Error reading instance {filename}: {e}")
                    continue

                instance_results = {'parameters': {}}

                for param in params:
                    costs = []
                    valid_solutions = 0
                    exec_times = []
                    proximities = []
                    total_simulations = 5

                    for _ in range(total_simulations):
                        try:
                            start_time = time.time()
                            # Pass the required arguments to your_method
                            best_solution, best_cost = your_method(nodes, demands, capacity, trucks)
                            exec_time = time.time() - start_time

                            proximity = calculate_proximity(optimal_cost, best_cost)
                            proximities.append(proximity)

                            is_valid, _, _ = verify_solution(
                                {'nodes': nodes, 'demands': demands, 'capacity': capacity},
                                best_solution
                            )

                            costs.append(best_cost)
                            exec_times.append(exec_time)

                            if is_valid:
                                valid_solutions += 1
                        except Exception as e:
                            print(f"Error during execution for {filename}, param={param}: {e}")
                            continue

                    if costs:
                        initial_cost = costs[0]
                        instance_results['parameters'][param] = {
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

                results[filename] = instance_results

    print("Final evaluation results:", results)
    return results

def display_results(results):
    """
    Displays the evaluation results.

    Args:
        results (dict): Evaluation results.
    """
    for instance, instance_results in results.items():
        print(f"\nInstance: {instance}")
        for param, metrics in instance_results['parameters'].items():
            print(f"  Parameter: {param}")
            print(f"    Average Cost: {metrics['average_cost']:.2f}")
            print(f"    Min Cost: {metrics['min_cost']:.2f}")
            print(f"    Max Cost: {metrics['max_cost']:.2f}")
            print(f"    Valid Solutions: {metrics['valid_percentage']:.2f}%")
            print(f"    Average Execution Time: {metrics['average_execution_time']:.4f} seconds")
            print(f"    Average Proximity: {metrics['average_proximity']:.2f}%")
            print(f"    Diversity: {metrics['diversity']:.2f}")
            print(f"    Convergence Rate: {metrics['convergence_rate']:.2f}%")