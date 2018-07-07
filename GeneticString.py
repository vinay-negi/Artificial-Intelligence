import random
from fuzzywuzzy import fuzz
import string

class DNAStructure:
    def __init__(self, length):
        self.pattern = list((random.choice(string.ascii_lowercase+' ')) for _ in range(length))
        self.fitness = -1

    def __str__(self):
        tmp = ''.join(self.pattern)
        return 'DNA: ' + tmp + ' # Fitness: ' + str(self.fitness)


def fitness(chromosome, target):
    for dna in chromosome:
        dna.fitness = fuzz.ratio(dna.pattern, str(target))

    return chromosome


def selection(chromosome):
    chromosome = sorted(chromosome, key=lambda dna: dna.fitness, reverse=True)
    split = int(0.2 * len(chromosome))
    if split is 0:
        split = 1
    print(chromosome[0])
    return chromosome[:split]


def crossover(chromosome, target_len, population):
    offspring = []

    for _ in range(population - len(chromosome)):
        parent1 = random.choice(chromosome)
        parent2 = random.choice(chromosome)

        child = DNAStructure(target_len)
        for i in range(target_len):
            if i % 2:
                child.pattern[i] = parent1.pattern[i]
            else:
                child.pattern[i] = parent2.pattern[i]
        offspring.append(child)
    chromosome.extend(offspring)

    return chromosome


def mutate(chromosome, mutation_rate):
    for dna in chromosome:
        for inx, _ in enumerate(dna.pattern):
            if random.uniform(0.0, 1.0) <= mutation_rate:
                dna.pattern[inx] = random.choice(string.ascii_lowercase+' ')

    return chromosome


def get_chromosome(target_len, population)->list:
    return [DNAStructure(target_len) for _ in range(population)]


def genetic(target, target_len, generation, population, mutation_rate):
    chromosome = get_chromosome(target_len, population)
    for gen in range(generation):
        print(f'Generation {gen}')
        chromosome = fitness(chromosome, target)
        chromosome = selection(chromosome)
        chromosome = crossover(chromosome, target_len, population)
        chromosome = mutate(chromosome, mutation_rate)

        if any(dna.fitness == 100 for dna in chromosome):
            print(f'Target achieved at Generation {gen}')
            exit(0)


if __name__ == '__main__':
    population_ = 150
    generation_ = 10000
    target_ = list('genetic algorithm')
    mutation_rate_ = 0.02
    target_len_ = len(target_)
    genetic(target_, target_len_, generation_, population_, mutation_rate_)
