# Operating System Examples

This directory contains **essential** practical code examples demonstrating core operating system concepts. Only the most fundamental examples are included to focus on what truly matters for understanding OS internals.

## Directory Structure

### Core OS Concepts
- **01-processes/** - Process creation, signals, and lifecycle (3 C examples)
- **02-threads/** - Thread basics and thread pools (3 C, 1 Go, 1 Python)
- **03-memory/** - Memory management with mmap (2 C examples)
- **04-synchronization/** - Synchronization primitives (6 C, 1 Go, 1 Python = 8 examples)
- **05-file-system/** - File I/O operations (2 C examples)
- **07-ipc/** - Inter-Process Communication (7 C, 2 Python = 9 examples)

### Practical Patterns
- **06-patterns/** - Concurrent design patterns (4 C, 4 Go, 4 Python)

**Total: 40 focused examples (27 C, 6 Go, 9 Python)**

**Philosophy:** Focus on fundamental concepts that every OS student must understand, with practical design patterns to see how these concepts are used in real applications.

## Language Guide

### C Examples (Primary)
C examples focus on low-level system calls and direct OS interaction. These are **essential** for understanding how operating systems actually work. All core concepts are demonstrated in C.

**Requirements:**
- GCC or Clang compiler
- POSIX-compliant system (Linux, macOS, Unix)
- Standard C library

**Compilation:**
```bash
gcc -o output_name source_file.c -pthread
```

### Go Examples (Modern Patterns)
Go examples demonstrate modern concurrency patterns that complement C's low-level approach. Go's goroutines and channels provide an elegant view of concurrent programming.

**Requirements:**
- Go 1.16 or later

**Running:**
```bash
go run example.go
```

### Python Examples (High-Level View)
Python examples show high-level abstractions built on top of OS primitives. Particularly valuable for comparing design patterns - showing how the same pattern looks in a high-level vs. low-level language.

**Requirements:**
- Python 3.7 or later

**Running:**
```bash
python3 example.py
```

## Why This Structure?

### Focus on Fundamentals First
Before learning advanced topics, you must understand:
- How processes work (fork, exec, wait, signals)
- How processes communicate (pipes, shared memory, message queues)
- How memory works (virtual memory, mmap)
- How files work (file descriptors, system calls)
- How threads work (creation, synchronization)

### Then Learn Patterns
Once you understand the primitives, you can see how they combine into real-world patterns. The **06-patterns/** section shows the same patterns in all three languages:

- **C** → Understand the mechanics (manual locks, queues, threads)
- **Go** → See modern idioms (goroutines, channels)
- **Python** → Appreciate high-level abstractions (ThreadPoolExecutor, Queue)

This comparison is invaluable for understanding:
- What's essential vs. language-specific
- Trade-offs between control and convenience
- Why certain languages excel at certain tasks

## Safety Notes

⚠️ **Warning:** Some examples demonstrate low-level operations that can crash programs or consume system resources. Run examples in isolated environments or containers when appropriate.

## Learning Path (Recommended Order)

### Phase 1: Core OS Primitives (C Fundamentals)
**Goal:** Understand how operating systems really work

1. **Processes** (`01-processes/`)
   - `fork_exec.c` - How processes are created
   - `wait_example.c` - Process lifecycle and waiting
   - `signal_handling.c` - Asynchronous event handling

2. **Memory** (`03-memory/`)
   - `mmap_example.c` - Virtual memory and memory mapping
   - `memory_layout.c` - Understanding process memory layout

3. **File System** (`05-file-system/`)
   - `file_operations.c` - Basic file I/O with system calls
   - `directory_traversal.c` - Working with directories

4. **Inter-Process Communication** (`07-ipc/`)
   - `pipe_example.c` - Anonymous pipes (parent-child)
   - `named_pipe.c` - Named pipes (FIFOs)
   - `shm_posix.c` - POSIX shared memory (fastest IPC)
   - `mq_posix.c` - POSIX message queues
   - Optional: `shm_sysv.c`, `mq_sysv.c` (System V alternatives)
   - Advanced: `unix_socket.c` (bidirectional local IPC)

### Phase 2: Concurrency Fundamentals
**Goal:** Understand threads and synchronization

5. **Thread Basics** (`02-threads/`)
   - Start: `pthread_basics.c` (C threading fundamentals)
   - Compare: `thread_pool.go`, `thread_pool.py` (modern approaches)
   - Understand: `thread_safety.c` (why synchronization matters)

6. **Synchronization Primitives** (`04-synchronization/`)
   - Learn in order:
     - `mutex_example.c` → Basic mutual exclusion
     - `condition_variable.c` → Efficient waiting
     - `semaphore_example.c` → Counting and signaling
     - `rwlock_example.c` → Read-heavy optimization
     - `barrier_example.c` → Multi-thread coordination
     - `producer_consumer.c` → Putting it all together
   - Compare: `producer_consumer_channels.go` (Go's approach)

### Phase 3: Practical Design Patterns
**Goal:** See how primitives combine into real patterns

7. **Design Patterns** (`06-patterns/`)
   - Study each pattern in all 3 languages:
     - **Boss-Worker** → Task distribution and load balancing
     - **Pipeline** → Staged data processing
     - **Producer-Consumer** → Decoupling production/consumption
     - **Reader-Writer** → Optimizing concurrent reads
   - Compare implementations to understand trade-offs

## Additional Resources

- See main documentation in `../` for theoretical background
- Each subdirectory contains its own README with specific examples
- Code examples are heavily commented for educational purposes

