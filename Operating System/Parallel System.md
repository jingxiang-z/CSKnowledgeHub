# Parallel Systems

## Table of Contents

1. [Overview](#overview)
2. [Shared Memory Multiprocessor Models](#shared-memory-multiprocessor-models)
3. [Cache Coherence](#cache-coherence)
4. [Memory Consistency Models](#memory-consistency-models)
5. [Scheduling in Parallel Systems](#scheduling-in-parallel-systems)
6. [Scalable OS Design](#scalable-os-design)
7. [Related Topics](#related-topics)
8. [References](#references)

## Overview

Parallelism has become fundamental to modern computing systems. Any general-purpose CPU chip contains multiple cores designed to exploit hardware parallelism. Operating systems must be specifically designed to leverage this hardware architecture while managing the complex challenges of shared memory access, data consistency, and scalability.

Parallel systems enable multiple processors to work simultaneously on different parts of a computation, but this introduces unique challenges not present in single-processor systems. The primary concerns include maintaining data consistency across multiple caches, implementing efficient synchronization mechanisms, and designing schedulers that optimize cache utilization.

### Key Challenges

**Hardware Complexity:**
- Multiple processors with private caches accessing shared memory
- Maintaining cache coherence across processors
- Managing interconnection network contention

**Software Complexity:**
- Implementing scalable synchronization primitives
- Designing cache-aware scheduling algorithms
- Minimizing shared data structures to reduce contention

**Scalability:**
- Balancing parallelism benefits against coordination overhead
- Ensuring performance increases with additional processors
- Managing NUMA (Non-Uniform Memory Access) effects

## Shared Memory Multiprocessor Models

Shared memory multiprocessors consist of CPUs, memory, and an interconnection network. The defining characteristic is that the entire address space is accessible from any CPU. Each CPU typically has its own private cache hierarchy.

### Dance Hall Architecture

In this architecture, CPUs are located on one side of the interconnection network, and memory banks are situated on the other side. All memory accesses traverse the interconnection network, with uniform access latency from any CPU to any memory location.

### Symmetric Multiprocessor (SMP)

SMP systems use a simple bus connecting all CPUs to main memory. This architecture is considered symmetric because access time from any CPU to memory is identical. The shared bus provides a natural broadcast medium for cache coherence protocols but can become a bottleneck as the number of processors increases.

**Characteristics:**
- Uniform memory access (UMA) time
- Simple interconnection topology
- Limited scalability due to bus contention
- Common in small to medium-scale systems

### Distributed Shared Memory (DSM)

DSM, also called NUMA (Non-Uniform Memory Access), associates memory banks with individual CPUs. While all CPUs can access all memory via the interconnection network, access to local memory is significantly faster than access to remote memory.

**Characteristics:**
- Non-uniform access latency
- Better scalability than SMP
- Requires NUMA-aware algorithms for optimal performance
- Local memory access avoids network traversal

### Cache Coherence Classification

Shared memory systems are further categorized by their hardware support for cache coherence:

**Cache-Coherent (CC) Multiprocessor:**
- Hardware maintains cache coherence automatically
- Provides shared address space and consistency guarantees
- Higher hardware complexity but simpler programming model

**Non-Cache Coherent (NCC) Multiprocessor:**
- Hardware provides shared address space only
- Software (OS) must ensure cache coherence
- Lower hardware cost but increased software complexity

## Cache Coherence

The cache coherence problem arises when multiple processors cache copies of the same memory location. If one processor modifies its cached copy, other processors must somehow be notified or their copies must be invalidated to maintain consistency.

### The Problem

Consider a shared memory location `y` cached by processors P1, P2, and P3. If P1 writes a new value `y'` to its local cache, P2 and P3 must subsequently observe `y'` rather than the stale value `y`. This is the fundamental cache coherence problem.

**Without coherence mechanisms:**
- Different processors see different values for the same memory location
- Program behavior becomes unpredictable
- Parallel programs cannot function correctly

### Hardware Coherence Schemes

#### Write Invalidate

When a processor writes to a cached location, the hardware broadcasts an invalidate signal for that memory address. Other caches with copies of that location invalidate their local copies upon receiving the signal.

**Mechanism:**
- P1 writes to memory location y
- Hardware broadcasts "invalidate y" on the interconnection network
- Snoopy caches in P2, P3, etc., observe the broadcast
- Caches containing y invalidate their local copies
- Subsequent reads by P2 or P3 fetch the new value from memory or P1's cache

**Advantages:**
- Reduces bandwidth for write-intensive sharing patterns
- Only one message per write operation

**Disadvantages:**
- Subsequent reads by other processors incur cache misses
- Poor performance when multiple readers exist

#### Write Update

When a processor writes to a cached location, the hardware sends the new value to all caches holding a copy. These caches immediately update their local copies to the new value.

**Mechanism:**
- P1 writes value y' to memory location y
- Hardware sends "update y to y'" on the network
- Caches in P2, P3, etc., observe the update
- Caches holding y modify their copies to y'

**Advantages:**
- Readers immediately see updated values without cache misses
- Better for read-intensive sharing patterns

**Disadvantages:**
- Higher bandwidth consumption for writes
- Update messages carry data, not just addresses

### Scalability Implications

As the number of processors increases, maintaining cache coherence introduces growing overhead, particularly for shared data. This overhead can prevent performance from scaling linearly with processor count.

Chuck Thacker's observation captures this fundamental tension: "Shared memory machines scale well when you don't share memory." This highlights the importance of minimizing shared data structures in parallel algorithms and OS design.

## Memory Consistency Models

The memory consistency model (MCM) defines the contract between hardware and software regarding the ordering and visibility of memory operations across multiple processors. It specifies what behavior a programmer can expect when writing multi-threaded applications.

### Sequential Consistency

Proposed by Leslie Lamport in 1977, sequential consistency is the most intuitive memory consistency model. It guarantees that the result of any execution is the same as if operations of all processors were executed in some sequential order, and operations of each processor appear in program order.

**Two Key Properties:**

1. **Program Order:** Memory accesses from a single processor maintain their textual (program) order. If instruction A precedes instruction B in the program, A's memory access completes before B's.

2. **Arbitrary Interleaving:** Memory accesses from different processors can be arbitrarily interleaved, but some global sequential order exists that all processors observe consistently.

**Example:**

Consider two processors executing:
```
Processor 1:          Processor 2:
a = 1                 c = b
b = 1                 d = a
```

Sequential consistency ensures that the outcome (c=0, d=1) is impossible because it would require b to be read before it was written while a was read after it was written, violating any possible sequential interleaving.

### Memory Consistency vs. Cache Coherence

These concepts are related but distinct:

**Memory Consistency Model:**
- Defines what application programmers need to understand
- Specifies ordering guarantees for memory operations
- Contract between hardware/software about behavior
- Programmer's expectation of system behavior

**Cache Coherence:**
- Implementation mechanism for maintaining consistency
- How the system enforces the consistency model with private caches
- Hardware-software partnership detail
- System's internal mechanism to meet the consistency guarantee

## Scheduling in Parallel Systems

Effective scheduling in parallel systems requires balancing traditional concerns (fairness, priority) with cache affinity to optimize memory hierarchy utilization.

### Scheduling Fundamentals

**Decision Points:**
The OS scheduler makes decisions when a thread:
- Makes a blocking I/O system call
- Synchronizes with other threads (acquires lock, waits on condition)
- Exhausts its time quantum

**Traditional Factors:**
- First Come, First Served (FCFS): fairness
- Static Priority: priority-based preemption
- Dynamic Priority: interactive boost, aging

### Memory Hierarchy and Cache Affinity

Modern processors exhibit a growing disparity between CPU speed and memory latency, often exceeding two orders of magnitude. This makes cache hits critical for performance.

**Cache Hierarchy:**
- L1 cache: Per-core, smallest, fastest (1-4 cycles)
- L2 cache: Per-core or shared, medium size (10-20 cycles)
- L3 cache: Shared across cores, largest (40-75 cycles)
- Main memory: Off-chip (100-300 cycles)

**Cache Affinity Principle:**
If thread T1 previously ran on processor P1, rescheduling T1 on P1 increases the probability that T1's working set remains in P1's cache hierarchy (L1, L2, or L3).

**Challenge:**
Caches may be polluted by other threads (T2, T3) that executed on P1 between T1's deschedulings, reducing the benefit of cache affinity.

### Cache Affinity Scheduling Policies

#### Fixed Processor

Each thread is permanently assigned to a specific processor from creation to termination. Initial assignment based on load balancing.

**Advantages:**
- Maximizes cache affinity over thread lifetime
- Simple implementation

**Disadvantages:**
- Poor load balancing if workload changes
- Can lead to idle processors while others are overloaded

#### Last Processor

When a processor becomes idle, it preferentially selects threads that last executed on that processor.

**Advantages:**
- Exploits cache affinity for recently executed threads
- Better load balancing than fixed processor

**Disadvantages:**
- Doesn't account for cache pollution from intervening threads

#### Minimum Intervening (MI)

Tracks an affinity index for each thread-processor pair: the number of threads that executed on processor P_j since thread T_i last ran on P_j. Scheduler chooses the processor with minimum affinity index.

**Mechanism:**
- Maintain affinity_index[T_i][P_j] for each thread-processor pair
- When scheduling T_i, select P_j that minimizes affinity_index[T_i][P_j]
- Lower index means less cache pollution

**Advantages:**
- Explicitly models cache pollution
- Makes informed decisions about cache warmth

**Disadvantages:**
- O(N×M) space for N threads and M processors
- Doesn't account for future pollution from queued threads

#### Minimum Intervening Plus Queue (MI+Q)

Extends MI by considering both affinity index and the processor's current queue length.

**Decision Function:**
```
Choose processor P_j that minimizes:
    affinity_index[T_i][P_j] + queue_length[P_j]
```

**Advantages:**
- Accounts for future cache pollution from queued threads
- Better prediction of actual cache state when thread runs
- Improved load balancing

**Disadvantages:**
- Additional complexity
- Still requires substantial metadata

#### Limited Minimum Intervening

Reduces metadata overhead by tracking affinity only for the top K candidate processors rather than all processors.

**Advantages:**
- O(N×K) space instead of O(N×M)
- Practical for large-scale systems

**Disadvantages:**
- May miss optimal processor if not in top K

### Implementation Considerations

**Queue Organization:**

**Global Queue:**
- Simple implementation
- Suitable for FCFS
- Poor scalability due to contention
- Not cache-aware

**Local Queues:**
- Per-processor queue
- Organized by policy (priority, affinity)
- Better scalability
- Supports work stealing for load balancing

**Work Stealing:**
When a processor's local queue is empty, it examines peer processor queues and pulls runnable threads. This balances load while maintaining cache affinity preference.

**Priority Composition:**

Thread priority typically combines multiple components:

```
Total_Priority = Base_Priority + Affinity_Component + Age_Component
```

- **Base Priority:** Initial static priority
- **Affinity Component:** Derived from affinity policy (MI, MI+Q)
- **Age Component:** "Senior citizen discount" to prevent starvation

### Performance Metrics

| Metric | Perspective | Description |
|--------|-------------|-------------|
| Throughput | System-centric | Threads completed per unit time |
| Response Time | User-centric | Time from arrival to completion |
| Variance | User-centric | Consistency of response times |

### Load-Aware Scheduling

The optimal scheduling policy depends on system load:

**Light to Medium Load:**
- MI and MI+Q policies effective
- Caches remain relatively warm
- Affinity benefits outweigh scheduling overhead

**Heavy Load:**
- Fixed processor may be preferable
- Caches likely polluted regardless
- Affinity benefits diminish
- Simpler policy reduces overhead

**Adaptive Approach:**
An agile operating system may dynamically select scheduling policies based on current load and thread characteristics.

### Procrastination

A processor may insert an idle loop rather than immediately scheduling a low-affinity thread, hoping a high-affinity thread becomes runnable shortly. This optimization can improve overall throughput by maintaining cache warmth.

**Trade-off:**
- Benefit: Better cache utilization
- Cost: Temporarily idle processor

### Multicore and Hardware Multithreading

Modern multicore processors feature multiple cores per chip, often with hardware multithreading (simultaneous multithreading or SMT) supporting multiple hardware threads per core.

**Example Configuration:**
- 4 cores per chip
- 4 hardware threads per core
- 16 total hardware threads
- Shared L2 or L3 cache

**Hardware Multithreading:**
The hardware automatically switches between threads during long-latency operations (cache misses, memory accesses) to keep the core busy.

**OS Goal:**
Schedule threads such that their collective working sets fit within the last-level cache (LLC). If the working set exceeds LLC capacity, frequent off-chip memory accesses degrade performance.

### Cache-Aware Scheduling for Multicore

**Profiling:**
Categorize threads through runtime profiling:
- **Cache Frugal:** Small working set
- **Cache Hungry:** Large working set

**Scheduling Decision:**
Select a set of threads such that:
```
sum(working_set_size[threads]) ≤ LLC_capacity
```

**Example:**
For 16 hardware threads and 8MB L3 cache, select threads whose combined working sets total less than 8MB.

**Challenges:**
- Profiling overhead must be minimized
- Working set size changes dynamically
- Scheduling is NP-complete, requiring heuristics

**Research Status:**
Scheduling for parallel systems remains an active research area. Optimal algorithms for various workload characteristics and architectural configurations have not been definitively established.

## Scalable OS Design

Designing scalable operating systems for shared-memory multiprocessors requires addressing fundamental challenges that limit performance as processor count increases.

### Challenges in Parallel OS Design

**1. OS Bloat and System Software Bottlenecks**

Modern operating systems contain millions of lines of code. Global data structures and centralized services become serialization points, limiting parallelism.

**2. Memory Latency**

The processor-to-memory speed gap exceeds 100:1 and continues growing. Even cache hits at L2 or L3 incur significant latency compared to register access.

**3. NUMA Effects**

In distributed shared memory systems, local memory access is significantly faster than remote memory access. OS must be NUMA-aware to minimize remote accesses.

**4. Deep Memory Hierarchy**

Multiple cache levels (L1, L2, L3) before main memory increase complexity. OS decisions affect which level of the hierarchy data resides in.

**5. False Sharing**

Large cache block sizes (typically 64 bytes) mean programmatically unrelated data items may reside in the same cache block. When different processors write to different items in the same block, cache coherence protocols treat it as shared data, causing unnecessary invalidations and coherence traffic.

**Example:**
```
struct {
    int counter_A;  // Updated by P1
    int counter_B;  // Updated by P2
} shared_data;
```

If counter_A and counter_B reside in the same cache line, updates by P1 and P2 cause false sharing despite no programmatic relationship.

### Design Principles for Scalable OS

**1. Cache-Conscious Decisions**

Pay attention to spatial and temporal locality. Design data structures and algorithms to exploit cache hierarchies.

**2. Minimize Sharing**

"Shared memory machines scale well when you don't share memory." Limit sharing of kernel data structures to reduce contention and coherence overhead.

**3. Keep Memory Accesses Local**

In NUMA systems, allocate memory close to processors that will access it. Reduce inter-node memory traffic.

**4. Avoid False Sharing**

Align frequently updated data structures to cache line boundaries. Pad structures to ensure independent data items occupy separate cache lines.

### Case Study: Page Fault Service

Page fault handling illustrates typical parallelism bottlenecks in OS services.

**Workflow:**
1. Virtual address generated
2. TLB lookup (fast path)
3. Page table walk if TLB miss
4. Page fault if page not present
5. OS allocates physical page frame (PFN)
6. OS performs I/O to load page
7. OS updates page table
8. OS updates TLB

**Bottlenecks:**
- Physical page frame allocation (shared allocator)
- Page table updates (shared data structure)
- Global locks protecting page table

**Parallelizable Operations:**
- TLB lookups (processor-local)
- I/O operations (independent for different pages)
- Page table walks (read-only, can be concurrent)

### Recipe for Scalable Parallel OS

**Step 1: Functional Decomposition**

Identify the functionality and service requirements.

**Step 2: Minimize Shared Data Structures**

Only with minimal shared data structures can services execute truly concurrently. This is the critical step.

**Step 3: Logical vs. Physical Design**

- **Logical Design:** Present a clean abstraction with shared data structures
- **Physical Implementation:** Replicate or partition data structures to enable concurrency

### Tornado OS: Clustered Objects

Tornado, developed at the University of Toronto, exemplifies scalable OS design through its **clustered objects** approach: a single object reference (logical) has multiple physical representations (replicas or partitions). OS components see one logical object, but the implementation can be replicated (per-CPU, per-core) or partitioned based on access patterns. Software explicitly manages consistency across replicas, minimizing reliance on hardware cache coherence.

#### Object-Oriented Memory Management

Tornado decomposes memory management into a hierarchy of clustered objects. For example, during a page fault: Process Object → Region Object (address space portion) → File Cache Manager → Page Frame Manager & I/O handler. Each object can have different replication strategies: Process Objects are replicated per-CPU (mostly read-only), Region Objects are partitioned for concurrent page fault handling, and physical memory managers reduce allocation contention through partitioning.

#### Key Benefits

- **Simplified logical design:** Components use consistent interfaces regardless of physical representation
- **Incremental optimization:** Start with singleton, add replication based on profiling
- **Reduced lock contention:** Replicas enable independent concurrent access
- **Optimized common case:** Frequent operations (page faults) scale well; rare operations may have overhead but don't impact overall performance

#### Non-Hierarchical Locking

Traditional hierarchical locking (lock entire object chain: Process → Region → FCM → I/O) prevents concurrent page faults in different regions. Tornado uses **reference counting** instead: increment ref_count on access, decrement after operation. This prevents object destruction during use but doesn't block concurrent access by other threads, enabling parallel operations on different regions with locks scoped to individual objects only.

#### Additional Optimizations

**Software-Managed Consistency:** Updates propagated selectively to relevant replicas only (not broadcast like hardware cache coherence), reducing unnecessary coherence traffic.

**NUMA-Aware Allocation:** Heap space partitioned and allocated from local physical memory, reducing central allocator contention and minimizing remote memory accesses.

#### Inter-Process Communication

Objects communicate via protective procedure calls. Local IPC (same processor) uses handoff scheduling without context switching; remote IPC (different processors) requires full context switches. IPC mechanisms also maintain consistency among object replicas.

### Alternative Approaches

#### Corey System (MIT)

Similar principles to Tornado with application involvement:

**Address Ranges:**
Applications provide hints about memory regions they will operate on, allowing OS to partition structures accordingly.

**Shares:**
Applications hint whether resources (e.g., file descriptors) will be shared or private, enabling optimizations.

**Dedicated Cores:**
Dedicating specific cores for kernel activity improves locality for kernel data structures.

#### Cellular Disco (Stanford)

Addresses device driver portability in parallel systems through virtualization.

**Problem:**
Optimizing OS for every parallel architecture is expensive, especially rewriting device drivers.

**Solution:**
Thin virtualization layer (VMM) between guest OS and host OS:

- Guest OS (e.g., IRIX) runs unmodified on VMM
- Host OS (e.g., on Origin 2000 SMP) provides device drivers
- VMM translates guest I/O requests to host OS calls
- Minimal overhead (often < 10% for many applications)

**I/O Handling:**
1. Guest OS issues I/O operation
2. Traps to VMM (trap and emulate)
3. VMM rewrites as its own request
4. Passes to host OS
5. Host completes I/O
6. Interrupt directed to VMM
7. VMM emulates interrupt to guest

**Benefits:**
- Avoids rewriting device drivers for each guest OS
- Leverages existing host OS functionality
- VMM manages multiprocessor resources efficiently
- Enables OS heterogeneity on parallel hardware

## Related Topics

- **[Synchronization](Synchronization.md)** - Comprehensive coverage of synchronization primitives and algorithms
- **[Process and Thread](Process%20and%20Thread.md)** - Process and thread fundamentals, scheduling, and IPC
- **[Memory Management](Memory%20Management.md)** - Virtual memory, page tables, and memory hierarchies
- **[Introduction](Introduction.md)** - Operating system architectures and design principles

## References

**Course Materials:**
- cs6210: Advanced Operating Systems - Georgia Tech OMSCS

**Foundational Papers:**

- Tornado: Maximizing Locality and Concurrency in a Shared Memory Multiprocessor Operating System - University of Toronto (Clustered Objects)

