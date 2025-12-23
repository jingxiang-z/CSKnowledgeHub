/*
 * thread_pool.cpp
 * 
 * Demonstrates a thread pool implementation with a work queue.
 * Shows how to efficiently reuse threads for multiple tasks using C++11 threads.
 * 
 * Compilation: g++ -std=c++11 -o thread_pool thread_pool.cpp -pthread
 * Usage: ./thread_pool
 */

#include <atomic>
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
    // Member variables for thread pool
    std::vector<std::thread> workers;           // Vector of worker threads
    std::queue<std::function<void()>> tasks;    // Task queue (FIFO)
    
    // Synchronization primitives
    std::mutex queue_mutex;                     // Protects shared queue data
    std::condition_variable condition;          // Signals when tasks are available
    std::condition_variable tasks_done;         // Signals when all tasks complete
    
    // Flags
    std::atomic<bool> shutdown;                 // Shutdown flag
    std::atomic<int> active_tasks;              // Count of currently executing tasks
    
public:
    // Constructor: create a thread pool with specified number of threads
    ThreadPool(size_t num_threads) : shutdown(false), active_tasks(0) {
        // Create num_threads worker threads
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this] {
                // Worker thread main loop
                while (true) {
                    std::function<void()> task;
                    
                    {
                        // Wait for a task or shutdown signal
                        std::unique_lock<std::mutex> lock(this->queue_mutex);
                        
                        this->condition.wait(lock, [this] {
                            return this->shutdown || !this->tasks.empty();
                        });
                        
                        // Exit if shutting down and no tasks remain
                        if (this->shutdown && this->tasks.empty()) {
                            return;
                        }
                        
                        // Get task from queue
                        task = std::move(this->tasks.front());
                        this->tasks.pop();
                        ++active_tasks;
                    }
                    
                    // Execute task outside the lock
                    task();
                    
                    // Mark task as completed
                    {
                        std::lock_guard<std::mutex> lock(this->queue_mutex);
                        --active_tasks;
                        if (active_tasks == 0 && tasks.empty()) {
                            tasks_done.notify_all();
                        }
                    }
                }
            });
        }
    }
    
    // Destructor: signal shutdown and wait for all threads to finish
    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            shutdown = true;
        }
        
        // Wake up all threads
        condition.notify_all();
        
        // Join all worker threads
        for (std::thread& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }
    
    // Add a new task to the pool
    template<class F>
    void enqueue(F&& f) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            
            // Don't accept new tasks if stopping
            if (shutdown) {
                throw std::runtime_error("Cannot enqueue on stopped ThreadPool");
            }
            
            // Add task to queue
            tasks.emplace(std::forward<F>(f));
        }
        
        // Notify one waiting worker
        condition.notify_one();
    }
    
    // Wait for all tasks to complete
    void wait() {
        std::unique_lock<std::mutex> lock(queue_mutex);
        tasks_done.wait(lock, [this] {
            return tasks.empty() && active_tasks == 0;
        });
    }
    
    // Delete copy constructor and assignment operator
    ThreadPool(const ThreadPool&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;
};

// Example task function
void task(int id) {
    std::cout << "Task " << id << " executing on thread " 
              << std::this_thread::get_id() << std::endl;
    
    // Simulate some work
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    std::cout << "Task " << id << " completed" << std::endl;
}

int main() {
    std::cout << "=== Thread Pool Example ===\n" << std::endl;
    
    // Create a thread pool with 4 worker threads
    std::cout << "Creating thread pool with 4 worker threads..." << std::endl;
    ThreadPool pool(4);
    std::cout << "Thread pool created successfully\n" << std::endl;
    
    // Submit 10 tasks to the pool
    std::cout << "Submitting 10 tasks to the pool..." << std::endl;
    for (int i = 0; i < 10; ++i) {
        // Use lambda with capture to pass the task id
        pool.enqueue([i] {
            task(i);
        });
    }
    std::cout << "All tasks submitted\n" << std::endl;
    
    // Wait for all tasks to complete
    std::cout << "Waiting for all tasks to complete..." << std::endl;
    pool.wait();
    
    std::cout << "\nAll tasks completed. Thread pool will be destroyed..." << std::endl;
    
    // Pool is automatically destroyed when it goes out of scope
    
    std::cout << "Thread pool destroyed" << std::endl;
    std::cout << "\n=== Program Complete ===" << std::endl;
    
    return 0;
}
