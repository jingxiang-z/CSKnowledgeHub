# Inter-Process Communication (IPC) Examples

Essential examples demonstrating various IPC mechanisms for communication between processes.

## C Examples

### ⭐⭐⭐ Pipes
- `pipe_example.c` - **ESSENTIAL** - Anonymous pipes for parent-child communication
- `named_pipe.c` - **ESSENTIAL** - Named pipes (FIFOs) for unrelated processes

### ⭐⭐⭐ Shared Memory
- `shm_posix.c` - **ESSENTIAL** - POSIX shared memory (shm_open/mmap)
- `shm_sysv.c` - **Important** - System V shared memory (shmget/shmat)

### ⭐⭐⭐ Message Queues
- `mq_posix.c` - **ESSENTIAL** - POSIX message queues
- `mq_sysv.c` - **Important** - System V message queues

### ⭐⭐ Unix Domain Sockets
- `unix_socket.c` - **Important** - Unix domain sockets for local IPC

## Python Examples

### ⭐⭐ High-Level IPC
- `multiprocessing_ipc.py` - **Important** - Pipes and queues via multiprocessing module
- `shared_memory.py` - **Important** - Shared memory in Python 3.8+

## Compilation & Running

### C Examples
```bash
# Compile
gcc -o pipe_example pipe_example.c

# For real-time extensions (POSIX message queues)
gcc -o mq_posix mq_posix.c -lrt

# Run
./pipe_example
```

### Python Examples
```bash
python3 multiprocessing_ipc.py
```

## Key Concepts Covered

**IPC Mechanisms:**
- ✅ **Pipes** - Unidirectional byte streams (anonymous and named)
- ✅ **Shared Memory** - Fastest IPC via shared address space (POSIX and SysV)
- ✅ **Message Queues** - Structured message passing (POSIX and SysV)
- ✅ **Unix Domain Sockets** - Bidirectional local communication

**Important Concepts:**
- ✅ When to use each IPC mechanism
- ✅ Synchronization with IPC (shared memory needs external sync)
- ✅ Performance trade-offs
- ✅ POSIX vs. System V IPC APIs

## IPC Mechanism Comparison

| Mechanism | Bidirectional | Structured Data | Synchronization | Speed | Use Case |
|-----------|--------------|-----------------|-----------------|-------|----------|
| **Pipe** | No (one-way) | No (byte stream) | Built-in | Fast | Parent-child, simple data |
| **Named Pipe** | No (but can use 2) | No (byte stream) | Built-in | Fast | Unrelated processes |
| **Shared Memory** | N/A | Yes (any structure) | **Manual required** | **Fastest** | High-volume data sharing |
| **Message Queue** | Yes | Yes (typed messages) | Built-in | Medium | Structured messages |
| **Unix Socket** | Yes | No (byte stream) | Built-in | Medium | Complex bidirectional |

## Learning Order

**Recommended progression:**
1. Start with `pipe_example.c` - simplest IPC, parent-child only
2. Move to `named_pipe.c` - understand FIFOs for unrelated processes
3. Study `shm_posix.c` - fastest IPC, but requires synchronization
4. Learn `mq_posix.c` - structured message passing
5. Compare `shm_sysv.c` and `mq_sysv.c` - older System V API
6. Advanced: `unix_socket.c` - most flexible local IPC

## POSIX vs System V IPC

**POSIX IPC (Modern, Recommended):**
- Uses file-like interface (open, close, unlink)
- Better integration with standard I/O
- More portable across modern Unix systems
- Examples: `shm_posix.c`, `mq_posix.c`

**System V IPC (Legacy, Still Common):**
- Uses key-based identification (ftok)
- Requires explicit cleanup (ipcs/ipcrm commands)
- More complex API
- Still widely used in production systems
- Examples: `shm_sysv.c`, `mq_sysv.c`

## Synchronization with IPC

⚠️ **Critical:** Shared memory does NOT include synchronization!
- Must use semaphores, mutexes, or other primitives
- See `04-synchronization/` for synchronization examples
- Message queues and pipes have built-in synchronization

## Performance Considerations

**Speed (Fastest to Slowest):**
1. Shared Memory (no data copying, direct access)
2. Pipes (one copy through kernel)
3. Unix Domain Sockets (similar to pipes)
4. Message Queues (may involve more copying and structure overhead)

**Use shared memory when:**
- High-volume data transfer
- Multiple readers/writers
- You can handle synchronization

**Use pipes when:**
- Simple parent-child communication
- Streaming data
- Don't need random access

**Use message queues when:**
- Need structured messages
- Priority-based message handling
- Multiple independent message types

## Cleanup Commands

```bash
# List System V IPC resources
ipcs

# Remove shared memory segment
ipcrm -m <shmid>

# Remove message queue
ipcrm -q <msgid>

# Remove POSIX shared memory
rm /dev/shm/my_shm_name

# List POSIX message queues
ls /dev/mqueue/
```

## Common Pitfalls

1. **Forgetting to unlink POSIX objects** - causes resource leaks
2. **Not synchronizing shared memory** - leads to race conditions
3. **Ignoring error handling** - IPC calls can fail in many ways
4. **Mixing POSIX and System V** - use consistent API within a program
5. **Not setting proper permissions** - can cause access denied errors


