import cupy as cp

assert cp.is_available(), 'CUDA is unavailable.'

find_index_kernel = cp.ElementwiseKernel(
    'raw int32 data, int32 rand_val',
    'int32 index',
    '''
    int left = 0;
    int right = data.size() - 1;
    while (left < right) {
        int mid = (left + right) / 2;
        if (rand_val < data[mid]) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    index = left;
    ''',
    'find_index_kernel'
)

def get_fitness(generation, target):
    return cp.sum(cp.abs(generation - target), axis=1, dtype=cp.int32)

def make_roulette(fitnesses):
    mx = cp.max(fitnesses)
    mn = cp.min(fitnesses)
    arranged_fitnesses = mx + mn - fitnesses
    return cp.cumsum(arranged_fitnesses, dtype=cp.int32)

def selection(roulette, n):
    nums = cp.random.randint(0, roulette[-1], size=(n, 2), dtype=cp.int32)
    indices = find_index_kernel(roulette, nums)
    return indices

def crossover(indices, generation):
    x_points = cp.random.randint(0, generation.shape[-1], size=indices.shape[0], dtype=cp.int32)
    targets = generation[indices]
    mask1 = cp.arange(0, targets.shape[-1], dtype=cp.uint32) < x_points[:, None]
    mask2 = cp.arange(0, targets.shape[-1], dtype=cp.uint32) >= x_points[:, None]
    return cp.where(mask1, targets[:, 0], 0) + cp.where(mask2, targets[:, 1], 0)

def mutation(generation, propability):
    mask = cp.random.random(size=generation.shape[0]) < propability
    rows = cp.arange(generation.shape[0])[mask]
    cols = cp.argmax(cp.abs(generation - target), axis=-1)[mask]
    indices = (rows, cols)
    generation[indices] = cp.random.randint(0, 255, size=rows.shape[0], dtype=generation.dtype)

def sort_generation(fitnesses, n_parents):
    return cp.argsort(fitnesses)[:n_parents]

def make_offsprings(
        generation, fitnesses,
        gen_size, probability, n_parents
    ):

    sorted_indices = sort_generation(fitnesses, n_parents)
    roulette = make_roulette(generation)

    parents_indices = selection(roulette, gen_size - n_parents)
    offspring = crossover(parents_indices, generation)
    mutation(offspring, probability)
    return cp.concatenate((generation[sorted_indices], offspring))

def get_best_score(generation):
    return cp.min(get_fitness(generation))


best_fitness = 99999

gen_size = 128
ggap = 0.8
n_parents = int(gen_size * (1 - ggap))
mutation_probability = 0.03

target = cp.array(list(map(ord, input('String Approximation : '))), dtype=cp.int16)
len_chromo = len(target)


generation = cp.random.randint(0, 255, size=(gen_size, len_chromo), dtype=cp.int16)
fitnesses = get_fitness(generation, target)

while best_fitness > 0:
    generation = make_offsprings(
        generation, fitnesses,
        gen_size, mutation_probability, n_parents
    )

    fitnesses = get_fitness(generation, target)
    best_fitness = cp.min(fitnesses)

result = generation[cp.argmin(fitnesses)].get()
print('result:', ''.join(map(chr, result)))
print('Algorithm Ended!')