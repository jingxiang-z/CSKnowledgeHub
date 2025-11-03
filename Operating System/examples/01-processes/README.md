# Process Management Examples

Essential examples demonstrating process creation, lifecycle, and signals.

## C Examples

### ⭐⭐⭐ Core Process Operations
- `fork_exec.c` - **ESSENTIAL** - Process creation using fork() and exec()
- `wait_example.c` - **ESSENTIAL** - Parent waiting for child processes and process lifecycle

### ⭐⭐ Signal Handling
- `signal_handling.c` - **Important** - Custom signal handlers and asynchronous events

## Compilation & Running

### C Examples
```bash
# Compile
gcc -o fork_exec fork_exec.c

# Run
./fork_exec
```

### Python Examples
```bash
python3 multiprocessing_basics.py
```

## Key Concepts Covered

- ✅ Process creation with fork()
- ✅ Process replacement with exec() family
- ✅ Parent-child relationships
- ✅ Process termination and exit status (wait/waitpid)
- ✅ Signal generation and handling
- ✅ Process identification (PID, PPID)

