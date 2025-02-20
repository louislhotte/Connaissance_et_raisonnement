# Connaissance_et_raisonnement
Repository for course "Connaissance et Raisonnement" from CentraleSupélec (SAT solvers, logic, FOL, etc...). It contains both TDs & the final project.

# Optimizing Delivery Planning Allocation Using Predictive Street Analytics and SAT-Based Scheduling

## Abstract
In the competitive landscape of low-margin industries such as food delivery, operational optimization is paramount. This study focuses on enhancing the efficiency of delivery operations for Delivroo-like establishments by optimizing the scheduling of deliveries using constraint-based optimization techniques. 

Leveraging predictive analytics for street congestion conditions and integrating SAT-based planning methodologies, this research aims to allocate client-delivery personnel pairs optimally and schedule deliveries efficiently. Unlike conventional linear programming approaches, this project utilizes PySAT—a SAT solver framework—for solving the optimization problem, aligning with the pedagogical objectives of the CentraleSupélec course "Connaissance et Raisonnement." 

Building on previous successes in time series forecasting for street state predictions, this work extends the scope to comprehensive scheduling optimization, providing practical insights into SAT-based problem-solving methodologies.

## 1. Introduction
The food delivery sector operates under stringent margin constraints, necessitating advanced optimization strategies to maintain profitability and service efficiency. Effective scheduling not only reduces delivery times but also minimizes operational costs and enhances customer satisfaction. Traditional approaches to this problem often employ linear programming techniques (e.g., Gurobi) to solve the Vehicle Routing Problem (VRP). However, this study explores an alternative methodology utilizing PySAT, a tool designed for solving Boolean satisfiability problems (SAT), to address the complexities of delivery planning allocation.

## 2. Background and Related Work
Optimization in delivery logistics has been extensively studied, with the VRP being a central focus (Toth & Vigo, 2014). Machine learning models, particularly ensemble methods like LightGBM and deep learning architectures such as Multi-Layer Perceptrons (MLP) and Long Short-Term Memory networks (LSTM), have been effectively employed for predictive analytics in traffic and street conditions (cf. Walmart Sales Forecasting Academic Project, 2024, present in another repository of mine). Additionally, SAT solvers have gained prominence for their applicability in various combinatorial optimization problems (Biere et al., 2009). This research integrates these domains to formulate a novel approach for delivery route optimization.

## 3. Problem Statement
The objective is to develop an optimized system for allocating client orders to delivery personnel and determining the likelihood of a future delivery plan to be successful based on known parameters. This involves:
- Predicting street congestion conditions (e.g., traffic congestion, transit times) using ensemble learning models.
- Modeling the allocation problem : client-delivery personnel pairs with time variables based on predicted street states and delivery requirements.
- Running experiments to determine how likely it is for an ensemble of deliveries to be solvable, knowing only base variables (number of deliverers, number of clients, time range).

## 4. Methodology

### 4.1 Predictive Analytics for Street Congestion
An ensemble learning pipeline combining LightGBM and MLP models is employed to forecast street conditions. Potential enhancements include integrating LSTM or transformer-based models to capture temporal dependencies in traffic patterns. The congestion data predictions directly impact the estimated delivery times, which are then incorporated into the SAT-based scheduling model.

### 4.2 Allocation and Scheduling with PySAT
The allocation of clients to delivery personnel is modeled as a constraint satisfaction problem. Boolean variables represent whether a delivery person is assigned to a client and at what time the delivery starts. Constraints enforce deadlines, workload limits, and congestion-adjusted delivery times. 

### 4.3 Evaluation Metrics
Given that SAT aims to determine whether a given problem is solvable or not, the evaluation metric will be the difficulty of the problem given its input parameters. The difficulty will be defined as the solvability rate (number of problems from this set of input parameters that are solvable). In other words, we'll determine empirically solvability_rate = f(n_deliverers, n_clients, time_range.)

### 4.4 Modeling the Optimization Problem with PySAT

#### 4.4.1 Variables

1. **Assignment Variables (\(A_{i,j}\))**:
   - **Definition**: Binary variables indicating whether delivery person \(i\) is assigned to client \(j\).
   - **Domain**: \(A_{i,j} \in \{0, 1\}\)
   - **Interpretation**: \(A_{i,j} = 1\) if delivery person \(i\) is assigned to client \(j\), otherwise \(0\).

2. **Time Variables (\(T_{i,j,t}\))**:
   - **Definition**: Binary variables indicating whether the delivery for client \(j\) by delivery person \(i\) starts at time \(t\).
   - **Domain**: \(T_{i,j,t} \in \{0, 1\}\)
   - **Interpretation**: \(T_{i,j,t} = 1\) if the delivery starts at time \(t\), otherwise \(0\).

#### 4.4.2 Constraints

1. **Assignment Constraints**:
   - Each client is assigned to exactly one delivery person.
   - A delivery person can only handle one delivery at a time.
   
2. **Time Scheduling Constraints**:
   - Each delivery has exactly one starting time.
   - The delivery must complete before the client’s deadline.
   
3. **Congestion-Aware Time Constraints**:
   - If a delivery starts at time \(t\), its completion time depends on predicted congestion conditions.
   - The delivery must not exceed the available working hours of the delivery person.

4. **Work Shift Constraints**:
   - A delivery person can only work in a continuous time block of 4-8 hours.

### 4.5 Implementation Steps for the MVP

1. **Data Collection and Preprocessing**:
   - Collect street congestion data and preprocess it using LightGBM and MLP models.
   
2. **Predictive Analytics Integration**:
   - Use trained models to generate congestion forecasts.
   
3. **Constraint Modeling and Encoding**:
   - Define the SAT variables and constraints in PySAT.
   
4. **SAT Solver Execution**:
   - Run PySAT to determine if a feasible schedule exists.
   
5. **Solution Evaluation**:
   - Measure solvability rates based on input parameters.

6. **Documentation and Iteration**:
   - Document each step of the MVP development for reproducibility.
   - Use feedback from the MVP to refine the model, variables, and constraints for the full-scale project.

## 5. Expected Contributions
This study aims to:
- Demonstrate the feasibility of using SAT-based solvers for complex scheduling problems.
- Provide a comprehensive framework integrating predictive analytics with constraint-based optimization.
- Enhance practical problem-solving skills and familiarity with PySAT within an academic setting.

## 6. Conclusion
Optimizing delivery schedules through advanced predictive models and constraint-solving techniques holds significant potential for improving operational efficiency in the food delivery sector. By employing PySAT, this research explores a novel approach beyond traditional linear programming methods, contributing to both academic knowledge and practical applications in logistics optimization.

## References
- Biere, A., Heule, M. J., van Maaren, H., & Walsh, T. (2009). *Handbook of Satisfiability*. IOS Press.
- Toth, P., & Vigo, D. (Eds.). (2014). *Vehicle Routing: Problems, Methods, and Applications*. SIAM.
- Walmart Sales Forecasting Academic Project. (2024). [Louis LHOTTE]
- CentraleSupélec Course "Connaissance et Raisonnement". (2025)

