# Thread Management Examples

Essential examples demonstrating threading fundamentals and the practical thread pool pattern.

## C Examples (POSIX Threads)

### ⭐⭐⭐ Threading Fundamentals
- `pthread_basics.c` - **ESSENTIAL** - Creating and joining threads
- `thread_safety.c` - **ESSENTIAL** - Thread-safe programming and race conditions

### ⭐⭐ Thread Pool Pattern
- `thread_pool.c` - **Important** - Thread pool with work queue (manual implementation)

## Go Examples (Goroutines)

### ⭐⭐ Thread Pool Pattern
- `thread_pool.go` - **Important** - Thread pool pattern with goroutines and channels

## Python Examples

### ⭐⭐ Thread Pool Pattern
- `thread_pool.py` - **Important** - ThreadPoolExecutor (high-level abstraction)

## Compilation & Running

### C Examples
```bash
gcc -o pthread_basics pthread_basics.c -pthread
./pthread_basics
```

### Go Examples
```bash
go run thread_pool.go
```

### Python Examples
```bash
python3 thread_pool.py
```

## Key Concepts Covered

- ✅ Thread creation and termination (pthread_create, pthread_join)
- ✅ Thread safety and race conditions
- ✅ Why synchronization is necessary (see 04-synchronization for solutions)
- ✅ Thread pool pattern (reusing threads for multiple tasks)
- ✅ Work queue implementation
- ✅ Comparing thread pool approaches across languages:
  - **C**: Manual implementation with pthreads and work queue
  - **Go**: Idiomatic goroutine pool with channels
  - **Python**: High-level ThreadPoolExecutor

