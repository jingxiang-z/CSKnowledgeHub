# Makefile for Operating System Process Examples
# Compiles three example programs demonstrating process management concepts

# Compiler and flags
CC = gcc                          # C compiler
CFLAGS = -Wall -Wextra -std=c99   # Enable warnings and use C99 standard
LDFLAGS =                         # Linker flags (none needed for these examples)

# Build directory
BIN_DIR = bin

# Target executables (with bin directory prefix)
TARGETS = $(BIN_DIR)/fork_exec $(BIN_DIR)/wait_example $(BIN_DIR)/signal_handling

# Source files
SOURCES = fork_exec.c wait_example.c signal_handling.c

# Default target: build all executables
all: $(TARGETS)

# Create bin directory if it doesn't exist
$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

# Build fork_exec executable
# Demonstrates process creation with fork() and program execution with exec()
$(BIN_DIR)/fork_exec: fork_exec.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build wait_example executable
# Demonstrates parent process waiting for child processes using wait() and waitpid()
$(BIN_DIR)/wait_example: wait_example.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build signal_handling executable
# Demonstrates signal handling with custom signal handlers
$(BIN_DIR)/signal_handling: signal_handling.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Run all examples in sequence
run-all: all
	@echo "========================================="
	@echo "Running fork_exec example..."
	@echo "========================================="
	$(BIN_DIR)/fork_exec
	@echo ""
	@echo "========================================="
	@echo "Running wait_example..."
	@echo "========================================="
	$(BIN_DIR)/wait_example
	@echo ""
	@echo "========================================="
	@echo "Running signal_handling (press Ctrl+C to exit)..."
	@echo "========================================="
	@timeout 5 $(BIN_DIR)/signal_handling || true
	@echo ""

# Run individual examples
run-fork: $(BIN_DIR)/fork_exec
	$(BIN_DIR)/fork_exec

run-wait: $(BIN_DIR)/wait_example
	$(BIN_DIR)/wait_example

run-signal: $(BIN_DIR)/signal_handling
	@echo "Press Ctrl+C to exit..."
	$(BIN_DIR)/signal_handling

# Clean up compiled executables and temporary files
clean:
	rm -rf $(BIN_DIR) *.o *.out core

# Help target to show available commands
help:
	@echo "Available targets:"
	@echo "  all          - Build all executables (default) in $(BIN_DIR)/"
	@echo "  run-all      - Build and run all examples"
	@echo "  run-fork     - Build and run fork_exec example"
	@echo "  run-wait     - Build and run wait_example example"
	@echo "  run-signal   - Build and run signal_handling example"
	@echo "  clean        - Remove $(BIN_DIR)/ directory and compiled files"
	@echo "  help         - Show this help message"

# Phony targets (not actual files)
.PHONY: all clean distclean run-all run-fork run-wait run-signal help

