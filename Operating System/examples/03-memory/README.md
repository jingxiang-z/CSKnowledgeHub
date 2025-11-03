# Memory Management Examples

Essential examples demonstrating virtual memory and process memory layout.

## C Examples (Only)

Memory management examples are C-only because they require direct system calls and low-level memory operations that are abstracted away in higher-level languages.

### ⭐⭐⭐ Virtual Memory
- `mmap_example.c` - **ESSENTIAL** - Using mmap() for memory mapping

### ⭐⭐ Memory Layout
- `memory_layout.c` - **Important** - Understanding process memory layout (text, data, heap, stack)

## Compilation & Running

```bash
# Basic compilation
gcc -o mmap_example mmap_example.c

# Run
./mmap_example
```

## Key Concepts Covered

- ✅ Virtual memory with mmap()
- ✅ Memory mapping (file-backed and anonymous)
- ✅ Process memory layout (text, data, heap, stack)
- ✅ Virtual to physical address translation
- ✅ Understanding how OS manages memory

