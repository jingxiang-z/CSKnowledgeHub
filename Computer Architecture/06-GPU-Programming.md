# 06 GPU Programming

## Table of Contents
1. [Overview](#overview)
2. [CUDA Programming Model](#cuda-programming-model)
3. [Asynchronous Execution and Concurrency](#asynchronous-execution-and-concurrency)
4. [Memory Management and Optimization](#memory-management-and-optimization)
5. [Programming Constructs](#programming-constructs)
6. [Hardware Architecture and Compute Capability](#hardware-architecture-and-compute-capability)
7. [Compilation and Interoperability](#compilation-and-interoperability)

## Overview

CUDA (Compute Unified Device Architecture) is NVIDIA's parallel computing platform and programming model designed to leverage the massive throughput of GPUs for general-purpose computing. This document covers the CUDA programming model, execution hierarchy, memory management, and programming constructs.

**Key Concepts:**
- **Heterogeneous Computing:** CPU (host) handles serial/control code, GPU (device) executes data-parallel kernels
- **Scalable Hierarchy:** Threads organized into blocks and grids, automatically scheduled across hardware SMs
- **Memory Hierarchy:** Multiple memory spaces with varying latency/bandwidth characteristics require careful management
- **Asynchronous Execution:** Streams and CUDA Graphs enable overlapping computation, data transfer, and multi-kernel execution

## CUDA Programming Model

The CUDA programming model is designed to expose and manage parallelism in a way that scales automatically with the number of available processor cores on a GPU. It achieves this through a specific execution hierarchy, memory model, and hardware architecture abstraction.

### Core Philosophy and Scalability

The fundamental design separates workloads between the host (CPU) and the device (GPU). The CPU handles serial or task-parallel parts of an application, while the GPU executes the highly data-parallel portions. This is a form of heterogeneous programming.

The key to scalability is the decomposition of a problem into a grid of independent thread blocks. Each block can be scheduled on any available Streaming Multiprocessor (SM) in any order, allowing a compiled CUDA program to execute efficiently on GPUs with varying numbers of SMs without modification. A GPU with more SMs will simply execute the program faster.

### Execution Hierarchy

The execution model is defined by a hierarchical organization of parallel threads:

```
Grid
├── Block (0,0)           Block (1,0)           Block (2,0)
│   ├── Thread(0,0)      ├── Thread(0,0)       ├── Thread(0,0)
│   ├── Thread(1,0)      ├── Thread(1,0)       ├── Thread(1,0)
│   ├── Thread(2,0)      ├── Thread(2,0)       ├── Thread(2,0)
│   └── ...              └── ...               └── ...
└── Block (0,1) ...
```

**Hierarchy Levels:**

• **Threads:** The most granular unit of execution. Each thread executes an instance of a kernel function and has a unique `threadIdx` (x, y, z coordinates).

• **Thread Blocks:** Groups of threads (up to 1024 on current hardware) organized in 1D, 2D, or 3D. Threads within a block can cooperate via shared memory and synchronize using `__syncthreads()`. Each block has a unique `blockIdx`.

• **Grid:** The complete collection of thread blocks launched for a kernel. Blocks are independent and can execute in any order.

**Practical Example - Vector Addition:**

```cuda
// Kernel: Each thread adds one pair of elements
__global__ void vectorAdd(float* A, float* B, float* C, int N) {
    // Calculate global thread index
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < N) {
        C[idx] = A[idx] + B[idx];
    }
}

// Host code: Launch kernel
int N = 1000000;
int threadsPerBlock = 256;
int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;

vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
// Launches 3907 blocks × 256 threads = ~1M threads
```

**2D Example - Matrix Addition:**

```cuda
__global__ void matrixAdd(float* A, float* B, float* C, int width, int height) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;

    if (col < width && row < height) {
        int idx = row * width + col;
        C[idx] = A[idx] + B[idx];
    }
}

// Launch with 2D grid and blocks
dim3 threadsPerBlock(16, 16);  // 256 threads per block
dim3 blocksPerGrid((width + 15) / 16, (height + 15) / 16);

matrixAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, width, height);
```

### Memory Hierarchy

CUDA exposes several distinct memory spaces, each with different performance characteristics, scope, and caching behaviors.

| Memory Type                   | Location      | Scope   | Latency | Characteristics                                              |
| ----------------------------- | ------------- | ------- | ------- | ------------------------------------------------------------ |
| **Registers**                 | On-chip (SM)  | Thread  | ~1 cycle | Fastest memory, private to a single thread. Limited resource that impacts occupancy. |
| **Shared Memory**             | On-chip (SM)  | Block   | ~5 cycles | Low latency, high bandwidth. Used for data sharing and cooperation between threads. ~48-163 KB per SM. |
| **L1 Cache**                  | On-chip (SM)  | Block   | ~30 cycles | Caches global/local memory. Unified with shared memory in modern GPUs. |
| **L2 Cache**                  | On-chip (GPU) | Grid    | ~200 cycles | Shared across all SMs. Typically 512 KB - 40 MB depending on architecture. |
| **Global Memory**             | Device DRAM   | Grid    | ~400 cycles | Large capacity (GBs), high latency. Must coalesce accesses. |
| **Constant Memory**           | Device DRAM   | Grid    | ~400 cycles | Read-only, cached. Fast for uniform reads across warps. |
| **Texture/Surface Memory**    | Device DRAM   | Grid    | ~400 cycles | Read-only (texture) or RW (surface), cached. Optimized for 2D spatial locality. |
| **Local Memory**              | Device DRAM   | Thread  | ~400 cycles | Private to thread. Used for register spills. Same latency as global. |

**Shared Memory Example - 1D Stencil:**

```cuda
__global__ void stencil_1d(float* in, float* out, int N) {
    __shared__ float temp[BLOCK_SIZE + 2];  // Block data + halo

    int gidx = blockIdx.x * blockDim.x + threadIdx.x;
    int lidx = threadIdx.x + 1;  // Local index (offset for halo)

    // Load data to shared memory
    temp[lidx] = in[gidx];
    if (threadIdx.x == 0 && gidx > 0)
        temp[0] = in[gidx - 1];  // Left halo
    if (threadIdx.x == blockDim.x - 1 && gidx < N - 1)
        temp[lidx + 1] = in[gidx + 1];  // Right halo

    __syncthreads();  // Wait for all loads to complete

    // Compute using shared memory (fast!)
    if (gidx < N)
        out[gidx] = (temp[lidx-1] + temp[lidx] + temp[lidx+1]) / 3.0f;
}
```

**Benefits:** 3 global memory reads reduced to 1 per thread; neighbors accessed from shared memory ~80× faster than global memory.

### SIMT Architecture

The GPU hardware executes threads in groups of 32, known as **warps**. This is managed by the Single-Instruction, Multiple-Thread (SIMT) architecture.

• **Execution:** All 32 threads in a warp execute the same instruction at the same time.

• **Divergence:** If a data-dependent conditional branch causes threads within a warp to take different execution paths, the warp serially executes each path, disabling threads that are not on the active path. This **warp divergence** can significantly reduce performance, and minimizing it is a key optimization strategy.

• **Independence:** Different warps execute independently of each other, whether they are on the same code path or not.

## Asynchronous Execution and Concurrency

Maximizing performance in CUDA relies on keeping all hardware components—the host CPU, the device GPU, and the data bus between them—busy. This is achieved through asynchronous operations that allow the host to queue work for the device and continue its own execution without waiting.

### Streams

A **stream** is a sequence of operations (kernel launches, memory copies) that execute on the device in the order they are issued by the host. Streams enable overlapping of data transfers and computation.

**Without Streams (Sequential):**
```
Time →
CPU:    |Copy H→D|─wait─|Kernel|─wait─|Copy D→H|─wait─|
GPU:              |Copy  |Kernel|Copy  |
        └─────────┴──────┴──────┴──────┘ Total time
```

**With Streams (Concurrent):**
```
Time →
Stream 0: |Copy₀ H→D|Kernel₀|Copy₀ D→H|
Stream 1:      |Copy₁ H→D|Kernel₁|Copy₁ D→H|
Stream 2:           |Copy₂ H→D|Kernel₂|Copy₂ D→H|
         └─────────┴────────┴─────────┘ Total time (faster!)
```

**Example Code:**

```cuda
cudaStream_t stream1, stream2;
cudaStreamCreate(&stream1);
cudaStreamCreate(&stream2);

// Launch operations in parallel streams
cudaMemcpyAsync(d_A1, h_A1, size, H2D, stream1);
cudaMemcpyAsync(d_A2, h_A2, size, H2D, stream2);

kernel1<<<grid, block, 0, stream1>>>(d_A1);
kernel2<<<grid, block, 0, stream2>>>(d_A2);

cudaMemcpyAsync(h_B1, d_B1, size, D2H, stream1);
cudaMemcpyAsync(h_B2, d_B2, size, D2H, stream2);

// Synchronize when needed
cudaStreamSynchronize(stream1);
cudaStreamSynchronize(stream2);
```

**Key Points:**
- **Async API:** Functions with `Async` suffix return immediately, queuing work on the stream
- **Concurrency:** Different streams can execute concurrently (copy + compute overlap)
- **Synchronization:** Use `cudaStreamSynchronize()`, events, or `cudaDeviceSynchronize()` to wait
- **Default Stream:** Stream 0 synchronizes with all other streams (blocks concurrency)
- **Priorities:** Streams can have priorities to influence scheduling

### CUDA Graphs

For complex workflows involving many small operations, the CPU overhead of launching each operation individually can become a bottleneck. **CUDA Graphs** solve this by allowing an entire sequence of operations to be defined upfront, instantiated, and launched with a single API call.

• **Structure:** A graph is a directed acyclic graph (DAG) of nodes, where nodes represent operations (kernels, memcopies, events) and edges represent dependencies.

• **Creation:**

  ◦ **Graph API:** Graphs can be built explicitly by calling functions like `cudaGraphAddKernelNode`.

  ◦ **Stream Capture:** The most common method is to begin capturing a stream (`cudaStreamBeginCapture`), execute a sequence of operations into that stream as usual, and then end the capture. The runtime records the operations and their dependencies as a graph.

• **Execution:** Once created, a graph is instantiated into an executable graph (`cudaGraphExec_t`), which can be launched into a stream repeatedly with minimal CPU overhead (`cudaGraphLaunch`).

• **Updates:** The parameters of nodes in an instantiated graph (e.g., kernel arguments, memcpy addresses) can be updated without rebuilding the entire graph.

## Memory Management and Optimization

Efficiently managing memory is central to CUDA programming. The runtime provides a spectrum of allocation and management APIs tailored to different use cases.

### Fundamental Memory APIs

• **Device Memory:** `cudaMalloc()` allocates memory in the GPU's global memory space. `cudaMallocPitch()` is recommended for 2D arrays, as it adds padding to ensure rows are aligned for optimal access performance.

• **Page-Locked (Pinned) Host Memory:** `cudaHostAlloc()` allocates host memory that is non-pageable. Data transfers to and from this memory are significantly faster because they can be performed by the GPU's DMA engine without OS intervention. It is a prerequisite for overlapping data transfers with kernel execution.

  ◦ **Mapped Memory:** Page-locked memory can be mapped into the device's address space, allowing kernels to access host memory directly. This avoids explicit `cudaMemcpy` calls, as data is transferred on-demand.

### Advanced Memory Systems

• **Unified Memory (UM):** This system provides a single, managed memory space accessible from both the host and the device using a single pointer.

  ◦ **cudaMallocManaged()****:** Allocates memory that is coherent and can be accessed by both CPU and GPU. The system automatically migrates data pages to the processor that is accessing them.

  ◦ **__managed__****:** A variable specifier for creating global-scope managed variables.

  ◦ **Performance Hints:** `cudaMemPrefetchAsync()` can be used to explicitly move data to a specific processor before it is accessed, hiding migration latency. `cudaMemAdvise()` provides hints about data usage patterns (e.g., `cudaMemAdviseSetReadMostly`) to help the driver optimize data management.

• **Stream Ordered Memory Allocator:**

  ◦ **cudaMallocAsync()** **/** **cudaFreeAsync()**: These functions allocate and free memory with stream-ordered semantics. A memory block is not available for use until the allocation operation completes in its stream, and it is not available for reuse until the free operation completes.

  ◦ **Memory Pools (cudaMemPool_t):** This allocator uses memory pools to avoid expensive OS calls, reusing freed memory to satisfy subsequent allocation requests efficiently. Pools can be configured with specific properties, such as being sharable between processes (IPC).

• **Graph Memory Nodes:**

  ◦ Memory can be allocated and freed via nodes within a CUDA Graph (`cudaGraphAddMemAllocNode`). The memory's lifetime is tied to the graph's execution.

  ◦ The system can perform advanced optimizations, reusing the same physical memory for different graph allocations whose lifetimes do not overlap, significantly reducing the overall memory footprint.

## Programming Constructs

CUDA provides APIs and language extensions that enable more complex and efficient parallel algorithms.

### Cooperative Groups

Cooperative Groups is a C++ template library for defining and synchronizing groups of threads with more flexibility than the standard thread block.

• **Group Types:** Provides handles for implicit groups (e.g., `this_thread_block()`, `this_grid()`) and allows for the creation of explicit, partitioned groups (e.g., `tiled_partition`, `coalesced_threads`).

• **Collectives:** Offers a rich set of collective operations that can be performed on a group, such as `sync()`, `reduce()`, `scan()`, and `memcpy_async()`. These primitives make it easier to write correct and efficient cooperative algorithms.

• **Grid-Level Synchronization:** When used with cooperative launch APIs, `grid_group::sync()` allows for synchronization across all thread blocks in a grid.

### CUDA Dynamic Parallelism (CDP)

CDP enables a kernel executing on the device to configure and launch other kernels.

• **Parent/Child Grids:** The launching kernel creates a parent grid, and the new kernel is a child grid. Parent and child grids share global memory but have distinct shared and local memory.

• **Synchronization:** Modern implementations use stream-based synchronization to control the relationship between parent and child kernel launches, allowing for flexible scheduling and execution patterns.

## Hardware Architecture and Compute Capability

A GPU's features and specifications are defined by its **Compute Capability (CC)**, a version number (e.g., 7.5, 8.6, 9.0) that corresponds to its hardware architecture (e.g., Turing, Ampere, Hopper).

### Streaming Multiprocessors (SMs)

The SM is the fundamental processing unit of the GPU. It contains CUDA cores, special function units, Tensor Cores (on newer architectures), schedulers, registers, and a unified on-chip memory that is partitioned between L1 cache and shared memory. The number of SMs and their specific resources (e.g., register file size, shared memory capacity) are key determinants of a GPU's performance.

### Key Architectural Evolutions

• **Independent Thread Scheduling (Volta, CC 7.x):** Changed how threads within a warp are scheduled, allowing for more fine-grained concurrency but breaking code that relied on implicit warp-synchronous behavior. This necessitated the introduction of `_sync` variants of warp intrinsics (e.g., `__shfl_sync`) that take an explicit mask of participating threads.

• **Tensor Cores (Volta, CC 7.x+):** Specialized hardware units that accelerate mixed-precision matrix multiply-accumulate operations, crucial for deep learning and HPC. They are programmed via warp matrix functions (WMMA).

## Compilation and Interoperability

### The Compiler and PTX

The `nvcc` compiler driver separates host code (compiled by a standard host C++ compiler like GCC or MSVC) from device code.

• Device code (`__global__`, `__device__` functions) is first compiled into **PTX (Parallel Thread Execution)**, a virtual instruction set architecture.

• PTX is then compiled into a binary object (`cubin`) for a specific target architecture.

• Including PTX in an application allows the CUDA driver to just-in-time (JIT) compile it for newer GPU architectures, providing forward compatibility.

### API Levels

CUDA exposes two main APIs:

• **Runtime API:** A high-level, C++-style API (e.g., `cudaMalloc`, `<<<...>>>`). It manages contexts and module loading implicitly.

• **Driver API:** A lower-level, C-style API (e.g., `cuMemAlloc`, `cuLaunchKernel`). It requires explicit management of contexts, modules, and functions. The Runtime API is built on top of the Driver API, and the two can be used interoperably.

### Interoperability with Other APIs

CUDA provides mechanisms to share resources with external APIs, avoiding expensive data copies.

• **Graphics Interop:** Allows sharing of buffers and textures with Direct3D, OpenGL, and Vulkan. CUDA can map these graphics resources into its address space to be read or written by kernels.

• **External Resource Interop:** A more general mechanism for importing memory and synchronization objects from other APIs using OS-native handles (like file descriptors on Linux). This is used for interoperability with Direct3D 12 and Vulkan.

## References

This document is based on content from:
- **NVIDIA CUDA C++ Programming Guide** - Official CUDA documentation
- **CS8803 OMSCS** (Georgia Institute of Technology) - GPU Hardware and Software course