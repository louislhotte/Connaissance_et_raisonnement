# variables.py
import csv
from datetime import datetime
import networkx as nx

class StreetData:
    def __init__(self, arc_name):
        self.arc_name = arc_name
        self.time_windows = {}
        
    def add_time_window(self, dt, debit, occupancy):
        self.time_windows[dt] = {
            'hourly_flow': debit,
            'occupancy_rate': occupancy
        }

class DeliveryPerson:
    def __init__(self, person_id, capacity, hourly_rate=30):
        self.id = person_id
        self.capacity = capacity  # Max number of deliveries
        self.hourly_rate = hourly_rate  # EUR/hour

class Client:
    def __init__(self, client_id, location, time_window):
        self.id = client_id
        self.location = location  # Street name
        self.order_size = 1 # For simplification every load is the same size (else the clause for the capacity would be very complex)
        self.time_window = time_window  # (start, end) datetime tuple

def load_predictions(filename):
    streets = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            arc = row['arc']
            if arc not in streets:
                streets[arc] = StreetData(arc)
                
            dt = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M')
            streets[arc].add_time_window(
                dt,
                float(row['debit_horaire']),
                float(row['taux_occupation'])
            )
    return streets
