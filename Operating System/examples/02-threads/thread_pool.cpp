/*
 * thread_pool.cpp
 * 
 * Demonstrates a thread pool implementation with a work queue.
 * Shows how to efficiently reuse threads for multiple tasks using C++11 threads.
 * 
 * Compilation: g++ -std=c++11 -o thread_pool thread_pool.cpp -pthread
 * Usage: ./thread_pool
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <functional>
#include <vector>
#include <chrono>

class ThreadPool {
private:
    // TODO: Add member variables for thread pool
    // - vector of worker threads
    // - task queue
    // - synchronization primitives (mutex, condition variable)
    // - stop flag
    
public:
    // Constructor: create a thread pool with specified number of threads
    ThreadPool(size_t num_threads) {
        // TODO: Initialize worker threads
    }
    
    // Add a new task to the pool
    template<class F>
    void enqueue(F&& f) {
        // TODO: Add task to queue and notify a worker
    }
    
    // Destructor: wait for all threads to finish
    ~ThreadPool() {
        // TODO: Signal threads to stop and join them
    }
};

int main() {
    std::cout << "Thread pool example - To be implemented\n";
    
    // TODO: Create thread pool and enqueue tasks
    
    return 0;
}
