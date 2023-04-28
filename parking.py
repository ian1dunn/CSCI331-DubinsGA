import numpy as np
import matplotlib.pyplot as plt

from Population import Population
from config import NUM_OPTIMIZATION_PARAMETERS, POP_SIZE, GAMMA_CONSTRAINTS, BETA_CONSTRAINTS

#
# Populations
#
# Generation 0:
gamma = np.random.uniform(low=GAMMA_CONSTRAINTS[0], high=GAMMA_CONSTRAINTS[1],
                          size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
beta = np.random.uniform(low=BETA_CONSTRAINTS[0], high=BETA_CONSTRAINTS[1],
                         size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
random_population = np.ravel([gamma, beta], 'F')
random_population.resize([POP_SIZE, NUM_OPTIMIZATION_PARAMETERS * 2])

initial_population = Population(random_population)
print(initial_population)

individuals = initial_population.get_individuals()
for i in range(0, len(individuals)):
    print(f"{i}: {individuals[i].g()}")
