from pysat.solvers import Solver
from itertools import product

def encode_sat(num_livreurs, num_clients, max_time, deadlines, congestion):
    clauses = []
    
    # Variables
    def A(i, j):
        return i * num_clients + j + 1  # Unique ID for A_ij
    
    def T(i, j, t):
        return num_livreurs * num_clients + (i * num_clients * max_time) + (j * max_time) + t + 1  # Unique ID for T_ijt
    
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
        if t + congestion[t] > deadlines[j]:
            clauses.append([-T(i, j, t)])
    
    # Pas d'overlap des livraisons pour un livreur
    for i, t in product(range(num_livreurs), range(max_time)):
        deliveries_at_t = [T(i, j, t) for j in range(num_clients)]
        for d1, d2 in product(deliveries_at_t, repeat=2):
            if d1 < d2:
                clauses.append([-d1, -d2])  # Pas deux livraisons en même temps
    
    return clauses, A, T

# Exemple d'entrée
num_livreurs = 3
num_clients = 10
max_time = 10
deadlines = [5, 7, 8, 9, 10, 6, 8, 9, 7, 10]
congestion = [0, 1, 2, 1, 0, 2, 1, 1, 0, 1]

clauses, A, T = encode_sat(num_livreurs, num_clients, max_time, deadlines, congestion)

# Résolution
solver = Solver(name='g3')
for clause in clauses:
    solver.add_clause(clause)

if solver.solve():
    model = solver.get_model()
    print("Solution trouvée:")
    for i in range(num_livreurs):
        for j in range(num_clients):
            if A(i, j) in model:
                for t in range(max_time):
                    if T(i, j, t) in model:
                        print(f"Livreur {i} livre client {j} à l'heure {t}")
else:
    print("Pas de solution trouvée.")