# main.py
from logic import *
from eval import *
from variables import DeliveryPerson, Client

# DEFINING THE VARIABLES

DELIVERY_PERSONS = [
    DeliveryPerson(1, 5),
    DeliveryPerson(2, 5),
    DeliveryPerson(3, 6)
]

CLIENTS = [
    Client(1, "Champs-Elysées", (datetime(2023,12,8,12,0), datetime(2023,12,8,14,0))),
    Client(2, "Convention", (datetime(2023,12,8,12,30), datetime(2023,12,8,14,30))),
    Client(3, "Saint-Pères", (datetime(2023,12,8,13,0), datetime(2023,12,8,15,0)))
]


if __name__ == '__main__':
    # Load data and initialize
    street_data = load_predictions('predictions.csv')
    optimizer = SATOptimizer(DELIVERY_PERSONS, CLIENTS, street_data)
    optimizer.create_variables()
    optimizer.create_base_clauses()
    
    # Solve results 
    solution = optimizer.solve()
    print(solution)
    print("Optimal assignments:")
    for var, val in solution.items():
        if val and var.startswith('A_'):
            print(f"{var}: {val}")
    
    # Evaluate solution
    start_time = datetime(2023, 12, 8, 12, 0)  # Match client time windows
    evaluate(solution, DELIVERY_PERSONS, CLIENTS, street_data, start_time)