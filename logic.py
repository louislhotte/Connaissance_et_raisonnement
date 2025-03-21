from pysat.solvers import Solver
from itertools import product
import numpy as np

# Generate data
def generate_data(min_clients, max_clients, min_livreurs, max_livreurs, min_max_time, max_max_time):
    num_clients = np.random.randint(min_clients, max_clients)
    num_livreurs = np.random.randint(min_livreurs, max_livreurs)
    max_time = np.random.randint(min_max_time, max_max_time)
    deadlines = np.random.randint(1, max_time, num_clients)
    locations = np.random.choice(["Champs-Elysées", "Convention", "Saint-Pères"], num_clients)
    return num_clients, num_livreurs, max_time, deadlines, locations

# Associate congestion to locations
def build_congestion_matrix(locations, max_time, predictions):
    congestion_matrix = np.zeros((len(locations), max_time))
    for i, location in enumerate(locations):
        if location == "Champs-Elysées":
            congestion_matrix[i] = predictions[predictions["arc"] == "Champs-Elysées"][0:max_time].taux_occupation.to_numpy()
        elif location == "Convention":
            congestion_matrix[i] = predictions[predictions["arc"] == "Convention"][0:max_time].taux_occupation.to_numpy()
        elif location == "Saint-Pères":
            congestion_matrix[i] = predictions[predictions["arc"] == "Saint-Pères"][0:max_time].taux_occupation.to_numpy()
    return congestion_matrix

# Encode the problem in SAT
def encode_sat(num_livreurs, num_clients, max_time, deadlines, congestion_matrix, alpha):
    clauses = []
    
    # Variables
    def A(i, j):
        return i * num_clients + j + 1  # Unique ID for A_ij : livreur i livre le client j
    
    def T(i, j, t):
        return num_livreurs * num_clients + (i * num_clients * max_time) + (j * max_time) + t + 1  # Unique ID for T_ijt
    # T_ijt : livraison du client j par le livreur i démarre à l'heure t
    
    # Un client est assigné à un seul livreur
    for j in range(num_clients):
        clauses.append([A(i, j) for i in range(num_livreurs)])  # Au moins un livreur
        for i1, i2 in product(range(num_livreurs), repeat=2):
            if i1 < i2:
                clauses.append([-A(i1, j), -A(i2, j)])  # Un seul livreur par client
    
    # Une seule heure de départ par livraison
    for i, j in product(range(num_livreurs), range(num_clients)):
        clauses.append([T(i, j, t) for t in range(max_time)])  # Un t au moins
        for t1, t2 in product(range(max_time), repeat=2):
            if t1 < t2:
                clauses.append([-T(i, j, t1), -T(i, j, t2)])  # Un seul t
    
    # Respect des deadlines
    for i, j, t in product(range(num_livreurs), range(num_clients), range(max_time)):
        if t + congestion_matrix[j][t]*alpha > deadlines[j]:
            clauses.append([-T(i, j, t)])
    
    # Pas d'overlap des livraisons pour un livreur
    for i, t in product(range(num_livreurs), range(max_time)):
        for j in range(num_clients):
            start_var = T(i, j, t) 
            busy_time = int(np.ceil(congestion_matrix[j][t] * alpha))  # Time the deliverer remains busy

            # Prevent other deliveries during the busy period
            for t_busy in range(t + 1, min(t + busy_time, max_time)):
                for j2 in range(num_clients):  # Check all possible other deliveries
                    if j != j2:  # Avoid self-comparison
                        conflict_var = T(i, j2, t_busy)
                        clauses.append([-start_var, -conflict_var])  # If `start_var` is true, `conflict_var` must be false

    # A worker can't work more than an 8-hour shift (T(i, j, t) -> !T(i, j, t+k) if 12 > k > 8)
    for i, j, t in product(range(num_livreurs), range(num_clients), range(max_time)):
        for k in range(8, 13):
            if t + k < max_time:
                clauses.append([-T(i, j, t), -T(i, j, t+k)])
    
    return clauses, A, T

def calculate_hours_worked(solution, num_livreurs, num_clients, max_time, A, T, congestion_matrix, ALPHA):
    hours_worked = [0] * num_livreurs
    for i in range(num_livreurs):
        for j in range(num_clients):
            if A(i, j) in solution:
                for t in range(max_time):
                    if T(i, j, t) in solution:
                        hours_worked[i] += 1*congestion_matrix[j][t]*ALPHA
    return hours_worked


# Function to check solvability
def check_solvability(num_clients, num_livreurs, max_time, deadlines, locations, alpha, predictions):
    congestion_matrix = build_congestion_matrix(locations, max_time, predictions)
    clauses, A, T = encode_sat(num_livreurs, num_clients, max_time, deadlines, congestion_matrix, alpha)
    
    solver = Solver(name='g3')
    for clause in clauses:
        solver.add_clause(clause)
    
    return solver.solve()