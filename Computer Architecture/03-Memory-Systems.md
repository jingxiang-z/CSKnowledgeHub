# CPU Memory Systems

## Table of Contents
1. [Introduction](#introduction)
2. [Memory Hierarchy](#memory-hierarchy)
3. [Cache Architecture](#cache-architecture)
4. [Cache Optimizations](#cache-optimizations)
5. [Virtual Memory](#virtual-memory)
6. [Multi-Core Memory Systems](#multi-core-memory-systems)
7. [Cache Coherence](#cache-coherence)
8. [Memory Consistency](#memory-consistency)
9. [Synchronization](#synchronization)
10. [References](#references)

## Introduction

The memory system is a critical component of modern computer architecture. The performance gap between fast processors and slow memory—known as the **memory wall**—necessitates a complex hierarchy of memory technologies that balance speed, capacity, and cost.

### The Memory Wall

While processor speed has improved exponentially (Moore's Law), memory latency has improved at a much slower rate (approximately 1.1× every two years). This growing disparity makes memory access a primary performance bottleneck. The memory hierarchy, with its multiple levels of caching, is the architectural solution to this problem.

### Key Principles

Memory hierarchy design exploits two fundamental principles:

**Temporal Locality**: If a piece of data is accessed, it is likely to be accessed again soon. Caches store recently accessed data to make future accesses faster.

**Spatial Locality**: If a piece of data is accessed, data located nearby is likely to be accessed soon. Caches load blocks of contiguous data to exploit this pattern.

## Memory Hierarchy

Modern systems employ a multi-level hierarchy of memory technologies, each with different characteristics:

| Level | Type | Typical Size | Latency | Bandwidth | Volatile |
|-------|------|--------------|---------|-----------|----------|
| **Registers** | SRAM | 128-256 bytes | <1 ns (~1 cycle) | ~1 TB/s | Yes |
| **L1 Cache** | SRAM | 32-64 KB per core | ~1 ns (~4 cycles) | ~1 TB/s | Yes |
| **L2 Cache** | SRAM | 256 KB-2 MB per core | ~3-5 ns (~12 cycles) | ~500 GB/s | Yes |
| **L3 Cache** | SRAM | 4-64 MB shared | ~10-20 ns (~40 cycles) | ~300 GB/s | Yes |
| **Main Memory** | DRAM | 8-128 GB | ~50-100 ns (~200 cycles) | ~50-100 GB/s | Yes |
| **SSD** | Flash NAND | 256 GB-4 TB | ~100 μs | ~3-7 GB/s | No |
| **HDD** | Magnetic | 1-20 TB | ~5-10 ms | ~100-200 MB/s | No |

**Design Principle**: Each level serves as a cache for the next level, with data automatically promoted to faster levels upon access.

## Cache Architecture

Caches are small, fast SRAM-based memories that store recently accessed data from main memory.

### Cache Organization Fundamentals

**Cache Size**: Total storage capacity (e.g., 32 KB, 256 KB, 8 MB)

**Cache Line (Block)**: The smallest unit of data transfer between cache and memory, typically 64 bytes in modern processors

**Cache Line Structure**:
```
[ Valid Bit | Dirty Bit | Tag | Data Block (64 bytes) ]
```
- **Valid Bit**: Indicates if the line contains valid data
- **Dirty Bit**: Indicates if data has been modified (for write-back caches)
- **Tag**: Identifies which memory block is stored in this line
- **Data Block**: The actual cached data

### Address Breakdown

A memory address is divided into three parts for cache lookup:

```
Memory Address (e.g., 64-bit):
┌─────────────────┬──────────────┬────────────┐
│      Tag        │    Index     │   Offset   │
└─────────────────┴──────────────┴────────────┘
```

- **Offset**: Selects specific byte within cache line (6 bits for 64-byte line)
- **Index**: Selects which cache set to check
- **Tag**: Identifies which specific memory block is in that set

### Cache Organization Types

#### 1. Direct-Mapped Cache

Each memory block maps to exactly one cache line.

**Index Calculation**: `cache_line = (address / block_size) % num_lines`

**Example**:
```
Address: 0x1234
Block size: 64 bytes
Cache: 1024 lines

Index = (0x1234 / 64) % 1024 = 73
Memory block 0x1234 can ONLY go to line 73
```

**Advantages**:
- Simple and fast
- Single comparison needed
- Low hardware cost

**Disadvantages**:
- High conflict miss rate
- Poor utilization if addresses map to same line

#### 2. Fully Associative Cache

Any memory block can be placed in any cache line.

**Address Structure**: Only Tag and Offset (no Index)

**Lookup**: Must check all cache lines in parallel

**Advantages**:
- Lowest conflict miss rate
- Best cache utilization

**Disadvantages**:
- Complex hardware (requires parallel comparators for all lines)
- Slow and power-hungry
- Doesn't scale to large sizes

**Use Case**: TLBs (small, fully associative)

#### 3. N-Way Set-Associative Cache

A compromise between direct-mapped and fully associative. Cache is divided into sets, and each memory block can map to any line within its designated set.

**Structure**: `num_sets = num_lines / associativity`

**Example (4-way set-associative)**:
```
Cache with 1024 lines, 4-way set-associative:
256 sets × 4 ways = 1024 lines

Set 0:  [ Way 0 | Way 1 | Way 2 | Way 3 ]
Set 1:  [ Way 0 | Way 1 | Way 2 | Way 3 ]
...
Set 255:[ Way 0 | Way 1 | Way 2 | Way 3 ]

Address maps to one set, can use any of 4 ways
```

**Advantages**:
- Balances complexity and performance
- Significantly reduces conflict misses compared to direct-mapped
- Moderate hardware cost (4 or 8 parallel comparisons)

**Disadvantages**:
- More complex than direct-mapped
- Requires replacement policy

**Typical Configurations**: 4-way to 16-way for L1/L2 caches

### Cache Lookup Process

1. **Extract fields** from memory address (Tag, Index, Offset)
2. **Index lookup**: Use Index to select cache set
3. **Tag comparison**: Compare Tag with all ways in the set in parallel
4. **Hit/Miss determination**:
   - **Cache Hit**: Tag matches and Valid=1 → Read data using Offset
   - **Cache Miss**: No matching tag → Fetch block from next memory level

**Hit Time**: Time to determine hit/miss and read data (~1-4 cycles for L1)

### Replacement Policies

When a set is full and a new block needs to be loaded, a replacement policy decides which block to evict.

#### Least Recently Used (LRU)

Evicts the block that hasn't been accessed for the longest time.

**Implementation**:
- **2-way**: Single bit (MRU indicator)
- **4-way**: 3-bit pseudo-LRU tree
- **8-way**: 7-bit pseudo-LRU tree or timestamp-based approximation

**Advantages**: Exploits temporal locality well

**Disadvantages**: Complex to implement perfectly for high associativity

#### Pseudo-LRU (PLRU)

Approximates LRU with less hardware:
- Use a tree of bits to track relative recency
- Not always evicts true LRU but close enough

#### Other Policies

- **First In, First Out (FIFO)**: Evicts oldest block by insertion time
- **Random**: Randomly selects a block to evict (surprisingly effective and simple)
- **Least Frequently Used (LFU)**: Evicts block with fewest accesses

### Write Policies

Determine how writes are handled in the cache hierarchy.

#### Write-Hit Policies

**Write-Through**:
- Write updates both cache and next level (memory) simultaneously
- **Pros**: Simplifies coherence, always consistent
- **Cons**: High memory traffic, slower writes

**Write-Back**:
- Write only updates cache; set Dirty bit
- Write to memory only when line is evicted
- **Pros**: Reduced memory traffic, faster writes
- **Cons**: More complex, need dirty bit, potential inconsistency

**Modern Standard**: Write-back is used in nearly all modern processors due to performance benefits.

#### Write-Miss Policies

**Write-Allocate**:
- On write miss, fetch block into cache, then write
- Usually paired with write-back
- **Pros**: Future accesses benefit from cached data

**No-Write-Allocate**:
- On write miss, write directly to memory, don't load into cache
- Usually paired with write-through
- **Pros**: Avoids polluting cache with write-only data

### Performance Metrics

**Average Memory Access Time (AMAT)**: The primary cache performance metric:

$$
AMAT = Hit\ Time + (Miss\ Rate \times Miss\ Penalty)
$$

**Example**:
- L1 Hit Time: 1 cycle
- L1 Miss Rate: 5%
- L2 Access Time (Miss Penalty): 10 cycles

$$
AMAT = 1 + (0.05 \times 10) = 1.5\ cycles
$$

**Multi-Level AMAT**:
$$
AMAT = Hit\ Time_{L1} + (Miss\ Rate_{L1} \times Hit\ Time_{L2}) + (Miss\ Rate_{L1} \times Miss\ Rate_{L2} \times Miss\ Penalty_{L2})
$$

### Cache Miss Types (3 C's)

**Compulsory Misses**: First access to a block (cold start)
- **Reduction**: Prefetching, larger block size

**Capacity Misses**: Cache is too small to hold all needed blocks
- **Reduction**: Larger cache

**Conflict Misses**: Blocks map to same set/line, evicting each other despite available space elsewhere
- **Reduction**: Higher associativity

**Coherence Misses** (multi-core): Another processor invalidates this core's copy
- **Reduction**: Cache coherence protocol optimization

## Cache Optimizations

Modern processors employ sophisticated techniques to optimize the three components of AMAT.

### Reducing Hit Time

#### 1. Smaller, Faster L1 Caches

Keep L1 small (32-64 KB) to minimize access latency. Use L2/L3 for capacity.

#### 2. Pipelined Cache Access

Break cache access into multiple pipeline stages to achieve higher clock frequencies, though it increases latency in cycles.

#### 3. Virtually Indexed, Physically Tagged (VIPT) Caches

Use virtual address bits for Index (fast) and physical address bits for Tag (correct).

**Constraint**: Cache size must satisfy:
$$
Cache\ Size \leq Associativity \times Page\ Size
$$

For 4 KB pages: 4-way set-associative cache can be up to 16 KB.

**Benefit**: TLB lookup and cache index can happen in parallel, reducing hit time.

#### 4. Way Prediction

In set-associative caches, predict which way will hit to reduce latency:
- Access predicted way first
- If wrong, check other ways in next cycle
- 90%+ prediction accuracy makes this effective

### Reducing Miss Rate

#### 1. Larger Cache Size

More capacity reduces capacity misses but increases hit time and cost.

#### 2. Higher Associativity

Reduces conflict misses:
- Direct-mapped → 2-way: ~50% miss rate reduction
- 2-way → 4-way: ~20% miss rate reduction
- 4-way → 8-way: ~10% miss rate reduction
- Diminishing returns beyond 8-way

#### 3. Larger Block Size

Exploits spatial locality better:
- Typical: 64-byte blocks
- **Trade-off**: Too large increases miss penalty and can cause cache pollution

#### 4. Prefetching

Fetch data into cache before it's explicitly requested.

**Hardware Prefetching**:
- Detects access patterns (sequential, stride-based)
- Automatically issues prefetch requests
- **Example**: If accessing addresses 0x100, 0x140, 0x180 (stride=64), prefetch 0x1C0

**Software Prefetching**:
- Compiler inserts prefetch instructions
- **Example**:
  ```c
  for (i = 0; i < N; i++) {
      __builtin_prefetch(&a[i+8]);  // Prefetch 8 iterations ahead
      result += a[i] * b[i];
  }
  ```

**Challenges**: Must balance prefetch aggressiveness vs. bandwidth waste and cache pollution.

#### 5. Compiler Optimizations

**Loop Interchange**: Reorder nested loops to improve spatial locality:
```c
// Original (poor locality in C):
for (i = 0; i < N; i++)
    for (j = 0; j < M; j++)
        sum += A[j][i];  // Column-wise access

// Optimized (good locality):
for (j = 0; j < M; j++)
    for (i = 0; i < N; i++)
        sum += A[j][i];  // Row-wise access
```

**Loop Blocking (Tiling)**: Break large loops into smaller blocks that fit in cache:
```c
// Matrix multiply with blocking:
for (ii = 0; ii < N; ii += BLOCK_SIZE)
    for (jj = 0; jj < N; jj += BLOCK_SIZE)
        for (kk = 0; kk < N; kk += BLOCK_SIZE)
            for (i = ii; i < ii+BLOCK_SIZE; i++)
                for (j = jj; j < jj+BLOCK_SIZE; j++)
                    for (k = kk; k < kk+BLOCK_SIZE; k++)
                        C[i][j] += A[i][k] * B[k][j];
```

### Reducing Miss Penalty

#### 1. Multi-Level Caches

Create a hierarchy (L1, L2, L3) where misses in faster caches are served by slower ones before going to main memory.

**Typical Configuration**:
- L1: 32-64 KB, 4-way, 4 cycles
- L2: 256 KB-1 MB, 8-way, 12 cycles
- L3: 8-32 MB, 16-way, 40 cycles
- Main Memory: GB-scale, 200+ cycles

#### 2. Non-Blocking Caches

Allow cache to continue serving hits while handling outstanding misses.

**Hit-Under-Miss**: Service cache hits while one miss is outstanding

**Miss-Under-Miss**: Handle multiple simultaneous misses (Memory-Level Parallelism)

**Implementation**: **Miss Status Handling Registers (MSHRs)** track in-progress misses:
- Typical: 8-16 MSHRs per core
- Each MSHR tracks one outstanding miss
- Subsequent accesses to same block wait on that MSHR (don't generate duplicate requests)

#### 3. Critical Word First

When fetching a cache line, send the requested word first:
- Processor can resume while rest of line loads
- Reduces effective miss penalty by ~50% for large blocks

#### 4. Early Restart

As soon as requested word arrives, forward it to processor before entire line is loaded.

## Virtual Memory

Virtual memory provides each program with its own large, private address space, mapped by the OS to smaller physical memory.

### Mechanism

**Paging**: Memory is divided into fixed-size pages (typically 4 KB, sometimes 2 MB or 1 GB "huge pages").

**Page Table**: Data structure mapping virtual page numbers to physical frame numbers, maintained by OS.

**Translation**:
```
Virtual Address:
┌─────────────────────┬─────────────┐
│  Virtual Page Number │   Offset    │
└─────────────────────┴─────────────┘
            ↓ (Page Table Lookup)
Physical Address:
┌─────────────────────┬─────────────┐
│ Physical Frame Number│   Offset    │
└─────────────────────┴─────────────┘
```

### Translation Lookaside Buffer (TLB)

A small, dedicated cache storing recent virtual-to-physical page translations.

**Typical Specifications**:
- **Size**: 64-2048 entries
- **Organization**: Fully associative or highly associative (8-way to 16-way)
- **Separate or Unified**: Often separate I-TLB (instruction) and D-TLB (data)
- **Levels**: Modern processors have L1 and L2 TLBs

**TLB Entry**:
```
[ Valid | VPN | PFN | Permissions (R/W/X) | Dirty | Access Time ]
```

### Address Translation Process

1. **TLB Lookup**: Check if VPN is in TLB
   - **TLB Hit**: Use PFN immediately (~1 cycle)
   - **TLB Miss**: Proceed to page table walk

2. **Page Table Walk** (on TLB miss):
   - Modern systems use multi-level page tables (4 levels for x86-64)
   - Each level is a memory access (~200 cycles each)
   - Total cost: 800+ cycles for a TLB miss with page walk

3. **Page Fault** (if page not in physical memory):
   - OS loads page from disk (millions of cycles)
   - Updates page table
   - Resumes instruction

**Performance Impact**: TLB misses can severely degrade performance. Large pages (2 MB or 1 GB) reduce TLB misses by covering more address space per entry.

### TLB and Cache Interaction

**Virtually Indexed, Physically Tagged (VIPT)**:
- Best of both worlds: fast indexing, correct tagging
- TLB and cache lookup happen in parallel
- Commonly used in L1 caches

**Physical Addressing**:
- Cache indexed and tagged with physical address
- Must wait for TLB translation
- Used in L2/L3 caches

## Multi-Core Memory Systems

Multi-core processors introduce new challenges in memory system design due to shared resources and the need for cache coherence.

### Shared vs. Private Caches

**Private L1/L2 Caches**:
- Each core has its own L1 and L2 caches
- **Pros**: Low latency, no contention
- **Cons**: Requires coherence protocol, potential duplication

**Shared L3 Cache**:
- Single large cache shared by all cores
- **Pros**: Better capacity utilization, natural data sharing
- **Cons**: Higher latency, potential contention

**Typical Modern Configuration**:
```
Core 0: [L1-I] [L1-D] [L2]
Core 1: [L1-I] [L1-D] [L2]
Core 2: [L1-I] [L1-D] [L2]
Core 3: [L1-I] [L1-D] [L2]
        └──────────┬──────────┘
          Shared [L3 Cache]
                 │
           [Main Memory]
```

## Cache Coherence

In shared-memory multiprocessors with private caches, multiple copies of the same memory block can exist. **Cache coherence** ensures all cores see a consistent view of memory.

### Coherence Definition

A system is coherent if:

1. **Read after Write**: A read by processor P1 returns the value of the last write to that location (by any processor)
2. **Write Serialization**: All processors see writes to the same location in the same order

### Coherence Protocols

#### Snooping-Based Protocols

All cache controllers monitor (snoop) a shared bus to observe memory transactions.

**Operation**:
- On a memory operation, broadcast on bus
- All caches check their tags
- Take action to maintain coherence

**Limitation**: Does not scale beyond ~16 cores due to bus contention

#### Directory-Based Protocols

A central or distributed directory maintains the state of each memory block.

**Directory Entry** tracks:
- Which caches have a copy
- Whether any copy is modified

**Operation**:
- Requests sent to directory
- Directory sends targeted messages to relevant cores
- No broadcast needed

**Scalability**: Scales to hundreds of cores (used in large multi-socket servers)

### MSI Protocol

A simple coherence protocol with three states per cache line:

**States**:

- **Modified (M)**: This cache has the only valid, modified copy (exclusive ownership)
  - Memory is stale
  - Must write back on eviction

- **Shared (S)**: Multiple caches may have clean copies
  - Memory is up-to-date
  - Can be read but not written without transitioning to M

- **Invalid (I)**: Cache line does not contain valid data

**State Transitions** (simplified):

```
         Read Miss
    ┌─────────────────┐
    │                 ↓
  [I] ──Write──→ [M] ←──Write──── [S]
    │     ↑            │              ↑
    └──────┴────────────┴──────────────┘
         Read from other core / Write-back
```

**Example**:
```
Core 0 reads X:    I → S (fetch from memory)
Core 1 reads X:    I → S (share from memory)
Core 0 writes X:   S → M (invalidate Core 1, gain exclusive ownership)
Core 1 state:      S → I (invalidated by Core 0's write)
Core 1 reads X:    I → S (fetch from Core 0's M copy, Core 0 downgrades M → S)
```

### MOSI / MOESI Protocols

Enhanced protocols adding additional states for optimization:

**Owned (O)**: Dirty data but other shared copies exist
- Allows cache-to-cache transfer of modified data without writing to memory
- Reduces memory traffic

**Exclusive (E)**: Clean, exclusive copy (only this cache has it)
- Allows silent transition to M on write (no bus transaction needed)
- Distinguishes "I'm the only one with this" from "others might have this too"

**MOESI State Machine**: 5 states providing optimal performance
- **M**: Modified, exclusive, dirty
- **O**: Owned, shared, dirty (can service read requests)
- **E**: Exclusive, clean
- **S**: Shared, clean
- **I**: Invalid

**Benefit**: Reduces bus traffic and memory writes, improves performance

### Coherence Traffic and Performance Impact

**Coherence Misses**: A new class of cache misses in multi-core systems
- **True Sharing**: Multiple cores access same data (necessary communication)
- **False Sharing**: Different data in same cache line accessed by different cores

**False Sharing Example**:
```c
struct {
    int counter0;  // Used by thread 0
    int counter1;  // Used by thread 1
} shared;  // Both in same 64-byte cache line

// Each increment causes coherence traffic even though different variables!
```

**Solution**: Pad data structures to align to cache line boundaries

## Memory Consistency

While coherence defines ordering for accesses to a single location, **memory consistency** defines ordering for accesses to different locations.

### Sequential Consistency (SC)

The strongest model: execution appears as if all memory operations from all processors were executed in some single sequential order, with operations of each processor appearing in program order.

**Guarantee**: What you expect from sequential programming

**Cost**: Severely restricts compiler and hardware optimizations (no reordering, no overlapping)

**Example**:
```
Core 0:     Core 1:
A = 1       B = 1
r1 = B      r2 = A

SC guarantees: (r1, r2) cannot be (0, 0)
```

### Relaxed Consistency Models

Weaken ordering constraints to allow higher performance.

**Weak Ordering**: Ordinary accesses can be reordered; synchronization operations (fences) enforce ordering

**Release Consistency**:
- **Acquire**: Before entering critical section (barrier, lock acquire)
- **Release**: After exiting critical section (barrier, lock release)
- Compiler and hardware can reorder operations between acquire-release pairs

**Total Store Order (TSO)** (x86, SPARC):
- Writes can be buffered and reordered with respect to subsequent reads
- Writes to same location remain ordered

**Benefit**: Allows better performance through store buffers and non-blocking caches

**Requirement**: Programmers must use explicit fences/barriers for correctness

## Synchronization

Parallel programs require synchronization to coordinate access to shared data.

### Atomic Instructions

Hardware primitives providing indivisible read-modify-write operations:

#### Atomic Exchange (Swap)
```assembly
XCHG reg, mem    # Atomically swap reg ↔ mem
```

#### Test-and-Set
```c
bool test_and_set(bool *lock) {
    bool old = *lock;
    *lock = true;
    return old;  // All atomic
}
```

#### Compare-and-Swap (CAS)
```c
bool CAS(int *ptr, int expected, int new_value) {
    if (*ptr == expected) {
        *ptr = new_value;
        return true;
    }
    return false;  // All atomic
}
```

#### Load-Linked / Store-Conditional (LL/SC)

A more efficient pair of instructions (used in ARM, RISC-V, PowerPC):

```assembly
LL   R1, (R2)        # Load-linked: load value and mark address
# ... compute new value ...
SC   R3, (R2)        # Store-conditional: store only if no intervening write
                     # Returns 1 if successful, 0 if failed
```

**Advantage**: No bus locking during spin-wait (unlike XCHG), reduces contention

### Locks (Mutual Exclusion)

Ensure only one thread executes a critical section at a time.

#### Simple Spinlock

```c
typedef struct { volatile int locked; } spinlock_t;

void acquire(spinlock_t *lock) {
    while (test_and_set(&lock->locked))
        ;  // Spin until acquired
}

void release(spinlock_t *lock) {
    lock->locked = 0;
}
```

**Problem**: Heavy bus traffic from spinning

#### Test-and-Test-and-Set (TATAS)

```c
void acquire(spinlock_t *lock) {
    while (1) {
        while (lock->locked)  // Spin on cached copy (no bus traffic)
            ;
        if (!test_and_set(&lock->locked))
            return;  // Acquired!
    }
}
```

**Improvement**: Only generates bus traffic when lock appears available

#### Ticket Lock

Provides fairness (FIFO ordering):

```c
typedef struct {
    volatile int next_ticket;
    volatile int now_serving;
} ticketlock_t;

void acquire(ticketlock_t *lock) {
    int my_ticket = atomic_inc(&lock->next_ticket);
    while (lock->now_serving != my_ticket)
        ;  // Wait for our turn
}

void release(ticketlock_t *lock) {
    lock->now_serving++;
}
```

### Barriers

Synchronization point where all threads must arrive before any can proceed.

#### Centralized Barrier

```c
typedef struct {
    volatile int counter;
    int num_threads;
} barrier_t;

void barrier(barrier_t *b) {
    atomic_dec(&b->counter);
    while (b->counter > 0)
        ;  // Wait for all threads
    if (last_thread)
        b->counter = b->num_threads;  // Reset for next use
}
```

**Problem**: Serial arrival, cache line bouncing

#### Tree Barrier

Threads synchronize in tree structure to reduce contention (O(log N) depth instead of O(N)).

#### Sense-Reversing Barrier

Alternates a "sense" bit to allow reuse without race conditions:

```c
typedef struct {
    volatile int counter;
    volatile bool sense;
    int num_threads;
} barrier_t;

void barrier(barrier_t *b) {
    bool my_sense = local_sense;
    if (atomic_dec(&b->counter) == 0) {
        b->counter = b->num_threads;
        b->sense = my_sense;  // Release all waiters
    } else {
        while (b->sense != my_sense)
            ;  // Spin until released
    }
    local_sense = !local_sense;
}
```

## References

This document synthesizes memory system design principles from:

- **Georgia Institute of Technology** - OMSCS CS 6200 and CS 6210 graduate courses
- **Columbia University** - Graduate Computer Science courses
- Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach* (6th ed.). Morgan Kaufmann
- Culler, D. E., Singh, J. P., & Gupta, A. (1998). *Parallel Computer Architecture: A Hardware/Software Approach*. Morgan Kaufmann
- Sorin, D. J., Hill, M. D., & Wood, D. A. (2011). *A Primer on Memory Consistency and Cache Coherence*. Morgan & Claypool Publishers

For related topics, see:
- [01-Fundamentals.md](01-Fundamentals.md) - Basic architecture and performance
- [02-Processor-Design.md](02-Processor-Design.md) - Pipeline and out-of-order execution
- [04-Storage-Systems.md](04-Storage-Systems.md) - Secondary storage and RAID systems
