from time import time
from Genetic_Algorithm_CPU import cpu_main
from Genetic_Algorithm_GPU import gpu_main
import string, random, sys

candidates = string.printable[:-5]

mutation_probability = 0.05
generation_size = 128
generation_gap = 0.8

def choice_one_random_string():
    return candidates[random.randrange(0, len(candidates))]

def make_random_string(length):
    return ''.join(choice_one_random_string() for _ in range(length))

def benchmark(length, n):
    targets = [make_random_string(length) for _ in range(n)]

    
    start = time()
    for x in targets:
        cpu_main(
            string=x,
            mutation_probability=mutation_probability,
            generation_size=generation_size,
            generation_gap=generation_gap
        )
    
    cpu_time = time() - start


    start = time()
    for x in targets:
        gpu_main(
            string=x,
            gen_size=generation_size,
            ggap=generation_gap,
            mutation_probability=mutation_probability
        )
    
    gpu_time = time() - start


    print(f'CPU : {cpu_time / n:.4f}ms')
    print(f'GPU : {gpu_time / n:.4f}ms')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Not Appropriate Usage')
        exit()

    if not sys.argv[1].isdigit() or not sys.argv[2].isdigit():
        print('Input is only allowed Natural Number.')
        exit()
        
    benchmark(
        length=int(sys.argv[1]),
        n=int(sys.argv[2]),
    )