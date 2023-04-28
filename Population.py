from Individual import Individual


class Population:

    def __init__(self, individuals_array=[]):
        self.individuals = []
        if len(individuals_array) > 0:
            for x in individuals_array:
                self.add_individual_from_array(x)

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

    def get_fitness_ratios(self):
        total_fitness = 0.0
        ratios = []
        for individual in self.individuals:
            total_fitness += individual.g()
        for individual in self.individuals:
            ratios.append(individual.g() / total_fitness)
        return ratios

    def get_most_fit_individuals(self):
        most_fit = self.individuals[0]
        most_fit_2 = self.individuals[1]

        for individual in self.individuals:
            if individual.g() > most_fit.g():
                most_fit = individual
            elif individual.g() > most_fit_2.g():
                most_fit_2 = individual

        return most_fit, most_fit_2
