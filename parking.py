import numpy as np
import matplotlib.pyplot as plt

from GA import GA
from Population import Population
from config import NUM_OPTIMIZATION_PARAMETERS, POP_SIZE, GAMMA_CONSTRAINTS, BETA_CONSTRAINTS, J_TOLERANCE, \
    MAX_GENERATIONS

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
# individuals = initial_population.individuals
# for i in range(0, len(individuals)):
#     print(f"{i}: {individuals[i].g()}")

ga = GA(initial_population)
print(ga)
while ga.generation <= MAX_GENERATIONS and ga.population.get_most_fit_individuals()[0].J() > J_TOLERANCE:
    ga.evolve()
    print(ga)

s_f = ga.population.get_most_fit_individuals()[0].get_s_f()

print("\nFinal state values:")
print(f"x_f = {s_f[0]}")
print(f"y_f = {s_f[1]}")
print(f"alpha_f = {s_f[2]}")
print(f"v_f = {s_f[3]}")

