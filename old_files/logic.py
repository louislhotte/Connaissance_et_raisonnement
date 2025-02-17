# logic.py
import subprocess
from variables import load_predictions
from datetime import datetime
from eval import evaluate

class SATOptimizer:
    def __init__(self, delivery_persons, clients, street_data):
        self.delivery_persons = delivery_persons
        self.clients = clients
        self.street_data = load_predictions("predictions.csv")
        self.variables = {}
        self.clauses = []
        
    def create_variables(self):
        """Generate SAT variables for assignments and sequencing"""
        var_id = 1
        
        # Assignment variables A_ij = deliverer i assigned to client j
        for dp in self.delivery_persons:
            for client in self.clients:
                self.variables[f'A_{dp.id}_{client.id}'] = var_id
                var_id += 1
                
        # Sequencing variables S_ijk (i: deliverer, j,k: clients)
        # indicating whether client (j) is visited immediately before client (k) by delivery person (i)
        for dp in self.delivery_persons:
            for j in self.clients:
                for k in self.clients:
                    if j.id != k.id:
                        self.variables[f'S_{dp.id}_{j.id}_{k.id}'] = var_id
                        var_id += 1
        
        # Route variables R_ij = whether client j is included in the route of delivery person i
        for dp in self.delivery_persons:
            for client in self.clients:
                self.variables[f'R_{dp.id}_{client.id}'] = var_id
                var_id += 1
                        
        return var_id  # Total variables count
    
    def create_base_clauses(self):
        """Create fundamental constraints"""

        ### 1: Each client assigned to exactly one delivery person
        for client in self.clients:
            clause = []
            for dp in self.delivery_persons:
                clause.append(self.variables[f'A_{dp.id}_{client.id}'])
            self.clauses.append(clause)  # At least one assignment
            
            # At most one assignment
            for i in range(len(self.delivery_persons)):
                for j in range(i+1, len(self.delivery_persons)):
                    self.clauses.append([
                        -self.variables[f'A_{self.delivery_persons[i].id}_{client.id}'],
                        -self.variables[f'A_{self.delivery_persons[j].id}_{client.id}']
                    ])
                    
        ### 2: Simplified capacity constraints for delivery persons (all loads have the same size)
        for dp in self.delivery_persons:
            max_clients = dp.capacity  # Maximum number of clients this delivery person can handle
            assignment_vars = [self.variables[f'A_{dp.id}_{client.id}'] for client in self.clients]
            
            # Add a cardinality constraint to limit the number of assignments
            self.add_cardinality_constraint(assignment_vars, max_clients)

        ### 3: Flow conservation constraints
        self.add_flow_conservation_constraints()

        ### 4: Subtour elimination constraints
        self.add_subtour_elimination_constraints()

        # ### 4: Time window constraints
        # self.add_time_window_constraints()

        # ### 5: Time window constraints
        # self.add_deliverer_activity_range_constraints()

    def add_deliverer_activity_range_constraints(self):
        """Add constraints to enforce deliverer activity range (4-8 hours continuous)."""
        # Add variables for start and end times of each delivery person's activity
        var_id = max(self.variables.values()) + 1  # Start new variable IDs after existing ones
        for dp in self.delivery_persons:
            self.variables[f'start_{dp.id}'] = var_id
            var_id += 1
            self.variables[f'end_{dp.id}'] = var_id
            var_id += 1

        # Add constraints for each delivery person
        for dp in self.delivery_persons:
            # Constraint 1: Activity duration is between 4 and 8 hours
            # end_i - start_i >= 4 and end_i - start_i <= 8
            self.clauses.append([
                -self.variables[f'start_{dp.id}'],
                self.variables[f'end_{dp.id}'],
                4  # Minimum duration (4 hours)
            ])
            self.clauses.append([
                self.variables[f'start_{dp.id}'],
                -self.variables[f'end_{dp.id}'],
                8  # Maximum duration (8 hours)
            ])

            # Constraint 2: All deliveries for this delivery person must occur within [start_i, end_i]
            for client in self.clients:
                # Convert time window to hours (e.g., 9:00 AM -> 9, 5:00 PM -> 17)
                delivery_time = client.time_window[0].hour  # Use start of time window as delivery time
                # Ensure delivery time is within [start_i, end_i]
                self.clauses.append([
                    -self.variables[f'A_{dp.id}_{client.id}'],
                    self.variables[f'start_{dp.id}'],
                    -delivery_time  # start_i <= delivery_time
                ])
                self.clauses.append([
                    -self.variables[f'A_{dp.id}_{client.id}'],
                    -self.variables[f'end_{dp.id}'],
                    delivery_time  # delivery_time <= end_i
                ])
    
    def add_time_window_constraints(self):
        """Add constraints to ensure deliveries are made within the specified time windows."""
        for dp in self.delivery_persons:
            for client in self.clients:
                # Get the street data for the client's location
                street_data = self.street_data[client.location]
                
                # Get the client's time window (start and end times)
                time_window_start = client.time_window[0]
                time_window_end = client.time_window[1]
                
                # Look up the occupancy rate at the start of the time window
                if time_window_start in street_data.time_windows:
                    occupancy_rate = street_data.time_windows[time_window_start]['occupancy_rate']
                else:
                    # Default occupancy rate if no data is available
                    occupancy_rate = 0.5  # Assume moderate traffic
                
                # Calculate transit time based on occupancy rate
                # For simplicity, assume transit time = base_time * (1 + occupancy_rate)
                base_time = 1  # Base transit time in hours
                transit_time = base_time * (1 + occupancy_rate)
                
                # Ensure delivery time (including transit time) is within the client's time window
                # Delivery time = start of the delivery person's activity + transit time
                self.clauses.append([
                    -self.variables[f'A_{dp.id}_{client.id}'],
                    self.variables[f'start_{dp.id}'],
                    -time_window_start.hour + transit_time  # start_i + transit_time >= time_window_start
                ])
                self.clauses.append([
                    -self.variables[f'A_{dp.id}_{client.id}'],
                    -self.variables[f'end_{dp.id}'],
                    time_window_end.hour - transit_time  # end_i - transit_time <= time_window_end
                ])
    
    def add_flow_conservation_constraints(self):
        """Add flow conservation constraints for sequencing variables."""
        for dp in self.delivery_persons:
            for client_j in self.clients:
                # Constraint: If A_{i,j} = 1, then sum_{k} S_{i,j,k} = 1
                clause_if_assigned = []
                for client_k in self.clients:
                    if client_j.id != client_k.id:
                        clause_if_assigned.append(self.variables[f'S_{dp.id}_{client_j.id}_{client_k.id}'])
                # Add the constraint: A_{i,j} -> sum_{k} S_{i,j,k} = 1
                self.clauses.append([-self.variables[f'A_{dp.id}_{client_j.id}']] + clause_if_assigned)
                
                # Constraint: If sum_{k} S_{i,j,k} = 1, then A_{i,j} = 1
                for client_k in self.clients:
                    if client_j.id != client_k.id:
                        self.clauses.append([
                            -self.variables[f'S_{dp.id}_{client_j.id}_{client_k.id}'],
                            self.variables[f'A_{dp.id}_{client_j.id}']
                        ])

            for client_k in self.clients:
                # Constraint: If A_{i,k} = 1, then sum_{j} S_{i,j,k} = 1
                clause_if_assigned = []
                for client_j in self.clients:
                    if client_j.id != client_k.id:
                        clause_if_assigned.append(self.variables[f'S_{dp.id}_{client_j.id}_{client_k.id}'])
                # Add the constraint: A_{i,k} -> sum_{j} S_{i,j,k} = 1
                self.clauses.append([-self.variables[f'A_{dp.id}_{client_k.id}']] + clause_if_assigned)
                
                # Constraint: If sum_{j} S_{i,j,k} = 1, then A_{i,k} = 1
                for client_j in self.clients:
                    if client_j.id != client_k.id:
                        self.clauses.append([
                            -self.variables[f'S_{dp.id}_{client_j.id}_{client_k.id}'],
                            self.variables[f'A_{dp.id}_{client_k.id}']
                        ])
    
    def add_subtour_elimination_constraints(self):
        """Add subtour elimination constraints using MTZ formulation."""
        # Add auxiliary variables u_j for each client j to represent the order of visits
        u_vars = {}
        var_id = max(self.variables.values()) + 1  # Start new variable IDs after existing ones
        for client in self.clients:
            u_vars[client.id] = var_id
            var_id += 1

        for dp in self.delivery_persons:
            for client_j in self.clients:
                for client_k in self.clients:
                    if client_j.id != client_k.id:
                        # MTZ constraint: u_j - u_k + n * S_{i,j,k} <= n - 1
                        # Where n is the number of clients
                        n = len(self.clients)
                        self.clauses.append([
                            -self.variables[f'S_{dp.id}_{client_j.id}_{client_k.id}'],
                            u_vars[client_j.id],
                            -u_vars[client_k.id],
                            n - 1
                        ])

        # Add the auxiliary variables to the variables dictionary
        for client_id, var in u_vars.items():
            self.variables[f'u_{client_id}'] = var
    
    def add_cardinality_constraint(self, variables, max_count):
        """
        Add a cardinality constraint to ensure that at most `max_count` variables can be true.
        This uses a pairwise encoding for simplicity.
        """
        from itertools import combinations
        
        # Generate all possible subsets of size (max_count + 1)
        for subset in combinations(variables, max_count + 1):
            # Add a clause to ensure that at least one variable in the subset is false
            clause = [-var for var in subset]
            self.clauses.append(clause)
                
    def generate_cnf(self, filename):
        """Generate DIMACS format CNF file"""
        with open(filename, 'w') as f:
            f.write(f'p cnf {len(self.variables)} {len(self.clauses)}\n')
            for clause in self.clauses:
                f.write(' '.join(map(str, clause)) + ' 0\n')
                
    def solve(self, cnf_file='problem.cnf'):
        """Execute GOPHERSAT and parse results"""
        self.generate_cnf(cnf_file)
        result = subprocess.run(
            ['gophersat_win64.exe', cnf_file],
            stdout=open('solution.out', 'w')
        )
        return self.parse_solution(result.stdout)
        
    def parse_solution(self, output):
        with open('solution.out', 'r') as f:
            lines = f.readlines()
            if lines[1] == 's SATISFIABLE\n':
                print('Le probleme est solvable')
            solution = {}
            for line in lines:
                if line.startswith('v '):
                    assignments = list(map(int, line[2:].strip().split()))
                    for var in assignments:
                        var_id = abs(var)
                        for name, vid in self.variables.items():
                            if vid == var_id:
                                solution[name] = var > 0
        return solution
