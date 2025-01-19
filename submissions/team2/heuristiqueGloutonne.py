import math
import os
import sys
from collections import defaultdict

# Add the path to the 'template_code' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from template_code.read_instances import read_instance
from template_code.verify_solution import verify_solution
from template_code.verify_solution import euclidean_distance

def greedy_cvrp(nodes, demands, capacity, trucks):
    """
    Solves the CVRP using a greedy heuristic approach.

    Args:
        nodes (dict): Node coordinates as {node_id: (x, y)}.
        demands (dict): Node demands as {node_id: demand}.
        capacity (int): Vehicle capacity.
        trucks (int): Number of trucks (routes) to use.

    Returns:
        list: Routes for each vehicle.
        float: Total cost of the solution.
    """
    # Exclude the depot (node 0) and the node with the maximum ID
    unvisited = set(demands.keys()) - {0}
    max_id_node = max(unvisited)  # Find the node with the maximum ID
    unvisited.remove(max_id_node)  # Remove the node with the maximum ID

    routes = [[] for _ in range(trucks)]  # Initialize empty routes for all trucks
    depot = 0

    # Assign nodes to routes while respecting capacity constraints
    while unvisited:
        for route in routes:
            if not unvisited:
                break

            current_capacity = capacity
            current_node = depot

            while unvisited:
                # Find the closest unvisited node that fits within the remaining capacity
                next_node = None
                min_distance = float("inf")

                for node in unvisited:
                    if demands[node] <= current_capacity:
                        distance = euclidean_distance(nodes[current_node], nodes[node])
                        if distance < min_distance:
                            min_distance = distance
                            next_node = node

                if not next_node:  # No more nodes can be added to this route
                    break

                # Add the selected node to the route
                route.append(next_node)
                current_capacity -= demands[next_node]
                unvisited.remove(next_node)
                current_node = next_node

    # Ensure all customers are visited
    if unvisited:
        raise ValueError(f"Not all customers were visited. Remaining nodes: {unvisited}")

    # Calculate the total cost of the solution
    cost = calculate_cost(routes, nodes)

    return routes, cost
def calculate_cost(solution, nodes):
    """
    Calculates the total cost of a CVRP solution.

    Args:
        solution (list): List of routes.
        nodes (dict): Node coordinates.

    Returns:
        float: Total cost of the solution.
    """
    cost = 0
    depot = 0
    for route in solution:
        prev_node = depot
        for node in route:
            cost += euclidean_distance(nodes[prev_node], nodes[node])
            prev_node = node
        cost += euclidean_distance(nodes[prev_node], nodes[depot])
    return cost

def format_solution(solution):
    """
    Formats the solution into a readable string format.

    Args:
        solution (list): List of routes.

    Returns:
        str: Formatted solution.
    """
    formatted_routes = []
    for i, route in enumerate(solution):
        formatted_routes.append(f"Route #{i + 1}: {' '.join(map(str, route))}")
    return "\n".join(formatted_routes)

def process_all_vrp_files(data_directory):
    """
    Processes all .vrp files in the specified directory and displays their solutions.

    Args:
        data_directory (str): Path to the directory containing .vrp files.
    """
    # Walk through the data directory
    for root, dirs, files in os.walk(data_directory):
        for filename in files:
            if filename.endswith(".vrp"):
                file_path = os.path.join(root, filename)
                print(f"\nProcessing file: {filename}")

                try:
                    # Read the instance data
                    instance_data = read_instance(file_path)

                    # Parse instance data
                    nodes = instance_data["nodes"]
                    demands = instance_data["demands"]
                    capacity = instance_data["capacity"]
                    trucks = instance_data["trucks"]

                    # Solve the CVRP using the greedy heuristic
                    routes, cost = greedy_cvrp(nodes, demands, capacity, trucks)

                    # Verify the solution
                    is_feasible, violations, details = verify_solution(instance_data, routes)

                    # Output the solution and its cost
                    formatted_routes = format_solution(routes)
                    print(formatted_routes)
                    print(f"Total cost: {cost}")

                    if is_feasible:
                        print("The solution is feasible.")
                    else:
                        print("The solution is NOT feasible.")
                        print("Violations:", violations)
                        print("Details:", details)

                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    # Directory containing the .vrp files
    data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))

    # Process all .vrp files in the directory
    process_all_vrp_files(data_directory)