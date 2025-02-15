# Connaissance_et_raisonnement
Repository for course "Connaissance et raisonnement" from CentraleSupélec (SAT solvers, logic, FOL, etc...). It contains both TDs &amp; the final project.

# Optimizing Delivery Route Allocation Using Predictive Street Analytics and SAT-Based Pathfinding

## Abstract
In the competitive landscape of low-margin industries such as food delivery, operational optimization is paramount. This study focuses on enhancing the efficiency of delivery operations for Delivroo-like establishments by optimizing the pathfinding algorithms employed by delivery personnel. 
Leveraging predictive analytics for street conditions and integrating constraint-based optimization techniques, this research aims to allocate client-delivery personnel pairs optimally and determine the most efficient delivery routes. Unlike conventional linear programming approaches, this project utilizes GOPHERSAT—a SAT solver framework—for solving the optimization problem, aligning with the pedagogical objectives of the CentraleSupélec course "Connaissance et Raisonnement." 

Building on previous successes in time series forecasting for street state predictions, this work extends the scope to comprehensive route optimization, providing practical insights into SAT-based problem-solving methodologies.

## 1. Introduction
The food delivery sector operates under stringent margin constraints, necessitating advanced optimization strategies to maintain profitability and service efficiency. Effective route optimization not only reduces delivery times but also minimizes operational costs and enhances customer satisfaction. Traditional approaches to this problem often employ linear programming techniques (e.g., Gurobi) to solve the Vehicle Routing Problem (VRP). However, this study explores an alternative methodology utilizing GOPHERSAT, a tool designed for solving Boolean satisfiability problems (SAT), to address the complexities of delivery route optimization.

## 2. Background and Related Work
Optimization in delivery logistics has been extensively studied, with the VRP being a central focus (Toth & Vigo, 2014). Machine learning models, particularly ensemble methods like LightGBM and deep learning architectures such as Multi-Layer Perceptrons (MLP) and Long Short-Term Memory networks (LSTM), have been effectively employed for predictive analytics in traffic and street conditions (cf. Walmart Sales Forecasting Academic Project, 2024, present in another repository of mine). Additionally, SAT solvers have gained prominence for their applicability in various combinatorial optimization problems (Biere et al., 2009). This research integrates these domains to formulate a novel approach for delivery route optimization.

## 3. Problem Statement
The objective is to develop an optimized system for allocating client orders to delivery personnel and determining the most efficient sequential delivery paths. This involves:
- Predicting street conditions (e.g., traffic congestion, transit times) using ensemble learning models.
- Allocating client-delivery personnel pairs based on predicted street states and delivery requirements.
- Defining optimal delivery routes for each delivery person using GOPHERSAT to solve the resultant conditional satisfiability problems.

## 4. Methodology

### 4.1 Predictive Analytics
An ensemble learning pipeline combining LightGBM and MLP models is employed to forecast street conditions. Potential enhancements include integrating LSTM or transformer-based models to capture temporal dependencies in traffic patterns.

### 4.2 Allocation and Pathfinding with GOPHERSAT
The allocation of clients to delivery personnel is modeled as a constraint satisfaction problem. Conditional `.cnf` (Conjunctive Normal Form) files are constructed to represent the constraints inherent in delivery operations, such as delivery time windows, personnel capacity, and street condition predictions. GOPHERSAT is utilized to solve these `.cnf` files, thereby determining feasible and optimized delivery routes.

### 4.3 Evaluation Metrics
The performance of the proposed optimization framework is evaluated based on delivery time efficiency, computational scalability, and adherence to constraints. Comparative analysis with linear programming approaches is conducted to benchmark effectiveness.

### 4.4 Modeling the Optimization Problem with GOPHERSAT

To effectively utilize GOPHERSAT for optimizing delivery routes, it is essential to accurately model the problem as a Boolean satisfiability (SAT) instance. This involves defining the necessary variables and constraints that represent the delivery operations. This section outlines the modeling approach, detailing the variables, constraints, and the process of constructing the corresponding Conjunctive Normal Form (CNF) for GOPHERSAT.

#### 4.4.1 Variables

Variables in the SAT model represent decisions that need to be made to optimize the delivery routes. For this problem, the primary variables include:

1. **Assignment Variables (\(A_{i,j}\))**:
   - **Definition**: Binary variables indicating whether delivery person \(i\) is assigned to client \(j\).
   - **Domain**: \(A_{i,j} \in \{0, 1\}\)
   - **Interpretation**: \(A_{i,j} = 1\) if delivery person \(i\) is assigned to client \(j\), otherwise \(0\).

2. **Sequencing Variables (\(S_{i,j,k}\))**:
   - **Definition**: Binary variables indicating whether client \(j\) is visited immediately before client \(k\) by delivery person \(i\).
   - **Domain**: \(S_{i,j,k} \in \{0, 1\}\)
   - **Interpretation**: \(S_{i,j,k} = 1\) if client \(k\) is visited immediately after client \(j\) by delivery person \(i\), otherwise \(0\).

3. **Route Variables (\(R_{i,j}\))**:
   - **Definition**: Binary variables indicating whether client \(j\) is included in the route of delivery person \(i\).
   - **Domain**: \(R_{i,j} \in \{0, 1\}\)
   - **Interpretation**: \(R_{i,j} = 1\) if client \(j\) is part of delivery person \(i\)'s route, otherwise \(0\).

#### 4.4.2 Constraints

Constraints ensure that the assignments and routes adhere to operational requirements and optimize the delivery process. The primary constraints include:

1. **Assignment Constraints**:
   - **Each Client is Assigned to Exactly One Delivery Person**:
     \[
     \forall j \in \text{Clients}, \quad \sum_{i \in \text{DeliveryPersons}} A_{i,j} = 1
     \]
   - **Capacity Constraints**:
     \[
     \forall i \in \text{DeliveryPersons}, \quad \sum_{j \in \text{Clients}} w_j \cdot A_{i,j} \leq C_i
     \]
     where \(w_j\) is the weight or size of client \(j\)'s order, and \(C_i\) is the capacity of delivery person \(i\).

2. **Sequencing Constraints**:
   - **Flow Conservation**:
     \[
     \forall i \in \text{DeliveryPersons}, \forall j \in \text{Clients}, \quad \sum_{k \in \text{Clients}} S_{i,j,k} = A_{i,j}
     \]
     \[
     \forall i \in \text{DeliveryPersons}, \forall k \in \text{Clients}, \quad \sum_{j \in \text{Clients}} S_{i,j,k} = A_{i,k}
     \]
   - **Subtour Elimination**:
     Implement constraints to prevent the formation of subtours, ensuring that the route is continuous and starts and ends appropriately.

3. **Time Window Constraints**:
   - Ensure that each delivery is made within the specified time window for each client, considering the predicted street conditions and transit times.

4. **Deliverer activity range**:
   - Each worker can only be active once a day for a continuous time period of 4 to 8 hours. (he can't make a delivery 9 hours after the first one)

#### 4.4.3 Constructing the CNF Representation

To utilize GOPHERSAT, the defined variables and constraints must be translated into a CNF format. The following steps outline the process:

1. **Variable Encoding**:
   - Assign a unique integer identifier to each Boolean variable \(A_{i,j}\), \(S_{i,j,k}\), and \(R_{i,j}\).
   - Maintain a mapping between variables and their integer identifiers for reference in the CNF clauses.

2. **Clause Generation**:
   - **Assignment Constraints**:
     - For each client \(j\), add clauses to ensure that exactly one \(A_{i,j}\) is true.
     - Example: \(A_{1,j} \lor A_{2,j} \lor \ldots \lor A_{n,j}\)\) and pairwise clauses \(\neg A_{i,j} \lor \neg A_{k,j}\) for \(i \neq k\).
   
   - **Capacity Constraints**:
     - Encode the capacity limitations using clauses that restrict the sum of assigned orders to each delivery person.
     - This may require auxiliary variables or cardinality constraints supported by GOPHERSAT.
   
   - **Sequencing Constraints**:
     - Encode flow conservation by ensuring that if a delivery person is assigned to a client, there is exactly one preceding and one succeeding client in the route.
   
   - **Time Window and Street Condition Constraints**:
     - Translate temporal and conditional constraints into logical expressions that can be represented in CNF.
   
   - **Subtour Elimination**:
     - Implement additional clauses or use advanced encoding techniques to prevent subtours within the routes.

3. **Generating the CNF File**:
   - Compile all clauses into a `.cnf` file following the DIMACS format, which includes:
     - A header specifying the number of variables and clauses.
     - Each subsequent line representing a clause with space-separated integers ending with `0`.

#### 4.4.4 Developing a Minimal Viable Product (MVP)

To ensure the feasibility and functionality of the proposed optimization framework, developing an MVP is crucial. The MVP should encompass the following steps:

1. **Define a Simplified Scenario**:
   - Select a small number of delivery personnel and clients to manage complexity.
   - Use simplified street condition predictions (e.g., binary congested or free-flowing).

2. **Implement Variable Encoding**:
   - Create a mapping for variables \(A_{i,j}\), \(S_{i,j,k}\), and \(R_{i,j}\) to unique integers.

3. **Formulate Basic Constraints**:
   - Implement assignment constraints ensuring each client is assigned to one delivery person.
   - Incorporate basic capacity constraints based on delivery personnel limits.

4. **Generate the CNF File**:
   - Translate the variables and constraints into CNF clauses.
   - Ensure the CNF file adheres to the DIMACS format for compatibility with GOPHERSAT.

5. **Run GOPHERSAT and Validate Solutions**:
   - Execute GOPHERSAT with the generated CNF file.
   - Verify that the returned solutions satisfy all constraints and optimize the delivery routes as intended.

6. **Iterate and Expand**:
   - Gradually introduce more variables and constraints, such as sequencing and time windows.
   - Enhance street condition predictions with more granular data and integrate them into the model.

By following this modeling approach and developing an MVP, the project can systematically address the complexities of delivery route optimization using GOPHERSAT, ensuring both academic rigor and practical applicability.

### 4.5 Implementation Steps for the MVP

To streamline the development process, the following implementation steps are recommended for creating the MVP:

1. **Data Collection and Preprocessing**:
   - Gather data on delivery personnel, clients, street conditions, and delivery requirements.
   - Preprocess the data to fit the simplified scenario of the MVP.

2. **Predictive Analytics Integration**:
   - Utilize the existing ensemble learning models (LightGBM and MLP) to generate initial predictions for street conditions.
   - For the MVP, use static or simulated predictions to focus on the optimization aspect.

3. **Constraint Modeling and CNF Generation**:
   - Develop scripts or use existing libraries to encode variables and constraints into CNF format.
   - Ensure that the CNF generation process is scalable for future iterations.

4. **GOPHERSAT Integration**:
   - Set up GOPHERSAT and verify its compatibility with the generated CNF files.
   - Automate the process of running GOPHERSAT and parsing its output for solution extraction.

5. **Solution Evaluation**:
   - Develop metrics to assess the quality of the solutions provided by GOPHERSAT.
   - Compare the MVP results with baseline methods to ensure validity.

6. **Documentation and Iteration**:
   - Document each step of the MVP development for reproducibility.
   - Use feedback from the MVP to refine the model, variables, and constraints for the full-scale project.

## 5. Expected Contributions
This study aims to:
- Demonstrate the feasibility of using SAT-based solvers for complex route optimization in real-world applications.
- Provide a comprehensive framework integrating predictive analytics with constraint-based optimization.
- Enhance practical problem-solving skills and familiarity with GOPHERSAT within an academic setting.

## 6. Conclusion
Optimizing delivery routes through advanced predictive models and innovative constraint-solving techniques holds significant potential for improving operational efficiency in the food delivery sector. By employing GOPHERSAT, this research explores a novel avenue beyond traditional linear programming methods, contributing to both academic knowledge and practical applications in logistics optimization.

## References
- Biere, A., Heule, M. J., van Maaren, H., & Walsh, T. (2009). *Handbook of Satisfiability*. IOS Press.
- Toth, P., & Vigo, D. (Eds.). (2014). *Vehicle Routing: Problems, Methods, and Applications*. SIAM.
- Walmart Sales Forecasting Academic Project. (2024). [Louis LHOTTE]
- CentraleSupélec Course "Connaissance et Raisonnement". (2025)