# 05 Database Implementation

## Table of Contents

1. [Overview](#overview)
2. [Transactions and ACID Properties](#transactions-and-acid-properties)
3. [Storage Management](#storage-management)
4. [Buffer Management](#buffer-management)
5. [Indexing Structures](#indexing-structures)
6. [Query Execution](#query-execution)
7. [Storage Formats and Optimization](#storage-formats-and-optimization)
9. [References](#references)

## Overview

This chapter covers the internal implementation of database systems, exploring how databases efficiently manage data storage, retrieval, and processing. Topics include storage management, buffer management, indexing structures, query execution models, and performance optimizations.

### Key Implementation Concerns

**Performance:**
- Minimize disk I/O (primary bottleneck)
- Efficient memory utilization
- Fast query execution

**Reliability:**
- ACID transaction guarantees
- Crash recovery mechanisms
- Data durability

**Scalability:**
- Handle growing data volumes
- Support concurrent users
- Efficient resource utilization

### Why C++ for Databases?

Modern database systems are often implemented in C++ for several reasons:

| Advantage | Benefit |
|-----------|---------|
| **Performance** | Compiled to machine code, minimal runtime overhead |
| **Hardware Control** | Direct memory management, precise resource control |
| **Type Safety** | Compile-time error detection |
| **Low-Level Access** | Direct manipulation of bits, bytes, and memory |

**Performance Comparison:**
- C++ sum of 100M integers: 100 microseconds
- Python equivalent: 5.24 seconds
- **Performance ratio: ~50,000× faster**

## Transactions and ACID Properties

**Transactions** are logical units of work that maintain database consistency and reliability. They are governed by **ACID properties**.

### ACID Properties

#### Atomicity

**"All or Nothing"** - Transactions execute completely or not at all.

**Characteristics:**
- No partial updates visible
- Transaction failure causes rollback
- Ensures database never in intermediate state

**Implementation:**
- Write-Ahead Logging (WAL)
- Undo logs for rollback
- Redo logs for recovery

**Example:**
```
Bank transfer: $100 from Account A to Account B

BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 'A';  -- Deduct
  UPDATE accounts SET balance = balance + 100 WHERE id = 'B';  -- Add
COMMIT;

If system crashes after first UPDATE:
- Atomicity ensures rollback
- Neither account modified
- No money lost or created
```

#### Consistency

**Maintains database integrity constraints.**

**Characteristics:**
- Database moves from one valid state to another
- All constraints satisfied before and after transaction
- Business rules preserved

**Example:**
```
Constraint: Total money in system remains constant

Before: A=$1000, B=$500, Total=$1500
Transfer $100 from A to B
After: A=$900, B=$600, Total=$1500 ✓

Consistency maintained: total unchanged
```

#### Isolation

**Concurrent transactions don't interfere with each other.**

**Characteristics:**
- Transactions appear to execute sequentially
- Intermediate states not visible to others
- Prevents read/write conflicts

**Isolation Levels:**

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|-----------|-------------------|--------------|
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** | Prevented | Possible | Possible |
| **Repeatable Read** | Prevented | Prevented | Possible |
| **Serializable** | Prevented | Prevented | Prevented |

**Implementation:**
- Locking protocols (two-phase locking)
- Multi-Version Concurrency Control (MVCC)
- Timestamp ordering

#### Durability

**Committed changes survive system failures.**

**Characteristics:**
- Changes persisted to non-volatile storage
- Survive crashes, power failures
- Write-Ahead Logging ensures durability

**Implementation:**
- Force log records to disk before commit
- Redo logs reconstruct committed transactions
- Checkpoint mechanisms for recovery

### History of ACID

The ACID acronym was formalized by **Andreas Reuter (1983)** and **Theo Härder**, building on earlier concepts from database theory.

## Storage Management

Storage management handles the physical organization of data on disk and its transfer to memory.

### Storage Hierarchy

| Storage Type | Latency | Capacity | Volatile | Cost/GB |
|--------------|---------|----------|----------|---------|
| **DRAM** | ~30 ns | GB | Yes | High |
| **SSD** | ~100 μs | TB | No | Medium |
| **HDD** | ~10 ms | TB | No | Low |

**Key Insight:** Memory is ~100,000× faster than disk, driving all storage management decisions.

### Data Lifecycle

**Hot Data (DRAM):**
- Frequently accessed
- Cached for speed
- Volatile (lost on power failure)
- Limited capacity

**Durable Data (Disk):**
- Permanent storage
- Slower access
- Persistent across failures
- Large capacity

**Database manages movement** between tiers based on access patterns.

### File I/O in C++

Databases use file I/O for persistence:

```cpp
#include <fstream>

// Write data to file
std::ofstream outputFile("data.db");
outputFile << "Record data";
outputFile.close();

// Read data from file
std::ifstream inputFile("data.db");
std::string data;
inputFile >> data;
inputFile.close();

// Error handling critical
if (!inputFile) {
    std::cerr << "Error opening file" << std::endl;
    // Handle error appropriately
}
```

### Memory Management

#### Heap vs. Stack Allocation

**Stack:**
- Fast allocation/deallocation
- Limited size
- Automatic lifetime management
- Scope-bound

**Heap:**
- Dynamic allocation
- Large pool of memory
- Manual lifetime management (or smart pointers)
- Survives beyond function scope

**Database Usage:**
- Large data structures → heap
- Temporary local variables → stack
- Page buffers → heap
- Control structures → stack

#### Smart Pointers (RAII)

**Resource Acquisition Is Initialization (RAII)** ties resource lifetime to object scope.

**Problems with Raw Pointers:**
1. Memory leaks
2. Dangling pointers
3. Double-free errors
4. Ownership ambiguity

**Smart Pointer Solution:**

```cpp
// std::unique_ptr - exclusive ownership
std::unique_ptr<Page> page = std::make_unique<Page>();
// Automatically deleted when out of scope

// std::shared_ptr - shared ownership
std::shared_ptr<Buffer> buffer = std::make_shared<Buffer>();
// Deleted when last reference removed

// Move semantics for transfer
std::unique_ptr<Page> page2 = std::move(page);
// page is now null, page2 owns the resource
```

### Page Structure

**Page** is the basic unit of disk storage:

**Characteristics:**
- Fixed size (typically 4KB, 8KB, 16KB)
- Atomic unit of I/O
- Contains multiple tuples
- Includes metadata (used space, free space)

**Slotted Page Structure:**

```
┌─────────────────────────────────────┐
│         Page Header                 │
├─────────────────────────────────────┤
│  Slot Array (offset, length pairs) │
├─────────────────────────────────────┤
│         Free Space                  │
├─────────────────────────────────────┤
│         Tuple N                     │
│         Tuple N-1                   │
│         ...                         │
│         Tuple 1                     │
└─────────────────────────────────────┘
```

**Advantages:**
- Direct access to any tuple by slot index
- Efficient space utilization
- Simplified compaction
- Support for variable-length tuples

### Serialization and Deserialization

**Purpose:** Convert in-memory structures to on-disk format and vice versa.

**Serialization (Write):**
```cpp
void Page::serialize(const std::string& filename) {
    std::ofstream file(filename, std::ios::binary);

    // Write number of tuples
    size_t num_tuples = tuples.size();
    file.write(reinterpret_cast<const char*>(&num_tuples), sizeof(num_tuples));

    // Write each tuple
    for (const auto& tuple : tuples) {
        tuple->serialize(file);
    }
}
```

**Deserialization (Read):**
```cpp
void Page::deserialize(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);

    // Read number of tuples
    size_t num_tuples;
    file.read(reinterpret_cast<char*>(&num_tuples), sizeof(num_tuples));

    // Read each tuple
    for (size_t i = 0; i < num_tuples; ++i) {
        auto tuple = std::make_unique<Tuple>();
        tuple->deserialize(file);
        tuples.push_back(std::move(tuple));
    }
}
```

## Buffer Management

The **buffer manager** caches frequently accessed pages in memory to minimize disk I/O.

### Buffer Pool Architecture

```
┌────────────────────────────────────┐
│        Query Processor             │
├────────────────────────────────────┤
│       Buffer Manager               │
│  ┌──────────────────────────────┐  │
│  │    Buffer Pool (DRAM)        │  │
│  │  ┌─────┐  ┌─────┐  ┌─────┐   │  │
│  │  │Page │  │Page │  │Page │   │  │
│  │  │ 1   │  │ 2   │  │ 3   │   │  │
│  │  └─────┘  └─────┘  └─────┘   │  │
│  └──────────────────────────────┘  │
├────────────────────────────────────┤
│      Storage Manager               │
├────────────────────────────────────┤
│          Disk Storage              │
└────────────────────────────────────┘
```

### Buffer Manager Components

**Data Structures:**
- **Page Table (Hash Map)**: Maps page IDs to buffer pool frames
- **Replacement Policy**: Determines which page to evict
- **Dirty Bit**: Tracks modified pages requiring write-back

**Operations:**
```cpp
class BufferManager {
public:
    Page* getPage(PageID page_id);      // Fetch page (from buffer or disk)
    void unpinPage(PageID page_id);     // Release page reference
    void flushPage(PageID page_id);     // Write page to disk
    void evictPage();                   // Remove page from buffer
private:
    std::unordered_map<PageID, Frame*> page_table;
    ReplacementPolicy* policy;
};
```

### Cache Eviction Policies

#### FIFO (First-In-First-Out)

**Strategy:** Evict oldest page in buffer.

**Advantages:**
- Simple implementation
- Low overhead

**Disadvantages:**
- May evict frequently accessed pages
- Ignores access patterns
- Poor for workloads with hot pages

#### LRU (Least Recently Used)

**Strategy:** Evict page with oldest access time.

**Advantages:**
- Considers recency of access
- Good for temporal locality
- Better than FIFO for typical workloads

**Disadvantages:**
- Sequential scans pollute cache
- Overhead of tracking access times

**Implementation:**
```cpp
// LRU using doubly-linked list + hash map
class LRUPolicy {
private:
    std::list<std::pair<PageID, Page*>> lru_list;  // Most recent at front
    std::unordered_map<PageID, list::iterator> page_map;

public:
    void touch(PageID page_id) {
        // Move to front (most recent)
        auto it = page_map[page_id];
        lru_list.splice(lru_list.begin(), lru_list, it);
    }

    PageID evict() {
        // Remove from back (least recent)
        PageID victim = lru_list.back().first;
        lru_list.pop_back();
        page_map.erase(victim);
        return victim;
    }
};
```

#### TwoQ Policy

**Strategy:** Separate queues for single-access and frequently-accessed pages.

**Architecture:**
```
┌─────────────────────────┐
│   FIFO Queue (Cold)     │  ← New pages enter here
│   Read-once pages       │
└─────────────────────────┘
           ↓ On second access
┌─────────────────────────┐
│    LRU Queue (Hot)      │  ← Frequently accessed
│   Multi-access pages    │
└─────────────────────────┘
```

**Benefits:**
- Prevents buffer pool flooding from sequential scans
- Prioritizes frequently accessed pages
- Evicts cold pages first

**Eviction Priority:**
1. Evict from FIFO queue (cold pages)
2. Only if FIFO empty, evict from LRU queue

### Buffer Pool Flooding

**Problem:** Sequential scans bring many pages into buffer, evicting hot pages.

**Example:**
```
Normal state:
Buffer: [Hot1, Hot2, Hot3, Hot4, Hot5]  ← Frequently used

After sequential scan:
Buffer: [Scan98, Scan99, Scan100, Scan101, Scan102]  ← Never reused
Lost: All hot pages evicted
```

**Solution:** TwoQ, LRU-K, or bypass buffer for known sequential scans.

## Indexing Structures

Indexes provide fast access paths to data without full table scans.

### Hash Index

**Structure:** Maps keys to locations using hash function.

**Operations:**
```cpp
class HashIndex {
private:
    std::unordered_map<Key, std::vector<RecordID>> index;

public:
    void insert(Key key, RecordID rid) {
        index[key].push_back(rid);
    }

    std::vector<RecordID> find(Key key) {
        return index[key];  // O(1) average case
    }
};
```

**Performance:**
- **Point query**: O(1) average, O(n) worst case
- **Range query**: O(n) (must scan entire index)
- **Insert/Delete**: O(1) average

**Use Cases:**
- Equality searches
- Primary key lookups
- Hash joins

**Collision Handling:**
- **Chaining**: Store colliding entries in linked list
- **Open Addressing**: Probe for next available slot (linear, quadratic, double hashing)

### B+ Tree Index

**Structure:** Balanced tree optimized for disk-based storage.

```
                  [Root: 50]
                 /          \
        [20, 40]              [70, 90]
       /    |    \           /   |    \
   [10,15] [30] [45]    [60,65] [80] [95]
     ↓      ↓    ↓        ↓      ↓    ↓
   Data   Data  Data    Data   Data  Data
```

**Properties:**
- **Balanced**: All leaves at same depth
- **Sorted**: Keys in order
- **High Fanout**: Each node contains many keys (typically 100-200)
- **Leaf Linking**: Leaves linked for range scans

**Node Structure:**

**Internal Node:**
```
┌──────────────────────────────────┐
│  K1 | K2 | K3 | ... | Kn        │  Keys
├──────────────────────────────────┤
│ P0 | P1 | P2 | P3 | ... | Pn    │  Pointers to children
└──────────────────────────────────┘
```

**Leaf Node:**
```
┌──────────────────────────────────┐
│  K1 | K2 | K3 | ... | Kn        │  Keys
├──────────────────────────────────┤
│  V1 | V2 | V3 | ... | Vn        │  Values (RecordIDs)
├──────────────────────────────────┤
│  Next Leaf Pointer               │  For range scans
└──────────────────────────────────┘
```

**Performance:**
- **Point query**: O(log_F N) where F = fanout
- **Range query**: O(log_F N + K) where K = result size
- **Insert**: O(log_F N)
- **Delete**: O(log_F N)

**Example Capacity:**

With 4KB pages, 8-byte keys, 8-byte pointers:
- **Fanout**: ~250 entries per node
- **Height 3 tree**: 250³ = 15.6 million records
- **Height 4 tree**: 250⁴ = 3.9 billion records

**Advantages:**
- Efficient range queries
- Sequential access via leaf links
- Guaranteed logarithmic performance
- Self-balancing
- Optimized for disk access

### B+ Tree Operations

**Search:**
```cpp
Value* search(Key key) {
    Node* node = root;

    // Descend to leaf
    while (!node->isLeaf) {
        int i = findChildIndex(node, key);
        node = node->children[i];
    }

    // Search in leaf
    return node->find(key);
}
```

**Insert:**
```cpp
void insert(Key key, Value value) {
    Node* leaf = findLeaf(key);
    leaf->insert(key, value);

    if (leaf->isFull()) {
        splitNode(leaf);  // May cascade up tree
    }
}
```

**Split Operation:**
```
Before split (capacity 4):
┌────────────────────────────┐
│  10 | 20 | 30 | 40 | 50   │  ← Overflow
└────────────────────────────┘

After split:
┌──────────────┐         ┌──────────────┐
│  10 | 20     │ ← Left  │  40 | 50     │ ← Right
└──────────────┘         └──────────────┘
        ↓                        ↓
    Parent: [30]  ← Middle key promoted
```

## Query Execution

Query execution transforms SQL into physical operations that retrieve and process data.

### Query Processing Pipeline

```
SQL Query
   ↓
Parser (Syntax check, create parse tree)
   ↓
Optimizer (Choose execution plan)
   ↓
Execution Engine (Execute operators)
   ↓
Buffer Manager (Fetch pages)
   ↓
Result
```

### Operator Framework

**Philosophy:** Modular, composable operators like Lego blocks.

**Base Operator Interface:**
```cpp
class Operator {
public:
    virtual void open() = 0;          // Initialize
    virtual Tuple* next() = 0;        // Get next tuple
    virtual void close() = 0;         // Cleanup
};
```

**Common Operators:**

| Operator | Purpose | Example |
|----------|---------|---------|
| **Scan** | Read table | `SELECT * FROM table` |
| **Select** | Filter rows | `WHERE salary > 50000` |
| **Project** | Choose columns | `SELECT name, salary` |
| **Join** | Combine tables | `FROM t1 JOIN t2 ON t1.id = t2.id` |
| **GroupBy** | Aggregate | `GROUP BY department` |
| **Sort** | Order results | `ORDER BY name` |

**Example Query Plan:**

```sql
SELECT department, AVG(salary)
FROM employees
WHERE salary > 50000
GROUP BY department;
```

**Execution Plan:**
```
GroupBy(department, AVG(salary))
   ↓
Select(salary > 50000)
   ↓
Scan(employees)
```

### Iterator Model (Volcano Model)

**Characteristics:**
- **Pull-based**: Parent calls next() on child
- **Pipelined**: Tuples flow through operators
- **Memory efficient**: Process one tuple at a time

**Example:**
```cpp
class SelectOperator : public Operator {
private:
    Operator* child;
    Predicate predicate;

public:
    void open() { child->open(); }

    Tuple* next() {
        while (Tuple* t = child->next()) {
            if (predicate.evaluate(t)) {
                return t;  // Pass matching tuple
            }
        }
        return nullptr;  // No more tuples
    }

    void close() { child->close(); }
};
```

### Query Optimization

**Goals:**
- Minimize disk I/O
- Reduce intermediate result sizes
- Choose efficient join algorithms
- Leverage indexes

**Optimization Techniques:**

**1. Predicate Pushdown:**
```
Bad:  Join → Filter
Good: Filter → Join  (fewer tuples to join)
```

**2. Index Selection:**
```
Instead of: Full table scan
Use:        Index scan when selective predicate exists
```

**3. Join Order:**
```
For: A ⋈ B ⋈ C

If |A| = 100, |B| = 1000, |C| = 10
Optimal: (A ⋈ C) ⋈ B
Bad: (B ⋈ C) ⋈ A
```

**4. Join Algorithms:**

| Algorithm | Cost | Use When |
|-----------|------|----------|
| **Nested Loop** | O(N × M) | Small tables, no indexes |
| **Index Join** | O(N × log M) | Index on join key |
| **Hash Join** | O(N + M) | Equijoin, memory available |
| **Merge Join** | O(N + M) | Sorted inputs |

## Storage Formats and Optimization

### Row vs. Columnar Storage

#### Row Storage (NSM - N-ary Storage Model)

**Structure:** All attributes of a record stored together.

```
Page:
┌─────────────────────────────────────┐
│ Row1: [ID=1, Name=Alice, Age=30]   │
│ Row2: [ID=2, Name=Bob, Age=25]     │
│ Row3: [ID=3, Name=Carol, Age=35]   │
└─────────────────────────────────────┘
```

**Advantages:**
- Efficient for fetching entire rows
- Good for OLTP workloads
- Simple implementation

**Disadvantages:**
- Reads unnecessary columns
- Poor cache locality for column scans
- Inefficient for analytical queries

#### Columnar Storage (DSM - Decomposition Storage Model)

**Structure:** Each attribute stored separately.

```
ID Column:    [1, 2, 3, ...]
Name Column:  [Alice, Bob, Carol, ...]
Age Column:   [30, 25, 35, ...]
```

**Advantages:**
- Read only needed columns
- Better compression (similar data together)
- Excellent cache locality
- Efficient for OLAP workloads

**Disadvantages:**
- Expensive row reconstruction
- Poor for transactional workloads
- Complex implementation

**Performance Comparison:**

Query: `SELECT AVG(temperature) FROM weather WHERE timestamp BETWEEN ...`

| Storage Type | Pages Read | Query Time |
|--------------|-----------|------------|
| **Row** | 1000 | 112 ms |
| **Columnar** | 10 | 3.6 ms |

**Reason:** Only temperature column needed, not all columns.

### Compression

Columnar storage enables effective compression due to:
- **Uniform data types** per column
- **Data redundancy** (repeating values)
- **Sorted data** in many cases

**Compression Techniques:**

| Technique | Best For | Example |
|-----------|----------|---------|
| **Delta Encoding** | Sorted numeric data | [100, 102, 105] → [100, +2, +3] |
| **Run-Length Encoding** | Repeated values | [A, A, A, B, B] → [3×A, 2×B] |
| **Dictionary Encoding** | Categorical data | [NY, CA, NY, TX] → [0, 1, 0, 2] + dict |
| **Bit-Packing** | Small-range integers | 7-bit values in 7 bits (not 8) |

**Compression Benefits:**
- Reduced storage space (2-10× typical)
- Reduced I/O (fewer pages to read)
- Faster queries (less data to process)
- Operates directly on compressed data (where possible)

### Vectorized Execution

**Problem:** Tuple-at-a-time processing has high overhead.

**Solution:** Process batches of tuples (vectors) together.

**Benefits:**
- **Reduced function call overhead**
- **Better CPU cache utilization**
- **SIMD (Single Instruction Multiple Data) opportunities**

**SIMD Example:**
```cpp
// Without SIMD: 4 operations
result[0] = a[0] + b[0];
result[1] = a[1] + b[1];
result[2] = a[2] + b[2];
result[3] = a[3] + b[3];

// With SIMD: 1 operation
__m128i va = _mm_load_si128(a);  // Load 4 integers
__m128i vb = _mm_load_si128(b);
__m128i vr = _mm_add_epi32(va, vb);  // Add 4 integers simultaneously
_mm_store_si128(result, vr);
```

**Performance Impact:**
- **4× throughput** with 128-bit SIMD
- **8× throughput** with 256-bit AVX
- **16× throughput** with 512-bit AVX-512

## References

**Course Materials:**
- CS 6400: Database Systems Concepts and Design - Georgia Tech OMSCS
- CS 6422: Database System Implementation - Georgia Tech OMSCS
