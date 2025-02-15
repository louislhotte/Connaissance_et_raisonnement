# eval.py
import matplotlib.pyplot as plt
from datetime import datetime

def evaluate(solution, delivery_persons, clients, street_data, start_time):
    # Calculate hours worked for each delivery person
    hours_worked = []
    labels = []
    
    for dp in delivery_persons:
        # Find all clients assigned to this delivery person
        assigned_clients = []
        for client in clients:
            var_name = f'A_{dp.id}_{client.id}'
            if solution.get(var_name, False):
                assigned_clients.append(client)
        
        if not assigned_clients:
            # No clients assigned, so hours worked is 0
            hours = 0.0
        else:
            # Determine the earliest start and latest end time among assigned clients
            start_times = [client.time_window[0] for client in assigned_clients]
            end_times = [client.time_window[1] for client in assigned_clients]
            earliest_start = min(start_times)
            latest_end = max(end_times)
            
            # Calculate total hours worked
            delta = latest_end - earliest_start
            hours = delta.total_seconds() / 3600  # Convert seconds to hours
        
        hours_worked.append(hours)
        labels.append(f'Delivery Person {dp.id}')
    
    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.bar(labels, hours_worked, color='skyblue')
    plt.xlabel('Delivery Person')
    plt.ylabel('Hours Worked')
    plt.title('Hours Worked by Each Delivery Person')
    plt.ylim(0, max(hours_worked) + 1 if max(hours_worked) > 0 else 5)  # Adjust y-axis for better visibility
    plt.show()