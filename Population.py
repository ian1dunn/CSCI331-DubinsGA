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

    def get_individuals(self):
        return self.individuals

    def get_population_size(self):
        return len(self.individuals)
