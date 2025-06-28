import random

from matplotlib import pyplot as plt

class GeneticAlgorithm:
    def __init__(self, queens_count=8, population_size=100, generations=500, mutation_rate=0.1):
        self.N = queens_count
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()
        self.best_fitness_progress = []

    def initialize_population(self):
        ''' Generise pocetnu populaciju '''
        population = []
        for _ in range(self.population_size):
            population.append(self.generate_chromosome())
        return population

    def generate_chromosome(self):
        ''' Generise hromozom (pozicije kraljica) '''
        chromosome = list(range(self.N))
        random.shuffle(chromosome)
        return chromosome
    
    def fitness(self, chromosome):
        ''' Vraca broj sukoba (nenapadajucih kraljica) '''
        conflicts = 0
        for i in range(len(chromosome)):
            for j in range(i + 1, len(chromosome)):
                if abs(chromosome[i] - chromosome[j]) == abs(i - j):
                    conflicts += 1
        return conflicts
    
    def selection(self):
        ''' Bira hromozome sa najmanje sukoba (najbolje hromozome)
            Ovdje bira 5 rendom hromozoma i vraca najbolji
        '''
        tournament = random.sample(self.population, 5)
        return min(tournament, key=lambda x: self.fitness(x))

    def crossover(self, parent1, parent2):
        '''
        Vrši ukrštanje između dva roditelja i vraća potomka.
        '''
        point = random.randint(0, self.N - 1)
        child = parent1[:point]
        for gene in parent2:
            if gene not in child:
                child.append(gene)
        return child

    
    def mutate(self, chromosome):
        ''' Vrsi mutaciju jednog gena u hromozomu - mijenja poziciju kraljice '''
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.N), 2)
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        return chromosome

    def run(self):
        ''' Pokreće genetski algoritam i vraća najbolje rešenje '''
        for generation in range(self.generations):
            self.population.sort(key=lambda x: self.fitness(x))
            best = self.population[0]
            self.best_fitness_progress.append(self.fitness(best))

            if self.fitness(best) == 0:
                print(f"Rešenje pronađeno u generaciji {generation}: {best}")
                return best

            next_generation = [best]  # elitizam
            while len(next_generation) < self.population_size:
                parent1 = self.selection()
                parent2 = self.selection()
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                next_generation.append(child)

            self.population = next_generation

        best = min(self.population, key=lambda x: self.fitness(x))
        print(f"Najbolje pronađeno rešenje: {best}, broj konflikata: {self.fitness(best)}")
        return best
    
    def plot_fitness(self):
        plt.plot(self.best_fitness_progress)
        plt.title("Napredak genetskog algoritma")
        plt.xlabel("Generacija")
        plt.ylabel("Broj konflikata")
        plt.grid()
        plt.show()

    def print_board(self, chromosome):
        print("\n Tabla:")
        for i in range(self.N):
            row = ['.'] * self.N
            row[chromosome[i]] = 'Q'
            print(" ".join(row))

if __name__ == "__main__":
    ga = GeneticAlgorithm(queens_count=11, population_size=100, generations=600, mutation_rate=0.2)
    solution = ga.run()
    ga.print_board(solution)
    ga.plot_fitness()