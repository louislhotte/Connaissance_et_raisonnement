import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
solvability_data = pd.read_csv('solvability_data.csv').values

# Create a DataFrame
data = pd.DataFrame({
    'num_clients': [data[0] for data in solvability_data],
    'num_livreurs': [data[1] for data in solvability_data],
    'max_time': [data[2] for data in solvability_data],
    'solvability_rate': [data[3] for data in solvability_data]
})

# Set up the matplotlib figure
plt.figure(figsize=(18, 12))

# --- 1. Simple Plots: Solvability Rate vs Each Variable (Averaged Over the Other Two) ---

# Plot 1: Solvability Rate vs Number of Clients (Averaged Over num_livreurs and max_time)
plt.subplot(2, 3, 1)
avg_solvability_clients = data.groupby('num_clients')['solvability_rate'].mean()
sns.lineplot(x=avg_solvability_clients.index, y=avg_solvability_clients.values, marker='o')
plt.title('Solvability Rate vs Number of Clients\n(Averaged Over Num Livreurs and Max Time)')
plt.xlabel('Number of Clients')
plt.ylabel('Solvability Rate')
plt.grid(True)

# Plot 2: Solvability Rate vs Number of Livreurs (Averaged Over num_clients and max_time)
plt.subplot(2, 3, 2)
avg_solvability_livreurs = data.groupby('num_livreurs')['solvability_rate'].mean()
sns.lineplot(x=avg_solvability_livreurs.index, y=avg_solvability_livreurs.values, marker='o')
plt.title('Solvability Rate vs Number of Livreurs\n(Averaged Over Num Clients and Max Time)')
plt.xlabel('Number of Livreurs')
plt.ylabel('Solvability Rate')
plt.grid(True)

# Plot 3: Solvability Rate vs Max Time (Averaged Over num_clients and num_livreurs)
plt.subplot(2, 3, 3)
avg_solvability_time = data.groupby('max_time')['solvability_rate'].mean()
sns.lineplot(x=avg_solvability_time.index, y=avg_solvability_time.values, marker='o')
plt.title('Solvability Rate vs Max Time\n(Averaged Over Num Clients and Num Livreurs)')
plt.xlabel('Max Time')
plt.ylabel('Solvability Rate')
plt.grid(True)

# --- 2. Heatmaps: Solvability Rate vs Pairs of Variables (Averaged Over the Third) ---

# Heatmap 1: Solvability Rate vs Number of Clients and Number of Livreurs (Averaged Over max_time)
plt.subplot(2, 3, 4)
heatmap_data_clients_livreurs = data.groupby(['num_clients', 'num_livreurs'])['solvability_rate'].mean().unstack()
sns.heatmap(heatmap_data_clients_livreurs, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Solvability Rate vs Num Clients and Num Livreurs\n(Averaged Over Max Time)')
plt.xlabel('Number of Livreurs')
plt.ylabel('Number of Clients')

# Heatmap 2: Solvability Rate vs Number of Livreurs and Max Time (Averaged Over num_clients)
plt.subplot(2, 3, 5)
heatmap_data_livreurs_time = data.groupby(['num_livreurs', 'max_time'])['solvability_rate'].mean().unstack()
sns.heatmap(heatmap_data_livreurs_time, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Solvability Rate vs Num Livreurs and Max Time\n(Averaged Over Num Clients)')
plt.xlabel('Max Time')
plt.ylabel('Number of Livreurs')

# Heatmap 3: Solvability Rate vs Number of Clients and Max Time (Averaged Over num_livreurs)
plt.subplot(2, 3, 6)
heatmap_data_clients_time = data.groupby(['num_clients', 'max_time'])['solvability_rate'].mean().unstack()
sns.heatmap(heatmap_data_clients_time, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Solvability Rate vs Num Clients and Max Time\n(Averaged Over Num Livreurs)')
plt.xlabel('Max Time')
plt.ylabel('Number of Clients')

# Adjust layout
plt.tight_layout()

# Save the plots
plt.savefig('solvability_visualization.png')

# Show the plots
plt.show()

