import random

class GeneticAlgorithm:
    """
    This is a generic class for implementing a genetic algorithm.
    """
    def __init__(self, *gene_sizes, mode="real", initial_genomes="random", genomes=20):
        """
        Create a GeneticAlgorithm object.

        @params
        *gene_sizes -- Integers representing the max value each gene can take on.
                If mode is "real", then values can be any real number on the
                closed interval [0, max_value]. Otherwise, the values must be
                integers on that interval.
        mode -- Mode for the values of genes.  Can be "real" or "integer".
                Defaults to "real".
        initial_genomes -- How to create initial genomes.  Can be "zeros",
                "random", or a user defined function which must accept a list of
                gene sizes, number of genomes, and mode and return a list of
                Genome objects.
                Defaults to "random".
        genomes -- Number of genomes to use in the genetic algorithm.
        """

        self.gene_sizes = gene_sizes
        self.number_of_genomes = genomes
        self.mode = mode

        if initial_genomes == "random":
            self.genomes = random_genomes(self.gene_sizes, self.number_of_genomes, self.mode)
        elif initial_genomes == "zeros":
            self.genomes = zero_genomes(self.gene_sizes, self.number_of_genomes, self.mode)
        elif isinstance(initial_genomes, type(lambda: 0)):
            self.genomes = initial_genomes(self.gene_sizes, self.number_of_genomes, self.mode)
        else:
            raise TypeError("initial_genomes must be 'zeros', 'random', or a function, not " + str(initial_genomes))

    def __getitem__(self, index):
        return self.genomes[index]

    def fitness(self, genome):
        raise NotImplementedError

    def new_generation(self):
        raise NotImplementedError

class ConvergeAlgorithm(GeneticAlgorithm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.choices = []

    def update_choice(self, genome):
        self.choices.append(genome)

    def fitness(self, genome):
        s = 0
        for i, good_genome in enumerate(self.choices[::-1]):
            s += good_genome.distance(genome) / (i + 1)
        return -s

    def new_generation(self, keep=1, cross=5, random=1):
        self.genomes.sort(key=self.fitness, reverse=True)
        new_genomes = self.genomes[:keep]
        for i in range(random):
            new_genomes.append(random.choice(self.genomes))

        while len(new_genomes) < self.number_of_genomes:
            genome1 = random.choice(self.genomes[:cross])
            genome2 = random.choice(self.genomes[:cross])
            new_genomes.append(genome1.cross(genome2))

        self.genomes = new_genomes


def random_genomes(gene_sizes, number_of_genomes, mode="real"):
    """
    Create a list of random genomes.
    """
    genomes = []
    if mode == "real":
        for i in range(number_of_genomes):
            values = [random.uniform(0, size) for size in gene_sizes]
            genomes.append(RealGenome(values))
    elif mode == "integer":
        for i in range(number_of_genomes):
            values = [random.randint(0, size) for size in gene_sizes]
            genomes.append(IntegerGenome(values))
    else:
        raise ValueError("mode must be 'real' or 'integer'")
    return genomes

def zero_genomes(gene_sizes, number_of_genomes, mode="real"):
    """
    Create a list of genomes with zeros everywhere.
    """
    genomes = []
    if mode == "real":
        for i in range(number_of_genomes):
            values = [0.0 for size in gene_sizes]
            genomes.append(RealGenome(values))
    elif mode == "integer":
        for i in range(number_of_genomes):
            values = [0 for size in gene_sizes]
            genomes.append(IntegerGenome(values))
    else:
        raise ValueError("mode must be 'real' or 'integer'")
    return genomes
