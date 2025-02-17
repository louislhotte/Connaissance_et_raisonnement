import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

solvability_data = pd.read_csv('solvability_data.csv').values

# Extract data for plotting
num_clients_list = np.array([data[0] for data in solvability_data])
num_livreurs_list = np.array([data[1] for data in solvability_data])
max_time_list = np.array([data[2] for data in solvability_data])
solvability_rate_list = np.array([data[3] for data in solvability_data])

# Create a figure with subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Solvability Rate Analysis', fontsize=16, fontweight='bold')

# Plot 1: Solvability Rate vs Number of Clients
sc1 = axes[0].scatter(num_clients_list, solvability_rate_list, c=max_time_list, cmap='plasma', alpha=0.8, edgecolor='k')
axes[0].set_xlabel('Number of Clients', fontsize=12)
axes[0].set_ylabel('Solvability Rate', fontsize=12)
axes[0].set_title('Solvability Rate vs Number of Clients', fontsize=14)
cbar1 = fig.colorbar(sc1, ax=axes[0])
cbar1.set_label('Max Time', fontsize=12)

# Add a trend line
slope, intercept, r_value, _, _ = linregress(num_clients_list, solvability_rate_list)
axes[0].plot(num_clients_list, intercept + slope * num_clients_list, 'r--', label=f'Trend (R²={r_value**2:.2f})')
axes[0].legend()

# Plot 2: Solvability Rate vs Number of Livreurs
sc2 = axes[1].scatter(num_livreurs_list, solvability_rate_list, c=max_time_list, cmap='plasma', alpha=0.8, edgecolor='k')
axes[1].set_xlabel('Number of Livreurs', fontsize=12)
axes[1].set_ylabel('Solvability Rate', fontsize=12)
axes[1].set_title('Solvability Rate vs Number of Livreurs', fontsize=14)
cbar2 = fig.colorbar(sc2, ax=axes[1])
cbar2.set_label('Max Time', fontsize=12)

# Add a trend line
slope, intercept, r_value, _, _ = linregress(num_livreurs_list, solvability_rate_list)
axes[1].plot(num_livreurs_list, intercept + slope * num_livreurs_list, 'r--', label=f'Trend (R²={r_value**2:.2f})')
axes[1].legend()

# Plot 3: Solvability Rate vs Max Time
sc3 = axes[2].scatter(max_time_list, solvability_rate_list, c=num_clients_list, cmap='plasma', alpha=0.8, edgecolor='k')
axes[2].set_xlabel('Max Time', fontsize=12)
axes[2].set_ylabel('Solvability Rate', fontsize=12)
axes[2].set_title('Solvability Rate vs Max Time', fontsize=14)
cbar3 = fig.colorbar(sc3, ax=axes[2])
cbar3.set_label('Number of Clients', fontsize=12)

# Add a trend line
slope, intercept, r_value, _, _ = linregress(max_time_list, solvability_rate_list)
axes[2].plot(max_time_list, intercept + slope * max_time_list, 'r--', label=f'Trend (R²={r_value**2:.2f})')
axes[2].legend()

# Adjust layout and show plots
plt.tight_layout()
plt.show()