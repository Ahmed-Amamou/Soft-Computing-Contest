import matplotlib.pyplot as plt

# Data for comparison
instances = ['F-n45-k4', 'F-n72-k4', 'F-n135-k7']
algorithm1_times = [44, 71, 134]  # Execution times for Algorithm 1
algorithm2_times = [4, 4, 7]      # Execution times for Algorithm 2

# Plotting a Box Plot
plt.figure(figsize=(8, 6))
plt.boxplot([algorithm1_times, algorithm2_times], labels=['Algorithm 1', 'Algorithm 2'], patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='blue'),
            medianprops=dict(color='red', linewidth=1.5))

# Add titles and labels
plt.title('Execution Time Variability Between Algorithms', fontsize=14)
plt.ylabel('Execution Time (ms)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Show the Box Plot
plt.tight_layout()
plt.show()

# Optional: Bar Chart for Comparison
x = range(len(instances))  # X-axis positions
bar_width = 0.35

plt.figure(figsize=(8, 6))
plt.bar(x, algorithm1_times, width=bar_width, label='Algorithm 1', color='lightblue')
plt.bar([i + bar_width for i in x], algorithm2_times, width=bar_width, label='Algorithm 2', color='lightgreen')

# Add titles, labels, and legend
plt.title('Execution Time Comparison Between Algorithms', fontsize=14)
plt.xlabel('Instances', fontsize=12)
plt.ylabel('Execution Time (ms)', fontsize=12)
plt.xticks([i + bar_width / 2 for i in x], instances)  # Center the instance labels
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Show the Bar Chart
plt.tight_layout()
plt.show()
