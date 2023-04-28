import numpy as np

#
# Constants
#

J_TOLERANCE = 0.1
MAX_POP_SIZE = 500
MAX_GENERATIONS = 1200
MAX_EXECUTION_TIME_MIN = 7  # max execution time in minutes

#
# GA Configuration parameters
#
POP_SIZE = 200
NUM_OPTIMIZATION_PARAMETERS = 10  # per control variable
BINARY_CODE_LENGTH = 7  # per optimization parameter
MUTATION_RATE = 0.005  # 0.5%
K = 200  # infeasibility constant


#
# ODEs
#


def X_DOT(v, alpha): return v * np.cos(alpha)


def Y_DOT(v, alpha): return v * np.sin(alpha)


def ALPHA_DOT(gamma): return gamma


def V_DOT(beta): return beta


#
# Bound constraints
#
GAMMA_CONSTRAINTS = [-0.524, 0.524]
BETA_CONSTRAINTS = [-5, 5]

#
# Initial Conditions, Boundary Conditions
#
s_0 = np.array([0, 8, 0, 0])
s_f = np.array([0, 0, 0, 0])


#
# Feasible region
#


def is_feasible(x, y):
    if x <= 4 and y > 3:
        return True
    elif (-4 < x < 4) and y > -1:
        return True
    elif x >= 4 and y > 3:
        return True
    else:
        return False