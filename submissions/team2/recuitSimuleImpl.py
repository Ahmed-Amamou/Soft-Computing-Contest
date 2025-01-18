import math
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from template_code.read_instances import read_instance
from template_code.verify_solution import verify_solution
from template_code.verify_solution import euclidean_distance


def calculate_cost(solution, nodes):
    """Calculates the total cost of a CVRP solution."""
    cost = 0
    depot = 0
    for route in solution:
        prev_node = depot
        for node in route:
            cost += euclidean_distance(nodes[prev_node], nodes[node])
            prev_node = node
        cost += euclidean_distance(nodes[prev_node], nodes[depot])
    return cost


def generate_initial_solution(num_customers, num_vehicles, capacity, demands):
    """Generates an initial random solution for CVRP."""
    customers = list(range(1, num_customers + 1))
    random.shuffle(customers)
    solution = []
    for _ in range(num_vehicles):
        route = []
        route_capacity = 0
        while customers and (route_capacity + demands[customers[0]] <= 100):
            customer = customers.pop(0)
            route.append(customer)
            route_capacity += demands[customer]
        solution.append(route)

    if customers: 
        solution.append(customers)

    return solution


def perturb_solution(solution):
    """Creates a new solution by perturbing the current one."""
    new_solution = [route[:] for route in solution]

    # Select two random routes and swap a customer between them
    route1, route2 = random.sample(range(len(new_solution)), 2)
    if new_solution[route1] and new_solution[route2]:
        customer1 = random.choice(new_solution[route1])
        customer2 = random.choice(new_solution[route2])

        new_solution[route1].remove(customer1)
        new_solution[route2].remove(customer2)
        new_solution[route1].append(customer2)
        new_solution[route2].append(customer1)

    return new_solution


def simulated_annealing(instance_data, initial_temp, final_temp, alpha, max_iterations):
    """Solves CVRP using simulated annealing."""
    nodes = instance_data["nodes"]
    demands = instance_data["demands"]
    capacity = instance_data["capacity"]
    num_vehicles = instance_data["trucks"]
    num_customers = len(demands)-1
    print(num_customers)
   

    current_solution = generate_initial_solution(num_customers, num_vehicles, capacity, demands)
    current_cost = calculate_cost(current_solution, nodes)

    best_solution = current_solution
    best_cost = current_cost
    temperature = initial_temp

    while temperature > final_temp:
        for _ in range(max_iterations):
            new_solution = perturb_solution(current_solution)
            is_feasible, total_cost, message = verify_solution(instance_data, new_solution)
            if not is_feasible:
                # print(is_feasible,total_cost,message)
                continue

            new_cost = calculate_cost(new_solution, nodes)
            cost_diff = new_cost - current_cost

            if cost_diff < 0 or random.random() < math.exp(-cost_diff / temperature):
                current_solution = new_solution
                current_cost = new_cost
                temperature *= alpha
                print(f"Current Solution: {current_solution}, Current Cost: {current_cost}, Temperature: {temperature}")

                if current_cost < best_cost:
                    best_solution = current_solution
                    best_cost = current_cost

            if temperature < final_temp:
                break

    return best_solution, best_cost


def format_solution(solution):
    """Formats the solution into a readable string format."""
    formatted_routes = []
    for i, route in enumerate(solution):
        formatted_routes.append(f"Route #{i + 1}: {' '.join(map(str, route))}")
    return "\n".join(formatted_routes)

if __name__ == "__main__":
    # Example usage
    file_path = "../../data/B/B-n34-k5.vrp"  
    instance_data = read_instance(file_path)

    initial_temp = 1000
    final_temp = 5
    alpha = 0.99
    max_iterations = 100

    best_solution, best_cost = simulated_annealing(
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


    if is_feasible:
        print("The final solution is feasible.")
    else:
        print("The final solution is NOT feasible.")
        print("Violations:", violations)
        print("Details:", details)