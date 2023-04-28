import time

import numpy as np
import matplotlib.pyplot as plt

import Individual
from GA import GA
from Population import Population
from config import NUM_OPTIMIZATION_PARAMETERS, POP_SIZE, GAMMA_CONSTRAINTS, BETA_CONSTRAINTS, J_TOLERANCE, \
    MAX_GENERATIONS, MAX_EXECUTION_TIME_MIN

# Generate random initial population of individuals
gamma = np.random.uniform(low=GAMMA_CONSTRAINTS[0], high=GAMMA_CONSTRAINTS[1],
                          size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
beta = np.random.uniform(low=BETA_CONSTRAINTS[0], high=BETA_CONSTRAINTS[1],
                         size=(NUM_OPTIMIZATION_PARAMETERS * POP_SIZE))
random_population = np.ravel([gamma, beta], 'F')
random_population.resize([POP_SIZE, NUM_OPTIMIZATION_PARAMETERS * 2])

# Create initial populations
initial_population = Population(random_population)

# Create GA for initial population and print
ga = GA(initial_population)
print(ga)

# Start running evolutions
start = time.time()
last = start
max_time = time.time() + MAX_EXECUTION_TIME_MIN * 60  # Set timer for MAX_EXECUTION_TIME_MIN minutes from now
while ga.generation <= MAX_GENERATIONS and time.time() < max_time \
        and ga.population.get_most_fit_individuals()[0].J() > J_TOLERANCE:
    ga.evolve()
    print(ga)
    print(f"Took {round(time.time() - last, 2)} seconds for this generation ({round(time.time() - start, 2)} seconds "
          f"total)")
    last = time.time()

# Final individual properties
final = ga.population.get_most_fit_individuals()[0]
states = np.array(final.get_states())
controls = final.get_individual_array()
control_interpolations = final.get_control_interpolations()  # gamma, beta

# Print final states
s_f = Individual.get_s_f(states)
print("\nFinal state values:")
print(f"x_f = {s_f[0]}")
print(f"y_f = {s_f[1]}")
print(f"alpha_f = {s_f[2]}")
print(f"v_f = {s_f[3]}")

# Write to controls.dat
with open("controls.dat", "w") as file:
    file.write("\n".join(controls))

#
# Generate plots
#
plt.style.use('seaborn-poster')
x = np.linspace(0, NUM_OPTIMIZATION_PARAMETERS, 100)

#
# State history
#
plt.figure()
plt.xlabel('Time (s)')
plt.ylabel('x (ft)')
plt.plot(x, states[:, 0], 'b')

plt.figure()
plt.xlabel('Time (s)')
plt.ylabel('y (ft)')
plt.plot(x, states[:, 1], 'b')

plt.figure()
plt.xlabel('Time (s)')
plt.ylabel('α (rad)')
plt.plot(x, states[:, 2], 'b')

plt.figure()
plt.xlabel('Time (s)')
plt.ylabel('v (ft/s)')
plt.plot(x, states[:, 3], 'b')

# Control History
plt.figure()
plt.plot(x, control_interpolations[0](x), 'b')
plt.xlabel('Time (s)')
plt.ylabel('γ (rad/s)')

plt.figure()
plt.plot(x, control_interpolations[1](x), 'b')
plt.xlabel('Time (s)')
plt.ylabel('β (rad/s)')

# State Trajectory
plt.figure()

plt.hlines(y=3, xmin=-15, xmax=-4, colors='black')
plt.hlines(y=3, xmin=4, xmax=15, colors='black')
plt.hlines(y=-1, xmin=-4, xmax=4, colors='black')

plt.vlines(x=-4, ymin=-1, ymax=3, colors='black')
plt.vlines(x=4, ymin=-1, ymax=3, colors='black')

plt.plot(states[:, 0], states[:, 1], 'g')
plt.xlabel('x (ft)')
plt.ylabel('y (ft)')

plt.grid()
plt.show()
