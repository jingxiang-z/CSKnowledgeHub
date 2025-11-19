# Makefile for Operating System Thread Examples
# Compiles examples demonstrating thread synchronization and concurrency patterns

# Compiler and flags
CC = gcc                                    # C compiler
CXX = g++                                   # C++ compiler
CFLAGS = -Wall -Wextra -std=c99 -pthread    # C compiler flags with pthread support
CXXFLAGS = -Wall -Wextra -std=c++11 -pthread # C++ compiler flags with pthread support
LDFLAGS = -pthread                          # Linker flags for pthread

# Build directory
BIN_DIR = bin

# Target executables (with bin directory prefix)
C_TARGETS = $(BIN_DIR)/thread_pool_c \
            $(BIN_DIR)/producer_consumer_c \
            $(BIN_DIR)/reader_writer_c \
            $(BIN_DIR)/boss_worker_c \
            $(BIN_DIR)/pipeline_c

CPP_TARGETS = $(BIN_DIR)/thread_pool_cpp \
              $(BIN_DIR)/producer_consumer_cpp \
              $(BIN_DIR)/reader_writer_cpp \
              $(BIN_DIR)/boss_worker_cpp

ALL_TARGETS = $(C_TARGETS) $(CPP_TARGETS)

# Source files
C_SOURCES = thread_pool.c producer_consumer.c reader_writer.c boss_worker.c pipeline.c
CPP_SOURCES = thread_pool.cpp producer_consumer.cpp reader_writer.cpp boss_worker.cpp

# Default target: build all executables
all: $(ALL_TARGETS)

# Create bin directory if it doesn't exist
$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

# ==================== C Implementations ====================

# Build thread_pool C executable
# Demonstrates thread pool pattern with work queue using POSIX threads
$(BIN_DIR)/thread_pool_c: thread_pool.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build producer_consumer C executable
# Demonstrates producer-consumer pattern with bounded buffer
$(BIN_DIR)/producer_consumer_c: producer_consumer.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build reader_writer C executable
# Demonstrates reader-writer lock pattern
$(BIN_DIR)/reader_writer_c: reader_writer.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build boss_worker C executable
# Demonstrates boss-worker (master-slave) pattern
$(BIN_DIR)/boss_worker_c: boss_worker.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Build pipeline C executable
# Demonstrates pipeline pattern for data processing
$(BIN_DIR)/pipeline_c: pipeline.c | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# ==================== C++ Implementations ====================

# Build thread_pool C++ executable
# Demonstrates thread pool pattern using C++11 threads
$(BIN_DIR)/thread_pool_cpp: thread_pool.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

# Build producer_consumer C++ executable
# Demonstrates producer-consumer pattern using C++11 synchronization
$(BIN_DIR)/producer_consumer_cpp: producer_consumer.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

# Build reader_writer C++ executable
# Demonstrates reader-writer lock pattern using C++11
$(BIN_DIR)/reader_writer_cpp: reader_writer.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

# Build boss_worker C++ executable
# Demonstrates boss-worker pattern using C++11 threads
$(BIN_DIR)/boss_worker_cpp: boss_worker.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

# ==================== Run Targets ====================

# Run all examples (C versions)
run-all-c: $(C_TARGETS)
	@echo "========================================="
	@echo "Running thread_pool (C)..."
	@echo "========================================="
	$(BIN_DIR)/thread_pool_c
	@echo ""

# Run all examples (C++ versions)
run-all-cpp: $(CPP_TARGETS)
	@echo "========================================="
	@echo "Running thread_pool (C++)..."
	@echo "========================================="
	$(BIN_DIR)/thread_pool_cpp
	@echo ""

# Run all C and C++ examples
run-all: run-all-c run-all-cpp

# Individual run targets for C
run-thread-pool-c: $(BIN_DIR)/thread_pool_c
	$(BIN_DIR)/thread_pool_c

run-producer-consumer-c: $(BIN_DIR)/producer_consumer_c
	$(BIN_DIR)/producer_consumer_c

run-reader-writer-c: $(BIN_DIR)/reader_writer_c
	$(BIN_DIR)/reader_writer_c

run-boss-worker-c: $(BIN_DIR)/boss_worker_c
	$(BIN_DIR)/boss_worker_c

run-pipeline-c: $(BIN_DIR)/pipeline_c
	$(BIN_DIR)/pipeline_c

# Individual run targets for C++
run-thread-pool-cpp: $(BIN_DIR)/thread_pool_cpp
	$(BIN_DIR)/thread_pool_cpp

run-producer-consumer-cpp: $(BIN_DIR)/producer_consumer_cpp
	$(BIN_DIR)/producer_consumer_cpp

run-reader-writer-cpp: $(BIN_DIR)/reader_writer_cpp
	$(BIN_DIR)/reader_writer_cpp

run-boss-worker-cpp: $(BIN_DIR)/boss_worker_cpp
	$(BIN_DIR)/boss_worker_cpp

# ==================== Utility Targets ====================

# Clean up compiled executables and temporary files
clean:
	rm -rf $(BIN_DIR) *.o *.out core

# Help target to show available commands
help:
	@echo "Available targets:"
	@echo "  all                    - Build all executables (default) in $(BIN_DIR)/"
	@echo ""
	@echo "Build specific implementations:"
	@echo "  $(BIN_DIR)/thread_pool_c          - Build thread pool (C)"
	@echo "  $(BIN_DIR)/thread_pool_cpp        - Build thread pool (C++)"
	@echo "  $(BIN_DIR)/producer_consumer_c    - Build producer-consumer (C)"
	@echo "  $(BIN_DIR)/producer_consumer_cpp  - Build producer-consumer (C++)"
	@echo "  $(BIN_DIR)/reader_writer_c        - Build reader-writer (C)"
	@echo "  $(BIN_DIR)/reader_writer_cpp      - Build reader-writer (C++)"
	@echo "  $(BIN_DIR)/boss_worker_c          - Build boss-worker (C)"
	@echo "  $(BIN_DIR)/boss_worker_cpp        - Build boss-worker (C++)"
	@echo "  $(BIN_DIR)/pipeline_c             - Build pipeline (C)"
	@echo ""
	@echo "Run examples:"
	@echo "  run-all                - Run all C and C++ examples"
	@echo "  run-all-c              - Run all C examples"
	@echo "  run-all-cpp            - Run all C++ examples"
	@echo "  run-thread-pool-c      - Run thread pool (C)"
	@echo "  run-thread-pool-cpp    - Run thread pool (C++)"
	@echo "  run-producer-consumer-c - Run producer-consumer (C)"
	@echo "  run-producer-consumer-cpp - Run producer-consumer (C++)"
	@echo "  run-reader-writer-c    - Run reader-writer (C)"
	@echo "  run-reader-writer-cpp  - Run reader-writer (C++)"
	@echo "  run-boss-worker-c      - Run boss-worker (C)"
	@echo "  run-boss-worker-cpp    - Run boss-worker (C++)"
	@echo "  run-pipeline-c         - Run pipeline (C)"
	@echo ""
	@echo "Utility:"
	@echo "  clean                  - Remove $(BIN_DIR)/ directory and compiled files"
	@echo "  help                   - Show this help message"

# Phony targets (not actual files)
.PHONY: all clean run-all run-all-c run-all-cpp \
        run-thread-pool-c run-thread-pool-cpp \
        run-producer-consumer-c run-producer-consumer-cpp \
        run-reader-writer-c run-reader-writer-cpp \
        run-boss-worker-c run-boss-worker-cpp \
        run-pipeline-c help

