import pandas as pd
import re

input_file = r"C:\Users\bouka\OneDrive\Bureau\soft comp\Soft-Computing-Contest\excelConversion\inputs\rechercheLocaleOutputB.txt"
output_file = "rechercheLocaleOutputB.xlsx"

data = {
    "File": [],
    "Best Cost": [],
    "Verification Result": [],
    "Execution Time": [],
}

with open(input_file, "r") as file:
    lines = [line.strip() for line in file if line.strip()]  

    for i in range(0, len(lines), 5):  
        try:
            print(f"Processing lines {i + 1} to {i + 4}:")
            print(lines[i:i+4])

            file_line = lines[i]
            cost_line = lines[i + 1]
            verification_line = lines[i + 2]
            execution_line = lines[i + 3]
            
            file_match = re.search(r"File: (.+)", file_line)
            cost_match = re.search(r"Best Cost: (.+)", cost_line)
            verification_match = re.search(r"Verification Result: (.+)", verification_line)
            execution_match = re.search(r"Execution Time: (.+)", execution_line)
            
            if file_match and cost_match and verification_match and execution_match:
                file_name = file_match.group(1)
                best_cost = float(cost_match.group(1))
                verification_result = verification_match.group(1)
                execution_time = float(re.search(r"([\d.]+)", execution_match.group(1)).group(1))  
                
                data["File"].append(file_name)
                data["Best Cost"].append(best_cost)
                data["Verification Result"].append(verification_result)
                data["Execution Time"].append(execution_time)
            else:
                print(f"Skipping malformed record starting at line {i + 1}")
                print(f"Matches: file_match={file_match}, cost_match={cost_match}, verification_match={verification_match}, execution_match={execution_match}")
        except IndexError:
            print(f"Skipping incomplete record starting at line {i + 1}")

df = pd.DataFrame(data)

df.to_excel(output_file, index=False)

print(f"Data successfully written to {output_file}")
