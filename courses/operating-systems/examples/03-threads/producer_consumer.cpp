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

#include <atomic>
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <chrono>
#include <vector>
#include <random>

const int BUFFER_SIZE = 10;
const int NUM_PRODUCERS = 5;
const int NUM_CONSUMERS = 2;
const int ITEMS_TO_PRODUCE = 20;

// Shared buffer (FIFO queue)
std::queue<int> buffer;
std::mutex buffer_mutex;
std::condition_variable not_full;   // Signals producers when space available
std::condition_variable not_empty;  // Signals consumers when items available

// Global counter for item generation (atomic for thread-safety)
std::atomic<int> item_produce(0);

void producer(int id) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 100000);

    while (true) {
        // Check termination condition and generate unique item ID
        int item = item_produce.fetch_add(1);
        if (item >= ITEMS_TO_PRODUCE) {
            break;
        }

        // Simulate production time (outside critical section)
        std::this_thread::sleep_for(std::chrono::microseconds(dis(gen)));

        // Enter critical section for buffer access
        std::unique_lock<std::mutex> lock(buffer_mutex);

        // Wait while buffer is full
        not_full.wait(lock, [] {
            return buffer.size() < BUFFER_SIZE;
        });

        // Add item to queue (enqueue)
        buffer.push(item);

        std::cout << "Producer " << id << ": Produced item " << item 
                  << " (buffer: " << buffer.size() << "/" << BUFFER_SIZE << ")\n";

        // Notify one waiting consumer
        not_empty.notify_one();

        // Lock automatically released here (RAII)
    }
    std::cout << "Producer " << id << ": Finished\n";
}

void consumer(int id) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 10000);
    int consumed_count = 0;

    while (true) {
        // Enter critical section for buffer access
        std::unique_lock<std::mutex> lock(buffer_mutex);

        // Wait while buffer is empty
        not_empty.wait(lock, [] {
            return !buffer.empty() || item_produce.load() >= ITEMS_TO_PRODUCE;
        });

        // Check if we should exit (production done and buffer empty)
        if (buffer.empty() && item_produce.load() >= ITEMS_TO_PRODUCE) {
            std::cout << "Consumer " << id << ": Finished (consumed " 
                      << consumed_count << " items)\n";
            break;
        }

        // Remove item from queue (dequeue)
        int item = buffer.front();
        buffer.pop();
        consumed_count++;

        std::cout << "Consumer " << id << ": Consumed item " << item 
                  << " (buffer: " << buffer.size() << "/" << BUFFER_SIZE << ")\n";

        // Notify one waiting producer
        not_full.notify_one();

        lock.unlock();  // Explicitly release lock before sleeping

        // Simulate consumption time (outside critical section)
        std::this_thread::sleep_for(std::chrono::microseconds(dis(gen)));
    }
}

int main() {
    std::cout << "=== Producer-Consumer Simulation (C++) ===\n";
    std::cout << "Buffer size: " << BUFFER_SIZE << "\n";
    std::cout << "Producers: " << NUM_PRODUCERS << ", Consumers: " << NUM_CONSUMERS << "\n";
    std::cout << "Items to produce: " << ITEMS_TO_PRODUCE << "\n";
    std::cout << "==========================================\n\n";

    std::vector<std::thread> producers;
    std::vector<std::thread> consumers;

    // Create producer threads
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        producers.emplace_back(producer, i + 1);
    }

    // Create consumer threads
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        consumers.emplace_back(consumer, i + 1);
    }

    // Wait for all producers to finish
    for (auto& t : producers) {
        t.join();
    }

    // Wake all consumers so they can check termination condition
    not_empty.notify_all();

    // Wait for all consumers to finish
    for (auto& t : consumers) {
        t.join();
    }

    std::cout << "\n==========================================\n";
    std::cout << "All threads completed successfully!\n";
    std::cout << "==========================================\n";
    
    return 0;
}

