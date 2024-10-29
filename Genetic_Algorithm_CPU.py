from __future__ import annotations
import random

class Chromosome:
    def __init__(
        self,
        chromosome_length: int, mutation_probability: float, goal: str,
        parent_chromosome01: Chromosome | None = None,
        parent_chromosome02: Chromosome | None = None
    ):
        self._length = chromosome_length
        self._mutation_prob = mutation_probability
        self._target = goal
        self._chromo = ''

        if parent_chromosome01 is None and parent_chromosome02 is None:
            self.make_random_chromosome()
        else:
            self.make_chromosome_based_on_parents(parent_chromosome01, parent_chromosome02)

    @property
    def length(self):
        return self._length

    @property
    def mutation_probability(self):
        return self._mutation_prob
    
    @property
    def target(self):
        return self._target
    
    @property
    def chromo(self):
        return self._chromo
    
    @chromo.setter
    def chromo(self, value: str):
        self._chromo = value

    def random_character(self):
        return chr(random.randint(0, 255))
    
    def make_random_chromosome(self):
        chromosome = [
            self.random_character()
            for _ in range(self.length)
        ]

        self.chromo = ''.join(chromosome)
    
    def get_fitness(self):
        goal = self.target
        assert len(goal) == len(self.chromo), f"length of chromosome is wrong -> {goal} vs {self.chromo}"

        fitness = 0
        for ind in range(len(goal)):
            fitness += (
                abs(ord(goal[ind]) - ord(self._chromo[ind]))
            )

        return fitness
    
    def __add__(self, partner: Chromosome):
        assert isinstance(partner, Chromosome), "operand is not Chromosome class"

        return Chromosome(
            chromosome_length=self.length,
            mutation_probability=self.mutation_probability,
            goal=self.target,
            parent_chromosome01=self,
            parent_chromosome02=partner
        )

    def make_chromosome_based_on_parents(
        self,
        parent_chromosome01: Chromosome,
        parent_chromosome02: Chromosome
    ):
        xpoint = random.randint(0, self.length)
        child = parent_chromosome01.chromo[:xpoint] + parent_chromosome02.chromo[xpoint:]
        goal = self.target

        if random.random() < self.mutation_probability:
            diffs = [
                abs(ord(goal[i]) - ord(child[i]))
                for i in range(self.length)
            ]

            mx_ind = diffs.index(max(diffs))
            child = child[:mx_ind] + self.random_character() + child[mx_ind + 1:]

        self.chromo = child
    

class Controller:
    def __init__(
        self,
        goal: str, mutation_probability: float,
        generation_size: int, generation_gap: float,
    ):
        self._target = goal
        self._mutation_prob = mutation_probability
        self._gen_size = generation_size
        self._ggap = generation_gap

    @property
    def goal(self):
        return self._target
    
    @property
    def mutation_probability(self):
        return self._mutation_prob
    
    @property
    def generation_size(self):
        return self._gen_size
    
    @property
    def generation_gap(self):
        return self._ggap
    
    @property
    def generation(self):
        return self._generation
    
    @generation.setter
    def generation(self, value: list[Chromosome]):
        self._generation = value

    def make_random_generation(self):
        self.generation = [
            Chromosome(
                chromosome_length=len(self.goal),
                mutation_probability=self.mutation_probability,
                goal=self.goal
            ) for _ in range(self.generation_size)
        ]

    def get_generation_fitnesses(self):
        return list(sorted(
            self.generation    
        , key=lambda x: (x.get_fitness(), x.chromo)))
    
    def make_roulette(self, sorted_generation: list[Chromosome]):
        fitnesses = [chromosome.get_fitness() for chromosome in sorted_generation]
        max_fitness, min_fitness = max(fitnesses), min(fitnesses)
        inverted_fitnesses = (max_fitness + min_fitness) * len(fitnesses) - sum(fitnesses)
        prev_value = 0.0
        roulette = []
        
        for fitness in fitnesses:
            inverted_fitness = (max_fitness + min_fitness) - fitness
            prev_value += inverted_fitness / inverted_fitnesses
            roulette.append(prev_value)

        return roulette
    
    def selection(self, sorted_generation: list[Chromosome], roulette: list[float]) -> Chromosome:
        dart = random.random()
        for idx, prob in enumerate(roulette):
            if dart < prob:
                return sorted_generation[idx]
            
        return sorted_generation[-1]

    def make_children(self):
        sorted_generation = self.get_generation_fitnesses()
        n_parents = int(self.generation_size * (1 - self.generation_gap))
        new_generation = sorted_generation[:n_parents]
        roulette = self.make_roulette(sorted_generation=sorted_generation)

        for _ in range(self.generation_size - n_parents):
            parent01 = self.selection(sorted_generation, roulette)
            parent02 = self.selection(sorted_generation, roulette)
            new_generation.append(
                parent01 + parent02
            )
        
        self.generation = new_generation
        return sorted_generation[0]


    def start(self):
        self.iter_num = 0
        self.make_random_generation()
        best_fitness = 256 * len(self.goal)

        while best_fitness > 0:
            self.iter_num += 1
            best_chromosome = self.make_children()
            best_fitness = best_chromosome.get_fitness()

def cpu_main(mutation_probability, generation_size, generation_gap, string):
    Controller(
        goal=string,
        mutation_probability=mutation_probability,
        generation_size=generation_size,
        generation_gap=generation_gap
    ).start()

if __name__ == "__main__":
    cpu_main(
        mutation_probability=0.05,
        generation_size=128,
        generation_gap=0.8,
        string=input('String Approximation : ')
    )

    print("Algorithm ended")