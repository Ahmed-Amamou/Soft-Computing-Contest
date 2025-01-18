import math
import os
import sys
from read_instances import read_instance
from verify_solution import verify_solution
from verify_solution import euclidean_distance

def greedy_cvrp(nodes, demands, capacity):
    """
    Solves the CVRP using a greedy heuristic approach.

    Args:
        nodes (dict): Node coordinates as {node_id: (x, y)}.
        demands (dict): Node demands as {node_id: demand}.
        capacity (int): Vehicle capacity.

    Returns:
        list: Routes for each vehicle.
    """
    unvisited = set(demands.keys()) - {0}  # Exclude the depot (node 0)
    routes = []
    depot = 0

    while unvisited:
        current_capacity = capacity
        current_route = []
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
            current_route.append(next_node)
            current_capacity -= demands[next_node]
            unvisited.remove(next_node)
            current_node = next_node

        routes.append(current_route)

    return routes


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


if __name__ == "__main__":
    # Example usage
    file_path ="../data/A/A-n33-k5.vrp"  # Adjust the path to your .vrp file
    instance_data = read_instance(file_path)

    # Parse instance data
    nodes = instance_data["nodes"]
    demands = instance_data["demands"]
    capacity = instance_data["capacity"]

    # Solve the CVRP using the greedy heuristic
    routes = greedy_cvrp(nodes, demands, capacity)
    cost = calculate_cost(routes, nodes)

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
