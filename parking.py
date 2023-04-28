import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

from Population import Population
from config import *

#
# Populations
#
# Generation 0:
gamma = np.random.uniform(low=GAMMA_CONSTRAINTS[0], high=GAMMA_CONSTRAINTS[1],
                          size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
beta = np.random.uniform(low=BETA_CONSTRAINTS[0], high=BETA_CONSTRAINTS[1],
                         size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
random_population = np.ravel([gamma, beta], 'F').resize([POP_SIZE, NUM_OPTIMIZATION_PARAMETERS * 2])
initial_population = Population(random_population)


def J(i):
    # Where i is a np array [gamma_0, beta_0, ..., gamma_x, beta_x]
    gamma = i[::2]  # even elements
    beta = i[1::2]  # odd elements

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
            prev[0] + h * X_DOT(prev[3], prev[2]),  # x
            prev[1] + h * Y_DOT(prev[3], prev[2]),  # y
            prev[2] + h * ALPHA_DOT(gamma(i)),  # alpha
            prev[3] + h * V_DOT(beta(i))  # v
        ]
        solution.append(next)

    return solution.reverse()[0]  # Return final state
