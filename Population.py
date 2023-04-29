import numpy as np

from Individual import Individual


class Population:

    def __init__(self, individuals_array=[]):
        self.individuals = []
        if len(individuals_array) > 0:
            for x in individuals_array:
                self.add_individual_from_array(x)
        self.fitness = []

    def __str__(self):
        out = []
        i = 0
        for individual in self.individuals:
            out.append(f"Individual {i}: {str(individual)}")
            i += 1

        return "[\n" + ",\n".join(out) + "\n]"

    def add_individual(self, individual):
        self.individuals.append(individual)

    def add_individual_from_array(self, array):
        individual = Individual()
        for i in range(0, len(array), 2):
            individual.add_parameter(array[i], array[i + 1])
        self.add_individual(individual)

    def get_population_size(self):
        return len(self.individuals)

    def calculate_fitness(self):
        self.fitness = []
        for individual in self.individuals:
            self.fitness.append(individual.g())

    def get_fitness_ratios(self):
        total_fitness = np.sum(self.fitness)
        ratios = []
        for value in self.fitness:
            ratios.append(value / total_fitness)
        return ratios

    def get_most_fit_individuals(self, n):
        sorted_fitness = np.sort(self.fitness)[::-1]  # Fitnesses in decreasing order
        top_individuals = []

        for i in range(n):
            top_individuals.append(self.individuals[self.fitness.index(sorted_fitness[i])])
        return top_individuals
