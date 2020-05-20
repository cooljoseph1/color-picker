class Genome:
    def __init__(self, values):
        self.values = values

    def __getitem__(self, index):
        return self.values[index]

    def __iter__(self):
        return iter(self.values)

    def cross(self, genome):
        raise NotImplementedError

    def mutate(self, amount):
        raise notImplementedError

    def distance(self, genome):
        return sum((g1 - g2)**2 for g1, g2 in zip(self, genome))

class RealGenome(Genome):
    def cross(self, genome):
        values = [(g1 + g2) / 2 for g1, g2 in zip(self, genome)]
        return Genome(values)

    def mutate(self, amount):
        self.values = [(g + random.uniform(-amount, amount)) for g in self]

class IntegerGenome(Genome):
    def cross(self, genome):
        values = [(g1 + g2) // 2 for g1, g2 in zip(self, genome)]
        return IntegerGenome(values)

    def mutate(self, amount):
        self.values = [(g + random.randint(-amount, amount)) for g in self]
