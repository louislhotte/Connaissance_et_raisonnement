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