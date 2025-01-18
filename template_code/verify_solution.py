import math

def euclidean_distance(node1, node2):
    """
    Computes the Euclidean distance between two nodes.

    Args:
        node1 (tuple): Coordinates of the first node (x, y).
        node2 (tuple): Coordinates of the second node (x, y).

    Returns:
        float: Euclidean distance.
    """
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

def verify_solution(instance_data, solution):
    """
    Verifies the feasibility of a CVRP solution and computes its cost.

    Args:
        instance_data (dict): Parsed .vrp instance data.
        solution (list of lists): Solution routes, e.g., [[1, 2, 3], [4, 5, 6]].

    Returns:
        tuple: (is_feasible (bool), total_cost (float), message (str))
    """
    nodes = instance_data["nodes"]
    demands = instance_data["demands"]
    capacity = instance_data["capacity"]
    depot = 0
    required_trucks = instance_data.get("trucks", None)
    optimal_value = instance_data.get("optimal_value", None)

    visited = set()  # To track visited customers
    total_cost = 0

    # Check if the number of trucks matches the required number
    if required_trucks is not None and len(solution) != required_trucks:
        return False, 0, (
            f"Invalid solution: Expected {required_trucks} trucks, but got {len(solution)}."
        )

    for route in solution:
        load = 0
        route_cost = 0

        # Start from the depot
        prev_node = depot

        for node in route:
            if node in visited:
                return False, 0, f"Invalid solution: Customer {node} was visited more than once."


            visited.add(node)
            load += demands[node]
            if load > capacity:
                return (
                    False,
                    0,
                    f"Invalid solution: Capacity exceeded on route {route}. Current load is {load}, capacity is {capacity}."
                )

            route_cost += euclidean_distance(nodes[prev_node], nodes[node])
            prev_node = node

        # Return to the depot
        route_cost += euclidean_distance(nodes[prev_node], nodes[depot])
        total_cost += route_cost

    # Check if all customers were visited exactly once
    all_customers = set(nodes.keys()) - {0}  # All customers (excluding depot and last node)
    all_customers.remove(max(all_customers))  # Remove the last node
    if visited != all_customers:
        unvisited = all_customers - visited
        return False, 0, f"Invalid solution: Not all customers were visited. Missing: {unvisited}"

    # If we reach here, the solution is feasible
    if optimal_value is not None:
        diff_from_optimal = total_cost - optimal_value
        message = (
            f"Congratulations! Your solution is valid and the total cost is {total_cost:.2f}."
        )
    else:
        message = f"Congratulations! Your solution is valid with a total cost of {total_cost:.2f}."

    return True, total_cost, message
