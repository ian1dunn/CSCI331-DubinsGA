from random import randint, random

import numpy as np

from Individual import Individual, binary_string_to_individual
from Population import Population
from config import BINARY_CODE_LENGTH, MUTATION_RATE, MAX_POP_SIZE


def reproduce(parent1, parent2):
    c = randint(0, len(parent1))
    p1 = [  # 01011010
        parent1[:c:],  # 0101
        parent1[c::]  # 1010
    ]
    p2 = [  # 00111100
        parent2[:c:],  # 0011
        parent2[c::]  # 1100
    ]
    return (
        p1[0] + p2[1],  # 0101 + 1100
        p1[1] + p2[0]  # 1010 + 0011
    )


def mutate(binary_string):
    mutated = ""
    for digit in binary_string:
        if random() < MUTATION_RATE:
            if digit == '0':
                mutated += '1'
            else:
                mutated += '0'
        else:
            mutated += digit
    return mutated


class GA:
    def __init__(self, population):
        self.population = population
        self.generation = 0
        self.fitness_ratios = population.get_fitness_ratios()

    def __str__(self):
        most_fit = self.population.get_most_fit_individuals()
        return f"Generation {self.generation} : J = {most_fit[0].J()}"

    def get_binary_parents(self):
        parents = np.random.choice(self.population.individuals, size=2, replace=False, p=self.fitness_ratios)
        binary_parents = []
        for individual in parents:
            binary_parents.append(individual.get_binary_string())
        return binary_parents

    def evolve(self):
        population_new = Population()

        # Crossover and mutate
        for i in range(self.population.get_population_size() // 2):
            if self.population.get_population_size() == MAX_POP_SIZE - 2:
                break

            parents = self.get_binary_parents()
            children = reproduce(parents[0], parents[1])  # Crossover

            # Add mutations
            population_new.add_individual(binary_string_to_individual(mutate(children[0])))
            population_new.add_individual(binary_string_to_individual(mutate(children[1])))

        # Elitism - add 2 most fit individuals from old population
        old_most_fit = self.population.get_most_fit_individuals()
        population_new.add_individual(old_most_fit[0])
        population_new.add_individual(old_most_fit[1])

        self.population = population_new  # Set new population
        self.generation += 1  # Update generation
        self.fitness_ratios = self.population.get_fitness_ratios()  # Recalculate fitness ratios
