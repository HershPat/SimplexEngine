# Simplex Engine 

### simplex.py
Main program that handles user input and executes the simplex algorithm. Contains:
- User input collection for variables, constraints and objective function
- Tableau creation and execution
- Solution output

### constraint.py 
Class that handles constraints for the simplex algorithm. Contains:
- Constraint initialization and variable management
- Inequality handling
- Normalization and canonical form checking
- Slack variable calculation
### tableau.py
Class that implements the simplex tableau and algorithm. Contains:
- Tableau initialization and management
- Objective function handling
- Row operations and pivot calculations
- Solution tracking and output

## Usage
1. Run simplex.py
2. Enter the number of variables and constraints
3. Specify if this is a minimization or maximization problem
4. Enter coefficients for the objective function
5. For each constraint:
   - Enter coefficients for each variable
   - Specify the inequality (<=, >= or =)
   - Enter the right-hand side value
6. The program will output:
   - The final tableau
   - The optimal solution values
   - The optimal objective value

## Example
For the linear program:

Maximize: 

For the linear program:

Maximize: 

Z = 3x₁ + 2x₂

Subject to:

2x₁ + x₂ <= 18,
2x₁ + 3x₂ <= 42,
3x₁ + x₂ <= 24,
x₁, x₂ >= 0


Input sequence:
1. Number of variables: 2
2. Number of constraints: 3
3. Function type: Max
4. Objective coefficients: 3, 2
5. Constraint 1:
   - Coefficients: 2, 1
   - Inequality: <=
   - RHS: 18
6. Constraint 2:
   - Coefficients: 2, 3
   - Inequality: <=
   - RHS: 42
7. Constraint 3:
   - Coefficients: 3, 1
   - Inequality: <=
   - RHS: 24

Output:
Final tableau:

[[ 0.    1.   -0.5   0.5   0.   12.  ]

 [ 0.    0.   -1.75  0.25  1.    3.  ]

 [ 1.    0.    0.75 -0.25  0.    3.  ]

 [ 0.    0.    1.25  0.25  0.   33.  ]]

Optimal Solution:
x₁ = 3.0
x₂ = 12.0
s₁ = 0.0
s₂ = 0.0
s₃ = 3.0

Optimal value: 33.0

## Implementation Details

The program is implemented in Python and consists of three main classes:

1. `Tableau` - Handles the simplex tableau operations including:
   - Creating and maintaining the tableau matrix
   - Performing pivot operations
   - Determining entering/leaving variables
   - Executing the simplex algorithm iterations
   - Computing final solutions

2. `Constraint` - Manages constraint information:
   - Stores constraint coefficients and inequality type
   - Handles normalization of constraints
   - Determines slack variable coefficients
   - Validates constraint format

3. `simplex.py` - Main program that:
   - Takes user input for problem specification
   - Constructs the initial tableau
   - Executes the simplex algorithm
   - Outputs the solution

## Requirements

- Python 3.6+
- NumPy library

## Usage

Run the program from the command line:

```bash
python simplex.py
```



