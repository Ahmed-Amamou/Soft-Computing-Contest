import matplotlib.pyplot as plt

# Data for comparison
instances = ['A-n32-k5', 'A-n45-k6', 'B-n50-k7']
algorithm1 = [784, 1325, 2048]  # Total distance by Algorithm 1
algorithm2 = [800, 1350, 2100]  # Total distance by Algorithm 2

# Calculate Gap (%)
gap_percentage = [
    ((algo2 - algo1) / algo1) * 100
    for algo1, algo2 in zip(algorithm1, algorithm2)
]

# Plotting the Gap (%) Line Chart
plt.figure(figsize=(8, 6))
plt.plot(instances, gap_percentage, marker='o', linestyle='-', color='blue', label='Gap (%)')

# Add titles and labels
plt.title('Performance Gap Between Algorithms', fontsize=14)
plt.xlabel('Instances', fontsize=12)
plt.ylabel('Gap (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
