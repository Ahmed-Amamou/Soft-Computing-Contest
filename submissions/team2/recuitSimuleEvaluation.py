import os
import random
import sys
import statistics
import time

# Add the path of the 'template_code' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../template_code')))
from read_instances import read_instance
from verify_solution import verify_solution
from recuitSimuleImpl import simulated_annealing, format_solution

def parse_solution_file(solution_path):
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

def load_optimal_solution(solution_path):
    optimal_routes, optimal_cost = parse_solution_file(solution_path)
    return optimal_cost

def calculate_proximity(optimal_cost, generated_cost):
    proximity = (abs(optimal_cost - generated_cost) / optimal_cost) * 100
    return proximity

def evaluate_algorithm(data_path, sa_fn, solution_path, initial_temp=1000, final_temp=5, alpha=0.99, max_iterations=100):
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
                    instance_data = read_instance(instance_path)
                    nodes, demands, capacity = instance_data["nodes"], instance_data["demands"], instance_data["capacity"]
                    print(f"Instance data loaded for {filename}")

                    optimal_routes, optimal_cost = parse_solution_file(solution_file)
                    print(f"Optimal cost loaded: {optimal_cost}")

                except Exception as e:
                    print(f"Error reading instance {filename}: {e}")
                    continue

                instance_results = {
                    'initial_temps': {},
                }

                for init_temp in [initial_temp]:
                    costs = []
                    valid_solutions = 0
                    exec_times = []
                    proximities = []
                    total_simulations = 5

                    for _ in range(total_simulations):
                        try:
                            print(f"Running simulated_annealing with initial_temp={init_temp} for {filename}")

                            start_time = time.time()

                            best_solution, best_cost = sa_fn(
                                instance_data,
                                init_temp,
                                final_temp,
                                alpha,
                                max_iterations
                            )

                            exec_time = time.time() - start_time

                            print(f"Best Solution: {best_solution}, Best Cost: {best_cost}")

                            proximity = calculate_proximity(optimal_cost, best_cost)
                            proximities.append(proximity)
                            print(f"Proximity to optimal solution: {proximity:.2f}%")

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
                            print(f"Error during simulated_annealing or validation for {filename}, initial_temp={init_temp}: {e}")
                            continue

                    if costs:
                        initial_cost = costs[0]
                        instance_results['initial_temps'][init_temp] = {
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
                        print(f"No costs recorded for {filename} with initial_temp={init_temp}")

                results[filename] = instance_results

    print("Final evaluation results:", results)
    return results

def display_results(results):
    for instance, instance_results in results.items():
        print(f"\nInstance: {instance}")
        for init_temp, metrics in instance_results['initial_temps'].items():
            print(f"  Initial Temperature: {init_temp}")
            print(f"    Average Cost: {metrics['average_cost']:.2f}")
            print(f"    Min Cost: {metrics['min_cost']:.2f}")
            print(f"    Max Cost: {metrics['max_cost']:.2f}")
            print(f"    Valid Solutions: {metrics['valid_percentage']:.2f}%")
            print(f"    Average Execution Time: {metrics['average_execution_time']:.4f} seconds")
            print(f"    Average Proximity: {metrics['average_proximity']:.2f}%")
            print(f"    Diversity: {metrics['diversity']:.2f}")
            print(f"    Convergence Rate: {metrics['convergence_rate']:.2f}%")










def evaluate_one_instance(instance_path, sa_fn, solution_path, initial_temp=1000, final_temp=5, alpha=0.99, max_iterations=100, total_simulations=0):
    try:
        # Load instance data
        instance_data = read_instance(instance_path)
        nodes, demands, capacity = instance_data["nodes"], instance_data["demands"], instance_data["capacity"]
        print(f"Instance data loaded for {instance_path}")

        # Load optimal solution data
        optimal_routes, optimal_cost = parse_solution_file(solution_path)
        print(f"Optimal cost loaded: {optimal_cost}")

    except Exception as e:
        print(f"Error loading instance or solution data: {e}")
        return None

    results = {
        'initial_temp': initial_temp,
        'costs': [],
        'valid_solutions': 0,
        'exec_times': [],
        'proximities': [],
        'diversity': 0,
        'convergence_rate': 0,
    }

    for simulation in range(total_simulations):
        try:
            print(f"Running simulation {simulation + 1}/{total_simulations} with initial_temp={initial_temp}")

            start_time = time.time()

            # Run simulated annealing
            best_solution, best_cost = sa_fn(
                instance_data,
                initial_temp,
                final_temp,
                alpha,
                max_iterations
            )

            is_feasible, violations, details = verify_solution(instance_data, best_solution)

            # Format and display the solution
            formatted_solution = format_solution(best_solution)
            print(formatted_solution)
            print(f"Cost {best_cost}")


            exec_time = time.time() - start_time

            print(f"Simulation {simulation + 1}: Best Solution = {best_solution}, Best Cost = {best_cost}")

            # Calculate proximity
            proximity = calculate_proximity(optimal_cost, best_cost)
            print(f"Proximity to optimal: {proximity:.2f}%")

            # Verify solution validity
            is_valid, _, _ = verify_solution(
                instance_data,
                best_solution
            )
            print(f"Solution validity: {is_valid}")

            # Store results
            results['costs'].append(best_cost)
            results['exec_times'].append(exec_time)
            results['proximities'].append(proximity)

            if is_valid:
                results['valid_solutions'] += 1

        except Exception as e:
            print(f"Error during simulation {simulation + 1}: {e}")
            continue

    # Calculate summary statistics
    if results['costs']:
        initial_cost = results['costs'][0]
        results.update({
            'average_cost': statistics.mean(results['costs']),
            'min_cost': min(results['costs']),
            'max_cost': max(results['costs']),
            'valid_percentage': (results['valid_solutions'] / total_simulations) * 100,
            'average_execution_time': statistics.mean(results['exec_times']),
            'average_proximity': statistics.mean(results['proximities']),
            'diversity': statistics.variance(results['costs']) if len(results['costs']) > 1 else 0,
            'convergence_rate': ((initial_cost - min(results['costs'])) / initial_cost * 100)
        })

    print(f"Evaluation for instance {instance_path} completed:\n", results)
    return results


if __name__ == "__main__":
    instance_file = "../../data/B/B-n44-k7.vrp"  
    solution_file = "../../data/B/B-n44-k7.sol"

    results = evaluate_one_instance(
        instance_path=instance_file,
        sa_fn=simulated_annealing,
        solution_path=solution_file,
        initial_temp=1000,
        final_temp=5,
        alpha=0.99,
        max_iterations=100,
        total_simulations=4
    )

    print("Evaluation Results:")
    display_results({'single_instance': {'initial_temps': {1000: results}}})
