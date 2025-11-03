# Synchronization Examples

Essential examples demonstrating synchronization primitives in progressive order, from basic to advanced.

## C Examples (POSIX)

### ⭐⭐⭐ Basic Synchronization (Start Here)
- `mutex_example.c` - **ESSENTIAL** - Mutex (mutual exclusion) - the foundation
- `condition_variable.c` - **ESSENTIAL** - Condition variables - waiting for conditions
- `semaphore_example.c` - **ESSENTIAL** - Semaphores (binary and counting)

### ⭐⭐ Advanced Primitives
- `rwlock_example.c` - **Important** - Reader-writer locks - multiple readers, single writer
- `barrier_example.c` - **Important** - Barrier synchronization - coordinating multiple threads

### ⭐⭐⭐ Classic Problem
- `producer_consumer.c` - **ESSENTIAL** - Producer-consumer problem (combines multiple primitives)

## Go Examples

### ⭐⭐ Modern Synchronization
- `producer_consumer_channels.go` - **Important** - Producer-consumer using channels (Go idiom)

## Python Examples

### ⭐⭐ Basic Synchronization
- `locks_example.py` - **Important** - Locks and basic thread synchronization in Python

## Compilation & Running

### C Examples
```bash
gcc -o mutex_example mutex_example.c -pthread
./mutex_example
```

### Go Examples
```bash
go run mutex_channels.go
```

### Python Examples
```bash
python3 locks_basics.py
```

## Key Concepts Covered

**Fundamental Primitives:**
- ✅ **Mutexes** - Basic mutual exclusion (lock/unlock)
- ✅ **Condition Variables** - Waiting for conditions to become true
- ✅ **Semaphores** - Counting resources (binary and counting variants)
- ✅ **Reader-Writer Locks** - Optimizing for read-heavy workloads
- ✅ **Barriers** - Synchronizing multiple threads at a point

**Advanced Concepts:**
- ✅ Producer-consumer problem (classic synchronization pattern)
- ✅ When to use each primitive
- ✅ Performance implications of different approaches
- ✅ Modern alternatives (Go channels vs. traditional locks)

## Learning Order

**Recommended progression:**
1. Start with `mutex_example.c` - understand basic locking
2. Move to `condition_variable.c` - learn how to wait efficiently
3. Study `semaphore_example.c` - understand counting and signaling
4. Explore `rwlock_example.c` - optimize for read-heavy scenarios
5. Practice `barrier_example.c` - coordinate multiple threads
6. Synthesize with `producer_consumer.c` - see primitives work together
7. Compare with `producer_consumer_channels.go` - modern approach

