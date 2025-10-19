# Synchronization

## Table of Contents

1. [Overview](#overview)
2. [Fundamentals](#fundamentals)
3. [Basic Synchronization Primitives](#basic-synchronization-primitives)
4. [Atomic Operations](#atomic-operations)
5. [Advanced Lock Algorithms](#advanced-lock-algorithms)
6. [Barrier Synchronization](#barrier-synchronization)
7. [Performance Considerations](#performance-considerations)
8. [Implementation Examples](#implementation-examples)
9. [Related Topics](#related-topics)
10. [References](#references)

## Overview

Synchronization is a fundamental mechanism in concurrent and parallel programming that coordinates the execution of multiple threads or processes to ensure proper order of execution, prevent race conditions, and avoid data corruption. As modern systems increasingly rely on parallelism across multiple cores and processors, effective synchronization becomes critical for correctness and performance.

Synchronization mechanisms range from basic primitives like mutexes and semaphores used in single-machine multithreading to advanced algorithms like queueing locks and distributed barriers designed for scalable parallel systems. The choice of synchronization mechanism depends on factors including contention levels, architectural characteristics (cache-coherent vs. non-cache-coherent), and scalability requirements.

### Key Challenges

**Correctness:**

- Preventing race conditions when multiple threads access shared data
- Ensuring atomicity of compound operations
- Maintaining data consistency across execution units

**Performance:**
- Minimizing latency when acquiring free locks
- Reducing contention when multiple threads compete for resources
- Avoiding excessive cache coherence traffic

**Scalability:**
- Ensuring performance improves with additional processors
- Managing overhead that grows with system size
- Balancing fairness with efficiency

## Fundamentals

### Race Conditions

A race condition occurs when multiple threads access shared resources simultaneously, and the final result depends on the unpredictable timing or ordering of thread execution. Race conditions lead to non-deterministic behavior and program errors.

**Example Scenario:**
```c
// Shared variable
int counter = 0;

// Two threads executing simultaneously
Thread 1: counter = counter + 1;  // Read: 0, Write: 1
Thread 2: counter = counter + 1;  // Read: 0, Write: 1
// Expected result: 2, Actual result: 1
```

Without synchronization, both threads may read the same initial value, perform their increment, and write back the same incremented value, losing one update.

### Critical Sections

A critical section is a segment of code that accesses shared resources and must not be executed by more than one thread at a time. Synchronization mechanisms protect critical sections to ensure mutual exclusion.

**Properties of Correct Critical Section Implementation:**

1. **Mutual Exclusion:** Only one thread can execute in the critical section at a time
2. **Progress:** If no thread is in the critical section and threads wish to enter, selection of the next thread cannot be postponed indefinitely
3. **Bounded Waiting:** A limit exists on the number of times other threads can enter the critical section after a thread requests entry
4. **Performance:** Overhead of entering and exiting the critical section should be minimal

### Thread Safety

Thread safety refers to code that behaves correctly when accessed by multiple threads simultaneously. Thread-safe code avoids data races and maintains invariants even under concurrent access.

**Approaches to Thread Safety:**

1. **Synchronization:** Use locks, semaphores, or other primitives to serialize access
2. **Immutability:** Use immutable data structures that cannot be modified after creation
3. **Thread-Local Storage:** Give each thread its own copy of data
4. **Lock-Free Programming:** Use atomic operations and careful algorithm design

### Deadlock

Deadlock is a situation where two or more threads are permanently blocked, each waiting for a resource held by another thread in the cycle. Deadlocks result from improper synchronization and can freeze program execution.

**Four Necessary Conditions for Deadlock:**

1. **Mutual Exclusion:** Resources cannot be shared
2. **Hold and Wait:** Threads hold resources while waiting for others
3. **No Preemption:** Resources cannot be forcibly taken from threads
4. **Circular Wait:** A circular chain of threads exists, each waiting for a resource held by the next

**Prevention Strategies:**
- Lock ordering: Always acquire locks in the same order
- Timeout mechanisms: Release locks if acquisition takes too long
- Deadlock detection: Periodically check for cycles and break them

## Basic Synchronization Primitives

### Locks (Mutexes)

A mutex (mutual exclusion lock) is the most fundamental synchronization primitive. It allows threads to acquire exclusive access to shared resources, ensuring only one thread executes in the critical section at a time.

#### Exclusive Lock

An exclusive or mutual exclusion lock can be held by only one thread at a time. While one thread holds the lock, all other threads attempting to acquire it must wait.

**Operations:**
- `lock()`: Acquire the lock, blocking if already held
- `unlock()`: Release the lock
- `trylock()`: Attempt to acquire without blocking, returns success/failure

**Use Cases:**
- Protecting shared data structures during modification
- Ensuring atomicity of compound operations
- Preventing race conditions

#### Shared Lock (Read-Write Lock)

A shared lock allows multiple threads to hold the lock simultaneously for read-only access while providing exclusive access for writes. This enables concurrent readers while still providing mutual exclusion with writers.

**Operations:**
- `read_lock()`: Acquire shared read access (multiple readers allowed)
- `write_lock()`: Acquire exclusive write access (only one writer)
- `unlock()`: Release the lock

**Use Cases:**
- Data structures with frequent reads and infrequent writes
- Database systems with read-heavy workloads
- Configuration data accessed by many threads

#### POSIX Mutex Example

```c
#include <pthread.h>

// Shared data
int sharedValue = 0;
pthread_mutex_t mutex;

void* incrementSharedValue(void* arg) {
    for (int i = 0; i < 100000; i++) {
        // Lock the mutex to protect the critical section
        pthread_mutex_lock(&mutex);
        
        // Critical section: increment the shared value
        sharedValue++;
        
        // Unlock the mutex to release the critical section
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    // Initialize the mutex
    pthread_mutex_init(&mutex, NULL);
    
    // Create two threads
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, incrementSharedValue, NULL);
    pthread_create(&thread2, NULL, incrementSharedValue, NULL);
    
    // Wait for threads to finish
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    
    // Destroy the mutex
    pthread_mutex_destroy(&mutex);
    
    printf("Final Value: %d\n", sharedValue);
    return 0;
}
```

#### Read-Write Lock Example

```c
#include <pthread.h>

int sharedData = 0;
pthread_rwlock_t rwlock;

void* reader(void* arg) {
    pthread_rwlock_rdlock(&rwlock);
    printf("Reader %ld: Read data: %d\n", (long)arg, sharedData);
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}

void* writer(void* arg) {
    pthread_rwlock_wrlock(&rwlock);
    sharedData++;
    printf("Writer %ld: Wrote data: %d\n", (long)arg, sharedData);
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}

int main() {
    pthread_rwlock_init(&rwlock, NULL);
    
    // Create reader and writer threads
    pthread_t readerThreads[3], writerThreads[2];
    for (long i = 0; i < 3; i++) {
        pthread_create(&readerThreads[i], NULL, reader, (void*)i);
    }
    for (long i = 0; i < 2; i++) {
        pthread_create(&writerThreads[i], NULL, writer, (void*)i);
    }
    
    // Wait for threads to finish
    for (long i = 0; i < 3; i++) {
        pthread_join(readerThreads[i], NULL);
    }
    for (long i = 0; i < 2; i++) {
        pthread_join(writerThreads[i], NULL);
    }
    
    pthread_rwlock_destroy(&rwlock);
    return 0;
}
```

### Semaphores

Semaphores are synchronization primitives that maintain a count and allow a specified number of threads to access a shared resource concurrently. They are more general than mutexes and can coordinate multiple threads.

**Types:**

1. **Binary Semaphore:** Count is either 0 or 1, similar to a mutex
2. **Counting Semaphore:** Count can be any non-negative integer

**Operations:**
- `wait()` or `P()`: Decrement the count, blocking if count is 0
- `signal()` or `V()`: Increment the count, potentially waking a waiting thread

**Use Cases:**
- Limiting concurrent access to a resource pool
- Producer-consumer synchronization
- Signaling between threads

#### POSIX Semaphore Example

```c
#include <semaphore.h>

int sharedData = 0;
sem_t semaphore;

void* producer(void* arg) {
    for (int i = 1; i <= 10; i++) {
        // Produce data
        sharedData = i;
        printf("Produced: %d\n", sharedData);
        
        // Signal the semaphore to indicate new data is available
        sem_post(&semaphore);
        
        sleep(1);
    }
    return NULL;
}

void* consumer(void* arg) {
    for (int i = 1; i <= 10; i++) {
        // Wait for new data to be available
        sem_wait(&semaphore);
        
        // Consume the data
        printf("Consumed: %d\n", sharedData);
        sharedData = 0;
        
        sleep(1);
    }
    return NULL;
}

int main() {
    // Initialize the semaphore with initial value 0
    sem_init(&semaphore, 0, 0);
    
    pthread_t producerThread, consumerThread;
    pthread_create(&producerThread, NULL, producer, NULL);
    pthread_create(&consumerThread, NULL, consumer, NULL);
    
    pthread_join(producerThread, NULL);
    pthread_join(consumerThread, NULL);
    
    sem_destroy(&semaphore);
    return 0;
}
```

### Condition Variables

Condition variables provide a mechanism for threads to wait until a specific condition is met before proceeding. They are always used in conjunction with a mutex to protect the condition check.

**Operations:**
- `wait(mutex)`: Atomically release mutex and wait for signal
- `signal()`: Wake up one waiting thread
- `broadcast()`: Wake up all waiting threads

**Use Cases:**
- Producer-consumer patterns with complex conditions
- Implementing monitors
- Thread coordination based on state changes

#### Condition Variable Example

```c
#include <pthread.h>

int sharedData = 0;
pthread_mutex_t mutex;
pthread_cond_t condition;

void* producer(void* arg) {
    for (int i = 1; i <= 10; i++) {
        pthread_mutex_lock(&mutex);
        
        sharedData = i;
        printf("Produced: %d\n", sharedData);
        
        // Signal the consumer that new data is available
        pthread_cond_signal(&condition);
        
        pthread_mutex_unlock(&mutex);
        sleep(1);
    }
    return NULL;
}

void* consumer(void* arg) {
    for (int i = 1; i <= 10; i++) {
        pthread_mutex_lock(&mutex);
        
        // Wait for new data to be available
        while (sharedData == 0) {
            pthread_cond_wait(&condition, &mutex);
        }
        
        printf("Consumed: %d\n", sharedData);
        sharedData = 0;
        
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&condition, NULL);
    
    pthread_t producerThread, consumerThread;
    pthread_create(&producerThread, NULL, producer, NULL);
    pthread_create(&consumerThread, NULL, consumer, NULL);
    
    pthread_join(producerThread, NULL);
    pthread_join(consumerThread, NULL);
    
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&condition);
    return 0;
}
```

## Atomic Operations

Individual load and store instructions are inherently atomic, but implementing synchronization primitives requires atomicity across multiple operations. This necessitates specialized Read-Modify-Write (RMW) instructions that execute as indivisible units.

### Read-Modify-Write (RMW) Instructions

RMW operations are sometimes generically called Fetch and φ instructions, where φ represents some operation. These instructions read from memory, modify the value in a register, and write it back atomically.

### Test and Set

Returns the current value of a memory location and atomically sets it to one.

```c
int TestAndSet(int *L) {
    int old = *L;
    *L = 1;
    return old;
}
```

**Use Case:** Basic spinlock implementation

**Properties:**
- Single atomic operation
- Returns previous state
- Sets to locked state (1)

### Fetch and Increment

Fetches the current value and atomically increments the memory location.

```c
int FetchAndIncrement(int *L) {
    int old = *L;
    *L = old + 1;
    return old;
}
```

**Use Case:** 
- Ticket locks for fair ordering
- Generating unique sequence numbers
- Atomic counters

**Properties:**
- Returns old value
- Increments by 1 (or specified amount)
- Useful for FIFO ordering

### Fetch and Store

Atomically returns the old value and stores a new value.

```c
int FetchAndStore(int *L, int new_value) {
    int old = *L;
    *L = new_value;
    return old;
}
```

**Use Case:**
- MCS lock implementation
- Atomic swaps
- Building lock-free data structures

**Properties:**
- Atomic swap operation
- Returns previous value
- Stores arbitrary new value

### Compare and Swap (CAS)

Conditionally updates a memory location if its current value matches an expected value.

```c
bool CompareAndSwap(int *L, int expected, int new_value) {
    if (*L == expected) {
        *L = new_value;
        return true;
    }
    return false;
}
```

**Use Case:**
- Lock-free algorithms
- Handling race conditions in complex scenarios
- Building sophisticated synchronization primitives

**Properties:**
- Conditional atomic update
- Returns success/failure
- Enables optimistic concurrency
- Foundation for lock-free programming

### Fetch and Decrement

Atomically fetches the current value and decrements it.

```c
int FetchAndDecrement(int *L) {
    int old = *L;
    *L = old - 1;
    return old;
}
```

**Use Case:**
- Counting barriers
- Reference counting
- Resource allocation

## Advanced Lock Algorithms

Implementing scalable synchronization primitives requires careful algorithm design to minimize latency, contention, and network traffic in parallel systems.

### Performance Metrics

**Latency:**
Time required for a thread to acquire a free lock. This should be minimized for optimal performance in the uncontended case.

**Waiting Time:**
Time a thread waits when the lock is held by another thread. Largely application-dependent but affected by implementation fairness.

**Contention:**
Time required for one thread to acquire a lock when multiple threads simultaneously attempt acquisition after a release. Critical for scalability in high-contention scenarios.

### Spinlock Implementations

#### Native Spinlock (Spin on Test and Set)

The simplest spinlock implementation where threads repeatedly execute TestAndSet until successful.

```c
void Lock(int *L) {
    while (TestAndSet(L) == 1) {
        // spin (busy wait)
    }
}

void Unlock(int *L) {
    *L = 0;
}
```

**Problems:**
- Heavy network contention from continuous TestAndSet operations
- Cannot exploit caches (TestAndSet bypasses cache, accesses memory directly)
- Disrupts useful work on other processors
- O(N) bus transactions per lock acquisition under contention

**When to Use:**
- Very low contention scenarios
- When advanced RMW instructions are unavailable
- Short critical sections

#### Caching Spinlock (Spin on Read)

Threads spin on a cached copy of the lock variable, only attempting TestAndSet when they observe the lock becoming free through cache coherence.

```c
void Lock(int *L) {
    while (true) {
        // Spin on cached value
        while (*L == 1) {
            // read from cache
        }
        // Lock appears free, try to acquire
        if (TestAndSet(L) == 0) {
            return;  // acquired
        }
    }
}

void Unlock(int *L) {
    *L = 0;
}
```

**Improvement:**
- Reduces contention while lock is held
- Exploits cache coherence mechanisms
- Less network traffic than native spinlock

**Remaining Problem:**
- Thundering herd when lock is released
- All waiters simultaneously attempt TestAndSet
- O(N²) bus transactions for write-invalidate coherence
- Still generates significant contention on release

#### Spinlock with Exponential Backoff

After failing to acquire a lock, threads delay for a period before retrying. The delay increases exponentially if contention persists, dynamically adapting to load.

```c
void Lock(int *L) {
    int delay = BASE_DELAY;
    while (TestAndSet(L) == 1) {
        sleep(delay);
        delay = min(delay * 2, MAX_DELAY);
    }
}

void Unlock(int *L) {
    *L = 0;
}
```

**Advantages:**
- Works on non-cache-coherent (NCC) multiprocessors
- Adapts to contention dynamically
- Reduces network traffic significantly
- Simple to implement

**Disadvantages:**
- Non-deterministic acquisition order (unfair)
- Delay tuning affects performance
- May introduce unnecessary latency
- No guarantee of bounded waiting

**When to Use:**
- Systems with only TestAndSet available
- Variable contention scenarios
- When fairness is not critical

#### Ticket Lock

Uses two counters to ensure FIFO ordering: `next_ticket` (incremented for each requester) and `now_serving` (incremented on release).

```c
typedef struct {
    int next_ticket;
    int now_serving;
} TicketLock;

void Lock(TicketLock *L) {
    int my_ticket = FetchAndIncrement(&L->next_ticket);
    while (L->now_serving != my_ticket) {
        // spin
    }
}

void Unlock(TicketLock *L) {
    L->now_serving++;
}
```

**Advantages:**
- Fair: first-come, first-served ordering
- Single RMW operation per acquisition
- Bounded waiting time
- Simple implementation

**Disadvantages:**
- Still noisy: all waiters observe `now_serving` updates
- O(N) cache coherence traffic per release
- Not scalable for large N
- All threads spin on same variable

**When to Use:**
- Fairness is important
- Moderate number of threads
- Cache-coherent systems

### Queueing Locks

Queueing locks address fairness and noisiness by giving each waiting thread a unique spin location and signaling only the next thread when the lock is released.

#### Array-Based Queueing Lock (Anderson)

Uses an array of flags sized to the number of processors, functioning as a circular queue.

```c
typedef struct {
    int flags[N];      // has_lock or must_wait
    int queue_last;
} AndersonLock;

void Lock(AndersonLock *L, int *my_slot) {
    *my_slot = FetchAndIncrement(&L->queue_last) % N;
    while (L->flags[*my_slot] == MUST_WAIT) {
        // spin on unique location
    }
    L->flags[*my_slot] = MUST_WAIT;
}

void Unlock(AndersonLock *L, int my_slot) {
    int next_slot = (my_slot + 1) % N;
    L->flags[next_slot] = HAS_LOCK;
}
```

**Advantages:**
- Fair: FIFO ordering
- Each thread spins on unique location
- Exactly one thread signaled on release
- Single RMW per critical section
- Predictable performance

**Disadvantages:**
- O(N) space per lock
- Wasteful for large N or many locks
- Array size must accommodate worst-case contention
- Poor cache utilization if N is large

**When to Use:**
- Cache-coherent systems
- Known maximum thread count
- High contention scenarios
- When fairness is critical

#### Link-Based Queueing Lock (MCS)

Uses a linked list of queue nodes with dynamic space allocation, developed by Mellor-Crummey and Scott.

```c
typedef struct QNode {
    bool got_it;
    struct QNode *next;
} QNode;

typedef QNode* MCSLock;

void Lock(MCSLock *L, QNode *my_node) {
    my_node->next = NULL;
    my_node->got_it = false;
    
    QNode *predecessor = FetchAndStore(L, my_node);
    if (predecessor != NULL) {
        predecessor->next = my_node;
        while (!my_node->got_it) {
            // spin on local variable
        }
    }
}

void Unlock(MCSLock *L, QNode *my_node) {
    if (my_node->next == NULL) {
        if (CompareAndSwap(L, my_node, NULL)) {
            return;  // no successor
        }
        // Wait for successor to link in
        while (my_node->next == NULL) {
            // spin briefly
        }
    }
    my_node->next->got_it = true;
}
```

**Advantages:**
- Fair: FIFO ordering
- Space proportional to actual contention (dynamic)
- Each thread spins on local variable
- Typically one RMW per critical section
- Excellent scalability

**Disadvantages:**
- More complex implementation
- Unlock requires CompareAndSwap for corner cases
- Two RMW operations in rare scenarios
- Link list maintenance overhead

**When to Use:**
- High scalability requirements
- Unknown or variable thread counts
- Cache-coherent systems
- Long critical sections where fairness matters

### Algorithm Selection Guidelines

| Scenario | Recommended Algorithm | Rationale |
|----------|----------------------|-----------|
| Low contention, short critical sections | Exponential backoff | Simple, adapts well, low overhead |
| High contention, fairness required | Anderson or MCS | Fair ordering, scalable |
| Only TestAndSet available | Exponential backoff | Best option without advanced RMW |
| Variable contention | Exponential backoff | Adapts dynamically to load |
| Large-scale parallel systems | MCS Lock | Best scalability, dynamic space |
| Cache-coherent with known N | Anderson Lock | Excellent performance, simple |
| Non-cache-coherent systems | Exponential backoff | Doesn't rely on cache coherence |

## Barrier Synchronization

Barrier synchronization ensures all participating threads reach a designated point before any proceed. This is essential for coordinating phases in parallel algorithms.

### Semantics

All threads must arrive at the barrier and wait until all threads have arrived before any can proceed to the next computation phase. This establishes a global synchronization point.

### Centralized Barrier (Counting Barrier)

Uses a shared counter initialized to N (number of threads). Each arriving thread atomically decrements the counter and spins until it reaches zero.

```c
typedef struct {
    int count;
    int N;
} CountingBarrier;

void Barrier(CountingBarrier *B) {
    FetchAndDecrement(&B->count);
    
    // Wait for all to arrive
    while (B->count > 0) {
        // spin
    }
    
    // Wait for reset (avoid race on re-entry)
    while (B->count != B->N) {
        // spin
    }
    
    // Last thread resets (not shown in simplified version)
}
```

**Problem:**
Race condition if threads proceed before count is reset. Requires two spinning episodes for safety.

**Advantages:**
- Simple implementation
- Easy to understand

**Disadvantages:**
- Two spin loops required
- Centralized counter creates hot spot
- Not scalable

### Sense Reversing Barrier

Eliminates one spin loop by using a sense flag that reverses when all threads arrive.

```c
typedef struct {
    int count;
    int N;
    bool sense;
} SenseBarrier;

// Per-thread variable
thread_local bool local_sense = true;

void Barrier(SenseBarrier *B) {
    local_sense = !local_sense;
    
    if (FetchAndDecrement(&B->count) == 1) {
        // Last thread: reset and release all
        B->count = B->N;
        B->sense = local_sense;
    } else {
        // Wait for sense to change
        while (B->sense != local_sense) {
            // spin
        }
    }
}
```

**Advantages:**
- Single spinning episode
- Simpler than counting barrier
- Correct re-entry handling

**Disadvantages:**
- Centralized count and sense create hot spots
- Limited scalability for large N
- High cache coherence traffic

**When to Use:**
- Small to medium number of threads
- Cache-coherent systems
- Simple barrier needs

### Tree Barrier

Hierarchical barrier using divide-and-conquer to limit sharing to small groups.

**Structure:**
- N processors grouped into clusters of K processors
- Forms a tree with log_K(N) levels
- Each cluster has local count and sense variables

**Arrival Phase:**
1. Thread decrements local group counter
2. Last thread in group propagates arrival to parent level
3. Continues up to root

**Wake-up Phase:**
1. Root (last arriving thread) reverses sense
2. Signal propagates down tree level by level
3. Each parent releases its children

**Advantages:**
- Reduces contention through hierarchical grouping
- O(log N) communication complexity
- More scalable than centralized barriers

**Disadvantages:**
- Spin locations dynamically determined (problematic for NCC NUMA)
- Arity K affects contention levels
- Complex implementation

### MCS Barrier

Modified tree barrier with statically determined spin locations, using a 4-ary arrival tree and binary wake-up tree.

**Arrival Tree (4-ary):**
- Each child signals parent at unique, pre-assigned location
- Parent checks ChildNotReady vector
- Static assignment enables efficient NUMA implementation

**Wake-up Tree (Binary):**
- Parent uses ChildPointer structures to signal children
- Children spin on statically determined locations
- Binary structure based on theoretical performance results

**Advantages:**
- Static spin locations optimize for NUMA
- Reduces cache coherence traffic
- Suitable for various architectures
- Excellent scalability

**Disadvantages:**
- More complex implementation
- Less spatial locality than single cache line per group
- Requires careful initialization

### Tournament Barrier

Organizes barrier as a tournament with predetermined winners advancing each round.

**Arrival Phase:**
```
for round = 0 to log(N)-1:
    if I am winner in this round:
        wait for signal from opponent
        advance to next round
    else:
        signal opponent
        break
```

**Wake-up Phase:**
```
for round = log(N)-1 down to 0:
    if I was winner:
        signal opponent in this round
```

**Advantages:**
- Statically determined spin locations (excellent for NCC NUMA)
- Uses only atomic read and write (no RMW required)
- O(log N) communication complexity
- Exploits network parallelism
- Works with message passing (clusters)

**Disadvantages:**
- Cannot pack multiple spins in one cache line
- Less spatial locality than MCS
- Fixed tournament structure

### Dissemination Barrier

Information diffusion where in round k, processor P_i sends to P_{(i + 2^k) mod N}.

```
for round = 0 to ceiling(log N)-1:
    target = (my_id + 2^round) mod N
    send message to target
    wait for message from source
```

**Advantages:**
- No hierarchical structure
- Works on NCC NUMA and clusters
- Independent, distributed decisions
- N need not be a power of 2
- Simple implementation

**Disadvantages:**
- O(N log N) total messages
- Higher communication complexity than tree barriers
- More network traffic

### Barrier Algorithm Comparison

| Algorithm | Communication | Spin Location | RMW Required | Best Architecture |
|-----------|--------------|---------------|--------------|-------------------|
| Counting | O(N) | Dynamic | Yes | Small CC systems |
| Sense Reversal | O(N) | Dynamic | Yes | Small CC systems |
| Tree | O(log N) | Dynamic | Yes | CC systems |
| MCS | O(log N) | Static | Yes | NUMA, CC |
| Tournament | O(log N) | Static | No | NCC NUMA, Clusters |
| Dissemination | O(N log N) | Static | No | NCC NUMA, Clusters |

## Performance Considerations

### Contention and Scalability

As the number of threads or processors increases, synchronization overhead can limit scalability. Key factors include:

**Cache Coherence Traffic:**
- Write operations to shared lock variables trigger invalidations
- More threads mean more cache coherence messages
- Can saturate interconnection network

**Memory Latency:**
- Access to shared synchronization variables may miss cache
- NUMA effects make remote access expensive
- Deep memory hierarchies increase latency variance

**Fairness vs. Performance:**
- Fair algorithms (FIFO ordering) may have higher overhead
- Unfair algorithms can lead to starvation
- Trade-off depends on application requirements

### False Sharing

False sharing occurs when independent variables reside in the same cache line, causing unnecessary cache coherence traffic.

**Example:**
```c
struct {
    int counter_A;  // Updated by Thread 1
    int counter_B;  // Updated by Thread 2
} shared_data;  // Both in same cache line
```

**Solutions:**
- Pad structures to cache line boundaries (typically 64 bytes)
- Align frequently updated variables separately
- Use thread-local storage when possible

### Lock-Free Programming

Lock-free programming designs algorithms that guarantee system-wide progress without using locks, typically using atomic operations like CAS.

**Advantages:**
- No deadlock possible
- Better scalability in some scenarios
- Eliminates lock contention overhead

**Disadvantages:**
- Complex algorithm design
- Difficult to verify correctness
- May have higher overhead in low-contention scenarios
- ABA problem requires careful handling

**Use Cases:**
- High-contention data structures
- Real-time systems requiring bounded latency
- Systems where lock overhead is prohibitive

### Wait-Free Programming

Wait-free programming is stronger than lock-free: every operation completes in a bounded number of steps regardless of other threads' actions.

**Properties:**
- Strongest progress guarantee
- No thread can be indefinitely delayed
- Ideal for real-time systems

**Challenges:**
- Very difficult to implement
- Often requires helping mechanisms
- Higher overhead than lock-free

## Implementation Examples

### Producer-Consumer with Semaphores

```c
#include <semaphore.h>

#define BUFFER_SIZE 10

int buffer[BUFFER_SIZE];
int in = 0, out = 0;

sem_t empty, full;
pthread_mutex_t mutex;

void* producer(void* arg) {
    for (int i = 0; i < 100; i++) {
        int item = produce_item();
        
        sem_wait(&empty);
        pthread_mutex_lock(&mutex);
        
        buffer[in] = item;
        in = (in + 1) % BUFFER_SIZE;
        
        pthread_mutex_unlock(&mutex);
        sem_post(&full);
    }
    return NULL;
}

void* consumer(void* arg) {
    for (int i = 0; i < 100; i++) {
        sem_wait(&full);
        pthread_mutex_lock(&mutex);
        
        int item = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        
        pthread_mutex_unlock(&mutex);
        sem_post(&empty);
        
        consume_item(item);
    }
    return NULL;
}

int main() {
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);
    pthread_mutex_init(&mutex, NULL);
    
    pthread_t prod, cons;
    pthread_create(&prod, NULL, producer, NULL);
    pthread_create(&cons, NULL, consumer, NULL);
    
    pthread_join(prod, NULL);
    pthread_join(cons, NULL);
    
    sem_destroy(&empty);
    sem_destroy(&full);
    pthread_mutex_destroy(&mutex);
    
    return 0;
}
```

### Reader-Writer Problem

```c
#include <pthread.h>

int readers = 0;
pthread_mutex_t mutex;
pthread_mutex_t write_lock;

void* reader(void* arg) {
    pthread_mutex_lock(&mutex);
    readers++;
    if (readers == 1) {
        pthread_mutex_lock(&write_lock);  // First reader locks writers
    }
    pthread_mutex_unlock(&mutex);
    
    // Read shared data
    read_data();
    
    pthread_mutex_lock(&mutex);
    readers--;
    if (readers == 0) {
        pthread_mutex_unlock(&write_lock);  // Last reader unlocks writers
    }
    pthread_mutex_unlock(&mutex);
    
    return NULL;
}

void* writer(void* arg) {
    pthread_mutex_lock(&write_lock);
    
    // Write to shared data
    write_data();
    
    pthread_mutex_unlock(&write_lock);
    return NULL;
}
```

### Dining Philosophers (Deadlock Avoidance)

```c
#define N 5

pthread_mutex_t forks[N];

void* philosopher(void* arg) {
    int id = *(int*)arg;
    int left = id;
    int right = (id + 1) % N;
    
    while (1) {
        think();
        
        // Avoid deadlock: acquire lower-numbered fork first
        if (left < right) {
            pthread_mutex_lock(&forks[left]);
            pthread_mutex_lock(&forks[right]);
        } else {
            pthread_mutex_lock(&forks[right]);
            pthread_mutex_lock(&forks[left]);
        }
        
        eat();
        
        pthread_mutex_unlock(&forks[left]);
        pthread_mutex_unlock(&forks[right]);
    }
    return NULL;
}
```

## Related Topics

- **[Process and Thread](Process%20and%20Thread.md)** - Process and thread fundamentals, lifecycle, and scheduling
- **[Parallel System](Parallel%20System.md)** - Parallel architectures, cache coherence, and scalable OS design
- **[Memory Management](Memory%20Management.md)** - Virtual memory and memory consistency

## References

**Course Materials:**
- CS 6210: Advanced Operating Systems - Georgia Tech OMSCS
- CS 6200: Introduction to Operating Systems - Georgia Tech OMSCS
- COMS W4118: Operating Systems I - Columbia University

