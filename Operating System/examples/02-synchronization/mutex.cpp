/*
 * mutex_example.cpp
 * 
 * Demonstrates C++ mutex usage and RAII-based locking mechanisms.
 * Compares different locking strategies and shows why RAII is important
 * for exception safety and preventing deadlocks.
 * 
 * Key C++ features:
 * - std::mutex for mutual exclusion
 * - std::lock_guard for simple RAII locking
 * - std::unique_lock for flexible locking (can unlock before scope ends)
 * - std::scoped_lock (C++17) for locking multiple mutexes (deadlock prevention)
 * 
 * Compilation: g++ -std=c++17 -o mutex_example mutex_example.cpp -pthread
 * Usage: ./mutex_example
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>

// TODO: Create shared data and mutex:
//   - Shared counter variable
//   - std::mutex counter_mutex

// TODO: Implement example 1: Without mutex (race condition)
//   - Multiple threads increment counter without synchronization
//   - Demonstrates the race condition

// TODO: Implement example 2: With std::lock_guard
//   - Shows RAII-based automatic lock/unlock
//   - Lock is released when lock_guard goes out of scope
//   - Exception safe

// TODO: Implement example 3: With std::unique_lock
//   - Shows manual unlock capability
//   - Useful when you need to unlock before scope ends
//   - Can be moved (unlike lock_guard)

// TODO: Implement example 4: With std::scoped_lock (C++17)
//   - Shows locking multiple mutexes atomically
//   - Prevents deadlock when locking multiple resources
//   - Demonstrate with two resources and two mutexes

int main() {
    std::cout << "Mutex examples - To be implemented\n";
    
    // TODO: Run all examples and compare results
    // TODO: Show counter values with and without synchronization
    
    return 0;
}

