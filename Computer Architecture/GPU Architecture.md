# GPU Architecture

## Table of Contents
1. [Overview](#overview)
2. [GPU vs. CPU Architecture](#gpu-vs-cpu-architecture)
4. [GPU Microarchitecture](#gpu-microarchitecture)
5. [Advanced Architectural Optimizations](#advanced-architectural-optimizations)
6. [Performance Modeling and Simulation](#performance-modeling-and-simulation)
7. [Multi-GPU Systems](#multi-gpu-systems)
8. [Machine Learning Acceleration](#machine-learning-acceleration)

## Overview

Graphics Processing Units (GPUs) have evolved from fixed-function graphics hardware into powerful, programmable parallel processors essential for high-performance computing (HPC) and machine learning (ML). This document examines GPU hardware architecture, microarchitectural optimizations, and design principles.

**Key Concepts:**
- GPUs are **throughput-optimized** processors designed for massive data-parallel workloads, contrasting with latency-optimized CPUs
- The **Single Program, Multiple Data (SPMD)** programming model is executed on **Single Instruction, Multiple Thread (SIMT)** hardware
- Performance relies on massive multithreading to hide memory latency and maximize execution unit utilization
- Specialized hardware like tensor cores and high-bandwidth memory systems enable efficient ML acceleration

## GPU vs. CPU Architecture

The fundamental design philosophy of GPUs diverges significantly from that of Central Processing Units (CPUs). This divergence stems from their target applications: CPUs are optimized for latency-sensitive tasks, while GPUs are designed for throughput-sensitive, data-parallel workloads.

### Core Architectural Distinctions

A primary distinction lies in their approach to parallelism and execution. CPUs excel at maximizing single-thread performance, whereas GPUs are built to handle thousands of threads simultaneously.

| Feature                   | CPU (Central Processing Unit)  | GPU (Graphics Processing Unit)             |
| ------------------------- | ------------------------------ | ------------------------------------------ |
| **Target Applications**   | Latency-sensitive applications | Throughput-sensitive applications          |
| **Precise Exceptions**    | Yes                            | No (not prioritized)                       |
| **System Role**           | Host                           | Accelerator                                |
| **ISA (Instruction Set)** | Public or open (e.g., x86)     | Open/Closed (e.g., NVIDIA PTX virtual ISA) |
| **Programming Model**     | SISD/SIMD                      | SPMD                                       |

• **SISD:** Single Instruction, Single Data

• **SIMD:** Single Instruction, Multiple Data

• **SPMD:** Single Program, Multiple Data

### Parallelism Paradigms

GPUs and CPUs employ different models to achieve parallelism.

• **SIMD (Single Instruction, Multiple Data):** A model where a single instruction operates on multiple data elements simultaneously. This is highly efficient for repetitive, data-parallel tasks like vector calculations but can be restrictive with branching logic due to its lockstep execution. CPUs utilize vector processing units for SIMD.

• **SPMD (Single Program, Multiple Data):** A more flexible model where multiple autonomous processors (or threads) execute the same program but operate on different data sets. This is the dominant programming pattern for GPUs, allowing for complex workflows with branching and conditional logic. Data decomposition is a typical pattern for SPMD.

• **SIMT (Single Instruction, Multiple Thread):** The hardware execution model that underpins the SPMD programming style on GPUs. It groups threads into "warps" (or "wave-fronts"), where a single instruction is fetched and executed across all threads in the warp.

## GPU Microarchitecture

The performance of a GPU is dictated by its underlying microarchitecture, which is designed to support massive multithreading and high-throughput memory access. This section examines the key architectural components that enable GPU performance.

### Streaming Multiprocessors (SMs)

The **Streaming Multiprocessor (SM)** is the fundamental processing unit of a GPU. A modern GPU contains multiple SMs that execute thread blocks independently.

**GPU Architecture Overview:**

```
┌───────────────────────────────────────────────────────────────┐
│                        GPU Device                             │
│                                                               │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │   SM 0    │  │   SM 1    │  │   SM 2    │  │   SM n    │   │
│  │           │  │           │  │           │  │    ...    │   │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘   │
│        │              │              │              │         │
│        └──────────────┴──────────────┴──────────────┘         │
│                           │                                   │
│                    ┌──────┴───────┐                           │
│                    │  L2 Cache    │                           │
│                    │ (shared)     │                           │
│                    └──────┬───────┘                           │
│                           │                                   │
│                  ┌────────┴─────────┐                         │
│                  │  Global Memory   │                         │
│                  │  (DRAM/HBM)      │                         │
│                  └──────────────────┘                         │
└───────────────────────────────────────────────────────────────┘
```

**Single SM Internal Structure:**

```
┌─────────────────────────────────────────────────────────────────┐
│              Streaming Multiprocessor (SM)                      │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐         │
│  │            Warp Scheduler & Dispatch               │         │
│  │  (Selects ready warps, issues instructions)        │         │
│  └────────────┬──────────────────────┬────────────────┘         │
│               │                      │                          │
│  ┌────────────▼───────────┐  ┌───────▼───────────────┐          │
│  │  Register File         │  │  Register File        │          │
│  │  (32K-64K registers)   │  │  (32K-64K registers)  │          │
│  └────────────┬───────────┘  └───────┬───────────────┘          │
│               │                      │                          │
│  ┌────────────▼───────────────────────▼───────────────┐         │
│  │         Execution Units (per partition)            │         │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌────────┐    │         │
│  │  │ INT  │ │ FP32 │ │ FP64 │ │ SFU  │ │ Tensor │    │         │
│  │  │ ALU  │ │ Core │ │ Core │ │      │ │  Core  │    │         │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └────────┘    │         │
│  │    (×16)    (×16)    (×4)     (×4)      (×4)       │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐           │
│  │     Shared Memory / L1 Cache (unified)           │           │
│  │          48 KB - 164 KB (configurable)           │           │
│  └──────────────────────────────────────────────────┘           │
│                          │                                      │
│  ┌──────────────────────▼──────────────────────────┐            │
│  │         Load/Store Units (LSU)                  │            │
│  └───────────────────────┬─────────────────────────┘            │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           ▼
                    To L2 / Global Memory
```

**SM Specifications (Example: NVIDIA A100):**
- **108 SMs** per GPU
- **64 CUDA cores** (FP32) per SM
- **32 INT32 cores** per SM
- **4 Tensor Cores** (3rd gen) per SM
- **Register File:** 65,536 × 32-bit registers per SM
- **Shared Memory:** Up to 164 KB per SM
- **Max Threads:** 2,048 threads per SM
- **Max Thread Blocks:** 32 blocks per SM
- **Max Warps:** 64 warps per SM (2048 threads ÷ 32)

### Thread Block to Warp Mapping

Understanding how thread blocks are mapped to SMs and divided into warps is crucial for GPU programming:

**Thread Block → SM → Warp Hierarchy:**

```
┌───────────────────────────────────────────────────────────┐
│               Kernel Launch: Grid of Blocks               │
│                                                           │
│   Block 0   Block 1   Block 2   Block 3   Block 4  ...    │
│   ┌────┐    ┌────┐    ┌────┐    ┌────┐    ┌────┐          │
│   │256 │    │256 │    │256 │    │256 │    │256 │          │
│   │thds│    │thds│    │thds│    │thds│    │thds│          │
│   └──┬─┘    └──┬─┘    └──┬─┘    └──┬─┘    └──┬─┘          │
│      │         │         │         │         │            │
└──────┼─────────┼─────────┼─────────┼─────────┼────────────┘
       │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   SM 0   │ │   SM 1   │ │   SM 2   │ │   SM 3   │
│          │ │          │ │          │ │          │
│ Block 0  │ │ Block 1  │ │ Block 2  │ │ Block 3  │
│ Block 4  │ │ Block 5  │ │ Block 6  │ │ Block 7  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
 (scheduler dynamically assigns blocks to available SMs)
```

**Within an SM: Block Divided into Warps:**

```
┌───────────────────────────────────────────────────────────┐
│              SM executing Block 0 (256 threads)           │
│                                                           │
│  Thread IDs:  0 ──────────────────────► 255               │
│               │                           │               │
│               ▼                           ▼               │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Warp 0: Threads  0-31   [████████] Ready           │  │
│  │  Warp 1: Threads 32-63   [████████] Executing       │  │
│  │  Warp 2: Threads 64-95   [░░░░░░░░] Stalled (wait)  │  │
│  │  Warp 3: Threads 96-127  [████████] Ready           │  │
│  │  Warp 4: Threads 128-159 [████████] Ready           │  │
│  │  Warp 5: Threads 160-191 [░░░░░░░░] Stalled (wait)  │  │
│  │  Warp 6: Threads 192-223 [████████] Executing       │  │
│  │  Warp 7: Threads 224-255 [████████] Ready           │  │
│  └─────────────────────────────────────────────────────┘  │
│           │                                               │
│           └──► Warp Scheduler picks ready warps           │
│                                                           │
│  Each warp = 32 threads executing in lockstep (SIMT)      │
└───────────────────────────────────────────────────────────┘
```

**Warp Execution Example (32 threads):**

```
Thread IDs in Warp 0:
┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 0 │ 1 │ 2 │ 3 │...│28 │29 │30 │31 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┘
  ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
┌─────────────────────────────────────┐
│  Single Instruction Fetch           │ ← One PC for entire warp
└─────────────────────────────────────┘
  ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ALU│ALU│ALU│ALU│...│ALU│ALU│ALU│ALU│ ← 32 ALUs execute same instruction
│ 0 │ 1 │ 2 │ 3 │...│28 │29 │30 │31 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┘
  │   │   │   │   │   │   │   │   │
  ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
Result for each thread (different data)
```

**Key Concepts:**
- **Block Assignment:** Hardware scheduler dynamically assigns blocks to any available SM
- **Warp Formation:** Each block is divided into warps of 32 consecutive threads (by threadIdx)
- **Warp Scheduling:** SM can have multiple warps resident; scheduler switches between ready warps
- **SIMT Execution:** All threads in a warp execute the same instruction simultaneously
- **Latency Hiding:** When one warp stalls (memory access), scheduler switches to another ready warp (zero-overhead context switch)

### Multithreading and Context Switching

GPUs use extensive hardware multithreading to hide latency from cache misses or long-latency arithmetic operations.

• **GPU Multithreading:** An SM maintains the state (Program Counter, registers) for many warps in hardware. When one warp stalls (e.g., on a memory access), the scheduler can instantly switch to another ready warp for execution. This is not a software context switch; it's a hardware-level switch with zero overhead.

• **CPU Context Switching:** A heavyweight operation managed by the OS. It involves saving the current thread's state to memory and loading the state of a new thread, incurring significant performance overhead.

Hardware support for GPU multithreading requires multiple PCs (one per active warp) and a very large register file to hold the context for all threads.

### Bank Conflicts and High-Bandwidth Access

To provide high bandwidth to the numerous execution units, both the register file and shared memory are divided into multiple partitions called **banks**. Multiple banks can be accessed simultaneously, but a **bank conflict** occurs if multiple threads in a warp try to access different addresses that map to the same bank.

**Shared Memory Bank Organization (typical: 32 banks):**

```
Address:  0    1    2    3   ...  31   32   33   34  ...  63
         ┌────┬────┬────┬────     ────┬────┬────┬────     ────┐
Bank:    │ 0  │ 1  │ 2  │ 3  │...│31  │ 0  │ 1  │ 2  │...│31  │
         └────┴────┴────┴────     ────┴────┴────┴────     ────┘
         Each bank can serve one 32-bit word per cycle
```

**Conflict-Free Access (Stride = 1):**
```
Warp threads: 0    1    2    3    4   ...  31
Access:      [0]  [1]  [2]  [3]  [4] ... [31]
             │    │    │    │    │       │
             ▼    ▼    ▼    ▼    ▼       ▼
Banks:      B0   B1   B2   B3   B4  ... B31
            ✓    ✓    ✓    ✓    ✓       ✓  ← All parallel, 1 cycle
```

**2-Way Bank Conflict (Stride = 16):**
```
Warp threads: 0    1    2    3   ...
Access:      [0]  [16] [32] [48] ...
             │    │    │    │
             ▼    ▼    ▼    ▼
Banks:      B0   B16  B0   B16  ... ← Threads 0,2 conflict on B0
                                      Threads 1,3 conflict on B16
Result: 2× slower (serialized into 2 passes)
```

**32-Way Bank Conflict (All access same bank):**
```
Warp threads: 0    1    2    3   ...  31
Access:      [0]  [32] [64] [96] ... [992]
             │    │    │    │        │
             └────┴────┴────┴────────┘
                      ▼
                    Bank 0  ← All 32 threads hit same bank
Result: 32× slower (fully serialized)
```

**Avoiding Bank Conflicts:**

```c
// BAD: Stride = 32 → all threads access same bank
__shared__ float data[32][32];
float val = data[threadIdx.x][0];  // All threads read column 0

// GOOD: Stride = 1 → each thread accesses different bank
float val = data[0][threadIdx.x];  // Each thread reads different column

// BETTER: Add padding to avoid column-wise conflicts
__shared__ float data[32][33];  // +1 padding breaks stride pattern
float val = data[threadIdx.x][0];  // Now conflict-free!
```

**Key Points:**
- **Register File Bank Conflicts:** Can occur if threads in a warp access registers that fall into the same bank. Compilers attempt to optimize register allocation and instruction layout to avoid this.
- **Shared Memory Bank Conflicts:** Common performance bottleneck. Hardware serializes conflicting accesses, reducing throughput proportionally to conflict degree.
- **Detection:** Profile with `nvprof` or NVIDIA Nsight Compute to identify bank conflicts
- **Impact:** Can reduce effective bandwidth by 2-32×

### GPU Pipeline and Execution

The GPU pipeline is designed around warp-level execution. Unlike CPU pipelines that process individual instructions, GPU pipelines operate on entire warps (32 threads) simultaneously:

```
┌─────────────────────────────────────────────────────────┐
│                    Warp Scheduler                        │
│  (Selects ready warp from scoreboard)                   │
└─────────────────────────────────────────────────────────┘
                          ↓
         ┌────────────────┴────────────────┐
         │   I-Fetch (single PC per warp)  │
         └────────────────┬────────────────┘
                          ↓
         ┌────────────────┴────────────────┐
         │          Decode                  │
         └────────────────┬────────────────┘
                          ↓
         ┌────────────────┴────────────────┐
         │   Register File Read (32-wide)  │
         └────────────────┬────────────────┘
                          ↓
         ┌────────────────┴────────────────┐
         │   Execute (32 ALUs, with mask)  │
         │   Active: ████████░░░░████████  │ ← Active mask
         └────────────────┬────────────────┘
                          ↓
         ┌────────────────┴────────────────┐
         │   Register File Write-Back      │
         └─────────────────────────────────┘
```

**Pipeline Stages:**

1. **Fetch:** Fetches a single instruction for the entire warp using one program counter
2. **Decode:** Decodes the instruction once for all 32 threads
3. **Register Access:** Reads source operands from the register file (32 lanes wide)
4. **Scheduling (Scoreboarding):** Tracks operand readiness for all warps; selects ready warps using policies like Round-Robin or Greedy-Then-Oldest
5. **Execution:** Executes on 32 ALUs in SIMT fashion, respecting the active mask
6. **Write-Back:** Writes results back to registers for active threads only

**Active Mask for Divergence Handling:**

When threads in a warp take different control flow paths (e.g., if-else branches), the GPU uses an **active mask** - a 32-bit bitmask indicating which threads execute each path. Inactive threads are disabled but still occupy execution slots, reducing effective throughput:

```
if (threadIdx.x % 2 == 0) {
    // Path A - even threads
} else {
    // Path B - odd threads
}

Execution:
  Path A: mask = 10101010...  (50% utilization)
  Path B: mask = 01010101...  (50% utilization)
  Total: 2 passes required
```

### Global Memory Coalescing

One of the most critical performance optimizations is global memory coalescing. When a warp executes a memory instruction, it can generate up to 32 individual memory requests. Proper access patterns allow the hardware to combine these into minimal transactions.

**Coalesced Access Pattern (Optimal):**
```
Thread:  0    1    2    3    4   ...  31
Address: 0x00 0x04 0x08 0x0C 0x10 ... 0x7C

Memory: [████████████████████████████████] ← Single 128-byte transaction
        Sequential, aligned access
        Bandwidth: 128 bytes transferred
```

**Uncoalesced Access Pattern (Poor):**
```
Thread:  0    1    2    3    4   ...  31
Address: 0x00 0x80 0x100 0x180 ...     (stride = 128)

Memory: [██..][██..][██..][██..]...        ← 32 separate transactions
        Scattered access
        Bandwidth: 32 × 128 = 4096 bytes transferred for same data!
```

**Example - Array Access:**
```c
// Good: Coalesced (stride = 1)
float value = array[threadIdx.x];  // Each thread reads consecutive element

// Bad: Uncoalesced (stride = 32)
float value = array[threadIdx.x * 32];  // Scattered reads, 32× bandwidth waste
```

**Rules for Coalescing:**
- Threads in a warp should access **consecutive** memory addresses
- Access should be **aligned** to cache line boundaries (typically 128 bytes)
- Modern GPUs (Compute Capability 6.0+) are more forgiving but still penalize poor patterns
- Coalesced access can achieve **10-20× higher throughput** than uncoalesced access

## Advanced Architectural Optimizations

Modern GPU architectures incorporate sophisticated mechanisms to manage control flow, memory, and scheduling, addressing key performance challenges.

### Handling Divergent Branches

When threads in a warp diverge at a conditional branch, the hardware serializes execution. It executes one path for the active threads, then the other path for the remaining threads.

• **SIMT Stack:** The hardware uses a stack to manage divergence. When a divergent branch occurs, it pushes the alternative path's PC and the reconvergence point (immediate post-dominator) onto the stack. After completing one path, it pops the alternative PC and executes that path. When the reconvergence point is reached, the warp becomes fully active again.

• **Dynamic Warp Formation:** An optimization where the hardware can regroup active threads from different, divergent warps that are executing the same instruction path into new, fully utilized warps. This improves execution unit utilization but must manage potential register file bank conflicts.

### Register File Optimizations

The massive register file on an SM is a major consumer of area and power. Optimizations aim to reduce its size and latency:

• **Observation:** Not all threads are active simultaneously, and not all allocated registers are "live" (containing a value that will be used later). Many register values are read only once.

• **Hierarchical Register Files:** A smaller, faster L0 cache can be placed in front of the main register file to provide low-latency access to frequently used values.

• **Register File Virtualization:** A small physical register file is used to store actual values, while a larger namespace is maintained. This allows for resource sharing, as only live registers need to occupy physical storage.

### GPU Virtual Memory

Modern GPUs support virtual memory, which is crucial for programmability and features like UVA.

• **Address Translation:** GPUs have a memory management unit with a Translation Lookaside Buffer (TLB) to cache virtual-to-physical address translations. A TLB miss triggers a hardware page table walk, which can involve multiple memory accesses.

• **Challenges:** A single warp executing an uncoalesced memory instruction can generate many separate memory requests, leading to a storm of TLB accesses and potential page table walks, creating a significant performance bottleneck.

• **On-Demand Paging (UVA):** When a GPU thread accesses a page not resident in its memory, it generates a page fault. This fault is handled by the host CPU and driver, which involves copying the page from host to device memory. This process has very high latency (tens of microseconds). Prefetching techniques, such as NVIDIA's tree-based neighborhood prefetching, are used to mitigate this latency.

### Warp Scheduling Policies

The scheduler on an SM decides which ready warp to execute next. This decision significantly impacts performance.

• **Round-Robin (RR):** Schedules warps in a circular order. This policy is fair and can expose parallelism but may perform poorly with respect to cache locality, as it quickly cycles through the working sets of many warps, leading to cache thrashing.

• **Greedy-Then-Oldest (GTO):** Prioritizes executing instructions from the same warp until it encounters a long-latency stall (e.g., cache miss). It then switches to the next oldest ready warp. This improves cache locality by keeping a warp's working set in the cache for longer.

• **Two-Level Scheduling:** Divides warps into "active" and "pending" groups. The scheduler only searches the small active set for a ready warp, reducing scheduling overhead and power consumption.

• **Cache-Conscious Scheduling:** Explicitly limits the number of active warps to keep the combined working set size of scheduled warps smaller than the L1 cache capacity, reducing cache misses.

## Performance Modeling and Simulation

Simulators and analytical models are crucial tools for GPU architecture research and performance analysis.

### Cycle-Level Simulation

Cycle-level simulators model the microarchitecture in detail, tracking the state of the machine on a cycle-by-cycle basis. They are accurate but extremely slow.

• **Execution-Driven vs. Trace-Driven:** Execution-driven simulators execute the program instructions during simulation. Trace-driven simulators run on a pre-recorded log (trace) of instructions.

• **Modeling Core Components:** Simulators use queue-based models to represent pipeline stages. The key modeling challenges for GPUs include the warp as the fundamental unit, handling divergent branches (SIMT stack), and accurately modeling memory coalescing.

• **Simulation Acceleration:** Due to the slow speed, techniques are needed to accelerate simulation:

  ◦ **Sampling:** Simulate only a small, representative portion of the program's execution (e.g., SimPoint). For GPUs, this can be done at the block, kernel, or warp level.

  ◦ **Simplifying Models:** Abstract away parts of the architecture that are not under study (e.g., using a fixed latency for memory).

  ◦ **Reducing Workloads:** Use smaller input sizes or fewer iterations.

### Analytical Models

Analytical models use mathematical formulas to provide first-order performance estimates. They are fast and provide insight but are less accurate than simulators.

• **CPI (Cycles Per Instruction) Model:** A model where performance is calculated as a base CPI plus penalties for stall events (e.g., cache misses, branch mispredictions). For multithreaded processors like GPUs, the ideal CPI is divided by the number of warps that can hide latency.

• **Roofline Model:** A visual performance model that identifies whether an application is compute-bound or memory-bound. It plots achieved performance (GFLOPS) against **arithmetic intensity** (FLOPS per byte of memory traffic).

**Interpretation:**
- **Memory-Bound** (left of ridge): Performance scales linearly with bandwidth. Optimize by reducing memory traffic (caching, data reuse, compression)
- **Compute-Bound** (right of ridge): Performance limited by compute throughput. Optimize by increasing computational efficiency (better algorithms, FMA instructions)
- **Ridge Point** = Peak FLOPS / Peak Bandwidth

**Example:** A GPU with 10 TFLOPS peak and 1 TB/s bandwidth has ridge point at 10 FLOPS/byte. A kernel with intensity of 5 FLOPS/byte is memory-bound; one with 20 FLOPS/byte is compute-bound.

## Multi-GPU Systems

To meet the ever-increasing demands of HPC and AI, performance is scaled by using multiple GPUs, either within a single server or across a datacenter.

### Multi-GPU Hardware and Interconnects

• **Monolithic Scaling Limits:** Scaling a single GPU chip has limits due to cost and manufacturing yield.

• **Multi-Chip Modules (MCM):** Modern high-end GPUs are often composed of multiple smaller GPU chips connected on a silicon interposer, appearing as a single logical GPU to the programmer.

• **Interconnects:** High-speed interconnects are required for communication between GPUs.

  ◦ **NVLink:** NVIDIA's proprietary high-speed interconnect, offering much higher bandwidth than standard PCI-Express.

  ◦ **NVSwitch:** A switching fabric that connects multiple NVLinks, enabling all-to-all communication between a large number of GPUs.

  ◦ **RDMA (Remote Direct Memory Access):** A technology that allows a network interface to transfer data directly to/from the memory of another system without involving the CPU, enabling low-latency, high-bandwidth communication across GPU boards.

### Concurrency and Multi-Tenancy

In datacenter environments, it is often desirable to run multiple jobs or tenants on a single physical GPU to increase utilization.

• **CUDA Streams:** Allow a single application to express concurrent operations (e.g., overlapping computation and data transfer) that can be scheduled by the GPU hardware.

• **Multi-Process Service (MPS):** Allows multiple MPI processes or separate client applications to run concurrently on a single GPU by sharing its resources. SMs are spatially partitioned, but other resources like L2 cache and memory bandwidth are shared, which can lead to performance interference.

• **Multi-Instance GPU (MIG):** A hardware feature that partitions a single GPU into multiple, fully isolated GPU instances. Each instance has its own dedicated SMs, memory path, L2 cache, and DRAM bandwidth, providing a predictable quality of service (QoS) for multi-tenant workloads.

## Machine Learning Acceleration

GPUs are the dominant platform for ML due to their massive parallelism, high memory bandwidth, and specialized hardware features.

### Core ML Operations

ML workloads, particularly Deep Neural Networks (DNNs), are composed of highly data-parallel operations:

• **Element-wise operations** (e.g., activation functions)

• **Reduction operations** (e.g., pooling)

• **Dot-product operations**, which form the basis of **GEMM (General Matrix Multiplication)**. GEMM is the computational core of fully connected and convolutional layers.

### Tensor Cores and Systolic Arrays

• **Tensor Cores:** Specialized hardware units introduced by NVIDIA to accelerate matrix-multiply-accumulate (MMA) operations, which are central to GEMM. A single tensor core instruction can perform a 4x4 matrix multiplication (e.g., FP16 inputs with FP32 accumulation) in a single cycle, providing a massive throughput increase over standard SIMT ALUs.

• **Systolic Arrays:** A common microarchitecture for implementing matrix multiplication accelerators. Data is pumped through a grid of processing elements in a rhythmic, pipelined fashion, maximizing data reuse and computational density.

### Floating-Point Formats and Quantization

• **Quantization:** The process of reducing the number of bits used to represent a number. In ML, using lower-precision formats like **FP16 (half-precision)**, **BFLOAT16**, **FP8**, or **INT8** offers significant benefits:

  ◦ **Reduced Storage:** Halves the memory footprint and bandwidth requirements compared to FP32.

  ◦ **Increased Arithmetic Intensity:** Improves the ratio of computation to memory access.

  ◦ **Higher Throughput:** Hardware like tensor cores can perform more low-precision operations per cycle than high-precision ones.

• **Transformer Engine:** A specialized unit in recent NVIDIA GPUs that dynamically scales tensor data to optimal precision formats (e.g., FP8) to accelerate transformer models while maintaining accuracy.

### Sparsity

ML models often contain many zero-valued weights after training and pruning. Sparsity support allows hardware to skip computations involving these zeros.

• **Structured Sparsity:** Modern GPUs support hardware acceleration for structured sparsity, where a fixed pattern of non-zero elements is assumed (e.g., 2 out of every 4 elements are non-zero). This simplifies the hardware design for identifying and skipping zero-value computations, effectively doubling the throughput for sparse matrix operations.

## Summary

This document has covered the fundamental principles of GPU architecture from multiple perspectives:

1. **Architectural Philosophy:** GPUs are throughput-optimized processors that leverage massive parallelism through the SPMD programming model executed on SIMT hardware.

2. **Microarchitecture:** Key components include Streaming Multiprocessors with large register files, shared memory, and warp-based execution. Hardware multithreading hides latency, while memory coalescing and bank conflict avoidance are critical for performance.

3. **Advanced Optimizations:** Modern GPUs employ sophisticated techniques including SIMT stacks for divergence handling, register file virtualization, virtual memory with UVA support, and intelligent warp scheduling policies.

4. **Scalability:** Multi-GPU systems use high-speed interconnects like NVLink and technologies like MIG for efficient resource sharing in datacenter environments.

5. **ML Acceleration:** Specialized hardware including tensor cores, support for reduced-precision arithmetic, and structured sparsity enable GPUs to efficiently accelerate machine learning workloads.

## References

This document is based on content from:
- **CS8803 OMSCS** (Georgia Institute of Technology) - GPU Hardware and Software course
- NVIDIA GPU architecture documentation and research papers
