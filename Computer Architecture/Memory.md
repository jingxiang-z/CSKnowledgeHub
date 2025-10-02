## Cache

### Introduction

- Cache Mechanism: Cache memory is a type of high-speed volatile computer memory that provides high-speed data access to the CPU and improves overall system performance.

  - **Temporal Locality:** If a piece of data is accessed, it is likely to be accessed again soon. Cache stores this data so that future accesses can be faster.

  - **Spatial Locality:** If a piece of data is accessed, data located near it is likely to be accessed soon. Cache loads blocks of data to take advantage of this pattern.

- Cache Levels:

  - **L1 Cache:** The Level 1 cache is the smallest and fastest cache, located closest to the CPU. It is usually divided into separate instruction and data caches (L1i and L1d).
  - **L2 Cache:** The Level 2 cache is larger and slightly slower than the L1 cache. It serves as a secondary cache that stores data not found in the L1 cache.
  - **L3 Cache:** The Level 3 cache is larger and slower than L2 but faster than the main memory. It is shared among the cores of a multi-core processor.

### Performance

**Average Memory Access Time (AMAT)** is a critical metric used to evaluate the performance of cache memory in computer systems.

1. **Hit Time (HT):** The time it takes to access data from the cache when there is a cache hit. This includes the time to determine if the data is in the cache and to read it.
2. **Miss Rate (MR):** The percentage of memory accesses that result in a cache miss. It is the ratio of the number of cache misses to the total number of memory accesses.
3. **Miss Penalty (MP):** The additional time required to fetch data from the next level of the memory hierarchy (e.g., main memory or a lower-level cache) when a cache miss occurs.

$$
AMAT=Hit Time+(Miss Rate×Miss Penalty)
$$

### Organization

- **Cache Size**

  - **Definition:** The total storage capacity of the cache, typically measured in kilobytes (KB), megabytes (MB), or gigabytes (GB).

  - **Impact:** A larger cache can store more data, reducing the miss rate and improving performance. However, larger caches are more expensive and can have higher access latencies.

- **Cache Lines (Blocks)**

  - **Definition:** The smallest unit of data that can be stored in the cache. Each cache line or block typically ranges from 32 to 128 bytes in size.

  - Structure:
    - **Data Field:** Stores the actual data from memory.
    - **Tag Field:** Identifies the memory address of the data stored in the cache line.
    - **Status Bits:** Include valid bits (indicating if the data is valid) and dirty bits (indicating if the data has been modified).

- **Direct-Mapped Cache:**

  - **Structure:** Each block of main memory maps to exactly one cache line.

  - Indexing:

     The memory address is divided into three parts: tag, index, and offset.

    - **Tag:** Identifies the specific block.
    - **Index:** Identifies the specific cache line.
    - **Offset:** Identifies the specific byte within the cache line.

  - **Advantages:** Simple and fast to access.

  - **Disadvantages:** High conflict miss rate, as multiple memory blocks can map to the same cache line.

- **Fully Associative Cache:**

  - **Structure:** Any block can be stored in any cache line.

  - Indexing:

     The memory address is divided into tag and offset.

    - **Tag:** Identifies the specific block.
    - **Offset:** Identifies the specific byte within the cache line.

  - **Advantages:** Low conflict miss rate.

  - **Disadvantages:** Complex and slower due to the need for associative search.

- **Set-Associative Cache:**

  - **Structure:** Compromise between direct-mapped and fully associative caches. Memory blocks are divided into sets, and each block can map to any line within a set.

  - Indexing:

     The memory address is divided into tag, set index, and offset.

    - **Tag:** Identifies the specific block.
    - **Set Index:** Identifies the specific set within the cache.
    - **Offset:** Identifies the specific byte within the cache line.

  - **Advantages:** Balances complexity and performance.

  - **Disadvantages:** More complex than direct-mapped but less flexible than fully associative.

### Cache Lookup

1. **Address Mapping:**
   - When the CPU needs to access data, it generates a memory address. The address is divided into three parts: tag, index, and offset.
     - **Tag:** Identifies the specific block of memory.
     - **Index:** Identifies the specific cache set.
     - **Offset:** Identifies the specific byte within the cache line.
2. **Cache Lookup Process:**
   - **Indexing:** The cache controller uses the index part of the address to locate the relevant set in the cache.
   - **Tag Comparison:** Within the identified set, the cache controller compares the tag part of the address with the tags stored in the cache lines to check for a match.
   - Hit or Miss:
     - **Cache Hit:** If a matching tag is found, it means the requested data is in the cache. The data is then accessed using the offset.
     - **Cache Miss:** If no matching tag is found, it means the data is not in the cache. The system then fetches the data from the next level of the memory hierarchy (L2, L3, or main memory).
3. **Handling Cache Misses:**
   - **Read Miss:** The data is fetched from the next memory level and loaded into the cache. If necessary, an existing cache line is evicted based on the replacement policy.
   - **Write Miss:** Depending on the write policy (write-through or write-back), the data is either written directly to the next memory level or marked as dirty and written back later.
4. **Cache Write Policies:**
   - **Write-Through:** Data is written to both the cache and the next memory level simultaneously. Ensures data consistency but can be slower.
   - **Write-Back:** Data is written only to the cache initially and marked as dirty. It is written back to the next memory level only when the cache line is evicted. This reduces write latency but requires more complex control logic.
5. **Replacement Policies:**
   - **Least Recently Used (LRU):** Replaces the cache line that has not been used for the longest time.
   - **First In, First Out (FIFO):** Replaces the oldest cache line.
   - **Random:** Replaces a randomly selected cache line.
   - **Least Frequently Used (LFU):** Replaces the cache line with the fewest accesses.

## Cache Improvement

1. **Reducing Hit Time**

   - Smaller, Faster Caches: Use a smaller L1 cache to keep the hit time low. Smaller caches are faster because they have less data to search through.

   - Optimized Cache Access Paths: Design the hardware to minimize the delay in accessing the cache. This includes optimizing the paths and logic gates involved in cache access.

   - Parallel Access: Allow simultaneous access to different parts of the cache to improve hit time, particularly useful for multi-core processors.

2. **Reducing Miss Rate**

   - Increasing Cache Size: Larger caches store more data, reducing the likelihood of cache misses. However, this comes with increased cost and potentially higher hit time.
     - Higher Associativity: Using set-associative or fully associative caches instead of direct-mapped caches can significantly reduce conflict misses.
     - Common configurations are 2-way, 4-way, 8-way set-associative caches, where each block can be placed in multiple locations.

   - Smarter Replacement Policies: Implementing more effective replacement policies like Least Recently Used (LRU) instead of simpler policies like FIFO can help keep more useful data in the cache.

   - Cache Line Size Optimization: Adjust the cache line size to balance spatial locality. Larger lines exploit spatial locality better but might lead to increased miss penalties if not utilized fully.

3. **Reducing Miss Penalty**

   - Multi-Level Caches: Use multiple levels of cache (L1, L2, L3) to create a hierarchy. Higher-level caches (L2, L3) can store more data and reduce the miss penalty when an L1 miss occurs.

   - Faster Memory Technologies: Use faster memory technologies (e.g., SRAM for caches, DDR for main memory) to reduce the time it takes to fetch data on a miss.

   - Prefetching: Implement hardware or software prefetching to load data into the cache before it is actually needed, thereby reducing miss penalties. Prefetching can be sequential (based on access patterns) or stride-based.

   - Write Policies: Use write-back caches instead of write-through caches to reduce the number of writes to main memory, thereby reducing miss penalties.

   - Non-Blocking Caches: Allow the cache to continue servicing requests while handling a miss, improving overall performance and reducing the effective miss penalty.

### Pipelined Cache

### TLB Cache Overlap

### Virtually Accessed Cache

### Way prediction

### Replacement Policy

 

## Main Memory

### Virtual Memory

- **Virtual Address Space:** Each process is given its own virtual address space, which the process uses to address memory. This space is larger than the actual physical memory and provides isolation between processes.
- **Paging:** Memory is divided into fixed-size blocks called pages. Virtual memory is managed in units of pages, and both virtual and physical memory are divided into pages of the same size (commonly 4KB).
- **Page Table:** A data structure used to map virtual addresses to physical addresses. Each process has its own page table, which the operating system maintains to keep track of the mapping between virtual and physical memory.
- **Page Frames:** The physical memory is divided into page frames, which are the same size as pages. Virtual pages are mapped to these physical page frames.

### TLB

- **Purpose:**The primary purpose of the TLB is to reduce the time required to translate virtual addresses to physical addresses. Without a TLB, each memory access would require traversing the page table, which is much slower.
- **Structure:**The TLB is a small, fast cache located within the CPU. It typically holds a limited number of entries, each mapping a virtual page number to a physical frame number.
- **TLB Entries:**
  - **Virtual Page Number (VPN):** The part of the virtual address that identifies the page.
  - **Physical Frame Number (PFN):** The part of the physical address that identifies the frame.
  - **Control Bits:** Including valid bits, dirty bits, and other status flags.

### Address Mapping

1. **Virtual Address Generation:** When an application accesses memory, it generates a virtual address. This virtual address consists of two main parts:
   - **Virtual Page Number (VPN):** Identifies the specific page in the virtual address space.
   - **Offset:** Identifies the specific byte within the page.
2. **TLB Lookup:**
   - The first step in address translation is to check the Translation Lookaside Buffer (TLB). The TLB is a cache that stores recent translations of virtual addresses to physical addresses.
   - **TLB Hit:** If the TLB contains the translation for the given VPN, the corresponding Physical Frame Number (PFN) is retrieved. The physical address is then formed by combining the PFN with the offset.
   - **TLB Miss:** If the translation is not in the TLB, a page table lookup is required.
3. **Page Table Lookup:**
   - The page table is a data structure maintained by the operating system that maps virtual addresses to physical addresses. Each process has its own page table.
   - **Page Table Hierarchy:** Modern systems often use a multi-level page table to manage memory efficiently. Common structures include two-level, three-level, or even four-level page tables.