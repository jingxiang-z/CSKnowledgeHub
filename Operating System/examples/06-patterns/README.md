# Concurrent Design Patterns

Essential concurrent programming patterns implemented in C, Go, and Python for comparison.

These patterns solve common concurrency problems and show how different languages approach the same challenges.

## Pattern Overview

| Pattern | Description | Key Concepts |
|---------|-------------|--------------|
| **Boss-Worker** | One boss distributes work to worker threads | Task distribution, work queue |
| **Pipeline** | Data flows through stages of processing | Stream processing, staged computation |
| **Producer-Consumer** | Producers create data, consumers process it | Bounded buffer, coordination |
| **Reader-Writer** | Multiple readers, exclusive writers | Read optimization, write exclusion |

## C Examples

### ⭐⭐⭐ Essential Patterns
- `boss_worker.c` - Boss-worker (master-slave) pattern
- `pipeline.c` - Pipeline pattern with stages
- `producer_consumer.c` - Producer-consumer pattern
- `reader_writer.c` - Reader-writer pattern

## Go Examples

### ⭐⭐⭐ Essential Patterns
- `boss_worker.go` - Boss-worker with goroutines and channels
- `pipeline.go` - Pipeline using channel composition
- `producer_consumer.go` - Producer-consumer with channels
- `reader_writer.go` - Reader-writer with sync.RWMutex

## Python Examples

### ⭐⭐⭐ Essential Patterns
- `boss_worker.py` - Boss-worker with ThreadPoolExecutor
- `pipeline.py` - Pipeline with Queue
- `producer_consumer.py` - Producer-consumer with Queue
- `reader_writer.py` - Reader-writer with threading.Lock

## Compilation & Running

### C Examples
```bash
gcc -o boss_worker boss_worker.c -pthread
./boss_worker
```

### Go Examples
```bash
go run boss_worker.go
```

### Python Examples
```bash
python3 boss_worker.py
```

## Key Concepts Covered

**Design Patterns:**
- ✅ Boss-Worker: Task distribution and load balancing
- ✅ Pipeline: Staged processing and data flow
- ✅ Producer-Consumer: Decoupling production from consumption
- ✅ Reader-Writer: Optimizing for concurrent reads

**Language Comparisons:**
- ✅ **C**: Manual implementation with pthreads, queues, and locks
- ✅ **Go**: Idiomatic goroutines and channels
- ✅ **Python**: High-level threading abstractions

**Practical Applications:**
- ✅ Task processing systems
- ✅ Data transformation pipelines
- ✅ Event processing
- ✅ Caching systems
- ✅ Web servers

## Pattern Selection Guide

**Use Boss-Worker when:**
- You have many independent tasks
- Tasks have varying execution times
- You want load balancing

**Use Pipeline when:**
- Data goes through sequential stages
- Each stage can work independently
- You want to maximize throughput

**Use Producer-Consumer when:**
- Production and consumption rates differ
- You need a buffer between producers and consumers
- Multiple producers or consumers exist

**Use Reader-Writer when:**
- Reads are much more frequent than writes
- You want to maximize read concurrency
- Write operations are infrequent but need exclusivity

