import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from logic import *
from scipy.stats import linregress


"""
Logic of the problem :
If a deliverer starts a delivery j at time t, he'll be busy for a time = congestion_matrix[j][t]*alpha hours
A deliverer works in shift of 8 hours maximum
"""

global ALPHA
ALPHA = 1/10 # Scaling factor of the congestion (congestion is in range[10, 40])
predictions = pd.read_csv("predictions.csv", delimiter=";")


######### GENERATE DATA #########

# Define parameter ranges
n_clients_range = range(5, 15, 2)
n_livreurs_range = range(2, 6)
max_time_range = range(24, 49, 5)

# Number of instances to generate per parameter combination
num_instances = 3

# Data storage
solvability_data = []

n_problems = len(n_clients_range) * len(n_livreurs_range) * len(max_time_range) * num_instances
problem_count=0
# Iterate through parameter ranges
for num_clients in n_clients_range:
    for num_livreurs in n_livreurs_range:
        for max_time in max_time_range:
            solvable_count = 0
            for _ in range(num_instances):
                problem_count+=1
                print('processing problem {}/{}'.format(problem_count, n_problems), end='\r')
                deadlines = np.random.randint(1, max_time, num_clients)
                locations = np.random.choice(["Champs-Elysées", "Convention", "Saint-Pères"], num_clients)

                if check_solvability(num_clients, num_livreurs, max_time, deadlines, locations, ALPHA, predictions):
                    solvable_count += 1
            solvability_rate = solvable_count / num_instances
            solvability_data.append((num_clients, num_livreurs, max_time, solvability_rate))

# Save solvability data as a dataframe csv

solvability_df = pd.DataFrame(solvability_data, columns=['num_clients', 'num_livreurs', 'max_time', 'solvability_rate'])
solvability_df.to_csv('solvability_data.csv', index=False)

