# Makefile for Operating System Process Examples
# Compiles three example programs demonstrating process management concepts

# Compiler and flags
CC = gcc                          # C compiler
CFLAGS = -Wall -Wextra -std=c99   # Enable warnings and use C99 standard
LDFLAGS =                         # Linker flags (none needed for these examples)

# Target executables
TARGETS = fork_exec wait_example signal_handling

# Source files
SOURCES = fork_exec.c wait_example.c signal_handling.c

# Default target: build all executables
all: $(TARGETS)

# Build fork_exec executable
# Demonstrates process creation with fork() and program execution with exec()
fork_exec: fork_exec.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build wait_example executable
# Demonstrates parent process waiting for child processes using wait() and waitpid()
wait_example: wait_example.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build signal_handling executable
# Demonstrates signal handling with custom signal handlers
signal_handling: signal_handling.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Run all examples in sequence
run-all: all
	@echo "========================================="
	@echo "Running fork_exec example..."
	@echo "========================================="
	./fork_exec
	@echo ""
	@echo "========================================="
	@echo "Running wait_example..."
	@echo "========================================="
	./wait_example
	@echo ""
	@echo "========================================="
	@echo "Running signal_handling (press Ctrl+C to exit)..."
	@echo "========================================="
	@timeout 5 ./signal_handling || true
	@echo ""

# Run individual examples
run-fork: fork_exec
	./fork_exec

run-wait: wait_example
	./wait_example

run-signal: signal_handling
	@echo "Press Ctrl+C to exit..."
	./signal_handling

# Clean up compiled executables and temporary files
clean:
	rm -f $(TARGETS) *.o *.out core

# Help target to show available commands
help:
	@echo "Available targets:"
	@echo "  all          - Build all executables (default)"
	@echo "  fork_exec    - Build only fork_exec example"
	@echo "  wait_example - Build only wait_example example"
	@echo "  signal_handling - Build only signal_handling example"
	@echo "  run-all      - Build and run all examples"
	@echo "  run-fork     - Build and run fork_exec example"
	@echo "  run-wait     - Build and run wait_example example"
	@echo "  run-signal   - Build and run signal_handling example"
	@echo "  clean        - Remove compiled executables"
	@echo "  help         - Show this help message"

# Phony targets (not actual files)
.PHONY: all clean distclean run-all run-fork run-wait run-signal help

