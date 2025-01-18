import matplotlib.pyplot as plt

# Data for comparison
instances = ['A-n32-k5', 'A-n45-k6', 'B-n50-k7']
algorithm1 = [784, 1325, 2048]
algorithm2 = [800, 1350, 2100]

# Bar chart for Total Distance
x = range(len(instances))
plt.bar(x, algorithm1, width=0.4, label='Algorithm 1', color='blue', align='center')
plt.bar(x, algorithm2, width=0.4, label='Algorithm 2', color='orange', align='edge')

# Formatting
plt.xlabel('Instances')
plt.ylabel('Total Distance')
plt.title('Comparison of Total Distance')
plt.xticks(x, instances)
plt.legend()
plt.show()
