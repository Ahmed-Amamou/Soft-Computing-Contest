import pandas as pd
import re

input_file = r"C:\Users\bouka\OneDrive\Bureau\soft comp\Soft-Computing-Contest\excelConversion\inputs\RecuitSimuleOutputA.txt"
output_file = "RecuitSimuleOutputB.xlsx"

data = {
    "File": [],
    "Route 1": [],
    "Route 2": [],
    "Route 3": [],
    "Route 4": [],
    "Route 5": [],
    "Route 6": [],
    "Cost": [],
    "Final Solution": [],
    "Execution Time": [],
}

with open(input_file, "r") as file:
    lines = [line.strip() for line in file if line.strip()]

    for i in range(0, len(lines), 10):
        try:
            file_line = lines[i]
            route1_line = lines[i + 1]
            route2_line = lines[i + 2]
            route3_line = lines[i + 3]
            route4_line = lines[i + 4]
            route5_line = lines[i + 5]
            route6_line = lines[i + 6]
            cost_line = lines[i + 7]
            final_solution_line = lines[i + 8]
            execution_line = lines[i + 9]
            
            file_match = re.search(r"File: (.+)", file_line)
            route1_match = re.search(r"Route #1: (.+)", route1_line)
            route2_match = re.search(r"Route #2: (.+)", route2_line)
            route3_match = re.search(r"Route #3: (.+)", route3_line)
            route4_match = re.search(r"Route #4: (.+)", route4_line)
            route5_match = re.search(r"Route #5: (.+)", route5_line)
            route6_match = re.search(r"Route #6: (.+)", route6_line)
            cost_match = re.search(r"Cost: (.+)", cost_line)
            final_solution_match = re.search(r"The final solution is (.+)", final_solution_line)
            execution_match = re.search(r"Execution time: (.+)", execution_line)
            
            if file_match and cost_match and route1_match and final_solution_match and execution_match:
                file_name = file_match.group(1)
                route1 = route1_match.group(1) if route1_match else None
                route2 = route2_match.group(1) if route2_match else None
                route3 = route3_match.group(1) if route3_match else None
                route4 = route4_match.group(1) if route4_match else None
                route5 = route5_match.group(1) if route5_match else None
                route6 = route6_match.group(1) if route6_match else None
                cost = float(cost_match.group(1)) if cost_match else None
                final_solution = final_solution_match.group(1)
                execution_time = float(re.search(r"([\d.]+)", execution_match.group(1)).group(1)) if execution_match else None
                
                data["File"].append(file_name)
                data["Route 1"].append(route1)
                data["Route 2"].append(route2)
                data["Route 3"].append(route3)
                data["Route 4"].append(route4)
                data["Route 5"].append(route5)
                data["Route 6"].append(route6)
                data["Cost"].append(cost)
                data["Final Solution"].append(final_solution)
                data["Execution Time"].append(execution_time)
            else:
                print(f"Skipping malformed record starting at line {i + 1}")
                print(f"Matches: file_match={file_match}, cost_match={cost_match}, execution_match={execution_match}")
        except IndexError:
            print(f"Skipping incomplete record starting at line {i + 1}")

df = pd.DataFrame(data)
df.to_excel(output_file, index=False)
print(f"Data successfully written to {output_file}")
