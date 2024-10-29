from time import time
from Genetic_Algorithm_CPU import cpu_main
from Genetic_Algorithm_GPU import gpu_main
import string, random, sys

candidates = string.printable[:-5]

mutation_probability = 0.05
generation_gap = 0.8

def choice_one_random_string():
    return candidates[random.randrange(0, len(candidates))]

def make_random_string(length):
    return ''.join(choice_one_random_string() for _ in range(length))

def benchmark(length, n, generation_size_cpu, generation_size_gpu):
    targets = [make_random_string(length) for _ in range(n)]

    
    start = time()
    for x in targets:
        cpu_main(
            string=x,
            mutation_probability=mutation_probability,
            generation_size=generation_size_cpu,
            generation_gap=generation_gap
        )
    
    cpu_time = time() - start


    # heating GPU, this is for accurate measuring of gpu time consumption.
    gpu_main(
        string=make_random_string(length),
        gen_size=generation_size_gpu,
        ggap=generation_gap,
        mutation_probability=mutation_probability
    )


    start = time()
    for x in targets:
        gpu_main(
            string=x,
            gen_size=generation_size_gpu,
            ggap=generation_gap,
            mutation_probability=mutation_probability
        )
    
    gpu_time = time() - start


    print(f'CPU : {cpu_time / n:.4f}s')
    print(f'GPU : {gpu_time / n:.4f}s')

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Not Appropriate Usage')
        exit()

    if not sys.argv[1].isdigit() or not sys.argv[2].isdigit() \
        or not sys.argv[3].isdigit() or not sys.argv[4].isdigit():
        print('Input is only allowed Natural Number.')
        exit()
        
    benchmark(
        length=int(sys.argv[1]),
        n=int(sys.argv[2]),
        generation_size_cpu=int(sys.argv[3]),
        generation_size_gpu=int(sys.argv[4])
    )