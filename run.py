import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from logic import *
from scipy.stats import linregress
import time


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
n_clients_range = range(2, 100, 15)
n_livreurs_range = range(2, 30, 5)
max_time_range = range(12, 24*4, 10)

# Number of instances to generate per parameter combination
num_instances = 10

# Data storage
solvability_data = []

n_problems = len(n_clients_range) * len(n_livreurs_range) * len(max_time_range) * num_instances
problem_count=0

# Start timer
start = time.time()

# Iterate through parameter ranges
for num_clients in n_clients_range:
    for num_livreurs in n_livreurs_range:
        for max_time in max_time_range:
            solvable_count = 0
            for _ in range(num_instances):
                problem_count+=1
                if problem_count % 10 == 0:
                    # Estimate time left
                    elapsed = time.time() - start
                    time_per_problem = elapsed/problem_count
                    remaining = time_per_problem*(n_problems-problem_count)
                    print('Processing problem {}/{}'.format(problem_count, n_problems),
                    ' Estimated time left : {:.2f} seconds'.format(remaining), end='\r')

                deadlines = np.random.randint(1, max_time, num_clients)
                locations = np.random.choice(["Champs-Elysées", "Convention", "Saint-Pères"], num_clients)

                if check_solvability(num_clients, num_livreurs, max_time, deadlines, locations, ALPHA, predictions):
                    solvable_count += 1
            solvability_rate = solvable_count / num_instances
            solvability_data.append((num_clients, num_livreurs, max_time, solvability_rate))

# Save solvability data as a dataframe csv

solvability_df = pd.DataFrame(solvability_data, columns=['num_clients', 'num_livreurs', 'max_time', 'solvability_rate'])
solvability_df.to_csv('solvability_data.csv', index=False)

