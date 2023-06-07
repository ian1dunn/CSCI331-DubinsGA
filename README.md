> # CSCI-311: Intro to AI

# Autonomous Parking Using Reinforcement Learning

## Overview
The objective of this project is to design an agent program that finds the state and control histories for a Dubins’ car that implements parallel parking while avoiding obstacles (e.g., sidewalk, other cars). The agent must learn to perform this task on its own using reinforcement learning (RL), specifically a genetic algorithm (GA) solver.

> ![Dubins' Car](https://github.com/ian1dunn/CSCI331-DubinsGA/assets/10554606/1ba1a08d-fc11-4efc-a93f-d2782671ad7b "Dubins' Car")

> ![Car feasibility regions with parameters](https://github.com/ian1dunn/CSCI331-DubinsGA/assets/10554606/b47661cb-17a4-4a90-b6be-ea8ee52bcb9b "Car feasibility regions with parameters")

### State/Control Variables
```
s = [x, y, 𝛼, v]
u = [𝛾, 𝛽]
```
Where:
- x - position on the x axis (ft)
- y - position on the y axis (ft)
- 𝛼 - heading angle with respect to the local horizontal (rad)
- v - velocity (ft/s)
- 𝛾 - heading angle rate (rad/s)
- 𝛽 - acceleration (ft/s 2 )

### Sample Output
See [`/output`](https://github.com/ian1dunn/CSCI331-DubinsGA/tree/main/output) for an example of the final program output as well as its graphs and control history.

## Usage
Edit config.py to modify the program parameters, if desired. These will change the way the genetic algorithm runs and creates new generations.
> **NOTE:** This program takes a minute or two to run. It's as fast as I could get it and still much faster than the project requirements. The population sizes are large and each individual's control points need to be interpolated and operated on by Euler's method to find a list of final control states.

Run `python parking.py` to run the main program driver. The algorithm will continue generating populations until an individual is within the valid threshold.

Once an individual is found, the driver will do several things: 
- Print out the final state the car ACTUALLY reached.
  - This should be within a very small threshold of the expected final state.
- Save the final control history of the graph to a file named `controls.dat`.
- Display and save several graphs:
  - State Trajectory (the path of the car)
  - State Histories
    - x
    - y
    - 𝛼
    - v
  - Control Histories
    - 𝛾
    - 𝛽

### Parameters

#### Constants

```
J_TOLERANCE = 0.1           - Cost function tolerance for success
MAX_POP_SIZE = 500          - Maximum population size
MAX_GENERATIONS = 1200      - Maximum generations
MAX_EXECUTION_TIME_MIN = 7  - Maximum execution time (minutes).
```

#### GA Configuration

```
POP_SIZE = 200                     - 
NUM_OPTIMIZATION_PARAMETERS = 10   - Number of optimization parameters per individual (the number of control points)
BINARY_CODE_LENGTH = 7             - Binary code length of optimization parameters
MUTATION_RATE = 0.005              - How likely a bit is to mutate (%).
K = 200                            - Infeasibility constant (abnormally large cost for being in an infeasible region)
```

#### ODEs (Ordinary Differential Equations)

```
def X_DOT(v, alpha): return v * np.cos(alpha)  - The rate of change in x given velocity and heading angle
def Y_DOT(v, alpha): return v * np.sin(alpha)  - The rate of change in y given velocity and heading angle
def ALPHA_DOT(gamma): return gamma             - The rate of change in heading angle given gamma control parameter (heading angle change rate)
def V_DOT(beta): return beta                   - The rate of change of velocity given beta control parameter (acceleration)
```

#### Boundary Constraints

```
GAMMA_CONSTRAINTS = [-0.524, 0.524]  - The constraints that the gamma control parameter (heading angle change rate) can be randomly generated in.
BETA_CONSTRAINTS = [-5, 5]           - The constraints that the beta control parameter (acceleration) can be randomly generated in.
```

#### Initial Condition & Final Condition

```
s_0 = np.array([0, 8, 0, 0])  - The initial state of the car [x, y, alpha, v]
s_f = np.array([0, 0, 0, 0])  - The final state of the car   [x, y, alpha, v]
```

#### Feasible Region

Function that defines the feasible region of the program. Returns true if the car is in the feasible region, false if otherwise. 
```
def is_feasible(x, y):
    if x <= 4 and y > 3:
        return True
    elif (-4 < x < 4) and y > -1:
        return True
    elif x >= 4 and y > 3:
        return True
    else:
        return False
```
