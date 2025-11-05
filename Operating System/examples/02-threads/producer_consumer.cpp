/*
 * producer_consumer.cpp
 * 
 * Demonstrates the producer-consumer pattern using C++11 threading primitives.
 * Shows how to use std::mutex, std::condition_variable, and std::queue
 * for thread-safe communication between producer and consumer threads.
 * 
 * Key C++ features:
 * - std::mutex for mutual exclusion
 * - std::condition_variable for signaling
 * - std::unique_lock for flexible locking with RAII
 * - std::queue<T> for type-safe buffer
 * - std::thread for thread management
 * 
 * Compilation: g++ -std=c++11 -o producer_consumer producer_consumer.cpp -pthread
 * Usage: ./producer_consumer
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <chrono>

// TODO: Define a bounded buffer size (e.g., const int BUFFER_SIZE = 10)

// TODO: Create shared data structures:
//   - std::queue<int> buffer
//   - std::mutex buffer_mutex
//   - std::condition_variable not_full
//   - std::condition_variable not_empty

// TODO: Implement producer function
//   - Takes producer ID and number of items to produce
//   - Locks mutex, checks if buffer is full (wait on not_full)
//   - Adds item to queue
//   - Notifies consumers via not_empty

// TODO: Implement consumer function
//   - Takes consumer ID and number of items to consume
//   - Locks mutex, checks if buffer is empty (wait on not_empty)
//   - Removes item from queue
//   - Notifies producers via not_full

int main() {
    std::cout << "Producer-consumer pattern - To be implemented\n";
    
    // TODO: Create producer and consumer threads
    // TODO: Join all threads
    
    return 0;
}

