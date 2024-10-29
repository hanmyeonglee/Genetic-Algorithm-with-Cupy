# Genetic Algorithm with CUDA
This project approaches to a genetic algorithm, specifically a simple String Approximation Algorithm, using GPU(CUDA). It (will) only uses Cupy, not raw C codes.

## Requirements
1. `CUDA`
2. `Cupy`
3. `Anaconda(Optional)`

### Environments
- `CUDA Driver Version: 560.94`
- `CUDA Version: 12.4`
- `Cupy Version: 13.3.0`
- `Anaconda Version: 24.9.1`

### Installation Guide for CUDA
1. Windows: <https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/>
2. Linux: <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/>

### Installation Guide for Cupy
- <https://docs.cupy.dev/en/stable/install.html>

## Run

### Genetic Algorithm
- `python ./Genetic_Algorithm_GPU.py`

### Benchmark
- `python ./benchmark.py <string_length> <iter_num>`

## Benchmark
`<string_length> <iteration_number> <cpu_GA_generation_size> <gpu_GA_generation_size>`

1. `8 16 128 1024`
- CPU : 0.4972s
- GPU : 0.2267s

2. `16 16 128 1024`
- CPU : 1.1540s
- GPU : 0.5704s

3. `32 16 128 1024`
- CPU : 3.9948s
- GPU : 1.2608s

4. `64 16 128 1024`
- CPU : 11.4446s
- GPU : 2.5063s

5. `128 16 128 1024`
- CPU : 53.7115s
- GPU : 5.1431s

## TODO
**This project is not completed.**

1. RawKernel to Cupy API Code
2. Cleaning code