/*
 * reader_writer.cpp
 * 
 * Demonstrates the reader-writer pattern using C++17 shared_mutex.
 * Shows how multiple readers can access data concurrently while
 * writers get exclusive access.
 * 
 * Key C++ features:
 * - std::shared_mutex (C++17) for reader-writer semantics
 * - std::shared_lock for shared (read) access
 * - std::unique_lock for exclusive (write) access
 * - RAII ensures locks are automatically released
 * 
 * Compilation: g++ -std=c++17 -o reader_writer reader_writer.cpp -pthread
 * Usage: ./reader_writer
 */

#include <iostream>
#include <thread>
#include <shared_mutex>
#include <mutex>
#include <vector>
#include <chrono>

// TODO: Create shared data structure:
//   - Shared resource (e.g., int shared_data or std::vector<int>)
//   - std::shared_mutex rw_mutex

// TODO: Implement reader function
//   - Takes reader ID
//   - Acquires shared lock: std::shared_lock<std::shared_mutex> lock(rw_mutex)
//   - Reads shared data
//   - Multiple readers can hold shared locks simultaneously

// TODO: Implement writer function
//   - Takes writer ID
//   - Acquires exclusive lock: std::unique_lock<std::shared_mutex> lock(rw_mutex)
//   - Modifies shared data
//   - Only one writer can hold exclusive lock at a time
//   - No readers allowed while writer has lock

int main() {
    std::cout << "Reader-writer pattern - To be implemented\n";
    
    // TODO: Create multiple reader threads and writer threads
    // TODO: Join all threads
    
    return 0;
}

