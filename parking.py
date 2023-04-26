import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

#
# Constants
#
J_TOLERANCE            = 0.1
MAX_POP_SIZE           = 500
MAX_GENERATIONS        = 1200
MAX_EXECUTION_TIME_MIN = 7 * 60 * 1000 
MAX_EXECUTION_TIME     = MAX_EXECUTION_TIME_MIN * 60 * 1000 # max execution time in ms

#
# GA Configuration parameters
#
POP_SIZE                    = 200
NUM_OPTIMIZATION_PARAMETERS = 10 # per control variable
BINARY_CODE_LENGTH          = 7 # per optimization parameter
MUTATION_RATE               = 0.005 # 0.5%
K                           = 200 # infeasibility constant

#
# ODEs
#
X_DOT     = lambda v, alpha : v * np.cos(alpha)
Y_DOT     = lambda v, alpha : v * np.sin(alpha)
ALPHA_DOT = lambda gamma : gamma
V_DOT     = lambda beta : beta

#
# Bound constraints
#
GAMMA_CONSTRAINTS = [-0.524, 0.524]
BETA_CONSTRAINTS  = [-5, 5]

#
# Initial Conditions, Boundary Conditions
#
s_0 = np.array([0, 8, 0, 0])
s_f = np.array([0, 0, 0, 0])

#
# Feasible region
#
def is_feasible(x, y):
    if(x <= 4 and y > 3):
        return True
    elif((x > -4 and x < 4) and y > -1):
        return True
    elif(x >= 4 and y > 3):
        return True
    else:
        return False
    
#
# Populations
#
# Generation 0:
gamma = np.random.uniform(low=GAMMA_CONSTRAINTS[0], high=GAMMA_CONSTRAINTS[1], 
                          size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
beta = np.random.uniform(low=BETA_CONSTRAINTS[0], high=BETA_CONSTRAINTS[1], 
                          size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
population = np.ravel([gamma, beta], 'F')
population.resize([POP_SIZE, NUM_OPTIMIZATION_PARAMETERS * 2])

# v = actual value, s = binary substring
def encode_to_decimal(v, s, ub, lb):
    R = ub - lb
    encoded = ((v - lb) / R) * (2**s - 1)
    if(v < 0): encoded *= -1
    return int(encoded)

def encode_to_binary(d):
    binary = bin(d).replace("-", "")[2:].zfill(BINARY_CODE_LENGTH)
    if d < 0:
        binary = '-' + binary
    return binary

def decode_to_actual(d, s, ub, lb):
    R = ub - lb
    if(d < 0): 
        d *= -1
    decoded = (d/(2**s - 1)) * R + lb
    if(d > 0):
        decoded *= -1
    return decoded 

def decode_to_decimal(b):
    int(b, 2)

def J(i):
    # Where i is a np array [gamma_0, beta_0, ..., gamma_x, beta_x]
    gamma = i[::2] # even elements
    beta = i[1::2] # odd elements

    gamma_interpolation = CubicSpline(gamma, bc_type='natural')
    beta_interpolation = CubicSpline(beta, bc_type='natural')

    sf = eulers(gamma_interpolation, beta_interpolation, s_0, 0, 10)
    if is_feasible(sf[0], sf[1]):
        return np.linalg.norm(s_f - sf)
    else:
        return K
    
def g(i):
    return 1 / (J(i) + 1)

def eulers(gamma, beta, s0, t0, tf):
    h = (tf - t0) / 100
    solution = np.array([s0])
    for i in range(t0, tf):
        prev = solution[i]

        next = [
            prev[0] + h * X_DOT(prev[3], prev[2]), # x
            prev[1] + h * Y_DOT(prev[3], prev[2]), # y
            prev[2] + h * ALPHA_DOT(gamma(i)), # alpha
            prev[3] + h * V_DOT(beta(i)) # v
        ]
        solution.append(next)
    
    return solution.reverse()[0] # Return final state

def toString(i):
    out = []
    j = 0
    for num, v in enumerate(i):
            if num % 2 == 0:
                out.append(f"    gamma_{j}: {v}")
            else:
                out.append(f"    beta_{j}:  {v}")
                j += 1
    return "[\n" + ",\n".join(out) + "\n]"

def individualToDecimal(i):
    out = []
    for num, v in enumerate(i):
        if num % 2 == 0:
            decimal = encode_to_decimal(v, 
                BINARY_CODE_LENGTH, GAMMA_CONSTRAINTS[1], 
                GAMMA_CONSTRAINTS[0])
            out.append(decimal)
        else:
            decimal = encode_to_decimal(v, 
                BINARY_CODE_LENGTH, BETA_CONSTRAINTS[1], 
                BETA_CONSTRAINTS[0])
            out.append(decimal)
    return out

def individualToBinary(i):
    out = []
    for x in i:
        out.append(encode_to_binary(x))
    return out

decimal = individualToDecimal(population[0])
binary = individualToBinary(decimal)

print(toString(population[0]))
print(toString(decimal))
print(toString(binary))